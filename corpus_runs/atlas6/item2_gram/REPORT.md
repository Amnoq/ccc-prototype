# Item-2 Gram test — REPORT

**Date:** 2026-10-09. **Status:** complete.
**Analyst:** subagent (parent: main agent). Atlas records read-only throughout.
**Context:** A3 test §6 left Item 2 OPEN — no Hodge-index-type theorem for the
dictionary's form exists in the record. This is the reviewer's proposed first
feasibility test, via the elliptic template (C×C, Gram of {Δ′, Γ′}, det 4q−a² ≥ 0
from the Hodge signature statement).

## 1. Feasibility verdict: FEASIBLE (computation goes through; the PSD fails)

The proposed Gram matrix G_ij = W(h_{a_i} ∗ h_{a_j}), h_a(r) = e^{−ar²},
is well-defined and computable with the existing machinery. The convolution
is exact (§2), the result is admissible for W (§3), and every entry was
computed via the prime side (pole + archimedean − prime sum), never the zero
sum. **The matrix is not positive semidefinite** — see §5. The failure is
structural (confirmed in 50-digit precision, every 2×2 principal submatrix),
not a numerical artifact. Its meaning is analyzed in §6: it does not threaten
RH, because the test conflates two different convolutions.

## 2. The convolution (exact theorem)

For h_a(r) = e^{−ar²}, h_b(r) = e^{−br²}, additive convolution on ℝ:

(h_a ∗ h_b)(r) = ∫_{−∞}^{∞} e^{−as²} e^{−b(r−s)²} ds
              = √(π/(a+b)) · exp(−[ab/(a+b)]·r²).

*Derivation:* as² + b(r−s)² = (a+b)(s − br/(a+b))² + abr²/(a+b); the Gaussian
integral gives √(π/(a+b)). Status: **exact theorem** (elementary calculus).

Hence, with K_ij = √(π/(a_i+a_j)) and c_ij = a_i·a_j/(a_i+a_j),

    G_ij = W(h_{a_i} ∗ h_{a_j}) = K_ij · W(h_{c_ij})      (W linear).

Note c_ij < min(a_i, a_j) (harmonic: 1/c_ij = 1/a_i + 1/a_j).

## 3. Admissibility (exact)

K_ij·h_{c_ij} is a scaled Schwartz function (smooth, rapid decay, even,
entire). The symmetric Guinand–Weil formula as implemented in
`prime-sieve-geometry/weil_positivity.py` requires: h even (✓), Fourier pair
g of Gaussian decay so the prime sum converges (✓ — verified numerically,
tail < 10^{−18} even at the smallest c), archimedean integral convergent
(✓). Linearity of W (pole, archimedean integral, prime sum each linear in h)
justifies G_ij = K_ij·W(h_{c_ij}). Status: **exact** — no regularity
obstruction; the naive-regularization pathology seen in the Li n=1 case does
not arise (Gaussians are smooth and admissible as-is).

## 4. Numerical results (computationally verified)

a_i ∈ {0.02, 0.05, 0.1, 0.5, 1.0}. Entries via prime side only
(vectorized `weil()` machinery; 26,152 prime powers to 300k; mpmath
archimedean at 30 digits). Zero-side values computed separately afterwards
as a cross-check only.

Per-entry (c, K, pole, arch, psum, W_prime, W_zero):

