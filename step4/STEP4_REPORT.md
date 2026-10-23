# Step 4 Demonstration — Full Experiment Report

**Date:** 2026-10-08. **Experiment:** labeled vs binary judgments,
three arms, 120 human-graded parity probes. **Status:** complete;
verdict adjudicated per the pre-registered decision rule.

## Design (pre-registered, STEP4_DEMONSTRATION_CHARTER.md)

- **Corpus:** 120 probes (12 chunks × 10), human grades 0/0.5/1
  from `corpus_runs/r5/rescore_v7/` (ground truth: 95× 1.0,
  24× 0.5, 1× 0.0; all sub-1.0 OMISSION). Two drift-control files
  excluded from the 120 per the charter.
- **Judges:** 4 subagents, same model, 30 probes each, blind to
  grades (never opened `rescore_v7/`). Each judge rendered Arm A
  (binary) FIRST then Arm B (packet) INDEPENDENTLY per probe —
  disagreement permitted by design.
- **Arm A (binary):** faithful/unfaithful → ACT / don't-act.
- **Arm B (labeled):** verdict packet (claim + label + span +
  boundary) → MECHANICAL collapse per COLLAPSE_SPEC.md v1.
- **Arm C (null):** B's labels shuffled (seed 42, single
  pre-registered draw) pre-collapse, then mechanical collapse.
- **Ground-truth mapping:** human 1.0 → ACT correct, else missed
  act; human 0.0 → any ACT is false auto-act; human 0.5 →
  QUEUE/surface correct, auto-ACT is false auto-act.
- **≈ operationalization (fixed before seeing results):** |diff|
  ≤ 2 on an error count.

## Materials correction (mid-run, recorded)

The judge briefs initially pointed at
`corpus_runs/cNN/rehydrated_v7.json`, which does not exist. One
judge (j4) judged `corpus_runs/cNN/extraction.json` — a
different, earlier-stage document (5 strands/21 anchors vs 6
strands/19 anchors; different content). Caught on the first
completion handoff via content comparison. All judges redirected
to `corpus_runs/r5/cNN/rehydrated_v7.json` — the material the
humans graded. j4's chunks re-judged fresh by a new judge; the
wrong-file outputs were discarded, not reused. j3 independently
found the correct path. Final corpus: all 120 probes judged
against the graded material, blind rule intact throughout.

## Per-arm error tables (computationally verified)

| arm | false auto-acts | missed acts | queued | review load | action dist |
|---|---|---|---|---|---|
| A (binary) | 17 | 0 | 0 | 0.000 | ACT 112, NO ACT 8 |
| B (labeled) | 7 | 16 | 32 | 0.267 | ACT 86, QUEUE 32, SURFACE 2 |
| C (shuffled) | 17 | 26 | 32 | 0.267 | ACT 86, QUEUE 32, SURFACE 2 |

Precision/recall on the 95 human-1.0 probes:
- A: precision 95/112 = 84.8%, recall 95/95 = 100%.
- B: precision 79/86 = 91.9%, recall 79/95 = 83.2%.

Label distribution (Arm B, n=120): exact 32, computationally_verified
39, conjectural 43, heuristic 6, killed 0, unstated 0, superseded 0
(not emittable). Arm C inherits the same multiset by construction.

## Where B's errors come from (computationally verified)

- B's 16 QUEUE-on-1.0 ("missed acts"): ALL 16 carried the
  `conjectural` label. Judges saw partial coverage where humans
  scored full fidelity — under-confidence. 6 of 16 from one judge
  (c10–c12: 17 conjectural of 30 — judge-level calibration
  variance, the charter's "judge quality bounds everything").
- B's 7 false auto-acts: 6 `computationally_verified` + 1 `exact`,
  all on human-0.5 probes — over-confidence; judges verified the
  substance but missed the omission the humans docked.
- B correctly queued 10 of A's 17 false auto-acts (all
  `conjectural` → QUEUE) — the machinery working as designed on
  more than half the binary arm's errors.

## Token pricing (tiktoken cl100k_base, measured live)

- Arm A marginal output: mean 2.1 tokens/decision.
- Arm B packet: mean 167.2, p90 214, max 281 tokens/decision.
- Marginal label-machinery cost: ≈165 tokens/decision (~80× the
  binary output), given a shared assessment. In deployment both
  arms pay the assessment/inference cost; B adds the packet.
- 73% of packets exceed the spec's original 120-token budget
  (structural — matches the benchmark finding; spec revised to
  200 in v1.1).

## Verdict vs the pre-registered decision rule

- **Claim FAILS as stated** (computationally verified): B has
  strictly fewer false auto-acts (7 < 17) BUT its missed-act
  rate is worse (16 > 0). The "no worse missed-act rate"
  condition is not met.
- **Polar opposite FAILS** (computationally verified): B ≉ A
  (|7−17| = 10 > 2; |16−0| = 16 > 2). The arms are decisively
  different, not approximately equal.
- **Null FAILS** (computationally verified): C ≉ B (|17−7| = 10
  > 2 on false auto-acts; |26−16| = 10 > 2 on missed). Shuffled
  labels are strictly worse on both metrics — **the labels
  carry real information; they are not noise.**

## The actual finding (all three named legs exhausted)

A discriminating trade-off the charter did not name:
**the label machinery is informative and moves the operating
point, but the pre-registered collapse is miscalibrated for
these judges.** B buys −10 false auto-acts (deployed unfaithful
extractions) for +16 queued full-fidelity probes and 26.7%
review load, at ~80× marginal token cost.

