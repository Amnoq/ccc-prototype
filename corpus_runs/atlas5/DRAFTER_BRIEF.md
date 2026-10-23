# Atlas-5 Drafter Brief (R4 one-shot extraction)

You are an extraction drafter for the Atlas-5 RH receipt run. Read this
whole brief, then do exactly what it says — one chunk, one JSON file.

## What you read

- READ: the single primary-text URL assigned to you (e.g.
  `https://ar5iv.org/html/2004.09765`), fetched with `browser.open`,
  restricted to the line range assigned to you (e.g. "lines 0–400 of
  the fetched text"). Fetch the page text, then work only within your
  assigned range.
- READ NOTHING ELSE. In particular, never read anything under
  `~/workspace/ccc-prototype/corpus_runs/atlas/` (the pilot corpus /
  relational sky), any other sky's materials, or any chunk/summary
  files under `~/workspace/ccc-prototype/corpus_runs/atlas5/chunks/`
  (those are provenance records, not drafting sources). You are
  blind by design: the merge must earn every cross-sky resolution,
  and you must not insert one by hand.
- Do NOT save the fetched text to disk. Read it, extract from it,
  and let it go (Atlas-2 license-policy D2: no full text kept on
  disk).

## What you produce

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas5/extractions/<chunkid>.json`
(e.g. `comp_platttrudgian2021_p1.json` for the first assigned range
of the Platt–Trudgian paper), with
exactly these top-level keys — the same schema as the pilot:

- `concepts`: list of `{"id": "c1", "kind": "<kind>", "label": "<label>"}`.
  `kind` is one of: `claim`, `definition`, `method`, `result`,
  `conjecture`, `question`. The `label` states the concept in the
  PAPER'S OWN vocabulary — its terms, its notation, its names.
  Do NOT invent canonical labels and do NOT borrow labels from any
  other corpus or tradition.
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

## Preprint discipline (Alpöge–Furman chunk ONLY)

If your chunk comes from the Alpöge–Furman paper (arXiv:2608.13637):
the paper is a PREPRINT as of 2026-10-07, not a refereed publication.
Add top-level `"preprint": true` to your JSON file, and add
`"preprint": true` to every anchor. Do NOT upgrade any status on the
grounds that the result is "known" or "will survive review" — the
status is what the preprint text itself earns. For all other chunks,
omit the flag entirely.

## Calibration rules

- Extract what the paper SAYS, not what it implies to an expert.
  A claim the paper cites without proof is `conjectural`-from-this-
  chunk at best (note the citation); a claim the paper proves is
  `exact`.
- Numbers, constants, and named results go in notes (e.g.
  "3×10^12", "67.25%", "N(T)"), because the merge scores on them.
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
