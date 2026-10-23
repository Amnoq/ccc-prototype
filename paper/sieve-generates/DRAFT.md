# The Sieve Generates: Novel Derivations of Prime-Distribution Facts from a Relational Sieve

**Author:** [NEEDS SOURCE: author name as the user wishes it to appear]
**Date:** 2026-10-08 (draft v0.1)
**Epistemic status of this document:** draft for the router's review.
Every factual claim below carries an epistemic label in brackets:
[exact] = proved; [computationally verified] = computed live and
rerunnable, with controls; [conjectural] = precise but unproved;
[heuristic] = suggestive, not precise; [appears new] = a bounded
pilot literature search found no prior statement — not an absolute
novelty claim.

---

## Abstract

We present three results of the same shape, produced by an
independently constructed geometric sieve ("the circle sieve"):
each reaches a *classical* destination in prime distribution by a
*generative* path — one the sieve computes rather than one the
literature states. (1) Admissibility of prime constellations,
stipulated as a hypothesis in the bounded-gaps literature
(Zhang; Maynard), emerges as a computed property of the sieve's
output: inadmissible patterns die with no survivors, exactly as
predicted, while nine admissible patterns yield exactly the
enumerated prime-tuple counts [computationally verified]. (2) The
Hardy–Littlewood twin-prime constant 2C₂ falls out as the
renormalized total weight of a deformed incidence complex —
never inserted, converging to 1.32032… [computationally verified].
(3) The Prime Number Theorem is restated as the combinatorial
identity "total weight 1" on the sieve's weighted complex, with
the zeta zeros entering as regulators of the infinite sum
[framing novel; mathematics classical]. None of these is a new
theorem about primes; each is a new *derivation* of a
prime-distribution fact, found by an atlas-style literature
comparison and verified against rerunnable sieve code. The
twin-prime asymptotic itself is explicitly unclaimed.

---

## 1. Introduction

The sieve never tests for primality. It maps every composite as a
first-class discovery showing everything that went into making it,
and what remains relating only to zero is prime. That single design
fact — nothing inserted by hand — is the thesis of this paper,
pursued to three classical destinations.

The *circle sieve* is a geometric sieve built from first
principles in September 2026: points on a line (or circle) are
marked when they share a residue-class boundary with a prime's
territory; unshared points are the primes. The construction is
independent of the classical literature (provenance documented in
§2; agreement with the classical sieve checked to 10⁴). Its native
mathematical object is an *incidence complex*: faces S are finite
sets of primes, and the sieve's state is a weighted sum over
faces. From this one object, deformed in controlled ways, the
paper derives three classical facts generatively:

- **ND-1 (§4).** Admissibility — stipulated as an input hypothesis
  in Zhang's and Maynard's theorems — is *computed*: the deformed
  sieve's survivors exhibit it. [computationally verified]
- **ND-2 (§5).** The twin singular series 2C₂ is *derived* as the
  renormalized total weight of the deformed complex.
  [computationally verified]
- **ND-3 (§6).** The Prime Number Theorem is *restated* as total
  weight 1 on the weighted complex. [framing novel; classical]

The standing distinction, held throughout: the *destinations* are
classical; the *paths* are the contribution. The paper also
documents exactly where the derivations stop — the twin-prime
asymptotic is unclaimed (§7), and the upgrade paths are stated
openly (§9).

---

## 2. The circle sieve and its incidence complex

### 2.1 The sieve

Fix a bound x. For each prime p, define a marking rule: n is
*marked* at p if n mod p lies in a prescribed residue set
R_p ⊆ **Z**/p**Z**. A point n ≤ x is a *survivor* if it is marked
by no prime. In the undeformed (classical) sieve, R_p = {0} for
all p: the survivors are exactly the primes ≤ x [exact — verified
by finite check to N = 10⁴ against an independent primality
sieve; see K8-4 below].

