# Atlas-5 Report: the constellations around the Riemann Hypothesis

**Date:** 2026-10-07 · **Coordinator:** Atlas-5 (depth 1/2) · **Charter:** `ATLAS5_CHARTER.md`

## Verdict

The atlas machine drew three analytic skies around RH — computation (109 concepts), proportion (91), density (75) — and held them against the pilot's relational sky (read-only, 305 nodes). **Both positive controls resolved** (AF displaces PRZZ's 5/12; PT2021 subsumes Gourdon's 10¹³ — the method is not broken). **The analytic skies barely touch each other**: one genuine link (computation↔density, via explicit zero-density estimates); computation↔proportion and proportion↔density do not touch — they share only the topic of RH, not a referent. **The wall holds, with exactly one crack**: a single analytic↔relational link — Weil's explicit formula / Weil positivity, invoked by name on both sides (Alpöge–Furman as the analytic engine of the 2/3 bound, preprint; the pilot as a computed face-sum-native verification, exact). Everything else across the wall — GUE statistics, moments, mollifiers, formal-verification provenance — was rejected as shared framework or vocabulary, not shared referent. False merges: 0. Contradictions: 0. No papers dropped. RH remains a receipt, not the goal — and the receipt says the relational floor the pilot exhibits is, with one classical exception, invisible to the analytic literature it stands beneath.

## What was built

| Sky | Papers | Chunks | Concepts | Anchors | Edges | Loops | Preprint-tagged |
|---|---|---|---|---|---|---|---|
| Computation | Platt–Trudgian 2021 (refereed) + Gourdon 2004 (unpublished ms.) | 6 | 109 | 109 | 92+ | 6 | 0 |
| Proportion | PRZZ 2019 (refereed) + Alpöge–Furman 2026 (**preprint**) | 4 | 91 | 91 | 79+ | 2 | 42 (AF files) |
| Density | Guth–Maynard 2024 (refereed) + Chourasiya–Simonič 2025 (**preprint**) | 4 | 75 | 75 | 71+ | 1 | 43 (CS files) |
| Relational | pilot `atlas_graph.json` (read-only, unmodified) | — | 305 nodes | — | — | — | — |
| **Total** | 6 | 14 | **275** | 275 | — | 9 | 85 |

All 6 paper IDs verified by live search/retrieval before drafting (none guessed); one brief guess (arXiv:2106.06027 for PT2021) was caught and corrected to arXiv:2004.09765. Provenance per paper in `manifest.json`. **Gap-fill:** the first pass missed Gourdon §2 (lines ~700–2278, the Odlyzko–Schönhage/Greengard–Rokhlin implementation and band-limited interpolation — the algorithmic core); the p1 drafter's handoff exposed the hole and 3 fill-in drafters closed it under the same blind discipline. Notably, the §2 method nodes generated **zero** cross-sky candidates — the algorithmic core is the most isolated part of the map.

## Sky↔sky results (the pre-registered question)

| Pair | Mechanical candidates | Adjudicated | Verdict |
|---|---|---|---|
| computation ↔ proportion | 37 | 0 links | **no touch** — shared RH theme, no shared referent (rejected) |
| proportion ↔ density | 12 | 0 links | **no touch** — technique class / shared subject / citation (rejected) |
| computation ↔ density | 4 | **1 split_link** | **touch** — explicit N(σ,T) zero-density estimates (shares-object) |
| computation ↔ relational | 100 | 0 links | no touch — GUE rejected (framework, not referent); rest generic |
| proportion ↔ relational | 180 | **1 split_link** | **one touch** — Weil explicit formula / Weil positivity (shares-classical-object) |
| density ↔ relational | 29 | 0 links | no touch |

**Link density** (adjudicated links per possible sky pair, Atlas-2/3/4 units): analytic↔analytic 1/3 pairs touch; analytic↔relational 1/3 skies touch. The wall's measure: 1 link across 309 candidates (362 mechanical, 309 involving the analytic–relational wall after the re-merge).

**Positive controls:** PC1 (AF record-context ↔ PRZZ 5/12 theorem, *displaces-record*) RESOLVED; PC2 (PT2021 Thm 1 ↔ Gourdon 10¹³ verification, *extends-record*) RESOLVED. Both are split_links (link, not merge — different papers, different epistemic roles). Method not failed.

**False merges:** 0 (bar held — no within-sky merges were even proposed; all drafters used distinct labels). **Contradictions surfaced:** 0.

## The one crack in the wall (read carefully)

