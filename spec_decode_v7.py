"""Independent v7 decoder from DECODE_SPEC.md alone.

No codec imports whatsoever: telomere scan, 4-digit header, gamma ints,
layout-aware int-stream decode, raw note block, prime-product strands,
v7 strength enum + genre field, merge lattice — all reimplemented from
the spec text.
"""
import json
import os
import re
import sys

STATUS_NAMES = ("unstated", "heuristic", "conjectural",
                "verified-numeric", "exact", "killed", "superseded")
GENRE_NAMES = ("none", "original", "reframed", "identification")
NGENRES = 4
# legacy string -> strength, per DECODE_SPEC v7 section (lossy-
# conservative: "verified" -> verified-numeric, never exact)
STATUS_FROM_STRING = {
    "exact": 4, "derived": 4,
    "computationally_verified": 3, "computationally-verified": 3,
    "verified": 3,
    "conjectural": 2, "asserted": 2,
    "heuristic": 1,
    "superseded": 6,
    "killed": 5, "rejected": 5, "refuted": 5,
}


def primes_upto(n):
    sieve = [True] * (n + 1)
    out = []
    for i in range(2, n + 1):
        if sieve[i]:
            out.append(i)
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return out


def spec_decode_v7(text, registry_names):
    m = re.search(r"zz(\d{7})(.*?)(\d{7})ZZ", text, re.DOTALL)
    assert m and m.group(1) == m.group(3)
    ctx = m.group(1)
    version, RR, FF = int(ctx[0]), int(ctx[1:3]), int(ctx[3:5])
    assert version == 7, f"want v7, got {version}"
    body = m.group(2)
    fp = sum(ord(c) for n in registry_names for c in n) % 100
    assert fp == FF, f"fp {fp} != {FF}"
    assert len(registry_names) == RR

    # v7 body framing is v6's: 4-digit header; header + triplets +
    # NOTETEXT + cksum
    NNNN, P = int(body[0:4]), int(body[4])
    trip_end = 5 + 3 * NNNN
    trips = [int(body[5 + 3 * i:8 + 3 * i]) for i in range(NNNN)]

    bits = "".join(format(t, "09b") for t in trips)
    bits = bits[:len(bits) - P] if P else bits

    pos = 0

    def rd():
        nonlocal pos
        n = 0
        while bits[pos] == "0":
            n += 1
            pos += 1
        v = int(bits[pos:pos + n + 1], 2)
        pos += n + 1
        return v - 1

    ints = []
    assert rd() == 7, "bad version int"
    ints.append(7)
    B, E = rd(), rd()
    ints += [B, E]
    assert B == RR and E >= 1
    nS = rd()
    ints.append(nS)
    for _ in range(nS):
        ints += [rd(), rd()]
    nE = rd()
    ints.append(nE)
    for _ in range(nE):
        ints.append(rd())
    nA = rd()
    ints.append(nA)
    for _ in range(nA):
        ints.append(rd())
    nN = rd()
    ints.append(nN)
    lens = [rd() for _ in range(nN)]
    ints += lens
    nT = rd()
    ints.append(nT)
    for _ in range(nT):
        ints.append(rd())
    ints.append(rd())  # Lp

    note_len = sum(lens)
    notetext = body[trip_end:trip_end + note_len]
    assert len(notetext) == note_len, "truncated note text"
    cksum = body[trip_end + note_len:]
    assert len(body) == trip_end + note_len + 3, "body length mismatch"
    expect = (NNNN + P + sum(trips)
              + sum(ord(c) for c in notetext)) % 1000
    assert expect == int(cksum), "checksum mismatch"
    notes, p = [], 0
    for ln in lens:
        notes.append(notetext[p:p + ln])
        p += ln

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
    q = 4  # ints = [7, B, E, nS, ...]
    strands = []
    for _ in range(nS):
        li, code = ints[q], ints[q + 1]
        q += 2
        assert 0 <= li <= B
        strands.append({"label": name(li) if li else None,
                        "members": [name(i) for i in unproduct(code)]})
    assert ints[q] == nE
    q += 1
    edges = []
    for _ in range(nE):
        c = ints[q]
        q += 1
        t, ab = c % B, c // B
        a, b = ab // B, ab % B
        assert 0 <= a < B and 0 <= b < B and 0 <= t < B
        edges.append((name(a + 1), name(t + 1), name(b + 1)))
    assert ints[q] == nA
    q += 1
    anchors = []
    for _ in range(nA):
        ak = ints[q]
        q += 1
        # v7 anchor: ak = ((s*G + g)*B + c)*B + n
        n = ak % B
        w = ak // B
        c0 = w % B
        v = w // B
        g = v % NGENRES
        s = v // NGENRES
        assert (0 <= s <= 6 and 0 <= g < NGENRES
                and 0 <= c0 < B and 0 <= n <= nN)
        anchors.append({"concept": name(c0 + 1),
                        "status": STATUS_NAMES[s],
                        "genre": GENRE_NAMES[g],
                        "note": notes[n - 1] if n else None})
    assert ints[q] == nN
    q += 1 + nN
    assert ints[q] == nT
    q += 1
    entity_status = []
    for _ in range(nT):
        qq = ints[q]
        q += 1
        c0 = qq % B
        qq //= B
        u = qq % E
        qq //= E
        f = qq % E
        s = qq // E
        assert 0 <= s <= 6 and 1 <= f < E and 0 <= u < E and 0 <= c0 < B
        entity_status.append({"concept": name(c0 + 1),
                              "status": STATUS_NAMES[s],
                              "valid_from": f,
                              "valid_until": u or None})
    loops = [name(i) for i in unproduct(ints[q])]
    q += 1
    assert q == len(ints), "trailing ints"

    # merge lattice: newer epoch wins; ties break toward terminal, then
    # stronger live (enum order encodes it: 6>5>4>3>2>1>0)
    table = {}
    for e in entity_status:
        cur = table.get(e["concept"])
        code = STATUS_NAMES.index(e["status"])
        if (cur is None or e["valid_from"] > cur[1]
                or (e["valid_from"] == cur[1]
                    and code > STATUS_NAMES.index(cur[0]))):
            table[e["concept"]] = (e["status"], e["valid_from"],
                                   e["valid_until"])
    return {"strands": strands, "edges": edges, "anchors": anchors,
            "entity_status": entity_status, "status_table": table,
            "loops": loops}


