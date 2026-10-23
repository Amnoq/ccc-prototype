# Atlas-7 Report — mapping the skies around Birch–Swinnerton-Dyer

**Date:** 2026-10-08 · **Coordinator:** Atlas-7 (depth 1/2) · **Status:** COMPLETE

## Verdict

**The wall is real, and the crack is exactly the conjecture's own bridge.** The analytic sky (Shu–Yin explicit Gross–Zagier) and the algebraic sky (Sweeting Kolyvagin/patches Euler systems) touch five times — more contact than any Atlas-2..5 sky pair — but every touch runs through the single load-bearing bridge BSD itself names: Gross–Zagier + Kolyvagin converting Heegner-point nonvanishing into *rank = analytic order*. Everything else is disjoint: Selmer groups are computed three different ways for three different purposes, BSD is invoked in four different roles and rejected as a link everywhere (it is the subject, not a bridge), and the computational sky's descent machinery shares almost nothing with the Kolyvagin machinery — their philosophical kinship is a recorded **miss**, not a link. All 9 cross-sky links are **splits**, 0 are merges: the two sides share objects (the GZ formula, Heegner points, Selmer groups, the canonical height) but never the same *role* for them. A proof route would have to walk each split_link upgrading the cited role to a proved one — the map names the upgrades, same as Atlas-6's Weil bridge. The computational sky barely touches the theoretical skies (2 + 1 links): rank records and BSD-verification computations live on a different floor from the GZ/Kolyvagin core.

## Metric table (pre-registered)

| Metric | Value |
|---|---|
| Papers / skies | 4 papers, 3 skies (analytic 1, algebraic 1, computational 2) |
| Concepts extracted | 374 (an1 80 · al1 121 · c1 119 · c2 54) |
| Nodes after Pass 1 | 373 live (1 merge: A7-15, within-paper restatement) |
| Within-paper edges | 289 |
| Mechanical candidates | 872 cross-sky + 342 within-sky (reviewed selectively; semantic stream from the start) |
| Adjudicated links | 9 split_links · 1 merge · 4 rejected · 1 missed |
| Sky-pair density (Atlas-2..6 units: links per pair) | analytic↔algebraic **5** · analytic↔computational **2** · algebraic↔computational **1** |
| Rank↔L-value bridge anatomy | 9 links: GZ formula (A7-01, A7-02), Heegner points (A7-03), Selmer groups (A7-04, A7-07, A7-11), CM points (A7-05), canonical height (A7-09); **all split_link**, named role-differences in adjudication record |
| Control S1 (AL1↔AN1 Gross–Zagier lineage) | **RESOLVED** — 3 split_links; AL1 explicitly cites the GZ formula |
| Control S2 (C2↔C1 Fisher lineage) | **RESOLVED** — split_link; C2 cites Fisher's 2-power isogeny Selmer machinery |
| False merges | **0** (bar held; over-merge worse than under-merge) |
| Contradictions | **0** cross-sky; 2 paper-internal (c2 Kihara surface killed; c1 internal), preserved as extracted |
| Drops | **0** — all 4 papers fetched first-try via ar5iv HTML |

## The bridge anatomy (rank↔L-value)

The conjecture's claimed bridge — *non-trivial Heegner point → GZ formula → L′(1)≠0 → Kolyvagin → rank 1* — is the only place the skies interleave, and it interleaves as **splits**, each with a named role-difference:

1. **The GZ formula itself** (A7-01, A7-02): AN1 *proves* a new explicit GZ formula for E_p/E_{3p²}; AL1 *cites* the classical GZ formula as a black-box identification inside the p-converse theorem. Same theorem-type, opposite directions of travel.
2. **Heegner points** (A7-03): AN1 needs one non-torsion point R as seed; AL1 builds a whole Kolyvagin system of classes from Heegner points of varying conductor. One point vs a system.
3. **Selmer groups** (A7-04, A7-07, A7-11): three-way split — computed 3-Selmer dimensions to pin a BSD 3-part (analytic), abstract Selmer structures controlled by Kolyvagin systems toward the converse (algebraic), n-Selmer computed via descent to find points (computational).
4. **CM points** (A7-05): the Heegner cycle whose height GZ evaluates (analytic) vs construction material for cohomology classes (algebraic).
5. **Canonical height** (A7-09): computed through GZ as the bridge to L-values (analytic) vs regulator certifying generator independence (computational).

BSD itself links nothing: an1 proves instances of it, al1 states it as unused background, c1 tests its rank prediction, c2 uses it as search heuristic — four roles, shared name only (A7-06, A7-08, A7-10, A7-13 all rejected).

