#!/usr/bin/env python3
"""Localized windows h_{T,sig}(r) = exp(-(r-T)^2/2sig^2)+exp(-(r+T)^2/2sig^2).
W(h) via PRIME SIDE ONLY (pole + archimedean - prime sum), D10a-step2
normalization. Zero side afterwards as cross-check only.
Pre-registration: ../WINDOWS.md section 1 (written before this ran).
"""
import json, math
import numpy as np
import mpmath

mpmath.mp.dps = 30
SQRT2OPI = math.sqrt(2.0 / math.pi)

# ---------- prime powers to N (Lambda(n) = log p for n = p^k) ----------
def prime_powers(N):
    bs = bytearray(b"\x01") * (N + 1)
    bs[0:2] = b"\x00\x00"
    for i in range(2, int(N ** 0.5) + 1):
        if bs[i]:
            bs[i * i:N + 1:i] = b"\x00" * (((N - i * i) // i) + 1)
    out = []
    for p in range(2, N + 1):
        if bs[p]:
            q, lp = p, math.log(p)
            while q <= N:
                out.append((q, lp))
                q *= p
    out.sort()
    return out

N = 500000
PP = prime_powers(N)
ns = np.array([q for q, lp in PP], dtype=np.float64)
lps = np.array([lp for q, lp in PP], dtype=np.float64)
logns = np.log(ns)
ninvsqrt = ns ** -0.5
print(f"{len(PP)} prime powers to {N}", flush=True)

# ---------- zeros for cross-check only (li_check cache, 300 zeros) ----------
with open("../li_check/zeros_cache.json") as f:
    zc = json.load(f)
gammas = np.array([g for s, g in zc if g > 0], dtype=np.float64)
print(f"{len(gammas)} positive zeros, max {gammas.max():.1f}", flush=True)

def h_window(r, T, sig):
    return np.exp(-(r - T) ** 2 / (2 * sig ** 2)) + np.exp(-(r + T) ** 2 / (2 * sig ** 2))

def prime_side(T, sig):
    # pole: exact form (pre-reg 1.2); mpmath for the tiny exponent
    expo = -(T * T - 0.25) / (2 * sig * sig)
    pole = float(4 * mpmath.exp(expo) * mpmath.cos(T / (2 * sig * sig)))
    # archimedean: (1/pi) int_0^inf h(r)[Re psi(1/4+ir/2) - log pi] dr
    logpi = mpmath.log(mpmath.pi)
    Tm, Ts = mpmath.mpf(T), mpmath.mpf(sig)
    def f(r):
        rr = float(r)
        hh = math.exp(-(rr - T) ** 2 / (2 * sig ** 2)) + math.exp(-(rr + T) ** 2 / (2 * sig ** 2))
        return hh * (mpmath.re(mpmath.digamma(mpmath.mpc(0.25, 0.5 * r))) - logpi)
    lo = max(0.0, T - 12 * sig)
    hi = T + 12 * sig
    mid = mpmath.quad(f, [lo, hi])
    outer = mpmath.quad(f, [0, lo]) + mpmath.quad(f, [hi, mpmath.inf]) if lo > 0 else mpmath.quad(f, [hi, mpmath.inf])
    arch = float((mid + outer) / mpmath.pi)
    # prime sum: 2*sig*sqrt(2/pi) * sum Lambda(n) n^-1/2 e^{-sig^2 (log n)^2/2} cos(T log n)
    env = np.exp(-sig * sig * logns * logns / 2.0)
    terms = 2 * sig * SQRT2OPI * lps * ninvsqrt * env * np.cos(T * logns)
    psum = float(np.sum(terms))
    # analytic tail bound (pre-reg 1.3)
    U = math.log(N)
    tail = 2 * sig * SQRT2OPI * math.exp(-sig * sig * U * U / 4.0) * 1.0
    W = pole + arch - psum
    return dict(T=T, sig=sig, pole=pole, arch=arch, psum=psum, W=W,
                tail_bound=tail, n_terms=len(PP))

def zero_side(T, sig):
    # cross-check only: sum over rho of h(gamma_rho); h even -> 2*sum_{gamma>0}
    return float(2 * np.sum(h_window(gammas, T, sig)))

results = []
for T, sig in [(14, 0.5), (25, 0.5), (50, 0.5), (100, 0.5), (200, 0.5), (100, 1.0)]:
    r = prime_side(T, sig)
    z = zero_side(T, sig)
    r["W_zero"] = z
    r["abs_diff"] = abs(r["W"] - z)
    smooth = 2 * sig * math.log(T / (2 * math.pi)) / math.sqrt(2 * math.pi)
    r["smooth_est"] = smooth
    results.append(r)
    print(f"T={T:>3} sig={sig}: W_prime={r['W']:.8f} W_zero={z:.8f} "
          f"|d|={r['abs_diff']:.2e} arch={r['arch']:.6f} psum={r['psum']:.6f} "
          f"pole={r['pole']:.1e} tail<{r['tail_bound']:.1e} smooth~{smooth:.3f}",
          flush=True)

with open("windows_numbers.json", "w") as f:
    json.dump(results, f, indent=1)
print("wrote windows_numbers.json", flush=True)
