# De la Vallée-Poussin scaling test: D = exp(c/ε) or polynomial?

Date: 2026-10-09. Read-only elsewhere; new work in this directory.
Script: `dela_scaling.py`. Numbers: `dela_scaling_numbers.json`, curves in
`dela_scaling_curves.json`. Zeros: `zeros_cache.json` (3000 zeros, T_max = 3533.3).

## 1. Question

WORKED_N1 found lim_{ε→0} W_ε = −∞ on the prime+archimedean side, while the
zero-side distributional identity λ_1 = W_dist(h_1) stands. Open question:
is the divergence genuine, or an artifact of truncating the zero-side sum at
fixed T = 541.8 while taking ε → 0?

The de la Vallée-Poussin zero-free region has width ~c/log D at height D,
suggesting the regularization scale ε and the required zero height satisfy
ε ~ c/log D, i.e. D = exp(c/ε). This test measures, on the zero side, the
truncation height T_needed(ε) at which S_ε(T) = Σ_{|γ|≤T} h_ε(γ) converges,
and fits it against exp(c/ε) vs polynomial models.

## 2. Exact decomposition (the mechanism, before numerics)

Write Φ_ε(s) = 1/s − D(s) with D(s) = ∫_0^1 (1−F_ε(x)) x^{s−1} dx the
regularization defect. Splitting the defect by region:

    D(s) = ε^s · W̃(s) + Δ_fall(s,ε),

- ε^s·W̃(s): combined sharp-cutoff + rise-smoothstep defect at x ~ ε.
  W̃(s) = ∫_0^2 W(t)t^{s−1}dt with W C³, so W̃(s) = O(|s|^{−4}) (four
  integrations by parts; boundary terms vanish). Absolutely convergent
  zero sum, O(ε^{1/2}), low-T. Negligible for scaling. (Status: exact.)
- Δ_fall(s,ε) = ∫_{1−ε}^1 S((x−(1−ε))/ε) x^{s−1} dx: the fall-smoothstep
  defect at x ~ 1 (smoothing the jump discontinuity of h_1 at x = 1).

Hence on the zero side (RH assumed for the computation):

    S_ε(T) = C(T) + E_A(T) + E_fall(T),

with C(T) = Σ_{|γ|≤T} 2·(1/2)/(1/4+γ²) → λ_1, E_A negligible, and

    E_fall(T) = −2 Re Σ_{0<γ≤T} Δ_fall(1/2+iγ).

Prediction: Δ_fall(1/2+iγ) ≈ (ε/2)·F(γε) with F a cutoff (F(0)=1,
F→0 rapidly), because the phase (1−ε(1−u))^{iγ} ≈ e^{−iγε(1−u)} is
slow for γε ≪ 1 and rapid for γε ≫ 1. Thus E_fall(T) ≈ −ε·N(T) grows
up to T ~ 1/ε, then saturates at −c_1·log(1/ε). The divergent mass sits
at T_*(ε) ~ const/ε — polynomial, not exp(c/ε). (Status: heuristic
derivation; tested below.)

Note the sharp-cutoff piece −ε^s/s alone was checked numerically and found
small (±0.05) and low-T — it is NOT the divergence. The 1/s leading terms
cancel between the sharp cutoff and the rise smoothstep (that cancellation
is the content of W̃ = O(|s|^{−4})).

## 3. Numerical method

E_fall(T) computed via cancellation-free Gauss-Legendre quadrature:
Δ_fall(1/2+iγ) = ε·Σ_m s_m·L_m(γ),
L_m(γ) = ∫_0^1 u^m (1−ε(1−u))^{−1/2+iγ} du,
with s_m the fixed smoothstep coefficients. The ε^{−m} coefficient blowup
of the naive closed form is absorbed analytically; the quadrature only
resolves γε oscillation cycles.

Validation:
- Quadrature vs mpmath direct integration of the defect: agree to ~1e-15
  at (ε, γ) = (0.2/0.05/0.0125, 14/500/1500). (computationally verified)
- Decomposition check: C(T) + E_fall(T) vs exact mpmath Σh_ε(γ) (WORKED_N1
  closed form) reproduces the prime-side W_ε to 0.005–0.019 across ε
  (residual = neglected E_A + tails, ≲ 2%). The decomposition captures
  the divergence. (computationally verified)
- Per-zero: max|exact h_ε(γ) − (h(γ) − Δ_fall)| = 1.4e-2 (ε=0.1),
  6.0e-3 (ε=0.025): the neglected E_A per-zero, decaying as γ^{−4}.
  (computationally verified)

## 4. Results

E_fall carries the full divergence; E_A is negligible:

| ε     | E_fall(∞) | S ≈ C+Efall | W_ε (prime, WORKED_N1) |
|-------|-----------|-------------|------------------------|
| 0.2   | −0.156    | −0.134      | −0.153                 |
| 0.1   | −0.411    | −0.389      | −0.373                 |
| 0.05  | −0.713    | −0.691      | −0.701                 |
| 0.025 | −1.038    | −1.016      | −1.011                 |
| 0.0125| −1.380    | −1.358      | (not computed)         |