The geometry: each prime owns "territory" (its residue classes);
a composite has no identity except as an overlap of prime
territories, and a prime is a point sharing no boundary with any
earlier prime's territory. The marking rule is the algebra; the
territories are the picture.

### 2.2 The incidence complex

The sieve's native object is the simplicial complex Δ_x whose
faces S are finite sets of distinct primes with ∏S ≤ x. The
z-sieve count S(x, z) = #{n ≤ x : n unmarked by all p ≤ z}
satisfies the *μ-identity*

    S(x,z) = Σ_{d|P(z)} μ(d)·E_d(x),                     (1)

where P(z) = ∏_{p≤z} p and E_d(x) is the exact count of n ≤ x
lying in the marked residue classes modulo d — computed by the
Chinese Remainder Theorem [exact — this is inclusion–exclusion
over CRT classes; the implementation's exactness was confirmed
computationally at (z,x) = (13, 50000) and (30, 200000)].

### 2.3 Provenance (K8-4)

The circle sieve was constructed geometrically, from first
principles, without the sieve literature — then checked against
the classical Eratosthenes sieve: unshared points coincide with
classical primes at N = 30, 200, 2000, 10000 (10/46/303/1229
primes, all matching) [exact — a finite check, rerunnable:
`verification/verify_k8_4_circle_sieve.py`]. This is a
*provenance* claim about the construction, not a mathematical
novelty claim about sieves in general: the independence is the
point, because every derivation below runs on the sieve's own
machinery, with nothing about primes inserted by hand.

---

## 3. Method: how Atlas-8 found the cracks

