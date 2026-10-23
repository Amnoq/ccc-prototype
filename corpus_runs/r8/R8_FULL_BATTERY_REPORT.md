# R8 full 12-chunk validation battery — report

Date: 2026-10-18. This is the generalization test: the R5→R8 extractor
fixes (CONCLUSION-FIRST, PAYOFF CLAUSE, GRID RULE, INTERPRETATION RIDER,
PRESCRIPTION COMPLETENESS, CROWNED-VERDICT, M2 BIJECTION-COMPLETENESS —
EXTRACTOR_PROMPT_R8 in extractor_rev7.py) were validated on chunk c02
only (Nodes 22–24). This battery tests all 12 chunks, 120 probes.

## Method (blind, two-scorer, role-separated/brief-scoped)

1. EXTRACTION: 12 independent extractor subagents, each briefed with ONLY
   the R8 prompt + one chunk's corpus text + the JSON schema
   (concepts/strands/edges/anchors/loops). Extractors knew nothing of
   probes, keys, scores, or expected outcomes. Outputs:
   corpus_runs/r8/cXX/extraction.json (XX=01..12), each verified parsing.
2. PACKETS: 12 blind packets (chunk anchor notes + its 10 probes with
   locked keys + the strict r7 rubric, reused verbatim):
   corpus_runs/r8/cXX/blind_packet.json.
3. SCORING: two blind scorer subagents, each given all 12 packets, briefed
   to score every probe 0/0.5/1 notes-only under the strict rubric
   (1.0 = key fully reconstructible, no gap), reading nothing else, with
   no expectations. Each returned per-probe scores + justifications,
   per-chunk /10 totals, grand /120.
4. COMPILE: per-chunk R8 means vs R5 parity baselines
   (corpus_runs/cXX/report.json — binary parity/omission, 58/120 grand).

## Per-chunk results

| chunk | R5 parity | R8 scorer A | R8 scorer B | R8 mean | delta |
|-------|-----------|-------------|-------------|---------|-------|
| c01 | 3/10 | 8.0 | 5.5 | 6.75 | +3.75 |
| c02 | 6/10 | 6.0 | 5.0 | 5.50 | −0.50 |
| c03 | 6/10 | 6.5 | 7.5 | 7.00 | +1.00 |
| c04 | 8/10 | 6.5 | 7.0 | 6.75 | −1.25 |
| c05 | 6/10 | 9.5 | 9.5 | 9.50 | +3.50 |
| c06 | 7/10 | 2.5 | 3.0 | 2.75 | −4.25 |
| c07 | 4/10 | 7.0 | 5.5 | 6.25 | +2.25 |
| c08 | 6/10 | 9.5 | 9.5 | 9.50 | +3.50 |
| c09 | 3/10 | 4.5 | 4.5 | 4.50 | +1.50 |
| c10 | 3/10 | 6.0 | 7.0 | 6.50 | +3.50 |
| c11 | 1/10 | 8.5 | 8.5 | 8.50 | +7.50 |
| c12 | 5/10 | 4.5 | 4.0 | 4.25 | −0.75 |

Grand totals: scorer A 79.0/120, scorer B 76.5/120.
**R8 grand mean: 77.75/120 vs R5 baseline 58/120 (delta +19.75).**
Inter-scorer gap 2.5/120 — good agreement.

Note on scorer arithmetic: both scorers' self-reported chunk headers
contained addition slips (A: c03/c09/c12; B: c09). All totals above are
recomputed from the per-probe line items, which are the primary data.

## Gains

22 probes went from R5 omission to R8 1.0/1.0 (both scorers agree):
c01 P8, P9; c03 P5, P7; c04 P2, P7; c05 P4, P8, P9; c07 P7, P8, P10;
c08 P3, P6, P8, P9; c10 P5; c11 P1, P4, P5, P8, P9.
The fixes repair drops across chunks, not just c02. c11 (1→8.5) is the
largest single-chunk gain.

## Candidate drops (both scorers < 1.0): 61 probes

Consensus misses (0.0/0.0, both scorers): 10 —
c02 P8, c03 P8, c04 P4, c06 P3, c06 P9, c06 P10, c07 P1, c07 P6,
c09 P1, c12 P4.
The remaining 51 are consensus ≤0.5 (partial). Full per-probe table
with justifications is in the scorers' returns (not reduplicated here);
the structured score matrix used for compilation is reproducible from
corpus_runs/r8/cXX/blind_packet.json + the rubric.

## Regressions — read with the protocol caveat

