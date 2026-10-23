# Harness MVP Scope — `memory_harness.py`

Date: 2026-09-28. Parent decision: DECISION_TREE.md node 10 (open).
Status: scope; no code yet.

## 1. Objective

Answer exactly one question: **can an LLM extractor produce v5-grade
structure from real prose at probe parity with the source, at a cost
that amortizes?** Everything in this MVP exists to run that experiment.
Nothing else gets built.

## 2. Non-objectives (explicitly deferred)

- Read-path retrieval at scale (relevance subgraph selection). Phase 1
  reads whole checkpoints only.
- Registry evolution: versioning beyond per-checkpoint fingerprints,
  merges, splits, deprecation, garbage collection.
- Temporal validity / conflict resolution (v6 consideration).
- Multi-session amortization infrastructure.
- Production hardening, auth, multi-user, UI.
- Fountain-layer integration (already lives in the codec; not re-tested).

If a design choice tempts scope beyond the extractor gate, it loses.

## 3. The gating experiment

### 3.1 Corpus

Real prose, not synthetic (synthetic would repeat the scale test's
caveat). Proposal: one contiguous 2–4k-token chunk of a real session
transcript from this CCC arc — technical, entity-dense, argumentative
(e.g. the scale-test or decision-brief discussion). Criteria: named
concepts recur, claims relate to each other (supports/contradicts/
bounds), some claims get superseded mid-discussion (statuses get
exercised). Final chunk choice is open (see §10).

### 3.2 Extraction schema (strict)

The extractor emits JSON with exactly:

- `concepts`: `[{id, label, kind}]` — kind from a small fixed set
  (TBD: e.g. claim, method, result, entity, metric).
- `strands`: `[{id, label, concept_ids[]}]` — labeled, per v5.
- `edges`: `[{a, b, rel}]` — directed, rel from a **fixed vocabulary**
  (proposed starter set: supports, contradicts, bounds, generalizes,
  implements, depends_on, causes, measures, defines, exemplifies;
  capped at ~12; vocabulary changes are versioned).
- `anchors`: `[{concept_id, status, note}]` — status from a fixed set
  (proposed: asserted, verified, superseded, open_question).
- `loops`: `[{concept_id}]` — references a concept (usually kind
  `open_question`). **Refinement (2026-09-28, M1):** the scope
  originally said free-text loops, but the v5 wire can only carry
  registry indices, so loop bodies live on the concept's label.

No free-form fields except `label`, `note`, `text`. The schema is the
contract the verifier enforces.

### 3.3 Deterministic verifier

Pure function, no LLM. Hard fails (trigger one repair retry with the
failure list fed back to the extractor):

1. Every id referenced resolves to a declared concept.
2. Every `rel` is in the vocabulary; every `status`/`kind` in its set.
3. No duplicate `(a, b, rel)` edges.
4. Every strand is non-empty; every concept appears in ≥1 strand or
   edge (orphans are warnings, not failures — recorded).
5. The structure round-trips through the v5 codec (encode→decode is
   identity) and the wire validates (checksums, fingerprint).

Two failed repairs = extraction failure for that chunk (counted in
the metrics, not silently retried forever).

### 3.4 Probe protocol

1. Write N=10 why/how probes **from the source prose**, blind to the
   extraction (separate pass, before seeing the structure).
2. Answer each probe twice: (a) from the source prose, (b) from the
   extracted structure only, injected in the grouped compact format
   (the scale-test injection syntax).
3. Score: **parity** = same correct answer from both. Record two
   failure modes separately: *omission* (unanswerable from structure)
   and *hallucination* (structure supports a wrong answer — hard fail
   class, worse than omission).
4. Target: parity ≥ 9/10, zero hallucinations.

### 3.5 Cost accounting

Per chunk: extraction input tokens (source + schema prompt + any
repair retry), extraction output tokens. Savings per session =
prose_tokens − injected_structure_tokens (measured, not projected;
expect ~2.2x on structured content). **Break-even sessions =
extraction_cost / savings_per_session.** Target: break-even ≤ 3
(the scale test's cold-start amortization was ~2–3 sessions for the
codec alone; extraction must not blow past that).

### 3.6 Go / no-go thresholds (proposed, not validated)

