# Blind decoder brief — round 4 (D-item syntax fidelity)

## Your role
BLIND DECODER, round 4. The encoding syntax has changed: mechanisms now
ride as **D-items** — the paperwork's natural derivation form
(rule / staged generation / carried verifications / honest boundary /
honest label). Read in full, in order:
`corpus_runs/DITEM_SPEC.md`, `corpus_runs/DITEM_ITEMS.md`
(under `~/workspace/ccc-prototype/`).

## Hard rules (unchanged)
1. No corpus files. Only the two files above.
2. No recalled conclusions. A step needing a fact not in the D-item +
   spec + your derivation + code + textbook math -> STOP, mark the gap.
3. No web search on the mechanism topics.
4. Code allowed and expected: recompute every verification check.
5. Textbook mathematics allowed.
6. Corpus-specific names only for properties you derived in the trace.
7. The D-items contain no smuggled answers (checked): Generates stages
   carry prescriptions, not outcomes; Verified carries checks to
   recompute. If you catch a smuggled value/statement, flag TRIPLE FLAW.

## What is new this round
- **Checksums:** for each Verified check, recompute by code and compare
  against the carried values -> CHECKSUM-MATCH (report the exact
  comparison, including edge cases) or CHECKSUM-MISMATCH (report the
  discrepancy exactly).
- **Honest boundary (the main test):** state each item's boundary, then
  answer the probe questions below. A probe whose answer the boundary
  forbids -> BOUNDARY-BLOCKED (cite the boundary). A probe answerable
  from the derivation -> answer it with derivation citation.
- **UNVERIFIED:** a check marked [pending data] -> UNVERIFIED with the
  criterion stated.

## Probe questions (answer all five, with citations)
1. D-T1: does the item establish π₂(x) ~ 1.32032·x/(log x)²?
2. D-T1: does the item establish that the survivors ≤200000 are twin lowers?
3. D-T8: does the item prove the prime number theorem?
4. D-T8: does the item establish Σw(S) → 1 numerically?
5. D-T2: does the item establish that link-face counts match direct counts at full scale?

## Calibration
Honest CHECKSUM-MISMATCH, BOUNDARY-BLOCKED, UNVERIFIED, DRIFT, LOST are
successes. Do not force a MATCH or an establishment the item does not support.

## Required output (per D-item)
- Well-formedness check (six fields present?).
- Per Generates stage: derivation trace (numbered steps) + verdict.
- Per Verified check: recomputation + CHECKSUM-MATCH/MISMATCH/UNVERIFIED.
- Honest boundary restated + the conclusions it forbids.
- Answers to the applicable probe questions.
- Honest label: carried (no derivation).
- Final table + any TRIPLE FLAW flags.
