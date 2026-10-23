# Li Equivalence Check — Atlas-6 A2

Date: 2026-10-09. Read-only on atlas records; new work only in this directory.
Task: does A2 ("Li's criterion as proof lemma (BOM)") reduce to Weil positivity
W(f,g), i.e. is A2 a facet of the Weil crack or an independent candidate?

## 1. A2 target statement (as adjudicated)

From `cross_bridge_links.json` (verdict `split_link`, relation `shares-criterion`):

- (a) `bom:li-s-criterion-as-used-in-the-proof-local-role-b` — "Li's criterion
  as used in the proof [local role B]": BOM uses it as the lemma for the
  converse of Theorem 1 (cited via Bombieri–Lagarias; "conjectural-from-this-text").
- (b) `rel:10b-li-s-criterion-via-the-face-sum-rh-n-0-n-n-e` — the pilot computed
  λ_n via the D1 face-sum as the most computable positivity criterion
  (heuristic/programmatic, D10b).

Target statement: **Li's criterion, RH ⟺ λ_n ≥ 0 for all n ≥ 1**,
where λ_n = Σ_ρ [1 − (1 − 1/ρ)^n], sum over nontrivial zeros with
multiplicity, symmetric summation. As invoked by BOM: the lemma for the
converse direction of Theorem 1.

## 2. Pre-registered criterion (revised per reviewer)

Logical equivalence is too weak (both λ_n ≥ 0 ∀n and W(f∗f̃) ≥ 0 ∀f are
equivalent to RH, so statement-equivalence passes trivially). Required
instead: **functional identity** — an explicit family h_n (n ≥ 1) with

    λ_n = W(h_n)   EXACTLY,

using the same W, same normalization as AF's definition.

AF's definition (corpus `extractions/weil_analytic_af_w1.json`, status "exact"):
W(f,g) = Σ_ρ m_ρ f̂(γ_ρ)·conj(ĝ(γ̄_ρ)), γ_ρ = (ρ−1/2)/i,
on compactly supported test functions. The unary reading used here:
W_dist(F) = Σ_ρ m_ρ F̂(ρ) (Mellin transform, symmetric sum, multiplicity),
which satisfies W_AF(f,g) = W_dist(f ∗ g̃) with g̃(x) = x⁻¹·conj(g(1/x)).
"Same normalization" = sum over zeros with multiplicity m_ρ, symmetric
summation, Mellin transform F̂(s) = ∫₀^∞ F(x) x^{s−1} dx.

Additionally: is each h_n of square form f ∗ f̃? Outcomes:
- h_n exists and is square → A2 facet: 8 facets, A3 only open candidate.
- h_n exists, not square → A2 still a facet (same W); cone question separate.
- No h_n → 7 facets; A2, A3 independent (obstruction must name the failure).

## 3. Literature leg

From the corpus (`extractions/weil_analytic_bom_w1.json`), read in full:

- Construction (status **exact**): "The Li sum is realized as sum g_n(rho)
  g_n(1-rho) with g_n the inverse Mellin transform of 1 - (1 - 1/s)^n
  (so g_n(x) = P_n(log x) on (0,1], explicit polynomial P_n); truncation
  g_{n;epsilon} plus limit (3.4) via de la Vallee-Poussin zero-free region
  and final smoothing by multiplicative convolution with a smooth
  approximate Dirac at 1."
- Theorem 2 (status **exact**): "T[f] = T[f*] = sum_rho f-hat(rho), and RH
  is equivalent to T[f* * f] >= 0 with equality only for f = 0. Proved from
  the Explicit Formula plus Theorem 1; in fact equivalent to
  T[g_{n;epsilon} * g_{n;epsilon}*] > 0 for all n, epsilon."
- Li's criterion itself (status **conjectural** in extraction): "Criterion
  due to X.-J. Li [4], via Bombieri-Lagarias [1]: RH is equivalent to the
  sum in (3.3) being > 0 for n = 1,2,3,... Used as the lemma for the
  converse; cited, not proved here; the displayed sum is scan-fragmented."

Epistemic status:
- The g_n construction (inverse Mellin of 1−(1−1/s)^n, P_n(log x) on
  (0,1], truncation/smoothing): **computationally verified** — corpus
  "exact", and independently re-derived from scratch below (matches term
  for term).
- The Bombieri–Lagarias connection as the proof-lemma for BOM's converse:
  **cited, not verified** — BOM cites it; it is not proved in the corpus
  material read.
- "The recollection" (λ_n via explicit formula through 1−(1−1/s)^n):
  **confirmed** against the corpus chunk read in full, not trusted blindly.

## 4. Mathematical leg

### 4a. The explicit family h_n (functional identity: YES)

Define, for n ≥ 1 and x > 0,

    h_n(x) = P_n(log x) · 1_{(0,1]}(x),

    P_n(t) = Σ_{k=1}^{n} C(n,k)·(−1)^{k+1}·(−t)^{k−1}/(k−1)!.

