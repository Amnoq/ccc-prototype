# PERTURB triples v2.1 — round 3 (wider inventory)

Fixed 2026-10-03, under PERTURB_SPEC_V2_1. Generative/definitional
content only: no numerical conclusion values, no theorem statements.
Pre-registered predictions (testing the law's predictive power):
T4 GOOD, T5 GOOD, T6 MIXED, T7 MIXED, T8 GOOD-ish, T9 MIXED,
T1-mu retest predicted REGENERATED under the tightened prescription.

## T4/E025 — link recursion
PERTURB(
  seed: { domain: "phi(x,a) = count of integers <=x with no prime factor <= p_a (p_a = a-th prime); phi(x,0)=floor(x)",
          shape: "integer counts per (x,a)",
          aggregation: "n/a" },
  binary-op: { rule: "recursion: phi(x,a) = phi(x,a-1) - phi(x/p_a, a-1); combinatorial reading: split off the p_a-divisible class (binary: divisible by p_a or not)",
               polarity: "n/a (recursion, not marking)",
               conventions: ["p_a = a-th prime", "phi(x,0)=floor(x)"] },
  axis: { order: "a = 1,2,3,...", extent: "finite(a)" },
  derive: ["recursion unfolding"],
  asserted: [],
  observe: {
    recursion-statement: "restate binary-op",
    link-identification: "prescription: show the count recursion is the shadow of the link operation — removing vertex p_a splits faces into those containing p_a and those not, giving the two terms",
    face-counts-match: "criterion: link-recursion counts vs direct face counts; VERIFY-BY-DATA — no dataset in triple, mark UNVERIFIED with criterion stated"
  },
  definitions: { "link({p})": "subcomplex of faces not using vertex p",
                 "phi(x,a)": "as in seed domain" },
  @exact-recursion
)

## T5/E004 — Lambda = mu*log dictionary
PERTURB(
  seed: { domain: "arithmetic functions on n>=1: mu (Moebius, values -1/0/1), log",
          shape: "sign structure +-1 on squarefree support; divisor lattice",
          aggregation: "Dirichlet convolution: (f*g)(n) = sum_{d|n} f(d) g(n/d)" },
  binary-op: { rule: "Moebius inversion step: Lambda = mu * log, i.e. Lambda(n) = sum_{d|n} mu(d) log(n/d)",
               polarity: "n/a (transform)",
               conventions: [] },
  axis: { order: "single transform step; n increasing for verification", extent: "finite(N)" },
  derive: ["Moebius inversion on the divisor lattice (textbook)",
           "log n = sum_{d|n} Lambda(d) (textbook, from unique factorization)"],
  asserted: [],
  observe: {
    dictionary-statement: "restate: Lambda = mu*log; Lambda is one Dirichlet convolution from mu",
    structural-derivation: "prescription: derive Lambda = mu*log by applying divisor-lattice Moebius inversion to the textbook identity log n = sum_{d|n} Lambda(d)",
    numerical-check: "prescription: compute Lambda(n) via the convolution for n<5000 and compare against direct von Mangoldt (log p if n = p^k else 0); report max absolute error"
  },
  definitions: { "Lambda": "von Mangoldt function", "mu": "Moebius function", "*": "Dirichlet convolution" },
  @verified
)

## T6/E014 — face-weights definition
PERTURB(
  seed: { domain: "subsets S of primes <= z",
          shape: "binary: subset in/out",
          aggregation: "weighted sums over subsets" },
  binary-op: { rule: "assign weight w(S) = (-1)^{|S|+1} log(prod S) / prod S",
               polarity: "n/a (assignment)",
               conventions: [] },
  axis: { order: "z increasing", extent: "finite(z)" },
  derive: ["Dirichlet series of subset sums via Euler products (textbook)"],
  asserted: [],
  observe: {
    weight-definition: "restate w(S)",
    sign-alternation: "prescription: read off the (-1)^{|S|+1} factor — state how weights alternate with |S|",
    dirichlet-gf: "prescription: form the Dirichlet series sum_S w(S)*(prod S)^{-s} as an Euler product over p; identify the closed form via derive[0]; report exactly what you get",
    sum-limit: "prescription: compute partial sums S(X) = sum_{prod S <= X} w(S) for X in {1e3, 1e4, 1e5}; report values and trend"
  },
  definitions: { "w(S)": "(-1)^{|S|+1} log(prod S)/prod S", "prod S": "product of primes in S" },
  @definition
)

## T7/E050 — explicit-formula verification procedure
PERTURB(
  seed: { domain: "nontrivial zeros rho = 1/2 + i*gamma of zeta, as data (list ordered by height)",
          shape: "ordered list",
          aggregation: "n/a" },
  binary-op: { rule: "truncated explicit-formula sum at height T: psi_T(x) = x - sum_{|gamma|<=T} x^rho/rho - log(2*pi) - (1/2)log(1-x^{-2}); error E(T) = |psi_T(x) - psi(x)| at fixed x",
               polarity: "n/a (computation)",
               conventions: ["x fixed; decoder chooses a moderate x and states it", "principal terms only"] },
  axis: { order: "T increasing", extent: "finite(T)" },
  derive: ["explicit-formula truncation error bounds (textbook)"],
  asserted: [],
  observe: {
    procedure-statement: "restate the computation",
    error-decay-shape: "prescription: from the formula's tail, derive qualitatively how E(T) behaves as T grows (via derive[0]); no numbers required",
    error-values: "criterion: compute E(T) for T in {50, 400} and compare; VERIFY-BY-DATA — zero list not in triple, mark UNVERIFIED with criterion stated"
  },
  definitions: { "psi_T(x)": "truncated sum per binary-op", "E(T)": "absolute error at fixed x" },
  @verified
)

## T8/E015 — PNT reframed as total weight 1
PERTURB(
  seed: { domain: "subsets S of primes (equivalently squarefree n)",
          shape: "binary in/out",
          aggregation: "weighted sum" },
  binary-op: { rule: "w(S) = (-1)^{|S|+1} log(prod S)/prod S  [definition included for self-containment]",
               polarity: "n/a (assignment + summation)",
               conventions: [] },
  axis: { order: "X increasing; sum over prod S <= X", extent: "finite(X)" },
  derive: ["partial summation / Dirichlet series (textbook)",
           "Tauberian theorems (textbook, if applicable)"],
  asserted: [],
  observe: {
    reframing-statement: "restate: total weight S(X) -> 1",
    partial-sums: "prescription: compute S(X) = sum_{prod S <= X} w(S) for X in {1e3, 1e4, 1e5}; report values and trend",
    pnt-equivalence: "prescription: relate S(X) -> 1 to the prime number theorem via derive[0..1]; state the chain explicitly, or mark DRIFT with the exact gap"
  },
  definitions: { "w(S)": "as in binary-op", "S(X)": "partial sum over prod S <= X" },
  @reframing
)

## T9/E071 — Selberg quadratic form on Delta_z
PERTURB(
  seed: { domain: "Selberg sieve weights lambda_d on squarefree d <= z (z small)",
          shape: "real vector indexed by d",
          aggregation: "quadratic form" },
  binary-op: { rule: "assemble the Selberg quadratic form Q on the Delta_z complex from the weights; Cholesky-factorize; report definiteness and eigenvalues",
               polarity: "n/a (construction + factorization)",
               conventions: ["z <= 19 (small cases only)"] },
  axis: { order: "z over small cases", extent: "finite" },
  derive: ["Cholesky factorization / positive-definiteness criteria (textbook)"],
  asserted: [],
  observe: {
    construction-description: "describe the procedure: weights -> Gram matrix -> Cholesky",
    pd-verification: "criterion: Cholesky succeeds with all eigenvalues > 0 for z <= 19; VERIFY-BY-DATA — corpus weight definitions not in triple, mark UNVERIFIED with criterion stated (note what would be needed)"
  },
  definitions: { "Q": "Selberg quadratic form", "lambda_d": "sieve weights (corpus-optimized; definitions not in triple)" },
  @executed-small-cases
)

## T1-mu retest (v2.1 tightened prescription)
Same T1 v2 triple as in PERTURB_TRIPLES_V2.md, except the mu-identity
observable prescription is replaced by the functional-role form (spec
v2.1 change (c)):
  mu-identity: "prescription: derive an exact equation expressing the unmarked count U(X,z) solely through the R_p sets and their moduli (no unevaluated remainders); the standard name for such an equation in this mechanism is 'mu-identity'. State the equation explicitly. Log any residual imprecision (e.g. equivalence to a mu-factored form not shown) as a precision note, not a gap."
Decode ONLY this observable (the rest of T1 stands as scored in round 2).
