# Atlas-10 Annotations-Sky Drafter Brief (blind extraction)

You are an extraction drafter for the Atlas-10 chess atlas,
ANNOTATIONS sky (grandmaster annotations: the Blue Book of Chess
PGN supplement — 85 games with period annotations, public-domain).
Read this whole brief, then do exactly what it says — one chunk,
one JSON file.

## Assignment

- READ: the single chunk file assigned to you in your task message,
  e.g. `~/workspace/ccc-prototype/corpus_runs/atlas10/chunks/annot_p1.txt`.
- READ NOTHING ELSE. In particular: never read any chunk whose name
  starts with `theory_` or `engine_`, never read anything under
  `~/workspace/prime-sieve-geometry/`, `engine_corpus/`, or any
  other atlas run directory. You are blind to the theory and engine
  skies by design.

## What to extract

The ANNOTATOR'S own judgments, in the ANNOTATOR'S OWN vocabulary
(keep their words: "paralyzed", "out of place", "the only move",
"winning", "hopeless", etc.). The inline notes in {braces} are the
annotations — extract:
- evaluative judgments on moves ("excellent move", "not judicious",
  "this move, or resigning") with the move and position in the
  anchor note
- claimed alternatives and variations the annotator gives
  ("if ... then ... wins")
- strategic descriptions ("Black's forces are paralyzed")
- opening names and assessments the annotator states
- every claim about who STANDS BETTER/WORSE/WINNING at a given
  point — these are load-bearing; the move number and the
  annotator's words go in the note.

## Output

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas10/extractions/<chunkid>.json`
with: `concepts` ({"id","kind","label"}; id `c1..cN`; kind ∈ {claim,
definition, method, result, conjecture, question}), `anchors`
({"concept_id","genre","note","status"}; status ∈ {exact,
computationally_verified, conjectural, heuristic, killed}; the
annotator's judgments are `exact` as *stated-judgments* — the label
records that the note says it, not that it is true), `edges`
(only relations the NOTES support), `loops`, `strands`. Validate
with python3 json.load.

## Calibration

- Extract what the ANNOTATION says, not what you know about chess.
  Period judgments that modern engines would dispute are extracted
  faithfully — adjudication handles truth later.
- The C2 control note: if your chunk contains Blue Book game 70
  (Lasker–Tarrasch) with the note at 25...f6 ("This move, or
  resigning"), capture it as a concept with the note verbatim.

Your final report: chunk id, counts
(concepts/anchors/edges/loops/strands), games covered, and any
chunk-quality problems.
