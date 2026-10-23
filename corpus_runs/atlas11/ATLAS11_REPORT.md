# Atlas-11 Report — analytics↔geometry, the real test

**Date:** 2026-10-08
**Run:** pilot scale (2 + 2 + 1 papers), Atlas-2 pipeline, blind drafters, pre-registered controls.

## Verdict: FAIL — the wall is the finding

Ledger item 5 (outcome class `pass`, p_ai_1 = 0.65, logged pre-extraction) resolves **0**.

The pre-registered bar (charter, fixed before extraction):

> PASS = adjudicated direct A↔G links exist at Atlas-2-like density or below, links concentrated at/near the bridge, BOTH controls resolved, 0 false merges. FAIL = 0 direct links (the wall — the wall is then the finding) OR linkage substantially above Atlas-2 density (the wide scenario — the wide map is then the finding) OR a control fails.

The FAIL clause's first condition fired: **0 adjudicated direct analytics↔geometry links** (0 merged / 0 split; 123 of 123 reviewed candidates marked missed). Both controls resolved, 0 false merges, 0 contradictions — the method worked; the skies simply do not touch at this scale. The wide-linkage polar opposite did **not** materialize either: no above-Atlas-2-density linkage anywhere. This is the clean wall, exactly as the charter anticipated it.

## Evidence

**Corpus** (all IDs search-verified 2026-10-08; Langlands-proper papers excluded from the skies by design):
- Analytics A1: Soundararajan, "Moments of the Riemann zeta-function" (math/0612106) — 2 chunks, 4,736 words
- Analytics A2: Michel–Venkatesh, "The subconvexity problem for GL₂" (0903.3591) — 15 chunks, 46,482 words
- Geometry G1: Mulase, "Hitchin integrable systems, deformations of spectral curves, and KP-type equations" (0801.0015, v2) — 6 chunks, 16,338 words
- Geometry G2: Tosteson, "Stability in the homology of Deligne-Mumford compactifications" (1801.03894, v1) — 3 chunks, 7,702 words
- Bridge B1: Frenkel, "Lectures on the Langlands Program and Conformal Field Theory" (hep-th/0512172) — 23 chunks, 71,775 words, re-drafted fresh