The three derivations were not the pilot's starting point. They
surfaced through an *atlas* run (Atlas-8, 2026-10-07) comparing
two bodies of knowledge: six landmark prime-distribution papers
(Zagier, Granville, Zhang, Maynard, Green–Tao, Elkies; 212
foreign concepts) against the circle-sieve program's own
documents (133 home concepts, including 39 span/interval nodes).
Procedure: blind extraction (each side drafted without seeing the
other's vocabulary), reviewed merge (345 concepts post-merge),
and adjudication of 13 candidate cross-sky links: 11 split-links,
2 rejected, 0 false merges, 0 contradictions; the seeded
positive control resolved [methodology documented in
`corpus_runs/atlas8/ATLAS8_REPORT.md`].

The crack-hunting question, asked of every adjudicated link:
*does the literature state what the sieve side holds here?*
Every unstated touch became a crack candidate; each was then
verified computationally against the read-only sieve
implementation. Result: 4 of 5 candidates verified, 0 refuted, 1
honestly undecidable (K8-5, truncated source). The four verified
cracks are the same shape: literature and sieve touch on the
same object, and the sieve holds something the literature does
not state. ND-1, ND-2, ND-3 below are K8-2, K8-3, K8-1 in
derivation-novelty order; K8-4 is §2.3 above.

---

## 4. ND-1. Admissibility derived as sieve output

**Epistemic label:** [computationally verified]. Strongest of the
three derivations.

### 4.1 The literature's form

Zhang (Theorem 1) and Maynard (Prop. 4.2 / Theorem 1.2) prove
bounded gaps and positive proportions for prime constellations.
Both *stipulate* as an input hypothesis that the tuple
H = {h_1, …, h_k} be *admissible*: H does not cover all residue
classes modulo any prime p. Admissibility is checked by hand
before the theorem runs.

### 4.2 The sieve's derivation

Deform the marking rule per constellation H:

    R_p = { −h mod p : h ∈ H }.                            (2)

Now n is marked if n mod p ∈ R_p for some p — i.e., if p
divides some n + h_i. The survivors of the deformed sieve are
exactly the n for which all n + h_i are prime: the constellation
prime lowers. Nothing about admissibility is hypothesized.

**Theorem (the obstruction, exact).** If H is inadmissible —
some prime p covers every residue class mod p through H — then
the deformed sieve has no survivors.

*Proof.* If H covers all residues mod p, then for every n there
is h ∈ H with n ≡ −h (mod p), i.e. n mod p ∈ R_p; every n is
marked at p. ∎

The converse — H admissible ⟹ the deformed sieve has survivors
past the finite-z threshold — is the computational half:

- Nine constellations (twins, cousins, sexy, two triplet types,
  quad, quint, sext) at x = 10⁶: deformed-sieve survivors match
  independently enumerated constellation lowers exactly
  (twins 8169 = 8169; sext 5 = 5) [computationally verified].
- Finite-z densities match the constellation density δ_H to
  0.998–1.015; the finite singular series 𝔖_H(1000) matches the
  reference singular series to ~0.2% [computationally verified].
- The non-admissible control {0, 2, 4} *dies as the machine
  predicts*: exactly one survivor, (3, 5, 7); 𝔖_H(z) = 0 for
  z ≥ 3 [computationally verified — the vanishing is exact:
  at p = 3, |R_3| = 3, so the local factor (1 − 3/3) is 0].

**Exact algebraic core.** The static z-sieve satisfies the
deformed μ-identity (1) with E_d the exact CRT residue-class
counts. Faces of the deformed complex carry multiplicities
m(S) = ∏_{p∈S} |R_p| — the number of forbidden CRT classes
[exact, by the CRT].

### 4.3 What is novel

The admissibility *condition* is classical (a covering-set
observation). What is novel — and strongest here — is the
*derivation*: the condition emerges as a property of the
machine's output rather than being stipulated as a hypothesis.
The literature checks admissibility by hand before running the
theorem; here the sieve runs first, and admissibility is what
the survivors exhibit.

### 4.4 What would upgrade it

A proof (not only computation) of the converse: H admissible
⟺ the deformed sieve has survivors past the finite-z
threshold. The exact μ-identity core already suggests the shape;
the emergence half is currently computational. Rerunnable:
`verification/verify_k8_2_constellations.py`.

---

## 5. ND-2. The twin singular series as renormalized total weight

**Epistemic label:** [computationally verified] (the derivation).
The twin-prime asymptotic itself is explicitly UNCLAIMED (§7).

### 5.1 The literature's form

Hardy–Littlewood (1923): the twin-prime heuristic constant

    2C₂ = 2·∏_{p>2}(1 − 1/(p−1)²) = 1.3203236…,

stated as a constant; the asymptotic π₂(x) ~ 2C₂·x/(log x)² is
conjectural — no k > 1 case of prime k-tuples is known.

### 5.2 The sieve's derivation

Deform R_p = {0} (p = 2), {0, −2} (p odd): n is marked if p | n
or p | (n+2). **The deformation separates markers from
survivors**: in the classic sieve the markers and the survivors
coincide (primes); here the markers are the primes but the
survivors are a different set — the generative deformed sieve's
survivors ≤ 200000 are exactly the 2160 twin-prime lowers,
checked against an independent sieve [computationally verified].

Faces carry multiplicities m(S) = ∏_{p∈S}|R_p|; the finite total
weight is exactly

    δ(z) = ∏_{p≤z}(1 − |R_p|/p),   S(x,z)/x → δ(z)         (3)

[exact identities; the limit verified numerically: 0.071430 vs
0.071429 at z = 7, x = 200000]. Renormalize by the prime
baseline:

    δ(z) = [∏_{p≤z}(1 − 1/p)²] · 𝔖(z),
    𝔖(z) = ∏_{p≤z}(1 − |R_p|/p)/(1 − 1/p)².                (4)

The first factor → 0 (Mertens) [exact, classical]; the second
converges [exact, classical analysis]:

    𝔖(z) → 2C₂ = 1.32032…

verified: 1.367187, 1.344116, 1.330277, 1.322754 at
z = 7, 13, 30, 100; Atlas-8 re-check 𝔖(1000) = 1.320491
[computationally verified]. The constant comes *out of the
deformation* — never inserted.

### 5.3 What is novel

The constant is classical (1923). What is novel is the
generative path: the singular series derived as the renormalized
total weight of a deformed incidence complex, via the exact
deformed μ-identity. A bounded pilot literature search
(2026-09-30) found no prior statement of this generative
derivation [appears new].

### 5.4 Honest boundary

The passage 𝔖(z) → π₂(x) ~ 𝔖·x/(log x)² is the *unproven* twin
prime conjecture (numerical ratio 1.6091 at 2·10⁵ — slow
convergence, as expected). Verified: the algebra (local factors
assemble to 𝔖). Not claimed: the conjecture. This derivation is
the *mechanism*, not the proof. Rerunnable:
`verification/verify_k8_3_singular_series.py`.

---

## 6. ND-3. PNT as total weight 1 on the weighted complex

**Epistemic label:** [computationally verified] (the identity).
Framing novel; the underlying mathematics classical.

### 6.1 The literature's form

The Prime Number Theorem: π(x) ~ x/log x (equivalently
ψ(x) ~ x), proved by Tauberian contour argument (Hadamard /
de la Vallée Poussin; modern expositions e.g. Zagier/Newman).

### 6.2 The sieve's derivation

Give each nonempty face S of the incidence complex the
x-independent weight

    w(S) = (−1)^{|S|+1} · log(∏S) / ∏S.                    (5)

Then D1 reads ψ(x)/x = Σ_{∏S≤x} w(S)·(⌊x/∏S⌋/(x/∏S)) — the floor
a cutoff tending to 1 — and:

**Statement (classical, reframed).** Σ_{∏S≤X} w(S) → 1 as
X → ∞: the weighted infinite simplex has total weight 1. This
identity is equivalent to the Prime Number Theorem.

*On the equivalence.* Writing n = ∏S over squarefree n,
(−1)^{|S|+1} = −μ(n), so Σ_S w(S) = Σ_{n≤X} −μ(n)(log n)/n,
and Σ_{n≤X} μ(n)(log n)/n → −1 is a classical equivalent of
PNT [classical — standard analytic number theory; [NEEDS
SOURCE: cite a standard PNT-equivalents reference, e.g.
Landau or a modern text]]. The equivalence is classical; the
face-sum formulation on the sieve's complex is the reframing.

Verified numerically (Möbius sieve to 2·10⁶): partial sums
0.969931, 1.019210, 1.005585, 0.999922, 0.997215, 1.001658 at
X = 10³, 10⁴, 10⁵, 5·10⁵, 10⁶, 2·10⁶ — PNT-like oscillatory
convergence to 1 [computationally verified]. Rerunnable:
`verification/verify_k8_1_pnt_weight.py`.

**The zeros enter as regulators.** The Dirichlet generating
function of the weights is

    Σ_S w(S)/∏S^{s−1} = −ζ′(s)/ζ(s)²,                     (6)

verified numerically against ζ′/ζ² to ~4 digits at
s = 1.01…1.20 [computationally verified; the identity itself is
classical]. The *rate* at which the face-sum → 1 — the error in
the partial sums — is governed by the zeros of ζ via the
explicit formula [classical]: the zeros enter as *regulators*
of the infinite sum.

### 6.3 What is novel

Underneath, this is Möbius inversion in face-sum language —
classical mathematics, and the pilot labels it so: "Statement
(classical, reframed)." What is novel is the framing: PNT stated
as a property *of the sieve's native object* (the weighted
complex), with the zeta zeros cast as regulators of its
convergence. That framing is what makes the D6 deformation
formulable at all — the architecture's value, not a new proof.

