# R5 parity rescore — report

Date: 2026-10-06. Decision tree Node 21.
Protocol: blind, 4 scorers × 3 chunks, 10 locked probes/chunk,
0/0.5/1 rubric (SCORER_BRIEF_R5.md, identical to SCORER_BRIEF_V7.md).
Scorers saw ONLY `rehydrated_v7.json` + `probes.yaml`. All 120
per-probe records validated; totals recomputed. Plus 2 drift-control
scorings: S1 and S2 each scored an existing R4 rehydrated chunk
(c02, c06) under the same rubric, blind to prior scores.

## Parity

| chunk | R5 /10 | R4 /10 | Δ |
|-------|--------|--------|---|
| c01 | 7.0 | 4.5 | +2.5 |
| c02 | 9.0 | 6.5 | +2.5 |
| c03 | 9.5 | 7.0 | +2.5 |
| c04 | 10.0 | 9.5 | +0.5 |
| c05 | 9.5 | 9.0 | +0.5 |
| c06 | 9.5 | 9.0 | +0.5 |
| c07 | 8.0 | 6.0 | +2.0 |
| c08 | 9.5 | 8.5 | +1.0 |
| c09 | 8.5 | 7.0 | +1.5 |
| c10 | 9.0 | 8.0 | +1.0 |
| c11 | 7.5 | 7.0 | +0.5 |
| c12 | 10.0 | 7.5 | +2.5 |
| **mean** | **8.92** | **7.46** | **+1.46** |

Every chunk gained or held; zero declines. Range 7.0–10.0.
**Zero FABRICATION** (120 probes; all sub-1.0 probes OMISSION).

Per probe class (locked probe_classes.json: 15 NUMBER / 15 VERDICT / 90 MECHANISM):

| class | R5 | R4 | Δ |
|-------|-----|-----|-----|
| NUMBER | 0.867 | 0.73 | +0.14 |
| VERDICT | 0.833 | 0.70 | +0.13 |
| **MECHANISM** | **0.906** | **0.76** | **+0.15** |

## Cost (measured)

- Wire tokens: mean 913, range 585–1299 (R4: 483).
- Deployment break-even: mean **2.84**, **9/12 ≤ 3** (R4: 2.06,
  12/12). Breaches: c04 3.23, c05 3.22, c06 3.14.

## Calibration and the strictness question

Ones-rate: R5 **79.2%** vs R4 battery 50.8% — a real strictness gap
to reckon with. Two readings possible (lenient scorers vs richer
wires); the drift controls adjudicate:

| control | scorer | R4 wire (this scorer) | R4 wire (battery) | R5 wire (this scorer) |
|---|---|---|---|---|
| c02 | S1 | 7.5 | 6.5 | 9.0 |
| c06 | S2 | 6.0 | 9.0 | 9.5 |

- S1 runs +1.0 vs the battery (inside the ±1.5 known variance).
- S2 runs **−3.0** vs the battery on the identical wire — a
  strictly harsher scorer — yet scores the R5 wire at 9.5.
  Per-probe: on 7 probes where the battery gave the R4 wire 1.0,
  S2 gave 0.5; on the R5 wire S2 gives 1.0 on all 7. The R5 wire
  clears a *higher* bar. A leniency artifact cannot survive a
  strict scorer.
- Within-scorer wire deltas (same scorer, same probes — the
  strictness-free evidence): **+1.5** (c02), **+3.5** (c06).
  On MECHANISM probes only: +0.188 (c02), **+0.429** (c06).
  S2's report is explicit: the R4 wire "lost points on exactly the
  probes needing mechanism" — the derivation-chain notes are doing
  the work.

Reading: the wire effect is real and isolated from scorer
strictness. The absolute R5-vs-R4 cross-battery delta (+1.46)
carries between-scorer variance (observed −3.0 to +1.0 on
controls); the within-scorer deltas (+1.5/+3.5) are the rigorous
core.

## Verdict vs the pre-registered prediction

Prediction (Node 21 draft): MECHANISM ≥0.85 (from 0.76), BE_dep ≤3
held, zero fabrication held.

- **MECHANISM ≥0.85: MET** — 0.906. [computationally verified]
- **BE_dep ≤3: PARTIAL** — mean 2.84 ≤3 holds; 9/12 chunks ≤3
  (c04/c05/c06 breach). The strict 12/12 bar is not met.
  [computationally verified]
- **Zero fabrication: HELD** — 0/120. [computationally verified]

## Triadic reading

1. **Claim CONFIRMED:** R5 raises parity toward the ceiling —
   MECHANISM 0.906 clears the bar; within-scorer wire deltas prove
   the derivation notes caused it. The c02 boundary (most
   derivation-heavy chunk: 6.5 → 9.0) moved most.
2. **Polar opposite ELIMINATED as stated:** the mechanism gap was
   reducible — derivations do travel when the notes carry chains,
   not just verdicts. Its cost concern survives in weakened form:
   the gain cost 0.78 BE_dep of headroom (2.06 → 2.84), and 3/12
   chunks exceed the bar.
3. **Null HELD:** no fabrication (0/120); the R4 battery stands as
   the control arm; drift controls show the gain is in the wire,
   not the scorers.

## What R5 did and didn't move

Moved: mechanism derivations now travel — scorers reconstruct
proof steps, key moves, and prescriptions from notes (c02, c03,
c06, c09, c12 all show it). The V7 report's "systematic remaining
gap" (mechanism detail absent from notes) is substantially closed.

Didn't move: *interpretive framing* — S4's note: c11's remaining
0.5s are definitional/classical/retrodictive distinctions and
legitimation narratives, not numbers or steps. R5 improved wire
*content* more than interpretive *framing*. That is the next
boundary, if one is drawn.

## For the M4 decision (the user's)

The R5 distribution is the evidence the provisional GO was waiting
on: extraction CAN close the mechanism gap (MECHANISM 0.906 ≥ 0.85)
at a cost (BE_dep 2.84 mean, 3/12 chunks over the ≤3 bar) with zero
fabrication risk (0/120). The kill criteria remain armed: if the
user holds the original faithful-memory bar rather than the
redefined verdict-and-relation product, the 3 breaching chunks and
the interpretive-framing residue are the honest costs to weigh.