| (a_i,a_j) | c | K | W_prime | W_zero (10 zeros) |
|---|---|---|---|---|
| (0.02,0.02) | 0.01000 | 8.8623 | 2.993960e-01 | 2.993960e-01 |
| (0.02,0.05) | 0.01429 | 6.6992 | 1.191010e-01 | 1.191010e-01 |
| (0.02,0.1) | 0.01667 | 5.1166 | 7.292285e-02 | 7.292285e-02 |
| (0.02,0.5) | 0.01923 | 2.4580 | 4.331547e-02 | 4.331547e-02 |
| (0.02,1.0) | 0.01961 | 1.7550 | 4.013753e-02 | 4.013753e-02 |
| (0.05,0.05) | 0.02500 | 5.6050 | 1.357883e-02 | 1.357883e-02 |
| (0.05,0.1) | 0.03333 | 4.5765 | 2.563911e-03 | 2.563911e-03 |
| (0.05,0.5) | 0.04545 | 2.3900 | 2.275318e-04 | 2.275318e-04 |
| (0.05,1.0) | 0.04762 | 1.7297 | 1.476488e-04 | 1.476488e-04 |
| (0.1,0.1) | 0.05000 | 3.9633 | 9.175670e-05 | 9.175670e-05 |
| (0.1,0.5) | 0.08333 | 2.2882 | 1.175905e-07 | 1.175905e-07 |
| (0.1,1.0) | 0.09091 | 1.6900 | 2.588450e-08 | 2.588450e-08 |
| (0.5,0.5) | 0.25000 | 1.7725 | −4.44e-16 (noise) | 4.06e-22 |
| (0.5,1.0) | 0.33333 | 1.4472 | −2.22e-16 (noise) | 2.39e-29 |
| (1.0,1.0) | 0.50000 | 1.2533 | 0 (noise) | 8.26e-44 |

Prime side = zero side to 6+ digits wherever resolved. For c ≥ 0.25 the
prime side hits its float noise floor (~10^{−16} absolute, catastrophic
cancellation of pole+arch−psum) while the true values are 10^{−22}–10^{−44}:
a resolution limit of the float machinery, recorded not hidden.

Gram matrix G (prime side):

    [ 2.6533   0.7979   0.3731   0.1065   0.0704 ]
    [ 0.7979   0.0761   0.0117   5.44e-4  2.55e-4]
    [ 0.3731   0.0117   3.64e-4  2.69e-7  4.37e-8]
    [ 0.1065   5.44e-4  2.69e-7  ~1e-16   ~1e-16 ]
    [ 0.0704   2.55e-4  4.37e-8  ~1e-16   ~1e-16 ]

Eigenvalues: −2.0908e-01, −2.2691e-04, 3.3983e-08, 8.8016e-03, 2.9303e+00.
**Not PSD.** The 3×3 well-resolved principal submatrix alone has eigenvalues
(−2.0240e-01, 6.9805e-03, 2.9252e+00) — the failure sits in resolved entries,
not the noise tail. **Every one of the ten 2×2 principal submatrices has
negative determinant** (e.g. (0.02,0.05): −4.35e-01; (0.05,0.1): −1.10e-04).
Failing direction (λ_0 eigenvector): (−0.295, 0.806, 0.481, 0.148, 0.099).

High-precision confirmation: the zero-side matrix rebuilt in mpmath at 50
digits with 100 zeros (all terms positive, no cancellation anywhere) has
identical eigenvalues to 6 digits, and Cholesky decomposition fails. The PSD
failure is structural, not numerical. Status: **computationally verified**.

## 5. Why this does not threaten RH (the conflation)

The negative eigenvalues are real, but they are **not** a counterexample to
Weil positivity, because the test uses the wrong convolution. Two distinct
operations have been conflated:

- **Additive convolution on ℝ** (this test): (f ∗_{add} g)(r) = ∫f(s)g(r−s)ds.
  The Gram matrix above is G_ij = W_pilot(h_{a_i} ∗_{add} h_{a_j}).