---

## 7. What is not claimed

This section is load-bearing, not decorative. The paper claims
none of the following:

1. **No new theorem about primes.** Every destination (PNT, the
   twin constant, admissibility) is classical. The contribution
   is the generative path in each case.
2. **The twin-prime asymptotic is explicitly unclaimed.** ND-2
   derives the singular series; the passage to
   π₂(x) ~ 2C₂·x/(log x)² is the unproven conjecture.
3. **ND-1's converse is computational, not proved.** Inadmissible
   ⟹ no survivors is exact (trivial); admissible ⟹ survivors
   is verified to 10⁶, not proved. §4.4 states the upgrade.
4. **K8-5 (Selberg λ² as a face-native quadratic form) is
   undecidable by this instrument** — the source chunk is
   truncated mid-derivation; it is not a candidate until the
   derivation is complete.
5. **Novelty claims are bounded.** "Appears new" means a pilot
   literature search (2026-09-30) found no prior statement —
   not an exhaustive survey. The framing-novelty claim for ND-3
   is the pilot's, marked as such.

---

## 8. Honest limits

1. **Finite computation.** All "verified" labels rest on finite
   runs (x ≤ 10⁶ for constellations, ≤ 2·10⁵ for twins,
   X ≤ 2·10⁶ for the face-sum, z ≤ 1000 for 𝔖(z)). Nothing is
   claimed beyond the computed ranges except where exact
   identities (the μ-identity, CRT multiplicities, the covering
   argument) carry the weight — and those are labeled exact.
