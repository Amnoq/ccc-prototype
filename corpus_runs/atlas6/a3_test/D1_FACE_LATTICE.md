# D1 face-lattice test — informative version of the A3 Item-1 check

**Date:** 2026-10-09. **Status:** pre-registered prediction recorded below; computation not yet run.
**Analyst:** subagent (parent: main agent). Atlas records read-only throughout.

## 0. Context

The A3 Item-1 PASS ("inputs non-circular") was downgraded by the reviewer to
"inputs non-circular, low-information": divisibility is the entire
multiplicative structure of the integers, so recomputing Λ from it tests a
Möbius identity, not a finding about A3. This test runs the informative
version on the ACTUAL D1 object: the truncated sieve whose faces are indexed
by squarefree integers composed of primes p ≤ z (pilot's D1 face-sum,
`prime-sieve-geometry/DERIVATIONS.md` §D1).

## 1. PRE-REGISTERED PREDICTION (recorded BEFORE computation)

Truncating the face lattice at p ≤ z leaves a tail dominated by the smallest
missing faces (d ≈ p, p the smallest prime > z), each carrying the Gaussian
factor g(log(dm)) = C_a·e^{−(log dm)²/(4a)}. Hence, up to polynomial
prefactors in log z:

    |E(z)| = |W(h_a; z) − W(h_a)|  ~  e^{−(log z)²/(4a)}.

Falsifiable consequences:

- **P1 (scaling):** log|E(z)| ≈ −(log z)²/(4a) + O(log log z) across the
  tested z. If the measured curve does not follow the Gaussian-in-log-z
  scaling, report the discrepancy rather than smoothing it over.

- **P2 (hard-regime threshold):** W(h_a) ≈ 2e^{−aγ₁²} (γ₁ ≈ 14.1347) is tiny
  at large a, with pole and prime terms cancelling almost exactly. Certifying
  W > 0 numerically needs the tail below the signal:
  (log z)²/(4a) ≳ aγ₁², i.e. **log z ≳ 2aγ₁**. At a = 0.5 this is
  log z ≳ 14.13, i.e. **z ≳ 1.4×10⁶ before prefactors** — far beyond feasible
  z (≤ 3000, log z ≤ 8.0). So the a = 0.5 error curve MUST NOT cross below
  W_ref over the tested range; if it does, something is off.

- **P3 (easy regimes):** at a = 0.1 the threshold is log z ≳ 2·0.1·γ₁ ≈ 2.83
  (z ≳ 17); at a = 0.02 it is log z ≳ 0.57 (z ≳ 1.8). So a = 0.02 should be
  essentially exact already at z = 30, and a = 0.1 should converge by
  z ~ 100. If not, report the discrepancy.

## 2. Interpretive frame (stated up front)

The face lattice's size is set by the first zero: the finite lattice
determines W only to the accuracy at which z resolves γ₁. The lattice can't
see the zeros without already being large enough to encode them. That is the
circularity in its quantitative form — and it is what makes the PARTIAL
grade informative rather than vacuous.

## 3. Results

### 3.1 Method

W(h_a) = pole + arch − P_sum, per the A3 report §3 (symmetric Guinand–Weil,
D10a-step2 normalization): pole = 2e^{a/4};
arch = (1/π)∫_0^∞ e^{−ar²}[Re digamma(1/4+ir/2) − log π] dr (mpmath, 30 dps);
P_sum(z) = −2Σ_{d∈F_z, d≥2} μ(d)·log d·S(d), where F_z = {squarefree d : all
prime factors ≤ z} is the finite face lattice (subsets S of the prime label
set {p ≤ z}, d = ∏S, μ(d) = (−1)^{|S|}), S(d) = Σ_{m≥1}(dm)^{−1/2}g(log dm),
g(u) = C_a·e^{−u²/(4a)}, C_a = (1/2π)√(π/a). The "full" reference uses all
squarefree d (μ via linear sieve; validated term-identical to the A3
Möbius-recurrence values: P_full matches the A3 report to 9 digits at all
three a). Dmax/Mmax cutoffs are z-independent (common-mode), set from the
Gaussian tail and verified negligible by the A3 9-digit agreement.

This is the pilot's D1 face-sum restricted to the truncated sieve
Δ^{(z)}: P_sum = 2Σ_{S⊆{p≤z},S≠∅}(−1)^{|S|+1}·log(∏S)·S(∏S).

### 3.2 Reference values (full, untruncated)

| a    | P_sum (full) | W(h_a) ref       | A3 report |
|------|--------------|------------------|-----------|
| 0.02 | 0.004820125  | 3.708258e−02     | matches   |
| 0.10 | 0.325611035  | 4.209600e−09     | matches   |
| 0.50 | 1.069950188  | ~0 (1.3e−14 resid)| matches   |

arch: −1.968122333 (a=0.02), −1.725019202 (a=0.1), −1.196346718 (a=0.5).

### 3.3 Error vs z

|E(z)| = |W(h_a;z) − W_ref|, with predicted tail pred(z,a) = e^{−(log z)²/(4a)}:

| z    | π(z) | a=0.02 err | a=0.10 err | a=0.50 err | pred(0.5) |
|------|------|------------|------------|------------|-----------|
| 30   | 10   | 0 (vacuous)| 1.82e−13   | 3.77e−03   | 3.08e−03  |
| 100  | 25   | 0 (vacuous)| 0          | 5.11e−05   | 2.48e−05  |
| 300  | 62   | 0 (vacuous)| 0          | 2.06e−07   | 8.62e−08  |
| 1000 | 168  | 0 (vacuous)| 0          | 1.69e−10   | 4.35e−11  |
| 3000 | 430  | 0 (vacuous)| 0          | 6.28e−14   | 1.20e−14  |

