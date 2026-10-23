# Up-Stack Pilot Report — the full cup-stacking event (2026-10-03)

First live-model test of the wire leg: a model that never saw the source
prose decodes the telomere-wrapped v5 wire and the locked probes are scored
against what it rebuilt. Down-stack (extraction) was measured by the corpus
battery; this measures the up-stack (wire → structure → answers) and the
round trip.

## Design principle (user, 2026-10-03)

The decoding instructions sit stored on the receiving side previous to
transmission. The codec is resident on both ends; the wire carries only the
message. DECODE_SPEC (2,244 tokens) is a one-time resident cost, like the
extraction protocol living in memory — it does not enter per-session
break-even math.

## Method

- Pilot chunks: c04 (battery parity 8/10), c06 (7/10).
- Built the real wrapped v5 wire per chunk: telomere `zz5BBFFSS…`, gamma
  bitstream in decimal triples, checksum — via `codec.build_message_v5` /
  `encode_message_bits` / `wrap_telomere`. (c04: 418 chars; c06: 334 chars.)
- Two fresh rehydrator subagents, each blind to its chunk's prose and probes.
  Inputs: wrapped wire + ordered registry names + DECODE_SPEC.md (standing
  knowledge). Python allowed for all arithmetic — the deployment assumption
  is an agent with tools, not mental gamma-decoding.
- Phase 1: decode per spec (all 7 steps incl. fingerprint + checksum
  verification), write labeled structure. No probes seen.
- Fidelity checked deterministically against `decode_struct_v5`.
- Phase 2: separate scorer, blind to prose/wire, answers the 10 locked
  probes from the rehydrated structure only. Same 0/0.5/1 rubric as battery.

## Results

| | c04 | c06 |
|---|---|---|
| Decode fidelity vs deterministic | PERFECT (bit-identical) | PERFECT (bit-identical) |
| Verification gates (telomere/fp/checksum) | all pass, 0 repairs | all pass, 0 repairs |
| Up-stack parity (from wire) | 7.0/10 | 5.5/10 |
| Battery parity (from injection) | 8/10 | 7/10 |
| Miss classes | 9 omissions, 0 fabrication | 9.5 omissions, 0 fabrication |

## Findings

1. **The wire contributes zero additional loss.** Both decodes were
   bit-identical to the deterministic decoder. The 1.0–1.5 point gap vs
   battery parity is scorer variance (the up-stack scorer graded more
   conservatively), not wire degradation — there is nothing in the wire leg
   left to lose; everything lost was lost upstream at extraction.
2. **First live-model rehydration succeeds.** Chunk 1's open problem #1
   ("no live model has ever read this wire") is answered: yes — given the
   registry and the resident spec, a model decodes the wire faithfully,
   verification gates and all, with zero repairs.
3. **The omission taxonomy is unchanged through the wire.** Verdicts,
   relations, epistemic statuses survive; proof mechanisms, scaling
   arguments, numbers are what drop — identical to the battery. The "why"
   is the casualty at extraction; the wire transmits the casualty list
   faithfully.
4. **Up-stack cost is negligible.** Wire: 140 / 112 tokens. Registry names:
   354 / 390 tokens (sync, already accounted in the original design).
   Spec: 2,244 tokens one-time resident, amortizes to zero. Against
   ~2,500 tokens saved per session, the decode leg costs ~5%.

## Round-trip totals (down + up, timed together)

- c04: extraction break-even 2.16 lab / 1.82 deployment; +140-token wire.
  End-to-end parity ≈ 7–8/10. Zero hallucinations in either leg.
- c06: extraction break-even 2.02 / 1.70; +112-token wire.
  End-to-end parity ≈ 5.5–7/10. Zero hallucinations in either leg.

## Caveats

- Pilot is 2 chunks, not 12. Full-battery up-stack is the obvious next run
  if M4 goes forward.
- Rehydrators used Python for the arithmetic. A raw LLM hand-decoding gamma
  codes would fumble — the validated claim is "agent with tools + resident
  spec," which is the realistic deployment shape.
- No adversarial conditions yet: shuffled/corrupted/missing-line wires are
  still untested against a live model (the codec handles them
  deterministically; the model leg under corruption is open).
- The bottleneck is now definitively isolated: extraction (down-stack).
  All future parity work belongs there — the R3 numbers-preservation idea
  from the improvements list is the highest-leverage next experiment.

## Files

- `corpus_runs/upstack/c04_wire.json`, `c06_wire.json` — wire packages
  (wrapped wire, registry, expected struct)
- `corpus_runs/upstack/c04_rehydrated.json`, `c06_rehydrated.json`
- `corpus_runs/upstack/score_report.json`
