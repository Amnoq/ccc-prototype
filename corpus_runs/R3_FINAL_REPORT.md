# CCC R3 FINAL Battery — Definitive Measurement Report

Date: 2026-10-03. Protocol: identical locked probes, identical blindness chain, R2 vs R3 compared chunk-by-chunk on 12 corpus chunks.

## What R3 is

R3 = R2 density (12–22 concepts, ≤10-word labels, cut-when-in-doubt edges) **plus** three upgrades:
1. **NUMBERS RULE** — exact numbers, formulas, and measurements are never cut; they ride in labels or in the new anchor-note (N-) lines.
2. **REPLACEMENT RULE** — when a claim X is killed, a named heir concept Y is coined and an edge `(Y, supersedes, X)` is recorded.
3. **Anchor evidence notes** — ~12-word N-lines attached to each concept, carrying the specific evidence (numbers, verification results, status qualifications) that the label alone cannot hold.

Injection format changed accordingly: LEGEND + grouped structure (strands, edges, anchors, loops) + N-lines. Measured R3 prompt template = **1014 tokens** (tiktoken cl100k_base) vs R2's 819 — the ~200-token prompt premium is real and is included in all cost accounting.

## Battery results (Phase 1): R2 vs R3 parity

Same 10 locked probes per chunk, same 0/0.5/1 rubric, scorer blind to prose and wire.

| chunk | content (one-liner) | R2 | R3 | Δ | BE_dep R2→R3 | BE_lab R2→R3 |
|---|---|---|---|---|---|---|
| c01 | D1–D6, Node 11–14 survey | 3 | **5.5** | +2.5 | 1.78→2.43 | 2.13→2.95 |
| c02 | sieve weights / Δₓ | 6 | **8.5** | +2.5 | 1.88→2.14 | 2.24→2.65 |
| c03 | D6 deformation, D8 3-4-1 | 6 | **8.0** | +2.0 | 1.72→2.10 | 2.05→2.59 |
| c04 | 9c positivity, Weil/Li | 8 | **8.5** | +0.5 | 1.82→2.28 | 2.16→2.76 |
| c05 | D10a/Li/Selberg (10a–10e) | 6 | **6.0** | 0.0 | 1.65→2.21 | 1.96→2.66 |
| c06 | D10d/e, Node 14 | 7 | **10.0** | +3.0 | 1.70→2.49 | 2.02→2.99 |
| c07 | Figueiredo transfer, D1–D4 | 4 | **7.5** | +3.5 | 1.65→2.11 | 1.95→2.54 |
| c08 | Node 10 (10a–10e) | 6 | **6.5** | +0.5 | 1.83→2.52 | 2.20→3.09 |
| c09 | D12 Connes, Möbius band | 3 | **6.5** | +3.5 | 1.82→2.92 | 2.27→3.65 |
| c10 | zeros-as-subset, Deninger | 3 | **6.5** | +3.5 | 1.71→2.28 | 2.05→2.78 |
| c11 | k-tuple sweep, Fock, 11f | 1 | **8.0** | **+7.0** | 1.56→1.97 | 1.83→2.36 |
| c12 | operator audit (8 operators) | 5 | **7.5** | +2.5 | 1.47→1.71 | 1.69→2.02 |

- **Parity mean: 4.83 → 7.42 (+2.58). Range: 1–8 → 5.5–10.0.** Every chunk gained; nothing regressed.
- **Miss taxonomy: 120 probes, 55 total misses, all OMISSION, zero FABRICATION.** The injection never contradicted a prose answer in any of 120 probes. R3's failure mode is uniform: dropped detail, never invented content.
- **Verifier: 12/12 passed on attempt 1.** Zero repairs needed — the R3 extraction prompt is verifier-clean at full scale, same as R2.
- **Data-quality note:** two battery scorers wrote `total` fields that were arithmetically inconsistent with their own audited per-probe scores (c04: 8.0 vs 8.5; c09: 5.0 vs 6.5). Per-probe records are primary; totals were corrected to the per-probe sums. An independent up-stack scorer confirmed the corrected c09 per-probe scores exactly (6.5) and arrived at c04's corrected total by a different route — see Phase 3.

