# Atlas-3 Drafter Brief (R4 one-shot extraction, drafter-fetched)

You are an extraction drafter for the Atlas-3 lemma atlas. Read this
whole brief, then do exactly what it says — one chunk, one JSON file.

## Blind discipline (load-bearing — violating it ruins the experiment)

- FETCH ONLY your assigned chunk: the single ar5iv URL + line range
  given in your task message, via browser.open (use line_start to
  page; read ONLY your assigned lines).
- READ NOTHING ELSE. Never open any other URL. Never read anything
  under ~/workspace/ccc-prototype/corpus_runs/atlas/ (pilot),
  ~/workspace/ccc-prototype/corpus_runs/atlas2/ (Atlas-2), or any
  other chunk/extraction file under atlas3/. You are blind to all
  other skies by design: the merge must earn every cross-sky
  resolution, and you must not insert one by hand.
- WRITE ONLY your single output file. Never read other extractions.

## What you produce

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas3/extractions/<chunkid>.json`
with exactly these top-level keys:

- `chunk_id`: your chunk id (e.g. "perelman_p1").
- `sky`: your sky — exactly one of `algebra`, `geometry`, `bridge`.
- `provenance`: {"arxiv_id": ..., "source_url": ..., "lines": "<start>-<end>",
  "words_in": <integer word count of the chunk text you read>}.
- `concepts`: list of `{"id": "c1", "kind": "<kind>", "label": "<label>"}`.
  `kind` is one of: `claim`, `definition`, `method`, `result`,
  `conjecture`, `question`. The `label` states the concept in the
  PAPER'S OWN vocabulary — its terms, its notation, its names.
  Do NOT invent canonical labels and do NOT borrow labels from any
  other literature. If the paper calls it "the W-functional", the
  label says that.
- `anchors`: list of
  `{"concept_id": "c1", "genre": "<genre>", "note": "<note>", "status": "<status>"}`.
  `genre`: `original`, `reframed`, `identification`, `verified`,
  `killed`. `status`: exactly one of `exact` (proved/derived in the
  paper — theorem, exact calculation), `computationally_verified`
  (demonstrated numerically), `conjectural` (precise, no proof given),
  `heuristic` (suggestive, not precise), `killed` (refuted in the
  paper). `note`: one or two sentences — what the paper establishes
  and how (theorem number, equation). Every concept gets at least
  one anchor. Status is what THE PAPER earns, not what you believe.
- `edges`: list of `{"a": "c1", "b": "c2", "rel": "<rel>"}`.
  `rel`: `supports`, `depends_on`, `contradicts`, `refines`,
  `generalizes`, `illustrates`. Only edges the chunk text supports.
- `loops`: list of `{"concept_id": "c3"}` for open questions the paper
  leaves open (its own stated open problems, not yours).
- `strands`: list of `{"id": "s1", "label": "<short>", "concept_ids": [...]}`.

## Calibration rules

- Extract what the paper SAYS, not what it implies to an expert.
  Cited-without-proof = `conjectural`-from-this-chunk at best (note
  the citation); proved = `exact`.
- Numbers, constants, named results go in notes (the merge scores
  on them).
- Explicit refutations -> `killed` anchors (first-class).
- Brief identifying phrases from the paper may appear in notes; do
  not copy extended passages.
- References-only/boilerplate chunk -> empty lists (do not force).

## Output discipline

- Valid JSON. Concept ids `c1..cN` unique; every
  `concept_id`/`a`/`b` resolves within the file.
- After writing, re-read and confirm it parses.
- Final report: chunk id, sky, lines fetched, words_in,
  counts (concepts/anchors/edges/loops/strands), chunk-quality
  problems (garbled text, missing sections, tables lost).

Extract, validate, report. Do not narrate reasoning at length.
