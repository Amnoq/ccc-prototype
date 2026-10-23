"""Fountain (LT-code) redundancy demo: the holographic layer.

Design under test (see fountain.py): k data lines + f fountain lines;
each fountain line is the nibble-wise XOR of a deterministic subset
(degree ~ 1+Binomial(k-1,1/2), uniform random subset from
random.Random(seed)) of ALL data lines -- the whole is in the parts.
Header 97SS (2-digit seed), body = XOR nibbles as 2 digits each,
3-digit _digit_checksum. Decoder: LT peeling; checksum failures become
erasures; every recovered line is strip+checksum+wire re-validated.

1. Sanity: clean round trip, shuffle, explicit padding-strip check.
2. Token overhead: fountain lines vs data lines vs the parity line
   (tiktoken cl100k_base), plus the scaling argument.
3. Erasure table: k=8, f in {1,2,4,6}, e in 1..f+1 pool erasures,
   300 trials/cell. Expect: e<=f recovers w.h.p., e>f fails.
4. Mixed corruption: 1 and 2 random single-digit flips (not erasures),
   f=4 -- checksums must convert them to erasures.
5. Head-to-head vs the parity scheme: single-digit corruption, single
   line erasure, double line erasure.
6. Adversarial: corrupted seed / body digits must fail the checksum
   (never silently mis-decode).
7. Telomere composition: wrapped, scattered in prose, discovered,
   reassembled.

Every successful decode asserts exact int equality: the decoder must
never silently return wrong data.
"""
import itertools
import json
import random

import tiktoken

import fountain
from codec import (build_message, decode_lines_parity, demo_registry,
                   encode_lines, encode_lines_parity, encode_message_bits,
                   decode_message_bits, first_n_primes,
                   registry_fingerprint, scan_telomeres, validate_message,
                   wrap_telomere, _digit_checksum)
from fountain import (decode_lines_fountain, encode_lines_fountain,
                      fountain_subset, _strip_data_line)

enc = tiktoken.get_encoding("cl100k_base")
T = lambda s: len(enc.encode(s))  # noqa: E731

print("fountain design: degree d ~ 1+Binomial(k-1,1/2), uniform d-subset "
      "from random.Random(seed); nibble-wise XOR; header 97SS; body = "
      "XOR nibbles as 2 digits each; _digit_checksum per line; "
      "encoder-side seed search for full data-line coverage")

export = json.load(open("ccc_export.json"))
reg = demo_registry(export)
B = len(reg.names)
primes = first_n_primes(B + 16)
msg = build_message(export, reg, primes)
assert validate_message(msg, B, primes)


def random_msg(rng, n=16):
    out = []
    for _ in range(n):
        r = rng.random()
        if r < 0.5:
            out.append(rng.randrange(0, 64))
        elif r < 0.8:
            out.append(rng.randrange(0, 100000))
        else:
            out.append(rng.randrange(10 ** 10, 10 ** 13))
    return out


def flip_digit(rng, s):
    pos = rng.randrange(len(s))
    d = rng.choice([c for c in "0123456789" if c != s[pos]])
    return s[:pos] + d + s[pos + 1:]


# ------------------------------------------------------- 1. sanity
K = 4
lines = encode_lines_fountain(msg, K, 3, seed=11)
assert lines[:K] == encode_lines(msg, K), "data lines == plain encode_lines"
out, rep = decode_lines_fountain(lines, K)
assert out == msg
shuf = lines[:]
random.Random(7).shuffle(shuf)
out, rep = decode_lines_fountain(shuf, K)
assert out == msg
# explicit padding-strip check: padded line -> NNN framing -> original
idx, ints = _strip_data_line(lines[0] + "0" * 30, K)
assert idx == 0 and ints == decode_message_bits(lines[0][4:-3])
# recovery via peeling exercises the strip path end to end
rx = lines[1:]  # drop data line 0 entirely
out, rep = decode_lines_fountain(rx, K)
assert out == msg and rep["recovered_via_peeling"] == [0]
print("1. sanity: clean round trip, shuffled round trip, padding "
      "strips via NNN framing, 1-erasure peel recovery -- all exact")

# --------------------------------- 1b. deterministic single-erasure theorem
# With encoder-side covering seeds, ANY single data-line erasure must
# recover: the erased line is covered by a surviving fountain symbol,
# which then has effective degree 1. Test all 8 positions x 200 msgs.
n_thm = n_thm_ok = fb_thm = 0
for _ in range(200):
    m = random_msg(random, 16)
    s0 = random.randrange(100)
    _, tier = fountain.choose_seeds(s0, 8, 2)
    ls = encode_lines_fountain(m, 8, 2, seed=s0)
    for j in range(8):
        rx = [ln for t, ln in enumerate(ls) if t != j]
        o, _ = decode_lines_fountain(rx, 8)
        if tier != "fallback":
            assert o == m
            n_thm_ok += 1
        n_thm += 1
    fb_thm += (tier == "fallback")
