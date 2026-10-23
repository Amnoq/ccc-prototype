# Atlas-2 run log — coordinator decisions

## 2026-10-07: corpus verification
All arXiv IDs verified by search before fetching:
- 1102.5356 ✓ Sierra & Rodriguez-Laguna, "The H=xp model revisited and the Riemann zeros" (PRL 106, 200201)
- 2511.22755 ✓ Connes-Consani-Moscovici, "Zeta Spectral Triples"
- 2609.02882 ✓ Lamzouri, "A new proof that more than 2/3..." (v2, 8 Sep 2026)
- 2212.06867 ✓ Mossinghoff-Trudgian-Yang 2022, "Explicit zero-free regions..." (R=5.558691)
- 1410.3926 ✓ Mossinghoff-Trudgian 2015, "Nonnegative trigonometric polynomials..." (R=5.573412; Table 5 = F16 optimizer)
- 1807.06400 ✓ Deninger, "Dynamical systems for arithmetic schemes" (v4, 7 Feb 2024)
- 2301.11643 ✓ Deninger, "Primes, knots and periodic orbits" (expository; confirmed via secondary index)
- 2603.21490 ✓ Bellotti-Trudgian-Yang 2026, "Zero-free regions inspired by work of Heath-Brown" (1/(4.896 log t))

## 2026-10-07: BK substitution recorded
Charter named Berry-Keating 1999 "H=xp and the Riemann zeros" (Plenum chapter,
not freely available in clean text) → substituted with Berry & Keating 2011
"A compact hamiltonian with the same asymptotic mean spectral density as the
Riemann zeros" (J. Phys. A 44, 285203) — same authors, same xp program;
best obtainable primary text. (Would later be dropped — see below.)

## 2026-10-07: POLICY — no full-text local archival
The Lamzouri fetcher flagged a genuine policy conflict: saving full
copyrighted paper text to local chunk files without a verified permissive
license. Program-level decision: NO full paper text is ever written to
disk in Atlas-2. Pipeline restructured from fetch→chunk→extract to
fetch+extract in one agent: paper text is read in-transit via browser.open
and only extraction JSON (claims, labels, brief identifying phrases) is
persisted. This respects the fetcher's guardrail instead of overriding it.
Deliverables (atlas, report, grading packet) contain only brief quotes.
One chunk file written before the decision (sierra_p1.txt, 2972 words)
was deleted.

## 2026-10-07: coordinator mislabeling — corrected
The 8 spawn confirmations were misread; redirect messages went out with
wrong paper labels to two running agents:
- 19679791 is BTY2026 (was told "Sierra") → corrected to BTY2026, outputs bty2026_s<N>.json
- f4850175 is Deninger (was told "BTY2026") → corrected to Deninger, outputs deninger_s<N>.json
Both corrections delivered and acknowledged as pending; agents instructed
to rename any wrongly-named files. Correct final mapping:
d0c11d42=Sierra(done, chunk deleted, fresh extractor respawned),
4a5f7034=CCM, 6dd84b07=Lamzouri(done w/ blocker, fresh extractor respawned),
a65fad8d=MTY2022, 98f39eb8=MT2015, f4850175=Deninger, 35b0893f=BK2011,
19679791=BTY2026; fresh: 3723fa2a=Sierra, 5e0aab69=Lamzouri.

## 2026-10-07: BK2011 DROPPED (unobtainable in clean text)
The BK fetcher exhausted 5 routes: author's upload (Cloudflare bot-check
gate), IOP (paywall), archive.org (429 hard stop), reader proxy (auth
wall), web-wide search (no clean-text copy; paper never posted to arXiv).
Per the charter (drop unobtainable, never substitute secondary summaries)
and the agent's own flag (further substitution needs the user's call),
BK2011 is dropped from this run. Recovery path for the parent: a
live-browser fetch of the author's upload URL is the most promising
remaining route (same Cloudflare-check class the user solved himself on
2026-10-07). Seeded BK intersections (pilot 11a/11g/11h) do not run;
metrics adjust from 7 seeded intersections to 6.

