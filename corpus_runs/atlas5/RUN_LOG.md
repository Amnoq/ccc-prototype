# Atlas-5 run log

## 2026-10-07: chartered + launched
Charter: ATLAS5_CHARTER.md. Question: draw the RH constellations
(computation / proportion / density analytic skies + pilot relational
sky, read-only) — a receipt and proof of concept; RH remains a receipt,
not the goal.

## 2026-10-07: coordinator setup
- Read ATLAS5_CHARTER.md (complete spec).
- Adapted merge_atlas4.py -> merge_atlas5.py: skies
  computation/proportion/density (prefixes cmp/prp/den), pilot
  relational sky loaded READ-ONLY from ../../atlas/atlas_graph.json
  (namespaced rel:), preprint flag propagation (extraction-level
  "preprint": true -> every facet + node entry; never upgraded).
- Wrote DRAFTER_BRIEF.md (atlas5 paths; blind discipline incl. the
  pilot; preprint discipline for the Alpöge–Furman chunk only).
- Wrote build_html5.py (Atlas-2/3/4 render technique: galaxy layout,
  edges on, gold cross-links, clickable loop-constellations; preprint
  badge via status_note; relational sky read-only conversion with
  pilot loop resolution via (chunk, ref)).
- Verified all render patch targets against atlas_template.html.
- Spawned 3 retrieval subagents (computation / proportion / density),
  each: verify 2 paper IDs by live search, fetch clean primary text
  (ar5iv preferred), chunk ~2.5k words to atlas5/chunks/, provenance
  to <sky>_manifest.json, BK2011 drops recorded. Blind per sky.

## 2026-10-07: proportion retrieval landed; protocol correction
- Proportion sky secured: arXiv:2608.13637v2 (Alpöge–Furman, PREPRINT
  confirmed: submitted 13 Aug 2026, rev. 19 Aug 2026, no journal ref)
  + arXiv:1802.10521v3 (PRZZ, refereed, Res. Math. Sci. 7 (2020)).
  Lineage confirmed: AF abstract explicitly displaces PRZZ's 5/12
  and Wu's 0.6603 — the positive control is documented.
