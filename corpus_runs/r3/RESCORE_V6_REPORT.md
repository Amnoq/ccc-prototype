# Blind v6 parity rescore — report

Date: 2026-10-04. Decision tree Node 18, Track 1.
Protocol: `SCORER_BRIEF.md`. 4 scorers, each scoring v5 control
(`rehydrated.json`) and v6 candidate (`rehydrated_v6.json`) for 3
chunks, blind to prose/wire, against the 10 locked probes per chunk.
Rubric 0 / 0.5 / 1; miss classes OMISSION / FABRICATION.
Per-probe records primary; all totals recomputed from them.

## Result

| wire | mean /10 | range | full marks (1.0) | halves | zeros |
|------|----------|-------|------------------|--------|-------|
| v5 control (rescore) | **4.88** | 4.0–6.0 | 7/120 | 103/120 | 10/120 |
| v6 (rescore) | **6.00** | 4.5–9.0 | 32/120 | 80/120 | 8/120 |
| **delta** | **+1.12** | — | +25 | −23 | −2 |

Per-chunk (v5 → v6): c01 4.0→4.5, c02 5.0→5.0, c03 4.0→5.5,
c04 6.0→7.0, c05 5.0→5.5, c06 6.0→9.0, c07 4.0→6.5, c08 5.5→7.5,
c09 4.5→6.0, c10 4.5→5.0, c11 5.0→5.0, c12 5.0→5.5.
10/12 chunks gain, 2/12 tie, 0/12 decline.

Per-scorer deltas (each scorer did both wires): S1 +2.0, S2 +4.5,
S3 +6.0, S4 +1.0 — all four agree on direction.

Miss classes: **0 FABRICATION** in either wire (R3's zero-hallucination
bar preserved). All v6 misses are OMISSION.

Per probe class (from `probe_classes.json`):

| class | orig v5 (R3) | new v5 | new v6 |
|-------|--------------|--------|--------|
| NUMBER | 0.60 | 0.50 | 0.57 |
| VERDICT | 0.73 | 0.47 | 0.57 |
| MECHANISM | 0.68 | 0.49 | 0.61 |

The v6 gain is spread across all three classes and largest in
MECHANISM (+0.12/probe) — the exact class R3 identified as the
remaining frontier ("mechanism-grade why content").

## The calibration finding: scorer drift

The v5 control does **not** reproduce the published 6.79 — it scores
4.88, a −1.91 drift. The v5 structures are byte-identical to R3's, so
this is scorer strictness, not wire degradation.

Probe-by-probe transition (original R3 v5 → new v5 rescore, 120 probes):

- 1.0 → 0.5: **42** (the dominant move)
- 1.0 → 1.0: 7
- 0.5 → 0.5: 60 (stable)
- 0.5 → 0.0: 3
- 0.0 → 0.0: 6 (stable)
- 1.0 → 0.0: 1, 0.0 → 0.5: 1

The drift is a **threshold shift**: the new scorers systematically
withhold 1.0 (42 of the original 50 full marks downgraded to halves)
while 0.5s and 0.0s are largely stable. Rank ordering is preserved;
the bar for "complete" moved.

## Interpretation

1. **The absolute v6 number (6.00) cannot be compared to 6.79 or 7.42.**
   Different scorer protocols; the threshold shift invalidates
   cross-protocol level comparisons.
2. **The valid measurement is the within-protocol delta: +1.12**
   (v5 4.88 → v6 6.00), blind, same scorers, all four agreeing on
   direction, 10/12 chunks gaining. This is a real v6 effect.
3. **Mechanism of the gain:** v6 earns 32 full marks vs v5's 7 — the
   note channel converts 0.5s into 1.0s by supplying load-bearing
   numbers, mechanism steps, and honesty caveats. That is exactly what
   the note channel was designed to do.
4. **On the prediction** (v6 recovers the injection→wire gap toward
   7.42): the R3-measured wire loss was 0.63 (7.42→6.79, original
   scorer). The new-protocol v6 gain is +1.12 — larger than the
   measured loss. Consistent with full recovery of the gap, but not a
   direct confirmation: confirming 7.42 would require scoring the
   injection under the new protocol, which was not done. Stated as
   consistent-with, not established.
5. **No chunk regressed under v6.** The note channel is pure gain in
   this battery.

## Files

- Scores: `corpus_runs/r3/rescore_v5/cNN.json`,
  `corpus_runs/r3/rescore_v6/cNN.json` (24 files, all validated:
  10 probes P1–P10, scores in {0, 0.5, 1}, totals recomputed).
