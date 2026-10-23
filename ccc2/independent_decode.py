#!/usr/bin/env python3
"""CCC-2 independent wire decoder (fidelity control).

Written from ~/workspace/ccc-prototype/ccc2/SPEC.md (ccc2-wire/1) alone.
Standard library only. No project code read or reused.

Usage:
    python3 independent_decode.py <wire-file>

The wire file may be the telomere-wrapped wire (TELOMERE-CCC2-1:<payload>:TELOMERE-CCC2-1)
or the bare JSON wire object. Decoded records are printed to stdout as JSON:
a list of record dicts with `checksum` stripped. Any wire/record checksum
mismatch or well-formedness violation aborts with the spec error code on
stderr and a nonzero exit status.

Exit codes:
    0  decoded successfully
    2  WIRE-CHECKSUM-MISMATCH
    3  RECORD-CHECKSUM-MISMATCH
    4  MALFORMED
"""

import hashlib
import json
import re
import sys

FORMAT = "ccc2-wire/1"
TELOMERE = "TELOMERE-CCC2-1"

# SPEC.md §3 — the label vocabulary (first language).
LABELS = {
    "exact",
    "computationally_verified",
    "conjectural",
    "heuristic",
    "killed",
    "superseded",
    "unstated",
}

# SPEC.md §2 (L records) — the validated relation vocabulary.
RELS = {
    "supports",
    "contradicts",
    "bounds",
    "generalizes",
    "implements",
    "depends_on",
    "causes",
    "measures",
    "defines",
    "exemplifies",
    "refines",
    "supersedes",
}

ID_RE = re.compile(r"^(D|G|V|B|C|L)(\d+)$")
RECORD_TYPES = {"D", "G", "V", "B", "C", "L"}
C_KINDS = {"claim", "definition", "question"}
GENRES = {"original", "reframed", "identification"}


class DecodeError(Exception):
    code = "MALFORMED"


class WireChecksumMismatch(DecodeError):
    code = "WIRE-CHECKSUM-MISMATCH"


class RecordChecksumMismatch(DecodeError):
    code = "RECORD-CHECKSUM-MISMATCH"

    def __init__(self, record_id):
        self.record_id = record_id
        super().__init__("record id: %s" % record_id)


class Malformed(DecodeError):
    def __init__(self, field, record_id):
        self.field = field
        self.record_id = record_id
        super().__init__("field '%s', record id: %s" % (field, record_id))


def canonical(obj):
    """Canonical serialization per §4: JSON, keys sorted, no whitespace.

    Judgment call: "no whitespace" is realized as separators=(",", ":").
    ensure_ascii=False is used so non-ASCII text is encoded as UTF-8
    bytes rather than \\uXXXX escapes (the spec does not say either way).
    """
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unwrap_telomere(text: str) -> str:
    s = text.strip()
    prefix = TELOMERE + ":"
    suffix = ":" + TELOMERE
    if s.startswith(prefix):
        if not s.endswith(suffix) or len(s) <= len(prefix) + len(suffix):
            raise Malformed("telomere wrap (opened but not closed)", "wire")
        return s[len(prefix): -len(suffix)]
    return s


def check_label(value, field, record_id):
    if value not in LABELS:
        raise Malformed("%s (not in §3 label list)" % field, record_id)


def check_nonempty_str(value, field, record_id):
    if not isinstance(value, str) or not value.strip():
        raise Malformed("%s (required non-empty string)" % field, record_id)


def check_id(value, record_id):
    """Id format per §2: type letter + number, matching the record's type."""
    m = ID_RE.match(value) if isinstance(value, str) else None
    if m is None:
        raise Malformed("id (format <type-letter><number>)", record_id)