Two framings, both honest:
1. By the pre-registered taxonomy, B's 16 QUEUE-on-1.0 are
   "missed acts" and the claim fails.
2. QUEUE routes to human review — it is delayed action, not
   dropped action. Under perfect review, B's effective errors
   would be 7 false auto-acts vs A's 17, with zero true losses
   on either side; the price is the 26.7% review load. This
   reframing is post-hoc and assumes review quality the
   experiment did not measure — recorded here as interpretation,
   not verdict.

## Honest negatives (owned same-exchange)

- **Judge quality bounds everything** (charter's own caveat,
  confirmed live): judge-level calibration variance is large
  (2 vs 17 conjectural per 30 probes across judges). A
  better-calibrated judge population shifts the trade-off;
  this experiment measures judge+labels, not labels in the
  abstract.
- **The 0.5→QUEUE mapping is a design choice**, not a discovery
  (charter-stated). A different mapping (e.g. 0.5→SURFACE, or a
  confidence-weighted queue) would move the operating point.
- **No tuning per arm after seeing results.** The collapse was
  mechanical throughout; the trade-off was measured, not
  optimized.
- **Token pricing is marginal**, not total: both arms share the
  assessment cost; only the packet delta (~165 tokens) was
  measured. No model-inference cost was measured.
- **Single shuffle draw** for Arm C (seed 42, pre-registered).
  The C-vs-B gap (10 on both metrics) is large enough that
  draw variance is not a plausible alternative explanation,
  but it was not multi-drawn.

## Backward touch (chartered)

- **VERDICT_PACKET_SPEC.md:** SURVIVES. Packets were produced
  well-formed at all 120 probes; checksums computed; the labels
  carried measurable information (null dead). The spec's
  may/may-not rules were honored (no strengthening, no drops).
- **COLLAPSE_SPEC.md:** SURVIVES AS FRAMEWORK, QUALIFIED AS
  CALIBRATION. The tiers are coherent and mechanically
  applied, but the specific mapping (conjectural→QUEUE)
  combined with these judges' caution produces the
  precision/recall trade-off measured here. Rule 2 (caution
  permitted, confidence never) is validated by the error
  direction. The spec needs a calibration note, not a
  rewrite — recorded below.
- **Mesh plan (step 4):** the demonstration does NOT validate
  the mesh point as a strict win, but it validates the
  premise the mesh point needs: the label machinery is
  informative (not noise) and changes decisions. "Derive
  here, apply there" survives with the caveat that the apply
  side needs calibrated judges — which is itself a derivation
  problem (judge calibration), keeping the work on the
  derive side.
- **BENCHMARK_REPORT.md:** the A-vs-B token ratio (~80×
  marginal, ~165 tokens/decision delta) folds into the cost
  story: time is free, tokens bind, and now the token price
  of the label machinery is measured on a real task.

## Records

- Judge outputs: `step4/judge_outputs/j{1..4}/c{01..12}.json`
  (120 probes, blind, both arms).
- Analysis: `step4/scripts/analyze_step4.py` (mechanical
  collapse, seeded shuffle, metrics, decision rule).
- Results JSON: `step4/step4_results.json` (per-probe detail
  for all three arms + ground truth).
- This report: `step4/STEP4_REPORT.md`.
- Charter (now the record): `STEP4_DEMONSTRATION_CHARTER.md`
  § Results.

## Method self-assessment

Followed: §1 (charter pre-registered before execution; results
appended as the record), §2 (labels on every claim above;
post-hoc interpretation explicitly marked), §3 (triadic fork
pre-registered; all three legs adjudicated; the fourth pattern
— discriminating trade-off — reported as what the data showed,
not forced into a leg), §4 (backward touch to both specs, mesh
plan, benchmark — recorded above and in the files), §5 (why it
ends here: the decision rule is adjudicated; its chain: judge
calibration as the next load-bearing question), §6 (live
computation throughout; the materials error caught by content
comparison on the first handoff and corrected before analysis —
the method catching its own error mid-run; blind rule verified
intact; no tuning after seeing results; honest negatives owned
same-exchange). Deviation: one — the ≈ operationalization
(|diff| ≤ 2) was fixed at analysis time, before seeing results
but after the charter; it is not in the charter text. Recorded
here, not smuggled.

## Correction note — 2026-10-08 (appended, original text untouched)

A parallel-account calibration study (Order 1), verified on the main
account against `step4_results.json` and `step4/judge_outputs/`, found
transcription errors in this report's prose. The verdict, the error
tables, and all action counts were re-verified and stand unchanged.

1. "Label distribution (Arm B, n=120)": reported exact 32 /
   computationally_verified 39 / conjectural 43 / heuristic 6.
   Correct per the raw judge outputs: exact **42** /
   computationally_verified **44** / conjectural **32** / heuristic
   **2**. (Arm C inherits the same multiset — that sentence remains
   true; both arms' distributions match the raw data.)
2. "6 of 16 from one judge (c10–c12: 17 conjectural of 30" → **9 of
   16** from one judge (c10–c12: **16** conjectural of 30). j4's 16
   conjecturals include 9 that humans scored 1.0.
3. "2 vs 17 conjectural per 30 probes across judges" → "2 vs **16**".

Nothing downstream changes: B's 7 false auto-acts (6 cv + 1 exact, all
human-0.5), the 16 conjectural→QUEUE misses, and the precision/recall
trade-off are all confirmed against the raw data. The error was in the
prose transcription, not the analysis.
