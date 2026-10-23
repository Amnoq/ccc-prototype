# Reviewer sign-off on the Item-2 Gram test — 2026-10-09

Reviewer verdict: **computation accepted, diagnosis half right, recommendation wrong.**

## Accepted

- Convolution formula holds; reviewer rechecked (0.02,0.05): 2.653×0.0761 − 0.798² = −0.435 ✓ matches.
- Indefiniteness is real (structural, not numerical).
- The fault in the test is the reviewer's own: the proposed pairing W(h_{a_i}∗h_{a_j})
  does not satisfy ⟨h,h⟩ = W(h). REPORT §5's internal-tension note stands.

## Correction 1: two cones, not three (diagnosis half right)

REPORT §5 claimed three distinct objects (pointwise squares / additive-convolution
squares / multiplicative-convolution squares). Wrong: there are two.

Write h(r) = ∫g(u)e^{iru}du with u = log x. A pointwise square h = H·H̄ in r is the
Fourier dual of the additive autocorrelation g = G∗G̃ in u, which IS the
multiplicative f∗f̃ on ℝ₊. So the pilot's squares and Weil's squares are the SAME
cone; only the Gram test's pairing (additive convolution of the h's in r) was the
odd one out.

**Backward touch on A3:** "same generative move" is therefore stronger than same
shape — it is the same cone. (Status of this claim: reviewer's argument, not
independently verified here.)

## Correction 2: "W_pilot(h_a) ≥ 0 is unconditional" is FALSE

REPORT §5 stated the pilot's pointwise squares give unconditional positivity.
False: termwise |H(γ_ρ)|² ≥ 0 needs γ_ρ real, which is RH. For an off-line zero
γ = t − iδ, the conjugate pair contributes 2e^{−a(t²−δ²)}cos(2aδt), which can be
negative. Positivity at the Gaussians is OBSERVED, not proved.

**Consequence:** keeps A3 Item 1 low-information (as the reviewer already graded it).

## Correction 3: the faithful test needs no Mellin machinery (recommendation wrong)

REPORT §6 recommended redoing the Gram with multiplicative convolution on ℝ₊^×.
Unnecessary: take H_i = e^{−a_i r²/2}; then G_ij = W(H_i H̄_j) = m((a_i+a_j)/2)
with m(s) = W(h_s) — entries already in the REPORT's tables. Three limitations:

1. Zero side PSD trivially (Gram of positive vectors) — consistency check only.
2. Prime side: entries with s ≳ 0.2 sit below the float floor.
3. A violation needs an off-line zero at height T > 3×10¹², where e^{−aγ²} is
   zero at any resolvable a.

Reviewer: "I wouldn't spend a run on it." Not dispatched.

## Item 2 status

Remains OPEN. Refined requirement (reviewer): a real hit needs a space V and a
form B with B(H,H) = W(|H|²) whose signature is proved WITHOUT zeros. In the
elliptic case, negativity of the form on the complement yields reality of the
roots; here, zero-side positivity IS reality of γ. The Gaussian Gram says nothing
about that.

## Facet count

Conditional 8 pending reviewer's read of li_check/WORKED_N2.md (not yet seen at
sign-off time).