def check_boundary(value, record_id):
    """§5.4: honest_boundary must state a stop-line, not a bare status word.

    Judgment call: "bare status word" is interpreted as the boundary
    being exactly one of the §3 label values (e.g. "computationally_verified").
    A substantive stop-line containing label words in context passes.
    """
    check_nonempty_str(value, "honest_boundary", record_id)
    if value.strip().lower() in LABELS:
        raise Malformed("honest_boundary (bare status word, not a stop-line)", record_id)


def check_generates(stages, record_id):
    if not isinstance(stages, list):
        raise Malformed("generates (required list of stages)", record_id)
    for i, st in enumerate(stages):
        tag = "generates[%d]" % i
        if not isinstance(st, dict):
            raise Malformed(tag, record_id)
        check_nonempty_str(st.get("stage"), tag + ".stage", record_id)
        # §5.4: every generates stage must have a prescription.
        check_nonempty_str(st.get("prescription"), tag + ".prescription", record_id)


def check_verified(checks, record_id):
    if not isinstance(checks, list):
        raise Malformed("verified (required list of checks)", record_id)
    for i, c in enumerate(checks):
        tag = "verified[%d]" % i
        if not isinstance(c, dict):
            raise Malformed(tag, record_id)
        check_nonempty_str(c.get("check"), tag + ".check", record_id)
        pending = bool(c.get("pending"))
        if pending:
            # Pending checks carry a criterion instead of expected (§2).
            check_nonempty_str(c.get("criterion"), tag + ".criterion", record_id)
            if "expected" in c:
                raise Malformed(tag + " (pending check must not carry expected)", record_id)
        else:
            if "expected" not in c:
                raise Malformed(tag + ".expected", record_id)


def check_record_D(rec, rid):
    check_nonempty_str(rec.get("subtitle"), "subtitle", rid)
    check_nonempty_str(rec.get("rule"), "rule", rid)
    if "conventions" in rec:
        conv = rec["conventions"]
        if not isinstance(conv, list) or not all(isinstance(x, str) for x in conv):
            raise Malformed("conventions (optional; must be a list of strings)", rid)
    check_generates(rec.get("generates"), rid)
    check_verified(rec.get("verified"), rid)
    check_boundary(rec.get("honest_boundary"), rid)
    if "honest_label" not in rec:
        raise Malformed("honest_label", rid)
    check_label(rec["honest_label"], "honest_label", rid)
    if "genre" in rec and rec["genre"] not in GENRES:
        raise Malformed("genre (must be original|reframed|identification)", rid)


def check_record_G(rec, rid):
    for field in ("title", "verdict", "tried", "result", "transfer"):
        check_nonempty_str(rec.get(field), field, rid)


def check_record_V(rec, rid):
    check_nonempty_str(rec.get("subject"), "subject", rid)
    if "status" not in rec:
        raise Malformed("status", rid)
    check_label(rec["status"], "status", rid)
    check_nonempty_str(rec.get("consequence"), "consequence", rid)


def check_record_B(rec, rid):
    for field in ("x", "y", "buys", "limits"):
        check_nonempty_str(rec.get(field), field, rid)


def check_record_C(rec, rid):
    if rec.get("kind") not in C_KINDS:
        raise Malformed("kind (claim|definition|question)", rid)
    check_nonempty_str(rec.get("label"), "label", rid)
    if "status" not in rec:
        raise Malformed("status", rid)
    check_label(rec["status"], "status", rid)
    if rec["kind"] == "question":
        # §2: "Open questions take unstated (questions are not claims)."
        if rec["status"] != "unstated":
            raise Malformed("status (open question must be unstated)", rid)
    else:
        # Judgment call: non-question content is a claim/definition, so the
        # "unstated" label (the question marker) must not appear on it.
        if rec["status"] == "unstated":
            raise Malformed("status (unstated is reserved for questions)", rid)
    if "note" in rec and not isinstance(rec["note"], str):
        raise Malformed("note (NOTETEXT literal)", rid)


