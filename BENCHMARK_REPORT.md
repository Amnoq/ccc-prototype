# Application-half benchmark report

**Date:** 2026-10-08. **Kind:** pure measurement — nothing was tuned.
**Scripts:** `~/workspace/ccc-prototype/benchmark_wires.py` (tasks 1–2),
`~/workspace/ccc-prototype/benchmark_packets.py` (tasks 3–4).
Raw JSON: `/tmp/bench_wires.json`, `/tmp/bench_packets.json`
(ephemeral; per-chunk tables embedded below).
**Tokenizer:** tiktoken `cl100k_base` throughout.

## Method

- **v7** (`corpus_runs/r5/cNN/wire_v7.json`): timed the full
  application-half path — JSON parse → telomere scan/unwrap
  (`scan_telomeres`) → `decode_wire_v7` → `Registry` rebuilt from the
  shipped name list → `first_n_primes` → `decode_struct_v7`. Wire
  tokens measured on the `wrapped` string (same convention as the R5
  battery). "Per-record" for v7 = per anchor (the verdict-carrying
  unit in the rehydrated struct); per-anchor tokens are amortized
  (wire tokens ÷ anchors), reported alongside native note tokens.
- **D-wire** (`ccc2/wires/cNN.wire`): timed `ccc2/codec.py:decode`
  (telomere check → wire checksum → per-record checksum +
  wellformedness). Wire tokens on the full wrapped bytes. Per-record
  tokens on the canonical record JSON.
- Timing: 5 warm-up reps, then 30 timed reps per chunk
  (`time.perf_counter`); reported as mean/p90/min–max across the 12
  chunks. Cold-start measured separately (fresh process, no warm-up).
- **Packet simulation** (225 D-wire records): one packet per record
  per `VERDICT_PACKET_SPEC.md` — canonical JSON (keys sorted, no
  whitespace), SHA-256 checksum. Field mapping documented in
  `benchmark_packets.py` header: claim/label/boundary from native
  record fields (D=`honest_label`, V=`status`, C=`status`,
  G=`killed` per SPEC §2 "guardrail (killed path)", B/L=`heuristic`
  as a documented simulation assumption — D-wire v1 carries no
  native label for these); span is a **null-span placeholder**
  (`start:0,end:0`) because D-wire v1 records carry no source spans
  (the known Gate 4 step-0 gap). One-liners use native fields
  faithfully; first-sentence truncation is deterministic.
- **End-to-end**: build (dict → canonical → SHA-256) + apply
  (parse → checksum verify → tier lookup per `COLLAPSE_SPEC.md`),
  200 reps per record.

## Results

### Per-format table

| format | unit | ms/verdict mean | ms/verdict p90 | tokens/judgment mean | tokens/judgment p90 |
|---|---|---|---|---|---|
| v7 | anchor (n=215) | 0.041 | 0.057 | 51.0 | 60.0 |
| D-wire v1 | record (n=225) | 0.020 | 0.023 | 167.0 | 197.5 |
| verdict packet | packet (n=225) | 0.025¹ | 0.029¹ | 148.7 | 202.0 |

¹ packet build (0.014) + apply/verify/lookup (0.011). Record→packet→tier
end-to-end including amortized D-wire decode: ≈0.045 ms/verdict.

### Per-chunk detail — v7

| chunk | wire tok | decode ms² | anchors | tok/anchor | ms/anchor |
|---|---|---|---|---|---|
| c01 | 724 | 0.81 | 19 | 38.1 | 0.043 |
| c02 | 726 | 0.55 | 14 | 51.9 | 0.040 |
| c03 | 803 | 0.52 | 15 | 53.5 | 0.035 |
| c04 | 1020 | 0.63 | 18 | 56.7 | 0.035 |
| c05 | 1109 | 0.65 | 19 | 58.4 | 0.034 |
| c06 | 1026 | 0.81 | 20 | 51.3 | 0.041 |
| c07 | 1009 | 1.23 | 19 | 53.1 | 0.065 |
| c08 | 812 | 1.06 | 18 | 45.1 | 0.059 |
| c09 | 585 | 0.51 | 17 | 34.4 | 0.030 |
| c10 | 902 | 0.57 | 15 | 60.1 | 0.038 |
| c11 | 1299 | 0.76 | 20 | 65.0 | 0.038 |
| c12 | 936 | 0.69 | 21 | 44.6 | 0.033 |

² mean of 30 warm reps; p90 across chunks 1.03, range 0.51–1.23.
v7 anchor note text alone: mean 37.4 tokens, p90 72, max 95 (n=215).

### Per-chunk detail — D-wire

| chunk | wire tok | decode ms² | records | tok/record | ms/record |
|---|---|---|---|---|---|
| c01 | 4134 | 0.40 | 23 | 132.3 | 0.018 |
| c02 | 3282 | 0.33 | 18 | 134.1 | 0.018 |
| c03 | 2984 | 0.26 | 13 | 179.3 | 0.020 |
| c04 | 3944 | 0.33 | 18 | 170.5 | 0.018 |
| c05 | 4367 | 0.34 | 17 | 208.2 | 0.020 |
| c06 | 4189 | 0.38 | 17 | 198.6 | 0.022 |
| c07 | 4550 | 0.45 | 22 | 159.8 | 0.020 |
| c08 | 3760 | 0.45 | 20 | 139.6 | 0.023 |
| c09 | 3363 | 0.50 | 16 | 161.1 | 0.031 |
| c10 | 4501 | 0.43 | 20 | 176.9 | 0.021 |
| c11 | 5142 | 0.43 | 22 | 186.7 | 0.019 |
| c12 | 3888 | 0.29 | 19 | 156.5 | 0.015 |