## 2026-10-07: BTY filename collision — resolved
The pre-correction BTY-phase files written by f4850175 (which had told itself
"BTY2026") and the real BTY agent 19679791's files shared the bty2026_s<N>
namespace. Current on-disk bty2026_s1..s7.json (written ~20:17 CDT by
19679791) are verified genuine BTY2026 zero-free-regions extractions:
41 concepts matching the reported count, no Deninger contamination
(grep finds no "deninger" string), validate 100%. No rename/delete needed;
Deninger numbering (deninger_s1..s40) is intact and separate.

## 2026-10-07: Atlas-2 complete
All 7 obtained papers extracted (84 files, 521 concepts, 100% validated).
Final merge: 521 nodes, 383 edges, 16 loops, 0 flagged contradictions.
Cross-corpus: 310 candidates, 13 reviewed links (2 resolved, 10 split+link,
1 missed_correct, 0 false merges). chunks/ intentionally empty (policy D2:
no full-text archival). Deliverables: ATLAS2_REPORT.md, atlas2.html,
atlas2_cross.html (money view), cross_corpus_links.json, manifest.json,
grading_packet.json/.md. User grading pending.

## 2026-10-07: static PNG renders for phone viewing
The interactive HTML needs a real JS browser; the Android attachment
viewer does not run it (graph never draws, search input unfocusable).
Rendered static fallbacks with matplotlib/networkx (spring layout):
atlas2_overview.png (521 foreign nodes, status colors),
atlas2_crossview.png (826 nodes: gray pilot + colored foreign, 12 gold
cross-corpus links). Files verified visually.

## 2026-10-07: browser view rebuilt as a universe (user feedback)
User: the browser view showed "a bunch of floating dots" — no universe
of thought. Diagnosis: two causes. (1) The "all edges" toggle defaulted
OFF, so no relations were drawn at all — literally dots. (2) The layout
was one undifferentiated force cloud. Fix in build_html.py (template
untouched; pilot's built file unaffected): edges default ON; nodes carry
a cluster (foreign: paper from chunk prefix; money view: pilot = one
galaxy); cluster-aware init (galaxies on a ring, golden-spiral fill) +
galaxy gravity in tick(); cross-corpus bridges drawn gold. Verified: JS
syntax clean, layout sim holds galaxies distinct (mean radius ~150-180
vs 416 center spacing). Rebuilt atlas2.html and atlas2_cross.html.

## 2026-10-07: open loops -> clickable constellations (user: "lemmas like constellations")
Each open loop now resolves to its merged node id at build time
(foreign 16/16, pilot 29/45; unresolvable stay listed, not clickable).
Clicking a loop in the panel selects the node: its star lights up with
all its relations + the detail panel — the constellation around that
open question. Implemented as render-time patch on the shared template
(no template edit; pilot's built file untouched).

## 2026-10-07: his verdict on what the atlas shows (RH)
After the constellation build, his formulation (dictation-corrected: RH,
not "proof" in general): the two-skies-barely-touching IS the wall that
resists proof of RH. Not disagreement but disjointness — the analytic
sky's RH constellation (proportion/density axis: Sierra, CCM, Lamzouri's
67.25%) and the pilot's (Node 8 bridge, open by nature) share almost no
figures, so no proof-route can be drawn that both skies recognize. The
adjudication numbers are the evidence: 2 merges, 10 splits, 0
contradictions — not a debate, two different figures. Epistemic label:
his theorization, grounded in the adjudication data. Distinct from the
Node 11t prefactor wall (computational, resumable inventory) — this one
is paradigmatic. The atlas now has its thesis statement: it exhibits the
wall.

## 2026-10-07: his algebra-geometry theorization -> ledger item 3
His theorization: mapping algebra and geometry would show a very narrow
link between the two constellations, similarly to Atlas-2. He declined
my granular bar (<=5% / <=2 merges) — doesn't know the domains well
enough for that precision; noted this is the same observation-first
process he's used throughout (pattern from the data, then generalize).
Logged to prediction_ledger as item 3, outcome_class pass, in his
qualitative words; quantitative bar to be fixed at run-design time
before any run executes. Blind arm (coin flip); p_router pending, no AI
number stated (arm preserved).