- GO: parity ≥ 9/10 AND zero hallucinations AND break-even ≤ 3
  sessions AND verifier pass rate 100% within 2 repair attempts.
- NO-GO: miss on parity or any hallucination, or break-even > 5.
- Gray zone (7–8/10 parity, no hallucinations): one schema/vocabulary
  revision allowed, then re-run once. Two gray runs = no-go.

## 4. Storage schema (SQLite, phase-1 minimal)

```sql
concepts(id INTEGER PRIMARY KEY, label TEXT UNIQUE, kind TEXT,
         first_seen_session INT, status TEXT);
strands(id INTEGER PRIMARY KEY, label TEXT, session INT);
strand_members(strand_id INT, concept_id INT);
edges(a INT, b INT, rel TEXT,
      PRIMARY KEY (a, b, rel));
anchors(concept_id INT PRIMARY KEY, status TEXT, note TEXT);
checkpoints(id INTEGER PRIMARY KEY, session INT, wire TEXT,
            fingerprint TEXT, created TIMESTAMP);
```

No migration framework; no soft-delete. Evolution is deferred work
with its own scope.

## 5. Write path

transcript chunk → extractor (LLM, strict schema) → verifier
(§3.3; ≤2 repair retries) → entity resolution (phase-1 minimal:
exact/alias match against `concepts.label`; non-matching concepts
inserted as new; near-matches surfaced for human adjudication —
full automatic merge is experiment 2, not this build) → merge into
SQLite → v5 checkpoint (wire + fingerprint stored verbatim).

## 6. Read path (minimal, probe-answering only)

Load checkpoint → decode + validate wire → inject grouped compact
structure (subject-grouped minimal syntax from the scale test).
No relevance ranking, no subgraph selection — the whole checkpoint
is the working set at this scale. Retrieval is phase 2.

## 7. Entity resolution — experiment 2 (designed, not built)

Deferred until the extractor gate passes. Design sketch: alias-pair
test set mined from multi-session transcripts (e.g. "wheel_210" vs
"the mod-210 wheel"); candidate generation by embedding similarity
over labels+notes; adjudication accuracy as the metric; threshold:
precision ≥ 0.95 on merge decisions (a wrong merge corrupts the
registry silently — precision matters more than recall). The phase-1
merge hook (§5) is where this plugs in.

## 8. Milestones

- **M1** — schema + verifier + codec glue. Deterministic, no LLM.
  Done when: hand-written structure for the corpus chunk passes all
  verifier checks and round-trips v5. **DONE 2026-09-28**
  (`memory_harness.py`, `test_m1.py` 14/14).
- **M2** — extractor prompt + repair loop. Done when: 3 consecutive
  clean extractions (≤1 repair each) on held-out chunks.
  **DONE 2026-09-28** (`extractor.py`, `M2_REPORT.md`): 3 real transcript
  chunks (cursor layer / decode test / scale economics), repairs 1/0/0,
  all v5 round-trip clean. One failure mode found and fixed (null notes).
  Author served as the LLM — extractor-skill bias is the open caveat;
  naive-model trial still required. Economics preview on chunk 1:
  extraction 8868 tok vs ~2515 tok/session saving → break-even ≈3.5
  sessions (right at the M4 GO boundary; M3 decides).
- **M3** — probe protocol + cost accounting on the corpus. Done when:
  parity score, failure-mode breakdown, and break-even number exist.
- **M4** — go/no-go against §3.6. A decision, not a demo.

## 9. Kill criteria

No-go at M4 stops the harness. The codec work stands (nodes 0–9
closed; node 9c research contribution banked). No sunk-cost
continuation into retrieval or evolution machinery. This is written
down now so it holds later.

## 10. Open questions

1. Relation vocabulary: final list and cap (starter set in §3.2).
2. Corpus chunk: exact transcript segment.
3. Probe blindness: who writes probes (a separate model pass with no
   access to extraction output is the cleanest available control).
4. Repair-loop budget: 2 attempts is proposed; measure whether
   failures are schema misunderstandings (fixable in prompt) or
   genuine ambiguity (not fixable).
5. Concept `kind` set: needed at all in phase 1, or dead weight?
