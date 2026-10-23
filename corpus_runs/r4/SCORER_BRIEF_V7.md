# Blind parity rescore — scorer brief (v7/R4 wires)

Date: 2026-10-04. Decision tree Node 18, R4 parity re-measurement.
Replicates the R3/v6 blind scoring protocol exactly: ONE scorer, blind
to prose/wire, scoring the 10 locked probes per chunk from the
rehydrated structures only.

## Inputs you receive (and nothing else)

- `rehydrated_v7.json`: the decoded v7 structure — strands, edges,
  anchors (concept, v7 status, genre, note), entity statuses, loops.
  This is ALL you may consult.
- The chunk's `probes.yaml` (in `corpus_runs/cNN/`): 10 probes, each
  with `probe` and `answer_prose` (the gold standard).
- The rubric below (identical to SCORER_BRIEF.md).

You do NOT see the source prose, the extraction JSON, or the wire.
Score what the STRUCTURE supports, not what you happen to know.

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

## Output

Write `/home/hatch/workspace/ccc-prototype/corpus_runs/r4/rescore_v7/cNN.json`
per chunk: `{"chunk": "cNN", "wire": "v7", "probes":
[{"id": "P1", "score": 1.0, "miss_class": null}, ...], "total": N}`.
Per-probe records primary; `total` must equal their sum.