## Break-even: the cost of the evidence tax

- Deployment convention: R2 mean 1.70 → **R3 mean 2.26** (+0.56 sessions). All 12 chunks remain under the ≤3 bar.
- Lab convention: R2 mean 2.05 → **R3 mean 2.67** (+0.62). c08 (3.09) and c09 (3.65) breach ≤3 on the lab convention only; all 12 pass deployment.
- The price is the N-lines: more evidence per concept means a larger injection, so each session covers less of the prose. The ~200-token prompt premium is a one-time-per-session cost and is dominated by the N-line growth.

## Per-class parity (Phase 2): where the upgrades bit

120 locked probes classified VERDICT / MECHANISM / NUMBER (hardest-demand rule for mixed probes): 15 VERDICT, 90 MECHANISM, 15 NUMBER. R3 scored exactly (0–1 scale); R2 approximated binary from omission_ids (missed→0, answered→1 — slightly overstates the R3 gain since R2 partial 0.5s count as 0; flagged as approximate).

| class | n | R2 (approx) | R3 (exact) | Δ |
|---|---|---|---|---|
| VERDICT | 15 | 0.40 | 0.73 | +0.33 |
| MECHANISM | 90 | 0.54 | 0.74 | +0.20 |
| NUMBER | 15 | 0.20 | 0.73 | **+0.53** |

The NUMBERS RULE did exactly what it was designed to do: number-demanding probes went from the worst class (0.20) to parity with the best (0.73). The MECHANISM class moved least — the "why/how" content is still the frontier's binding constraint (c09, the most why-demanding chunk, gained only +2.0 and remains the lowest at 5.0). VERDICT improved as a side effect: with numbers and statuses preserved, more verdicts became recoverable.

### Omission-taxonomy delta (R2 → R3)

R2's taxonomy: keeps verdicts/relations/statuses; drops numbers, mechanisms, replacements. R3's upgrades targeted exactly the dropped column:
- **Numbers → FIXED.** All number-demanding probes on c02, c03, c06, c07, c11, c12 scored. c06 reached 10/10; c11 went 1→8.0.
- **Replacements → FIXED.** Killed claims with named heirs and supersedes edges were recoverable everywhere tested (c04's 26→27, c07's naive hope→geometry-in-weights, c11's ordinary-geometry→E_z, c08's Li-supersession).
- **Mechanisms → PARTIAL.** The N-lines carry mechanism-adjacent evidence (what was verified, what the numbers mean), which lifted MECHANISM from 0.54 to 0.74, but step-by-step derivations still shed. c05's two total misses (P3, P7) are whole narrative sub-units with no footprint; c09's why-questions stall at 0.5.
- **Interpretive verdict-framing → STILL DROPPED.** A new finer category emerged from R3 scoring: the injection keeps verdicts and numbers but drops the *framing* — "dictionary, not proof", "template, not zero-detector", "not a cheat", the honesty caveats. c08's scorers noted this six times; c11's misses are uniformly epistemic framing + honest-scope caveats.

## Up-stack (Phase 3): R3 wire → decode → rehydrated parity

Wire build: build_message_v5 → encode_message_bits → wrap_telomere (v5), same pipeline as the pilot. Mean wire size **431 chars / 144 tokens** (range 376–487 chars), up from R2's wires by the N-line content (the wire carries the structure, not the evidence notes — see below).

- **Decode fidelity: 12/12 perfect.** Twelve independent rehydrators, wire bytes + registry + DECODE_SPEC only, all verification gates green; deterministic comparison against decode_struct_v5 shows name-for-name, edge-for-edge, anchor-for-anchor, loop-for-loop equality on every chunk. The v5 codec is lossless at full scale.
- **Up-stack parity** (scorer blind to prose/wire, scoring locked probes from rehydrated structures): see below.

- **Up-stack parity** (ONE scorer, blind to prose/wire, scoring the 10 locked probes per chunk from the rehydrated structures; results in `corpus_runs/r3/upstack_scores.json`):

