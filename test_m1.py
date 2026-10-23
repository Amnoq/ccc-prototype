"""test_m1.py -- M1 acceptance (HARNESS_MVP_SCOPE.md).

Done when: a hand-written extraction passes the verifier, merges,
checkpoints, restores from shuffled telomere lines, and injects --
and the verifier rejects every malformed extraction below.
"""
import copy
import json
import random

import memory_harness as mh

DOC = {
    "concepts": [
        {"id": "c1", "label": "prime product encoding", "kind": "method"},
        {"id": "c2", "label": "shared codebook", "kind": "entity"},
        {"id": "c3", "label": "Elias-gamma wire", "kind": "method"},
        {"id": "c4", "label": "model-as-parser", "kind": "claim"},
        {"id": "c5", "label": "harness-parses", "kind": "claim"},
        {"id": "c6", "label": "2.2x steady-state", "kind": "result"},
        {"id": "c7", "label": "prompt caching", "kind": "entity"},
        {"id": "c8", "label": "cost play", "kind": "claim"},
        {"id": "c9", "label": "capacity play", "kind": "claim"},
        {"id": "c10", "label": "extractor gating", "kind": "open_question"},
    ],
    "strands": [
        {"id": "s1", "label": "c1",
         "concept_ids": ["c1", "c2", "c3"]},
        {"id": "s2", "label": "c9",
         "concept_ids": ["c4", "c5", "c6", "c7", "c8", "c9"]},
    ],
    "edges": [
        {"a": "c3", "b": "c1", "rel": "supports"},
        {"a": "c2", "b": "c1", "rel": "supports"},
        {"a": "c4", "b": "c5", "rel": "contradicts"},
        {"a": "c6", "b": "c1", "rel": "refines"},
        {"a": "c7", "b": "c8", "rel": "contradicts"},
        {"a": "c6", "b": "c9", "rel": "supports"},
    ],
    "anchors": [
        {"concept_id": "c5", "status": "verified",
         "note": "decisive Test A"},
        {"concept_id": "c8", "status": "superseded",
         "note": "killed by prompt caching"},
    ],
    "loops": [{"concept_id": "c10"}],
}

passed, failed = [], []


def check(name, fn):
    try:
        fn()
        passed.append(name)
    except Exception as e:  # noqa: BLE001
        failed.append((name, f"{type(e).__name__}: {e}"))


def expect_reject(name, doc):
    def fn():
        try:
            mh.validate_extraction(doc)
        except mh.ExtractionError:
            return
        raise AssertionError("verifier accepted a bad extraction")
    check(name, fn)


def mutate(path, value):
    d = copy.deepcopy(DOC)
    node = d
    for k in path[:-1]:
        node = node[k]
    node[path[-1]] = value
    return d


# --- happy path -----------------------------------------------------------
def happy_path():
    db = mh.open_db()
    cp_id, warnings = mh.checkpoint(DOC, db, session=1)
    assert not warnings, warnings
    # restore from shuffled lines scattered in noise: order-independence
    row = db.execute("SELECT wire_lines FROM checkpoints WHERE id=?",
                     (cp_id,)).fetchone()
    lines = json.loads(row[0])
    random.Random(7).shuffle(lines)
    db.execute("UPDATE checkpoints SET wire_lines=? WHERE id=?",
               (json.dumps(lines), cp_id))
    db.commit()
    struct, reg = mh.restore(cp_id, db)
    assert mh._canon_struct(struct) == mh._canon_doc(DOC), "restore mismatch"
    inj = mh.inject_grouped(struct, reg)
    leg = mh.legend_for(reg)
    assert inj.startswith("S"), "injection empty"
    assert len(leg) == len(reg.names)
    # every concept label appears in the legend
    for c in DOC["concepts"]:
        assert c["label"] in leg.values(), c["label"]
    # determinism: second checkpoint of the same doc, same fingerprint
    cp2, _ = mh.checkpoint(DOC, db, session=1)
    r1 = db.execute("SELECT fingerprint FROM checkpoints WHERE id=?",
                    (cp_id,)).fetchone()[0]
    r2 = db.execute("SELECT fingerprint FROM checkpoints WHERE id=?",
                    (cp2,)).fetchone()[0]
    assert r1 == r2, "fingerprint not deterministic"
    # merge reused concepts: still 10 concept rows, not 20
    n = db.execute("SELECT COUNT(*) FROM concepts").fetchone()[0]
    assert n == 10, f"expected 10 concepts after re-merge, got {n}"


check("happy path: verify/merge/checkpoint/restore/inject", happy_path)


def orphan_warning():
    d = copy.deepcopy(DOC)
    d["concepts"].append({"id": "c11", "label": "stray thought",
                          "kind": "claim"})
    w = mh.validate_extraction(d)  # must NOT raise
    assert any("c11" in x for x in w), f"no orphan warning: {w}"


check("orphan concept warns, does not fail", orphan_warning)


def adjudication_surface():
    db = mh.open_db()
    mh.checkpoint(DOC, db, session=1)
    d = copy.deepcopy(DOC)
    d["concepts"][0] = {"id": "c1b", "label": "Prime Product Encoding",
                        "kind": "method"}  # normalized match, new label
    for s in d["strands"]:
        s["concept_ids"] = ["c1b" if x == "c1" else x for x in s["concept_ids"]]
        if s["label"] == "c1":
            s["label"] = "c1b"
    for e in d["edges"]:
        for k in ("a", "b"):
            if e[k] == "c1":
                e[k] = "c1b"
    res = mh.merge_extraction(d, db, session=2)
    assert len(res["adjudications"]) == 1, res["adjudications"]
    assert res["adjudications"][0]["candidate"] == "prime product encoding"


check("near-match concept surfaced for adjudication", adjudication_surface)


# --- verifier negatives ----------------------------------------------------
expect_reject("bad rel rejected", mutate(("edges", 0, "rel"), "frobnicate"))
expect_reject("dangling edge endpoint rejected", mutate(("edges", 0, "a"), "c99"))
expect_reject("duplicate edge rejected",
              {**copy.deepcopy(DOC),
               "edges": DOC["edges"] + [copy.deepcopy(DOC["edges"][0])]})
expect_reject("empty strand rejected", mutate(("strands", 0, "concept_ids"), []))
expect_reject("bad status rejected", mutate(("anchors", 0, "status"), "maybe"))
expect_reject("duplicate anchor rejected",
              {**copy.deepcopy(DOC),
               "anchors": DOC["anchors"] + [copy.deepcopy(DOC["anchors"][0])]})
expect_reject("bad strand label rejected", mutate(("strands", 0, "label"), "c99"))
expect_reject("bad loop concept rejected", mutate(("loops", 0, "concept_id"), "c99"))
expect_reject("duplicate concept id rejected", mutate(("concepts", 1, "id"), "c1"))
expect_reject("duplicate concept label rejected",
              mutate(("concepts", 1, "label"), "prime product encoding"))
expect_reject("bad kind rejected", mutate(("concepts", 0, "kind"), "vibe"))


def main():
    print(f"\n{len(passed)} passed, {len(failed)} failed")
    for name, err in failed:
        print(f"FAIL {name}: {err}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
