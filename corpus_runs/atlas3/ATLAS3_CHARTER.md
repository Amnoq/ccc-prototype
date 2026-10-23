# Atlas-3 Charter — the two-skies test (algebra vs geometry)

**Date:** 2026-10-07
**Status:** chartered; launched on the user's "Go."
**Parent:** Atlas-2 (corpus_runs/atlas2/ATLAS2_REPORT.md) — PASSED.
**Question under test:** the user's theorization (ledger item 3, outcome
class `pass`): mapped as two skies, algebra and geometry show a very
narrow link between their constellations, similarly to Atlas-2's
pilot↔foreign result (2 genuine merges, 10 split-and-links,
0 contradictions from 310 reviewed candidates).

## Why this is the next move

Atlas-2's verdict ("the machinery survives foreign literature") plus
the user's thesis ("the atlas exhibits the wall that resists proof of
RH") turned the atlas from a test into an instrument with a claim:
knowledge domains form perspective-dependent skies, and the links
between skies are narrow. That claim is now ledger-registered and
falsifiable. Atlas-3 is the first run that tests it on new material —
with the two honest gaps from Atlas-2 closed by design: (1) token
costs instrumented per phase, (2) the narrowness bar pre-registered
below (the user's word "similarly" operationalized in Atlas-2 units;
the narrow/wide verdict itself remains his at grading — the instrument
never inserts the answer).

## Triadic fork

1. **Claim:** the direct algebra↔geometry cross-linkage is narrow at
   Atlas-2-like density, and whatever links exist concentrate at the
   seeded bridges (below). The skies are disjoint the way Atlas-2's
   were.
2. **Polar opposite:** the skies interweave widely — substantial
   adjudicated cross-links OUTSIDE the seeded bridges. Algebraic
   geometry exists; if the link is wide, the prediction is falsified
   at pilot scale and the wide links themselves are the finding
   (map exactly where the skies touch).
3. **Null / controls:** (a) drafters are BLIND across skies —
   algebra drafters never see geometry text and vice versa; the
   bridge paper is drafted blind to both skies' extractions.
   (b) the seeded bridge↔sky links are the POSITIVE CONTROL: they
   MUST resolve if the method works. If even the known bridges
   fail to resolve, the verdict is method failure, not narrowness
   — recorded as an R&D spec, never as confirmation.
   (c) fabrication spot-checks against paper text; the user's
   grading packet is the verdict's final leg (as always).

## Corpus (pilot scale: 2 + 2 + 1)

Purest skies — algebraic geometry is excluded by design (it IS the
bridge; including it would rig the test). The coordinator verifies
every ID by search (never guesses), records provenance (source URL,
version) per chunk, and applies the BK2011 rule: unobtainable in
clean primary text → dropped and recorded, NEVER substituted with
a secondary summary.

- **Algebra A1:** Harris, arXiv:2501.17197 — finite group modular
  representation theory (pure algebra; ID verified 2026-10-07).
- **Algebra A2:** coordinator selects a second pure-algebra paper
  (group theory / ring theory / homological algebra), verifies,
  records.
- **Geometry G1:** Perelman, math/0211159 — Ricci flow entropy
  formula (differential geometry landmark; coordinator verifies).
- **Geometry G2:** coordinator selects a second pure-geometry
  paper (differential geometry / topology), verifies, records.
- **Bridge B1:** Frenkel, hep-th/0512172 — Lectures on the
  Langlands Program and Conformal Field Theory (the famous narrow
  bridge; coordinator verifies; if unobtainable, the next-best
  primary Langlands exposition, recorded).

## Seeded intersections (positive controls — must resolve)

- **S1:** B1's automorphic / Galois-representation content ↔
  the algebra sky (A1/A2).
- **S2:** B1's geometric-Langlands content ↔ the geometry sky
  (G1/G2).

## Protocol (mirrors Atlas-2, with its lessons built in)

