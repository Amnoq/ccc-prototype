# Localized-window family h_{T,σ} — prime-side sign probe

**Date:** 2026-10-09. **Status:** pre-registration recorded below; computation not yet run.
**Analyst:** subagent (parent: main agent). Read-only on atlas records and
`prime-sieve-geometry/`; new work only in `a3_test/` (this file, `windows_run.py`).

## 0. Context

Gaussians fail as sign probes: W(h_a) ≈ 2e^{−aγ₁²} is tiny with cancelling
terms (A3 REPORT §5; D1_FACE_LATTICE). Reviewer proposal (sign-off 2026-10-09):
use localized windows h_{T,σ}(r) = e^{−(r−T)²/(2σ²)} + e^{−(r+T)²/(2σ²)} —
in the same cone as the pilot's squares and Weil's squares per the sign-off's
Fourier-duality argument (reviewer's claim, not independently verified here).
Signal should be order 1, prime side well-conditioned.

Machinery: symmetric Guinand–Weil, D10a-step2 normalization (A3 REPORT §3,
`prime-sieve-geometry/weil_positivity.py`):
W(h) = [h(i/2)+h(−i/2)] + (1/π)∫_0^∞ h(r)[Re ψ(1/4+ir/2)−log π]dr
       − 2Σ_{n≥2} Λ(n)n^{−1/2}g(log n),
g(u) = (1/2π)∫h(r)e^{−iru}dr. PRIME SIDE ONLY for W; zero side computed
afterwards as cross-check, never as input.

## 1. PRE-REGISTERED PREDICTION (recorded BEFORE computation)

### 1.1 Fourier pair (derived, not assumed)

For one shifted Gaussian, ∫e^{−(r−T)²/(2σ²)}e^{−iru}dr = e^{−iTu}·σ√(2π)·e^{−σ²u²/2}.
Summing both shifts and applying the (1/2π) convention:

    g(u) = σ√(2/π) · e^{−σ²u²/2} · cos(Tu),

i.e. the reviewer's "∝ σe^{−σ²u²/2}cos(Tu)" with constant √(2/π) ≈ 0.79788.
Sanity: T→0 gives g = 2σ/√(2π)·e^{−σ²u²/2}, twice the single-Gaussian pair. ✓

### 1.2 Pole term (derived)

h(i/2) = e^{−(T²−1/4−iT)/(2σ²)} + e^{−(T²−1/4+iT)/(2σ²)}
       = 2e^{−(T²−1/4)/(2σ²)}cos(T/(2σ²)); h(−i/2) identical. Hence

    pole = 4·e^{−(T²−1/4)/(2σ²)}·cos(T/(2σ²)).

Numerically ~0 at every test point (at σ=1/2, T=14: e^{−391.5} ≈ 10^{−170}).
Pre-registered: the code computes it exactly; expect 0.0 in float.

### 1.3 Prime-sum shape and cutoff

    psum = 2·σ√(2/π)·Σ_{n≥2} Λ(n)·n^{−1/2}·e^{−σ²(log n)²/2}·cos(T·log n),

W = pole + arch − psum. Envelope e^{−σ²(log n)²/2} dead once log n ≳ 6/σ
(e^{−18} ≈ 1.5×10^{−8}): at σ=1/2, n ≲ e^{12} ≈ 1.6×10⁵. Sum prime powers
to N = 500000 (existing sieve list extended); analytic tail bound for n > N:
for u ≥ U = log N, e^{−σ²u²/2} ≤ e^{−σ²U²/4}·n^{−σ²U/4}, so
tail ≤ 2σ√(2/π)·e^{−σ²U²/4}·Σ_{n>N}Λ(n)n^{−1/2−σ²U/4}.
At σ=1/2, U=13.12: e^{−10.76} ≈ 2.1×10^{−5}, exponent 1.288, Σ ≲ 1 →
tail ≲ 1.7×10^{−5} absolute. Resolved signal is order 1: well-conditioned.

### 1.4 Signal-size estimate (reviewer's, to VERIFY not trust)

Zero side on RH: Σ_ρ h(γ_ρ) ≈ 2·∫_0^∞ e^{−(γ−T)²/(2σ²)}·(1/2π)log(T/2π)dγ
= 2σ·log(T/2π)/√(2π). Predicted smooth values:

| T | σ | smooth 2σ·log(T/2π)/√(2π) |
|---|---|---|
| 14 | 1/2 | 0.32 |
| 25 | 1/2 | 0.55 |
| 50 | 1/2 | 0.83 |
| 100 | 1/2 | 1.10 |
| 200 | 1/2 | 1.38 |
| 100 | 1 | 2.21 |

CAVEAT (pre-registered): the smooth estimate is asymptotic; at small T the
discrete zeros dominate. From the known zeros: at T=14, γ₁=14.1347 sits in
the window → expect zero side ≈ 2·e^{−(0.1347)²/0.5} ≈ 1.93. At T=25,
γ=25.0109 → ≈ 2.00. At T=50, γ=49.7738 → 2·e^{−(0.2262)²/0.5} ≈ 1.81
(next zero 52.97 contributes ~0). The PRIME side must reproduce these
without any zero input — that is the test.

### 1.5 Falsifiability

- **Sign:** W must be positive at every T. These heights are far below the
  RH verification bound (3×10¹²); a negative prime-side W at any T ≤ 200
  would be a major finding (contradicts verified RH). None expected.
- **Agreement:** prime-side W vs zero-side cross-check: expect |Δ| ≲ 10^{−4}
  absolute (tail bound + float + arch quadrature). |Δ| > 10^{−3} means a bug.
- **Estimate check:** the smooth column above should track the computed
  values qualitatively, improving with T; the discrete predictions (1.93,
  2.00, 1.81 at T=14,25,50) are the sharp pre-registered numbers.

## 2. Results

Script: `windows_run.py` (this directory). Numbers: `windows_numbers.json`.
Prime powers to 500000 (41,724 terms). Zeros: li_check 300-zero cache
(cross-check only). mpmath 30 dps for the archimedean integral.

| T | σ | W (prime side) | W (zero side) | |Δ| | arch | psum | pole | smooth est |
|---|---|---|---|---|---|---|---|---|---|
| 14 | 0.5 | 1.92869854 | 1.92869856 | 1.7e-08 | 0.319285 | −1.609414 | −3.6e-170 | 0.320 |
| 25 | 0.5 | 1.99952850 | 1.99952851 | 9.5e-09 | 0.550832 | −1.448696 | 0 | 0.551 |
| 50 | 0.5 | 1.80621021 | 1.80621021 | 2.5e-09 | 0.827438 | −0.978772 | 0 | 0.827 |
| 100 | 0.5 | 0.19216907 | 0.19216906 | 2.0e-09 | 1.103984 | 0.911815 | 0 | 1.104 |
| 200 | 0.5 | 0.08235601 | 0.08235600 | 1.2e-09 | 1.380514 | 1.298158 | 0 | 1.381 |
| 100 | 1.0 | 1.85175388 | 1.85175388 | 2.2e-16 | 2.207937 | 0.356183 | 0 | 2.208 |

W = pole + arch − psum throughout (pole numerically zero as pre-registered).

### 2.1 Against the pre-registration

- **Fourier pair — CONFIRMED in use.** The derived g(u) = σ√(2/π)e^{−σ²u²/2}cos(Tu)
  drove the prime sum; prime-zero agreement to 1e-8–1e-16 validates the entire
  chain (pair, pole, arch, prime sum) end to end.
- **Pole — CONFIRMED ~0.** Computed −3.6e-170 at (14, 0.5); 0.0 elsewhere.
- **Cutoff/tail — CONFIRMED adequate.** Analytic tail bound 1.7e-05 (σ=0.5),
  3.2e-19 (σ=1.0); observed |Δ| is 1e-8–1e-16, far inside the bound.
- **Signal estimate — CORRECTED (verify-don't-trust applied).** The smooth
  asymptotic 2σ·log(T/2π)/√(2π) tracks the ARCHIMEDEAN term to ~3 digits
  (arch 1.103984 vs smooth 1.104 at T=100) — it is the smooth density, as it
  should be. It does NOT predict the zero side at narrow σ: local zero
  lumpiness dominates. The sharp pre-registered DISCRETE predictions all hit:
  T=14 → 1.9287 (predicted ≈1.93 from γ₁), T=25 → 1.9995 (predicted ≈2.00),
  T=50 → 1.8062 (predicted ≈1.81). At T=100, σ=0.5 the window sits in a local
  zero gap (W ≈ 0.19, not ~1.1); at σ=1.0 the wider window averages it out
  (1.85 vs smooth 2.21). The reviewer's "order 1 to 3 at T=100" stands as an
  order-of-magnitude envelope, not a point prediction.
- **Falsifiability — passed.** Sign positive at all six points (no RH
  contradiction at verified heights). |Δ| ≤ 1.7e-08 ≪ 1e-3 bug threshold.
  The zero-side cross-check is self-validating: had the 300-zero cache missed
  zeros inside a window, the prime side (no zero input) would have disagreed.

### 2.2 The local-density picture

The prime side reproduces the zero lumps with no zero input — this is the
explicit formula as a local zero-density probe, exactly the reviewer's
intent. At T=100, σ=0.5: arch (smooth, 1.104) minus prime sum (0.912) leaves
0.192 — the prime sum "knows" about the local zero gap. Sweeping T maps
local density; the signal stays order 0.1–2, every term order 1, no
catastrophic cancellation (contrast the Gaussian a=0.5 case: signal 10^{−44}).

## 3. Verdict

**The family resolves the sign where Gaussians couldn't — computationally
verified.** Prime-side W is well-conditioned (signal 0.08–2.0, tail < 2e-05,
prime-zero agreement 1e-8–1e-16), positive at every probed height, and tracks
local zero density without zero input.

**What it establishes:** a clean, well-conditioned prime-side sign probe at
verified heights; the T-sweep is a genuine local-density measurement.
**What it cannot establish:** anything about RH — at T ≤ 200 ≪ 3×10¹²,
positivity is expected (consistency check only); nothing about Item 2 (no
signature theorem, no space V with zero-free signature proof); nothing about
the Li cone question. It replaces a family that cannot resolve the sign with
one that can, and that is all it does.

## Epistemic summary

| Claim | Label |
|---|---|
| Fourier pair g(u) = σ√(2/π)e^{−σ²u²/2}cos(Tu) | exact theorem (derived §1.1) |
| Pole = 4e^{−(T²−1/4)/(2σ²)}cos(T/(2σ²)) | exact theorem |
| Prime-side W values (6 points) | computationally verified |
| Prime-zero agreement 1e-8–1e-16 | computationally verified |
| Discrete pre-registered predictions (1.93/2.00/1.81) | confirmed |
| Smooth estimate as asymptotic envelope | heuristic (corrected §2.1) |
| Sign positive at all T | computationally verified |
| "Consistency check only, not RH evidence" | exact argument |
| Cone membership of h_{T,σ} | reviewer's claim, not verified here |
