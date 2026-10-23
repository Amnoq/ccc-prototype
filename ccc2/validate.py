#!/usr/bin/env python3
"""CCC-2 fidelity validation: build wires for all 12 chunks, round-trip
each through the codec, and compare field-by-field. Gate: 12/12 exact.
"""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/ccc-prototype/ccc2")
from codec import encode, decode

BASE = "/home/hatch/workspace/ccc-prototype/ccc2"
CHUNKS = [f"c{i:02d}" for i in range(1, 13)]


def main():
    os.makedirs(f"{BASE}/wires", exist_ok=True)
    results = []
    for ch in CHUNKS:
        with open(f"{BASE}/corpus/{ch}/extraction.json") as f:
            ext = json.load(f)
        records = ext["records"]
        wire = encode(records, ch)
        with open(f"{BASE}/wires/{ch}.wire", "w") as f:
            f.write(wire)
        decoded, rep = decode(wire)
        # field-by-field comparison (decoded strips checksums by design;
        # both sides sorted by id — the wire's canonical order per spec)
        key = lambda r: r["id"]
        ok = (sorted(decoded, key=key) == sorted(records, key=key))
        n = len(records)
        types = {}
        for r in records:
            types[r["type"]] = types.get(r["type"], 0) + 1
        results.append((ch, ok, n, types))
        print(f"{ch}: {'OK' if ok else 'MISMATCH'} ({n} records {types})",
              flush=True)
        if not ok:
            # locate first divergence
            for a, b in zip(records, decoded):
                if a != b:
                    print(f"  first divergence at {a.get('id')}:")
                    for k in sorted(set(a) | set(b)):
                        if a.get(k) != b.get(k):
                            print(f"    {k}: {str(a.get(k))[:120]!r} vs "
                                  f"{str(b.get(k))[:120]!r}")
                    break
    good = sum(1 for _, ok, _, _ in results if ok)
    print(f"\n{good}/12 round-trip exact")
    return good == 12


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
