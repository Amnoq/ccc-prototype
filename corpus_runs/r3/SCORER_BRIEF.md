# Blind parity rescore — scorer brief (v6 wires)

Date: 2026-10-04. Decision tree Node 18, Track 1.
Replicates the R3 Phase-3 protocol exactly: ONE scorer, blind to
prose/wire, scoring the 10 locked probes per chunk from the rehydrated
structures only.

## Inputs you receive (and nothing else)

- `rehydrated_v6.json` (or `rehydrated.json` for the v5 control): the
  decoded structure — strands, edges, anchors (concept, status, note),
  entity statuses, loops. This is ALL you may consult.
- The chunk's `probes.yaml`: 10 probes, each with `probe` (the question)
  and `answer_prose` (the reference answer — the gold standard).
- This rubric.

You do NOT see the source prose or the wire. Do not use any outside
knowledge of the chunk's content beyond what the reference answer and
the structure give you. Score what the STRUCTURE supports, not what you
happen to know.

## Rubric (0 / 0.5 / 1 per probe — same as the battery)

For each probe, compare the rehydrated structure against the reference
answer (`answer_prose`):

- **1.0** — the structure contains everything needed to reconstruct the
  reference answer: the claim, its key numbers/mechanism, and its
  epistemic status/honesty caveats. A reader with only the structure
  could write an answer matching the reference.
- **0.5** — the structure supports a partial answer: the claim is
  present but a load-bearing number, mechanism step, or honesty caveat
  from the reference is missing.
- **0.0** — the claim is absent, or so stripped of its load-bearing
  content that the reference answer cannot be reconstructed.

Load-bearing means: numbers, formulas, mechanism steps, verdicts, and
honesty qualifiers ("not a new theorem", "remains unproven", scope of a
verification). A label naming the claim without its content scores 0.5
at best. Zero fabrication tolerance still applies: if the structure
*contradicts* the reference, that is 0.0, not 0.5 — but do not go
hunting for contradictions; score coverage.

Also record a `miss_class` per probe scoring < 1.0: OMISSION (content
absent from the structure) or FABRICATION (structure contradicts the
reference). The R3 battery found 0 fabrication; preserve that bar.

## Output

JSON: `{"chunk": "cNN", "wire": "v5"|"v6", "probes":
[{"id": "P1", "score": 1.0, "miss_class": null}, ...], "total": N}`.
Per-probe records are primary; `total` must equal their sum.

## Calibration notes (from R3)

- c04/c09 taught: distinguish scorer-strictness from wire loss. If the
  reference's nuance is genuinely in the structure, score it — do not
  punish the structure for the reference's verbosity.
- NUMBER probes: the number must be IN the structure (label or note),
  not merely implied.
- VERDICT probes: the verdict AND its status/qualifier must be present.
- MECHANISM probes: the mechanism's steps, not just its name.