- **Multiplicative convolution on ℝ₊^×** (Weil's criterion): (f ∗_{mult} g)(x)
  = ∫₀^∞ f(y)g(x/y)dy/y, with involution f̃(x) = x⁻¹·conj(f(1/x)).

That Weil's criterion governs the *multiplicative* convolution is established
in our own verified record: the Li check proved h_n is not of the form
f ∗ f̃ **"(multiplicative convolution, f̃(x) = x⁻¹·conj(f(1/x)))"**
(`li_check/REPORT.md` §4b, status exact theorem), and BOM's Theorem 2 is
stated for that convolution. The h_n themselves live on (0,1] with
P_n(log x) — the multiplicative group.

Weil's positivity theorem says W_Weil(f ∗_{mult} f̃) ≥ 0 (⟺ RH). It says
nothing about W_pilot(F ∗_{add} F). For F = Σv_i h_{a_i} (real),
W_pilot(F ∗_{add} F) = Σ_ρ (F ∗_{add} F)(γ_ρ), and the autocorrelation
(F ∗_{add} F)(γ) = ∫F(y)F(γ−y)dy can be negative at nonzero lag for
sign-changing F — there is no theorem forcing positivity. The observed
indefiniteness is therefore **compatible with RH**; it is the expected
behavior of the wrong pairing, not a crack in the right one.

A second, related conflation to retire: the pilot's "squares" h_a = |H_a|²
with H_a(r) = e^{−ar²/2} are **pointwise** squares (each term
|H_a(γ_ρ)|² ≥ 0 trivially, so W_pilot(h_a) ≥ 0 is unconditional given
convergence). Weil's "squares" f ∗ f̃ are **convolution** squares, whose
positivity is deep (⟺ RH). The D10a positivity exhibited is the pointwise
kind; the Gram test probed the additive-convolution kind; Weil's theorem
concerns the multiplicative-convolution kind. Three different objects.

Note the internal tension this resolves in the proposal itself: it asked for
a pairing with ⟨h,h⟩ = W(h), but G_ij = W(h_{a_i} ∗ h_{a_j}) gives
⟨h_a,h_a⟩ = W(h_a ∗ h_a) = K·W(h_{a/2}) ≠ W(h_a). No bilinear pairing built
this way satisfies ⟨h,h⟩ = W(h).

## 6. What this establishes and cannot establish about Item 2

**Establishes:**
- The additive-convolution pairing (f,g) ↦ W_pilot(f ∗_{add} g) is
  indefinite on the Gaussian span — ruled out as the sought pairing.
  (computationally verified)
- The convolution at the heart of the test is exact and the computation is
  faithful; the failure is in the pairing's positivity, not the numerics.
- A resolution limit of the float prime-side machinery: entries with
  W(h_c) ≲ 10^{−16} (c ≳ 0.2) are noise-dominated by pole/arch/psum
  cancellation. Any future Gram work in this regime needs higher precision
  or the zero side.

**Cannot establish:**
- Nothing here bears on RH: the negative eigenvalues live outside the cone
  where Weil positivity holds. (exact theoretical argument, §5)
- Nothing here advances Item 2 positively: ruling out one wrong pairing is
  negative information. Item 2 — a Hodge-index-type theorem for the
  dictionary's form, with positivity from a signature statement — remains
  **OPEN**, exactly as the A3 report left it.
- The "smallest eigenvalue pattern" does not exhibit a Hodge-type rank-one
  defect: the indefiniteness is systematic (every 2×2 fails), not a
  near-degeneracy of an otherwise PSD form. The defect language presupposes
  a PSD form with signature structure; there is none here.

**Recommendation for the faithful test:** redo the Gram construction with
the multiplicative convolution on ℝ₊^× (Li/BOM style): test functions on
(0,∞), G_ij = W_Weil(φ_i ∗_{mult} φ̃_j). That is the pairing Weil's theorem
actually governs. It requires the Mellin-side machinery, not the symmetric
Gaussian setup — a different computation, not attempted here.

## Epistemic summary

| Claim | Label |
|---|---|
| Convolution formula (h_a ∗ h_b) = √(π/(a+b))·h_{ab/(a+b)} | exact theorem |
| Admissibility of scaled Gaussians for W | exact |
| Prime-side entries (where resolved, c ≲ 0.15) | computationally verified |
| G not PSD (eigenvalues, all 2×2 dets, 50-digit confirmation) | computationally verified |
| PSD failure is structural, not numerical | computationally verified |
| Weil's criterion governs multiplicative, not additive, convolution | exact (per li_check/REPORT.md §4b; BOM Theorem 2 cited-not-verified for the full statement) |
| Failure compatible with RH; threatens nothing | exact theoretical argument |
| Item 2 remains OPEN | unchanged from A3 report |

**Bottom line:** the proposed Gram test is feasible and was executed
faithfully, but it tests the wrong pairing — additive convolution on ℝ,
whereas Weil positivity lives on multiplicative convolution on ℝ₊^×. The
matrix is genuinely indefinite (not a numerical artifact), and that
indefiniteness is exactly what one expects of the wrong pairing. Item 2 is
untouched: still OPEN, still awaiting its Hodge-index analogue.
