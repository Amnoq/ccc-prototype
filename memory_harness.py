"""memory_harness.py -- M1: extraction schema, deterministic verifier,
codec glue, SQLite store, checkpoint/restore, grouped injection.

Scope: HARNESS_MVP_SCOPE.md. M1 builds NO llm and NO retrieval:
hand-written extractions go validate -> merge -> checkpoint ->
restore -> inject. The extractor (M2) targets the schema validated here.

Design notes:
- The wire registry is vocab terms (REL_TYPES, then STATUSES, in fixed
  order) followed by the doc's concepts in doc order. Kinds are
  extractor-side metadata only (stored in SQLite, never on the wire:
  nothing references them).
- Refinement vs the scope's 3.2: loops reference concepts
  ({concept_id}, usually kind "open_question") instead of free text,
  because the v5 wire can only carry registry indices. Free-text loop
  bodies live on the concept's label.
- Checkpoints are self-contained: the wire lines plus the registry
  snapshot (labels in order) are stored together, so restore needs no
  ambient registry. Cross-session registry merging is phase 2.
"""

import json
import re
import sqlite3
import time

import codec
from codec import (Registry, build_message_v5, decode_struct_v5,
                   validate_message_v5, registry_fingerprint,
                   encode_lines_balanced, decode_lines,
                   wrap_telomere, scan_telomeres, first_n_primes,
                   build_message_v6, decode_struct_v6,
                   validate_message_v6, v6_status_of, V6_STATUS_NAMES,
                   apply_entity_status, encode_wire_v6, decode_wire_v6,
                   build_message_v7, decode_struct_v7,
                   validate_message_v7, v7_status_of, v7_genre_of,
                   V7_STATUS_NAMES, V7_GENRE_NAMES,
                   apply_entity_status_v7, encode_wire_v7, decode_wire_v7)

SCHEMA_VERSION = 1
WIRE_VERSION = 5  # telomere version selecting the v5 layout

# Fixed vocabularies. Order is load-bearing (registry indices), so
# changes are versioned via SCHEMA_VERSION, never edited in place.
REL_TYPES = ["supports", "contradicts", "bounds", "generalizes",
             "implements", "depends_on", "causes", "measures",
             "defines", "exemplifies", "refines", "supersedes"]
STATUSES = ["asserted", "verified", "superseded", "open_question"]
# v7 forward vocabulary (his labels; see corpus_runs/V7_STATUS_DESIGN.md).
# STATUSES stays frozen (registry order is load-bearing); v7 strings
# validate against the union.
V7_STATUS_VOCAB = ["exact", "derived", "computationally_verified",
                   "computationally-verified", "conjectural", "heuristic",
                   "killed", "rejected", "refuted"]
V7_GENRE_VOCAB = ["original", "reframed", "identification"]
KINDS = ["claim", "method", "result", "entity", "metric", "open_question"]

MAX_TELOMERE_CTX = 99  # wire context fields are 2 digits


class ExtractionError(Exception):
    """Raised when the deterministic verifier rejects an extraction."""

    def __init__(self, failures):
        self.failures = list(failures)
        super().__init__("extraction rejected:\n" +
                         "\n".join("  - " + f for f in failures))


# --------------------------------------------------------------------------
# deterministic verifier (scope 3.3)
# --------------------------------------------------------------------------

def _req(doc, key, failures):
    if not isinstance(doc, dict) or key not in doc:
        failures.append(f"missing required key {key!r}")
        return None
    return doc[key]


