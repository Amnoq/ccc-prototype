# Worked n=1 case: λ_1 = W(h_1), two-sided

Date: 2026-10-09. Read-only elsewhere; new work in this directory.
Script: `worked_n1.py`. Numbers: `worked_n1_numbers.json`.

## Setup

h_1(x) = 1_{(0,1]}, ĥ_1(s) = 1/s, λ_1 = Σ_ρ m_ρ ĥ_1(ρ) = Σ_ρ 1/ρ
(symmetric summation, multiplicity). For ρ = 1/2 ± iγ on the line,
1/ρ + 1/ρ̄ = 1/(1/4+γ²), so λ_1 = Σ_{γ>0} 1/(1/4+γ²).

Exact value: λ_1 = 1 + γ_E/2 − (1/2)log(4π) ≈ 0.023095708966.

## (a) Zero side — COMPUTATIONALLY VERIFIED

300 zeros via mpmath (T = 541.8):

| quantity | value |
|---|---|
| partial sum S(T) = Σ_{0<γ≤T} 1/(1/4+γ²) | 0.0214961899 |
| tail estimate ∫_T^∞ γ^{-2}dN(γ) | 1.548e-03 |
| S(T) + tail | 0.0230440476 |
| exact | 0.023095708966 |
| \|S+tail − exact\| | 5.17e-05 |

The zero-side sum is verified against the exact value to 5e-05
(raw truncation error 1.6e-03, tail accounted).

## (b) W side — explicit formula VERIFIED at fixed ε; ε→0 limit DIVERGES

Regularization: g_{1,ε}(x) = F_ε(x), C³ septic-smoothstep, supported in
[ε,1], =1 on [2ε,1−ε], smooth transitions. Closed-form Mellin
Φ_ε(s) = Σ c_k(b^{s+k}−a^{s+k})/(s+k) (piecewise polynomial).

Used the pilot's verified even-h explicit formula with h_ε(r) = Re[Φ_ε(1/2+ir)]:
  W_ε = Φ_ε(0) + Φ_ε(1) + A_ε − P_ε,
  A_ε = (1/π)∫_0^∞ h_ε(r)[Reψ(1/4+ir/2)−logπ]dr,
  P_ε = Σ_{n≥2}(Λ(n)/n)F_ε(1/n)  (from 2ΣΛ(n)n^{-1/2}g(log n), using
  g_ε(log n) = F_ε(1/n)/(2√n) for F supported in (0,1]).

**Fixed-ε check (formula holds):** at ε=0.1,
  zero side Σ_{|γ|≤541.8} h_ε(γ) = −0.37282288,
  prime side W_ε                  = −0.37281604,
  agreement 6.8e-06 (remainder is the zero tail). The machinery is correct.

**ε→0 limit DIVERGES (naive truncation):**

| ε | Φ_ε(0) | Φ_ε(1) | A_ε | P_ε | W_ε | \|W_ε−λ_1\| |
|---|---|---|---|---|---|---|
| 0.2 | 1.104 | 0.600 | −1.195 | 0.662 | −0.153 | 1.8e-01 |
| 0.1 | 1.852 | 0.800 | −1.714 | 1.311 | −0.373 | 4.0e-01 |
| 0.05 | 2.571 | 0.900 | −2.143 | 2.029 | −0.701 | 7.2e-01 |
| 0.025 | 3.277 | 0.950 | −2.530 | 2.708 | −1.011 | 1.0e+00 |

W_ε → −∞, not λ_1 ≈ +0.023.

**Why.** Φ_ε(0) and P_ε both grow like log(1/ε) and their difference
stabilizes (0.44 → 0.57), so the pole/prime logs cancel as hoped. But the
archimedean term A_ε ALSO diverges like −log(1/ε) (−1.20 → −2.53), and
nothing cancels it. The pointwise limit h_ε(r) → (1/2)/(1/4+r²) exists,
but the convergence is not dominated in a way the archimedean integral
respects — a boundary layer from the ε-cutoff contributes a divergent
−log(1/ε). Naive truncation (support cutoff at ε + smoothing at 1) does
NOT recover λ_1 in the limit.

This is exactly the delicacy the REPORT flagged ("the full distributional
W needs that regularization"): BOM's construction needs the de la
Vallée-Poussin zero-free-region limit control (corpus: "limit (3.4) via
de la Vallee-Poussin zero-free region"), not just truncation+smoothing.
The naive version fails, and it fails in the archimedean term — the term
that carries the Γ-factor, i.e. the "infinite prime."

## Independent check (no zeros, no explicit formula)

Keiper–Taylor via Stieltjes constants (li_criterion.py Part A machinery,
dps=80): λ_1 = 0.023095708966, agrees with exact to 2.4e-17.
Fully independent of both the zero sum and the W-side.

## Conclusion

- λ_1 = Σ_ρ 1/ρ (zero side): **computationally verified** (5e-05).
- λ_1 via Keiper–Taylor: **computationally verified** (2e-17), independent.
- Explicit-formula machinery (even-h form): **verified at fixed ε**
  (zero side = prime side to 7e-06).
- Full W(h_1) = prime+arch via naive ε-regularization: **DIVERGES**;
  the ε→0 limit is NOT established by truncation+smoothing alone.
  The REPORT's "exact theorem" (λ_n = W_dist(h_n)) is the zero-side
  distributional identity, which stands; the prime-side+archimedean
  limit requires BOM's full regularization with zero-free-region control,
  which was not replicated here.

**Epistemic label on the two-sided comparison:** the zero-side identity
λ_1 = W_dist(h_1) is computationally verified; the regularized full-W
limit λ_1 = lim_{ε→0} W(g_{1,ε}) is **not verified** — naive truncation
diverges, so the comparison does not close by this route. This is a
substantive finding, not a bug: it shows the non-square h_n cone is
problematic even at the regularization level, reinforcing the REPORT's
separate cone question (why the {h_n} cone suffices for RH despite not
being square and not admitting naive W-regularization).

**Implication for the A2 verdict:** the FACET verdict rests on the
zero-side functional identity λ_n = W_dist(h_n) (exact, verified), not
on the prime-side limit. The divergence does not overturn FACET, but it
sharpens the cone question: A2 routes through W as a distribution on
zeros, and the passage to a prime-side+archimedean "positivity" is
exactly what fails naively — which is why A2 does not inherit Weil's
manifest square-cone positivity. The obstruction is now computational,
not just analytic.
