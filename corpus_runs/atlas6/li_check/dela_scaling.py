#!/usr/bin/env python3
"""De la Vallee-Poussin scaling test: D = exp(c/eps) or polynomial?

Decomposition (exact):
  Phi_eps(s) - 1/s = -eps^s/s - eps^s * E1_tilde(s) - Dfall(s,eps)
where
  -eps^s/s            : sharp cutoff at x=eps  -> defect Dsharp (elementary)
  -eps^s*E1_tilde(s)  : rise smoothstep        -> defect Erise  (O(sqrt(eps)), negligible)
  -Dfall(s,eps)       : fall smoothstep at x=1 -> defect Efall  (THE divergent piece)

Numerics show Dsharp is small (+-0.05) and low-T. Prediction: Efall(T) grows
like -eps*N(T) up to T ~ 1/eps then saturates at -c1*log(1/eps). So the
divergent mass sits at T_*(eps) ~ const/eps (POLYNOMIAL), not exp(c/eps).

This script computes Efall(T) = -2 Re sum_{0<g<=T} Dfall(1/2+ig) via
cancellation-free Gauss-Legendre quadrature (K_m formulation), extracts
T_half(eps) and T_conv(eps), and fits exp(c/eps) vs polynomial models.
"""
import math, json, os
import numpy as np
import mpmath
mpmath.mp.dps = 40

LI_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- exact reference machinery (from worked_n1.py, mpmath) ----------
from math import comb

def tpoly_to_xpoly(d, x0, w):
    deg = len(d) - 1
    c = [mpmath.mpf(0)] * (deg + 1)
    for j, dj in enumerate(d):
        if dj == 0:
            continue
        for m in range(j + 1):
            c[m] += mpmath.mpf(dj) * comb(j, m) * ((-x0) ** (j - m)) / (mpmath.mpf(w) ** j)
    return c

def F_eps_pieces(eps):
    eps = mpmath.mpf(eps)
    d_ss = [mpmath.mpf(0)] * 8
    d_ss[4] = 35; d_ss[5] = -84; d_ss[6] = 70; d_ss[7] = -20
    d_fall = [mpmath.mpf(1), 0, 0, 0, -35, 84, -70, 20]
    return [
        (eps, 2 * eps, tpoly_to_xpoly(d_ss, eps, eps)),
        (2 * eps, 1 - eps, [mpmath.mpf(1)]),
        (1 - eps, mpmath.mpf(1), tpoly_to_xpoly(d_fall, 1 - eps, eps)),
    ]

def Phi_eps(s, pieces):
    s = mpmath.mpc(s)
    tot = mpmath.mpc(0)
    for a, b, c in pieces:
        for m, cm in enumerate(c):
            if cm == 0:
                continue
            tot += cm * (mpmath.power(b, s + m) - mpmath.power(a, s + m)) / (s + m)
    return tot

# smoothstep S(u) = 35u^4-84u^5+70u^6-20u^7 ; fall defect uses S (1-F = S on fall piece)
S_COEF = np.array([0, 0, 0, 0, 35, -84, 70, -20], dtype=float)
MS = np.nonzero(S_COEF)[0]

NQ = 1024
_t, _w = np.polynomial.legendre.leggauss(NQ)
U = 0.5 * (_t + 1)                 # (NQ,) nodes on (0,1)
WQ = 0.5 * _w                     # (NQ,) weights
UM = U[:, None] ** np.arange(8)[None, :]   # (NQ,8)
V = 1 - U                         # (NQ,)


def Dfall_vec(gammas, eps):
    """Dfall(1/2+i*g) = eps * sum_m s_m * L_m(g), L_m = int_0^1 u^m (1-eps(1-u))^{-1/2+ig} du."""
    gammas = np.asarray(gammas, dtype=float)
    base = 1 - eps * V                      # (NQ,), in (0,1]
    logb = np.log(base)                     # (NQ,)
    # phase = base^{-1/2 + i g} = exp((-1/2+ig)*logb)
    ph = np.exp((-0.5 + 1j * gammas[:, None]) * logb[None, :])   # (G,NQ)
    L = np.einsum('gq,qm->gm', ph * WQ[None, :], UM)              # (G,8)
    return eps * (L[:, MS] @ S_COEF[MS])                          # (G,) complex


