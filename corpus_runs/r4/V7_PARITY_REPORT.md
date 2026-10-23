# v7/R4 parity re-measurement — report

Date: 2026-10-04. Decision tree Node 20.
Protocol: blind, 4 scorers × 3 chunks, 10 locked probes/chunk,
0/0.5/1 rubric, miss classes. Scorers saw ONLY `rehydrated_v7.json`
+ `probes.yaml`. Brief: `corpus_runs/r4/SCORER_BRIEF_V7.md`.
All 24 per-probe records validated; totals recomputed.

## Parity

| chunk | v7 /10 |
|-------|--------|
| c01 | 4.5 |
| c02 | 6.5 |
| c03 | 7.0 |
| c04 | 9.5 |
| c05 | 9.0 |
| c06 | 9.0 |
| c07 | 6.0 |
| c08 | 8.5 |
| c09 | 7.0 |
| c10 | 8.0 |
| c11 | 7.0 |
| c12 | 7.5 |
| **mean** | **7.46** |

Range 4.5–9.5. Zero FABRICATION (120 probes). Distribution: 50.8%
ones, 47.5% halves, 1.7% zeros.

Per probe class:

| class | v7 | R3 injection (orig scorer) |
|-------|-----|---------------------------|
| NUMBER | 0.73 | 0.73 |
| VERDICT | 0.70 | 0.73 |
| MECHANISM | 0.76 | 0.74 |

MECHANISM is now the *strongest* class — the R3 frontier has
inverted. NUMBER exactly reproduces the R3 injection level.

## Cost (measured)

- Wire tokens: mean 483, range 344–659 (v6: 553; R3 injection path
  is not directly comparable — different payload).
- Deployment break-even: mean **2.06**, 12/12 ≤ 3 (v6: 2.36; R3
  injection: 2.26).

The v7/R4 combination is cheaper than v6 and cheaper than the R3
injection path, at higher parity than either wire.

## Calibration and comparability

The v7 scorers' ones-rate (50.8%) matches the original R3 scorer
(41.7%) far more closely than the strict v6 rescorers (5.8%). Under
that calibration:

- v7 **7.46** ≈ R3 injection **7.42**: the v7 wire preserves parity
  at the extraction's own level. The R3 wire loss (0.63) is gone —
  consistent with the v6 rescore finding (+1.12 > 0.63).
- NOT directly comparable to v6's 6.00 (different scorer
  strictness). The v5→v6 +1.12 remains the valid wire-to-wire
  comparison.

Caveat: "7.46 ≈ 7.42" is calibration-inferred (ones-rate), not a
controlled within-scorer comparison. The R4 extraction is also
better than R3's, so the gain combines extraction quality and wire
fidelity.

## Where the v7 statuses specifically carried probes

(From scorer reports; see rescore files for per-probe records.)

- Killed statuses + "framework survives" notes express splits
  inexpressible as bare labels (Connes LIVE-as-framework/KILLED-
  as-proof; the five operator kills).
- `conjectural` on negative literature searches vs `exact` on
  positive findings: the vocabulary's precision visible in scoring.
- `exact`+`identification` carried bridge probes (Λ=μ∗log,
  faces=Fock) that bare labels capped at 0.5.
- The exact/conjectural split on D_log (self-adjoint proved /
  eigenvalues unproved) structurally encodes "buys real spectrum,
  not the zeros."

## Systematic remaining gap

Scorers' recurring 0.5 pattern: **mechanism detail absent from
notes** — Deninger 3D-foliation mechanism, Lomb-Scargle method +
bandwidth limits, 14b's complexity moral, even-subspace legitimacy
argument, per-control numbers, perturbation-vector mechanism.
Claims and verdicts travel; the *why-it's-legitimate* machinery
often doesn't. The note channel helps mechanism *answers* (numbers,
qualifiers) but not mechanism *derivations* (proof steps) — c02,
the most derivation-heavy chunk, shows the boundary.