- DEVIATION CORRECTED: the retrieval agent wrote paraphrase-summaries
  to disk (copyright caution: license unconfirmed, declined full-text
  transcription). Paraphrases are secondary summaries — forbidden as
  substitutes by the charter — so the four chunk files were DELETED
  (manifest prop_manifest.json preserved as the record; source URLs
  retained: https://ar5iv.org/html/2608.13637 and /1802.10521).
- Adopted the Atlas-3 precedent: drafters fetch primary text directly
  via browser.open on verified ar5iv URLs (assigned line ranges),
  stronger blind discipline and primary-text fidelity, nothing
  transcribed to disk. DRAFTER_BRIEF.md updated accordingly.
- Redirect sent to computation + density retrieval agents: verify +
  provenance + ar5iv URL confirmation only; no transcription, no
  paraphrases; manifests only.

## 2026-10-07: computation retrieval landed (partial); same correction
- Computation sky: arXiv:2004.09765 (Platt–Trudgian 2021 — ID verified;
  my 2106.06027 guess was wrong) + Gourdon 2004 ("The 10^13 first zeros",
  author's site numbers.computation.free.fr, no arXiv ID).
- The agent wrote VERBATIM transcriptions to disk before the redirect
  arrived. Deleted per Atlas-2 D2 (no full text kept on disk; license
  discipline). Manifest comp_manifest.json retained (provenance + URLs).
- Drafters will fetch primary text directly via browser.open on the
  verified URLs. Redirect already sent to this agent mid-run.

## 2026-10-07: density retrieval landed; drafters fanned out
- Density sky: arXiv:2405.20552 (Guth–Maynard, refereed/Annals —
  brief's guess verified independently) + arXiv:2507.15184
  (Chourasiya–Simonič, PREPRINT). Lineage: CS cites GM as the
  σ≥0.7 record; GM improves Huxley/Ingham. No drops. Manifest only.
  Caveat: ar5iv abstract vs arXiv v2 abstract log-exponent mismatch
  recorded for drafters.
- 8 drafter subagents spawned (prop ×4, dens ×4), each: brief-first,
  one ar5iv URL + line range (~2.5k words), blind per sky, no disk
  writes of source text, preprint flags on AF + CS. Outputs to
  atlas5/extractions/<chunkid>.json.
- Computation retrieval still running under redirect; its 4 drafters
  spawn when its final manifest lands.

## 2026-10-07: computation manifest final; all drafters out
- Computation manifest final: PT2021 = 392 lines/~2k words (whole paper
  assigned to one drafter); Gourdon = 3578 lines/~19k words, sections
  mapped (history table L53-129; verification §3 L2278-2712).
  Gourdon URL is a PDF via browser.open (works; superscripts lost —
  drafters warned). No drops.
- 3 computation drafters spawned (PT full-paper; Gourdon L0-700 for the
  lineage/history table; Gourdon L2278-3000 for the §3 verification).
- 11 drafters total now running (prop 4, dens 4, comp 3), all blind per
  sky, preprint flags on AF + CS. Next: merge on arrival.

## 2026-10-07: extractions landing (4/11)
- prop_alpogefurman_p2: 16 concepts, preprint flags correct throughout.
- dens_guthmaynard_p1: 19 concepts; drafter flagged calibration calls
  (c1 exact w/ proof outside range noted; cited results conjectural).
- Both validated: JSON parses, all refs resolve, preprint discipline
  correct. 7 drafters still running.

## 2026-10-07: extractions at 6/11 (111 concepts)
All 6 files validated: JSON parses, concept/edge refs resolve,
preprint flags correct (AF-p2, CS-p1, CS-p2 flagged; others clean).
Breakdown: dens_cs 43 concepts (2 files), dens_gm 32 (2 files),
prop_af 16 (1 file), prop_przz 20 (1 file). 5 drafters still running
(prop_af_p1, prop_przz_p2, comp ×3).

## 2026-10-07: two more handoffs (6/11 files on disk)
- prop_przz_p1: 20 concepts. Notable: Feng's original θ_F=1/2−ε
  recorded as a KILLED claim (gap found in [8,48,58,60]) — negative
  results captured as first-class. Ladder concepts (Selberg, Levinson,
  Conrey, BCH, Feng) correctly conjectural-from-chunk.
- dens_chourasiyasimonic_p2: 18 concepts, preprint flags correct.
- 6 files on disk (dens_cs ×2, dens_gm ×2, prop_af_p2, prop_przz_p1);
  5 drafters still running (prop_af_p1, prop_przz_p2, comp ×3).

## 2026-10-07: density sky complete (75 concepts)
- dens_guthmaynard_p2: 13 concepts (Lemmas 4.3–4.5, Prop 4.6/5.1/6.1/7.1,
  Heath-Brown cited → conjectural per calibration).
- dens_chourasiyasimonic_p1: 25 concepts, 1 loop; preprint flags
  correct; v2-abstract discrepancy recorded in anchor note.
- Density sky total: 75 concepts across 4 files, all validated.
- 5 drafters remain: prop_af_p1, prop_przz_p2, comp ×3.

## 2026-10-07: proportion sky complete (91 concepts)
- prop_przz_p2: 29 concepts. Full mollifier-history ladder documented
  (Levinson→Conrey→BCH→Feng→BCR→BCY→Farmer→Bettin–Gonek); c8 dual
  anchors (killed Feng θ_F=1/2 + exact [58] repair).
- prop_alpogefurman_p1: 26 concepts, preprint flags correct; Theorem
  A/B, (Z)(P)(L) method chain, sharpness, extensions all captured.
- Proportion sky total: 91 concepts across 4 files, all validated.
- 3 computation drafters remain.

## 2026-10-07: Platt–Trudgian extraction landed (17 concepts)
- comp_platttrudgian2021_p1: 17 concepts, 3 loops, clean. Lineage
  survey richly documented with merge-scoring numbers (Wedeniwski
  2.41e11, Gourdon 2.44e12, Platt 2017 3.06e10, Franke 1e11) — the
  computation positive-control material is in place (PT2021 explicitly
  extending Gourdon's record).
- 2 Gourdon drafters remain.

## 2026-10-07: Gourdon §3 extraction landed (30 concepts)
- comp_gourdon2004_p2: 30 concepts (Gram points/blocks, Turing's
  method, 320,624,341 Rosser violations, GUE stats). Drafter worked
  around superscript-loss garbling; strict range discipline kept.
- 1 drafter remains: comp_gourdon2004_p1 (history table range).

## 2026-10-07: all extractions in; merge run
- 11/11 files, 239 concepts (comp 73, dens 75, prop 91). All validated.
- merge_atlas5.py executed (see output above).

## 2026-10-07: reviewed adjudication complete (Pass 2)
- 353 mechanical candidates reviewed; 15 records written to
  cross_sky_links.json: 4 split_links (2 positive controls + 2
  cross-sky), 11 representative rejections; ~340 generic
  token-overlap candidates rejected in bulk (no shared referent).
- Controls: PC1 (AF displaces PRZZ 5/12) RESOLVED; PC2 (PT2021
  subsumes Gourdon 10^13) RESOLVED. Method not failed.
- Cross-sky split_links: comp<->density (explicit N(sigma,T)
  estimates, shares-object); proportion<->relational (Weil explicit
  formula/positivity, shares-classical-object — the single wall
  touch). GUE rejected (framework, not referent). No merges (bar 0
  held); 0 contradictions surfaced.

## 2026-10-07: coverage gap found and being filled
- The p1 drafter's handoff revealed Gourdon §2 (lines ~700–2278:
  Odlyzko–Schoenhage/Greengard–Rokhlin implementation, band-limited
  interpolation — the algorithmic core) was never assigned to any
  drafter. Coordination hole in the chunk plan; the drafter assumed
  "another drafter's range" that did not exist.
- Dispatched 3 fill-in drafters (p3: 700–1230, p4: 1230–1760,
  p5: 1760–2278), same brief and blind discipline. On landing:
  validate, re-merge, review new candidates, rebuild HTML, amend
  report. Method caught its own gap via the paper trail.

## 2026-10-07: §2 fill-in p5 landed (13 concepts)
- comp_gourdon2004_p5: interpolation formula (21), Prop 4,
  C_M/D_M/E_M/F_M table, Z(t) fallback, §3 transition. Drafter
  deliberately under-graded the §3 RH claim (sibling territory).
- 2 fill-in drafters remain: p3 (700–1230), p4 (1230–1760).

## 2026-10-07: §2 fill-in p4 landed (12 concepts)
- comp_gourdon2004_p4: GR error control/complexity, FFT
  multievaluation, Prop 3 band-limited interpolation. Drafter notes
  §2.4.2 (application to Z(t)) starts at line 1764 — covered by p5.
- 1 fill-in drafter remains: p3 (700–1230, GR for huge heights).

## 2026-10-07: §2 gap filled; re-merge complete; run closed
- All 3 fill-in drafters landed and validated: p3 (11 concepts, GR
  multievaluation), p4 (12, GR error control + Prop 3), p5 (13,
  interpolation formula + §3 transition). 14 files, 275 concepts.
- Re-merge: computation 111 occ / 2 subjects / 107 standalone /
  92 edges; candidates 362 (+9, all in tokens-3 tail). The §2 method
  nodes produced ZERO cross-sky candidates — the algorithmic core is
  the map's most isolated region.
- Adjudication unchanged: the 15 records stand; no new links, no new
  merges, no contradictions. Verdict unchanged.
- HTML views + money PNG rebuilt; grading packet re-sampled (12
  triples); ATLAS5_REPORT.md amended (§2 note, 275 concepts, revised
  cost ~98k tokens ESTIMATE).
- Run closed. Deliverables: manifest.json, chunks/, extractions/
  (14), merge_atlas5.py, graphs/, cross_sky_links.json,
  build_html5.py, 5 HTML views, atlas5_money.png, ATLAS5_REPORT.md,
  grading_packet.md, RUN_LOG.md. Pilot and Atlas-2/3/4 untouched.