`prp:weil-s-explicit-formula-hermitian-form-w-f-g-sum` (conjectural, **preprint**) ↔ `rel:node10a` (exact): both invoke **Weil's explicit formula / Weil positivity by name** — AF as the Hermitian form whose positivity drives the 2/3 bound (cited to [Wei52, Bom00], not proved there); the pilot as the Guinand–Weil formula computed against the sieve (zero-vs-prime side verified to 2e-16, "positivity is face-sum-native"). Same named classical referent, different constructions, different epistemic status — hence split_link, not merge. This is a genuine touch, and it is thin: one classical formula, two different uses. It qualifies the wall; it does not breach it.

Deliberately **not** linked, though tempting: GUE (Gourdon's zero-spacing law vs the pilot's GUE-like pair hopping) — a universality class is a framework, not a referent; linking it would have been the inflation the wall test exists to prevent. The quantitative kinship is real and is recorded in the rejection reason.

## Honest limits

1. **No drops, but one fragile source.** Gourdon 2004 is an unpublished author's-site manuscript (not refereed). All routes to it worked (author's PDF via browser.open); it is labeled exactly as what it is. No BK2011 drop was needed.
2. **Two preprints in the corpus.** Alpöge–Furman (67.25%) and Chourasiya–Simonič carry `preprint: true` on all 85 of their concepts; the label propagated through merge into the graphs and HTML badges. Nothing was upgraded.
3. **Garbling tax.** The Gourdon fetch lost superscripts (all 10¹³ rendered as 1013); the drafter reconstructed exponents from context and flagged the uncertainty. A handful of values (e.g. p(0,u) Taylor coefficients) were summarized, not transcribed. Major numbers are recorded in anchor notes.
4. **Extraction is chunk-bound.** Drafters saw ~2.5k-word windows; cross-chunk context within a paper was not available to them. Within-sky merge found almost nothing to merge (1–2 subjects per sky) — concepts may be more fragmented than the papers warrant. Over-merge remains worse than under-merge, so this stands. (The §2 gap — found via the p1 drafter's own handoff note, filled by 3 more drafters — is the method catching its own coverage error; the re-merge changed no adjudication.)
5. **Adjudication coverage.** 353 mechanical candidates → 15 written records (4 split, 11 representative rejections) + bulk rejection of ~340 generic 3-token overlaps. The bulk rejections were inspected by pair-type, not one by one; a missed thin link in the long tail is possible but unlikely to change the verdict (the strong candidates were all reviewed individually, plus full semantic label review per sky).
6. **The wall test is asymmetric.** The pilot graph (305 nodes, the user's own program) was read-only and much larger than any analytic sky; candidate counts analytic↔relational are inflated by its size. The adjudication standard (shared referent, not shared theme) was applied identically on both sides.
7. **Coordinator adjudication.** Pass 2 was done by the coordinator, not a separate blind adjudicator. The positive controls were pre-registered precisely to check this step — both resolved, which is evidence the step worked, not proof it is unbiased.

## Cost table (ESTIMATE unless noted)

| Phase | Words in | Words out | Tokens @1.3× (ESTIMATE) |
|---|---|---|---|
| Retrieval (6 papers, manifests) | — | — | unmetered (search + fetch) |
| Extraction (14 drafters) | ~46,400 | ~29,000 (reported) | ~98,000 |
| Merge + adjudication + HTML (coordinator) | — | — | unmetered |
| **Total metered** | **~46,400** | **~29,000** | **~98,000** |

~2.6 tokens per word all-in (in+out). The §2 gap-fill added 3 drafters (~18.4k words in, ~1.8k out — one reporter's in-count looked anomalous-high and is included as stated). **Extrapolation:** a 10× corpus (~140 chunks) would cost roughly 1M tokens (ESTIMATE) at current drafter verbosity. The dominant cost is drafter output, not input — tighter output schemas would cut it ~2× (measured JSON artifacts were only ~12k words vs ~29k reported output; the rest was drafter working).

## Files

- `manifest.json` — consolidated provenance per paper (all IDs verified, no drops)
- `chunks/` — per-sky manifests; `extractions/` — 11 validated extraction JSONs (239 concepts)
- `merge_atlas5.py`, `graphs/` — per-sky graphs + `combined_graph.json` + `candidates.json`
- `cross_sky_links.json` — **all adjudications** (4 split_links, 11 representative rejections, bulk note)
- `build_html5.py`, `atlas5_{computation,proportion,density,relational,cross}.html` — per-sky + cross views
- `atlas5_money.png` — static money view (8 nodes, 4 gold links)
- `ATLAS5_REPORT.md` — this file · `RUN_LOG.md` — run ledger
- **Grading packet:** `grading_packet.md` — 12 sampled concept/paper-record/status triples + all 15 adjudication records rendered for review

The pilot's and Atlas-2/3/4 directories were not modified.
