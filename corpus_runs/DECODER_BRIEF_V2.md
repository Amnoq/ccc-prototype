# Blind decoder brief v2 (pre-registered 2026-10-03)

## Your role
BLIND DECODER, second round. The spec has been revised to v2
(`corpus_runs/PERTURB_SPEC_V2.md` — read it fully) to close gaps found
by a first decoder. Your triples are v2-conformant
(`corpus_runs/PERTURB_TRIPLES_V2.md` — read it fully). Test whether v2
closes the gaps: derive what you can, mark precisely where you cannot.

## Hard rules (unchanged)
1. No corpus files. Only the two v2 files above.
2. No recalled conclusions. A step needing a fact not in triple+spec+
   your derivation+code+textbook math -> STOP, mark the gap.
3. No web search on the mechanism topics.
4. Code allowed for finite computations.
5. Textbook mathematics allowed.
6. Corpus-specific names only for properties you derived in the trace.

## New in v2 (read the spec for details)
- Run the WELL-FORMEDNESS GATE first (W1–W5). T3 is expected to be
  REJECTED at the gate — report the failed checks and stop there for T3.
  (In v1 it decoded-then-failed; v2 should reject it upfront.)
- Polarity is now declared: survivors = keep-polarity elements at axis end.
- Conventions are part of the triple: apply them during STEP.
- `derive` names proof methods you may use by textbook machinery. For
  mu-identity: produce the identity EXPLICITLY as an equation via
  inclusion-exclusion, or mark DRIFT with the exact gap (partial
  derivations get partial credit — show how far the method takes you).
- `asserted` and `@status` are carried, never derived.
- New verdict UNVERIFIED: for observables whose prescription needs a
  dataset the triple does not supply — state the verification criterion
  and mark UNVERIFIED (not derived, not lost — pending data).
- Triple discipline (for your audit awareness): the v2 triples contain
  no numerical conclusion values and no theorem statements — only
  definitions, prescriptions, conventions, named methods. If you catch
  the triple handing you an answer (a value or statement smuggled as a
  "definition"), flag it as a TRIPLE FLAW rather than using it.

## Order and calibration
T3 first (expect REJECT at gate), then T1, then T2. As before: DRIFT,
LOST, UNVERIFIED, and REJECTED are successful outcomes when honest.
The v1 audit found 9 specific gaps; v2 claims to close them. Your job
is to check that claim — including finding any NEW gaps v2 introduced
(e.g. over-rich triples, ambiguous prescriptions).

## Required output (per triple, per observable)
- Gate result (for T3: stop here).
- Derivation trace: numbered steps citing spec-rule/triple-line/code.
- Verdict: REGENERATED / DRIFT / LOST / UNVERIFIED (+ gap log).
- Any TRIPLE FLAW flags.
- Final table: verdict per observable per triple.
