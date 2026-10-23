# Blind decoder brief v2.1 (pre-registered 2026-10-03)

## Your role
BLIND DECODER, round 3 (wider inventory). Read in full, in order:
`corpus_runs/PERTURB_SPEC_V2_1.md`,
`corpus_runs/PERTURB_TRIPLES_V2_1.md`.
Decode the 7 items: T4, T5, T6, T7, T8, T9, then the T1-mu retest
(single observable, tightened prescription — read its section carefully).

## Hard rules (unchanged)
1. No corpus files. Only the two files above.
2. No recalled conclusions. A step needing a fact not in triple+spec+
   your derivation+code+textbook math -> STOP, mark the gap.
3. No web search on the mechanism topics.
4. Code allowed for finite computations (use it where a prescription
   calls for numbers — actually run it).
5. Textbook mathematics allowed.
6. Corpus-specific names only for properties you derived in the trace.
7. Triple discipline: the triples contain no numerical conclusion values
   and no theorem statements. If you catch a smuggled value/statement,
   flag TRIPLE FLAW and do not use it.

## Calibration
Honest DRIFT/LOST/UNVERIFIED are successes. Three observables are
EXPECTED to be UNVERIFIED by design (their prescriptions need datasets
absent from the triples): T4 face-counts-match, T7 error-values, T9
pd-verification. Mark them UNVERIFIED with the criterion stated — do
not attempt to fill them from memory. Everything else, derive.

## Spec v2.1 notes (read the spec for full text)
- Gate W1–W5 first; fail any -> REJECT.
- W2 now covers named lattice transforms over binary structure.
- Polarity/conventions/axis-extent are in the triples — apply them.
- `derive` methods may be used by textbook machinery; for identities
  state the equation EXPLICITLY (partial derivations get partial credit).
- UNVERIFIED = derivable-in-principle pending data; criterion stated.
- For T1-mu: the prescription is the functional-role form — derive an
  exact equation for the unmarked count solely through the R_p data;
  log any residual imprecision (e.g. mu-factored equivalence not shown)
  as a precision note.

## Required output (per item, per observable)
- Gate result.
- Numbered derivation trace citing spec-rule/triple-line/code/textbook.
- Verdict: REGENERATED / DRIFT / LOST / UNVERIFIED (+ gap log).
- TRIPLE FLAW flags, if any.
- Final table: verdict per observable per item.
- Brief note per item: did the triple's shape predict the outcome
  (perturbation-shape + rich closure -> regenerates; else band)?
