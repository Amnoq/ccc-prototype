# Atlas-10 Report — the chess atlas

**Date:** 2026-10-08
**Status:** COMPLETE
**Question:** theory (the books) vs annotations (the grandmasters'
words) vs engine (executable ground truth) — walls or interweave?

## Verdict: INTERWEAVE where tested, WALLS where untested

The verdict is split by pair, and the split is the finding:

- **Annotations ↔ engine: INTERWEAVE.** The period annotators'
  judgments are directionally sound against Stockfish 17.1 at
  depth 20. Across 10 positionally-joined judgments in the two
  annotated games the engine analyzed, zero directional
  contradictions: every praised move ranks in the engine's top 3,
  no criticized move is the engine's top choice (K10-1, verified).
  The AlphaZero-expected cracks — things the engine knows that the
  annotators got wrong — did not materialize here. Where the
  annotator said "or resigning," the engine said mate in 8.
- **Theory ↔ engine: NARROW BRIDGES.** The only theory↔engine
  touches are the elementary mate rules (KBN within fifty moves,
  Q+K, R+K) — each a split_link with the same shape: the book
  teaches the bound, the engine exhibits the instance. Everything
  else in the theory sky (mobility doctrines, pawn structure,
  planning, piece values) has no engine counterpart in this run —
  not because it is wrong, but because the engine was never asked.
- **Theory ↔ annotations: MOSTLY WALLS.** 86 of 90 mechanical
  candidates were spurious token overlap. Four genuine
  split_links survive: doubled pawns (defect-to-manage vs asset),
  the gambit (used vs defined), the McCutcheon (asserted vs open
  question). The books and the annotators largely talk past each
  other — general doctrine vs game-specific judgment.

## Metric table

| Metric | Value |
|---|---|
| Concepts (post-merge) | 454 (theory 167 / annotations 263 / engine 24) |
| Extractions | 6 files, 462 concepts pre-merge |
| Merges | 9 reviewed (6 groups; 1 flagged weak: piece-value) |
| Contradictions | 0 |
| Adjudications | 93: 7 split_link · 86 rejected · 0 merge |
| theory↔annotations | 4 split / 83 rej · theory↔engine 3 split / 0 rej · annot↔engine 2* split / 3 rej |
| Controls | C1 RESOLVED · C2 RESOLVED (strengthened: mate-in-8) |
| Cracks | 2: 2 verified ✅ · 0 refuted · 0 undecidable |
| Drops | 0 (all three skies produced) |
| Cost | ~6 subagent extractions + ~40 min Stockfish 17.1 (326 positions, depth 20/24) |

\* A10-02 (C2) is the annotations↔engine control; K10-1 is the
crack built on the same join.

## The cracks

- **K10-1 (verified):** annotator–engine directional agreement —
  9/9 evaluative joins with zero contradictions, +1 historical
  note. The engine "knows" the agreement profile; the literature
  doesn't state it. Honest caveat: the directional comparison is
  exploratory (post-hoc), not pre-registered; the ranks and losses
  are pre-registered E1/E2 outputs.
- **K10-2 (verified):** engine divergence profiles per game
  (G1: 13/55, G2: 3/39, G3: 23/144, G4: 15/88 divergences; mean
  losses 20.09/16.62/2055.28/19.05cp) — structural facts about
  the corpus games that neither literature sky states.

## Controls

- **C1 (theory↔engine):** Capablanca ch. 15's KBN forced-mate
  claim → engine mate-in-2 (≤ 50 required). RESOLVED.
- **C2 (annotations↔engine):** Blue Book game 70's "this move, or
  resigning" at 25...f6 → engine mate-in-8. RESOLVED and
  strengthened.

## Honest limits

1. **Pilot scale:** 2 theory books, 1 annotation collection, 4
   games, 3 FENs. Nothing generalizes to "chess literature" or
   "grandmaster annotations" as wholes.
2. **The engine was asked narrow questions.** E1–E5 cover eval
   profiles, divergences, conversions, and deterioration
   structures. The theory sky's general doctrines (planning,
   mobility, pawn structure) were never put to the engine —
   the theory↔engine "wall" is untested territory, not a finding
   of disconnection.
3. **E4/E5 partial:** the endgame segment never began in 3 of 4
   games; zero forced-deterioration structures found (honest null).
4. **K10-1 is exploratory.** The directional rule was chosen after
   seeing the ranks. It re-runs deterministically, but it is not
   a pre-registered test.
5. **Single engine, single depth.** Stockfish 17.1 at depth 20/24.
   No second-engine corroboration; no time-odds sweep.
6. **The annot_p1 label repair** was mechanical (labels derived
   from the drafter's own anchor notes); original backed up as
   `extractions/annot_p1_raw.json`.
7. **Two runner bugs** caught by the method itself (multipv=1
   list shape; <3 legal moves PV count); both fixed, logged in
   RUN_LOG.md. One VM restart killed a background run mid-flight;
   no data lost (text extractions survived on disk).

## Adaptation grade: A−

The quantitative-sky pipeline (pre-registered procedures + blind
drafters + verify-against-executable) transferred cleanly from
Atlas-9's tape to a chess engine. The load-bearing gaps: (1) the
theory sky's general claims need engine-testable operationalizations
before theory↔engine can be more than mate rules; (2) node-id
stability must be designed in from the start (cid-keyed ids adopted
mid-run after a collision).

## Standing

Mapping run. The instrument draws; the decider decides.
