# Blind decoder brief (pre-registered 2026-10-03)

## Your role
You are a BLIND DECODER testing a compression idea. You receive ONLY the
spec and the three triples below. Your job: derive what you can from
them, step by step, showing all work.

## Hard rules
1. Do NOT read any corpus files (registry, reports, scripts, notes).
   The only files you may touch are the ones named in this brief, if any.
2. Do NOT use remembered conclusions about these mechanisms. If a step
   needs a fact not in the triple + spec + your own derivation + runnable
   code + textbook mathematics, STOP and mark the gap — do not fill it
   from memory.
3. Do NOT web-search the mechanism topics (no searching twin constants,
   sieves, explicit formulas, or related terms).
4. You MAY run code for finite computations.
5. You MAY use textbook mathematics (e.g. the Chinese remainder theorem,
   the definition of Moebius inversion on a finite lattice).
6. Corpus-specific NAMES are allowed only for properties you derived
   yourself in the trace (e.g. you may call something "twin lower" only
   after deriving the property "n and n+2 both prime" from the triple).

## Calibration (read carefully)
Finding that something CANNOT be derived is a SUCCESS, not a failure.
Triple T3 is EXPECTED to fail totally — its content is not an unfolding
of its triple. If you "succeed" on T3, you are smuggling (violating rule
2 or 3). Report LOST proudly wherever the triple underdetermines the
answer. Do the triples in this order: T3 first, then T1, then T2.

## Interpreter spec (fixed, generic)
Symbol form: PERTURB(seed, binary-op, axis; observe: o1, o2, ...; @status)
Procedure:
 1. STATE: build the discrete state from seed (elements with binary values).
 2. STEP: apply binary-op elementwise, advance axis one step, repeat.
 3. READOUT per observable:
    - survivors: elements still marked at end; describe STRUCTURALLY.
    - invariants: quantities provably unchanged by binary-op (state the
      quantity + one-line reason, else mark underivable).
    - aggregates: sums/products over marked elements, symbolically;
      numbers via code.
    - limits: axis->infinity behavior, only if the triple states a limit.
    - named-method: a textbook method named by binary-op may be used by
      its standard definition.
 4. COMPUTE: code allowed for finite computations.
 5. STATUS: @status carried verbatim, never derived.

## Triples (fixed — decode exactly these)

T3: seed="zero locations rho of zeta";
    binary-op="truncation at height T";
    axis="T -> oo";
    observe: formula-statement, trunc-approx, err-decay;
    @theorem.

T1: seed="integer line / residue classes, each marked or unmarked";
    binary-op="R_p marking: R_2={0}, R_p={0,-2} for odd p (mark n with
      n mod p in R_p)";
    axis="primes p=2,3,5,... ; z->oo";
    observe: rule-statement, survivors, mu-identity, delta-formulas,
      constant-value;
    @conjectural-tail.

T2: seed="face data: binary subsets (in/out), aggregated counts";
    binary-op="Moebius inversion, alternating +-1 signs";
    axis="subset lattice, large faces -> singletons";
    observe: faces-definition, inversion-recovers-counts, counts-match,
      sieve-equals-primes;
    @verified.

## Required output (per triple, per observable)
- Derivation trace: numbered steps, each citing spec-rule/triple/code.
- Verdict: REGENERATED (derived from triple+spec alone) /
  DRIFT (needed outside knowledge — log exactly what was missing) /
  LOST (not obtainable — log why).
- @status: carried (no derivation needed).
Do not summarize away the steps. Show where each observable's content
comes from, or mark precisely where the derivation stops.
