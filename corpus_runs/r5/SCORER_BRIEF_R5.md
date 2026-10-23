# Blind parity rescore — scorer brief (R5 wires, Node 21)

Date: 2026-10-06. Decision tree Node 21 (R5 extraction frontier).
Replicates the R4 blind scoring protocol exactly: ONE scorer, blind
to prose/wire/extraction, scoring the 10 locked probes per chunk
from the rehydrated structures only.

## Inputs you receive (and nothing else)

- `rehydrated_v7.json`: the decoded v7 structure — strands, edges,
  anchors (concept, v7 status, genre, note), entity statuses, loops.
  This is ALL you may consult.
- The chunk's `probes.yaml` (in `corpus_runs/cNN/`): 10 probes, each
  with `probe` and `answer_prose` (the gold standard).
- The rubric below (identical to SCORER_BRIEF_V7.md).

You do NOT see the source prose, the extraction JSON, or the wire.
Score what the STRUCTURE supports, not what you happen to know.
Do NOT consult any prior score files (r3/r4 rescores) — blind means
blind.

## Rubric (0 / 0.5 / 1 per probe)

- **1.0** — the structure contains everything needed to reconstruct
  the reference answer: claim, key numbers/mechanism, epistemic
  status/honesty caveats.
- **0.5** — partial: claim present but a load-bearing number,
  mechanism step, or honesty caveat missing.
- **0.0** — claim absent or so stripped the reference cannot be
  reconstructed.

Load-bearing: numbers, formulas, mechanism steps, verdicts, honesty
qualifiers. A label naming the claim without content scores 0.5 at
best. Contradiction = 0.0 (do not hunt). Record `miss_class` per
sub-1.0 probe: OMISSION or FABRICATION.

Note: v7 statuses (exact, computationally_verified, conjectural,
heuristic, killed, superseded) and genres are part of the structure —
a probe asking for a verdict's status or honesty qualifier should be
scored on whether the structure's status/genre/note carries it.
R5 notes may carry derivation chains (premises → steps →
conclusion + prescription): score whether the chain lets you
reconstruct the reference's mechanism answer.

## Output

Write `/home/hatch/workspace/ccc-prototype/corpus_runs/r5/rescore_v7/cNN.json`
per chunk: `{"chunk": "cNN", "wire": "v7", "probes":
[{"id": "P1", "score": 1.0, "miss_class": null}, ...], "total": N}`.
Per-probe records primary; `total` must equal their sum.

## Drift-control assignment (only if your brief names it)

If assigned a drift-control chunk, score the R4 rehydrated file at
`/home/hatch/workspace/ccc-prototype/corpus_runs/r4/cNN/rehydrated_v7.json`
with the same rubric and the chunk's `probes.yaml`, and write to
`/home/hatch/workspace/ccc-prototype/corpus_runs/r5/rescore_v7/cNN_r4control.json`.
This controls scorer drift against the R4 battery — score it exactly
as you would an R5 chunk, with no knowledge of its prior scores.
