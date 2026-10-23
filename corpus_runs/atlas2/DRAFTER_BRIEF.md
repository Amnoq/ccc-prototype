# Atlas-2 Drafter Brief (R4 one-shot extraction)

You are an extraction drafter for the Atlas-2 lemma atlas. Read this
whole brief, then do exactly what it says — one chunk, one JSON file.

## What you read

- READ: the single chunk file assigned to you, e.g.
  `~/workspace/ccc-prototype/corpus_runs/atlas2/chunks/sierra_p1.txt`.
- READ NOTHING ELSE. In particular, never read anything under
  `~/workspace/ccc-prototype/corpus_runs/atlas/` (the pilot corpus).
  You are blind to it by design: the merge must earn every
  cross-corpus resolution, and you must not insert one by hand.

## What you produce

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas2/extractions/<chunkid>.json`
(e.g. `sierra_p1.json` for chunk `sierra_p1.txt`), with exactly these
top-level keys — the same schema as the pilot:

- `concepts`: list of `{"id": "c1", "kind": "<kind>", "label": "<label>"}`.
  `kind` is one of: `claim`, `definition`, `method`, `result`,
  `conjecture`, `question`. The `label` states the concept in the
  PAPER'S OWN vocabulary — its terms, its notation, its names.
  Do NOT invent canonical labels and do NOT borrow labels from any
  other corpus. If the paper calls it "the deformed Hamiltonian",
  the label says that — not "Node 11i".
- `anchors`: list of
  `{"concept_id": "c1", "genre": "<genre>", "note": "<note>", "status": "<status>"}`.
  `genre` is one of: `original`, `reframed`, `identification`,
  `verified`, `killed`. `status` is exactly one of:
  `exact` (proved/derived in the paper — theorem, exact calculation),
  `computationally_verified` (demonstrated numerically in the paper),
  `conjectural` (precise statement, no proof given),
  `heuristic` (suggestive discussion, not precise),
  `killed` (refuted or shown impossible in the paper).
  The `note` is one or two sentences: what the paper establishes and
  how (theorem number, equation, numerical experiment). Every concept
  gets at least one anchor. The status is what THE PAPER earns for
  the claim — not what you believe about it.
- `edges`: list of `{"a": "c1", "b": "c2", "rel": "<rel>"}`.
  `rel` is one of: `supports`, `depends_on`, `contradicts`,
  `refines`, `generalizes`, `illustrates`. Only edges the chunk's
  text actually supports.
- `loops`: list of `{"concept_id": "c3"}` for open questions the
  paper leaves open (its own stated open problems, not yours).
- `strands`: list of `{"id": "s1", "label": "<short label>",
  "concept_ids": ["c1", "c2", ...]}` grouping concepts that form one
  argumentative thread in the chunk.

## Calibration rules

- Extract what the paper SAYS, not what it implies to an expert.
  A claim the paper cites without proof is `conjectural`-from-this-
  chunk at best (note the citation); a claim the paper proves is
  `exact`.
- Numbers, constants, and named results go in notes (e.g. "R=5.558691",
  "degree-16", "Table 5"), because the merge scores on them.
- When the paper explicitly refutes or rules out something, record it
  as a `killed` anchor — negative results are first-class.
- Brief identifying phrases from the paper may appear in notes; do not
  copy extended passages.
- If the chunk is references-only or boilerplate with no extractable
  content, write the JSON with empty lists (do not force concepts).

## Output discipline

- Valid JSON. Concept ids `c1..cN` unique within the file; every
  `concept_id`/`a`/`b` must resolve to a concept in the same file.
- After writing, re-read the file and confirm it parses (python3 -c
  "import json; json.load(open('...'))").
- Your final report: chunk id, counts (concepts/anchors/edges/loops/
  strands), and any chunk-quality problems (garbled text, missing
  sections, tables lost).

Do not narrate your reasoning at length. Extract, validate, report.