- Original R3 scores: `corpus_runs/r3/upstack_scores.json`.
- Probe classes: `corpus_runs/r3/probe_classes.json`.

## Appendix: scorer's per-probe notes (S4: c10–c12, received post-compile)

Numbers match the compiled aggregates. Detail on where v6 moved scores:

- **c10 P1 (0.5 → 1.0)** — Weyl's-law kill of L1–L3. v6 notes carried
  the two load-bearing details v5 lacked: the dimension-specific
  counting argument and the 12b enumeration numbers, plus the
  honest-loophole note. Reference fully reconstructible.
- **c12 P8 (0.5 → 1.0)** — Wu-Sprung kill. v6 note carried the
  zeros-as-input mechanism *and* the self-explaining kill (fractal
  artifact finding), which with the forward-direction-test edge
  reconstruct the full reference.
- **c11 flat 5.0/5.0.** v6 notes added real numbers (several probes
  visibly closer) but none crossed a full threshold — each still
  missed a load-bearing honesty qualifier or formula.
- **c10 P4 0.0 both wires** (OMISSION): the Prime Zipper Law guardrail
  (counterexample, rejected patch) is absent from both structures;
  only the bare label survives. A genuine structure gap, not scorer
  noise.

Scorer caveats: single-scorer judgments (per-probe records primary);
v6 gains came specifically from notes carrying numbers and honesty
qualifiers — where notes were thin, scores didn't move; blinding was
by input restriction (protocol-blind, not amnesiac), same as R3.

## Appendix: scorer's per-probe notes (S3: c07–c09)

- **c08 P3 (0.5 → 1.0)** — Guinand–Weil step-2. v5 labels named the
  claims; v6 notes delivered the load-bearing numbers (Gaussian
  squares, pole−arch−drain ≈ 0). "Labels name, notes prove."
- **c07 P9 (0.0 → 0.5)** — D9 four-components. v5 had only the
  headline (0.0); v6's note named two of four components — genuine
  gain, saturation numbers still don't travel.
- **c09 P9 (0.5 → 1.0)** — 11d spectral verdict. v6 notes added
  derivation evidence and the exact/continuous distinction.
- Pattern: v6 gains came almost entirely from notes; probes stuck at
  0.5 missed mechanism steps the notes didn't carry.
- Flagged strict calls: c07 P9/P10 (v5) and c09 P7 (both wires) at
  0.0 — a second scorer might calibrate to 0.5; per-probe records
  make that adjustment trivial.

## Appendix: scorer's per-probe notes (S1: c01–c03)

- **c03/P1, P3, P9** (all 0.5→1.0): notes added the marker/survivor
  mechanism, the honest-boundary numbers, and the 9a/9b/9c honesty
  qualifiers.
- **c01/P7** (0.5→1.0): note added the "shuffled weights also GUE"
  caveat — the structure now fully answers the bridge-plank probe.
- **c02 flat 5.0/5.0** — the most mechanism-heavy chunk (D1 proof
  steps, cone bijection, renormalization). Notes added verification
  scopes but not mechanism steps; every probe stayed at 0.5.
- Refinement on the class finding: v6's notes move probes whose gap
  is numbers or honesty qualifiers — including mechanism-class probes
  of that kind (c10/P1, c08/P3, c09/P9) — but not probes whose gap is
  proof steps. The note channel helps mechanism *answers*, not
  mechanism *derivations*. Consistent with R3: derivations remain the
  frontier.

## Appendix: scorer's per-probe notes (S2: c04–c06)

- **c06 P8** (0.5→1.0): v6 note answered "why it matters
  computationally" — purest note-channel demonstration.
- **c06 P7** (0.5→1.0): v6 notes completed the compatible/incompatible
  split the probe demands.
- **c04 P1** (0.5→1.0): v6 notes carried the load-bearing numbers the
  NUMBER rule requires.
- Within-band gains: several probes got real content without crossing
  (c04 P4/P5/P7, c05 P2/P8) — notes add value below the threshold too.
- **Extraction gaps vs wire gaps:** c05 P3/P7 at 0.0 on *both* wires —
  the content is absent from the extraction itself, not a wire loss.
  c06 P9/P10 at 0.5 both — K-theoretic construction never made it into
  labels or notes. (Relevant to the R4 battery: re-extraction may
  recover these.)
- Calibration flags (soft 1.0s): c06 P2/P6 v6, c04 P8 v6.
- Self-correction: scorer caught and fixed a c04 v5 total (6.5→6.0);
  per-probe records primary. On-disk totals verified.
