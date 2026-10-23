# R4 battery review log

Reviewer: coordinator (second-judge). Every draft is read and
mechanically verified (validate_extraction == [], v7 round-trip,
note word counts, loops unanchored) before acceptance.

## c04 — ACCEPTED (2026-10-04)

21 concepts · 19 anchors · 14 edges · 2 loops.
Statuses: exact 12 · computationally_verified 4 (all with scope) ·
killed 2 · heuristic 1. Genres: none 10 · original 5 · reframed 2 ·
identification 2.

Notable calls:
- c9 scoped to the exhibited case (3-4-1 = q=(1,2,1)) rather than
  smuggling the generalization into exact — exactly the honesty the
  R4 prompt demands.
- c15 (Weil thesis) correctly heuristic, not exact — good restraint.
- c11 kill preserves 9c′ survival — no over-killing.
- c5 (division of labor → exact): ACCEPTED via inheritance — a verdict
  that follows by exact reasoning from exact premises carried in the
  text. Calibration refinement recorded: verdicts inheriting exactness
  from exact premises → exact.
- c17 bug-note ("corrected run") folded honestly into the note.

## c03 — ACCEPTED (2026-10-04)

13 concepts · 12 anchors · 8 edges · 1 loop.
Statuses: exact 9 · computationally_verified 1 · conjectural 1 ·
heuristic 1. Genres: reframed 6 · original 4 · none 2.

Notable calls:
- c3 (deformed μ-identity → exact): identity is exact algebra
  (inclusion-exclusion over CRT classes), checks ride in the note with
  scope — same pattern as the pilot's D1. Correct.
- c5 (singular series → reframed): constant classical, derivation path
  new — "not a new theorem" via genre. Mirrors pilot PNT treatment.
- c6 (twin asymptotic → conjectural, ANCHORED, not loop): the honest
  boundary survives as a precise unproven claim. Calibration
  refinement: conjectural = precise claim + stated boundary + no proof
  (boundaries stay anchored); loops = open questions only.
- c11 (9b verdict → exact): same inheritance rule as c04/c5.
- c12 correctly heuristic ("speculative; undeveloped") — restraint
  where the text doesn't develop the idea.

## c05 — ACCEPTED (2026-10-04)

22 concepts · 21 anchors · 14 edges · 1 loop.
Statuses: computationally_verified 11 · exact 9 · heuristic 1.
Genres: original 15 · identification 1 · none 5.

Notable calls:
- c3 (derived bound → computationally_verified): the text says
  "(derived)" but h≥0 is certified numerically per-window, not proved
  generally — the tie-break rule applied correctly. Claiming exact
  would have overstated. This is the R4 prompt working as designed.
- c16 → heuristic because the TEXT labels it heuristic — the agent
  followed the text's own label rather than upgrading.
- c6 (resonance): components verified, gloss interpretive →
  computationally_verified with component scope; interpretive part
  visible in the label, not smuggled into the status.
- c21 (bug-catching → exact): weakest exact, ACCEPTED. Calibration
  refinement: documented procedural facts verified by the work itself
  (fixes made, runs corrected) → exact. The note documents the facts;
  the status answers "how well established."
- All three honest-boundary items preserved at the right level
  (c9 anchored CV, c16 anchored heuristic, c22 loop) — no boundary
  dropped or upgraded.

## c09 — ACCEPTED (2026-10-04)

21 concepts · 18 anchors · 13 edges · 3 loops.
Statuses: exact 10 · conjectural 4 · computationally_verified 2 ·
heuristic 1 · killed 1. Genres: original 2 · none 16.

Notable calls:
- c10 (CCM → conjectural): the RH-relevant claim (spectra = zeros)
  is unproven with boundary stated; construction facts live in the
  note. Chose the status for the claim that matters — exactly right.
- c13 → exact on the text's own "VERDICT (negative, exact)" label;
  the negative is definite (sqrt-spectrum vs 14.13, 21.02).
