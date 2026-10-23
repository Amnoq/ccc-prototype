# R4 extraction battery — report

Date: 2026-10-04. Decision tree Node 18.
Extractor: `extractor_rev3.py` (v7-native statuses + genres, open
questions unanchored). 11 chunks drafted by agents, c02 by pilot;
every draft second-judged by the coordinator against the R4 prompt
before acceptance. Review log: `corpus_runs/r4/REVIEW_LOG.md`.

## Battery totals

12 chunks · **238 concepts · 217 anchors** · all validate clean
(`validate_extraction` → `[]`), all v7 round-trip + independent
spec-decode exact.

| status | count | share |
|--------|-------|-------|
| exact | 127 | 59% |
| computationally_verified | 53 | 24% |
| killed | 14 | 6% |
| conjectural | 16 | 7% |
| heuristic | 7 | 3% |
| superseded | 0 | — |

| genre | count |
|-------|-------|
| original | 88 |
| none | 90 |
| reframed | 26 |
| identification | 13 |

Per-chunk anchor counts range 12–21 (all within the 12–22 concept
cap). Open questions: 19 across 11 chunks, all in loops, none
anchored. Zero fabrications; kill reasons preserved in notes.

## What the vocabulary did

The old R3 statuses (asserted/verified) collapsed distinctions the
R4 vocabulary separates:

- **killed (14)** handles negative results natively — 9c, 9c′,
  L1–L3, the five operator candidates, Connes-as-proof, the naive
  positivity hope. No euphemism; kill reasons ride in the notes.
- **conjectural (16)** holds precise unproven claims with stated
  boundaries: twin asymptotic, CCM spectra, Deninger program, the
  14c home candidate, negative literature searches.
- **computationally_verified (53)** always carries scope in the note
  (grids, N, error bounds, check points).
- **heuristic (7)** marks analogies and programmatic inferences,
  including two the text labels itself.

## Calibration refinements recorded during review

1. Verdicts inherit exactness from exact premises (c04/c5, c08/c13).
2. Composite verdicts: the closure-record can be exact while live
   content keeps its own status — split explicit in note + concepts
   (c10/c6, c01/c18).
3. Conjectural = precise claim + stated boundary + no proof;
   boundaries stay anchored, loops are for open questions only
   (c03/c6).
4. Negative literature searches → conjectural (can't prove a
   negative); positive findings → exact. Closed loop (bug fix
   verified by corrected run) vs open-ended search is the line
   (c11 block decision).
5. Chunk-local honesty: the same identity is exact where derived
   (c03/c3) and computationally_verified where only checked
   (c07/c14). Not inconsistency — the merge layer reconciles.
6. Documented procedural facts verified by the work → exact
   (bug-fix records, stipulated methods, conducted procedures).
7. Genre discipline: classical constant + new derivation →
   reframed ("not a new theorem"); X⟷Y correspondence exhibited
   term-by-term → identification; audit-use of classical results →
   none (not identification).

## Reviewer edits

Four chunks received reviewer edits before acceptance: c01 (genre
c4→reframed, status c9→exact, note c13), c06 (genre c9→none), c07
(genre c15→reframed), c11 (status c9→exact). All other drafts
accepted as written. The drafters' self-flagged soft calls were
independently verified; two (c09/c17, c05/c21) were judged
over-cautious in the right direction.

## Status

Battery complete and accepted. Next: full v7/R4 wire build,
measured token cost, and parity re-measurement (the v7-native
numbers for Node 19's comparison).
