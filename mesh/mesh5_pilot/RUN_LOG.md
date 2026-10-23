# MESH-5 Pilot — Run Log

**Charter:** mesh/MESH5_PILOT_CHARTER.md (GO 2026-10-09).
**Work dir:** mesh/mesh5_pilot/. Atlas records read-only.

## Phase A — link-discipline shakedown (K1 gate)

- **Status:** RUNNING (extractor dispatched 2026-10-09).
- **Corpus:** corpus_runs/atlas9/ATLAS9_REPORT.md (151 lines; chosen:
  claim-dense, no MESH-5 content → no hypothesis leakage to E_blind).
- **Brief:** mesh5_pilot/EXTRACTOR_BRIEF.md (5 rels; contradicts with
  5 worked + 5 near-miss examples from the Atlas-9 material; ≥3
  links/record; no epistemic labels; hypothesis never mentioned).
- **Target:** 20 records → mesh5_pilot/phase_a/shakedown_records.json.
- **Gate K1:** mean degree ≥ 3.0 AND contradicts ≥ 5% of links.
  Fail → revise discipline ONCE, re-shake on different material.
  Fail twice → STOP, NO-GO.

## Phase B — corpus + judging (gated on K1)

- 8 chunks × 15 probes = 120, new extractions (chunk sources
  pre-selected: atlas6 main, li_check, a3_test, atlas7, atlas8,
  atlas10, atlas11, item2_gram reports; retrospective/charter/tree
  excluded from extraction corpora).
- E_blind: full corpus, never told the rule. E_told: 40-record subset,
  told afterwards (Goodhart guard).
- Fixed judge j4: brief at mesh5_pilot/JUDGE_BRIEF.md (reconstructed
  from VERDICT_PACKET_SPEC v1.1; original brief text not preserved).
- K2: mapping ≥ 90%. K4: candidate pool ≥ 48 conjecturals.

## Phase C — held-out link audit

- Rubric: mesh5_pilot/AUDIT_RUBRIC.md (pre-registered). 40 records,
  extractor-blind. K3: E_told inflation >25% or audit fail >15% → NO-GO.

## STOP GATE — human grading

- Harness for the candidate pool (j4-labeled conjectural, ~64
  expected). Analysis resumes after grades exist.

## Phase A attempt 1 — K1 FAILED (2026-10-09)

- 20 records, 42 links, mean degree 4.2 (≥3.0 ✓).
- contradicts: 1/42 = 2.4% (< 5% ✗).
- Extractor diagnosis: Atlas-9 source genuinely lacks negations beyond
  the single A9-11 tension; rest are role-differences (brief near-misses
  applied correctly). implements 0 (unused, not forced — fine).
- **Revision (1 of 1 allowed):** brief → v2
  (EXTRACTOR_BRIEF_V2.md): adds first-class "limitation records"
  (X fails/is weak/remains open/was downgraded) + operational
  scope-narrowing contradicts principle with re-grounded examples.
  Corpus → corpus_runs/atlas6/a3_test/REPORT.md (genuine dialectic:
  downgrades, open items, negations). Pilot chunk c3 reassigned to
  D1_FACE_LATTICE.md to avoid overlap.
- V2 shakedown dispatched (fresh subagent, 20 records →
  phase_a/shakedown_records_v2.json). If v2 fails K1: STOP, NO-GO
  on discipline.

## Phase A attempt 2 — K1 FAILED (2026-10-09). PILOT NO-GO.

- 20 records, 49 links, mean degree 4.9 (≥3.0 ✓), min degree 3.
- contradicts: 2/49 = 4.1% (< 5% ✗). Independently recomputed.
- Extractor caveat (honest): both contradicts rest on the
  scope-narrowing clause against broad readings the source never
  asserted; held to "contradicts only claims the source asserts,"
  both downgrade to refines (true rate ~0-2%).
- Two failures on two corpora (consistent report: 2.4%; dialectic-rich
  report: 4.1%). Per charter §6: STOP. Do not proceed to Phase B.
- **Verdict: NO-GO on link discipline.** The 5% bar assumed a
  dialectic density the program's reports do not have; forcing it
  would manufacture false contradicts and poison M3* — the metric
  the pilot exists to test. The NO-GO protects the pilot's validity.
- **Chain:** MESH-5 stays OPEN. Fallback inventory (needs charter
  amendment + router word): (a) pilot redesigned around M1 (no
  contradicts needed) — but M1 doesn't implement the QUEUE-tier
  mechanism; (b) run with M3-as-in-support (as the retrospective
  did) — changes the pre-registered metric; (c) record the dead
  end: the "relative" vocabulary may be untestable on this material.
