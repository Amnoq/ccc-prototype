# M3 report — probe parity + cost accounting on held-out chunk 4 (2026-10-03)

## Protocol (per HARNESS_MVP_SCOPE.md §3.4–3.5)

1. **Probes written blind.** 10 why/how probes drafted from the chunk-4 source
   prose (`chunk4_memorysys_HELDOUT.txt`, the memory-system discussion) with
   prose answers locked in `m3_probes.yaml` — before any extraction existed.
2. **Extraction as a separate pass.** A subagent served as `llm_fn` with the
   exact `EXTRACTOR_PROMPT`, given only the prompt + chunk text (never saw the
   probes). Output saved to `m3_attempts/chunk4_a1.json`.
3. **Deterministic verification.** `validate_extraction` + `verify_roundtrip`.
4. **Probe answering from structure only.** Grouped compact injection built via
   `inject_grouped` (`m3_attempts/chunk4_injection.txt`); each probe answered
   strictly from the legend + injection, scored against the locked prose
   answers. Failure modes recorded separately: omission vs hallucination.
5. **Cost accounting** in cl100k_base tokens (tiktoken, same method as M2).

## Extraction result

- 34 concepts, 8 strands, 21 edges, 33 anchors, 3 loops.
- **Verifier: PASS on attempt 1, 0 repairs.** v5 round-trip clean.
- Verifier pass rate 100% within 2 repairs: **met.**

## Parity score: 9/10, zero hallucinations

| probe | topic | verdict |
|---|---|---|
| P1 | codec/transport vs memory system; gap vs Letta/Zep/Mem0 | parity (survey-citation detail dropped) |
| P2 | three stack layers + roles | parity ("evolving in lockstep" dropped) |
| P3 | extractor as gating problem; metric | parity |
| P4 | entity-resolution failure mode | parity (wheel_210 example dropped; mechanism preserved) |
| P5 | CCC meets RAG, doesn't replace it | parity |
| P6 | integrity as differentiator; corruptions; vector-store contrast | **omission (partial)** — corruption list present, but the competitive contrast ("vector stores offer none of this on interchange paths") and the subagent-hop selling point are not in the structure |
| P7 | v5 temporal gap vs Zep; v6 path | parity (st_verified→st_superseded example dropped) |
| P8 | memory_harness.py MVP components | parity |
| P9 | LongMemEval/LoCoMo as external yardstick | parity |
| P10 | decision-tree practice rationale | parity (purpose clause compressed) |

**Pattern of the misses:** the structure preserves claims, mechanisms, and
relations, but drops concrete illustrations, examples, and purpose clauses —
most of which live in anchor notes. The grouped injection drops anchor notes
entirely, which is what cost P6. That is a read-path finding, not an
extraction failure: either inject notes or accept the loss.

**No hallucinations:** nothing in the structure supports a wrong answer to any
probe.

## Cost accounting (measured)

| quantity | tokens (cl100k_base) |
|---|---|
| source prose | 1210 |
| extraction input (prompt + chunk) | 1852 |
| extraction output (JSON) | 2586 |
| **extraction total** | **4438** |
| injected structure (no legend) | 369 |
| injected structure (with legend) | 956 |
| savings / session (legend one-time, M2 convention) | 841 |
| **break-even** | **5.28 sessions** |

### Addendum 2026-10-03 — deployment accounting

The lab accounting above transmits the 642-token extractor prompt with every
extraction (per §3.5: "source + schema prompt + any repair retry"). The
deployment model is different: the extraction protocol lives in the LLM's
memory itself (system/fine-tuned/persistent), so the marginal per-extraction
input is the chunk alone. Recomputed on that basis:

| quantity | tokens (cl100k_base) |
|---|---|
| extraction input (chunk only) | 1210 |
| extraction output (JSON) | 2586 |
| **extraction total (marginal)** | **3796** |
| savings / session | 841 |
| **break-even (deployment)** | **4.51 sessions** |

This clears the written >5 no-go line but still misses the ≤3 GO bar. The
remaining gap is the output verbosity (2586 tok for the JSON) — the same
lever identified above. Note: the convention change applies to M2's figures
as well (chunk-1 break-even would revise from ~3.5 to ~3.0); M2_REPORT.md is
left as-measured, flagged here for consistency.

## Against the M4 thresholds (§3.6)

- parity ≥ 9/10: **met** (9/10)
- zero hallucinations: **met**
- break-even ≤ 3: **missed** (5.28; >5 is the written no-go line)
- verifier 100% within 2 repairs: **met**

Two structural observations on the cost miss:

1. **The extraction JSON (2586 tok) is 2.1× the source prose (1210 tok).**
   The 3.3× compression (1210→369) comes from the v5 codec + grouped
   injection, not from extraction per se. Extraction is the expensive,
   lossy step; the wire + injection is where the value materializes.
2. **Break-even is chunk-size-sensitive and this chunk is small**
   (1210 tok, below the 2–4k target). Extraction cost has a large fixed
   component (schema prompt + per-concept output overhead), so larger
   chunks amortize better. The output verbosity (34 concepts for 1.2k
   tokens) is the clearest lever — a tighter extraction directly cuts
   break-even.

## Caveats (honest)

1. Extractor was a separate model pass (an improvement on M2's
   author-as-LLM), but still one frontier model — the naive-model trial is
   still required before "an LLM can do this" generalizes.
2. The probe-answerer had read the prose when writing the probes.
   Mitigations: prose answers locked before extraction existed; answers
   produced from the injection file only. Interpretive leakage cannot be
   fully excluded.
3. Corpus is home turf (same CCC arc as M2). Messy dialogue untested.
4. n=1 chunk. This is a single measurement, not a distribution.

## Status

**M3 done.** Parity score, failure-mode breakdown, and break-even number
exist. M4 (go/no-go against §3.6) is now a decision awaiting input — the
numbers as measured sit split: parity/hallucination/verifier bars met,
cost bar missed on a below-target chunk.
