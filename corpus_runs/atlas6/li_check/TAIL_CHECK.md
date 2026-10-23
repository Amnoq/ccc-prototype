# 300-zero tail-correction check

**Date:** 2026-10-09. **Status:** complete. Read-only elsewhere; new work in
this directory. Script: `tail_check.py`. Numbers: `tail_check_numbers.json`.
Zeros reused from `zeros_cache.json` (300 zeros, T = 541.847).

## Method

WORKED_N1/N2 computed zero-side partial sums S(T) over 300 zeros and added a
tail estimate ∫_T^∞ term·dN via log-spaced trapezoidal integration truncated
at T×50 (n=1) / T×100 (n=2), reporting residuals 5.17e-05 (n=1 vs exact) and
1.05e-04 (n=2 vs Keiper). This check redoes the tail **analytically**: with
smooth density dN = (1/2π)ln(g/2π)dg and leading terms 1/g² (n=1), 4/g² (n=2),

- A₁(T) = (1/2π)(ln(T/2π)+1)/T,
- A₂(T) = (2/π)(ln(T/2π)+1)/T,

in closed form — no integration cutoff. Dropped model corrections (term vs
1/g²: ~4e-10; density O(1/g) piece: ~3e-7 n=1) are quantified and negligible
vs the residuals. The remaining model error is the oscillatory part of N(g),
whose boundary piece f(T)·S(T), S(T) = N(T) − smooth N(T), is measured
directly from the data at each ladder rung.

## 1. Truncation ladder — NO DRIFT

S(T_k) + A(T_k) at k = 100, 150, 200, 250, 300:

n=1 (ref = exact 0.023095708966):

| k | T_k | S(T_k) | A(T_k) | S+A | (S+A)−ref | S_osc(T_k) | f(T)·S_osc |
|---|------|------------|----------|------------|----------|------|------|
| 100 | 236.52 | 0.0199848524 | 3.114e-03 | 0.0230991071 | +3.40e-06 | +0.190 | +3.40e-06 |
| 150 | 318.85 | 0.0206423372 | 2.459e-03 | 0.0231015670 | +5.86e-06 | +0.596 | +5.86e-06 |
| 200 | 396.38 | 0.0210348603 | 2.066e-03 | 0.0231004765 | +4.77e-06 | +0.751 | +4.78e-06 |
| 250 | 470.77 | 0.0213012125 | 1.797e-03 | 0.0230985673 | +2.86e-06 | +0.633 | +2.86e-06 |
| 300 | 541.85 | 0.0214961899 | 1.603e-03 | 0.0230990869 | +3.38e-06 | +0.992 | +3.38e-06 |

Ladder spread of S+A: **3.0e-06**.

n=2 (ref = Keiper–Taylor 0.092345735228):

| k | T_k | S(T_k) | A(T_k) | S+A | (S+A)−ref | S_osc(T_k) | f(T)·S_osc |
|---|------|------------|----------|------------|----------|------|------|
| 100 | 236.52 | 0.0799023248 | 1.246e-02 | 0.0923593438 | +1.36e-05 | +0.190 | +1.36e-05 |
| 150 | 318.85 | 0.0825322549 | 9.837e-03 | 0.0923691744 | +2.34e-05 | +0.596 | +2.34e-05 |
| 200 | 396.38 | 0.0841023444 | 8.262e-03 | 0.0923648090 | +1.91e-05 | +0.751 | +1.91e-05 |
| 250 | 470.77 | 0.0851677517 | 7.189e-03 | 0.0923571711 | +1.14e-05 | +0.633 | +1.14e-05 |
| 300 | 541.85 | 0.0859476604 | 6.412e-03 | 0.0923592484 | +1.35e-05 | +0.992 | +1.35e-05 |

Ladder spread of S+A: **1.2e-05**.

No systematic drift at any rung. Moreover, at every rung the residual
(S+A)−ref equals the directly measured boundary oscillatory term
f(T_k)·S_osc(T_k) to the printed precision — the entire remaining error is
accounted for, not merely bounded.

## 2. Observed-vs-predicted gap — MARGINAL PASS, fully accounted

Gap S(300)−S(150) (pure data) vs analytic smooth integral over [T₁₅₀,T₃₀₀]:

| | observed | predicted | |obs−pred|/obs |
|---|---|---|---|
| n=1 | 8.5385272351e-04 | 8.5633289455e-04 | 2.90e-03 |
| n=2 | 3.4154055657e-03 | 3.4253315782e-03 | 2.91e-03 |

~2.5 significant figures (bar was ~3). The 0.29% miss is not unexplained:
obs−pred = −2.48e-06 (n=1) equals exactly the boundary-term difference
f(T₁₅₀)S_osc(T₁₅₀) − f(T₃₀₀)S_osc(T₃₀₀) = 5.86e-06 − 3.38e-06. The smooth
model's interval prediction is good to the measured oscillation; no hidden
bias.

## 3. Residual decomposition at k=300 — the reported residuals were self-inflicted

| | n=1 | n=2 |
|---|---|---|
| true tail (ref − S) | 1.599519e-03 | 6.398075e-03 |
| script-style tail (trapz to T×50 / T×100) | 1.547857e-03 | 6.293363e-03 |
| analytic tail (closed form) | 1.602897e-03 | 6.411588e-03 |
| integration-cutoff bias (analytic − script) | **+5.504e-05** | **+1.182e-04** |
| oscillatory residual (true − analytic) | −3.378e-06 | −1.351e-05 |
| reported residual | −5.166e-05 | −1.047e-04 |
| analytic residual | **+3.378e-06** | **+1.351e-05** |

The original scripts' log-spaced trapezoidal tail integration, cut at
T×50 (n=1) / T×100 (n=2), silently dropped 3.4% / 1.8% of the tail —
+5.5e-05 / +1.18e-04. That cutoff artifact accounts for essentially the
**entire** reported residual in both cases. With the closed-form tail the
n=1 residual is 3.4e-06 (15× smaller than reported) and n=2 is 1.35e-05
(8× smaller). The zero distribution beyond T=541.8 is, if anything, better
behaved than the smooth model needed it to be.

## Verdict

- **Error bars ±5e-05 (n=1) / ±1e-4 (n=2): HONEST but ~10× conservative.**
  The reported residuals were inside them, and the ladder shows no drift
  (spreads 3.0e-06 / 1.2e-05). True methodology error with the analytic tail
  is ~3–6e-06 (n=1), ~1–2.5e-05 (n=2).
- **Drift: none.** S+A is T_k-independent across 100–300 zeros; every rung's
  residual is exactly the measured boundary oscillatory term.
- **Methodology blemish (recorded, not hidden):** the worked-case scripts'
  numerical tail integration carried an uncontrolled truncation bias that
  dominated their reported residuals. Anyone reusing `worked_n1.py` /
  `worked_n2.py` tail code should use the closed forms A₁/A₂ above.

## Epistemic labels

| Claim | Status |
|---|---|
| Ladder S+A T_k-independent (spread 3.0e-06 / 1.2e-05) | computationally verified |
| Residual = f(T_k)·S_osc(T_k) at every rung | computationally verified |
| Cutoff bias +5.5e-05 / +1.18e-04 in script tails | computationally verified |
| Gap test ~2.5 sig figs, miss = boundary-term difference | computationally verified |
| Analytic-tail residuals 3.4e-06 / 1.35e-05 | computationally verified |
| Dropped model corrections (1/g² approx, O(1/g) density) negligible | analytic bound (~1e-9 / ~3e-7) |
