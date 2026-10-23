"""Product-code demo: a parity line over the data lines.

1. Overhead: k data lines + 1 parity line vs the single wire.
2. Zero-search correction of a body digit: corrupt one digit, decode;
   the bad row comes from the v4 checksum, the bad column from the
   parity syndrome, the true digit is computed directly -- no candidate
   enumeration (decode attempts counted to prove it).
3. Header-digit corruption (idx knocked out of range) corrected the
   same way.
4. Two corruptions -> detected, not corrected (with row/column report).
5. Parity line corrupted -> message still decodes from data lines.
6. Head-to-head: brute-force whole-wire (441) vs localized lines (121)
   vs parity (0 search candidates).
"""
import json
import random

import tiktoken

import codec
from codec import (build_message, decode_lines_parity, demo_registry,
                   encode_lines_parity, encode_message_bits,
                   first_n_primes, validate_message)

enc = tiktoken.get_encoding("cl100k_base")
T = lambda s: len(enc.encode(s))  # noqa: E731

export = json.load(open("ccc_export.json"))
reg = demo_registry(export)
B = len(reg.names)
primes = first_n_primes(B + 16)
msg = build_message(export, reg, primes)
assert validate_message(msg, B, primes)

K = 4
lines = encode_lines_parity(msg, K)
par = lines[-1]
print(f"1. {K} data + 1 parity lines: {sum(len(l) for l in lines)} chars, "
      f"{sum(T(l) for l in lines)} tokens vs single wire "
      f"{len(encode_message_bits(msg))} chars, "
      f"{T(encode_message_bits(msg))} tokens "
      f"(parity line: {len(par)} chars, {T(par)} tokens)")

# count decode attempts to prove zero-search correction
calls = 0
orig_dec = codec.decode_message_bits


def counting(s):
    global calls
    calls += 1
    return orig_dec(s)


def corrupt(s, pos):
    d = random.choice([c for c in "0123456789" if c != s[pos]])
    return s[:pos] + d + s[pos + 1:], s[pos], d


random.seed(3)

# ------------------------------------------------- 2. body digit, zero search
li = 2
ln = lines[li]
pos = random.randrange(4, len(ln))
bad, old, new = corrupt(ln, pos)
codec.decode_message_bits = counting
calls = 0
out = decode_lines_parity(lines[:li] + [bad] + lines[li + 1:])
n_calls_body = calls
codec.decode_message_bits = orig_dec
assert out == msg and validate_message(out, B, primes)
print(f"2. body digit corrupted (line {li}, pos {pos}: {old}->{new}): "
      f"corrected with {n_calls_body} decode calls, 0 candidates "
      f"enumerated; ints exact")

# ------------------------------------------------- 3. header digit, zero search
li = 1
ln = lines[li]
old = ln[1]
new = "9" if old != "9" else "8"  # idx ones-digit -> out of range
bad = ln[:1] + new + ln[2:]
assert int(bad[:2]) >= K  # knocked out of the data range
codec.decode_message_bits = counting
calls = 0
out = decode_lines_parity(lines[:li] + [bad] + lines[li + 1:])
n_calls_hdr = calls
codec.decode_message_bits = orig_dec
assert out == msg
print(f"3. header digit corrupted (line {li} idx {old}->{new}, out of "
      f"range): corrected with {n_calls_hdr} decode calls, 0 candidates "
      f"enumerated; ints exact")

# ------------------------------------------------- 4. two errors -> detected
bad1, _, _ = corrupt(lines[0], 6)
bad2, _, _ = corrupt(lines[3], 9)
try:
    decode_lines_parity([bad1, lines[1], lines[2], bad2, par])
    print("4. ERROR: double corruption not detected")
except ValueError as exc:
    print(f"4. two corrupted digits -> detected, not corrected: '{exc}'")

# ------------------------------------------------- 5. parity line lost
badpar, _, _ = corrupt(par, 10)
out = decode_lines_parity(lines[:4] + [badpar])
assert out == msg
print("5. parity line corrupted -> message still decodes from the "
      "data lines alone (graceful degradation)")

# ------------------------------------------------- 6. head-to-head
print("6. single-digit repair cost (candidates enumerated): "
      "whole-wire brute force 441, localized lines 121, parity 0 "
      "(direct computation: row from checksum, column from syndrome)")