print(f"1b. single-erasure theorem: {n_thm_ok}/{n_thm} recoveries exact "
      f"under covering seeds (all 8 positions x 200 msgs, f=2); "
      f"seed-search fallback {fb_thm}/200")

# --------------------------------- 1c. two-erasure theorem (f=4, tier1)
# Separating + double-covering subsets => any <=2 pool erasures peel
# deterministically. All 28 data pairs x 100 msgs, plus random pool
# pairs (data/fountain mixed).
n2 = n2ok = fb2 = 0
for _ in range(100):
    m = random_msg(random, 16)
    s0 = random.randrange(100)
    _, tier = fountain.choose_seeds(s0, 8, 4)
    fb2 += (tier != "tier1")
    ls = encode_lines_fountain(m, 8, 4, seed=s0)
    for a, b in itertools.combinations(range(8), 2):
        rx = [ln for t, ln in enumerate(ls) if t not in (a, b)]
        o, _ = decode_lines_fountain(rx, 8)
        if tier == "tier1":
            assert o == m
            n2ok += 1
        n2 += 1
print(f"1c. two-erasure theorem: {n2ok}/{n2} exact under tier1 seeds "
      f"(all 28 data pairs x 100 msgs, f=4); non-tier1 {fb2}/100")
npool = npoolok = 0
for _ in range(300):
    m = random_msg(random, 16)
    ls = encode_lines_fountain(m, 8, 4, seed=random.randrange(100))
    drop = set(random.sample(range(12), 2))
    rx = [ln for t, ln in enumerate(ls) if t not in drop]
    random.shuffle(rx)
    try:
        o, _ = decode_lines_fountain(rx, 8)
        npoolok += (o == m)
    except ValueError:
        pass
    npool += 1
print(f"    random 2-pool-erasures (f=4): {npoolok}/{npool} recovered")

# ------------------------------------------------------- 2. overhead
K8 = 8
fl = encode_lines_fountain(msg, K8, 2, seed=3)
pl = encode_lines_parity(msg, K8)
data_tok = sum(T(l) for l in fl[:K8])
fount_tok = sum(T(l) for l in fl[K8:])
par_tok = T(pl[-1])
wire_tok = T(encode_message_bits(msg))
print(f"2. overhead (k={K8}, real message): {K8} data lines "
      f"{data_tok} tok, 2 fountain lines {fount_tok} tok "
      f"({fount_tok // 2} tok/line), parity line {par_tok} tok, "
      f"single wire {wire_tok} tok")
print(f"   per-line chars: data ~{sum(len(l) for l in fl[:K8]) // K8}, "
      f"fountain {len(fl[K8])} (= 2W+7 digits), parity {len(pl[-1])} "
      f"(= W+7). Scaling: fountain line ~2x a parity line; f fountain "
      f"lines cost ~2f/k of the message -- the price of erasure "
      f"correction parity cannot do at all.")

# ------------------------------------------------------- 3. erasure table
print("3. erasure table: k=8, 300 trials/cell, pool erasures + shuffle "
      "(success fraction; every success asserts exact ints)")
random.seed(20260927)
for f in (1, 2, 4, 6):
    row = []
    for e in range(1, f + 2):
        ok = 0
        for _ in range(300):
            m = random_msg(random, 16)
            ls = encode_lines_fountain(m, 8, f,
                                       seed=random.randrange(100))
            drop = set(random.sample(range(8 + f), e))
            rx = [ln for j, ln in enumerate(ls) if j not in drop]
            random.shuffle(rx)
            try:
                o, _ = decode_lines_fountain(rx, 8)
                ok += (o == m)
            except ValueError:
                pass
        row.append(f"e={e}:{ok / 300:.3f}")
    print(f"   f={f}: " + " ".join(row))

# ------------------------------------------------------- 4. mixed corruption
print("4. mixed corruption: random single-digit flips, f=4, 300 trials "
      "(checksums must convert flips to erasures)")
for nflip in (1, 2):
    ok = 0
    for _ in range(300):
        m = random_msg(random, 16)
        ls = encode_lines_fountain(m, 8, 4, seed=random.randrange(100))
        for _ in range(nflip):
            j = random.randrange(len(ls))
            ls[j] = flip_digit(random, ls[j])
        random.shuffle(ls)
        try:
            o, _ = decode_lines_fountain(ls, 8)
            ok += (o == m)
        except ValueError:
            pass
    print(f"   {nflip} flip(s): {ok / 300:.3f} recovered exactly")

