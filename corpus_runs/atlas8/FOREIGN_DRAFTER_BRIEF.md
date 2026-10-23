# Atlas-8 Foreign-Sky Drafter Brief (R4 one-shot extraction)

You are an extraction drafter for the Atlas-8 lemma atlas, FOREIGN
sky (the landmark prime-distribution literature). Read this whole
brief, then the Atlas-2 drafter brief at
~/workspace/ccc-prototype/corpus_runs/atlas2/DRAFTER_BRIEF.md, then
do exactly what they say — one chunk, one JSON file.

## Assignment

- READ: the single chunk file assigned to you in your task message,
  e.g. `~/workspace/ccc-prototype/corpus_runs/atlas8/chunks/foreign_zhang_p1.txt`.
- READ NOTHING ELSE. In particular: never read any chunk file whose
  name starts with `home_`, never read anything under
  `~/workspace/ccc-prototype/corpus_runs/atlas/`,
  `~/workspace/prime-sieve-geometry/`, or any other atlas run
  directory. You are blind to the home sky by design: the merge
  must earn every cross-sky resolution, and you must not insert
  one by hand.

## Output

One JSON file at
`~/workspace/ccc-prototype/corpus_runs/atlas8/extractions/<chunkid>.json`
(e.g. `foreign_zhang_p1.json`), in EXACTLY the schema specified by
the Atlas-2 drafter brief (concepts/anchors/edges/loops/strands;
concept ids `c1..cN`; the same kind/genre/status/rel vocabularies).
Validate it parses with python3 after writing.

## Span directive (standing user instruction, 2026-10-07)

Treat the SPANS BETWEEN primes — gaps, intervals, spacings — as
FIRST-CLASS concepts, not background. His words: like music — if we
want to hear the song the zeta zeros are singing, we must pay
attention to the spans in between; the song is in the intervals,
not just the notes. Concretely: capture gap-structure claims
wherever they appear in your chunk — prime gaps (maximal gaps,
bounded gaps, gap distributions), admissible tuples as gap
patterns, zero spacings, intervals between arithmetic
progressions, sieve remainder/error intervals, anything the paper
states about what happens BETWEEN the primes. If the paper states
a gap claim with a number or bound, the number goes in the anchor
note.

## Calibration (in addition to the Atlas-2 brief's rules)

- Extract what the paper SAYS in the PAPER'S OWN vocabulary.
- The S1 control note: if your chunk contains Maynard's citation
  of Zhang's bounded-gaps breakthrough or the GPY method, capture
  it as a concept with the citation in the anchor note.
- Chunk-quality problems to report: garbled math from scan OCR
  (note it, extract the prose claims anyway), truncated sections.

Your final report: chunk id, counts
(concepts/anchors/edges/loops/strands), span concepts captured
(count them separately), and any chunk-quality problems.
