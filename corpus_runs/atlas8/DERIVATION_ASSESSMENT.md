# Derivation assessment — what is novel as a derivation

**Date:** 2026-10-07
**Request:** the user's correction — "not modifications, derivations":
look over the Atlas-8 material and inventory what is novel *as a
derivation*.
**Sources read:** CRACK_LIST.md (all 5 cracks), DERIVATIONS.md
(D1–D10e, Node 14), FRAMEWORK_WHOLE_VIEW_2026-10-05.md (D6,
D6-generalized), the four verification scripts + outputs.

## Standing distinction

Across every item below, the novelty is in the DERIVATION (how the
result is gotten — generatively, from the machine, nothing inserted
by hand), never in the destination (PNT, the twin constant,
admissibility — all classical). That is exactly the program's coin.
Each entry carries the pilot's own honest label where one exists.

## Inventory, ranked by derivation-novelty

### 1. D6-generalized — admissibility derived, not stipulated (STRONGEST)

- **What the literature does:** Zhang Theorem 1 / Maynard Prop 4.2
  STIPULATE admissibility of H as an input hypothesis.
- **What the sieve does:** deform the marking rule per constellation
  H; the deformed sieve's survivors ARE the constellation prime
  lowers (verified: 8169=8169 twins, sext 5=5 at 10⁶; finite-z
  densities match δ_H to 0.998–1.015); the non-admissible {0,2,4}
  DIES with exactly one survivor (3,5,7), 𝔖_H(z)=0 for z≥3.
- **The derivation:** the admissibility obstruction emerges from
  the machine, uninserted. Exact algebraic core (deformed
  μ-identity: S(x,z) = Σ μ(d)·E_d(x), verified exact) +
  computational verification of the emergence.
- **Label:** computationally_verified; "predictive test passed."
- **What would upgrade it:** a proof (not just computation) that
  H admissible ⟺ the deformed sieve has survivors — the exact
  core already suggests the shape.

### 2. D6 — the twin singular series as renormalized total weight

- **What the literature does:** states 2C₂ = 1.32032… as the
  classical (1923) heuristic constant.
- **What the sieve does:** δ(z) = ∏(1−|R_p|/p) factors as
  [∏(1−1/p)²]·𝔖(z); the first factor → 0 (Mertens), the second
  converges to 2C₂ — the constant falls out as the renormalized
  total weight of the deformed incidence complex. Verified:
  1.367187 → 1.320491 at z = 7…1000.
- **The derivation:** the constant is derived, never inserted.
  Pilot: "the constant is classical (1923); the generative
  deformation move appears new" (searched 2026-09-30).
- **Label:** computationally_verified (the derivation); the
  twin-prime asymptotic itself stays explicitly UNCLAIMED —
  honest boundary, the crack is the mechanism, not the proof.

### 3. D4 — PNT as total weight 1

- **What the literature does:** proves π(x) ∼ x/log x by Tauberian
  contour argument.
- **What the sieve does:** w(S) = (−1)^{|S|+1}·log(∏S)/∏S;
  Σ_{∏S≤X} w(S) → 1 ⟺ PNT. Verified: 0.969931 → 0.999922 at
  X = 10³…5·10⁵.
- **The derivation:** the pilot's own label — "Statement
  (classical, reframed)." Underneath is Möbius inversion in
  face-sum language.
- **Label:** computationally_verified (the identity); framing
  novel, math classical. Value is architectural: PNT now lives
  inside the sieve's native objects, which is what enables D6.

### 4. D1 / D2 / D5 — classical results, reframed (pilot's labels)

- D1: ψ(x) as signed face-sum — "Classical theorem (Möbius
  inversion), reframed."
- D2: Lehmer's recursion as the link recursion — "Classical
  (Lehmer 1959 prime-counting), reframed."
- D5: territory removal as soft-limit splitting — "A conceptual
  identification, not a new theorem" (D2's recursion read
  through Figueiredo's lens).
- D3: binary-geometry reformulation — "not new prime information."

### Not a derivation

- K8-4 (circle sieve independence): a provenance claim, verified
  by finite check — not a derivation of anything.

## Bottom line

Three novel derivations (D6-generalized, D6, D4-as-framing), each
verified computationally, each honest about the classical
destination. The pattern is the program's thesis in miniature:
the literature proves or stipulates; the sieve *generates* — and
the generated form is what was missing. None is a new theorem
about primes; all are new derivations *of* prime-distribution
facts, which is the currency the program trades in.

## Documentation

Expanded into program documentation at
`~/workspace/prime-sieve-geometry/NOVEL_DERIVATIONS.md`
(2026-10-07): ND-1 admissibility, ND-2 twin constant, ND-3 PNT —
each with the sieve's derivation, the literature's form, exactly
what is novel, the epistemic label, sources, and upgrade paths.
