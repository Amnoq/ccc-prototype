"""Independent wire decoder, implemented SOLELY from DECODE_SPEC.md.

Does not import any decode function from codec.py. (Imports Registry only
as the stand-in for 'the shared registry both sides hold'.)
Simulates: a naive model with the spec + the shared registry.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from codec import Registry  # shared-registry stand-in only

MAT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "decode_test_material")


def primes_upto(n):
    sieve = [True] * (n + 1)
    out = []
    for i in range(2, n + 1):
        if sieve[i]:
            out.append(i)
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return out


def factorize_small(x, primes):
    facs = []
    for p in primes:
        if p * p > x:
            break
        while x % p == 0:
            facs.append(p)
            x //= p
    if x > 1:
        facs.append(x)
    return facs


def spec_decode(text, registry_names):
    # Step 1: find telomere
    m = re.search(r"zz(\d{7})(.*?)(\d{7})ZZ", text, re.DOTALL)
    assert m and m.group(1) == m.group(3), "telomere not found / caps mismatch"
    ctx = m.group(1)
    version, RR, FF, SS = int(ctx[0]), int(ctx[1:3]), int(ctx[3:5]), int(ctx[5:7])
    assert version == 4, f"unsupported version {version}"
    body = m.group(2)
    assert body.isdigit(), "non-digit body"

    # Step 2: fingerprint
    fp = sum(ord(c) for n in registry_names for c in n) % 100
    assert fp == FF, f"fingerprint {fp} != {FF}"
    assert len(registry_names) == RR, "registry size mismatch"

    # Step 3: wire checksum
    NNN, P = int(body[0:3]), int(body[3])
    assert len(body) == 4 + 3 * NNN + 3, "bad body length"
    trips = [int(body[4 + 3 * i:7 + 3 * i]) for i in range(NNN)]
    CK = int(body[4 + 3 * NNN:])
    assert (NNN + P + sum(trips)) % 1000 == CK, "checksum mismatch"

    # Step 4: triples -> bits
    bits = "".join(format(t, "09b") for t in trips)
    bits = bits[:len(bits) - P] if P else bits

    # Step 5: gamma decode
    ints, pos = [], 0
    while pos < len(bits):
        n = 0
        while bits[pos] == "0":
            n += 1
            pos += 1
        v = int(bits[pos:pos + n + 1], 2)
        ints.append(v - 1)
        pos += n + 1
    assert pos == len(bits), "bitstream not exactly consumed"

    # Step 6: parse layout
    B = ints[0]
    assert B == RR
    primes = primes_upto(500)
    prime_to_idx = {p: i + 1 for i, p in enumerate(primes)}

    def unproduct(x):
        if x == 1:
            return []
        return sorted(prime_to_idx[p] for p in factorize_small(x, primes))

    pos = 1
    nS = ints[pos]
    pos += 1
    strands = [unproduct(ints[pos + k]) for k in range(nS)]
    pos += nS
    nE = ints[pos]
    pos += 1
    edges = []
    for k in range(nE):
        c = ints[pos + k]
        a, b = c // B, c % B
        assert 0 <= a < B and 0 <= b < B, "edge out of range"
        edges.append((a + 1, b + 1))
    pos += nE
    anchors = unproduct(ints[pos])
    loops = unproduct(ints[pos + 1])

    # Step 7: names
    name = lambda i: registry_names[i - 1]
    return {
        "strands": [[name(i) for i in s] for s in strands],
        "edges": sorted((name(a), name(b)) for a, b in edges),
        "anchors": [name(i) for i in anchors],
        "loops": [name(i) for i in loops],
    }


def main():
    with open(os.path.join(MAT, "wrapped.txt")) as f:
        wrapped = f.read().strip()
    with open(os.path.join(MAT, "legend.json")) as f:
        legend = json.load(f)
    # registry stand-in: rebuild full ordered name list (indices 1..B).
    # legend only has used indices; full list needed for index->name.
    # In deployment both sides hold the whole registry; here we
    # reconstruct it from the generator's concept order.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gen_decode_test as G
    reg_names = G.CONCEPTS

    # also test discovery inside prose
    text = "Some prose here. " + wrapped + " More prose."
    got = spec_decode(text, reg_names)

    with open(os.path.join(MAT, "struct.json")) as f:
        want = json.load(f)
    want_edges = sorted(tuple(sorted(e)) for e in want["edges"])
    got_edges = sorted(tuple(sorted(e)) for e in got["edges"])
    ok = (got["strands"] == want["strands"] and got_edges == want_edges
          and sorted(got["anchors"]) == sorted(want["anchors"])
          and sorted(got["loops"]) == sorted(want["loops"]))
    print("SPEC DECODE MATCHES REFERENCE:", ok)
    if not ok:
        print("GOT :", json.dumps(got, indent=1)[:1500])
        print("WANT:", json.dumps(want, indent=1)[:1500])


if __name__ == "__main__":
    main()
