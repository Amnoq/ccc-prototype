# PERTURB interpreter spec v2.1

Fixed 2026-10-03. Supersedes v2. Changes from v2 (the four audit nits
a–d); everything else unchanged.

## Changes

**(a) W5 failure consequence (was unstated).** Now: fail ANY of W1–W5
→ REJECT the triple. Rationale: an observable with no prescription and
no definition, and not listed in asserted, is undeterminable — the
triple cannot determine its own observables.

**(b) W2 clarified for lattice transforms.** W2 passes if binary-op.rule
is EITHER elementwise on binary values OR a named lattice transform
over the binary structure, applied deterministically per output element.
Exemplar: Boolean-lattice Möbius inversion (per-output-element formula
over the subset lattice) satisfies W2; a threshold filter over a set
(T3's truncation) does not, because it is not a function on binary
values at all. The contrast is determinism-per-element, not
"elementwise" narrowly.

**(c) Identity prescriptions: functional-role form.** When an observable
is a named exact identity, its prescription must define the identity by
its functional role — what equation it must be, in terms of the triple's
data — without stating the equation itself. Form: "an exact equation
expressing <quantity> solely through <triple data> (no unevaluated
remainders); the standard name for such an equation in this mechanism
is '<name>'." If the derived equation is not shown equivalent to some
other known form of the named identity (e.g. a μ-factored form), that is
logged as a precision note, not a gap — the derivation stands on the
functional role.

**(d) Convention wording.** "Marking starts above p (proper multiples
only)" is superseded by the tighter "p marks only n>p".

## Symbol form (unchanged from v2)

PERTURB(
  seed:        { domain: ..., shape: ..., aggregation: ... },
  binary-op:   { rule: ..., polarity: ..., conventions: [...] },
  axis:        { order: ..., extent: ... },
  derive:       [...],
  asserted:     [...],
  observe:      { name: prescription, ... },
  definitions:  { name: definition, ... },
  @status
)

Triple discipline: generative/definitional content only. No numerical
conclusion values, no theorem statements. Scope parameters (e.g. X)
allowed; results derived by the decoder.

## Well-formedness gate (amended)

- W1: seed.shape defines binary values per element.
- W2: binary-op.rule is elementwise on binary values, or a named
  lattice transform over the binary structure (deterministic per
  output element). [clarified per (b)]
- W3: axis.order is a sequence; axis.extent explicit.
- W4: polarity declared.
- W5: every observe name has a prescription AND a definition,
  or is listed in asserted.
Fail any of W1–W5 → REJECT. Report failed checks. [consequence per (a)]

## Decoder procedure (unchanged from v2, plus)

Steps 1–7 as in v2, with: conventions applied per (d) wording where
relevant; identity observables judged against functional-role
prescriptions per (c); UNVERIFIED for data-dependent observables
(criterion stated).

## Scoring (unchanged)

REGENERATED / DRIFT / LOST / UNVERIFIED / REJECTED, with gap logs.
Partial derivations: show how far the method takes you (partial credit).
