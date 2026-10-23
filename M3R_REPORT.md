# M3R report — revision + re-run (2026-10-03)

Gray-zone provision exercised: one extractor revision, one re-run, then the
M4 decision.

## The revision (extractor_rev1.py, decision-tree fork)

M3's cost miss had a diagnosed cause: extraction JSON at 2.1× source prose.
The revision targets verbosity while holding parity:
- 12–22 concepts (was 15–60), aggressive merging: one concept per idea
- labels ≤10 words; load-bearing specifics IN labels (M3 P6 lesson: anchor
  notes don't survive injection)
- notes ≤8 words, evidence only
- edges only if removal loses a real argument ("when in doubt, cut")

## The re-run design (stated fork)

No fresh held-out chunk exists. Re-ran on **chunk 1** (cursor-layer
discussion, 2852 tokens — inside the 2–4k target band, fresh to the revised
prompt) rather than chunk 4, because a 1.2k-token chunk would leave the cost
question ambiguous even if the revision worked (fixed costs dominate small
chunks). Ten new why/how probes written blind with prose answers locked in
`m3r_probes.yaml` before the revised extraction; extraction as a blind
separate subagent pass (never saw probes).

## Extraction result

- 20 concepts (target 12–22 met), 6 strands, 14 edges, 20 anchors, 3 loops.
- **Verifier: PASS attempt 1, 0 repairs.** v5 round-trip clean.

## Parity score: 7/10, zero hallucinations

| probe | topic | verdict |
|---|---|---|
| P1 | 11× vs 1.16× ledger; projection | parity (exact token figures dropped) |
| P2 | two hard boundaries | parity |
| P3 | model-side decoding as the big untested | parity (explicit prioritization dropped) |
| P4 | synchronizing-word → CCC architecture mapping | **omission** — definition, instances, and design rule present; the four-part mapping (grid=codebook, patter=wire, landing=reconstruction, envelope=checksum) absent |
| P5 | encoder-searches/decoder-walks + cursor | parity |
| P6 | compression measures semantic coherence | parity (graph-nearness mechanism compressed) |
| P7 | zipping-a-zip fails; residual-structure stages | parity (entropy reason, 20–30% figure dropped) |
| P8 | source-before-channel ordering + why | **omission (partial)** — constraint present, rationale absent |
| P9 | sentence types as grammar codebook | parity |
| P10 | two cursor caveats | **omission (partial)** — shared-graph caveat partial; toy-scale-loss caveat absent |

**Not directly comparable to M3's 9/10** (different chunk, different probe
set). But the omission pattern is consistent with what the density rules
incentivize: "when in doubt, cut it" cut exactly the mechanistic
justifications — mappings, rationales, caveats — while claims and relations
survived intact.

## Cost accounting (measured, cl100k_base)

| quantity | R2/chunk1 | M3 (R1/chunk4) |
|---|---|---|
| source prose | 2852 | 1210 |
| prompt (R2 819 / R1 642) | 819 | 642 |
| extraction output (JSON) | 1606 | 2586 |
| output/prose ratio | **0.56** | 2.14 |
| injected (no legend) | 251 | 369 |
| savings/session | 2601 | 841 |
| **break-even, lab (prompt transmitted)** | **2.03** | 5.28 |
| **break-even, deployment (protocol resident)** | **1.71** | 4.51 |

The revision worked as intended on cost: output/prose 2.14 → 0.56;
break-even meets the ≤3 GO bar under **both** accounting conventions.

## Against the M4 thresholds (§3.6)

- parity ≥ 9/10: **7/10** — at the gray-zone boundary (7–8/10)
- zero hallucinations: **met**
- break-even ≤ 3: **met** (2.03 lab / 1.71 deployment)
- verifier 100% within 2 repairs: **met**

## What the re-run actually established

The experiment isolated the trade-off cleanly: **density buys cost at the
price of why-depth.** R2 holds claims, relations, and statuses at 1.71–2.03
sessions break-even, but sheds the mechanistic justifications that why-probes
need. The gray-zone remedy (one revision + re-run) is now spent, so M4 is a
genuine judgment call, and it rests on a product question rather than a
measurement gap: does the harness's memory need to preserve *rationales*
(→ a smarter revision would have to keep density AND why-depth, or accept
higher cost) or is claim-level parity sufficient for the read path (→ GO)?

## Caveats

1. Extractor still a single frontier model; naive-model trial outstanding.
2. Probe-answerer had read the prose; mitigations as in M3 (locked answers,
   injection-file-only answering).
3. n=1 chunk per prompt version; chunk-1 probes skewed toward "why"
   (mechanism-demanding), which interacts with the density rules.
4. R1 was never run on chunk 1, so the parity delta (9/10 vs 7/10) confounds
   prompt revision with chunk/probe difficulty.

## Status

**M3R done.** M4 (go/no-go) is now decidable: cost bar met under both
conventions, parity at gray-zone boundary, zero hallucinations, verifier
clean. The remaining question is the product one above.
