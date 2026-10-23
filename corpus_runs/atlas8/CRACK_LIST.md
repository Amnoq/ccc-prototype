# Atlas-8 Crack List — candidate novel results

**Date:** 2026-10-07
**Question asked of every adjudicated link:** does the literature state
what the sieve side holds here? Every unstated touch is a crack
candidate. Span-priority applied throughout (gaps/intervals first).

Each crack carries four fields: the literature claim, the sieve
structure it touches, exactly what is unstated in the literature,
and its epistemic label — plus the verification verdict against
`sieve_complex.py` / `deformed_sieve.py` (read-only imports).

---

## K8-1 — PNT as total weight 1 (from A8-06) ✅ VERIFIED

- **Literature claim:** the Prime Number Theorem, π(x) ∼ x/log x,
  proved by Tauberian contour argument (Zagier/Newman, exact).
- **Sieve structure it touches:** D4 — the weighted infinite complex:
  w(S) = (−1)^{|S|+1}·log(∏S)/∏S over nonempty faces S;
  Σ_{∏S≤X} w(S) → 1.
- **What is unstated:** the literature proves PNT analytically; it
  does NOT state PNT as the combinatorial identity "total weight 1"
  on a weighted simplicial complex. The pilot marks the framing as
  appearing new (searched 2026-09-30); the underlying math is classical.
- **Epistemic label:** computationally_verified (the identity, re-checked
  here); the *framing-novelty* claim is the pilot's, marked "appears new".
- **Verification:** `verification/verify_k8_1_pnt_weight.py` —
  independent re-computation: X=1000 → 0.969931, X=5000 → 0.993342,
  X=20000 → 0.986125 (PNT-like oscillatory convergence toward 1;
  pilot: 0.999922 at 5·10⁵). Output: `k8_1_output.txt`.
- **Verdict: VERIFIED.** Candidate novel result: the face-sum
  formulation of PNT (the formulation, not the theorem).

## K8-2 — Admissible constellations as sieve output; admissibility emergent (from A8-09, A8-10, A8-12) ✅ VERIFIED

- **Literature claim:** Zhang Theorem 1 / Maynard Prop 4.2 / Theorem 1.2 —
  ADMISSIBLE tuples H are the input condition for bounded-gaps and
  positive-proportion theorems (exact).
- **Sieve structure it touches:** D6-generalized — nine admissible
  "combos" (twins, cousins, sexy, two triplet types, quad, quint, sext)
  plus the non-admissible {0,2,4} control, exhibited as deformed-sieve
  output; the admissibility obstruction emerges uninserted.
- **What is unstated:** the literature STIPULATES admissibility as an
  input hypothesis on H. It does NOT state the generative account:
  that the same constellations are produced as sieve output, and that
  the obstruction (which gap patterns are forbidden) emerges from the
  machine — e.g. {0,2,4} dies with exactly one survivor (3,5,7).
- **Epistemic label:** computationally_verified (the exhibition and the
  obstruction, re-checked here).
- **Verification:** `verification/verify_k8_2_constellations.py` —
  (a) deformed-sieve survivors ≤ 20000 are EXACTLY the 342 brute-force
  twin lowers; (b) the only prime triple (n,n+2,n+4) below 10⁵ is
  (3,5,7). Output: `k8_2_output.txt`.
- **Verdict: VERIFIED.** Candidate novel result: the generative
  (sieve-output) account of admissibility.

## K8-3 — Twin singular series as renormalized sieve weight (from A8-11) ✅ VERIFIED

- **Literature claim:** the prime k-tuples conjecture (Maynard, reframed;
  no k>1 case known); the Hardy–Littlewood twin constant 2C₂ = 1.32032…
  as the classical (1923) heuristic constant.
- **Sieve structure it touches:** D6 — the deformed sieve (R_p = {0,−2})
  DERIVES the constant as renormalized total weight:
  𝔖(z) = ∏_{p≤z}(1−|R_p|/p)/(1−1/p)² → 2C₂; the twin-density asymptotic
  itself stays explicitly UNCLAIMED (honest boundary).
- **What is unstated:** the literature states the constant as a
  heuristic; it does NOT derive it as the renormalized total weight of
  a generative sieve. The pilot: "the constant is classical (1923);
  the generative deformation move appears new."
