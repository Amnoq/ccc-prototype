"""Independent v5 decoder from DECODE_SPEC.md alone. No codec decode imports."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_decode_test_v5 as G

MAT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "decode_test_material_v5")


def primes_upto(n):
    sieve = [True] * (n + 1)
    out = []
    for i in range(2, n + 1):
        if sieve[i]:
            out.append(i)
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return out


def spec_decode_v5(text, registry_names):
    m = re.search(r"zz(\d{7})(.*?)(\d{7})ZZ", text, re.DOTALL)
    assert m and m.group(1) == m.group(3)
    ctx = m.group(1)
    version, RR, FF = int(ctx[0]), int(ctx[1:3]), int(ctx[3:5])
    assert version == 5, f"want v5, got {version}"
    body = m.group(2)
    assert body.isdigit()
    fp = sum(ord(c) for n in registry_names for c in n) % 100
    assert fp == FF, f"fp {fp} != {FF}"
    assert len(registry_names) == RR

    NNN, P = int(body[0:3]), int(body[3])
    assert len(body) == 4 + 3 * NNN + 3
    trips = [int(body[4 + 3 * i:7 + 3 * i]) for i in range(NNN)]
    assert (NNN + P + sum(trips)) % 1000 == int(body[4 + 3 * NNN:])

    bits = "".join(format(t, "09b") for t in trips)
    bits = bits[:len(bits) - P] if P else bits
    ints, pos = [], 0
    while pos < len(bits):
        n = 0
        while bits[pos] == "0":
            n += 1
            pos += 1
        ints.append(int(bits[pos:pos + n + 1], 2) - 1)
        pos += n + 1
    assert pos == len(bits)

    B = ints[0]
    assert B == RR
    primes = primes_upto(500)
    p2i = {p: i + 1 for i, p in enumerate(primes)}

    def unproduct(x):
        if x == 1:
            return []
        facs, tmp = [], x
        for p in primes:
            if p * p > tmp:
                break
            while tmp % p == 0:
                facs.append(p)
                tmp //= p
        if tmp > 1:
            facs.append(tmp)
        return sorted(p2i[p] for p in facs)

    name = lambda i: registry_names[i - 1]
    pos, out = 1, {}
    nS = ints[pos]
    pos += 1
    strands = []
    for _ in range(nS):
        li, code = ints[pos], ints[pos + 1]
        pos += 2
        assert 0 <= li <= B
        strands.append({"label": name(li) if li else None,
                        "members": [name(i) for i in unproduct(code)]})
    nE = ints[pos]
    pos += 1
    edges = []
    for k in range(nE):
        c = ints[pos + k]
        t, ab = c % B, c // B
        a, b = ab // B, ab % B
        assert 0 <= a < B and 0 <= b < B and 0 <= t < B
        edges.append((name(a + 1), name(t + 1), name(b + 1)))
    pos += nE
    nA = ints[pos]
    pos += 1
    anchors = []
    for k in range(nA):
        p = ints[pos + k]
        s, c_ = p // B, p % B
        assert 0 <= s < B and 0 <= c_ < B
        anchors.append((name(c_ + 1), name(s + 1)))
    pos += nA
    loops = [name(i) for i in unproduct(ints[pos])]
    return {"strands": strands, "edges": edges,
            "anchors": anchors, "loops": loops}


def main():
    wrapped = open(os.path.join(MAT, "wrapped.txt")).read().strip()
    got = spec_decode_v5("prose " + wrapped + " prose", G.BASE + G.TYPES +
                         G.STATUSES + G.LABELS)
    want = json.load(open(os.path.join(MAT, "struct.json")))
    norm = lambda es: sorted(tuple(e) for e in es)
    ok = (got["strands"] == want["strands"]
          and norm(got["edges"]) == norm(want["edges"])
          and norm(got["anchors"]) == norm(want["anchors"])
          and sorted(got["loops"]) == sorted(want["loops"]))
    print("V5 SPEC DECODE MATCHES:", ok)
    if not ok:
        print(json.dumps(got, indent=1)[:1200])


if __name__ == "__main__":
    main()
