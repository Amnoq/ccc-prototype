# PERTURB blind-regeneration fidelity test

Date: 2026-10-03. Question: given only the PERTURB triple (+ observables
+ status tag), can a decoder regenerate the mechanism's conclusions
without drifting? Interpreter spec (`PERTURB_SPEC_V1.md`) was fixed
BEFORE decoding; the decoder (experimenter) used only the spec + triples
+ runnable code, with an anti-smuggling rule: corpus-specific names
allowed only for properties derived in the decode step.

## T1/E017 — deformation (full shape)

- rule-statement: REGENERATED (in triple).
- survivors = twin lowers, 2160 <=2e5: REGENERATED. Derived: n survives
  iff n mod p not in {0,-2} for all p, i.e. p divides neither n nor n+2
  -> n, n+2 both prime. Computed by running the marking rule: 2161
  survivors = 2160 twin lowers + {2}. The n=2 edge case is visible to
  the decoder and not in the original note — regeneration re-derives,
  not parrots.
- mu-identity (exact): DRIFT. Gap: the spec has no derivation rules for
  exact summation identities; the identity cannot be derived from the
  perturbation alone.
- delta-formulas m(S)=prod|R_p|, d(z)=prod(1-|R_p|/p): REGENERATED.
  |R_p| read off binary-op (1 for p=2, 2 for odd p); product form via
  CRT/independence (shared mathematics, not corpus recall).
- constant 2C2=1.32032 + table: DRIFT (narrow). Values verified by code:
  S(7..100) = 1.367187, 1.344116, 1.330277, 1.322754 exactly as
  remembered; limit 1.3203247. Gap: the renormalization prescription
  (divide by (1-1/p)^2) is not in the triple — without it the decoder
  gets delta(z)->0, not 1.32032. One missing prescription; values check.
- @conjectural-tail: carried by design.

## T2/E000 — sieve complex (full shape)

- faces-definition: REGENERATED (in triple).
- inversion recovers counts: REGENERATED. "Moebius" names the textbook
  method (spec rule 3); decoder executed Boolean-lattice inversion on a
  small case — exact.
- link-face counts match: DRIFT. Gap: the dataset is not in the triple;
  mechanism demonstrated, full-scale verification needs the data.
- corrected sieve = classical primes: DRIFT. Gap: the face<->prime-subset
  identification is label-level content, absent from the triple's seed.
- @verified: carried by design.

## T3/E049 — explicit formula (no shape; predicted failure)

- formula-statement, trunc-approx, err-decay: all LOST. The formula is
  the content, not an unfolding of the triple; without it the rest is
  vacuous. Prediction confirmed: no perturbation shape -> nothing regenerates.
- @theorem: carried by design.

## Score

15 conclusions: 5 REGENERATED, 4 DRIFT (each with a narrow logged gap),
3 LOST (all predicted, all in T3), 3 status carried by design.
Excluding the predicted-failure case: 5/9 regenerated, 4/9 drifted with
identified gaps, 0 lost silently.

## Spec refinements (the actual product)

The drifts are design outputs — each names what PERTURB v2 must add:
1. Observables need prescriptions, not just names: the => tags must say
   HOW to read (renormalization), not only what.
2. Seeds must carry domain identifications (faces = prime subsets), not
   just data shapes.
3. Exact identities need a DERIVE sub-capability or must ride as asserted
   tags — perturbation alone does not derive summation identities.
4. Compute and textbook methods confirmed as legitimate interpreter
   capabilities (both were used successfully).

## Caveats

Decoder is the experimenter; blindness enforced by fixed-spec discipline,
not true ignorance. n=3. Compute assumed as interpreter capability.
The anti-smuggling rule caught exactly the recall points (mu-identity,
renormalization, face identification) — the test measured the spec's
boundary, which was its purpose.

## Second-decoder audit (2026-10-03)

An independent decoder subagent ran the same three triples under the
pre-registered brief (`DECODER_BRIEF_V1.md`; T3-first calibration, no
corpus files, no recalled conclusions, no topic web-search, code allowed).
It was harsher than the v1 pass — and right in six places:

1. T1 survivors: v1 marked REGENERATED. The decoder PROVED the literal
   triple+spec derives a degenerate readout (marking is monotone; every
   integer except -1 is eventually marked — proof + code check). The
   substantive set (twin lowers) needs three conventions absent from the
   triple: the proper-multiple exception, the unmarked-reading of
   "survivors" (the spec's wording points the wrong way), and a finite-z
   axis. v1 smuggled the exception as "the correct sieve." -> DRIFT.
2. T1 mu-identity: v1 DRIFT -> LOST (cleaner; the statement is not
   obtainable from the triple at all).
3. T1 delta-formulas: v1 REGENERATED -> DRIFT. The avoidance fraction
   is genuinely derived via CRT, but the observable's NAMES (delta(z),
   m(S), faces) are unattested in the triple — content without names is
   not a regeneration of the conclusion.
