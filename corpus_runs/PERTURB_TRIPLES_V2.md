# PERTURB triples v2 (conformant; generative content only)

Fixed 2026-10-03 with PERTURB_SPEC_V2. No numerical conclusion values,
no theorem statements below — only definitions, prescriptions,
conventions, and named methods. All values/identities must be derived
by the decoder.

## T3 (unchanged v1 triple — expected: REJECT at gate)
seed="zero locations rho of zeta";
binary-op="truncation at height T";
axis="T -> oo";
observe: formula-statement, trunc-approx, err-decay;
@theorem.

## T1 v2
PERTURB(
  seed: { domain: "integers n, 2<=n<=X (X a parameter)",
          shape: "each n unmarked initially",
          aggregation: "n/a" },
  binary-op: { rule: "for each prime p in axis order: mark n iff n mod p in R_p, where R_2={0}, R_p={0,-2} for odd p",
               polarity: "mark=remove",
               conventions: ["p does not mark itself (proper multiples only: marking starts above p)",
                             "0 is marked at p=2"] },
  axis: { order: "primes 2,3,5,...", extent: "finite(z)" },
  derive: ["inclusion-exclusion over the marking rule",
           "CRT independence of residues mod distinct primes"],
  asserted: [],
  observe: {
    rule-statement: "restate binary-op",
    survivors: "unmarked n at axis end (polarity mark=remove); describe structurally",
    mu-identity: "exact summation identity for the marked/unmarked counts, produced via derive[0]; state it as an equation, or mark DRIFT with the gap",
    delta-formulas: "define delta(z) := fraction of n<=X with n mod p not in R_p for all p<=z; define m(S) := product of |R_p| over p in S; derive both via derive[1]",
    constant-value: "prescription: renormalize delta(z) by dividing by prod_{p<=z}(1-1/p)^2; take z->infinity; compute numerically"
  },
  definitions: { R_p: "marked residue set for prime p: {0} for p=2, {0,-2} for odd p",
                 delta(z): "see observe prescription",
                 m(S): "see observe prescription" },
  @conjectural-tail
)
Parameter for the decode run: X=200000, z large (decoder chooses z; note the choice).

## T2 v2
PERTURB(
  seed: { domain: "faces = finite prime subsets: each subset S of primes <=z is a face",
          shape: "binary: subset in/out",
          aggregation: "superset-sums: g(T) = sum_{S superset T} f(S)" },
  binary-op: { rule: "Moebius inversion on the Boolean lattice: f(T) = sum_{S superset T} (-1)^{|S|-|T|} g(S)",
               polarity: "n/a (transform, not marking)",
               conventions: [] },
  axis: { order: "subset lattice, large faces -> singletons", extent: "finite" },
  derive: ["Moebius inversion on a finite lattice (textbook)"],
  asserted: [],
  observe: {
    faces-definition: "restate seed domain",
    inversion-recovers-counts: "apply binary-op to the seed aggregates; demonstrate exactness on a small case by code",
    counts-match: "criterion: inverted fine counts vs direct integer counts; VERIFY-BY-DATA — no dataset in triple, so mark UNVERIFIED with the criterion stated",
    sieve-equals-primes: "chain the seed identification (faces = prime subsets) with the derived exactness of inversion; state what follows"
  },
  definitions: { face: "finite prime subset S",
                 g(T): "superset-sum aggregate over faces containing T",
                 f(T): "fine count at face T" },
  @verified
)
