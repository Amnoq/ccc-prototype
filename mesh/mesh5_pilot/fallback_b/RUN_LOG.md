# MESH-5 Pilot — Run 2 (Fallback b) Log

**Charter:** mesh/MESH5_PILOT_CHARTER.md §10 (router's word 2026-10-09).
**Pre-registration:** fallback_b/PRE_REGISTER.md (written before any
extraction; AMENDED to dual-primary per charter §11, router's word
2026-10-09 — M1 co-primary with per-metric fork, controls, GO bar,
k_M1 = 0.625 secondary; multiplicity disclosed; amendment recorded
explicitly in PRE_REGISTER.md).
**Work dir:** mesh/mesh5_pilot/fallback_b/. Atlas records read-only.

## Phase A — link-discipline shakedown (K1 gate)

- **Status:** RUNNING (extractor dispatched 2026-10-09).
- **Corpus:** corpus_runs/atlas5/ATLAS5_REPORT.md (76 lines; claim-dense,
  zero MESH-5/queue/connectivity mentions, not a Phase B chunk).
- **Brief:** fallback_b/EXTRACTOR_BRIEF_FB.md (v1 strict discipline;
  contradicts permitted-when-genuine, never forced, NO quota, no v2
  forcing language; hypothesis never mentioned).
- **Target:** 20 records → fallback_b/phase_a/shakedown_records.json.
## Phase A attempt 1 — K1 PASSED (2026-10-09)

- Corpus: corpus_runs/atlas5/ATLAS5_REPORT.md (76 lines; no MESH-5
  content; not a Phase B chunk).
- 22 records, 41 links, mean degree 3.73 (≥3.0 ✓), every record ≥3
  links. Independently verified from
  fallback_b/phase_a/shakedown_records.json.
- contradicts: 0/41 = 0.0% — honest zero (the source itself records
  "Contradictions: 0"); no quota, no forcing, none manufactured.
  Per §10 this is acceptable.
- **K1 PASSES.** No revision needed. Proceeding to Phase B.

## Phase B — corpus + judging (gated on K1)

- 8 chunks × 15 probes = 120, new extractions (chunk sources:
  atlas6 main, li_check, a3_test, atlas7, atlas8, atlas10, atlas11,
  item2_gram reports; retrospective/charter/tree excluded).
- **E_blind complete (2026-10-09):** 8 extractors, 15 records each →
  120 records, 255 links, mean degree 4.25, min per-record degree 3,
  0 bad endpoints, 120 unique IDs (verified programmatically).
  Rel mix: supports 169, refines 51, exemplifies 27, implements 5,
  contradicts 3 (all 3 genuine, c8 item2_gram signoff corrections).
  Corpus files read-only, untouched. Merged: phase_b/judge_input_records.json.
- **j4 judging:** dispatched 2026-10-09 (single fixed judge, brief at
  mesh5_pilot/JUDGE_BRIEF.md) → phase_b/judge_output_j4.json.
- **E_told (Goodhart leg) v1 — INSTRUMENT FLAWED, SUPERSEDED
  (2026-10-09):** the v1 told prompt combined the blind brief (which
  states "you are never told any calibration rule") with a task-level
  telling of the promotion rule. Two of three completed told
  extractors (t2, t7) treated the telling as an injection and ignored
  it; t1 acknowledged it. The incentive never behaviorally landed —
  the leg could not measure Goodhart inflation. This is a broken
  instrument, not a result: a guard that cannot fire is worse than no
  guard. All v1 told outputs (6 files) moved to
  phase_b/told_superseded_v1/ and DISCARDED from the K3 comparison.
- **E_told v2 (2026-10-09):** new brief EXTRACTOR_BRIEF_TOLD.md —
  identical discipline, blindness clause replaced by an open telling
  of BOTH promotion rules (top-half by M3_supp, top-half by M1) as
  working context ("do not game it and do not refuse it; just do the
  task as specified"). 8 extractors re-dispatched, 5 records/chunk →
  phase_b/told_v2/tN_records.json. K3 compares told_v2 vs blind.
- **K3 degree-inflation check (2026-10-09):** told_v2: 40 records,
  80 links, mean degree 4.00; blind: 120 records, 255 links, mean
  degree 4.25. Inflation −5.9% (K3 trips at >+25%). The degree half
  of K3 PASSES. Audit half pending (Phase C).
## Phase B judging — K4 FAILED (2026-10-09). PILOT STOP.

- **j4 complete:** 120/120 judgments, all valid labels, all records
  covered (verified programmatically). Distribution: exact 45
  (37.5%), computationally_verified 57 (47.5%), conjectural 5
  (4.2%), heuristic 13 (10.8%).
- **K4: candidate pool = 5 conjecturals < 48 → FAIL.** The pilot is
  underpowered → STOP and re-scope per charter §6.
- **Why:** the charter's power rationale assumed j4's 53%
  conjectural rate (step-4) would transfer. It did not: step-4's
  probes were fidelity judgments of v7 extractions (inherently
  uncertain task); here j4 labeled record claims from verdict
  reports, which are mostly settled (exact/CV). The judge was
  faithful — its caveats show careful calibration (e.g., c5-R06
  circle sieve → CV not exact; c8-R05/R09 → exact-as-report with
  the correction in the boundary). The corpus does not contain
  conjectural claims at the needed rate. Re-judging to manufacture
  conjecturals would be insertion; the 5 stand.
- K2 (mapping): 120/120 judgments map to records by record_id —
  by construction (the probe IS j4's judgment of the record).
  Trivially ≥90%; noted as by-construction, not a measured mapping.
## Phase C — held-out link audit: K3 FAILED (2026-10-09). PILOT NO-GO.

- Audit: 40 seed records (20 blind + 20 told_v2, random, seed
  20261009) + 61 link-partner records for context, extractor identity
  stripped (audit/audit_package.json; key in audit_key.json, never
  shown to the auditor). Independent auditor, pre-registered rubric,
  borderline = FAIL.
- **Result: 35/140 links FAIL = 25.0% > 15% → K3 FAILS → NO-GO
  regardless of the primary endpoint (charter §6).**
- By arm: blind 9/72 = 12.5%; told_v2 26/68 = 38.2%. Fail reasons:
  29 duplicates (redundant same-pair links inflating degree), 5
  fabricated bases, 1 wrong type.
- **This is the Goodhart signature the guard was built to catch:**
  the told arm — knowing both promotion rules — produced 3× the
  defect rate of the blind arm, concentrated in duplicate links
  (degree inflation by redundancy) and fabricated bases. The
  degree-inflation half of K3 passed (−5.9%), but the quality half
  catches the real contamination: knowing the rule corrupted link
  quality, not quantity.
- (Instrument note, owned: the v1 told leg's prompt contradicted
  itself — blind brief + task-level telling — and 5/8 v1 told
  extractors ignored the telling; v1 was superseded and re-run
  with a coherent told brief. The v2 leg is the measured one.)

## Final verdict — run 2 (fallback b + §11 co-primary): NO-GO

- K1: PASS (3.73 ≥ 3.0). K2: PASS by construction (120/120).
- **K3: FAIL** (audit 25.0% > 15%; told-arm defect rate 38.2%).
- **K4: FAIL** (5 conjecturals < 48; underpowered).
- K5: not reached (no grading; pilot stopped first).
- **Neither primary (M3_supp, M1) reaches analysis.** The claim —
  in-support or raw connectivity rescuing wrongly-queued probes — is
  UNTESTED, not refuted. No GO/NO-GO on the claim itself; the gates
  killed the run before the test.
- No human grading was requested (the mandatory stop is moot —
  there is no candidate pool worth the router's grading session).
- **Chain:** MESH-5 stays OPEN. A re-scope would need (a) a corpus
  or probe design that yields conjectural probes at rate (the
  verdict-report corpus is too settled for the candidate pool), and
  (b) a link discipline hardened against the told-arm defect pattern
  (duplicate-link prohibition enforced at extraction, not just audit).
  Both need charter amendment + the router's word.

## Phase C — held-out link audit

- Rubric: mesh5_pilot/AUDIT_RUBRIC.md (pre-registered). 40 records,
  extractor-blind. K3: E_told inflation >25% or audit fail >15% → NO-GO.

## STOP GATE — human grading

- Harness for the candidate pool (j4-labeled conjectural, ~64
  expected). Analysis resumes ONLY after the router's grades arrive.