## Open measurement

The R4 *injection* (extraction JSON) parity was not scored. If
injection ≈ 7.5, the wire is lossless and the frontier is
extraction quality; if injection ≈ 9, the wire is still lossy.
That measurement separates the two.

## Appendix: scorer's per-probe notes (S1 v7: c01–c03)

Where the v7 status/genre layer decided probes:
- **c03 P3 → 1.0:** the `conjectural` status on the twin asymptotic
  *is* the honest-boundary answer; the derivation sits at `exact`.
- **c03 P9 → 1.0:** the 9a(`exact`)/9b(`exact`)/9c(`heuristic`+loop)
  status pattern encodes the closed/resolved/open verdict.
- **c02 P5, P8 → 1.0:** `heuristic` statuses encode the honesty
  qualifiers the references imply.
- **c01 P10 → 0.5:** genres carry the novelty table's
  packaging-vs-content distinction, but the standing rule
  ("no public novelty claim without re-search") is absent.
- **c01 P4/P9:** `killed` + `conjectural` directly encode the
  "closed negative BY THEOREM" and Node 12 verdict structures.

Persistent structure-level gaps:
- **c01 P5 → 0.0:** the Li-vs-Weil distinction is absent entirely —
  the probe's whole subject missing (extraction gap, cf. S2's
  c05 P3/P7).
- **c02 P2/P3/P9, c03 P4–P8:** stuck at 0.5 — claims, numbers, and
  statuses present but proof/mechanism steps absent. The derivation
  boundary, confirmed across scorers.

## Appendix: scorer's per-probe notes (S2 v7: c04–c06)

- **c04 P10 → 1.0:** `exact` + "translation≠proof" carried the
  cited-not-derived honesty.
- **c05 P6 → 1.0:** `exact` verdict + `heuristic` coda matched the
  reference's own epistemics; the status split *is* the answer.
- **c06 P9/P10 → 1.0:** `exact`+`identification` carried the
  "computed, never inserted" claims — 0.5 on v5/v6, recovered by R4.
- **c05 P7 → 1.0:** was 0.0 on v5/v6 (extraction gap); R4 recovered
  it. The extraction-gap diagnosis confirmed and fixed.
- **c05 P3 → 0.0** on all three wires: persistent extraction gap,
  not wire loss.

**Flag (honest):** on c06 the R4 extraction is NOT a strict superset
of v6's note content — it gained P9/P10 (mechanisms v6 lacked) but
lost two note details v6 had (P7 compatible/incompatible split, P8
O(π(z)) moral: 1.0→0.5). Net c06 9.0 vs 9.0, a wash with different
composition. Battery-wide v7-vs-v6 comparisons should carry this
caveat: re-extraction shifted content, not only added it.

## Appendix: scorer's per-probe notes (S3 v7: c07–c09)

Where statuses carried verdict-standing:
- **c07/P5 → 1.0:** `exact`+`reframed` vs `conjectural` split *is*
  the "closed on the algebra / honest boundary" distinction.
- **c07/P2 → 1.0:** `killed` carried the kept-negative-result framing.
- **c08/P2 → 1.0:** `reframed` + "≠ RH proof" carried the circularity
  warning.
- **c09/P4, P9 → 1.0:** "VERDICT negative exact" carried the
  exact-negative standing.
- **c08/P10 → 1.0:** `exact` verdict + open question unanchored in
  loops matched "verified kinds / open question."

Where statuses couldn't substitute for missing content (stayed 0.5):
- c07/P9, c09/P6, c09/P7, c07/P3/P4/P8, c08/P3/P5 — correct statuses,
  but load-bearing formulas/mechanism steps absent from notes.

**Finding:** the v7 vocabulary does its designed job at the verdict
level (statuses answer "what kind of claim is this"), but a status
never upgrades a probe past what the notes carry. The binding
constraint remains mechanism-grade content in notes, not the status
labels themselves.
