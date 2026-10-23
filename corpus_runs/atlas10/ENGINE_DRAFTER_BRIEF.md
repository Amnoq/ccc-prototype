# Atlas-10 Engine-Sky Drafter Brief (blind extraction)

You are an extraction drafter for the Atlas-10 chess atlas, ENGINE
sky (executable ground truth: Stockfish 17.1 analysis of fixed
games and positions). Read this whole brief, then
`~/workspace/ccc-prototype/corpus_runs/atlas10/ENGINE_PROCEDURES.md`
(the PRE-REGISTERED procedures — they are fixed; you do not modify
them), then do exactly what they say.

## Assignment

- RUN: `~/workspace/ccc-prototype/.venv/bin/python ~/workspace/ccc-prototype/corpus_runs/atlas10/run_engine_analysis.py`
  (writes `engine_raw.json`). NOTE: use the venv python — the system
  python3 does not have the chess library. If it fails, report the
  failure and stop — do not substitute, approximate, or invent
  analysis.
- READ: `engine_raw.json` and NOTHING ELSE. In particular: never
  read any chunk whose name starts with `theory_` or `annot_`,
  never read anything under `corpus/`, `~/workspace/prime-sieve-geometry/`,
  or any other atlas run directory. You are blind to the text
  skies by design. Your labels must be STRUCTURAL and NEUTRAL
  (see procedures: "eval-swing event", "played-move rank
  divergence", "forced-deterioration structure", "conversion
  failure"). NEVER use chess-literature words: no "blunder",
  "brilliant", "novelty", "zugzwang", "fortress", "winning",
  "lost" as labels.
- Your assigned scope is in your task message: either the four
  games (E1, E2, E4, E5) or the three FEN positions (E3) plus the
  two controls (C1, C2). Extract ONLY your scope.

## What to extract

From `engine_raw.json`, per the procedures: the eval-swing events
(E1), rank divergences (E2), outcome classes (E3), conversion
failures (E4), forced-deterioration structures (E5), and the control
readouts (C1: mate-in-N ≤ 50? C2: cp ≥ +300 or mate?). Every number
goes in the anchor note. Computed facts are
`computationally_verified`; the control verdicts are results.

## Output

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas10/extractions/engine_<id>.json`
with: `concepts` ({"id","kind","label"}; id `c1..cN`; kind ∈ {claim,
definition, method, result, conjecture, question}), `anchors`
({"concept_id","genre","note","status"}; status ∈ {exact,
computationally_verified, conjectural, heuristic, killed}),
`edges` (only relations the NUMBERS support), `loops` (e.g.,
procedures that could not run), `strands`. Validate with python3
json.load.

Your final report: engine id, counts
(concepts/anchors/edges/loops/strands), the C1/C2 readouts if in
your scope, positions actually processed, and any procedure that
could not run and why.
