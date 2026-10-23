#!/usr/bin/env python3
"""CCC-2 codec — D-wire encoder/decoder implementing SPEC.md v1.

Content layer derived (D/G/V/B/C/L native types, labels first
language, honest boundary as format field). Transport carried over
from v1 (JSON, telomere wrap, registry index, checksum discipline
per D5).
"""
import json, hashlib, re

FORMAT = "ccc2-wire/1"
TELOMERE = "TELOMERE-CCC2-1"

LABELS = {"exact", "computationally_verified", "conjectural",
          "heuristic", "killed", "superseded", "unstated"}
GENRES = {"original", "reframed", "identification"}
RELS = {"supports", "contradicts", "bounds", "generalizes",
        "implements", "depends_on", "causes", "measures",
        "defines", "exemplifies", "refines", "supersedes"}
KINDS = {"claim", "definition", "question"}

# required fields per type (checksum added at encode time)
REQUIRED = {
    "D": ["id", "type", "subtitle", "rule", "generates",
          "verified", "honest_boundary", "honest_label"],
    "G": ["id", "type", "title", "verdict", "tried",
          "result", "transfer"],
    "V": ["id", "type", "subject", "status", "consequence"],
    "B": ["id", "type", "x", "y", "buys", "limits"],
    "C": ["id", "type", "kind", "label", "status"],
    "L": ["id", "type", "from", "to", "rel"],
}
ID_RE = re.compile(r"^[DGVBCL]\d+$")


def canonical(obj):
    """Canonical serialization for checksums: sorted keys, no whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def record_checksum(rec):
    body = {k: v for k, v in rec.items() if k != "checksum"}
    return hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()


def check_wellformed(rec):
    """Returns list of problems (empty = well-formed). Per SPEC §2+§5."""
    probs = []
    t = rec.get("type")
    if t not in REQUIRED:
        return [f"unknown type {t!r}"]
    for f in REQUIRED[t]:
        if f not in rec:
            probs.append(f"missing field {f!r}")
    rid = rec.get("id", "")
    if not ID_RE.match(rid or ""):
        probs.append(f"bad id {rid!r}")
    elif rid and not rid.startswith(t):
        probs.append(f"id {rid!r} mismatches type {t!r}")
    if t == "D":
        for g in rec.get("generates", []):
            if "prescription" not in g:
                probs.append(f"D {rid}: generates stage lacks prescription")
        conv = rec.get("conventions")
        if conv is not None and not (
                isinstance(conv, list) and
                all(isinstance(s, str) for s in conv)):
            probs.append(f"D {rid}: conventions must be a list of strings")
        hb = rec.get("honest_boundary", "")
        if hb and len(hb.split()) < 8:
            probs.append(f"D {rid}: honest_boundary too thin to be a stop-line")
        if rec.get("honest_label") not in LABELS:
            probs.append(f"D {rid}: bad honest_label")
        if "genre" in rec and rec["genre"] not in GENRES:
            probs.append(f"D {rid}: bad genre")
    if t == "V" and rec.get("status") not in LABELS:
        probs.append(f"V {rid}: bad status")
    if t == "C":
        if rec.get("kind") not in KINDS:
            probs.append(f"C {rid}: bad kind")
        if rec.get("status") not in LABELS:
            probs.append(f"C {rid}: bad status")
        if rec.get("kind") == "question" and rec.get("status") != "unstated":
            probs.append(f"C {rid}: question must carry unstated")
        if rec.get("kind") != "question" and rec.get("status") == "unstated":
            probs.append(f"C {rid}: unstated is reserved for questions")
    if t == "L" and rec.get("rel") not in RELS:
        probs.append(f"L {rid}: bad rel")
    return probs


def encode(records, chunk):
    """records: list of dicts (without checksums). Returns wrapped wire str."""
    recs = []
    for r in records:
        r = dict(r)
        r["checksum"] = record_checksum(r)
        recs.append(r)
    recs.sort(key=lambda r: r["id"])
    wire_cs = hashlib.sha256(
        "".join(r["checksum"] for r in recs).encode()).hexdigest()
    wire = {"format": FORMAT, "chunk": chunk, "records": recs,
            "registry": {r["id"]: r["type"] for r in recs},
            "wire_checksum": wire_cs}
    payload = canonical(wire)
    return f"{TELOMERE}:{payload}:{TELOMERE}"


def decode(wire_str):
    """Returns (records, report). Raises ValueError on any failure."""
    m = re.fullmatch(re.escape(TELOMERE) + r":(.*):" + re.escape(TELOMERE),
                     wire_str, re.DOTALL)
    if not m:
        raise ValueError("telomere wrap missing or broken")
    wire = json.loads(m.group(1))
    if wire.get("format") != FORMAT:
        raise ValueError(f"format mismatch: {wire.get('format')!r}")
    recs = wire["records"]
    expect = hashlib.sha256(
        "".join(r["checksum"] for r in recs).encode()).hexdigest()
    if expect != wire["wire_checksum"]:
        raise ValueError("WIRE-CHECKSUM-MISMATCH")
    report = []
    for r in recs:
        if record_checksum(r) != r["checksum"]:
            raise ValueError(f"RECORD-CHECKSUM-MISMATCH: {r.get('id')}")
        probs = check_wellformed(r)
        if probs:
            raise ValueError(f"MALFORMED {r.get('id')}: " + "; ".join(probs))
        report.append((r["id"], "ok"))
    # strip checksums for the clean decoded records
    clean = [{k: v for k, v in r.items() if k != "checksum"} for r in recs]
    return clean, {"wire": wire["chunk"], "records": report}


if __name__ == "__main__":
    # self-test on the SPEC §6 example
    rec = {
        "id": "D1", "type": "D",
        "subtitle": "Deformation: the singular series as renormalized total weight",
        "rule": "p marks residues R_p = {0} (p=2), {0,−2} (p odd)",
        "conventions": ["p marks only n>p"],
        "generates": [{"stage": "s", "prescription": "p1"}],
        "verified": [{"check": "c", "expected": "e"}],
        "honest_boundary": "We verify the algebra here; the asymptotic passage is not derived and must not be presented.",
        "honest_label": "computationally_verified",
    }
    w = encode([rec], "c00")
    out, rep = decode(w)
    assert out[0]["subtitle"] == rec["subtitle"], "round-trip field loss"
    assert rep["records"] == [("D1", "ok")]
    # tamper check
    bad = w.replace("Deformation", "Deformatix")
    try:
        decode(bad)
        raise AssertionError("tamper not caught")
    except ValueError as e:
        assert "CHECKSUM" in str(e), e
    print("codec self-test: round-trip ok, tamper caught")
