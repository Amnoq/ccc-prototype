# Atlas-8 Span-Pass Drafter Brief (supplementary extraction)

Standing instruction from the user (2026-10-07): in extraction and
adjudication, the SPANS BETWEEN primes — gaps, intervals, spacings —
are first-class concepts, not background. His words: like music —
if we want to hear the song the zeta zeros are singing, we must pay
attention to the spans in between; the song is in the intervals, not
just the notes.

You are doing a SUPPLEMENTARY span pass over a home-sky chunk that
has already had its main extraction. Your job is narrow: extract
ONLY span/gap/interval concepts — whatever the main pass may have
treated as background.

## What you read

- READ: the single chunk file assigned to you, e.g.
  `~/workspace/ccc-prototype/corpus_runs/atlas8/chunks/home_sieve1.txt`.
- READ NOTHING ELSE. In particular, never read any chunk file whose
  name starts with `foreign_`, and never read anything under
  `~/workspace/prime-sieve-geometry/` or the pilot's raw documents
  beyond your assigned chunk. You are blind to the foreign
  literature by design.

## What you capture

Every claim, definition, method, result, conjecture, or question in
the chunk ABOUT:
- prime gaps (maximal gaps, gap records, gap distributions, the
  user's "combos" — admissible prime constellations as gap patterns),
- the residue/gap inventory (which residues mod m can be prime,
  which gaps are forbidden),
- spacings between zeta zeros or between tones/orbit lengths
  (rests between tones, interval structure),
- the sieve's own span structure (distances between unshared
  points, boundary-spacing, what the gaps between spammed
  boundaries look like),
- any statement of the form "the literature says X about gaps"
  vs "the sieve shows Y" — these are crack-hunt gold; record
  both sides in the anchor note.

If the chunk genuinely contains no span concepts, write the JSON
with empty lists (do not force concepts).

## What you produce

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas8/extractions/<chunkid>_spans.json`
(e.g. `home_sieve1_spans.json`), with exactly these top-level keys:

- `concepts`: list of `{"id": "sp1", "kind": "<kind>", "label": "<label>"}`.
  Concept ids `sp1..spN` (the `sp` prefix avoids any collision with
  the main pass). `kind` is one of: `claim`, `definition`,
  `method`, `result`, `conjecture`, `question`. The `label` states
  the concept in the CHUNK'S OWN vocabulary.
- `anchors`: list of
  `{"concept_id": "sp1", "genre": "<genre>", "note": "<note>", "status": "<status>"}`.
  Same genre/status vocabularies as the main brief
  (HOME_DRAFTER_BRIEF.md). Copy the text's own epistemic label
  when it gives one. Numbers and bounds go in notes — the
  crack-verification step will check them against the sieve.
- `edges`: list of `{"a": "sp1", "b": "sp2", "rel": "<rel>"}` with
  the same rel vocabulary. Only edges the chunk's text supports.
- `loops`: the chunk's own stated open span questions.
- `strands`: groupings of span concepts that form one thread.

## Output discipline

- Valid JSON. Every `concept_id`/`a`/`b` must resolve within the file.
- After writing, re-read the file and confirm it parses.
- Your final report: chunk id, counts, and any span concept you
  suspect the main pass captured under a different framing (note
  the main-pass concept id if you can infer it — helps the merge).

Do not narrate your reasoning at length. Extract, validate, report.