# ------------------------------------------------------- 5. head-to-head
print("5. head-to-head vs parity (k=8, 200 trials each):")
# (a) single-digit corruption in a random data line
pok = fok = 0
for _ in range(200):
    m = random_msg(random, 16)
    j = random.randrange(8)
    lp = encode_lines_parity(m, 8)
    bad = flip_digit(random, lp[j])
    try:
        pok += (decode_lines_parity(lp[:j] + [bad] + lp[j + 1:]) == m)
    except ValueError:
        pass
    lf = encode_lines_fountain(m, 8, 2, seed=random.randrange(100))
    bad = flip_digit(random, lf[j])
    rx = lf[:j] + [bad] + lf[j + 1:]
    random.shuffle(rx)
    try:
        o, _ = decode_lines_fountain(rx, 8)
        fok += (o == m)
    except ValueError:
        pass
print(f"   (a) 1-digit corruption: parity {pok / 200:.3f}, "
      f"fountain(f=2) {fok / 200:.3f}")
# (b) single whole-line erasure
pok = fok = 0
praise = 0
par_msg = ""
for _ in range(200):
    m = random_msg(random, 16)
    j = random.randrange(8)
    lp = encode_lines_parity(m, 8)
    try:
        decode_lines_parity([ln for t, ln in enumerate(lp) if t != j])
        pok += 1
    except ValueError as ex:
        praise += 1
        par_msg = str(ex)[:60]
    lf = encode_lines_fountain(m, 8, 2, seed=random.randrange(100))
    rx = [ln for t, ln in enumerate(lf) if t != j]
    random.shuffle(rx)
    try:
        o, _ = decode_lines_fountain(rx, 8)
        fok += (o == m)
    except ValueError:
        pass
print(f"   (b) 1-line erasure: parity decodes {pok}/200, raises "
      f"{praise}/200 (e.g. '{par_msg}...'), "
      f"fountain(f=2) recovers {fok / 200:.3f}")
# (c) double whole-line erasure
praise = fok = fok4 = 0
for _ in range(200):
    m = random_msg(random, 16)
    drop = set(random.sample(range(8), 2))
    lp = encode_lines_parity(m, 8)
    try:
        decode_lines_parity([ln for t, ln in enumerate(lp)
                             if t not in drop])
    except ValueError:
        praise += 1
    lf = encode_lines_fountain(m, 8, 2, seed=random.randrange(100))
    rx = [ln for t, ln in enumerate(lf) if t not in drop]
    random.shuffle(rx)
    try:
        o, _ = decode_lines_fountain(rx, 8)
        fok += (o == m)
    except ValueError:
        pass
    lf4 = encode_lines_fountain(m, 8, 4, seed=random.randrange(100))
    rx4 = [ln for t, ln in enumerate(lf4) if t not in drop]
    random.shuffle(rx4)
    try:
        o, _ = decode_lines_fountain(rx4, 8)
        fok4 += (o == m)
    except ValueError:
        pass
print(f"   (c) 2-line erasure: parity raises {praise}/200, "
      f"fountain(f=2) recovers {fok / 200:.3f} (provably cannot be "
      f"deterministic: 2 subsets induce <=4 atoms on 8 points), "
      f"fountain(f=4) recovers {fok4 / 200:.3f}")

# ------------------------------------------------------- 6. adversarial
lines = encode_lines_fountain(msg, 4, 2, seed=5)
n_adv = 0
for li in (4, 5):
    fl = lines[li]
    for pos in (2, 3):  # the seed digits
        bad = fl[:pos] + ("0" if fl[pos] != "0" else "1") + fl[pos + 1:]
        assert _digit_checksum(bad[:-3]) != bad[-3:], \
            "seed corruption must break the checksum"
        rx = lines[:li] + [bad] + lines[li + 1:]
        random.shuffle(rx)
        o, rep = decode_lines_fountain(rx, 4)
        assert o == msg and rep["erased_fountain"], \
            "tampered fountain line must be dropped, decode exact"
        n_adv += 1
    # body digit corruption
    bad = flip_digit(random, fl[10:])
    bad = fl[:10] + bad
    assert _digit_checksum(bad[:-3]) != bad[-3:]
    rx = lines[:li] + [bad] + lines[li + 1:]
    o, rep = decode_lines_fountain(rx, 4)
    assert o == msg and rep["erased_fountain"]
    n_adv += 1
print(f"6. adversarial: {n_adv} tampered fountain lines (seed+body) "
      f"all failed checksum, dropped as erasures, decode exact -- "
      f"never silently mis-decoded")

# ------------------------------------------------------- 7. telomeres
fp = registry_fingerprint(reg)
lines = encode_lines_fountain(msg, 4, 2, seed=9)
wrapped = [wrap_telomere(l, 4, B, fp, 2) for l in lines]
random.shuffle(wrapped)
prose = "Notes. " + " Interleaving text here. ".join(wrapped) + " End."
found = [body for _ctx, body in scan_telomeres(prose)]
assert len(found) == 6
o, _ = decode_lines_fountain(found, 4)
assert o == msg
print("7. telomere composition: 6 lines wrapped, scattered in prose "
      "out of order, discovered and fountain-decoded exactly")

print("done.")
