# Atlas-8 Home-Sky Drafter Brief (R4 one-shot extraction)

You are an extraction drafter for the Atlas-8 lemma atlas, HOME sky
(the circle-sieve side). Read this whole brief, then do exactly what
it says — one chunk, one JSON file.

## What you read

- READ: the single chunk file assigned to you, e.g.
  `~/workspace/ccc-prototype/corpus_runs/atlas8/chunks/home_sieve1.txt`.
- READ NOTHING ELSE. In particular, never read any chunk file whose
  name starts with `foreign_`, and never read anything under
  `~/workspace/prime-sieve-geometry/` or the pilot's raw documents
  beyond your assigned chunk. You are blind to the foreign
  literature by design: the merge must earn every cross-sky
  resolution, and you must not insert one by hand.

## What you produce

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas8/extractions/<chunkid>.json`
(e.g. `home_sieve1.json` for chunk `home_sieve1.txt`), with exactly
these top-level keys — the same schema as the pilot:

- `concepts`: list of `{"id": "c1", "kind": "<kind>", "label": "<label>"}`.
  `kind` is one of: `claim`, `definition`, `method`, `result`,
  `conjecture`, `question`. The `label` states the concept in the
  CHUNK'S OWN vocabulary — its terms, its notation, its names.
  Do NOT invent canonical labels. Pay special attention to: the
  sieve's mechanical rules (shared/unshared, spammed boundaries),
  the incidence complex and face-sum identities, epistemic labels
  the text already carries (exact / computationally_verified /
  conjectural / heuristic), and anything the text marks as NEW
  (framing appears new, prior art searched).
- `anchors`: list of
  `{"concept_id": "c1", "genre": "<genre>", "note": "<note>", "status": "<status>"}`.
  `genre` is one of: `original`, `reframed`, `identification`,
  `verified`, `killed`. `status` is exactly one of:
  `exact`, `computationally_verified`, `conjectural`, `heuristic`,
  `killed`. The `note` is one or two sentences: what the text
  establishes and how. Every concept gets at least one anchor.
  The status is what THE TEXT earns for the claim — copy the
  text's own epistemic label when it gives one.
- `edges`: list of `{"a": "c1", "b": "c2", "rel": "<rel>"}`.
  `rel` is one of: `supports`, `depends_on`, `contradicts`,
  `refines`, `generalizes`, `illustrates`. Only edges the chunk's
  text actually supports.
- `loops`: list of `{"concept_id": "c3"}` for open questions the
  text leaves open (its own stated open problems, not yours).
- `strands`: list of `{"id": "s1", "label": "<short label>",
  "concept_ids": ["c1", "c2", ...]}` grouping concepts that form one
  argumentative thread in the chunk.

## Calibration rules

- Extract what the text SAYS, not what it implies. A claim the
  text marks "framing appears new" is `original` genre; a
  reframing of classical math is `reframed` — record the text's
  own prior-art note in the anchor note.
- Numbers, N-ranges, and verification bounds go in notes (e.g.
  "N = 30 … 2000", "face-sum Möbius"), because the merge scores
  on them and the crack-verification step will check them.
- When the text explicitly kills something, record it as a
  `killed` anchor — negative results are first-class.
- If the chunk is references-only or boilerplate with no
  extractable content, write the JSON with empty lists.

## Output discipline

- Valid JSON. Concept ids `c1..cN` unique within the file; every
  `concept_id`/`a`/`b` must resolve to a concept in the same file.
- After writing, re-read the file and confirm it parses.
- Your final report: chunk id, counts (concepts/anchors/edges/loops/
  strands), and any chunk-quality problems.

Do not narrate your reasoning at length. Extract, validate, report.
