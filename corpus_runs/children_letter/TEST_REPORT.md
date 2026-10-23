# Foreign-corpus test 2: "For My Children" letter

Date: 2026-10-06. Second product-validation experiment: does the
R4/v7 pipeline work on non-technical, philosophical material?

## Source

"For My Children — The Part of the World You Can Touch" (letter,
8 pages, 1,747 words), authored by the user, addressed to his
children. Philosophical/exhortatory prose: one-reality relational
metaphysics, the dream picture, the golden rule and know-thyself
regrounded, responsibility vs blame, cycles, practical diagnostic
questions. Chosen because it is maximally distant in genre from both
the prime corpus and the Figueiredo physics test.

## Pipeline (one-shot, no second judge)

1. R4 extraction by a single drafter (subagent), with the fig_test
   instruction NOT to force the prime-sieve vocabulary: 13 concepts
   (12 claim + 1 method) · 13 anchors · 10 edges · 0 loops · 6
   strands. `validate_extraction` → `[]`.
2. v7 wire build: 70 ints, 13 notes, 284 wire tokens
   (prose 2,269; extraction JSON 1,192; BE_dep 1.74).
3. Codec round-trip: exact.
4. Independent spec decode from DECODE_SPEC alone: PASS (13/13
   anchors with status+genre+note, 10/10 edges).

## Findings

- **Machinery transfers across a third genre.** Statuses, genres,
  edges, notes, strands all function on philosophical prose.
  One-shot extraction validates clean — no second judge needed for
  *validity*, same as fig_test.
- **No vocabulary forcing.** The drafter found no D-items,
  guardrails, verdicts, or killed claims and invented none. The
  letter is constructive and exhortatory, like her §1.
- **Status distribution correctly lopsided the other way:** all 13
  anchors `heuristic`. Not a failure — the honest outcome: the
  author explicitly disclaims proof ("I cannot prove that to you,
  and I do not ask you to accept it as a rule"); every claim rests
  on intuition, analogy, or practical wisdom with no derivation
  path stated. The same vocabulary that marked her derivations
  `exact` marks his offerings `heuristic` — it discriminates,
  it doesn't flatter.
- **Closest-to-derivation check held:** the regress argument
  ("turn your attention toward the observer and it becomes the
  observed", c6) was considered for a stronger status but judged
  argument-by-analogy, not derivation — kept heuristic. The drafter
  flagged the soft call unprompted.
- **Genre layer worked:** `original` on the one-reality thesis, the
  witness-regress move, the ocean/hands formulation, and the three
  near-questions (the one claim extracted as a *method* — the
  letter's diagnostic procedure); `reframed` on the golden rule
  and know-thyself, matching the fig_test usage (classical maxim
  regrounded in the framework).
- **Edge vocabulary spread naturally:** exemplifies (dream→thesis),
  refines (witness→thesis, fault/responsibility→jurisdiction),
  supports, bounds (thesis bounds responsibility's scope), implements
  (three questions implement the jurisdiction; "be the water"
  implements the cycle claim).
- No "announced but deferred" roadmap content appeared, so the
  fig_test vocabulary gap was neither exercised nor resolved.

## Open

Faithfulness judgment by the domain expert (the author): does the
extraction capture what the letter actually says? That verdict is
his, not the pipeline's.