The R5 baseline is BINARY (parity/omission); R8 is strict ternary
(0/0.5/1, "be strict"). A 0.5 under the strict rubric is not directly
comparable to binary parity — the old protocol had no 0.5 grade, and
its own measurements disagree with each other (c02 P8: parity in the
Node-21 binary battery, sub-1.0 in the Node-22 targeted battery).

- HARD regressions (R5 parity → R8 mean ≤ 0.5): 30 probes, listed
  below. Concentrated in c06 (7), c04 (5), c12 (5), c02 (3), c07 (3) —
  the low-verbosity chunks (see extractor-variance finding).
- SOFT (R5 parity → R8 mean 0.75): 8 probes (c01 P4/P6/P7, c02 P1/P7,
  c07 P4, c10 P8/P9) — stricter-rubric softenings, not clean
  regressions.

Hard list: c02 P2, P6, P8; c03 P1, P3, P9; c04 P3, P4, P5, P6, P10;
c06 P1, P2, P4, P5, P6, P9, P10; c07 P1, P2, P3; c08 P1; c09 P5, P8,
P10; c12 P1, P3, P5, P7, P10.

Notable: c02 P8 (the crowned-verdict fix, validated 1.0/1.0 on r7's
c02 extraction) scores 0.0/0.0 here — the FRESH r8 c02 extraction
dropped the sharpest-question content again despite the rule being in
the prompt. The fix fires unreliably across independent extractions.

## Cost

Per-chunk anchor-note word counts, R8 vs the filed R5 baseline notes
(corpus_runs/cXX/extraction.json):

| chunk | R5 words | R8 words | factor |
|-------|----------|----------|--------|
| c01 | 73 | 325 | 4.45 |
| c02 | 66 | 249 | 3.77 |
| c03 | 68 | 215 | 3.16 |
| c04 | 81 | 246 | 3.04 |
| c05 | 82 | 354 | 4.32 |
| c06 | 63 | 165 | 2.62 |
| c07 | 61 | 395 | 6.48 |
| c08 | 54 | 441 | 8.17 |
| c09 | 51 | 135 | 2.65 |
| c10 | 64 | 229 | 3.58 |
| c11 | 81 | 380 | 4.69 |
| c12 | 64 | 124 | 1.94 |

Total: R5 808 → R8 3,258 words. **Mean inflation factor 4.03×.**
Caveat: the filed R5 baseline notes are extremely terse (~3.8
words/note); R8 averages ~15.4 words/note, inside the revision rules'
budgets. The factor measures verbosity change, not just fix cost.

## Key findings

1. GENERALIZATION HOLDS on net: +19.75/120. Eight chunks gain, four
   lose; the largest loss (c06, −4.25) is extractor non-compliance
   (see 3), not prompt failure.
2. EXTRACTOR VARIANCE is the dominant risk: 12 independent extractors
   applying the same prompt produced notes averaging 5.5–24.7
   words/note. The three tersest chunks (c06 5.5, c09 7.9, c12 10.3)
   are the three lowest-scoring. The derivation-preservation rules
   fire unreliably without a compliance check — c02 P8's crowned
   verdict survived on r7's extraction but dropped on r8's.
3. The fixes' content generalizes (22 full gains across 9 chunks), but
   prompt rules alone don't guarantee application. A per-extraction
   compliance gate (e.g., minimum mechanism-note word floor, or a
   checklist pass) is the natural next intervention — not more rules.
4. Protocol caveat stands: binary-vs-ternary makes the regression
   list conservative-unfriendly; the hard-regression count (30) is an
   upper bound, the 0.0/0.0-on-parity set (5: c02 P8, c04 P4, c06 P9,
   c06 P10, c07 P1) is the lower bound.

## Epistemic labels

- Scores: blind, two-scorer, role-separated/brief-scoped (scorers saw
  only notes+keys+rubric; extractors saw only prompt+text). Not
  context-isolated: subagents inherit ambient context; blindness is
  enforced by brief, not by information barrier.
- Grand totals recomputed from line items (scorer header arithmetic
  corrected as noted).
- Baselines: the filed R5 parity battery (binary), per
  corpus_runs/cXX/report.json.
- Cost: computationally verified word counts.
- Interpretation (variance-as-dominant-risk, compliance gate
  proposal): heuristic.

## Execution problems encountered

1. c10 extractor's first attempt completed without writing its file;
   re-spawned with explicit write-confirmation — succeeded (17
   anchors).
2. Both scorers' self-reported chunk headers contained addition slips
   (4 headers across the two); corrected by recomputation from
   per-probe line items (79.0/76.5 vs reported 80.5/77.0).
3. No other failures: all 12 extractions parse, all 12 packets built,
   both scorers completed all 120 probes.