def check_record_L(rec, rid, known_ids):
    for field in ("from", "to"):
        value = rec.get(field)
        if not isinstance(value, str) or ID_RE.match(value) is None:
            raise Malformed(field + " (record id)", rid)
        # Judgment call: a link must reference records present in the wire.
        if value not in known_ids:
            raise Malformed(field + " (references unknown record id)", rid)
    if rec.get("rel") not in RELS:
        raise Malformed("rel (not in §2 relation list)", rid)


CHECKERS = {
    "D": check_record_D,
    "G": check_record_G,
    "V": check_record_V,
    "B": check_record_B,
    "C": check_record_C,
}


def decode_wire(text):
    """Decode a CCC-2 wire. Returns the record list, checksums stripped.

    Raises WireChecksumMismatch, RecordChecksumMismatch, or Malformed.
    """
    payload = unwrap_telomere(text)
    try:
        wire = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise Malformed("wire JSON", "wire") from exc

    if not isinstance(wire, dict) or wire.get("format") != FORMAT:
        raise Malformed("format (must be %r)" % FORMAT, "wire")

    records = wire.get("records")
    if not isinstance(records, list):
        raise Malformed("records (list)", "wire")

    registry = wire.get("registry")
    if not isinstance(registry, dict):
        raise Malformed("registry (id -> type index)", "wire")

    if "wire_checksum" not in wire or not isinstance(wire["wire_checksum"], str):
        raise Malformed("wire_checksum", "wire")

    # --- §5.2: wire checksum from record checksums (as carried), id order.
    carried = {}
    for rec in records:
        if not isinstance(rec, dict):
            raise Malformed("record (object)", "wire")
        rid = rec.get("id")
        cs = rec.get("checksum")
        check_id(rid, rid if isinstance(rid, str) else "wire")
        if not isinstance(cs, str):
            raise Malformed("checksum", rid)
        if rid in carried:
            raise Malformed("id (duplicate within wire)", rid)
        carried[rid] = cs

    # Judgment call: "in id order" = lexicographic order on the id strings.
    wire_input = "".join(carried[rid] for rid in sorted(carried))
    if sha256_hex(wire_input.encode("utf-8")) != wire["wire_checksum"]:
        raise WireChecksumMismatch("wire checksum does not match")

    # --- §5.3: per-record checksum recomputation.
    for rec in records:
        rid = rec["id"]
        body = {k: v for k, v in rec.items() if k != "checksum"}
        if sha256_hex(canonical(body)) != rec["checksum"]:
            raise RecordChecksumMismatch(rid)

    # --- §5.4: well-formedness.
    known_ids = set(carried)
    if set(registry.keys()) != known_ids:
        raise Malformed("registry (must index exactly the record ids)", "wire")
    for rec in records:
        rid = rec["id"]
        rtype = rec.get("type")
        if rtype not in RECORD_TYPES:
            raise Malformed("type (one of D,G,V,B,C,L)", rid)
        m = ID_RE.match(rid)
        if m.group(1) != rtype:
            raise Malformed("id (type letter must match type field)", rid)
        if registry.get(rid) != rtype:
            raise Malformed("registry (type mismatch for id)", rid)
        if rtype == "L":
            check_record_L(rec, rid, known_ids)
        else:
            CHECKERS[rtype](rec, rid)

    # --- output: records with checksums stripped (§5.6: fields/labels verbatim).
    return [{k: v for k, v in rec.items() if k != "checksum"} for rec in records]


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: python3 independent_decode.py <wire-file>\n")
        return 1
    with open(argv[1], "r", encoding="utf-8") as fh:
        text = fh.read()
    try:
        decoded = decode_wire(text)
    except DecodeError as exc:
        sys.stderr.write("%s: %s\n" % (exc.code, exc))
        return {"WIRE-CHECKSUM-MISMATCH": 2,
                "RECORD-CHECKSUM-MISMATCH": 3}.get(exc.code, 4)
    sys.stdout.write(json.dumps(decoded, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