Derivation (inverse Mellin): for Re(s) > 0,
∫₀¹ P_n(log x) x^{s−1} dx, with t = log x, equals
Σ_{k=1}^{n} C(n,k)(−1)^{k+1}·(k−1)!/s^k/(k−1)!
= Σ_{k=1}^{n} C(n,k)(−1)^{k+1} s^{−k}
= 1 − (1 − 1/s)^n,
since 1 − (1−1/s)^n = −Σ_{k=1}^{n} C(n,k)(−s⁻¹)^k.
Hence, as meromorphic functions,

    ĥ_n(s) = 1 − (1 − 1/s)^n,

verified numerically (trapezoidal Mellin vs closed form, agreement
~10⁻⁸ at s = 2, 1/2+3i, 1.5−2i for n = 1,2,3).
Examples: h_1 = 1_{(0,1]}, h_2(x) = (2 + log x)·1_{(0,1]}.

Therefore, with symmetric summation and multiplicity,

    W_dist(h_n) = Σ_ρ m_ρ ĥ_n(ρ) = Σ_ρ m_ρ [1 − (1 − 1/ρ)^n] = λ_n,

**exactly, termwise**. The family h_n exists and is fully explicit.
Status: **exact theorem** (derived analytically, numerically confirmed).

Admissibility note (stated, not hidden): h_n is compactly supported
(supp ⊆ (0,1]) but not smooth — P_n(0) = n gives a jump discontinuity
of size n at x = 1. So h_n is BV, not C_c^∞; AF's W on "test functions"
applies directly only after BOM's regularization (truncation g_{n,ε},
de la Vallée-Poussin limit, smoothing by approximate Dirac at 1 — as the
corpus records). The zero-side identity λ_n = W_dist(h_n) is exact;
the full distributional W needs that regularization. This does not change
the verdict: the link routes through the same functional W.

### 4b. Square form (obstruction: PROVED — h_n is NOT f ∗ f̃)

Theorem. For every n ≥ 1 there is no (reasonable) f with h_n = f ∗ f̃
(multiplicative convolution, f̃(x) = x⁻¹·conj(f(1/x))).

Proof. (f ∗ f̃)̂(s) = f̂(s)·conj(f̂(1−s̄)). On the critical line
s = 1/2 + it, 1 − s̄ = s, so (f ∗ f̃)̂(1/2+it) = |f̂(1/2+it)|² ≥ 0
(real, nonnegative) for all t. But
ĥ_n(1/2+it) = 1 − ((−1+2it)/(1+2it))^n,
and (−1+2it)/(1+2it) has modulus 1 and non-constant argument, so
ĥ_n(1/2+it) is non-real for generic t — e.g. n = 1, t = 1 gives
0.4 − 0.8i; n = 2, t = 1 gives 1.28 − 0.96i; n = 3, t = 2 gives
0.8992 − 0.9949i. A non-real number cannot equal |f̂|² ≥ 0.
Contradiction. ∎  Status: **exact theorem**.

Consequence: A2 does not inherit Weil's square-cone manifest positivity.
λ_n ≥ 0 is positivity of W on the non-square sequence {h_n}.

## 5. Cone question (separate finding, per reviewer)

Li's criterion asserts that W_dist(h_n) ≥ 0 for all n — positivity on the
non-square cone {h_n} — already implies RH. Why does this cone suffice?
The Bombieri–Lagarias/diophantine mechanism: if RH fails, some zero has
|1 − 1/ρ| = 1 + t > 1 maximal, and Dirichlet simultaneous approximation
makes the Li sums λ_n = W_dist(h_n) negative infinitely often (corpus:
"the Li sum goes negative infinitely often", status exact). So {h_n}
probes the zero distribution finely enough to detect off-line zeros,
even though no h_n is a square. This is a different cone from Weil's
{f ∗ f̃} with the same detecting power — worth its own investigation,
not folded into the facet verdict. Status: heuristic (mechanism
described from the corpus; not proved here).

## 6. Verdict

- h_n exists (explicit, §4a) and is NOT square (§4b, proved obstruction).
- Per the revised criterion: **A2 is a facet of the Weil crack** (same
  functional W), but does not inherit the square-cone positivity.
- **Facet count: 8.** The four deletion-destroyed links (S0, A6, A8, A12)
  + A1, A11, A5 (same Weil-1952 complex at one remove) + A2 (via the
  h_n functional identity).
- **A3 (square dictionary, independently derived pilot side) is the only
  open candidate.**
- Note on the deletion-test puzzle: A2 survived node deletion because its
  nodes are not literally the explicit-formula nodes — but the Li check
  shows A2 routes through the Weil functional itself. Node-level deletion
  missed the functional-level identity; the "independent candidate" was a
  facet at one remove all along.

## Epistemic labels (summary)

| Claim | Status |
|---|---|
| A2 target = Li's criterion as BOM's converse lemma | adjudicated (record) |
| h_n explicit, ĥ_n(s) = 1−(1−1/s)^n | exact theorem |
| λ_n = W_dist(h_n) exactly (symmetric sum) | exact theorem |
| h_n not a square (critical-line obstruction) | exact theorem |
| h_n needs regularization for full W (jump at x=1) | exact (computed) |
| BOM g_n construction matches h_n | computationally verified |
| Bombieri–Lagarias as BOM's proof lemma | cited, not verified |
| Cone question (why non-square cone suffices) | heuristic, separate finding |
