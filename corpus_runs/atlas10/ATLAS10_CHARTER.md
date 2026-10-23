# Atlas-10 Charter — the chess atlas

**Date:** 2026-10-07
**Status:** chartered; launched on the user's tap
("let's go ahead and get that started").
**Parent:** Atlas-9 (corpus_runs/atlas9/) — COMPLETE (interweave,
not walls; 3 of 4 cracks verified).
**Question:** apply the atlas to chess — the flagship public map.
Three skies — theory (the books), annotations (the grandmasters'
words), engine (executable ground truth) — mapped against each
other to find the walls and the cracks. The AlphaZero precedent
says cracks exist here: things the engine knows that no
literature sky states.

## Triadic fork

1. **Claim:** the wall thesis holds in chess — theory and
   annotations barely touch the engine's ground truth except
   through narrow bridges; the cracks are engine-held facts no
   literature sky states.
2. **Polar opposite:** interweave — theory and annotations are
   densely confirmed by the engine; the literature already says
   what the engine knows.
3. **Null / controls:** (a) drafters BLIND per sky — the engine
   drafters never see the theory/annotation vocabularies and
   vice versa. (b) POSITIVE CONTROLS: documented pairs MUST
   resolve — e.g., a tablebase endgame result the theory books
   state (theory↔engine), and a famous annotated novelty the
   engine confirms at depth (annotations↔engine). Else method
   failure, reported plainly. (c) fabrication spot-checks; the
   user's grading packet is the final leg.

## Corpus (pilot scale)

- **Engine sky:** the executable territory. A FIXED set of
  positions/games selected by the coordinator (direction: famous
  theoretical positions + a handful of annotated games).
  ONLY actually-computable analysis — BK2011 strictly: if the
  engine is not runnable through the available instruments, it
  is dropped and recorded, never synthesized or proxied
  silently. Engine drafters follow PRE-REGISTERED procedures
  written BEFORE any analysis is run: fixed definitions of the
  structural concepts to extract (evaluation swings, novelty
  points, endgame conversions, drawing fortresses, zugzwang
  structures). Provenance per position in manifest.json.
- **Theory sky:** 1–2 documents of chess theory (coordinator
  selects; IDs verified live).
- **Annotations sky:** 1–2 collections of grandmaster
  annotations (coordinator selects; IDs verified live).

## Crack hunt

Every engine↔literature touch that the literature skies do not
state is a crack CANDIDATE (epistemic label: candidate). Each
candidate is verified against the engine — re-runnable analysis,
captured output — or marked refuted/undecidable on the record.
Zero refuted is a finding; zero verified is a finding.

## Deliverables (mirror Atlas-8/9)

- ATLAS10_REPORT.md — verdict, metric table, honest limits
- CRACK_LIST.md — every candidate with label and verification
- verification/ — rerunnable engine analyses + captured outputs
- atlas10_money.png — the money view (gold = adjudicated links)
- atlas10_interactive.html — the constellation browser
- grading_packet.md — sampled triples + ALL adjudications +
  drops + controls, for the user's grade
- manifest.json — corpus provenance
- blind discipline throughout; no sky sees another's vocabulary
  before adjudication

## Standing

Mapping run. The instrument draws; the decider decides.