def Dfall_ref(g, eps):
    """mpmath reference: direct quadrature of the fall-defect integral."""
    s = mpmath.mpc(0.5, g)
    f = mpmath.quad(lambda x: (35*((x-(1-eps))/eps)**4 - 84*((x-(1-eps))/eps)**5
                               + 70*((x-(1-eps))/eps)**6 - 20*((x-(1-eps))/eps)**7)
                               * mpmath.power(x, s - 1), [1 - eps, 1])
    return complex(f)


def main():
    zeros = np.array(sorted(p[1] for p in json.load(
        open(os.path.join(LI_DIR, 'zeros_cache.json'))) if p[1] > 0))
    T_MAX = zeros[-1]
    print(f"zeros: {len(zeros)}, T_max = {T_MAX:.1f}", flush=True)

    # ---- validation of Dfall quadrature vs mpmath ----
    print("validating Dfall quadrature vs mpmath...", flush=True)
    for eps in [0.2, 0.05, 0.0125]:
        for g in [14.134725141734695, 500.0, 1500.0]:
            got = Dfall_vec(np.array([g]), eps)[0]
            ref = Dfall_ref(g, eps)
            print(f"  eps={eps} g={g:8.1f} diff={abs(got-ref):.2e}", flush=True)

    lam1_exact = 1 + float(mpmath.euler) / 2 - 0.5 * math.log(4 * math.pi)
    C_cum = np.cumsum(2 * 0.5 / (0.25 + zeros * zeros))
    print(f"C(T_max) = {C_cum[-1]:.10f}  (lam_1 = {lam1_exact:.10f})", flush=True)

    EPS_LIST = [0.2, 0.1, 0.05, 0.025, 0.0125]
    W_TABLE = {0.2: -0.153, 0.1: -0.373, 0.05: -0.701, 0.025: -1.011}

    results = {}
    curves = {}
    for eps in EPS_LIST:
        print(f"\neps = {eps} ...", flush=True)
        # Efall(T) = -2 Re sum_{0<g<=T} Dfall(1/2+ig)   [the divergent piece]
        Df = Dfall_vec(zeros, eps)
        Efall = -2 * np.cumsum(Df).real
        # S_eps(T) = C(T) + Efall(T) + E_A(T); E_A = O(sqrt(eps)), low-T, neglected
        # (validated against mpmath exact below)
        S_approx = C_cum + Efall
        S_final = float(S_approx[-1])
        Ef = float(Efall[-1])
        # T_half: first T with |Efall| >= |Efall_final|/2
        T_half = None
        for g, e in zip(zeros, Efall):
            if abs(e) >= abs(Ef) / 2:
                T_half = float(g)
                break
        # T_conv(tol)
        for tol in [0.001, 0.0001]:
            key = f'T_conv_{tol:g}'
            T_conv = None
            worst = 0.0
            for i in range(len(zeros) - 1, -1, -1):
                dev = abs(S_approx[i] - S_final)
                if dev > worst:
                    worst = dev
                if worst >= tol:
                    T_conv = float(zeros[min(i + 1, len(zeros) - 1)])
                    break
            results.setdefault(eps, {})[key] = T_conv
        # fractions of Efall_final
        T_frac = {}
        for frac in [0.25, 0.5, 0.75, 0.9]:
            Tq = None
            for g, e in zip(zeros, Efall):
                if abs(e) >= abs(Ef) * frac:
                    Tq = float(g)
                    break
            T_frac[frac] = Tq
        results[eps] = dict(results.get(eps, {}), S_final=S_final,
                            Efall_final=Ef, T_half=T_half,
                            T_frac=T_frac, W_ref=W_TABLE.get(eps))
        step = max(1, len(zeros) // 500)
        curves[str(eps)] = [[float(zeros[i]), float(Efall[i])]
                            for i in range(0, len(zeros), step)]
        print(f"  S_final(C+Efall)={S_final:.6f} (W_ref prime side={W_TABLE.get(eps)}), "
              f"Efall_final={Ef:.4f}", flush=True)
        print(f"  T_half={T_half}, T_frac={T_frac}", flush=True)

    json.dump(results, open(os.path.join(LI_DIR, 'dela_scaling_numbers.json'), 'w'), indent=1)
    json.dump(curves, open(os.path.join(LI_DIR, 'dela_scaling_curves.json'), 'w'))

    # ---- validation: C + Efall vs exact full S_eps on a subset of zeros ----
    print("\n" + "=" * 70)
    print("Validation: (C + Efall) vs exact mpmath S_eps on subset")
    print("=" * 70)
    # (F_eps_pieces / Phi_eps defined at module top level)
    sub_idx = [0, 4, 19, 49, 99, 199, 399, 799, len(zeros) - 1]
    sub_idx = sorted(set(i for i in sub_idx if i < len(zeros)))
    for eps in [0.1, 0.025]:
        pieces = F_eps_pieces(eps)
        Df = Dfall_vec(zeros, eps)
        Efall = -2 * np.cumsum(Df).real
        maxdiff = 0.0
        for i in sub_idx:
            g = float(zeros[i])
            exact = 2 * float(mpmath.re(Phi_eps(mpmath.mpc(0.5, g), pieces)))
            approx = 2 * 0.5 / (0.25 + g * g) - 2 * float(Df[i].real)
            # note: exact h_eps(g) vs [h(g) - Dfall term]; diff = E_A per-zero + quad err
            maxdiff = max(maxdiff, abs(exact - approx))
        print(f"  eps={eps}: max|exact h_eps - (h - Dfall)| over {len(sub_idx)} zeros = {maxdiff:.2e}",
              flush=True)

    print("\n" + "=" * 70)
    print("Scaling fits")
    print("=" * 70)
    print(f"{'eps':>8} {'T_half':>10} {'T_c(1e-3)':>10} {'T_c(1e-4)':>10} "
          f"{'Efall_fin':>10} {'1/eps':>8}")
    for e in EPS_LIST:
        r = results[e]
        print(f"{e:>8} {str(r['T_half']):>10} {str(r['T_conv_0.001']):>10} "
              f"{str(r['T_conv_0.0001']):>10} {r['Efall_final']:>10.4f} {1/e:>8.0f}")

    def linfit(px, py):
        n = len(px)
        mx, my = sum(px) / n, sum(py) / n
        sxy = sum((x - mx) * (y - my) for x, y in zip(px, py))
        sxx = sum((x - mx) ** 2 for x in px)
        b = sxy / sxx
        a = my - b * mx
        ss = sum((y - (a + b * x)) ** 2 for x, y in zip(px, py))
        return a, b, ss

    for key in ['T_half', 'T_conv_0.001', 'T_conv_0.0001']:
        pts = [(e, results[e][key]) for e in EPS_LIST if results[e][key] is not None]
        if len(pts) < 3:
            print(f"{key}: too few points")
            continue
        px = [1 / e for e, _ in pts]
        py = [math.log(t) for _, t in pts]
        a1, b1, ss1 = linfit(px, py)
        px2 = [math.log(1 / e) for e, _ in pts]
        a2, b2, ss2 = linfit(px2, py)
        print(f"\n{key}:")
        print(f"  exp model   log T = {b1:.4f}/eps + {a1:.4f}  (c={b1:.4f}), rss={ss1:.4f}")
        print(f"  poly model  log T = {b2:.4f}*log(1/eps)+{a2:.4f}, rss={ss2:.4f}")
        rr = max(ss1, ss2) / max(min(ss1, ss2), 1e-12)
        print(f"  better: {'exp' if ss1 < ss2 else 'poly'} (rss ratio {rr:.1f}x)")
    # direct: T_frac[0.5] vs 1/eps linear fit (tests T_* ~ const/eps)
    pts = [(e, results[e]['T_frac'][0.5]) for e in EPS_LIST
           if results[e]['T_frac'][0.5] is not None]
    if len(pts) >= 3:
        px = [1 / e for e, _ in pts]
        py = [t for _, t in pts]
        a, b, ss = linfit(px, py)
        print(f"\nT_frac[0.5] = {b:.3f}/eps + {a:.1f}, rss={ss:.1f} "
              f"-> T_* ~ {b:.2f}/eps")


if __name__ == '__main__':
    main()
