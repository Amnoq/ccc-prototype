# PERTURB interpreter spec v1

Fixed 2026-10-03, BEFORE any decoding below. Generic: no mechanism-
specific clauses. The decoder below may use only this spec + the
triples + runnable code. It may not consult corpus text, notes, or
remembered conclusions.

## Symbol form

PERTURB(seed, binary-op, axis; observe: o1, o2, ...; @status)

- seed: discrete state description — elements with binary values
  (marked/unmarked, in/out, +/-1).
- binary-op: elementwise function on binary values; may carry
  element-dependent parameters named in the triple.
- axis: ordered steps (or limit) along which binary-op is applied.
- observe: named readouts to report on the unfolded state.
- @status: epistemic-status tag, carried verbatim, never derived.

## Decoder procedure

1. STATE: build the discrete state from seed. No corpus lookup.
2. STEP: apply binary-op elementwise, advance axis one step, repeat
   to axis end (or stated limit).
3. READOUT per observable:
   - survivors: elements still marked at end; describe STRUCTURALLY
     (the property defining them). Corpus-specific NAMES for that
     property are allowed only if the property itself is derived here.
   - invariants: quantities provably unchanged by binary-op — state
     quantity + one-line reason, else mark underivable.
   - aggregates: sums/products over marked elements, symbolically;
     numerical values via code (rule 4).
   - limits: axis->infinity behavior, only if the triple states a limit.
   - named-method: if binary-op names a textbook method (e.g.
     "Moebius"), its standard definition may be used.
4. COMPUTE: the decoder may run code for finite computations. It may
   NOT fetch corpus text or use remembered corpus conclusions.
5. STATUS: carried verbatim.

## Scoring (per conclusion)

- REGENERATED: derived by steps 1-5 above from triple alone.
- DRIFT: produced but required corpus-specific recall — log the gap
  (what the spec failed to supply).
- LOST: in the original conclusions but not obtainable from the triple.

## Triples under test (from exp2_procsym_triples.json)

T1/E017: seed="integer line / residue classes, each marked or unmarked";
  binary-op="R_p marking: R_2={0}, R_p={0,-2} odd p";
  axis="primes 2,3,5,... z->oo";
  observe: rule-statement, survivors, mu-identity, delta-formulas,
  constant-value; @conjectural-tail.
T2/E000: seed="face data: binary subsets (in/out), aggregated counts";
  binary-op="Moebius inversion, alternating +-1 signs";
  axis="subset lattice, large faces -> singletons";
  observe: faces-definition, inversion-recovers-counts, counts-match,
  sieve-equals-primes; @verified.
T3/E049: seed="zero locations rho of zeta";
  binary-op="truncation at height T";
  axis="T -> oo";
  observe: formula-statement, trunc-approx, err-decay; @theorem.