GENRE_FROM_STRING = {"original": 1, "reframed": 2, "identification": 3}


def want_from_doc(doc, epoch, reg_names):
    """Expected struct built from the extraction doc alone (no codec).
    reg_names: registry names in registry order (for member ordering).
    Legacy docs carry no genre -> 'none'; R4 docs carry it."""
    lab = {c["id"]: c["label"] for c in doc["concepts"]}
    order = {nm: i for i, nm in enumerate(reg_names)}
    strands = [{"label": (lab[s["label"]] if s.get("label") else None),
                "members": sorted((lab[i] for i in s["concept_ids"]),
                                  key=lambda nm: order[nm])}
               for s in doc["strands"]]
    edges = sorted((lab[e["a"]], e["rel"], lab[e["b"]])
                   for e in doc["edges"])
    anchors = sorted((lab[a["concept_id"]],
                      STATUS_NAMES[STATUS_FROM_STRING.get(a["status"], 0)],
                      GENRE_NAMES[GENRE_FROM_STRING.get(a.get("genre"), 0)],
                      a.get("note"))
                     for a in doc["anchors"])
    per = {}
    for a in doc["anchors"]:
        s = STATUS_FROM_STRING.get(a["status"], 0)
        per.setdefault(lab[a["concept_id"]], []).append(s)
    estatus = {}
    for c0, ss in per.items():
        term = [x for x in ss if x >= 5]
        s = max(term) if term else max(ss)
        estatus[c0] = (STATUS_NAMES[s], epoch, None)
    loops = sorted(lab[l["concept_id"]] for l in doc.get("loops", []))
    notes = sorted({a.get("note") for a in doc["anchors"] if a.get("note")})
    return strands, edges, anchors, estatus, loops, notes


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    # sender side only: build real v7 wires with the codec
    from memory_harness import (build_registry, to_v7_export,
                                validate_extraction)
    from codec import (first_n_primes, build_message_v7, encode_wire_v7,
                       wrap_telomere, registry_fingerprint)
    base = os.path.dirname(os.path.abspath(__file__))
    fails = 0
    for n in range(1, 13):
        ch = f"c{n:02d}"
        doc = json.load(open(f"{base}/corpus_runs/r3/{ch}/extraction.json"))
        assert not validate_extraction(doc)
        reg = build_registry(doc)
        primes = first_n_primes(len(reg.names))
        ints, notes = build_message_v7(to_v7_export(doc), reg, primes,
                                       epoch=n)
        body = encode_wire_v7(ints, notes)
        wrapped = wrap_telomere(body, 7, len(reg.names),
                                registry_fingerprint(reg), 1)
        got = spec_decode_v7("prose " + wrapped + " prose", reg.names)
        w_strands, w_edges, w_anchors, w_estatus, w_loops, w_notes = \
            want_from_doc(doc, n, reg.names)
        g_anchors = sorted((a["concept"], a["status"], a["genre"],
                            a["note"])
                           for a in got["anchors"])
        g_estatus = {e["concept"]: (e["status"], e["valid_from"],
                                    e["valid_until"])
                     for e in got["entity_status"]}
        ok = (got["strands"] == w_strands
              and sorted(got["edges"]) == w_edges
              and g_anchors == w_anchors
              and g_estatus == w_estatus
              and sorted(got["loops"]) == w_loops)
        # note survival: every doc note present verbatim on the wire
        wire_notes = {a["note"] for a in got["anchors"] if a["note"]}
        ok = ok and wire_notes == set(w_notes)
        print(ch, "SPEC DECODE MATCHES:", ok)
        if not ok:
            fails += 1
    print("FAILURES:", fails)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