2. **One instrument's view.** The derivations were found by
   comparing the literature against the program's own sieve;
   the "unstated in the literature" judgments rest on the six
   landmark papers plus the pilot's searches, not the whole
   literature.
3. **Provenance, not priority.** K8-4 documents that the circle
   sieve was built independently; it does not claim the
   geometric sieve idea is new to mathematics.
4. **The atlas is a finder, not a prover.** Atlas-8 surfaced the
   cracks and verified them computationally; turning ND-1's
   computational converse into a theorem is further work (§4.4).
5. **Author.** [NEEDS SOURCE: the user's preferred author name
   and affiliation line.]

---

## 9. Upgrade paths and conclusion

Each derivation states its own upgrade (§4.4, §5.4, §6.2), in
increasing difficulty:

1. **ND-1 → proof.** Prove admissible H ⟺ the deformed sieve
   has survivors past the finite-z threshold. The exact
   μ-identity core suggests the shape; this is the sharpest
   open item in the paper.
2. **ND-2 → the analytic bridge.** The derivation is the
   mechanism; the twin-prime asymptotic remains the unproven
   conjecture. The generated singular series is now available
   as a native object of the sieve for that attack.
3. **ND-3 → the zeros.** The face-sum formulation casts the
   zeta zeros as regulators of the sieve's own convergence —
   the natural language for asking what the sieve would need
   to *derive* them.

The pattern across all three is the program's thesis in
miniature: the literature proves or stipulates; the sieve
*generates* — and the generated form is what was missing.
Nothing was put in by hand — primality is never tested by a
predicate, admissibility is never stipulated, the constant is
never inserted. What remains, after the machine runs, is the
derivation.

---

## References

[NEEDS SOURCE: full bibliography to be assembled — Zhang (2014),
Maynard (2015/2016), Hardy–Littlewood (1923), Hadamard (1896),
de la Vallée Poussin (1896), Elkies (sieve notes), Granville,
Zagier, Green–Tao, plus the program documents:
FRAMEWORK_WHOLE_VIEW_2026-10-05.md, DERIVATIONS.md (D1–D10e),
NOVEL_DERIVATIONS.md, and the Atlas-8 records
(corpus_runs/atlas8/: ATLAS8_REPORT.md, CRACK_LIST.md,
DERIVATION_ASSESSMENT.md, grading_packet.md, verification/).]

---

*Draft v0.1 — written 2026-10-08 for the router's review. Code:
prime-sieve-geometry/{sieve_complex.py, deformed_sieve.py,
ktuple_deformation.py}; verification rerunnable at
ccc-prototype/corpus_runs/atlas8/verification/.*