## Honest limits

- **Pilot scale:** 4 papers; analytic sky deliberately thin (1 paper) — a recorded caveat, not an oversight. A fuller analytic sky (e.g., a second BSD-analytic paper) could add or dissolve links.
- **No drops:** all four primary texts obtained first-try via ar5iv HTML. BK2011 never triggered.
- **Adjudication by coordinator**, not a separate blind adjudicator (same as Atlas-5/6); the pre-registered controls are the method check, and both resolved.
- **A7-14 is a recorded miss**, not a rejection: Kolyvagin's program is philosophically a descent on Selmer groups, but neither paper engages the other's machinery — the link is plausible in the literature and absent in these extractions.
- **Extraction fidelity notes:** an1 — two commutative diagrams unreadable in ar5iv (extracted from surrounding prose only); c1 — diagram visuals dropped, prose assertions captured; al1 — one schema slip caught and fixed by the drafter pre-handoff; two an1 chunks self-repaired by the drafter (verified intact). Coordinator did not re-verify the mathematics.
- **words_in are drafter estimates** (line-density), not byte counts — all token figures labeled ESTIMATE.

## Cost table (per phase, tokens at 1.3× words, ESTIMATE unless noted)

| Phase | Words in | Words out | Tokens in (est) | Tokens out (est) |
|---|---|---|---|---|
| Extraction an1 (12 chunks) | ~22,700 | 2,393 (exact) | ~29,500 | ~3,100 |
| Extraction al1 (16 chunks) | ~37,060 | 5,961 (exact) | ~48,200 | ~7,750 |
| Extraction c1 (7 chunks) | ~12,010 | 4,902 (exact) | ~15,600 | ~6,370 |
| Extraction c2 (4 chunks) | 6,884 | 2,511 (exact) | ~8,950 | ~3,260 |
| **Extraction total** | **~78,654** | **15,767** | **~102,250** | **~20,500** |
| Merge/adjudication (mechanical) | ~168,000 (candidate JSON) | 12 KB adjudications | ~219,000 | — |
| Merge/adjudication (reviewed) | selective read of top candidates + semantic keyword passes | — | not metered | — |

- **Extraction yield:** 15,767 / 78,654 ≈ **20%** (5:1 compression, labels+notes).
- **Cost per 1k words_in:** ≈ 1,300 tokens in + 260 tokens out (ESTIMATE).
- **Extrapolation:** a 10× corpus (≈40 papers) ≈ **1.0M tokens in / 200k tokens out** for extraction; mechanical candidate generation grows ~quadratically in concepts (~2.2M tokens at 10×) but reviewed adjudication cost grows with the number of *genuine* bridges, not candidates — the expensive part is bounded by the map, not the corpus.

## Deliverables

- `manifest.json` — paper provenance, controls, drops (empty)
- `chunks/` — (chunk texts; see manifest for per-chunk provenance)
- `extractions/` — 39 chunk JSON files (an1×12, al1×16, c1×7, c2×4), all schema-validated 100%
- `merge_atlas7.py`, `graphs/atlas7_raw.json`, `graphs/atlas7_merged.json`
- `candidates_algebraic-analytic.json`, `candidates_algebraic-computational.json`, `candidates_analytic-computational.json`, `pass1_review.json` — mechanical streams
- `atlas7_adjudications.json` — all 15 adjudications (verdict, seed, relation, role-difference, reason)
- `atlas7_money.html` — money view (all skies, 9 gold links, role-difference legend, clickable loops)
- `atlas7_analytic.html`, `atlas7_algebraic.html`, `atlas7_computational.html` — per-sky views with bridge-counterpart ghosts
- `build_html7.py` — illustration builder (adapts the Atlas-6 technique)
- `GRADING_PACKET.md` — 20 sampled concept/paper-quote/status triples + ALL 15 adjudications
- `RUN_LOG.md` — phase log with validation entries

## What this means for the wall thesis

Atlas-2's thesis (the user's): the wall is disjointness, not disagreement. Atlas-5 (RH): analytic skies barely touched; one crack (Weil). Atlas-7 (BSD): the analytic and algebraic skies touch **through exactly one classical bridge** — and it is the bridge the conjecture itself is built on. The map says: BSD's difficulty is not that its skies disagree, but that its one genuine bridge is traversed in opposite directions by the two sides — the analytic side *produces* explicit formulas, the algebraic side *consumes* cited ones — and the computational floor underneath shares almost nothing with either. The crack is real, named, and narrow; the upgrades a proof route would need are written on the split_links.
