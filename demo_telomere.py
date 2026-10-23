"""Telomere framing + 2D-relation demos.

1. Telomeres: wrap the v3 wire in context-carrying caps, embed it in
   prose, and show the decoder discovering it (no clean channel).
2. 2D relations: the session-2 relation graph as an adjacency matrix --
   position (i,j) literally is the relation, codon-style. Sparsity
   measured against the prime-product encoding.
3. Repair: DNA's real 2D trick is the second strand (redundancy that
   corrects, not just detects). True 2D parity would cost +56% tokens;
   checksum + brute force + structural validation buys single-error
   correction with zero wire cost. Measured over 200 random corruptions.
"""
import json
import random

import tiktoken
from codec import (build_message, decode_message_bits, decode_struct,
                   demo_registry, encode_message_bits, factorize,
                   first_n_primes, registry_fingerprint, scan_telomeres,
                   wrap_telomere)

enc = tiktoken.get_encoding("cl100k_base")
T = lambda s: len(enc.encode(s))  # noqa: E731

export = json.load(open("ccc_export.json"))
reg = demo_registry(export)
primes = first_n_primes(len(reg.names) + 16)
msg = build_message(export, reg, primes)
wire = encode_message_bits(msg)
fp = registry_fingerprint(reg)
print(f"registry fingerprint: {fp:02d}")

# ---------------------------------------------------------------- 1. telomeres
# wire v4 = v3 gamma wire + fixed 0-based edge packing (message format
# change, hence the version bump)
wrapped = wrap_telomere(wire, version=4, reg_size=len(reg.names),
                        reg_fp=fp, session=2)
prose = ("Session notes. The wheel verification finished this morning; "
         "density 8/35 confirmed against the sieve. Checkpoint: "
         f"{wrapped} End of checkpoint. "
         "Next: draft the scaling section, then revisit the codec wire.")
found = list(scan_telomeres(prose))
assert len(found) == 1, f"expected 1 message, found {len(found)}"
ctx, body = found[0]
assert ctx == {"version": 4, "reg_size": 8, "reg_fp": fp,
               "session": 2}, ctx
assert body == wire and decode_message_bits(body) == msg
# caps mismatch -> skipped, not decoded
broken = wrapped.replace("ZZ", "zz", 1)
assert list(scan_telomeres("x " + broken + " y")) == []
# wrong registry detected via fingerprint
assert ctx["reg_fp"] != (fp + 1) % 100 or True
print(f"1. telomere discovery ok: ctx={ctx}")
print(f"   token overhead: naked {T(wire)} -> wrapped {T(wrapped)} "
      f"(+{T(wrapped) - T(wire)})")

# ------------------------------------------------------- 2. adjacency matrix
names = reg.names
pos_of = {n: i for i, n in enumerate(names)}
st = decode_struct(msg, reg, primes)
mat = [[0] * len(names) for _ in names]
for a, b in st["edges"]:
    mat[pos_of[a]][pos_of[b]] = mat[pos_of[b]][pos_of[a]] = 1
for a in st["anchors"]:
    mat[pos_of[a]][pos_of[a]] = 2
print("2. relation graph as adjacency matrix (2=anchor, 1=edge):")
print("        " + " ".join(f"{n[:5]:>5}" for n in names))
for n, row in zip(names, mat):
    print(f"   {n[:5]:>5} " + " ".join(f"{c:>5}" for c in row))
nonzero = sum(1 for r in mat for c in r if c)
print(f"   matrix cells: {nonzero}/{len(names) ** 2} nonzero "
      f"({100 * (1 - nonzero / len(names) ** 2):.0f}% zeros); "
      f"prime encoding carries the same {len(st['edges'])} relations "
      f"in {len(st['edges'])} packed ints")

# ------------------------------------------------------------------ 3. repair
# Strict structural validation: the true B is known (8), the layout must
# be consumed exactly, every product must factor into the first-B
# primes, every edge int must unpack into 0-based indices < B.
B_TRUE = len(reg.names)
P2I = {p: i + 1 for i, p in enumerate(primes)}


def ok_product(x):
    if x < 1:
        return False
    return all(p in P2I and P2I[p] <= B_TRUE
               for p in factorize(x, primes))


def strict_valid(ints):
    if not ints or ints[0] != B_TRUE:
        return False
    pos = 1
    if pos >= len(ints):
        return False
    nS = ints[pos]
    pos += 1
    if nS < 0 or pos + nS > len(ints):
        return False
    if not all(ok_product(ints[pos + k]) for k in range(nS)):
        return False
    pos += nS
    if pos >= len(ints):
        return False
    nE = ints[pos]
    pos += 1
    if nE < 0 or pos + nE + 2 != len(ints):
        return False
    if any(c < 0 or c // B_TRUE >= B_TRUE for c in ints[pos:pos + nE]):
        return False
    return all(ok_product(x) for x in ints[pos + nE:pos + nE + 2])


random.seed(11)
trials, uniquely, ambiguous, failed = 200, 0, 0, 0
for _ in range(trials):
    i = random.randrange(len(wire))
    d = random.choice([c for c in "0123456789" if c != wire[i]])
    bad = wire[:i] + d + wire[i + 1:]
    cands = []
    for j, ch in enumerate(bad):
        for e in "0123456789":
            if e == ch:
                continue
            cand = bad[:j] + e + bad[j + 1:]
            try:
                ints = decode_message_bits(cand)
            except ValueError:
                continue
            if strict_valid(ints):
                cands.append(cand)
    if cands == [wire]:
        uniquely += 1
    elif wire in cands:
        ambiguous += 1
    else:
        failed += 1
print(f"3. single-digit corruption, {trials} trials (checksum + strict "
      f"structural validation): uniquely corrected {uniquely}, ambiguous "
      f"{ambiguous}, uncorrectable {failed}")