- c15 → killed with the kill reasons preserved ("no zeros in
  machine; answer by hand; tautology"); replacement rule applied
  (c10 supersedes c15).
- c17 → exact ACCEPTED: cited to 10d (established in-program), same
  standing as cited classical results — the agent's flag was
  over-cautious, which is the right direction to err.
- c14 → heuristic on the text's own label. Three open questions in
  loops, none anchored.

## c11 — ACCEPTED (2026-10-04), one block edit by reviewer

21 concepts · 19 anchors · 6 edges · 2 loops.
Statuses: computationally_verified 8 · exact 7 · conjectural 4.
Genres: original 14 · identification 1 · none 4.

Notable calls:
- Prior-art block (reviewer decision): c6/c7/c8/c10 "no prior art
  found" → conjectural CONFIRMED. Rationale: the text itself marks
  novelty claims provisional ("re-search before any public claim");
  a negative literature search cannot be proved, unlike a bug fix
  verified by its corrected run (c05/c21 calibration does NOT extend
  here — closed loop vs open-ended search is the principled line).
  conjectural = precise + boundary-stated (search scope/date) +
  revisable, which is exactly a literature search's epistemics.
- c9 (prior art FOUND) → exact by reviewer edit: positive, checkable
  finding (repo exists); "priority unclear" caveat stays in the note.
  Precision over uniformity.
- c5 (D6 verdict → computationally_verified): inference from a
  computational sweep that passed its falsifiable test ({0,2,4}
  death) — not exact (not a proof), not conjectural (tested). Right.
- c13 (14c → exact + original): construction exhibited term-by-term;
  note documents the construction, which is what's exact.
- c19 (Λ=μ∗log → exact + identification): classical identity as
  bridge plank. Correct genre.
- Legacy c22 deliberately NOT coined (not in this chunk's text) —
  the discipline working: registry aliases are not chunk content.

## c08 — ACCEPTED (2026-10-04)

22 concepts · 21 anchors · 15 edges · 1 loop · 8 strands.
Statuses: exact 11 · computationally_verified 9 · conjectural 1.
Genres: original 12 · reframed 1 · identification 1 · none 7.

Notable calls:
- c1 (bridge span → conjectural): old R3 had it "verified" — plainly
  wrong for a programmatic inference. Precise, boundary-stated
  (circularity warning), unproven → conjectural, not heuristic
  (derivation path stated). Correct re-grade.
- c16 (function-field template → computationally_verified): template
  classical, but this text's contribution is the point-counting
  exhibition — a check with scope. Tie-break applied. Good discipline.
- c7 (dictionary → exact + identification): tightest form exhibited
  as exact algebra at σ=1/2. Consistent with the identification
  calibration.
- c18 → open_question/loop: the node's stated sharpest open question,
  straight R4 rule application.
- Honesty boundaries preserved: c2 "cited not derived", c3 "≠ RH
  proof", c22 "independence open → 10d".

## c10 — ACCEPTED (2026-10-04)

17 concepts · 15 anchors · 12 edges · 2 loops.
Statuses: exact 9 · computationally_verified 5 · conjectural 1.
Genres: original 9 · identification 1 · none 5.

Notable calls — the composite-verdict pattern (recurs; worth a
standing rule):
- c6 (Node 12 closed → exact): the VERDICT AS A RECORD is exact
  (Laplacian dead by theorem — factual); the live half stays
  conjectural, split in the note AND in c4's separate anchor. Rule:
  a verdict's closure-record can be exact while its live content
  keeps its own status — provided the split is explicit in note +
  concepts, not smuggled.
- c1 (framework → exact): same pattern — stipulation exact; live
  content (L4 conjectural) in note + c4.
- c7 (guardrails → exact): reading verdicts exact; D11's computational
  nature (counterexample (1129,1151)→21) preserved in the note.
- c14 (shuffled control → exact): the caveat follows by elementary
  logic from the exhibited measurement; text marks it (exact).
  Followed the text's own marking.
- c16 → computationally_verified (not exact): composite of two CV
  halves (13d GUE, 13e no prime lines). Right — didn't upgrade.
- Aggressive merging done well: 21→17, p<q,r<s kept separate as the
  mathematical fact it is.

## c07 — ACCEPTED (2026-10-04), one genre fix by reviewer

22 concepts · 20 anchors · 12 edges · 2 loops.
Statuses: exact 11 · computationally_verified 5 · killed 2 ·
conjectural 1 · heuristic 1.
Genres: original 7 · reframed 4 · identification 1 · none 8.

Notable calls:
- c14 (deformed μ-identity → computationally_verified): THE
  chunk-local honesty call. The text says "Exact" but THIS chunk
  doesn't carry the derivation — only the check (z=30, x=200000).
  Same identity is exact in c03 (derivation present), CV in c07
  (only checked). Not inconsistency — correct chunk-local
  epistemics; the merge layer reconciles. The protocol working.
- c2 (process transfer → exact): ACCEPTED as documented decision with
  demonstrated fruits (D1–D5). Not heuristic (not ungrounded), not
  unanchored (load-bearing commitment).
- c15 genre original→reframed by reviewer: identical content to
  c03/c5 (constant classical, derivation new); reframed is the
  honest genre. Battery consistency enforced.
- c16 (twin asymptotic → conjectural): clean, boundary stated.
- c21 (9c → killed) with kill reasons; c4 (naive hope → killed).
  Vocabulary handles negatives natively.
- Edges carry real structure: c4 causes c6, c16 bounds c15, c10
  exemplifies c11, c12 exemplifies c2.

## c01 — ACCEPTED (2026-10-04), three fixes by reviewer

22 concepts · 19 anchors · 10 edges · 3 loops.
Statuses: exact 12 · killed 3 · computationally_verified 2 ·
conjectural 2. Genres: reframed 4 · original 6 · identification 3 ·
none 6.

Notable calls:
- c4 genre original→reframed by reviewer (twin constant derivation;
  constant classical — battery consistency with c03/c5, c07/c15).
- c9 status computationally_verified→exact by reviewer (D10 verdict;
  consistency with c08/c22).
- c13 note fixed by reviewer (Weyl kills L1–L3; Heisenberg is
  supporting evidence, not the kill mechanism).
- c18 (14b+14c merged → conjectural): ACCEPTED — the home claim
  dominates; note splits "14b identity exact; home candidate"
  explicitly. Composite rule satisfied.
- c2 (Connes proof) killed here vs conjectural in c09 — CONSISTENT:
  c12 kills the 1999 *proof claim* (circular); c09 marks the
  *program* conjectural. Different claims, different statuses.

## c06 — ACCEPTED (2026-10-04), one genre fix by reviewer

15 concepts · 15 anchors · 11 edges · 0 loops.
Statuses: exact 11 · computationally_verified 4.
Genres: reframed 2 · original 5 · identification 2 · none 6.

Notable calls:
- c9 genre identification→none by reviewer: the zero-density audit
  *uses* classical estimates; no X⟷Y correspondence, so not
  identification.
- 0 loops legitimate: 1254-word results-dense chunk (10d/10e/14a–c);
  source has no open-question language. Closes things rather than
  opening them.
- c1 → computationally_verified (not exact): point counts exact but
  the *template exhibition* is the check — same calibration as
  c08/c16.

## c12 — ACCEPTED (2026-10-04), no edits

21 concepts · 20 anchors · 6 edges · 1 loop.
Statuses: exact 12 · killed 6 · conjectural 2.
Genres: original 5 · none 15.

Notable calls:
- Six kills with reasons preserved — the vocabulary handling the
  audit's negative results natively (c8 Bost-Connes, c12 Ruelle,
  c14 Sierra, c15 BBM, c16 Wu-Sprung, c2 Connes-as-proof).
- c5 (D_log eigenvalues → conjectural): matches c09/c10 CCM calls —
  the claim that matters is unproven.
- c5 depends_on c6 (open convergence question): the loop bounds the
  claim structurally, not just in a note.
- c20/c21 keep their conditionals explicit ("conditional on trace
  formula", "semilocal exact; full statement RH-equivalent").

### c06 addendum — drafter's late handoff (reasoning on c9)

The drafter argued c9 (zero-density audit) as identification: the
anchored claim is a "role-identification" (classical estimates ⟷ the
unconditionality plug-in), exhibited precisely. Reviewer edit to
genre none STANDS: identification is reserved for X⟷Y
correspondences between mathematical objects exhibited term-by-term
(Λ=μ∗log, faces=Fock, square dictionary). "X plays role R in
framework F" is a functional characterization — an application, not
a bridge. The drafter's other calls (c3 exact+original on the text's
own "derived"; c1 → computationally_verified honoring the text's
honest label over the exact point counts) were accepted as written.

### c01 addendum — drafter's late handoff (reasoning on c9)

The drafter argued c9 (D10 verdict) → computationally_verified via
the tie-break rule: the verdict summarizes mixed sub-results (9a
exact, 9b/10a computational), so doubt resolves downward. Reviewer
edit to exact STANDS, for a principled reason: the tie-break governs
doubt about the *claim's* status, but the D10 verdict is a
*closure-record* ("we found three kinds; none detected zeros"), and
the composite-verdict calibration (c10/c6) establishes that a
closure-record can be exact while its basis keeps mixed status —
provided the split is explicit. It is: the note names "9a/9b/10a",
and 9a/9b/10a hold their own anchors elsewhere. Downgrading every
summary verdict for mixed basis would make the vocabulary unable to
mark any verdict exact. The drafter's c5 flag (Figueiredo steer
leans on D5's closed status rather than re-exhibiting) is noted;
accepted as exact+identification since D5 is closed in-program.

### c12 addendum — drafter's late handoff (principles)

The drafter articulated the operative principle for cited results:
"anchor at what the text establishes, provenance in the note" —
applied to D_log self-adjointness (c4) and Deninger 2024 (c10), where
the text vouches without hedging (contrast the 50-zero figures,
which it explicitly withholds — that caution rides in c5's note).
Accepted. Residual risk noted by the drafter: grade inflation on
recent-literature reports; the notes let a decoder discount. Also
accepted: stipulated methods/standards → exact (checklist, forward
test, gold standard) as extension of "definitions → exact"; c11's
note ("labeled model-of-template; never ζ evidence") guards against
misreading "exact" as "the computation is exact."