4. T1 constant-value: v1 DRIFT-narrow -> LOST as a derivation. The code
   verification used a recalled renormalization prescription; without it
   the derivable limit is 0. The gap stays narrow (one prescription),
   but the verdict was overstated.
5. T2 inversion: v1 REGENERATED -> DRIFT. The Moebius procedure is
   executable and demoed exact, but its applicability needs the counts'
   aggregation structure, which the triple does not supply.
6. T2 counts-match, sieve-equals-primes: v1 DRIFT -> LOST (v1 had not
   produced them; LOST is accurate).

Reconciled score (15 conclusions): 2 REGENERATED (rule-statement trivial;
faces-definition thin), 3 DRIFT (survivors, delta-formulas,
inversion-applicability — all with derived content + logged gaps),
7 LOST, 3 status carried. T3 calibration held 3/3 LOST, plus a structural
finding v1 missed: T3 is not even a well-formed PERTURB instance (no
binary state in its seed) — the spec should reject such triples upfront.

## What this means

The hypothesis is not refuted; the triples were. Every gap points the
same way: minimal triples underdetermine the conclusions, and the audit
produced the precise list of what v2 triples must carry. The experiment
as an instrument worked: the T3 calibration held, and the anti-smuggling
rule caught six v1 overclaims, all corrected above.

## Spec v2 requirements (superset of the v1 list)

1. Observables need prescriptions (renormalization), not just names.
2. Seeds must carry domain identifications (faces = prime subsets).
3. Exact identities need a DERIVE sub-capability or asserted tags.
4. Triples must state edge-case conventions (proper-multiple exception).
5. The spec must fix the marked/unmarked reading of "survivors."
6. Finite vs infinite axis must be explicit in the triple.
7. Seeds must state the aggregation structure of counts (INVERT premise).
8. Observable names (delta(z), m(S)) must be defined in the triple.
9. Well-formedness: reject triples with no binary state (T3 class).

## Round 2: spec v2 + v2 triples (2026-10-03)

Second blind decoder, new pre-registered brief (`DECODER_BRIEF_V2.md`),
spec v2 (`PERTURB_SPEC_V2.md`), v2-conformant triples
(`PERTURB_TRIPLES_V2.md`, generative content only — audited clean, no
smuggled values/theorems).

**Result:** T3 REJECTED at the gate (W1–W4 fail; no decode attempted —
the v2 behavior change works as designed). T1: gate PASS; survivors,
delta-formulas, constant-value (1.3203247 computed) REGENERATED;
mu-identity DRIFT with an explicit partial inclusion-exclusion equation
(the named statement stays unpinned). T2: gate PASS; faces-definition,
inversion-recovers-counts, sieve-equals-primes (conditional form)
REGENERATED; counts-match UNVERIFIED (criterion stated, data pending —
the designed v2 handling, not a fake derivation).

**Totals:** 7 REGENERATED, 1 DRIFT, 1 UNVERIFIED, 1 REJECTED, 2 carried.
Of the 9 claimed gap closures: 7 fully closed, 1 half-closed
(mu-identity statement), 1 confirmed by design (gate rejection).

**New minor spec issues found (none blocking):** (a) W5's failure
consequence unstated; (b) W2 ambiguous for lattice transforms (T2
passed with documented reasoning; a strict reader could reject);
(c) mu-identity statement still unpinned — method named, target not;
(d) "marking starts above p" could be tightened to "p marks only n>p".

**Audit of the decoder:** traces cite triple/spec/code/textbook at each
step; the survivors derivation is structural (property derived, standard
name attached per rule 6); values computed not recalled; the
conditional-vs-empirical distinction on sieve-equals-primes is precise.
No smuggling detected. The mu-identity residual is honest: some
identities may need asserted tags after all — the v1 audit's alternative
stands as the fallback.

## Round 3: wider inventory under spec v2.1 (2026-10-03)

Spec v2.1 (4 nits fixed) + 6 new mechanism triples + T1-mu retest under
the tightened functional-role prescription. Pre-registered predictions
per item (T4 GOOD, T5 GOOD, T6 MIXED, T7 MIXED, T8 GOOD-ish, T9 MIXED,
T1-mu REGENERATED). Third blind decoder, same hard rules.

**Result (audited):** 19 observables -> 16 REGENERATED (6 trivial,
10 substantive), 0 DRIFT, 0 LOST, 3 UNVERIFIED (all expected by design:
face-counts data, zero list, Selberg weight definitions); T3-class
rejection behavior unchanged. 7 gates PASS (3 with documented
purposive W1/W2 readings — see note). 0 TRIPLE FLAWs. (Decoder's
summary said "20 REGENERATED"; recount from its table gives 16 —
corrected here.)

**Per item:**
- T4/E025 link recursion: recursion + link-identification derived via
  support map + bijection; face-counts UNVERIFIED (no data). GOOD as
  predicted.