def validate_extraction(doc):
    """Check a strict-schema extraction. Returns [warnings].
    Raises ExtractionError on any hard failure."""
    failures, warnings = [], []

    concepts = _req(doc, "concepts", failures) or []
    strands = _req(doc, "strands", failures) or []
    edges = _req(doc, "edges", failures) or []
    anchors = _req(doc, "anchors", failures) or []
    loops = doc.get("loops", [])

    ids, labels = {}, {}
    for i, c in enumerate(concepts):
        if not isinstance(c, dict):
            failures.append(f"concepts[{i}] not an object")
            continue
        cid, lab, kind = c.get("id"), c.get("label"), c.get("kind")
        if not isinstance(cid, str) or not cid:
            failures.append(f"concepts[{i}] bad id {cid!r}")
        elif cid in ids:
            failures.append(f"duplicate concept id {cid!r}")
        if not isinstance(lab, str) or not lab.strip():
            failures.append(f"concepts[{i}] bad label {lab!r}")
        elif lab in labels:
            failures.append(f"duplicate concept label {lab!r}")
        if kind not in KINDS:
            failures.append(f"concept {cid!r} bad kind {kind!r}")
        ids[cid] = lab
        labels[lab] = cid

    def resolve(ref, where):
        if ref not in ids:
            failures.append(f"{where} references unknown concept {ref!r}")
            return False
        return True

    seen_strands = set()
    for i, s in enumerate(strands):
        where = f"strands[{i}]"
        if not isinstance(s, dict):
            failures.append(f"{where} not an object")
            continue
        sid = s.get("id")
        if sid in seen_strands:
            failures.append(f"duplicate strand id {sid!r}")
        seen_strands.add(sid)
        lab = s.get("label")
        if lab is not None:
            resolve(lab, f"{where} label")
        mems = s.get("concept_ids")
        if not isinstance(mems, list) or not mems:
            failures.append(f"{where} has empty concept_ids")
            continue
        if len(set(mems)) != len(mems):
            failures.append(f"{where} has duplicate members")
        for m in mems:
            resolve(m, where)

    seen_edges = set()
    for i, e in enumerate(edges):
        where = f"edges[{i}]"
        if not isinstance(e, dict):
            failures.append(f"{where} not an object")
            continue
        a, b, rel = e.get("a"), e.get("b"), e.get("rel")
        ok = resolve(a, where) & resolve(b, where)
        if rel not in REL_TYPES:
            failures.append(f"{where} bad rel {rel!r}")
            ok = False
        if ok:
            if (a, b, rel) in seen_edges:
                failures.append(f"{where} duplicate edge "
                                f"({a!r},{b!r},{rel!r})")
            seen_edges.add((a, b, rel))

    seen_anchors = set()
    for i, a in enumerate(anchors):
        where = f"anchors[{i}]"
        if not isinstance(a, dict):
            failures.append(f"{where} not an object")
            continue
        cid, st = a.get("concept_id"), a.get("status")
        resolve(cid, where)
        if st not in STATUSES + V7_STATUS_VOCAB:
            failures.append(f"{where} bad status {st!r}")
        gn = a.get("genre")
        if gn is not None and gn not in V7_GENRE_VOCAB:
            failures.append(f"{where} bad genre {gn!r}")
        if cid in seen_anchors:
            failures.append(f"{where} duplicate anchor for {cid!r}")
        seen_anchors.add(cid)
        if "note" in a and not isinstance(a["note"], str):
            failures.append(f"{where} bad note")

    if not isinstance(loops, list):
        failures.append("loops not a list")
    else:
        for i, l in enumerate(loops):
            if not isinstance(l, dict) or not resolve(l.get("concept_id"),
                                                       f"loops[{i}]"):
                failures.append(f"loops[{i}] bad entry {l!r}")

    if failures:
        raise ExtractionError(failures)

    # warnings (never fail)
    used = set()
    for s in strands:
        if s.get("label"):
            used.add(s["label"])
        used.update(s["concept_ids"])
    for e in edges:
        used.update((e["a"], e["b"]))
    for a in anchors:
        used.add(a["concept_id"])
    for l in loops:
        used.add(l["concept_id"])
    for cid in ids:
        if cid not in used:
            warnings.append(f"orphan concept {cid!r} "
                            f"({ids[cid]!r}): in no strand/edge/anchor/loop")
    return warnings


# --------------------------------------------------------------------------
# codec glue: extraction -> registry -> v5 wire -> verified round-trip
# --------------------------------------------------------------------------

def build_registry(doc):
    """Deterministic registry: vocab terms first (fixed order), then the
    doc's concepts in doc order. Rebuilding from the same doc gives the
    same registry, hence the same fingerprint."""
    reg = Registry()
    for t in REL_TYPES + STATUSES:
        reg.add(t)
    for c in doc["concepts"]:
        reg.add(c["label"], c.get("kind", ""))
    return reg


