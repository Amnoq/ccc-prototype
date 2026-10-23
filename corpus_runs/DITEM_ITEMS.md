# D-item encodings — round 4 (fidelity of the D-item syntax)

Terse M1 form per DITEM_SPEC.md. Adapted from the paperwork's D6, D4, D1.
Generates stages carry prescriptions only; Verified carries checksums.

## D-T1. Deformation: the singular series as renormalized total weight
Rule: p marks residues R_p = {0} (p=2), {0,−2} (p odd); i.e. n marked if p|n or p|(n+2). (code: deformed_sieve.py)
  conventions: [p marks only n>p; polarity mark=remove; primes in order, finite z; scope X=200000]
Generates:
  1. markers-vs-survivors split: unmarked n at axis end; characterize structurally (no p|n and no p|(n+2))
  2. exact identities: mu-identity for unmarked counts via inclusion-exclusion over the marking rule (state as equation); m(S)=∏|R_p|; δ(z)=∏(1−|R_p|/p) via CRT independence
  3. singular series: renormalize δ(z) ÷∏_{p≤z}(1−1/p)² → 𝔖(z); take z→∞; compute limit; identify the constant
Verified:
  - survivors ≤X: 2160 twin lowers (check: run marking, count, compare)
  - mu-identity: exact at (z,x)=(13,50000) and (30,200000) (check: both sides by code)
  - 𝔖(z): 1.367187, 1.344116, 1.330277, 1.322754 at z=7,13,30,100; limit 1.32032 (check: recompute)
Honest boundary: we verify the algebra (local factors assemble to 𝔖); the passage to π₂(x) ~ 𝔖·x/(log x)² is the unproven twin prime conjecture — NOT derived here. Do not present the asymptotic as established.
Honest label: derived (rule→series) + computationally verified; beyond-boundary is conjectural.

## D-T8. Weighted infinite complex: PNT as total weight 1
Rule: w(S) = (−1)^{|S|+1}·log(∏S)/∏S for nonempty prime subsets S. (code: face_weights.py)
  conventions: [sums over ∏S ≤ X; S ranges over prime subsets]
Generates:
  1. Dirichlet GF: form Σ_S w(S)·(∏S)^{−s} as Euler product; identify closed form (derive, don't quote)
  2. total weight: S(X) = Σ_{∏S≤X} w(S); trend as X grows (compute)
  3. PNT link: express ψ(X)/X via the weights (Stirling/partial summation); exhibit S(X) as the constant term
Verified:
  - GF closed form (check: derive + code-check at s=1)
  - S(X): 0.969931, 1.019210, 1.005585 at X=10³,10⁴,10⁵, trending to 1 (check: recompute)
Honest boundary: reframes PNT, does not reprove it; the full S(X)→1 ⟺ PNT equivalence needs decay-rate control not derived here. Do not present as a PNT proof.
Honest label: derived (weights→GF) + computationally verified; equivalence is reframing.

## D-T2. Sieve counts via face-sum Möbius inversion
Rule: faces = finite prime subsets S; inversion f(T) = Σ_{S⊇T} (−1)^{|S|−|T|} g(S) for superset-sum aggregates g(T)=Σ_{S⊇T}f(S). (code: sieve_complex.py)
  conventions: [aggregation is superset-sums; finite Boolean lattice; polarity n/a (transform)]
Generates:
  1. inversion: recover fine counts f from aggregates g (apply rule; demo exactness on a small case by code)
  2. prime identification: faces = prime subsets (seed) + exact inversion → recovered structure is prime data (state conditionally)
Verified:
  - inversion exact on small cases (check: code demo)
  - [pending data: link-face counts from face dataset vs direct integer counts — criterion: compute both, compare]
Honest boundary: the inversion is exact given correct aggregates; the empirical full-scale count-match is a data verification, not derived here. Do not present it as established.
Honest label: exact (method) + computationally verified (small cases); full-data match pending data.
