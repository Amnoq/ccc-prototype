# Blind parity rescore — scorer brief (R4 injection)

Date: 2026-10-04. Decision tree Node 20, open measurement: R4
injection parity (separates wire loss from extraction frontier).
Replicates the blind scoring protocol: ONE scorer, blind to prose,
scoring the 10 locked probes per chunk from the extraction only.

## Inputs you receive (and nothing else)

- `extraction.json`: the R4 extraction — concepts, strands, edges,
  anchors (concept_id, v7 status, genre, note), loops. This is ALL
  you may consult. (This is the "injection": the full structured
  content before wire encoding.)
- The chunk's `probes.yaml` (in `corpus_runs/cNN/`): 10 probes, each
  with `probe` and `answer_prose` (the gold standard).
- The rubric below (identical to SCORER_BRIEF.md).

You do NOT see the source prose or the wire. Score what the
EXTRACTION supports, not what you happen to know.

## Rubric (0 / 0.5 / 1 per probe)

- **1.0** — the extraction contains everything needed to reconstruct
  the reference answer: claim, key numbers/mechanism, epistemic
  status/honesty caveats.
- **0.5** — partial: claim present but a load-bearing number,
  mechanism step, or honesty caveat missing.
- **0.0** — claim absent or so stripped the reference cannot be
  reconstructed.

Load-bearing: numbers, formulas, mechanism steps, verdicts, honesty
qualifiers. Record `miss_class` per sub-1.0 probe: OMISSION or
FABRICATION.

## Output

Write `/home/hatch/workspace/ccc-prototype/corpus_runs/r4/rescore_injection/cNN.json`
per chunk: `{"chunk": "cNN", "wire": "injection", "probes":
[{"id": "P1", "score": 1.0, "miss_class": null}, ...], "total": N}`.
Per-probe records primary; `total` must equal their sum.