def to_v5_export(doc):
    """Strict-schema extraction -> the export shape codec.build_message_v5
    expects (names, not ids)."""
    lab = {c["id"]: c["label"] for c in doc["concepts"]}
    return {
        "strands": [
            {"label": lab[s["label"]] if s.get("label") else None,
             "nodes": [{"id": lab[i]} for i in s["concept_ids"]]}
            for s in doc["strands"]],
        "constraints": [
            {"a": lab[e["a"]], "b": lab[e["b"]], "type": e["rel"]}
            for e in doc["edges"]],
        "anchors": [
            {"id": lab[a["concept_id"]], "status": a["status"]}
            for a in doc["anchors"]],
        "open_loops": [
            {"node": lab[l["concept_id"]]} for l in doc.get("loops", [])],
    }


def to_v6_export(doc):
    """v5 export shape + anchor notes (str or None)."""
    exp = to_v5_export(doc)
    notes = [a.get("note") for a in doc["anchors"]]
    for ae, n in zip(exp["anchors"], notes):
        ae["note"] = n
    return exp


def _canon_struct(s):
    strands = sorted((x["label"] or "", tuple(sorted(x["members"])))
                     for x in s["strands"])
    edges = sorted((a, t, b) for a, t, b in s["edges"])
    anchors = sorted((c, st) for c, st in s["anchors"])
    return (strands, edges, anchors, tuple(sorted(s["loops"])))


def _canon_doc(doc):
    lab = {c["id"]: c["label"] for c in doc["concepts"]}
    strands = sorted(
        ((lab[s["label"]] if s.get("label") else "") or "",
         tuple(sorted(lab[i] for i in s["concept_ids"])))
        for s in doc["strands"])
    edges = sorted((lab[e["a"]], e["rel"], lab[e["b"]])
                   for e in doc["edges"])
    anchors = sorted((lab[a["concept_id"]], a["status"])
                     for a in doc["anchors"])
    loops = tuple(sorted(lab[l["concept_id"]]
                         for l in doc.get("loops", [])))
    return (strands, edges, anchors, loops)


def verify_roundtrip(doc):
    """Full deterministic path: build registry, encode v5, validate the
    wire, decode, and require canonical identity. Returns (ints, reg).
    Raises ExtractionError if anything disagrees."""
    reg = build_registry(doc)
    B = len(reg.names)
    primes = first_n_primes(B)
    try:
        ints = build_message_v5(to_v5_export(doc), reg, primes)
        validate_message_v5(ints, B, primes)
        struct = decode_struct_v5(ints, reg, primes)
    except Exception as exc:
        raise ExtractionError([f"codec round-trip failed: {exc}"])
    if _canon_struct(struct) != _canon_doc(doc):
        raise ExtractionError(["codec round-trip changed the structure "
                               "(silent drop or reorder)"])
    return ints, reg


def _canon_struct_v6(struct, notes):
    strands = sorted((x["label"] or "", tuple(sorted(x["members"])))
                     for x in struct["strands"])
    edges = sorted((a, t, b) for a, t, b in struct["edges"])
    anchors = sorted((a["concept"], a["status"], a["note"] or "")
                     for a in struct["anchors"])
    statuses = {e["concept"]: (e["status"], e["valid_from"],
                               e["valid_until"] or 0)
                for e in struct["entity_status"]}
    return (strands, edges, anchors, tuple(sorted(notes)),
            statuses, tuple(sorted(struct["loops"])))


