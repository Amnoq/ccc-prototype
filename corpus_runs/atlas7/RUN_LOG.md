# Atlas-7 run log

## 2026-10-07: corpus selected and verified (coordinator)
All 4 arXiv IDs verified by live search (title/abstract match, none guessed):
- AN1 analytic: 1708.05266 — Shu & Yin, "An explicit Gross-Zagier formula related to the Sylvester Conjecture" (v2). Proves 3-part of BSD for E_p, E_{3p^2} via explicit GZ formula.
- AL1 algebraic: 2012.11771 — Sweeting, "Kolyvagin's Conjecture and patched Euler systems in anticyclotomic Iwasawa theory" (v3). Kolyvagin systems, Selmer rank, converse theorem.
- C1 computational: 0711.3774 — Fisher, 6/12-descent; Stein-Watkins database curves have rank >= BSD prediction.
- C2 computational: 2003.00077 — Elkies & Klagsbrun, new rank records with rational torsion (rank 20).
Positive controls: S1 = AL1<->AN1 (AL1 explicitly builds on Gross-Zagier); S2 = C2<->C1 (rank-computation lineage).
Manifest: manifest.json. Drafter brief: DRAFTER_BRIEF_A7.md.

## 2026-10-07: drafters dispatched
4 blind drafter subagents spawned (one per paper), each with paper assignment + source URL + blind discipline. Awaiting completions.

## 2026-10-08 ~01:34 UTC — Drafter 4/4 (c1, Fisher 6/12-descent) complete; validated 100%
- 7 chunk files (c1_p1..p7), 119 concepts / 119 anchors / 95 edges / 2 loops / 22 strands.
- Structural validation PASSED: unique concept ids, 1:1 concept↔anchor coverage, all edges/loops/strands resolve to concept ids, key set exactly {anchors,concepts,edges,loops,strands}.
- Epistemic profile: statuses exact 107 / computationally_verified 10 / heuristic 2; kinds claim 72, definition 22, result 12, method 11, question 2.
- words_out (file bytes/word): ~4,598; words_in ~12,010 est. Cost accounting at merge.
- Fetch route: ar5iv HTML, first try. No chunks dropped.

## 2026-10-08 ~01:35 UTC — Drafter 3/4 (c2, Elkies & Klagsbrun rank records) complete; validated 100%
- 4 chunk files (c2_p1..p4), 54 concepts / 54 anchors / 47 edges / 3 loops / 8 strands.
- Structural validation PASSED (same checks as c1).
- Epistemic profile: statuses exact 19 / computationally_verified 19 / heuristic 14 / conjectural 1 / killed 1; kinds result 23, method 12, claim 13, question 3, definition 2, conjecture 1.
- NOTE: one internal 'contradicts' edge (paper-stated: Kihara Z/6Z surface killed by negative evidence) — paper's own verdict, not a merge contradiction; recorded for the report's honesty check.
- words: 6884 in / 2459 out (drafter-counted).
- Fetch route: ar5iv HTML, first try. No chunks dropped.

## 2026-10-08 ~01:36 UTC — Drafter 2/4 (an1, Shu–Yin explicit GZ formula) complete; validated 100%
- 12 chunk files (an1_p1..p12; p12 = references-only, 0 concepts), 80 concepts / 80 anchors / 60 edges / 1 loop / 23 strands.
- Structural validation PASSED. Two chunks were self-repaired by the drafter (truncated + re-closed after JSON break; all strands verified intact; drafter's own handoff note).
- Epistemic profile: statuses exact 78 / conjectural 1 (Sylvester conjecture itself) / heuristic 1; kinds result 44, definition 19, method 13, claim 3, conjecture 1.
- Loop: l=2 part of BSD for E_p unaddressed by paper (paper-stated); 3-part closed.
- Chunk-quality notes: two xymatrix diagrams unreadable (extracted from prose; not reconstructed); eq (7.11) minor rendering noise, legible.
- Fetch route: ar5iv HTML, first try. No chunks dropped.

## 2026-10-08 ~01:38 UTC — Drafter 1/4 (al1, Sweeting Kolyvagin/patches Euler systems) complete; validated 100%
- 16 chunk files (al1_p1..p16), 121 concepts / 121 anchors / 87 edges / 2 loops / 33 strands.
- Structural validation PASSED. One schema slip (stray 'kind' key in two anchors) caught+fixed by drafter pre-handoff.
- Epistemic profile: statuses exact 105 / conjectural 16; kinds result 60, definition 47, claim 7, method 4, question 2, conjecture 1.
- Loops: full anticyclotomic MC (inert/non-ordinary p) unknown in full generality; only one direction of Kato's MC. Paper-stated gaps.
- Fetch route: ar5iv HTML, first try. No chunks dropped.

## Corpus extraction COMPLETE: 4/4 papers, 354 concepts total
| paper | sky | chunks | concepts | anchors | edges | loops | strands | words_in | words_out |
|---|---|---|---|---|---|---|---|---|---|
| an1 | analytic | 12 | 80 | 80 | 60 | 1 | 23 | ~22,500 est | 4,699 |
| al1 | algebraic | 16 | 121 | 121 | 87 | 2 | 33 | ~35,360 est | ~5,961 |
| c1 | computational | 7 | 119 | 119 | 95 | 2 | 22 | ~12,010 est | ~4,598 |
| c2 | computational | 4 | 54 | 54 | 47 | 3 | 8 | 6,884 | 2,459 |
| total |  | 39 | 374 | 374 | 289 | 8 | 86 | ~76,754 | ~17,717 |

## 2026-10-08 ~02:10 UTC — Pass 1 + Pass 2 + illustration + report COMPLETE
- Pass 1: exact-dup scan found 0 duplicate labels within sky; one reviewed merge (A7-15: c1 Stein-Watkins restatement p1<->p7). atlas7_merged.json: 373 live nodes, 289 edges.
- Pass 2: 872 mechanical cross-sky candidates + semantic review; 15 adjudications recorded in atlas7_adjudications.json: 9 split_link, 1 merge, 3 rejected, 1 missed (A7-14).
- Controls: S1 RESOLVED (A7-01/02/03 split_links), S2 RESOLVED (A7-12 split_link). False merges 0, contradictions 0 cross-sky.
- Illustration: build_html7.py -> atlas7_money.html + 3 per-sky views (bridge-counterpart ghosts, adj_id gold labels, role-difference legend, clickable loops). All views verified by JSON extraction.
- Grading packet: GRADING_PACKET.md (20 sampled triples + all 15 adjudications).
- Report: ATLAS7_REPORT.md (verdict first).
- Cost: extraction ~78.7k words in (ESTIMATE) / 15.8k out (exact); ~102k/20.5k tokens at 1.3x.

## 2026-10-08 ~02:16 UTC — Correction: adjudication totals field
- The Pass 2 line above and the report's metric table said "3 rejected," but the
  item-level records contain FOUR rejections (A7-06, A7-08, A7-10, A7-13 — BSD
  invoked in four different roles, rejected as a link everywhere). Totals now
  corrected in atlas7_adjudications.json ("rejected": 3 -> 4) and ATLAS7_REPORT.md
  to match the records. Original lines kept above as written; this entry is the
  correction on the record. Grading packet unaffected — all 15 adjudications were
  always carried item-by-item (20 sampled triples + all 15 adjudications).
