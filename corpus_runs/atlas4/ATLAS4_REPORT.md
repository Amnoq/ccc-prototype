# Atlas-4 Report — the archeology of AI itself (pilot)

**Date:** 2026-10-07
**Charter:** `ATLAS4_CHARTER.md`
**Ledger:** item 4 (outcome class `pass`, p_ai_1=0.70 shown, p_router pending)

## Verdict

The direct sky↔sky test found **0 adjudicated links**. Across 4 traditions of AI's own history — symbolic (McCarthy 1959), connectionist (Rumelhart–Hinton–Williams 1986), statistical (Cortes & Vapnik 1995), neuroscience (Hubel & Wiesel 1959) — 65 mechanical candidates and full semantic review of all 105 node labels surfaced no shared mathematical or empirical object between any two skies. The vocabularies are disjoint the way Atlas-3's were: advice-taker/deduction vs hidden-units/gradient vs margin/support-vectors vs receptive-fields/orientation.

The only cross-tradition links in the run are **4 split_links, all touching the bridge** (LeCun 1989):
- **S1 resolved:** bridge "synthesized kernels resemble H&W biological detectors" ↔ neuro on/off-region findings — `biological-precedent`.
- **S2 resolved:** bridge "constrained backpropagation" ↔ connectionist "generalized delta rule" — `method-application`.
- **Unseeded:** bridge "reduced VC-dimensionality" ↔ statistical "VC test-error bound" — `shares-concept`.
- **Unseeded:** bridge USPS zip-code database ↔ statistical USPS digit database — `shared-dataset` (same pool, different splits).

Zero merges, zero contradictions, zero false merges. Both positive controls resolved — the method finds links where the history documents them. The measurement is consistent with the user's prediction (narrow links, breakthroughs on the bridges), and unlike Atlas-3's S2, **both controls here are clean**. Per the charter the instrument still does not claim narrowness: the counts go to the user, whose narrow/wide verdict resolves ledger item 4.

## Metric table (Atlas-2/3 units)

| Metric | Atlas-2 | Atlas-3 pilot | Atlas-4 pilot |
|---|---|---|---|
| Corpus | 7 papers, 84 files, 521 concepts | 5 papers, 176 concepts | 5 papers, 106 concepts |
| Mechanical candidates | 310 | 3 | 65 |
| Adjudicated links | 13 (2 merges, 10 split, 1 unresolved) | 1 split_link | 4 split_links |
| Genuine merges | 2 | 0 | 0 |
| Contradictions | 0 | 0 | 0 |
| False merges | 0 | 0 | 0 |
| Direct sky↔sky links | — | 0 | **0** |
| S1 control | — | weak pass | **resolved** |
| S2 control | — | void (misseeded) | **resolved** |
| Cost | not instrumented | ~237k tok est. | ~59.6k tok est. (drafters only) |

## Honest limits

1. **Pilot scale, founding-paper gaps.** 106 concepts vs Atlas-2's 521. The connectionist extraction covers only the first ~8.6k words (scan pp. 1–32; the T-C/weight-sharing section the bridge cites lies beyond the chunk — the S2 weight-sharing attribution has no target node; S2 rests on the method link instead).
2. **H&W 1962 unobtainable (BK2011).** Four genuine routes failed (2× NCBI PMC 404 on PMC1359523, Europe PMC 403, unresolvable mirror). Substituted H&W 1959 per charter (same authors/program, recorded). Consequence for S1: the 1959 paper predates "simple/complex cell" language — the findings match the bridge's 1962 citation, the terms don't. Old J. Physiology PMC records appear systematically unservable through this fetch path (1959 also 404'd on PMC).
3. **Mechanical recall still noisy across vocabularies** (Atlas-3 limit #2 confirmed): 65 token-overlap candidates, nearly all generic ('hidden', 'units', 'error'); the 4 genuine links needed semantic review. 37 of 38 bridge↔connectionist mechanicals were noise around the 1 real method link.
4. **Tokens are ESTIMATES** (1.3× drafter-reported words). Coordinator/merge/illustration turns not instrumented. No dollar figure (no token price in the record).
5. **No merges is a finding about this corpus at this scale**, not a theorem about AI history. A wider corpus (backprop-era, transformers) could surface more — that's the full-corpus Atlas-4 design.
6. **The symbolic sky is the starkest result and the starkest caveat:** zero candidates of any kind against all four other skies. McCarthy's 1959 vocabulary (advice taker, deduction, common sense) shares literally nothing with the learning traditions — which is either the deepest disjointness in the run or an artifact of sampling one proposal paper. The user's grading should weigh this.

## Cost table (drafters only, ESTIMATE)

| Phase | Words in | Words out | Tokens est. |
|---|---|---|---|
| symbolic (McCarthy 59) | 5,505 | 1,616 | 7,157 / 2,101 |
| connectionist (RHW 86) | 8,600 | 2,022 | 11,180 / 2,629 |
| statistical (C&V 95) | 9,000 | 1,893 | 11,700 / 2,461 |
| neuro (H&W 59) | 7,518 | 1,294 | 9,773 / 1,682 |
| bridge (LeCun 89) | 5,600 | 1,766 | 7,280 / 2,296 |
| **Total** | **37,223** | **8,591** | **~48.4k / ~11.2k** |

Unit: ~1,600 tokens per 1k source words in, ~300 out. Extrapolation to a full-corpus Atlas-4 (say 20 papers, ~150k words): ~240k tokens in — shown arithmetic, still estimates.

## Records

- `manifest.json` (provenance per paper, drops, token accounting)
- `extractions/` (5 blind R4 JSONs, schema-validated)
- `graphs/` (per-sky + combined)
- `cross_sky_links.json` (11 adjudication records: 4 split_link, 7 rejected with reasons)
- `candidates.json` (65 mechanical candidates, both streams recorded)
- Views: `atlas4_symbolic.html`, `atlas4_connectionist.html`, `atlas4_statistical.html`, `atlas4_neuro.html`, `atlas4_bridge.html`, `atlas4_cross.html` (money view; 4 gold edges), `atlas4_crossview.png` (static)
- `RUN_LOG.md` (drafter phase notes, drop routes, substitution)
- Grading packet: `grading_packet.md` / `grading_packet.json`

## Branching

Per charter: (1) narrow + controls pass → full-corpus Atlas-4 (2 papers/sky, more bridges: backprop-era, transformers); the cost basis now exists. (2) The user's narrow/wide verdict at grading resolves ledger item 4 regardless.
