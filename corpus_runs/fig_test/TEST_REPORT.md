# Foreign-corpus test: Figueiredo §1 (arXiv:2405.09608)

Date: 2026-10-04. Product-validation experiment: does the R4/v7
pipeline work on material outside the prime corpus?

## Source

Section 1 ("Splitting amplitudes from joining surfaces") of
Figueiredo & Arkani-Hamed, "All-order splits and multi-soft limits
for particle and string amplitudes" (arXiv:2405.09608). 2,882 words —
same scale as the prime chunks. Chosen because the user knows this
paper (its generative process shaped D5).

## Pipeline (one-shot, no second judge)

1. R4 extraction by a single drafter, instructed NOT to force the
   prime vocabulary: 16 concepts · 16 anchors · 11 edges · 0 loops.
   `validate_extraction` → `[]`.
2. v7 wire build: 80 ints, 16 notes, 301 wire tokens.
3. Codec round-trip: exact.
4. Independent spec decode from DECODE_SPEC alone: PASS (16/16
   anchors with status+genre+note, 11/11 edges).

## Findings

- **Machinery transfers.** Statuses, genres, edges, notes, strands
  all function on foreign material. One-shot extraction validates
  clean — no second judge needed for *validity*.
- **No vocabulary forcing.** The drafter found no D-items,
  guardrails, or verdicts in her §1 and invented none. Her prose is
  constructive (builds the split formula) rather than
  verdict-driven (kills alternatives).
- **Status distribution correctly lopsided:** all 16 anchors
  `exact`. Not a failure — her §1 doesn't close anything
  negatively, conjecture, or hedge. The vocabulary didn't break;
  it had less to discriminate.
- **Vocabulary gap found:** no status for "announced but deferred"
  (roadmap). c12 (surface→physical map, "explored at one-loop")
  was marked exact as "documented framework scope" — the softest
  call, and a genuine gap: the R4 set has no "planned future work"
  status distinct from open_question.
- **Genre layer worked:** `identification` fired correctly on
  curves↔propagators (one-to-one stated dictionary);
  `reframed` on the u-equations as four-point special case.

## Open

Faithfulness judgment by the domain expert (the user knows this
paper): does the extraction capture what §1 actually says? That
verdict is his, not the pipeline's.
