# Blind parity rescore — scorer brief (CCC-2 wires, gate CCC2-4)

Date: 2026-10-06. Decision tree node CCC2-4 (parity gate).
Replicates the R5 blind scoring protocol exactly: ONE scorer, blind
to prose/wire/extraction/format-spec, scoring the 10 locked probes
per chunk from the rehydrated structures only.

## Inputs you receive (and nothing else)

- `rehydrated_ccc2_cNN.json`: the decoded CCC-2 wire — a flat list of
  records. Record types:
  - **D** (D-item / mechanism): `subtitle`, `rule` (generative rule),
    `conventions` (list), `generates[]` (each: `stage` + `prescription`
    — how to derive it), `verified[]` (each: `check` + `expected`, or
    `pending` + `criterion`), `honest_boundary` (where the derivation
    STOPS; what is NOT claimed), `honest_label` (epistemic status),
    `genre` (optional: original/reframed/identification).
  - **G** (guardrail): standing rules / constraints.
  - **V** (verdict): a verdict — its status and consequence.
  - **B** (bridge): `x` ⟷ `y`, plus `buys` (what it buys) and `limits`.
  - **C** (claim / definition / question).
  - **L** (typed link between records).
  This is ALL you may consult.
- The chunk's `probes.yaml` (in `corpus_runs/cNN/`): 10 probes, each
  with `probe` and `answer_prose` (the gold standard).
- The rubric below (identical to SCORER_BRIEF_R5.md).

You do NOT see the source prose, the extraction JSON, the wire, the
format spec, or the codec. Score what the STRUCTURE supports, not
what you happen to know. Do NOT consult any prior score files (r3/r4/
r5 rescores) — blind means blind.

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

Note: `honest_label` values (exact, computationally_verified,
conjectural, heuristic, killed, superseded, unstated) and `genre`
are part of the structure — a probe asking for a verdict's status or
honesty qualifier should be scored on whether the record's label /
honest_boundary / note carries it. D-item `generates[]` stages carry
derivation chains (stage → prescription): score whether the chain
lets you reconstruct the reference's mechanism answer. `honest_
boundary` is a required field — where it states what is NOT claimed,
that is the structure's honesty answer.

## Output

Write `/home/hatch/workspace/ccc-prototype/ccc2/parity_gate/rescores/cNN.json`
per chunk: `{"chunk": "cNN", "wire": "ccc2", "probes":
[{"id": "P1", "score": 1.0, "miss_class": null}, ...], "total": N}`.
Per-probe records primary; `total` must equal their sum. Include a
one-line note per sub-1.0 probe naming what was missing (or what
was fabricated, if any).

## Drift-control assignment (only if your brief names it)

If assigned a drift-control chunk, score the R5 rehydrated file at
`/home/hatch/workspace/ccc-prototype/corpus_runs/r5/cNN/rehydrated_v7.json`
with the R5 rubric (anchors: concept, v7 status, genre, note — score
whether the structure carries claim, numbers/mechanism, status/honesty)
and the chunk's `probes.yaml`, and write to
`/home/hatch/workspace/ccc-prototype/ccc2/parity_gate/rescores/cNN_r5control.json`.
This controls scorer drift against the R5 battery — score it exactly
as you would a CCC-2 chunk, with no knowledge of its prior scores.