² mean of 30 warm reps; p90 across chunks 0.45, range 0.26–0.50.

### Packet-budget compliance (task 3)

Budget: ≤120 tokens (VERDICT_PACKET_SPEC.md).

| metric | value |
|---|---|
| packets measured | 225 |
| tokens mean / p90 / max / min | 148.7 / 202.0 / 299 / 90 |
| over budget | **165/225 (73%)** |
| by type (mean tokens) | V 190, D 168, G 159, C 152, B 152, L 95 |

Field means: claim 30.5, boundary 30.1, span 14.0, record_ref 12.3,
format 8.0, label 4.0; fixed overhead (incl. 64-hex checksum and JSON
syntax) ≈ 66 tokens — leaving ~54 tokens for claim+boundary against
native ~61. **The budget failure is structural, not a mapping
artifact:** a tight variant (first-sentence claim AND boundary
everywhere) still leaves 147/225 (65%) over budget, mean 133.6,
max 243 (c05 C1 — a single 243-token sentence). The 120-token budget
is incompatible with carrying D-wire v1's native verdict text
verbatim; p90 compliance needs ≈200 tokens.

Sensitivity checks: realistic span vs null span = **+0 tokens**
(single-token integers — the placeholder does not bias the count);
B/L label `heuristic`→`conjectural` = +1.0 token/packet — the
budget conclusion is insensitive to the documented assumptions.

### Collapse tiers reached (task 4 input)

85 SURFACE only · 53 ACT · 33 ACT with spot-check · 30 BLOCK the
claim · 17 QUEUE for review · 7 NO ACTION (the 7 `unstated`
C-records = questions, per spec).

## Against the 50 ms decision-model bar

| path | ms/verdict | × under 50 ms |
|---|---|---|
| v7 anchor decode (warm, worst chunk p90) | 0.057 | ~880× |
| D-wire record decode (warm, worst) | 0.031 | ~1600× |
| packet build + verify + tier lookup (p90) | 0.029 | ~1700× |
| end-to-end record→packet→tier (p90) | ~0.05 | ~1000× |
| cold chunk decode, fresh process (c01) | 2.4–5.5 ms/chunk | ~10–20× |

**Time is not the constraint.** The honest framing: this pipeline is
mechanical decode + lookup — no model inference. Musubi's 50 ms is a
1.7B model's *inference* budget. The fair claim is narrower and
stronger: the verdict-packet machinery adds ~0.03–0.05 ms per
verdict — it does not move the 50 ms budget at all. **The binding
constraint is tokens, not time:** 149 mean / 202 p90 per packet
against the 120 budget, and D-wire's 167 tokens/record carriage.

## Caveats (what could make these numbers unrepresentative)

- **Warm vs cold:** timings above are warm (5 warm-up reps). Cold
  chunk decode in a fresh process: 2.4–5.5 ms (D-wire c01:
  4.6–5.3; v7 c01: 2.4–5.5) — one-time interpreter/import cost,
  still 10× under the bar.
- **Machine noise:** sub-ms timings on a shared VM are
  noise-dominated (e2e range 0.021–0.041 ms), but the conclusion is
  3 orders of magnitude from the bar — robust to any plausible
  noise. Report ranges, not point estimates, at this scale.
- **v7 per-record is amortized:** the v7 wire is an int stream +
  note table, not per-record separable; 51 tokens/anchor divides the
  whole wire by anchor count. The anchor's own note averages 37.4
  tokens — the remaining ~14 is shared structural carriage.
- **D-wire decodes faster than v7** (0.38 vs 0.73 ms/chunk) despite
  4.4× the bytes: v7's `decode_struct_v7` does prime factorization
  per strand/loop; D-wire is `json.loads` + SHA-256 per record.
- **Null-span placeholder** contributes 14 tokens and, per the
  sensitivity check, a real span would add ~0 — no bias.
- **B/L label assumption** (`heuristic`) moves packet tokens by
  ~1; budget conclusion unaffected.
- **No inference measured:** if a future application layer runs a
  model over packet contents, that cost is outside this benchmark.

## Bottom line

- Per-verdict time: everything measured is 10–1700× under the
  50 ms bar, warm and cold. The packet machinery is free in time.
- Per-verdict tokens: v7 anchor 51 (p90 60) · D-wire record 167
  (p90 198) · verdict packet 149 (p90 202).
- The 120-token packet budget fails at 73% (65% even under
  aggressive faithful truncation) — structurally, not artifactually.
  p90 compliance needs ≈200 tokens.

## Backward touch — Step 4 demonstration (2026-10-08)

The A-vs-B token ratio is now measured on a real task: binary
output mean 2.1 tokens/decision vs packet mean 167.2 (p90 214,
max 281) — the label machinery adds ≈165 tokens/decision
marginal (~80× the binary output), given a shared assessment.
Time was not measured in Step 4; the benchmark's finding stands
(packet machinery free in time). Cost story updated: time is
free, tokens bind, and the token price of the label machinery
is now priced against its measured decision value (Step 4:
−10 false auto-acts for +16 queued at 26.7% review load) —
whether the price is worth it is a deployment policy question
the numbers inform but do not settle.
