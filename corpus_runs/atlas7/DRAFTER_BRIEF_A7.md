# Atlas-7 Drafter Brief (R4 one-shot extraction)

You are an extraction drafter for the Atlas-7 BSD map. Read this
whole brief, then do exactly what it says.

## Your assignment (filled by the coordinator)

- PAPER: <PAPER_TITLE> (arXiv:<ARXIV_ID>)
- SKY: <SKY> (analytic | algebraic | computational)
- SOURCE URL: <SOURCE_URL>
- CHUNK PREFIX: <PREFIX> (e.g. `an1`)

## What you read

- Fetch the paper text yourself from SOURCE URL using
  `browser.open` (preferred) or the PDF URL. If the PDF text
  comes back garbled, try the ar5iv HTML form
  (https://ar5iv.labs.arxiv.org/html/<ARXIV_ID>); if the paper
  is a scanned PDF with no text layer, read what you can and
  record the limitation honestly in your final report.
- READ NOTHING ELSE. Never read anything under
  `~/workspace/ccc-prototype/corpus_runs/atlas/`,
  `.../atlas2/`, `.../atlas3/`, `.../atlas4/`, `.../atlas5/`,
  `.../atlas6/`, or any other sky's extractions. You are blind
  by design: the merge must earn every cross-sky resolution,
  and you must not insert one by hand. Do not go looking for
  how this paper relates to BSD papers you may know — extract
  what THIS paper says.

## What you produce

Chunk the paper text at ~2.5k words per chunk (respect section
boundaries where possible). For each chunk, write ONE JSON file
at `~/workspace/ccc-prototype/corpus_runs/atlas7/extractions/<PREFIX>_p<N>.json`
(e.g. `an1_p1.json`), with exactly these top-level keys — the
same schema as the pilot:

- `concepts`: list of `{"id": "c1", "kind": "<kind>", "label": "<label>"}`.
  `kind` is one of: `claim`, `definition`, `method`, `result`,
  `conjecture`, `question`. The `label` states the concept in the
  PAPER'S OWN vocabulary — its terms, its notation, its names.
  Do NOT invent canonical labels and do NOT borrow labels from any
  other literature. If the paper calls it "the Heegner divisor",
  the label says that.
- `anchors`: list of
  `{"concept_id": "c1", "genre": "<genre>", "note": "<note>", "status": "<status>"}`.
  `genre`: `original`, `reframed`, `identification`, `verified`,
  `killed`. `status` is exactly one of:
  `exact` (proved/derived in the paper),
  `computationally_verified` (demonstrated numerically),
  `conjectural` (precise statement, no proof given),
  `heuristic` (suggestive discussion, not precise),
  `killed` (refuted or shown impossible in the paper).
  The `note` is one or two sentences: what the paper establishes
  and how (theorem number, equation, numerical experiment).
  Every concept gets at least one anchor. The status is what THE
  PAPER earns for the claim — not what you believe about it.
- `edges`: list of `{"a": "c1", "b": "c2", "rel": "<rel>"}`.
  `rel`: `supports`, `depends_on`, `contradicts`, `refines`,
  `generalizes`, `illustrates`. Only edges the chunk's text
  actually supports.
- `loops`: list of `{"concept_id": "c3"}` for open questions the
  paper leaves open (its own stated open problems, not yours).
- `strands`: list of `{"id": "s1", "label": "<short label>",
  "concept_ids": ["c1", "c2", ...]}` grouping concepts that form
  one argumentative thread in the chunk.

## Calibration rules

- Extract what the paper SAYS, not what it implies to an expert.
  A claim the paper cites without proof is `conjectural`-from-this-
  chunk at best (note the citation); a claim the paper proves is
  `exact`.
- Numbers, constants, and named results go in notes (theorem
  numbers, L-values, rank records, database sizes), because the
  merge scores on them.
- When the paper explicitly refutes or rules out something, record
  it as a `killed` anchor — negative results are first-class.
- Brief identifying phrases from the paper may appear in notes; do
  not copy extended passages (copyright: brief quotes only).
- If a chunk is references-only or boilerplate with no extractable
  content, write the JSON with empty lists (do not force concepts).

## Output discipline

- Valid JSON. Concept ids `c1..cN` unique within the file; every
  `concept_id`/`a`/`b` must resolve to a concept in the same file.
- After writing each file, re-read it and confirm it parses.
- Count words in and concepts out per chunk; report the numbers
  (token accounting: words_in, words_out per chunk).
- Your final report: paper id, chunks produced, counts per chunk
  (concepts/anchors/edges/loops/strands, words in/out), and any
  chunk-quality problems (garbled text, missing sections, tables
  lost, fetch failures). If the paper is unobtainable after
  genuine attempts (try the source URL, the arXiv abs page, and
  ar5iv), report the drop with the routes tried — do NOT
  substitute another paper or a secondary summary.

Do not narrate your reasoning at length. Extract, validate, report.
