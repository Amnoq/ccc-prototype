# Worked n=2 case: λ_2 three-leg check

Date: 2026-10-09. Read-only elsewhere; new work in this directory.
Script: `worked_n2.py`. Numbers: `worked_n2_numbers.json`.
Zero cache: `zeros_cache.json` (300 zeros, persistent — /tmp cache was wiped).

Context: n=1 (WORKED_N1.md) verified the zero-side identity λ_1 = W_dist(h_1)
but showed naive ε-regularization of the full W side DIVERGES (archimedean
−log(1/ε) uncanceled). The naive W route is NOT repeated here — that failure
mode is established. n=1 was a normalization test (λ_1 has the elegant closed
form 1+γ_E/2−½log4π); n=2 tests the FAMILY structure: does the zero-side
functional identity λ_n = W_dist(h_n) extend cleanly to a genuinely different
test function?

## Setup

h_2(x) = (2 + log x)·1_{(0,1]}, ĥ_2(s) = 1 − (1−1/s)² = 2/s − 1/s².
Zero side (symmetric ρ↔ρ̄ pairing): λ_2 = Σ_{γ>0} 4γ²/(1/4+γ²)².
(Derivation: 2·Re[ĥ_2(1/2+iγ)] = 4γ²/(1/4+γ²)²; cross-checked numerically on
the first 3 zeros — direct pair form vs simplified form agree to 1e-12.)

## Leg 1: zero side — COMPUTATIONALLY VERIFIED (tail-dominated)

300 zeros via mpmath (T = 541.8):

| quantity | value |
|---|---|
| partial sum S(T) = Σ_{0<γ≤T} 4γ²/(1/4+γ²)² | 0.0859476604 |
| tail estimate ∫_T^∞ term·dN | 6.293e-03 |
| strict analytic upper bound (term < 4/γ²) | 6.412e-03 |
| S(T) + tail | 0.0922410229 |
| Keiper–Taylor (leg 2) | 0.092345735228 |
| \|S+tail − Keiper\| | 1.05e-04 |

The tail integral brackets below the strict bound (6.293e-03 < 6.412e-03),
and the residual 1.05e-04 is ~1.7% of the tail — same relative quality as
the n=1 case (5e-05 on a 1.548e-03 tail). Raw truncation error 6.4e-03 is
fully accounted for by the tail estimate.

## Leg 2: Keiper–Taylor via Stieltjes constants — COMPUTATIONALLY VERIFIED

li_criterion.py Part A machinery at dps=80 (no zeros anywhere):

    λ_2 = 0.092345735228046670385728486192067886774132216628246509399632597933985389203116114

Sanity: λ_1 = 0.023095708966 reproduced exactly (matches 1+γ_E/2−½log4π).
Independent of the zero sum (uses only Stieltjes constants + polygamma).

## Leg 3: closed-form anchor — CONFIRMED

|0.09234573522804667 − 0.0923457| = 3.52e-08 → recollection CONFIRMED.
(The "closed form" for λ_2 is Keiper's Stieltjes-constant expression; unlike
λ_1 it has no elementary constant-only form. The anchor value is confirmed
by the dps=80 computation, not trusted from memory.)

## Comparison

| leg | value |
|---|---|
| zero side (+tail) | 0.0922410229 |
| Keiper–Taylor | 0.092345735228 |
| recollected anchor | 0.0923457 ✓ |
| \|zero − Keiper\| | 1.05e-04 (tail-dominated) |

Internal consistency: λ_2 = 4λ_1 − Σ_{γ>0}(1/4+γ²)^{−2} gives
Σ(1/4+γ²)^{−2} = 4(0.023095708966) − 0.092345735228 = 3.71e-05,
consistent with the first zero alone contributing 2.5e-05. ✓

## Non-square status of h_2 — cited from REPORT.md §4b

The general proof covers all n ≥ 1: ĥ_n(1/2+it) non-real for generic t,
while a square's transform there is ≥ 0 real. For n=2 explicitly:
ĥ_2(1/2+i) = 1.28 − 0.96i (verified by hand here; matches REPORT).
No gap found; not re-proved.

## What n=2 adds beyond n=1

n=1 tested normalization: one function, one elegant closed form. n=2 tests
the FAMILY: h_2 is a genuinely different test function ((2+log x)·1_{(0,1]},
Mellin 2/s − 1/s², jump of size 2 at x=1, non-square by the same
obstruction), and the zero-side sum Σ_ρ m_ρĥ_2(ρ) converges to the
independently computed Keiper value. The functional identity
λ_n = W_dist(h_n) is not a one-off — it extends cleanly across the family,
with the same tail-dominated convergence profile as n=1. Combined with the
§4b non-square proof, this is the second worked instance of the reviewer's
middle branch: h_n exists, is not square, A2 routes through W itself.

## Epistemic labels

| Claim | Status |
|---|---|
| λ_2 = Σ_{γ>0} 4γ²/(1/4+γ²)² (pair-sum algebra) | exact theorem (cross-checked 1e-12) |
| zero-side sum → 0.0922410 ± ~1e-4 | computationally verified (tail-dominated) |
| λ_2 = 0.092345735228… via Stieltjes | computationally verified (dps=80) |
| recollection 0.0923457 | confirmed (3.5e-8) |
| family structure extends (n=1 → n=2) | computationally verified |
| h_2 non-square | exact theorem (REPORT §4b, cited) |
| naive W-side ε-regularization for n=2 | not attempted (n=1 established divergence) |