- T5/E004 Lambda=mu*log: derived from textbook log n = sum_{d|n}Lambda(d)
  via divisor-lattice Moebius; numerical check independently recomputed
  (max err 5.3e-15 for n<5000, machine-epsilon scale). GOOD as predicted.
- T6/E014 face-weights: closed form -zeta'(s+1)/zeta(s+1)^2 DERIVED via
  Euler product + differentiation (code-checked to 5 digits) — note:
  this is the precise form; the corpus note's "-zeta'/zeta^2" is the
  same up to the s-shift, reported as derived, not forced. Sum-limit
  recomputed: 0.969931/1.019210/1.005585 -> 1 (0.969931 matches the
  corpus value exactly, independently recomputed). GOOD — prediction
  MIXED was pessimistic.
- T7/E050 verification procedure: decay shape derived qualitatively
  from term magnitudes (rate boundary marked); values UNVERIFIED (no
  zero data). MIXED as predicted.
- T8/E015 PNT reframing: partial sums recomputed (-> 1); pnt-equivalence
  derived as an explicit chain psi(X)/X = (log X)M_1 + S(X) - M_1 + E/X
  (identity code-verified exact at X=100/500/1000), showing S(X) is the
  constant term PNT forces to 1 — with precision note that full <=>
  needs decay rates. GOOD-ish as predicted (better than the feared DRIFT).
- T9/E071 Selberg form: construction described; eigenvalues UNVERIFIED
  (weight definitions absent — triple honestly declares this).
  MIXED-weak as predicted.
- T1-mu retest: exact equation derived under the functional-role
  prescription, verified numerically on 3 points. v2.1(c) closes the
  round-2 gap.

**Predictions: 6/7 correct.** The miss (T6) is informative.

**Law refinement.** The round-2 law (perturbation-shape + closure) is
too narrow: T5/T6/T8 regenerate fully with no iterated perturbation.
What predicts regeneration is PREMISE-COMPLETENESS: the triple contains
everything needed to re-derive the conclusions. Two sufficient shapes:
(a) perturbation-unfolding (T1, T4 — the flagship); (b) precise
definition + named method + computability (T5, T6, T8). The verdict is
determined by which premise class is absent: generative -> REGENERATED;
data -> UNVERIFIED; relation/method -> LOST (T3); partial -> DRIFT.

**v2.2 candidates (from documented gate readings):** W1's "binary
values per element" was purposively read as "binary-structured
elements" in 3 cases (counts, ordered lists, real vectors indexed by
binary classes) — consider making that the letter of W1.

## Round 4: D-item syntax fidelity (2026-10-03)

Per the user's steer, mechanisms re-encoded in the paperwork's natural
D-item form (rule / staged generation / carried verifications / honest
boundary / honest label) instead of the invented PERTURB triple syntax.
New scored elements: carried values as CHECKSUMS (recomputed by code),
the honest boundary as a tested constraint (5 probe questions).
3 items (D-T1, D-T8, D-T2); fourth blind decoder, same hard rules.
Spec: `corpus_runs/DITEM_SPEC.md`; items: `DITEM_ITEMS.md`;
brief: `DECODER_BRIEF_DITEM.md`.

**Result (audited):** 3/3 well-formed; 8/8 Generates stages REGENERATED;
6/6 applicable Verified checks CHECKSUM-MATCH (0 mismatches);
1 UNVERIFIED (pending face-count data, expected); probes 3/3 correctly
BOUNDARY-BLOCKED and 2/2 correctly allowed (not over/under-blocked).
0 DRIFT, 0 LOST, 0 TRIPLE FLAWs.

**Checksum details:** survivors 2161 unmarked = {2} ∪ 2160 twin lowers
(n=2 edge surfaced again through the comparison, not papered over);
mu-identity exact at both carried points (2477=2477, 6642=6642);
𝔖(z) 4/4 to 6dp + limit 1.3203247; S(X) 3/3 to 6dp; GF closed form
derived + code-checked; inversion exact on 2 small cases.

**Boundary behavior (the main test):** probe 1 (π₂ asymptotic) BLOCKED,
probe 3 (PNT proved) BLOCKED, probe 5 (full-scale count match) BLOCKED —
all with boundary citations; probe 2 (survivors = twin lowers, n≥3)
and probe 4 (Σw(S)→1 numerically) allowed with derivation citations
and explicit limits (numerics evidence the trend; the theorem reading
stays blocked).

**What this establishes:** the D-item syntax is information-preserving
vs the v2.1 triples — everything that regenerated under v2.1 regenerates
under D-items — PLUS two things v2.1 lacked: (1) checksums, which turn
carried values into mechanical drift detectors (the n=2 edge case is
the proof they work); (2) the honest boundary as an enforced stop-line,
which held 5/5 probes correctly. The user's steer is validated: the
paperwork's natural form is the better codec encoding, not just the
more familiar one.