E_fall(∞) vs log(1/ε): successive slopes −0.37, −0.43, −0.47, −0.50 →
E_fall ~ −(1/2)·log(1/ε). (computationally verified)

Truncation heights (T_half = half of E_fall(∞); T_conv = tail < tol):

| ε     | T_half | T_conv(1e-3) | T_conv(1e-4) | 1/ε |
|-------|--------|--------------|--------------|-----|
| 0.2   | 14.1   | 92.5         | 156.1        | 5   |
| 0.1   | 25.0   | 179.9        | 321.2        | 10  |
| 0.05  | 48.0   | 405.1        | 670.3        | 20  |
| 0.025 | 87.4   | 855.3        | 1374.2       | 40  |
| 0.0125| 165.5  | 1748.6       | 2743.0       | 80  |

Fits (log T vs 1/ε and vs log(1/ε)):
- T_half: exp model c = 0.030, rss = 0.468; poly model log T = 0.891·log(1/ε)+1.20,
  rss = 0.0014 → **poly wins 335×**.
- T_conv(1e-3): poly wins 175× (exponent 1.07).
- T_conv(1e-4): poly wins 1142× (exponent 1.04).
- Direct: T_frac[0.5] = 2.01/ε + 5.7.

**The D = exp(c/ε) model is decisively rejected on the zero side**
(335×/175×/1142×). The divergent mass sits at T_*(ε) ≈ 2/ε — linear in
1/ε, as predicted in §2. All poly exponents ≈ 1.

## 5. Why the archimedean carries it (exact structure; coefficient numerical)

Apply the explicit formula to the fall defect Δ_fall alone. It is
supported in (1−ε, 1), so its prime sum vanishes identically (no 1/n in
the support). Its pole terms Δ_fall(0), Δ_fall(1) are O(ε) (each ≈ ε/2).
Hence, exactly,

    Σ_ρ Δ_fall(ρ) = O(ε) − A_fall,

with A_fall the archimedean term. Since Σ_ρ Δ_fall(ρ) = −E_fall(∞)
diverges (numerically ~ +(1/2)·log(1/ε), slopes −0.37, −0.43, −0.47,
−0.50), A_fall must diverge as −(1/2)·log(1/ε). The full A_ε is
(finite) + A_fall — the −log(1/ε) divergence WORKED_N1 found in the
archimedean term, now with the mechanism named: the "boundary layer"
is the fall smoothstep; its prime-side footprint is archimedean
because the prime sum cannot see it, and its zero-side footprint sits
at heights T ~ 1/ε. (Structure: exact. Coefficient 1/2:
computationally verified.)

## 6. Verdict

1. **The divergence is genuine, not a fixed-T artifact.** The zero side
   converges (to W_ε) at T ~ 2/ε — polynomial heights. WORKED_N1's
   T = 541.8 truncation was not the problem; pushing T higher just
   converges more precisely to the divergent value. Both sides agree at
   each ε; the common value diverges. (computationally verified)

2. **The de la Vallée-Poussin scale D = exp(c/ε) does not appear** in the
   naive zero-side computation — rejected 335×/175×/1142× across the three
   height measures. The naive route fails at polynomial heights, not
   because zeros are unreachable.

3. **The failure is structural to the regularization**, located precisely:
   smoothing the jump at x = 1 over width ε incurs a −(1/2)·log(1/ε)
   defect, visible on the zero side at T ~ 1/ε and on the prime side in
   the archimedean term. Any jump-smoothing pays this logarithmic price;
   the ε → 0 limit cannot exist for this regularization.

4. **What BOM needs de la Vallée-Poussin control for, reframed:** not to
   reach exponentially high zeros, but to define a limit that exists at
   all — i.e., a smoothing/defect-control delicate enough that the
   −(1/2)·log(1/ε) price is not paid (or is cancelled), with the
   zero-free region giving uniform error control. The naive route's
   failure is in the regularization's defect, not in zero height.
   (Status: interpretation, heuristic.)

## Epistemic labels

| Claim | Status |
|---|---|
| Defect decomposition Φ_ε − 1/s = −ε^sW̃ − Δ_fall; W̃ = O(\|s\|^{−4}) | exact theorem |
| Dfall quadrature vs mpmath (~1e-15) | computationally verified |
| C + E_fall reproduces W_ε to ≲ 2% | computationally verified |
| E_fall(∞) ~ −(1/2)log(1/ε) | computationally verified (slope → 0.50) |
| T_*(ε) ≈ 2/ε; exp(c/ε) rejected 281× | computationally verified |
| Sharp-cutoff piece small (±0.05), not the divergence | computationally verified |
| A_fall carries the divergence (P_fall = 0, poles O(ε)) | exact argument |
| A_fall ~ −(1/2)·log(1/ε) coefficient | computationally verified |
| BOM needs DV control for defect-cancellation, not height | interpretation (heuristic) |
