# CCC-2 parity gate — report

Date: 2026-10-06. Decision tree node CCC2-4.
Protocol: blind, 4 scorers × 3 chunks, 10 locked probes/chunk,
0/0.5/1 rubric (SCORER_BRIEF_CCC2.md, rubric-identical to
SCORER_BRIEF_R5.md). Scorers saw ONLY `rehydrated_ccc2_cNN.json`
(decoded D-wire records, checksums stripped) + `probes.yaml`.
All 120 per-probe records validated; totals recomputed. Plus 2
drift-control scorings (R5's protocol exactly): S1 scored the R5
v7 wire c02, S2 scored the R5 v7 wire c06, same rubric, blind to
prior scores. Wire integrity: validate.py 12/12 OK before
measurement; no repairs.

## Parity

| chunk | CCC-2 /10 | R5 /10 | Δ |
|-------|-----------|--------|---|
| c01 | 9.0 | 7.0 | +2.0 |
| c02 | 9.0 | 9.0 | +0.0 |
| c03 | 10.0 | 9.5 | +0.5 |
| c04 | 10.0 | 10.0 | +0.0 |
| c05 | 10.0 | 9.5 | +0.5 |
| c06 | 10.0 | 9.5 | +0.5 |
| c07 | 9.5 | 8.0 | +1.5 |
| c08 | 10.0 | 9.5 | +0.5 |
| c09 | 10.0 | 8.5 | +1.5 |
| c10 | 10.0 | 9.0 | +1.0 |
| c11 | 10.0 | 7.5 | +2.5 |
| c12 | 9.5 | 10.0 | −0.5 |
| **mean** | **9.75** | **8.92** | **+0.83** |

Range 9.0–10.0. Eleven chunks gained or held; one decline (c12
−0.5: Connes absorption mechanism reduced to a guardrail
parenthetical — OMISSION). **Zero FABRICATION** (120 probes; all
six sub-1.0 probes OMISSION).

Per probe class (locked probe_classes.json: 15 NUMBER / 15 VERDICT / 90 MECHANISM):

| class | CCC-2 | R5 | Δ |
|-------|-------|-----|-----|
| NUMBER | 0.967 | 0.867 | +0.10 |
| VERDICT | 0.933 | 0.833 | +0.10 |
| **MECHANISM** | **0.983** | **0.906** | **+0.077** |

## Cost (measured) — the structural finding

Wire tokens (tiktoken cl100k_base, wrapped wire — R3-identical
conventions):

| chunk | prose | wire | wire/prose | savings |
|-------|------:|-----:|----------:|--------:|
| c01 | 2597 | 4134 | 1.592 | −1537 |
| c02 | 2525 | 3282 | 1.300 | −757 |
| c03 | 2667 | 2984 | 1.119 | −317 |
| c04 | 2704 | 3944 | 1.459 | −1240 |
| c05 | 2921 | 4367 | 1.495 | −1446 |
| c06 | 2755 | 4189 | 1.521 | −1434 |
| c07 | 3005 | 4550 | 1.514 | −1545 |
| c08 | 2460 | 3760 | 1.528 | −1300 |
| c09 | 2017 | 3363 | 1.667 | −1346 |
| c10 | 2656 | 4501 | 1.695 | −1845 |
| c11 | 3295 | 5142 | 1.561 | −1847 |
| c12 | 3872 | 3888 | 1.004 | −16 |
| **total** | **33474** | **48104** | **1.437** | — |

Every wire is LARGER than its source prose (1.004×–1.695×, mean
1.437×). Savings are negative on 12/12 chunks, so the deployment
break-even `be_dep = (prose + output) / savings` is undefined —
the wire NEVER breaks even: each deployment session costs MORE
than reading the prose. This is not a marginal miss of the ≤3 bar;
it is a category failure. The 2.78×-vs-v7 size flagged in CCC2-3
is now adjudicated: the native richness expanded past the source.

## Calibration and the strictness question

Ones-rate: CCC-2 **95.0%** vs R5 battery 79.2% — a real strictness
gap to reckon with, larger than R5's own. Two readings possible
(lenient scorers vs richer wires); the drift controls adjudicate:

| control | scorer | R5 wire (this scorer) | R5 wire (battery) | CCC-2 wire (this scorer) |
|---|---|---|---|---|
| c02 | S1 | 8.5 | 9.0 | 9.0 |
| c06 | S2 | 5.5 | 9.5 | 10.0 |

- S1 runs −0.5 vs the battery (inside the ±1.5 known variance).
  Within-scorer wire delta c02: **+0.5** (9.0 − 8.5).
- S2 runs **−4.0** vs the battery on the identical wire — a far
  stricter scorer than any in the R5 battery — yet scores the
  CCC-2 wire at 10.0/10.0/10.0 across c04–c06. Per-probe: on 9
  probes where it gave the R5 wire 0.5 (each with a named,
  specific mechanism-step omission), it gives the CCC-2 wire 1.0.
  The CCC-2 wire clears a *much higher* bar. A leniency artifact
  cannot survive a strict scorer.
- Within-scorer wire deltas (same scorer, same probes — the
  strictness-free evidence): **+0.5** (c02), **+4.5** (c06).

Reading: the wire effect is real and isolated from scorer
strictness. The absolute CCC-2-vs-R5 cross-battery delta (+0.83)
carries between-scorer variance (observed −4.0 to −0.5 on
controls); the within-scorer deltas (+0.5/+4.5) are the rigorous
core. Both favor CCC-2.

Caveats (honest): S2's 5.5 on the R5 wire is far below the
battery's 9.5 — the rubric applied with unusual strictness to
mechanism-step completeness. The direction matches R5's own
strict scorer (−3.0), but the magnitude means +4.5 should be read
as "large positive," not a precise quantity. S2 also flagged mild
label inconsistency on some CCC-2 1.0s (e.g., c04 C2 labeled
"conjectural" while its note cites Selberg's theorem) —
content-complete, not penalized, but a label-hygiene note for the
format. S1 flagged one REAL content loss vs v7: the CCC-2 c02
wire dropped the "never put the answer in by hand" maxim that the
v7 wire carries verbatim — a standing methodological principle,
absent from the native encoding.

## Verdict vs the charter benchmarks

Charter control arm (v7/R5, same corpus + blind protocol):

- **Parity ≥8.92: MET and exceeded** — 9.75 (+0.83).
  [computationally verified; cross-battery absolute carries the
  stated between-scorer caveat, within-scorer deltas are the core]
- **Wire loss +0.00: HELD** — established CCC2-3, not re-litigated.
- **BE_dep ≤3: MISSED — structurally.** Wire exceeds prose on
  12/12 chunks (mean 1.437×); break-even never occurs. The bar is
  not narrowly missed but categorically inapplicable.
  [computationally verified]
- **Zero fabrication: HELD** — 0/120. [computationally verified]

## The central question

*Does CCC-2's extra carriage earn its cost — parity ≥8.92 at
acceptable break-even, or parity gains that justify the cost, or
neither?*

**Neither — with the quality leg confirmed.** The parity gains are
real (9.75 ≥ 8.92; MECHANISM 0.983 the highest measured class
score; within-scorer deltas positive under a strict scorer; zero
fabrication). But no parity gain can justify the cost in
deployment terms, because the wire is strictly dominated by the
prose: bigger every session, forever. The rebuild proved two
things at once: the native D-item form is the highest-fidelity
mechanism carrier measured — and unconstrained native richness is
incompatible with compression. CCC-2 is not a compression codec at
this size; it is an enrichment/annotation format wearing a
codec's telomeres.

## Triadic reading

1. **Claim CONFIRMED on quality, ELIMINATED on economics.** The
   native D-wire carries more than v7/R5 at the highest fidelity
   measured (9.75, MECHANISM 0.983, 0 fabrication). The format is
   validated as a carrier; the compression use-case is not.
2. **Polar opposite (v7/R5 stands as the codec): CONFIRMED.** The
   charter's kill criterion fires on the economics leg. The
   rebuild did not converge to v7 — it overshot on richness — so
   the simple "validated as derived" reading is unavailable; the
   weaker form holds instead: the D-item shape is validated as the
   right SHAPE for mechanism carriage (it beat v7 at carrying),
   while v7's terseness is validated as the right SIZE for
   compression. The two designs optimize different objectives.
3. **Null (ledger alone):** the ledger grows — the finding is
   recorded as a dead end with its mechanism (see backward touch).

## What CCC-2 moved and didn't

Moved: mechanism derivations travel more completely than R5
(0.983 vs 0.906); NUMBER improved too (0.967 vs 0.867 — D-item
`verified[]` checks carry numbers); VERDICT (0.933 vs 0.833 —
native V-records + honest labels). The c02/c06 derivation
boundaries R5 closed are now at ceiling on most chunks.

Didn't move: interpretive framing residue persists — c07-P1
(Figueiredo recipe enumeration) and c01-P10 (novelty-table entry)
still 0.5; the boundary R5 identified is narrowed but not closed.
And one regression: the "never put the answer in by hand" maxim
lost in c02's native encoding (S1's flag) — the format has no
natural slot for a maxim that isn't a mechanism, guardrail, or
verdict.

## Backward touch

- **CCC2-1/2/3:** the format derivation succeeded at its stated
  goal (fidelity + native richness) and the cost flagged in
  CCC2-3 is now a verdict: 1.437× prose, never breaks even. The
  design lesson is open, not patched: native richness needs a
  compression discipline — denser D-items, shorter boundaries,
  selective carriage — or the D-wire's honest role is annotation,
  not compression. Recorded as the open design question.
- **v1 Node 21 / the M4 evidence base:** R5's numbers stand (the
  control arm re-measured at 8.5/5.5 by two independent scorers;
  the 8.92 absolute carries the known between-scorer caveat,
  unchanged). The M4-relevant sharpening: the mechanism-content
  frontier is NOT exhausted at 0.906 (CCC-2 reached 0.983), but
  pushing it further now has a quantified cost incompatible with
  compression. R5 remains the best measured
  compression-quality point; further quality gains live off the
  compression curve. This does not move the M4 decision — it
  prices its alternatives.
- **Charter kill criterion:** fires on the economics leg → v7/R5
  stands as the codec; CCC-2's D-wire is validated as a
  high-fidelity annotation/enrichment format. Ledger +1 (D23:
  "native richness without compression discipline").

## Method self-assessment

Followed: §1 (CCC2-4 node with Q/decision/evidence/status), §2
(labels on every claim; the cross-battery comparison carries its
calibration caveat explicitly), §3 (triadic at the gate level —
claim / v7-R5 opposite / ledger null; drift controls as the
calibration leg; the polar-opposite leg is load-bearing: without
the R5 controls this would read "9.75, great"; with them it reads
"9.75 on quality, structurally disqualified on economics"),
§4 (backward touch to CCC2-1/2/3 and v1 Node 21, recorded above),
§5 (branching identifiers below), §6 (live computation; blind
protocol replicated exactly — same probes, same rubric, same
2-control calibration; honest negatives owned same-exchange: the
structural BE miss, the c12 decline, the maxim loss, the
label-hygiene flag, the S2 magnitude caveat). Deviation: none.

---

*Gate files: `parity_gate/` (brief, harness, rehydrated inputs,
rescores, cost table). Node record: CCC2-4 in DECISION_TREE.md.*
