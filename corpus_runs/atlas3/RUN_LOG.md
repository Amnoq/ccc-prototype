# Atlas-3 run log

## 2026-10-07: coordinator launched
Charter: ATLAS3_CHARTER.md. Pipeline: verify corpus -> fetch/chunk ->
blind R4 extraction fan-out -> merge (within-sky P1, cross-sky P2
reviewed adjudication) -> illustrate -> report + grading packet.
Token accounting per phase (words in/out; tokens = 1.3x ESTIMATE).

## 2026-10-07: corpus verified (all 5 retrievable, no drops)
All arXiv IDs verified by live ar5iv fetch (clean primary HTML text):
- A1 Harris 2501.17197 (375 lines, modular representation theory)
- A2 Liu-Ren 2309.02372 (1266 lines, Gorenstein homological algebra) — coordinator-selected
- G1 Perelman math/0211159 (2867 lines, Ricci flow entropy)
- G2 Chu-Li-Wang 2601.01736 (4227 lines, min-max minimal surfaces) — coordinator-selected
- B1 Frenkel hep-th/0512172 (12296 lines, Langlands lectures)
BK2011 rule not triggered. Purest-skies design held: algebraic geometry excluded.

## 2026-10-07: extraction fan-out (9 blind drafters)
Design change from charter (recorded): drafters fetch their own chunk
text via browser.open (assigned URL + line ranges) instead of reading
coordinator-transcribed files — primary text fidelity, stronger blind
discipline, no transcription corruption. Brief: DRAFTER_BRIEF_A3.md.
Chunks (prefix samples, ~2.5k+ words): harris_p1 (0-375, whole paper),
liuren_p1/p2 (0-650/650-1266), perelman_p1/p2 (0-950/950-1900),
chuliwang_p1/p2 (0-700/700-1400), frenkel_p1/p2 (0-1200/1200-2400).
Merge script: merge_atlas3.py (3 skies, within-sky P1, cross-sky
candidates for reviewed P2). Illustration: build_html3.py (Atlas-2
render-time patches reused verbatim).

## 2026-10-07: first extraction in (frenkel_p1, bridge)
11 concepts / 11 anchors / 11 edges / 2 loops / 4 strands; words_in ~9200
(drafter estimate). Content: Langlands duality, dual group ^L G,
Witten/Kapustin-Witten scenario, critical-level CFT + Beilinson-Drinfeld,
Part I Galois/adeles/ACFT. Calibration honest: cited-without-proof ->
conjectural-from-this-chunk; only Hecke-eigensheaf definition exact.

## 2026-10-07: 7/9 extractions in, merge smoke-tested on partial data
Valid: harris_p1, liuren_p2, perelman_p1, chuliwang_p1, chuliwang_p2,
frenkel_p1, frenkel_p2. Pending: liuren_p1, perelman_p2. (One transient
partial-write JSON error observed mid-run; file completed validly —
no repair needed.) Merge script runs clean on partial data; full merge
after all 9 land.

## 2026-10-07: 7/9 extractions complete (words_in = drafter estimates)
- frenkel_p1 (bridge): 11c/11a/11e/2l, ~9200w
- frenkel_p2 (bridge): 20c/20a/24e/1l, ~7400w
- perelman_p1 (geometry): 17c/17a/13e/2l, ~15200w
- chuliwang_p1 (geometry): 19c/19a/15e/1l, ~6900w
- chuliwang_p2 (geometry): 21c/21a/19e/0l, ~20000w
- harris_p1 (algebra): 20c/20a/24e/0l, ~3200w — includes a first-class
  KILLED anchor (Kuelshammer's objection: [2, Prop 2.7] false in generality)
- liuren_p2 (algebra): 17c/17a/13e/0l, ~6200w
Pending: liuren_p1, perelman_p2. Calibration discipline held across
reports (cited-without-proof -> conjectural-from-chunk; postponed proofs
-> conjectural with citation notes).

## 2026-10-07: adjudication, illustration, report, grading packet complete
Reviewed pass (write_links3.py): 5 records — 1 split_link (S1,
shares-discipline; WEAK PASS, semantic-only), 3 rejected (1 false
friend Galois/Galois-conjugates + 2 spurious token matches), 0 merged,
1 control void (S2 misseeded: geometric Langlands is complex-algebraic,
sky was differential), 0 contradictions, 0 false merges, 0 direct A<->G
links. Views built (build_html3.py): atlas3_algebra/geometry/bridge/
cross.html, JS valid; money view carries the single gold S1 link.
Deliverables: manifest.json, ATLAS3_REPORT.md (verdict first, honest
limits, cost table ~237k tokens ESTIMATE), grading_packet.md (12 triples
+ all 5 adjudications). Pilot's and Atlas-2's directories untouched.
