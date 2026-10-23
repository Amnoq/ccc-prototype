# Atlas-10 Theory-Sky Drafter Brief (blind extraction)

You are an extraction drafter for the Atlas-10 chess atlas, THEORY
sky (the chess literature: Capablanca's *Chess Fundamentals* and
Edward Lasker's *Chess Strategy*, both public-domain). Read this
whole brief, then do exactly what it says — one chunk, one JSON file.

## Assignment

- READ: the single chunk file assigned to you in your task message,
  e.g. `~/workspace/ccc-prototype/corpus_runs/atlas10/chunks/theory_capablanca_p1.txt`.
- READ NOTHING ELSE. In particular: never read any chunk whose name
  starts with `annot_` or `engine_`, never read anything under
  `~/workspace/prime-sieve-geometry/`, `engine_corpus/`, or any
  other atlas run directory. You are blind to the annotations and
  engine skies by design: the merge must earn every cross-sky
  resolution, and you must not insert one by hand.

## What to extract

The THEORY's own claims, in the AUTHOR'S OWN vocabulary (keep
their terms: "opposition", "passed pawn", "the initiative",
"relative value", etc.). Extract:
- named principles and rules (e.g., "advance the pawn that has no
  pawn opposing it", "act on the side where you have superior force")
- piece-value claims (relative values, bishop vs knight)
- endgame claims (which endings are won/drawn, the technique names)
- opening principles (centre control, development, king safety)
- named positions/methods the author teaches
- every claim the author makes about what WINS, DRAWS, or LOSES —
  these are the load-bearing ones; the exact position description
  goes in the anchor note verbatim (short).

## Output

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas10/extractions/<chunkid>.json`
with: `concepts` (list of {"id","kind","label"}; id `c1..cN`; kind ∈
{claim, definition, method, result, conjecture, question}),
`anchors` ({"concept_id","genre","note","status"}; status ∈ {exact,
computationally_verified, conjectural, heuristic, killed}; the
author's stated claims are `exact` as *stated-claims* — the label
records that the book says it, not that it is true; put the
book's own words briefly in the note), `edges` (a, b, rel ∈
{supports, depends_on, contradicts, refines, generalizes,
illustrates} — only relations the TEXT supports), `loops` (open
questions the text leaves open), `strands` (argumentative threads).
Validate with `python3 -c "import json; json.load(open(...))"`.

## Calibration

- Extract what the book SAYS, not what you know about chess.
  If Capablanca says something modern theory disputes, extract his
  claim faithfully — the adjudication handles truth later.
- The C1 control note: if your chunk contains the knight+bishop
  mate chapter (Capablanca ch. 15), capture the forced-mate claim
  as a concept with the fifty-move detail in the anchor note.
- Diagrams appear as [Illustration] placeholders — note the
  position is diagram-given, extract the surrounding claim anyway.

Your final report: chunk id, counts
(concepts/anchors/edges/loops/strands), and any chunk-quality
problems (truncation, garbled text).
