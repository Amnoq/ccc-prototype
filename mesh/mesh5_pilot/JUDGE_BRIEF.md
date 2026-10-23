# MESH-5 Pilot — Judge Brief (fixed judge "j4")

**Version:** 2026-10-09. **Note:** the step-4 j4 brief text was not
preserved as a file; this brief is reconstructed from
VERDICT_PACKET_SPEC.md v1.1 and the step-4 judge output format
(step4/judge_outputs/j4/). It is documented as reconstructed.
**Your task:** assign an epistemic label to every input record. That is
the entire task.

## Input

A JSON list of records, each: `{record_id, claim, span, source}`.
The claim is one sentence in the work's own words; the span is the
verbatim source quote.

## Output

For each record, render:
- `record_id`: echo it.
- `claim`: the claim as judged, in the work's own words. Never invent
  a private taxonomy about it.
- `label`: exactly one of the four below.
- `boundary`: ONE line stating what is NOT claimed — the honest
  stop-line. Not boilerplate; a real sentence about this claim's
  limits.
- `span`: echo the input span.

Write JSON `{"judgments": [...]}` to the assigned output path.

## The labels (assign exactly one per record)

- `exact`: proved as a theorem or definitional identity. No numerics
  needed; nothing left to check. Reserve for genuine proof.
- `computationally_verified`: verified by a live computation with
  controls, rerunnable from the record. The numbers were computed,
  not asserted.
- `conjectural`: a precise, sharp statement whose earning isn't done —
  unproved, or asserted without the computation that would verify it.
  Precision without proof.
- `heuristic`: suggestive but not yet precise — an analogy, a
  qualitative reading, a direction, not a testable claim.

## Rules

- Judge the claim against its span and source context. Do not import
  outside knowledge to upgrade or downgrade.
- The boundary must be specific to the claim. "Further work needed"
  is not a boundary.
- Labels only: do not add commentary, do not re-rank, do not link.
- If a claim is malformed (no identifiable assertion), label it
  `heuristic` and say so in the boundary — do not skip it.