Log-error vs predicted log-tail (a=0.5): differences +0.20, +0.72, +0.87,
+1.36, +1.65 (ratios 1.2–5.2×) — the O(log log z) prefactors. a=0.1, z=30:
ratio 0.66.

### 3.4 Against the pre-registered prediction

- **P1 (scaling) — CONFIRMED.** log|E(z)| tracks −(log z)²/(4a) to O(1) at
  every measured point. No smoothing, no discrepancy.
- **P2 (a=0.5 threshold) — CONFIRMED.** True W(h_{0.5}) ≈ 2e^{−aγ₁²} ≈ 7.6e−44.
  Measured err stays 6.3e−14 at best (z=3000) — thirty orders of magnitude
  above the signal. The curve never crosses below W_ref; positivity is
  unresolvable at every feasible z, exactly as predicted (threshold
  z ≈ 1.4×10⁶).
- **P3 (easy regimes) — CONFIRMED.** a=0.02: z-truncation vacuous already at
  z=30 (all contributing faces have prime factors ≤ 7). a=0.1: err 1.8e−13
  at z=30, zero thereafter — converged by z~100 as predicted.

### 3.5 Controlled tail bound

For missing faces (d with some prime factor > z, hence d > z):
|E(z)| ≤ 2Σ_{d∉F_z} log d·S(d), and for dm ≥ z,
e^{−(log dm)²/(4a)} ≤ (dm)^{−log z/(4a)}, giving
|E(z)| ≤ 2C_a·ζ(1/2+log z/(4a))·Σ_{d∉F_z}(log d)·d^{−1/2−log z/(4a)}.
Empirical envelope over the tested range: |E(z)| ≤ 6·e^{−(log z)²/(4a)}
(computationally verified envelope, not a proved constant).

## 4. Label-dependence naming

Per the PARTIAL bound (name, don't absorb):

(a) **Primality of labels — USED, number-theoretic.** The label set {p ≤ z}
is generated by the sieve of Eratosthenes, which tests primality. The face
lattice Δ^{(z)} (2^{π(z)}−1 nonempty faces) exists only once this list is given.

(b) **Label VALUES in face weights — USED, number-theoretic.** Each face S
carries weight log(∏S) and argument ∏S in S(∏S): the weight depends on the
PRODUCT of its labels — multiplicative structure of label values, beyond
mere distinctness. A bare index set would give uniform weights; the actual
weights need the values.

(c) **π(z) sets lattice size — USED, number-theoretic.** The dimension of
the complex (number of labels) is the prime-counting function.

(d) **p mod m / congruence conditions — NOT USED.** No step conditions on
residue classes.

(e) **μ via recurrence — GENERATED, not input.** μ(d)=(−1)^{|S|} read off
face dimension; the full-reference μ matches the divisibility-poset
recurrence (A3 report), so no prime table beyond (a).

The prime structure visible in the output (e.g., which d contribute) is
emergent from (a)+(b), in the sieve's own elimination spirit — but (a) and
(b) are genuine number-theoretic inputs and are named as such.

## 5. Per-input classification

| # | Input | Classification | Notes |
|---|-------|----------------|-------|
| 1 | Prime list p ≤ z (sieve) | number-theoretic label input | §4(a); sets lattice |
| 2 | Face lattice (subsets S, d=∏S) | incidence (Boolean lattice on labels) | 2^{π(z)} faces |
| 3 | Face weights log(∏S), S(∏S) args | number-theoretic (label values) | §4(b) |
| 4 | μ(d)=(−1)^{\|S\|} | incidence (face dimension) | generated, not imported |
| 5 | g, h_a, pole=2e^{a/4} | analytic (test function) | |
| 6 | digamma integral | analytic (classical; no zero data) | |
| 7 | Gaussian tail bound | elementary analysis | §3.5 |
| 8 | a_p | NOT USED | |
| 9 | ψ/π/prime sums as inputs | NOT USED | prime sum is OUTPUT |
| 10 | zeta zeros | NOT USED | |

## 6. Verdict

**PARTIAL — informative** (computationally verified).

- **What the finite face lattice determines:** W(h_a) up to the explicitly
  bounded tail |E(z)| ≲ 6·e^{−(log z)²/(4a)} (§3.5). Verified numerically:
  the error curve follows the pre-registered Gaussian-in-log-z scaling at
  every point (P1), with the easy regimes converging as predicted (P3).
- **What escapes it:** the SIGN of W — i.e., the positivity the Node 10a bar
  actually asks about. Certifying W > 0 needs log z ≳ 2aγ₁; at a = 0.5 that
  is z ≈ 1.4×10⁶, unreachable. The lattice resolves W only to the accuracy
  at which z resolves γ₁ ≈ 14.1347 — and γ₁ is exactly what the lattice
  cannot see without already being large enough to encode it.
- **Label dependence:** named in §4 — primality to generate the label set,
  label values in the face weights, π(z) for lattice size. No congruence
  dependence. None of it absorbed into "labels."

**Epistemic labels:** error scaling and reference values computationally
verified; tail-bound form exact (constant empirical); the threshold
log z ≳ 2aγ₁ exact given the tail form; "circularity in quantitative form"
heuristic — it is the interpretation the numbers force, stated as such.

**Relation to the A3 Item-1 question:** the vacuous integer-divisibility
version is superseded. On the actual D1 object, the answer is: the energy is
determined by the finite face lattice up to a controlled, pre-registered
tail — but the tail swallows the signal precisely where positivity is
nontrivial, at a threshold set by the first zero. PARTIAL, and informative
because it names the exact price of admission: z must resolve γ₁.
