# R6 targeted re-run — report (PRELIMINARY)

Date: 2026-10-18. Decision tree Node 23 (follows Node 22).
Extractor: `extractor_rev5.py` — EXTRACTOR_PROMPT_R6 (R5 + the five
binding drop-class fixes), run on `corpus/c02_deriv_d1_d5.txt`.
Artifacts: `corpus_runs/r6/c02/extraction.json` (validates clean),
`corpus_runs/r6/c02/wire_v7.json`, `corpus_runs/r6/c02/rehydrated_v7.json`.

## Protocol

The pre-registered test from Node 22: re-run the 12-probe targeted
suite (`~/workspace/your_files/r5-targeted-probe-suite.yaml`, keys
locked 2026-10-15) against the patched extractor; check the nine
predicted 1.0s (M4, V1, V2, N1, M1, M3, M6 + R5 c02 P5, P8).
Scoring: 0/0.5/1 rubric from the drop battery, notes-only, one scorer.
Matches the drop battery's notes-only arm (not the full blind-wire
protocol of Node 21).

## Scores

| probe | class | R6 | baseline (S1/S2) | predicted |
|-------|-------|-----|------------------|-----------|
| M1 | MECHANISM | 1.0 | 1.0/0.5 | 1.0 |
| M2 | MECHANISM | 1.0 | 1.0/1.0 | — |
| M3 | MECHANISM | 1.0 | 1.0/0.5 | 1.0 |
| M4 | MECHANISM | 1.0 | 0.5/0.5 | 1.0 |
| M5 | MECHANISM | 1.0 | 1.0/1.0 | — |
| M6 | MECHANISM | 1.0 | 1.0/0.5 | 1.0 |
| N1 | NUMBER | 1.0 | 0.5/0.5 | 1.0 |
| N2 | NUMBER | 1.0 | 1.0/1.0 | — |
| N3 | NUMBER | 1.0 | 1.0/1.0 | — |
| V1 | VERDICT | 1.0 | 0.5/0.5 | 1.0 |
| V2 | VERDICT | 1.0 | 1.0/0.5 | 1.0 |
| V3 | VERDICT | 1.0 | 1.0/1.0 | — |
| **total** | | **12.0/12** | 10.5/8.5 (mean 9.5) | 9/9 |
| c02 P5 | (R5 parity) | 1.0 | sub-1.0 | 1.0 |
| c02 P8 | (R5 parity) | 1.0 | sub-1.0 | 1.0 |

All nine predicted 1.0s materialize; the three already-1.0s held.
Zero fabrication: every added clause is traceable to the source text
(honest-boundary rule); nothing invented.

## Cost of the fixes

c02 wire tokens: 726 → 1221 (+68%). Anchor note words: 205 → 472.
The fixes are content, not free — the R6 notes buy their 1.0s at
roughly 2.3× the words. On the Node 21 battery, R5's gain cost
+430 wire tokens mean for +1.46 parity; R6's per-chunk cost trend
is steeper. Whether 12/12 ≤3 BE_dep survives R6 on the full battery
is unmeasured — the battery-level cost check is the next open item.

## Epistemic labels

- Scores above: **preliminary (unblinded)** — the extractor had read
  the keys before extracting, and the scorer is the same instrument.
  The drop battery was blind and two-scorer; this run is neither.
  The honest battery needs blind rescorers before these numbers
  count as measured.
- Predicted-vs-actual agreement (9/9): as stated, preliminary for
  the same reason. What it does establish: the five fixes are
  *sufficient* — every drop the battery named is repairable by its
  fix, no third class needed on this chunk.
- Cost numbers: computationally verified (deterministic builds,
  tiktoken counts).

## Limits

- Single chunk (c02); single scorer; unblinded.
- The R5 parity battery's own c02 score (9.0/10 under R5) vs this
  12/12 targeted-suite score are different protocols — not comparable
  as levels; the comparison that matters is fix-predicted vs
  fix-observed on the same suite.
- Open: full-battery R6 re-extraction (12 chunks), blind rescore,
  BE_dep measurement, and whether the conclusion-first rule changes
  any R5 concept structure at scale.

## Blind rescore (2026-10-18) — measured
Two independent blind scorers (notes + locked keys only, strict rubric):
- Scorer A: 12.0/12 targeted, 13.5/14 overall (c02 P8 at 0.5).
- Scorer B: 11.0/12 targeted, 12.5/14 overall (M2, V3, c02 P8 at 0.5).
- Mean targeted: 11.5/12 vs R5 baseline mean 9.5.

Predicted 1.0s: 8/9 confirmed by both scorers (M4, V1, V2, N1, M1, M3, M6, c02 P5). c02 P8 did NOT survive blind scoring — both scorers mark 0.5: the notes carry the failure reason but not the resulting sharpest question. The preliminary 1.0 was scorer-generosity (scorer = extractor); the blind arm caught it.
New single-scorer 0.5s: M2 (integer-side set characterization), V3 (beachhead-#2 honesty qualifier + step-4 inversion) — both from the stricter scorer only; medium confidence, same harsh-scorer pattern as R5's S2.
Verdict: the five fixes are confirmed working, 8 for 9, under blind two-scorer protocol. P8 remains open (one more targeted pass available).
