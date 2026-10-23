#!/usr/bin/env python3
"""Validate Atlas-2 extraction JSON files against the pilot schema.
Usage: python3 validate_atlas2.py <extractions_dir>
Reports per-file pass/fail with specific errors. Mechanical repairs only.
"""
import json, sys, glob, os

STATUSES = {"exact", "computationally_verified", "conjectural", "heuristic", "killed"}
REQUIRED_TOP = {"anchors", "concepts", "edges", "loops", "strands"}

def validate_file(path):
    errors = []
    try:
        with open(path) as f:
            d = json.load(f)
    except Exception as e:
        return [f"JSON parse error: {e}"]
    if not isinstance(d, dict):
        return ["top level is not an object"]
    missing = REQUIRED_TOP - set(d.keys())
    if missing:
        errors.append(f"missing top-level keys: {sorted(missing)}")
    concepts = d.get("concepts", [])
    cids = set()
    for i, c in enumerate(concepts):
        if not isinstance(c, dict):
            errors.append(f"concepts[{i}] not an object"); continue
        for k in ("id", "kind", "label"):
            if k not in c:
                errors.append(f"concepts[{i}] missing '{k}'")
        cid = c.get("id")
        if cid in cids:
            errors.append(f"duplicate concept id: {cid}")
        cids.add(cid)
    for i, a in enumerate(d.get("anchors", [])):
        if not isinstance(a, dict):
            errors.append(f"anchors[{i}] not an object"); continue
        cid = a.get("concept_id")
        if cid not in cids:
            errors.append(f"anchors[{i}] dangling concept_id: {cid}")
        st = a.get("status")
        if st not in STATUSES:
            errors.append(f"anchors[{i}] bad status: {st!r}")
        if "note" not in a:
            errors.append(f"anchors[{i}] missing 'note'")
    for i, e in enumerate(d.get("edges", [])):
        if not isinstance(e, dict):
            errors.append(f"edges[{i}] not an object"); continue
        for end in ("a", "b"):
            if e.get(end) not in cids:
                errors.append(f"edges[{i}] dangling {end}: {e.get(end)}")
        if "rel" not in e:
            errors.append(f"edges[{i}] missing 'rel'")
    for i, l in enumerate(d.get("loops", [])):
        if not isinstance(l, dict) or l.get("concept_id") not in cids:
            errors.append(f"loops[{i}] bad/dangling: {l}")
    for i, s in enumerate(d.get("strands", [])):
        if not isinstance(s, dict):
            errors.append(f"strands[{i}] not an object"); continue
        for cid in s.get("concept_ids", []):
            if cid not in cids:
                errors.append(f"strands[{i}] dangling concept_id: {cid}")
    # coverage: every concept should have at least one anchor
    anchored = {a.get("concept_id") for a in d.get("anchors", []) if isinstance(a, dict)}
    unanchored = cids - anchored
    if unanchored:
        errors.append(f"concepts without anchors: {sorted(unanchored)}")
    return errors

def main():
    ddir = sys.argv[1] if len(sys.argv) > 1 else "extractions"
    files = sorted(glob.glob(os.path.join(ddir, "*.json")))
    npass, nfail = 0, 0
    for path in files:
        errs = validate_file(path)
        name = os.path.basename(path)
        if errs:
            nfail += 1
            print(f"FAIL {name}")
            for e in errs:
                print(f"   - {e}")
        else:
            npass += 1
            print(f"ok   {name}")
    print(f"\n{len(files)} files: {npass} pass, {nfail} fail")
    return 1 if nfail else 0

if __name__ == "__main__":
    sys.exit(main())