**Extraction:** 5 blind paper-specific drafters (Atlas-2 schema), 49 chunk JSONs, 456 concepts, blindness held on all five (each drafter saw only its paper's chunks + the brief). 100% schema-validated on arrival.

**Merge (Pass 1, mechanical):** analytics 207 nodes / 161 edges / 7 loops; geometry 98 nodes / 82 edges / 4 loops; bridge 148 nodes / 119 edges / 7 loops. 453 merged nodes, 362 edges (all endpoints verified), 18 loops, **0 contradictions**. Alias map: 3 merges, 6 deliberate non-merges (over-merge worse than under-merge).

**Candidates (mechanical, IDF-weighted token+bigram overlap):** 381 total — 123 analytics↔geometry (threshold ≥8.0, recall-favoring discovery arm), 151 bridge↔analytics (≥10.0, S1 arm), 107 bridge↔geometry (≥10.0, S2 arm).

**Adjudication (Pass 2, reviewed, every candidate):**

| Arm | Reviewed | merged | split | missed |
|---|---|---|---|---|
| direct analytics↔geometry | 123 | 0 | 0 | 123 |
| bridge↔analytics (S1) | 151 | 0 | 44 (42 S1-bearing) | 107 |
| bridge↔geometry (S2) | 107 | 1 | 32 (33 S2-bearing) | 74 |

**Metrics in Atlas-2 units** (baseline: 13 adjudications / 310 candidates / 2 genuine merges):
- Direct A↔G density: **0 / 123 = 0%** vs Atlas-2's 2/310 ≈ 0.65%. Below Atlas-2 density — but the bar required links to *exist*, and none did.
- Concentration: operationalized as share of direct links at/near the bridge (either endpoint also adjudicated-linked to the bridge sky, or Langlands-adjacent subject matter). Vacuous at 0/0 — and, structurally, **all 77 resolved cross-sky links sit on the seeded bridge**; none bypass it.
- Controls: **S1 RESOLVED** (42 split_links — cuspidal automorphic representations, the GL₂ subconvexity theorem, Langlands' correspondence ↔ M–V's Plancherel/spectral theorem, Hecke operators, Eisenstein analogs); **S2 RESOLVED** (1 merged_link — the Hitchin fibration as algebraically completely integrable system, stated identically on both sides — + 32 split_links: non-abelian Hodge, abelianization/spectral correspondence, opers).
- False merges: **0**. The one merged link (Hitchin fibration theorem, bri↔geo) is the same theorem stated identically; every near-miss was declined to split or missed.

**Strongest declined near-misses (direct arm)** — all homonyms, verified against the notes: "projection formula" (M–V's (4.22) L² spectral-projection norm identity vs Mulase's sheaf projection formula π\*(π\*L⊗–) — same name, different theorems); "spectral" (automorphic spectral decomposition vs the spectrum of the Higgs field; "ramified" likewise homonymous); "adjoint" (adjoint L-function vs formal adjoint of a pseudo-differential operator); "compactly supported" (test functions vs compactly supported cohomology — boilerplate). A generator-miss scan (periods/Hecke/Eisenstein/Whittaker, Lax/KP/Hitchin, moment/character/orthogonal/curve/integrable/singular/family) found no genuine pair outside the candidate list. The wall is not a recall artifact at this candidate depth.

## Reading

The triadic fork resolves cleanly:
1. **Claim** (narrow direct linkage at/below Atlas-2 density): **falsified at pilot scale** — not by wide linkage but by zero linkage. The router's "very narrow link, similarly to Atlas-2" does not appear between these skies.
2. **Polar opposite** (wide linkage — the Langlands program as a deep bridge): **did not materialize** in the direct arm. The bridge itself maps richly to both skies (77 resolved links), but the skies do not touch each other. Langlands is a genuine bridge *to* each field, not a conduit *between* them at this sampling.
3. **Null/controls**: clean — blind extraction, both seeded controls resolved (S2 correctly seeded this time, unlike Atlas-3), 0 false merges, 0 contradictions.

Structural note: Atlas-11's shape mirrors Atlas-4's (0 direct sky↔sky links there too; all cross-sky traffic through the bridge). Two independent runs now show the same topology: disjoint skies, bridge-mediated contact. The difference is the bar — Atlas-4's claim permitted bridge-only contact; Atlas-11's router prediction required direct links to exist.

## Honest limits

1. **Pilot scale.** 5 papers, 453 nodes. A wider corpus (Weil conjectures, Deligne, Drinfeld, more of the Langlands literature on both sides) could in principle surface direct links the pilot misses — that's a full-corpus design, not a rescue of this verdict.
2. **Mechanical recall.** The direct arm's candidate list was recall-favoring (threshold 8.0) and the reviewer probed homonym clusters explicitly, but cross-vocabulary recall remains the known weak point (Atlas-3/4 limit). The wall is measured at this candidate depth, not proved.
3. **Chunk garbling.** PDF/LaTeX extraction garbled inline math throughout (dropped braces, `6` for ≤, mangled fractions); prose claims were fully extractable, exact exponents in some theorem statements were reconstructed from context and carry lower confidence. No sections or tables lost.
4. **One merged link** (Hitchin fibration theorem, bri↔geo) is same-theorem-stated-twice — it carries the S2 control honestly, but it is identity, not discovery.
5. **The S1 control's 44 links are split_links, not merges** — same objects in different epistemic roles (Frenkel defines, M–V proves/counts). Correct per the over-merge-worse-than-under-merge rule.
6. **Tokens are ESTIMATES** (1.3× words). Coordinator/adjudication/illustration turns not instrumented. No dollar figure.

## Cost table (ESTIMATE — 1.3× words, arithmetic shown)

| Phase | Words in | Words out | Tokens est. (in/out) |
|---|---|---|---|
| Fetch (5 papers → 49 chunks) | 147,033 | 147,033 | ~191k / ~191k |
| Draft (49 blind extractions) | 147,033 | 15,412 | ~191k / ~20k |
| Merge (script + alias review) | 15,412 | 81,664 (graphs+candidates) | ~20k / ~106k |
| Adjudicate (381 reviewed) | — | 80 records + packet | not instrumented |
| Illustrate (4 HTML views) | — | 4 pages | not instrumented |
| **Totals (instrumented)** | **~309k** | **~244k** | **~402k / ~317k** |

Per-paper draft: A1 4,736→854 · A2 46,482→6,215 · G1 16,338→1,751 · G2 7,702→1,871 · B1 71,775→4,721. Extrapolation to a full-corpus Atlas-11 (say 20 papers, ~600k words): draft phase alone ≈ 780k tokens in — shown arithmetic, still estimates.

## Records

- `ATLAS11_CHARTER.md` (pre-registered bar, triadic fork, seeded S1/S2)
- `manifest.json`, `chunker.py`, `chunks/` (49), `extractions/` (49 blind JSONs)
- `merge_atlas11.py`, `alias_map.json`, `graphs/` (3 skies + combined), `candidates.json` (381)
- `adjud_arm_{direct,s1,s2}.json` (reviewer inputs), `adjud_records_{direct,s1,s2}.json` (per-candidate verdicts)
- `cross_sky_links.json` (80 records: 1 merged_link, 76 split_link, 3 grouped rejections)
- `grading_packet.md` / `grading_packet.json` (15 sampled triples, all 80 adjudications, 0 contradictions; router override available on request)
- Views: `atlas11_analytics.html`, `atlas11_geometry.html`, `atlas11_bridge.html`, `atlas11_cross.html` (money view; gold = 77 adjudicated bridge-arm links; direct arm empty)
- `RUN_LOG.md` (fetch/draft/merge notes)
- Ledger: item 5 rendered **0**; p_ai_1=0.65 → Brier **0.4225** (ai_1 cumulative n=2, BS=0.2563)

## Branching

Per charter: wall → item 5 resolves 0. The narrow-link claim for analytics↔geometry is falsified at pilot scale; the wide map did not materialize. The corrected S2 design worked (controls resolved, unlike Atlas-3's void). A full-corpus Atlas-11 remains designable — with the pilot's cost basis (draft ≈ 1.3 tokens/word in) and the corrected seeding — but it needs the router's word; this run's verdict stands on its own.

## Lemma-rerun follow-up (2026-10-08)

A discriminating test of the mapping hypothesis ("better mapping → more accurate predictions"), run on the router's word. The mechanical candidate generation was re-run with IDENTICAL scoring (IDF-weighted token+bigram overlap, same thresholds 8.0/10.0/10.0) on lemmatized node text (`lemma-db/form2lemma.json` applied to label+note before tokenization; script: `lemma_rerun.py`). Rerun total: 532 candidates; **195 new** (absent from the original 381): 99 analytics↔geometry, 55 bridge↔analytics, 41 bridge↔geometry. The original 381 verdicts stand untouched — only the 195 new were adjudicated, by the same reviewed protocol (records: `adjud_lemma_rerun.json`; per-arm reviewer files `adjud_lemma_rerun_arm_{direct,s1,s2}.json`).

**Verdicts:**

| Arm | New reviewed | merged | split | missed |
|---|---|---|---|---|
| direct analytics↔geometry | 99 | 0 | 1 | 98 |
| bridge↔analytics (S1) | 55 | 0 | 5 | 50 |
| bridge↔geometry (S2) | 41 | 0 | 9 | 32 |
| **Total** | **195** | **0** | **15** | **180** |

The single direct-arm split: "push-forward" — the Plancherel measure dμ_P as push-forward of dχ (analytics) vs Borel–Moore classes pushing forward from lower degree (geometry). Same abstract operation, different objects; related, not the same concept, not a link.

**Bottom line for the hypothesis:** zero new direct links resolved. The wall stands at the deeper candidate depth — **222 reviewed in the direct arm (123 + 99), 0 links**. "Better mapping → more links" is NOT confirmed by this test: recall rose (195 new candidates surfaced), precision-relevant links did not. The new candidates were noisier than the originals — lemmatization manufactured matches from meta-discourse ('cite' from 'cited', "n't" bigrams, 'control' from negations, 'push forward' as boilerplate) and re-surfaced the same homonym traps (character, spectral, twist, representation, quotient, vector) that the original pass declined.

The controls corroborated the method: 5 new S1 splits (all genuine Hecke substance — eigenvalues as Fourier coefficients, Hecke correspondences, Hecke eigensheaves vs analytic spectral identities) and 9 new S2 splits (all genuine Hitchin/moduli substance — dual Prym fibrations, spectral correspondence, SYZ-mirror pairs, KZB/WZW structures). S1 total now 47 split_links, S2 total 1 merged + 41 split. No new merged links anywhere; the false-merge bar (0) held.

This follow-up does not touch ledger item 5, which stays scored as rendered. What it changes: the report's honest limit #2 ("the wall is measured at this candidate depth, not proved") is now retired at the deeper depth — the wall was probed with a strictly more recall-favoring instrument and did not move.