1. **Fetch → text → chunk** (~2.5k words/chunk). Provenance per
   chunk. Dead routes recorded (BK2011: five exhausted routes
   before a drop).
2. **Extract:** one-shot R4 drafters, same schema as Atlas-2
   (see corpus_runs/atlas2/DRAFTER_BRIEF.md and the extraction
   JSON shape). Each drafter works in ONE sky only, blind to the
   others, in that literature's own vocabulary — no canonical
   cross-sky labels; the merge earns resolutions. 100%
   validation on arrival; mechanical repairs only, recorded.
3. **Merge:** adapt corpus_runs/atlas2/merge_atlas2.py
   (MERGE_PLAN.md rules: explicit alias map, no silent fuzzy
   matching, over-merge worse than under-merge, contradictions
   surfaced never adjudicated):
   - Pass 1: merge WITHIN each sky.
   - Pass 2: cross-sky adjudication algebra↔geometry (the
     direct test) AND bridge↔each-sky (the positive controls).
     Every candidate recorded as resolved / split (reason) /
     missed; reviewed pass, not automatic.
4. **Illustrate:** reuse the Atlas-2 illustration stack
   (corpus_runs/atlas2/build_html.py — galaxy layout, gold
   bridges, clickable loop-constellations; adapt, don't
   reinvent): algebra sky + geometry sky + bridge as galaxies,
   money view with adjudicated cross-links.
5. **Grade + cost:** the user's grading packet (sampled
   concept/paper-quote/status triples, ALL adjudications, all
   splits, all contradictions); TOKEN ACCOUNTING PER PHASE —
   per-chunk word counts in/out, per-phase totals, tokens
   estimated at 1.3/word labeled ESTIMATE unless the runtime
   surfaces actuals (then actuals, labeled). Unit cost per 1k
   words and the honest extrapolation.

## Discriminating metrics (pre-registered)

- Direct A↔G adjudicated links: count and density per reviewed
  candidates, in Atlas-2 units (Atlas-2: 13 adjudications /
  310 candidates; 2 genuine merges).
- Concentration: what share of A↔G links fall on vs off the
  seeded bridges.
- Positive controls S1/S2: resolved (method works) or not
  (method R&D spec — narrowness NOT claimed).
- False merges among seeded pairs: pass bar 0.
- Contradictions flagged: vs Atlas-2's 0.
- User grading of the packet; HIS narrow/wide verdict resolves
  ledger item 3 (quantitative bar for "narrow" fixed here:
  Atlas-2-like density or below, links concentrated at seeds;
  he may set his own bar at grading — recorded either way).
- Cost: $/1k words per phase with the extrapolation arithmetic
  shown.

## Records

corpus_runs/atlas3/: this charter, manifest.json (provenance),
chunks/, extractions/, merge script (adapted), graphs, HTML
views, ATLAS3_REPORT.md (verdict first, honest limits, cost
table), grading packet. Atlas-2's and the pilot's directories
are read-only throughout.

## Branching identifiers

- **Why it ends here:** the narrow-link question is adjudicated
  as far as the pilot-scale instruments reach — counts measured,
  concentration mapped, controls checked, cost priced.
- **Its own chain:** (1) narrow + controls pass → full-corpus
  Atlas-3 (the field-scale design) with real cost numbers;
  (2) wide → the prediction falsified at pilot scale; the wide
  links mapped are the finding; ledger item 3 resolves 0;
  (3) controls fail → the failure taxonomy is the R&D spec;
  no narrowness claimed; (4) the grading packet goes to the
  user regardless — his verdict is the final leg.

## Correction 2026-10-07 (dictation)
The user meant ANALYTICS (analytic number theory), not algebra —
"algebra" was a dictation slip. His direction: finish this run as
chartered anyway. The algebra-vs-geometry pilot tests the same
structural prediction (two skies, narrow link); the
analytics-vs-geometry mapping is the natural follow-up run.
Ledger item 3's notes carry the correction; its claim and probabilities
are untouched.