def _canon_doc_v6(doc, epoch):
    lab = {c["id"]: c["label"] for c in doc["concepts"]}
    strands = sorted(
        ((lab[s["label"]] if s.get("label") else "") or "",
         tuple(sorted(lab[i] for i in s["concept_ids"])))
        for s in doc["strands"])
    edges = sorted((lab[e["a"]], e["rel"], lab[e["b"]])
                   for e in doc["edges"])
    anchors = sorted((lab[a["concept_id"]],
                      V6_STATUS_NAMES[v6_status_of(a["status"])],
                      a.get("note") or "")
                     for a in doc["anchors"])
    notes = sorted({a.get("note") for a in doc["anchors"] if a.get("note")})
    # expected entity statuses: same derivation as codec._v6_entity_statuses
    per = {}
    for a in doc["anchors"]:
        c0 = lab[a["concept_id"]]
        s = v6_status_of(a["status"])
        per.setdefault(c0, []).append(s)
    statuses = {}
    for c0, ss in per.items():
        term = [x for x in ss if x >= 4]
        s = max(term) if term else max(ss)
        statuses[c0] = (V6_STATUS_NAMES[s], epoch, 0)
    loops = tuple(sorted(lab[l["concept_id"]]
                         for l in doc.get("loops", [])))
    return (strands, edges, anchors, tuple(notes), statuses, loops)


def verify_roundtrip_v6(doc, epoch=1):
    """Full deterministic v6 path: build registry, encode v6 (with notes
    + entity statuses), validate, wire-encode, wire-decode, struct-decode,
    and require canonical identity including notes and statuses.
    Returns (ints, notes, reg). Raises ExtractionError on disagreement."""
    reg = build_registry(doc)
    B = len(reg.names)
    E = epoch + 1
    primes = first_n_primes(B)
    try:
        ints, notes = build_message_v6(to_v6_export(doc), reg, primes,
                                       epoch)
        validate_message_v6(ints, B, E, primes)
        body = encode_wire_v6(ints, notes)
        ints2, notes2 = decode_wire_v6(body)
        assert ints2 == ints and notes2 == notes, "wire codec mismatch"
        struct = decode_struct_v6(ints2, notes2, reg, primes)
    except Exception as exc:
        raise ExtractionError([f"v6 codec round-trip failed: {exc}"])
    if _canon_struct_v6(struct, notes2) != _canon_doc_v6(doc, epoch):
        raise ExtractionError(["v6 codec round-trip changed the structure "
                               "(silent drop or reorder)"])
    return ints, notes, reg


def to_v7_export(doc):
    """v6 export shape + anchor notes (str or None) + anchor genre
    (str or None; legacy docs carry none -> genre 0)."""
    exp = to_v6_export(doc)
    for ae, a in zip(exp["anchors"], doc["anchors"]):
        ae["genre"] = a.get("genre")
    return exp


def _canon_struct_v7(struct, notes):
    strands = sorted((x["label"] or "", tuple(sorted(x["members"])))
                     for x in struct["strands"])
    edges = sorted((a, t, b) for a, t, b in struct["edges"])
    anchors = sorted((a["concept"], a["status"], a["genre"],
                      a["note"] or "")
                     for a in struct["anchors"])
    statuses = {e["concept"]: (e["status"], e["valid_from"],
                               e["valid_until"] or 0)
                for e in struct["entity_status"]}
    return (strands, edges, anchors, tuple(sorted(notes)),
            statuses, tuple(sorted(struct["loops"])))


def _canon_doc_v7(doc, epoch):
    lab = {c["id"]: c["label"] for c in doc["concepts"]}
    strands = sorted(
        ((lab[s["label"]] if s.get("label") else "") or "",
         tuple(sorted(lab[i] for i in s["concept_ids"])))
        for s in doc["strands"])
    edges = sorted((lab[e["a"]], e["rel"], lab[e["b"]])
                   for e in doc["edges"])
    anchors = sorted((lab[a["concept_id"]],
                      V7_STATUS_NAMES[v7_status_of(a["status"])],
                      V7_GENRE_NAMES[v7_genre_of(a.get("genre"))],
                      a.get("note") or "")
                     for a in doc["anchors"])
    notes = sorted({a.get("note") for a in doc["anchors"] if a.get("note")})
    # expected entity statuses: same derivation as codec._v7_entity_statuses
    per = {}
    for a in doc["anchors"]:
        c0 = lab[a["concept_id"]]
        s = v7_status_of(a["status"])
        per.setdefault(c0, []).append(s)
    statuses = {}
    for c0, ss in per.items():
        term = [x for x in ss if x >= 5]
        s = max(term) if term else max(ss)
        statuses[c0] = (V7_STATUS_NAMES[s], epoch, 0)
    loops = tuple(sorted(lab[l["concept_id"]]
                         for l in doc.get("loops", [])))
    return (strands, edges, anchors, tuple(notes), statuses, loops)