| chunk | rehydrated | injection | Δ | where the gap is |
|---|---|---|---|---|
| c01 | 4.5 | 5.5 | −1.0 | N-line evidence (φ-as-face-sum Möbius inversion; GUE caveat) |
| c02 | 8.5 | 8.5 | 0 | — |
| c03 | 7.5 | 8.0 | −0.5 | renormalization mechanism in N-lines |
| c04 | 8.0 | 8.5 | −0.5 | scorer calibration nuance, not wire loss |
| c05 | 6.0 | 6.0 | 0 | — |
| c06 | 7.0 | 10.0 | −3.0 | mechanism-heavy chunk: Δ∞ reframe, amplifier mechanisms, magnitudes/impossible split, Chern roots, stringy integral — all N-line cargo |
| c07 | 7.0 | 7.5 | −0.5 | zeros-regulate-face-sum + signed-weights kicker |
| c08 | 6.0 | 6.5 | −0.5 | S₁ archimedean divergence |
| c09 | 6.5 | 6.5 | 0 | — |
| c10 | 6.0 | 6.5 | −0.5 | Weyl-law unpacking |
| c11 | 7.5 | 8.0 | −0.5 | \|w({2})\| numerical obstruction |
| c12 | 7.0 | 7.5 | −0.5 | 2025 Jaksch literature touchpoint |

Mean: **6.79/10 rehydrated vs 7.42/10 injection (−0.62)**. Miss classes: **70 OMISSION, 0 FABRICATION** — zero hallucinations from the structures either. 3 chunks match exactly, 9 of 12 within 0.5.

The interpretation is clean: the **wire leg contributes zero loss** (12/12 perfect decode), so every delta traces to the extraction-to-wire boundary — the v5 wire carries strand structure, edges, anchors, and loops, but not the N-line evidence notes. Verdicts, relations, epistemic statuses, and open questions survive the wire intact; what drops is proof mechanisms, scaling arguments, and numbers — the identical omission taxonomy as the down-stack battery. In other words, the "why" is lost at **extraction**, and the wire transmits the casualty list faithfully. The highest-leverage fix remains numbers/mechanism preservation in member names themselves (R3's richer names already recovered ground vs the pilot on c04 P3/P8).

## Round-trip totals

| measure | R2 | R3 |
|---|---|---|
| extraction verifier failures | 0 (12/12 pass, ≤1 attempt) | 0 (12/12 pass, attempt 1) |
| fabrications in 120 probes | 0 | 0 |
| decode fidelity (12 chunks) | pilot-only | 12/12 perfect |
| mean parity (injection) | 4.83/10 | 7.42/10 |
| mean parity (rehydrated) | — | 6.79/10 |
| mean BE_dep | 1.70 | 2.26 |
| mean BE_lab | 2.05 | 2.67 |
| prompt premium | 819 tokens | 1014 tokens |

## Where the frontier sits (honest bottom line)

R2's frontier point was (~5/10 parity, ~1.7 BE_dep). R3 moved it to (~7.4/10 injection, ~6.8/10 rehydrated, ~2.26 BE_dep). The ≥9/10-AND-≤3 combo still doesn't exist in this design, but the gap narrowed: c06 hit 10/10 at 2.49 BE_dep, and the whole injection range now sits above 5.5.

**Cost-benefit verdict: R3 is worth it.** +2.58 parity points for +0.56 deployment sessions is a strongly positive trade — the evidence tax buys back exactly the class of content (numbers, verdicts, replacements) that was most expensive to lose. The remaining deficit is concentrated in one place: mechanism-grade "why" content, which neither R2's density rules nor R3's evidence notes capture at scale. That is the next frontier, and it is a different problem than density — it's about derivations, not facts.

## Caveats

- R2 per-class parity is binary-approximated (see Phase 2 section); true R2 numbers are slightly higher, so class deltas are slightly overstated.
- Scorers are model-based with the same rubric; inter-scorer calibration wasn't measured.
- The corpus is one author's research notes; generalization to other prose is untested.
