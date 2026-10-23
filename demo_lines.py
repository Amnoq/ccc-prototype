"""Multi-line transport demo.

1. Overhead: k self-describing lines vs the single wire.
2. Order independence: reversed / shuffled lines reassemble exactly.
3. Parallel decode: lines decoded concurrently (independent code path,
   no shared state), reassembled in any order.
4. Telomere composition: each line wrapped in telomeres, scattered in
   prose, discovered and reassembled.
5. Localized repair: one corrupted digit. Whole-wire brute force vs
   per-line localization (bad line identified by its checksum, search
   confined to it). Candidate counts and wall time measured.
6. Partial failure: a dropped line is reported by index; surviving
   lines still decode on their own.
"""
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor

import tiktoken
from codec import (build_message, decode_lines, decode_message_bits,
                   demo_registry, encode_lines, encode_message_bits,
                   first_n_primes, registry_fingerprint, scan_telomeres,
                   validate_message, wrap_telomere, _digit_checksum)

enc = tiktoken.get_encoding("cl100k_base")
T = lambda s: len(enc.encode(s))  # noqa: E731

export = json.load(open("ccc_export.json"))
reg = demo_registry(export)
B = len(reg.names)
primes = first_n_primes(B + 16)
msg = build_message(export, reg, primes)
wire = encode_message_bits(msg)
assert validate_message(msg, B, primes)

K = 4
lines = encode_lines(msg, K)
print(f"1. {K} lines: {sum(len(l) for l in lines)} chars, "
      f"{sum(T(l) for l in lines)} tokens vs single wire {len(wire)} "
      f"chars, {T(wire)} tokens "
      f"(+{sum(T(l) for l in lines) - T(wire)} tokens line overhead)")

# ------------------------------------------------------- 2. order freedom
assert decode_lines(lines[::-1]) == msg
random.seed(7)
shuf = lines[:]
random.shuffle(shuf)
assert decode_lines(shuf) == msg
print("2. order independence: reversed and shuffled orders reassemble "
      "to identical ints")

# ---------------------------------------------------------- 3. parallel
def dec(ln):
    core = ln[:-3]  # strip the per-line header checksum
    return int(ln[:2]), decode_message_bits(core[4:])

with ThreadPoolExecutor(max_workers=K) as ex:
    got = dict(ex.map(dec, shuf))
assert [i for idx in sorted(got) for i in got[idx]] == msg
print("3. parallel: lines decoded concurrently in a thread pool, "
      "reassembled exactly (no shared state between lines)")

# ------------------------------------------------- 4. telomere composition
fp = registry_fingerprint(reg)
wrapped = [wrap_telomere(l, 4, B, fp, 2) for l in lines]
random.shuffle(wrapped)
prose = "Notes. " + " Interleaving text here. ".join(wrapped) + " End."
found = [body for _ctx, body in scan_telomeres(prose)]
assert len(found) == K and decode_lines(found) == msg
print(f"4. telomere composition: {K} lines discovered scattered in "
      f"prose (out of order), reassembled exactly")

# ------------------------------------------------- 5. localized repair
random.seed(21)


def digit_positions(s):
    return [i for i, ch in enumerate(s) if ch in "0123456789"]


def candidates(s):
    """All single-digit variants passing the v4 checksum.
    Returns (attempts, [(candidate, ints)])."""
    attempts, out = 0, []
    for i in digit_positions(s):
        for e in "0123456789":
            if e == s[i]:
                continue
            attempts += 1
            cand = s[:i] + e + s[i + 1:]
            try:
                out.append((cand, decode_message_bits(cand)))
            except ValueError:
                pass
    return attempts, out


# (a) whole-wire baseline: corrupt one digit of the single wire
i = random.choice(digit_positions(wire))
d = random.choice([c for c in "0123456789" if c != wire[i]])
bad_wire = wire[:i] + d + wire[i + 1:]
t0 = time.perf_counter()
n_whole, whole_c = candidates(bad_wire)
whole = [(c, ints) for c, ints in whole_c
         if validate_message(ints, B, primes)]
t_whole = time.perf_counter() - t0

# (b) lines: corrupt one digit in one line's v4 body (not its LLKK
# header or header checksum)
li = 1
ln = lines[li]
j = random.choice([p for p in digit_positions(ln) if 4 <= p < len(ln) - 3])
e = random.choice([c for c in "0123456789" if c != ln[j]])
bad_line = ln[:j] + e + ln[j + 1:]
t0 = time.perf_counter()
test_lines = lines[:li] + [bad_line] + lines[li + 1:]
bad_idx, good = None, {}
for q, l in enumerate(test_lines):
    try:
        good[q] = decode_message_bits(l[4:-3])
    except ValueError:
        bad_idx = q
assert bad_idx == li
n_local = K  # line identifications...
local_valid = []
n_cand, cands = candidates(bad_line[4:-3])  # search confined to bad line
n_local += n_cand
for c, ints in cands:
    full = [i for idx in range(K)
            for i in (ints if idx == bad_idx else good[idx])]
    if validate_message(full, B, primes):
        core = bad_line[:4] + c
        local_valid.append(core + _digit_checksum(core))
t_local = time.perf_counter() - t0

assert wire in [c for c, _ in whole], "truth lost in whole-wire repair!"
assert lines[li] in local_valid, "truth lost in localized repair!"
fixed = [c for c in local_valid
         if decode_lines(lines[:li] + [c] + lines[li + 1:]) == msg]
print(f"5. single-digit corruption repair:")
print(f"   whole wire: {n_whole} candidates tried, {t_whole * 1000:.1f} ms, "
      f"{len(whole)} checksum+structurally valid, truth included: True")
print(f"   localized:  bad line identified as #{bad_idx} by its checksum; "
      f"{n_local} candidates tried ({n_whole / n_local:.1f}x fewer), "
      f"{t_local * 1000:.1f} ms, {len(local_valid)} valid "
      f"(truth included; exact reassembly unique: {fixed == [lines[li]]})")

# ------------------------------------------------------- 6. partial failure
try:
    decode_lines([l for q, l in enumerate(lines) if q != 2])
    print("6. ERROR: dropped line not detected")
except ValueError as exc:
    survivors = [decode_message_bits(l[4:-3])
                 for q, l in enumerate(lines) if q != 2]
    print(f"6. dropped line -> decode_lines reports '{exc}'; the "
          f"{K - 1} surviving lines still decode independently "
          f"({sum(len(c) for c in survivors)}/{len(msg)} ints recovered)")