def verify_roundtrip_v7(doc, epoch=1):
    """Full deterministic v7 path: build registry, encode v7 (notes +
    entity statuses + genre), validate, wire-encode, wire-decode,
    struct-decode, and require canonical identity including statuses,
    genres, and notes. Returns (ints, notes, reg). Raises
    ExtractionError on disagreement."""
    reg = build_registry(doc)
    B = len(reg.names)
    E = epoch + 1
    primes = first_n_primes(B)
    try:
        ints, notes = build_message_v7(to_v7_export(doc), reg, primes,
                                       epoch)
        validate_message_v7(ints, B, E, primes)
        body = encode_wire_v7(ints, notes)
        ints2, notes2 = decode_wire_v7(body)
        assert ints2 == ints and notes2 == notes, "wire codec mismatch"
        struct = decode_struct_v7(ints2, notes2, reg, primes)
    except Exception as exc:
        raise ExtractionError([f"v7 codec round-trip failed: {exc}"])
    if _canon_struct_v7(struct, notes2) != _canon_doc_v7(doc, epoch):
        raise ExtractionError(["v7 codec round-trip changed the structure "
                               "(silent drop or reorder)"])
    return ints, notes, reg


# --------------------------------------------------------------------------
# SQLite store (scope 3.4)
# --------------------------------------------------------------------------

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS concepts(
  id INTEGER PRIMARY KEY, label TEXT UNIQUE NOT NULL, kind TEXT NOT NULL,
  status TEXT, first_seen_session INTEGER NOT NULL, seq INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS strands(
  id INTEGER PRIMARY KEY, label_concept_id INTEGER, session INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS strand_members(
  strand_id INTEGER NOT NULL, concept_id INTEGER NOT NULL,
  PRIMARY KEY (strand_id, concept_id));
CREATE TABLE IF NOT EXISTS edges(
  a INTEGER NOT NULL, b INTEGER NOT NULL, rel TEXT NOT NULL,
  PRIMARY KEY (a, b, rel));
CREATE TABLE IF NOT EXISTS anchors(
  concept_id INTEGER PRIMARY KEY, status TEXT NOT NULL, note TEXT);
CREATE TABLE IF NOT EXISTS checkpoints(
  id INTEGER PRIMARY KEY, session INTEGER NOT NULL,
  wire_lines TEXT NOT NULL, registry_json TEXT NOT NULL,
  fingerprint INTEGER NOT NULL, n_concepts INTEGER NOT NULL,
  created REAL NOT NULL);
"""


def open_db(path=":memory:"):
    db = sqlite3.connect(path)
    db.executescript(SCHEMA_SQL)
    return db


_NORM_RE = re.compile(r"\W+")


def _norm(label):
    return _NORM_RE.sub("", label).casefold()


def merge_extraction(doc, db, session):
    """Insert a verified extraction. Phase-1 entity resolution: exact
    label match reuses the concept; a normalized-but-not-exact match is
    inserted as new AND surfaced for human adjudication (no silent
    merge). Returns {"concept_rows": {doc_id: rowid}, "adjudications": [...]}.
    """
    validate_extraction(doc)  # merge never accepts unverified structure
    cur = db.cursor()
    existing = {r[0]: (r[1], r[2])
                for r in cur.execute("SELECT label, id, label FROM concepts")}
    norm_index = {_norm(lab): lab for lab in existing}
    concept_rows, adjudications = {}, []
    seq = cur.execute("SELECT COALESCE(MAX(seq), -1) FROM concepts"
                      ).fetchone()[0] + 1
    for c in doc["concepts"]:
        lab = c["label"]
        if lab in existing:
            concept_rows[c["id"]] = existing[lab][0]
            continue
        nl = _norm(lab)
        if nl in norm_index:
            adjudications.append({"proposed": lab,
                                  "candidate": norm_index[nl],
                                  "action": "needs_human"})
        cur.execute("INSERT INTO concepts(label, kind, first_seen_session,"
                    " seq) VALUES (?,?,?,?)",
                    (lab, c["kind"], session, seq))
        seq += 1
        concept_rows[c["id"]] = cur.lastrowid
    for s in doc["strands"]:
        lab_cid = s.get("label")
        cur.execute("INSERT INTO strands(label_concept_id, session)"
                    " VALUES (?,?)",
                    (concept_rows[lab_cid] if lab_cid else None, session))
        sid = cur.lastrowid
        for m in s["concept_ids"]:
            cur.execute("INSERT OR IGNORE INTO strand_members"
                        "(strand_id, concept_id) VALUES (?,?)",
                        (sid, concept_rows[m]))
    for e in doc["edges"]:
        cur.execute("INSERT OR IGNORE INTO edges(a, b, rel) VALUES (?,?,?)",
                    (concept_rows[e["a"]], concept_rows[e["b"]], e["rel"]))
    for a in doc["anchors"]:
        cur.execute("INSERT OR REPLACE INTO anchors(concept_id, status, note)"
                    " VALUES (?,?,?)",
                    (concept_rows[a["concept_id"]], a["status"],
                     a.get("note")))
        cur.execute("UPDATE concepts SET status=? WHERE id=?",
                    (a["status"], concept_rows[a["concept_id"]]))
    db.commit()
    return {"concept_rows": concept_rows, "adjudications": adjudications}


# --------------------------------------------------------------------------
# checkpoint / restore (telomere-wrapped multiline v5 wire)
# --------------------------------------------------------------------------

def checkpoint(doc, db, session):
    """Verify, merge, encode, and store a self-contained checkpoint.
    Returns the checkpoint id."""
    if not 0 <= session <= MAX_TELOMERE_CTX:
        raise ValueError("session out of telomere range")
    warnings = validate_extraction(doc)
    merge_extraction(doc, db, session)
    ints, reg = verify_roundtrip(doc)
    B = len(reg.names)
    if B > MAX_TELOMERE_CTX:
        raise ValueError(f"registry size {B} exceeds telomere context")
    fp = registry_fingerprint(reg)
    lines = encode_lines_balanced(ints)
    wrapped = [wrap_telomere(ln, WIRE_VERSION, B, fp, session)
               for ln in lines]
    cur = db.cursor()
    cur.execute("INSERT INTO checkpoints(session, wire_lines, registry_json,"
                " fingerprint, n_concepts, created) VALUES (?,?,?,?,?,?)",
                (session, json.dumps(wrapped),
                 json.dumps({"names": reg.names,
                             "kinds": {c["label"]: c.get("kind", "")
                                       for c in doc["concepts"]}}),
                 fp, len(doc["concepts"]), time.time()))
    db.commit()
    return cur.lastrowid, warnings


def _registry_from_snapshot(snap):
    reg = Registry()
    for t in REL_TYPES + STATUSES:
        reg.add(t)
    kinds = snap.get("kinds", {})
    for name in snap["names"]:
        if name not in reg.content:
            reg.add(name, kinds.get(name, ""))
    return reg


def restore(checkpoint_id, db):
    """Load a checkpoint, scan its telomere-wrapped lines (order does not
    matter), validate everything, and return (struct, registry)."""
    row = db.execute("SELECT session, wire_lines, registry_json, fingerprint"
                     " FROM checkpoints WHERE id=?",
                     (checkpoint_id,)).fetchone()
    if not row:
        raise KeyError(f"no checkpoint {checkpoint_id}")
    session, wire_lines, registry_json, fp = row
    text = "\n".join(json.loads(wire_lines))
    bodies = []
    for ctx, body in scan_telomeres(text):
        if ctx["version"] != WIRE_VERSION:
            raise ExtractionError(
                [f"checkpoint {checkpoint_id}: wire version "
                 f"{ctx['version']} != {WIRE_VERSION}"])
        if ctx["session"] != session:
            raise ExtractionError(
                [f"checkpoint {checkpoint_id}: session cap mismatch"])
        bodies.append(body)
    if not bodies:
        raise ExtractionError([f"checkpoint {checkpoint_id}: "
                               "no valid telomere lines found"])
    ints = decode_lines(bodies)  # order-independent reassembly
    reg = _registry_from_snapshot(json.loads(registry_json))
    B = len(reg.names)
    validate_message_v5(ints, B, first_n_primes(B))
    if registry_fingerprint(reg) != fp:
        raise ExtractionError([f"checkpoint {checkpoint_id}: "
                               "registry fingerprint mismatch"])
    struct = decode_struct_v5(ints, reg, first_n_primes(B))
    return struct, reg


# --------------------------------------------------------------------------
# read path, phase-1 minimal: grouped compact injection (scope 3.6)
# --------------------------------------------------------------------------

def legend_for(reg):
    return {i + 1: n for i, n in enumerate(reg.names)}


def inject_grouped(struct, reg):
    """Subject-grouped minimal injection (scale-test syntax):
    S<label>: members / E<subj>: rel obj,... / A: c s,... / L: loops."""
    idx = {n: i + 1 for i, n in enumerate(reg.names)}
    lines = []
    for s in struct["strands"]:
        li = idx[s["label"]] if s["label"] else 0
        ms = " ".join(str(idx[m]) for m in
                      sorted(s["members"], key=lambda m: idx[m]))
        lines.append(f"S{li}:" + ms)
    bys = {}
    for a, t, b in struct["edges"]:
        bys.setdefault(idx[a], []).append((idx[t], idx[b]))
    for a in sorted(bys):
        lines.append("E%d:" % a +
                     ",".join("%d %d" % p for p in sorted(bys[a])))
    lines.append("A:" + ",".join(
        "%d %d" % (idx[c], idx[st])
        for c, st in sorted(struct["anchors"], key=lambda p: idx[p[0]])))
    lines.append("L:" + " ".join(
        str(idx[l]) for l in sorted(struct["loops"], key=lambda l: idx[l])))
    return "\n".join(lines)


def inject_grouped_r3(doc, reg):
    """R3 injection: LEGEND + grouped structure + anchor notes (N-lines).

    M3 P6 found anchor notes were extracted but dropped by the injection;
    R3 makes notes live payload (numbers/evidence ride there). One N-line
    per anchor carrying a non-empty note: N<idx>: <note>. Takes the
    extraction doc (which has notes), not the wire-decoded struct.
    """
    lab = {c["id"]: c["label"] for c in doc["concepts"]}
    idx = {n: i + 1 for i, n in enumerate(reg.names)}
    lines = ["LEGEND (index: label):"]
    for i, n in enumerate(reg.names):
        lines.append("%d: %s" % (i + 1, n))
    lines.append("")
    lines.append("INJECTED STRUCTURE (grouped compact):")
    lines.append("")
    for s in doc["strands"]:
        li = idx[lab[s["label"]]] if s.get("label") else 0
        ms = " ".join(str(idx[lab[i]]) for i in
                      sorted(s["concept_ids"], key=lambda i: idx[lab[i]]))
        lines.append("S%d:" % li + ms)
    bys = {}
    for e in doc["edges"]:
        a, t, b = lab[e["a"]], e["rel"], lab[e["b"]]
        bys.setdefault(idx[a], []).append((idx[t], idx[b]))
    for a in sorted(bys):
        lines.append("E%d:" % a +
                     ",".join("%d %d" % p for p in sorted(bys[a])))
    lines.append("A:" + ",".join(
        "%d %d" % (idx[lab[a["concept_id"]]], idx[a["status"]])
        for a in sorted(doc["anchors"],
                        key=lambda a: idx[lab[a["concept_id"]]])))
    lines.append("L:" + " ".join(
        str(idx[lab[l["concept_id"]]])
        for l in sorted(doc.get("loops", []),
                        key=lambda l: idx[lab[l["concept_id"]]])))
    for a in sorted(doc["anchors"], key=lambda a: idx[lab[a["concept_id"]]]):
        note = (a.get("note") or "").strip()
        if note:
            lines.append("N%d: %s" % (idx[lab[a["concept_id"]]], note))
    return "\n".join(lines)