- **Epistemic label:** computationally_verified (the derivation,
  re-checked here); the asymptotic remains conjectural by the pilot's
  own honest boundary — this crack is the *mechanism*, not the proof.
- **Verification:** `verification/verify_k8_3_singular_series.py` —
  S(7)=1.367187, S(13)=1.344116, S(100)=1.322754, S(1000)=1.320491 →
  2C₂=1.3203236. Output: `k8_3_output.txt`.
- **Verdict: VERIFIED.** Candidate novel result: the generative
  derivation of the twin singular series.

## K8-4 — The circle sieve as an independently-derived sieve (from A8-13) ✅ VERIFIED

- **Literature claim:** the classical sieve setup (Elkies: sifted set,
  multiplicative density, Eratosthenes as naive prototype; exact).
- **Sieve structure it touches:** the linear circle sieve — geometric
  shared-boundary sifting, built from first principles WITHOUT the
  literature (user's construction, 2026-09-29).
- **What is unstated:** the literature does not contain the circle sieve;
  the independence is the point — a sieve re-derived geometrically,
  then checked against the classical one. (Not a mathematical novelty
  claim about sieves in general; a provenance claim about this sieve.)
- **Epistemic label:** exact (the verification is a finite check,
  re-checked here to N=10⁴).
- **Verification:** `verification/verify_k8_4_circle_sieve.py` —
  unshared points == classical primes at N=30, 200, 2000, 10000
  (10/46/303/1229 primes, all match). Output: `k8_4_output.txt`.
- **Verdict: VERIFIED.** Candidate novel result: the circle sieve as an
  independent geometric sieve (provenance + verification, not a new
  theorem about primes).

## K8-5 — Selberg λ² as a face-native quadratic form (from A8-02…A8-05) ❓ UNDECIDABLE

- **Literature claim:** Selberg's inequality and diagonalization lemma
  (Elkies, exact); k-dimensional Selberg weights and y-diagonalization
  (Maynard, exact).
- **Sieve structure it touches:** home:sieve4 — "Selberg's lambda² sieve
  as an optimized quadratic form Q(λ) on faces" (status line promises
  exact theorem + computational verification).
- **What is unstated:** the face-native quadratic-form reframing is the
  pilot's own and appears in no literature chunk.
- **Epistemic label:** heuristic-as-extracted — the source chunk is
  TRUNCATED mid-D10c (the optimizer, the minimum, and the classical
  comparison never appear). The claim cannot be evaluated from the
  extraction.
- **Verification:** none possible — undecidable-by-this-instrument
  (truncated source). The full D10c derivation would need to be
  recovered from the program's live documents first.
- **Verdict: UNDECIDABLE.** Not a candidate until the derivation is complete.

---

## Summary

| Crack | Span-priority | Literature states it? | Label | Verification |
|---|---|---|---|---|
| K8-1 PNT as total weight 1 | — | No (framing) | computationally_verified | ✅ verified |
| K8-2 Admissibility emergent | ✅ | No (generative account) | computationally_verified | ✅ verified |
| K8-3 Twin series as sieve weight | ✅ | No (derivation) | computationally_verified | ✅ verified |
| K8-4 Circle sieve independent | — | No (provenance) | exact | ✅ verified |
| K8-5 Selberg λ² face form | — | No | heuristic (truncated) | ❓ undecidable |

**4 of 5 crack candidates verify computationally against the sieve
implementation. 0 refuted.** The four verified cracks are all of the
same shape the run was designed to find: the literature and the sieve
touch on the same objects (PNT, admissible tuples, the twin constant,
the sieve itself), and in each case the sieve holds something the
literature does not state — a framing, a generative account, a
derivation, an independent construction. None is a new theorem about
primes; each is a candidate novel result about the *structure* — which
is exactly what the user's program trades in.

**Rejected pairs (A8-07, A8-08)** produced no cracks: shared names and
shared objects without shared claims are not touches.

**Misses (M8-1…M8-5)** are absences, not cracks: Cramér's conjecture,
Green–Tao APs, the Cramér urn model, the parity barrier (home-only),
and level of distribution have no counterpart on the other side.
