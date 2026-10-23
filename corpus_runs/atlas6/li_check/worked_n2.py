#!/usr/bin/env python3
"""WORKED_N2: lambda_2 three-leg check.

h_2(x) = (2+log x)*1_{(0,1]}, hhat_2(s) = 1-(1-1/s)^2 = 2/s - 1/s^2.
Zero side (symmetric, rho <-> rhobar): lambda_2 = sum_{gamma>0} 4g^2/(1/4+g^2)^2.
Keiper-Taylor via Stieltjes constants (li_criterion.py Part A machinery, dps=80).
Closed-form anchor: recollection lambda_2 ~= 0.0923457 -- CONFIRM by computation.

Naive W-side epsilon-regularization is NOT repeated (established diverging in n=1).
"""
import math, json, os
import mpmath
import numpy as np

mpmath.mp.dps = 50
LI_DIR = os.path.dirname(os.path.abspath(__file__))
ZCACHE = os.path.join(LI_DIR, 'zeros_cache.json')
OUT = os.path.join(LI_DIR, 'worked_n2_numbers.json')

def get_zeros(n):
    zs = []
    if os.path.exists(ZCACHE):
        zs = [complex(*p) for p in json.load(open(ZCACHE))]
    if len(zs) < n:
        print(f"computing zeros {len(zs)+1}..{n} ...", flush=True)
        for k in range(len(zs)+1, n+1):
            zs.append(complex(mpmath.zetazero(k)))
            if k % 25 == 0:
                print(f"  {k}/{n}", flush=True)
                json.dump([[z.real, z.imag] for z in zs], open(ZCACHE, 'w'))
        json.dump([[z.real, z.imag] for z in zs], open(ZCACHE, 'w'))
    return zs[:n]

numbers = {}

# ---------- Leg 1: zero side ----------
print("=" * 70)
print("Leg 1: zero side  lambda_2 = sum_{gamma>0} 4g^2/(1/4+g^2)^2")
print("=" * 70)
zeros = get_zeros(300)
gammas = sorted(z.imag for z in zeros if z.imag > 0)
T = gammas[-1]
S = math.fsum(4*g*g/((0.25+g*g)**2) for g in gammas)
# tail: numerical integral of term(g)*dN, dN=(1/2pi)ln(g/2pi)dg, log-spaced
N = 40000
a, b = T, T*100
gs = np.exp(np.linspace(math.log(a), math.log(b), N))
vals = (4*gs*gs/((0.25+gs*gs)**2)) * (1.0/(2*math.pi))*np.log(gs/(2*math.pi))
te = float(np.trapz(vals, gs))
# strict analytic upper bound: term < 4/g^2
bound = (2.0/math.pi)*(math.log(T/(2*math.pi))/T + 1.0/T)
print(f"N zeros: {len(gammas)}, T = {T:.1f}")
print(f"S(T)            = {S:.10f}")
print(f"tail (integral) = {te:.3e}")
print(f"tail (bound)    = {bound:.3e}")
print(f"S(T)+tail       = {S+te:.10f}")
numbers['zero_side'] = {'N': len(gammas), 'T': T, 'S': S, 'tail': te,
                        'bound': bound, 'Stail': S+te}
# cross-check pair-sum algebra on first 3 zeros
for g in gammas[:3]:
    s = complex(0.5, g)
    direct = 2*(1-(1-1/s)**2).real
    simp = 4*g*g/((0.25+g*g)**2)
    assert abs(direct-simp) < 1e-12, (g, direct, simp)
print("pair-sum algebra cross-check OK")

# ---------- Leg 2: Keiper-Taylor (Stieltjes, no zeros) ----------
print("=" * 70)
print("Leg 2: Keiper-Taylor via Stieltjes constants (dps=80)")
print("=" * 70)
mpmath.mp.dps = 80
NN = 40
c = [mpmath.mpf(1)] + [(-1)**(j-1)*mpmath.stieltjes(j-1)/math.factorial(j-1)
                       for j in range(1, NN+1)]
d = [mpmath.mpf(0)]*(NN+1)
for k in range(1, NN+1):
    d[k] = c[k] - sum(mpmath.mpf(j)/k*d[j]*c[k-j] for j in range(1, k))
l = [mpmath.mpf(0)]*(NN+1)
l[0] = -mpmath.log(2); logpi = mpmath.log(mpmath.pi)
for k in range(1, NN+1):
    lk = (-1)**(k+1)/k + d[k]
    if k == 1:
        lk += -logpi/2
    lk += mpmath.polygamma(k-1, mpmath.mpf('0.5'))/(math.factorial(k)*2**k)
    l[k] = lk
lam = {}
for n in range(1, NN+1):
    m = sum(l[k]*math.comb(n-1, k-1) for k in range(1, n+1))
    lam[n] = n*m
lam2 = lam[2]
print(f"lambda_2 (Keiper-Taylor, dps=80) = {lam2}")
print(f"  float: {float(lam2):.12f}")
numbers['keiper_taylor'] = {'lambda_2_str': str(lam2), 'lambda_2': float(lam2),
                            'lambda_1_check': float(lam[1])}
print(f"lambda_1 sanity (expect 0.023095708966): {float(lam[1]):.12f}")

# ---------- Leg 3: closed-form anchor ----------
print("=" * 70)
print("Leg 3: recollection lambda_2 ~= 0.0923457")
print("=" * 70)
recol = 0.0923457
diff = abs(float(lam2)-recol)
print(f"|Keiper - 0.0923457| = {diff:.2e}  ->  {'CONFIRMED' if diff < 1e-6 else 'MISMATCH'}")
numbers['recollection'] = {'value': recol, 'diff': diff,
                           'confirmed': bool(diff < 1e-6)}

# ---------- comparison ----------
print("=" * 70)
print("Comparison")
print("=" * 70)
zs_val = S+te
kt_val = float(lam2)
print(f"zero side (+tail) : {zs_val:.10f}")
print(f"Keiper-Taylor     : {kt_val:.10f}")
print(f"|zero - Keiper|   = {abs(zs_val-kt_val):.2e}  (tail-dominated)")
print(f"|zero - recol|    = {abs(zs_val-recol):.2e}")
json.dump(numbers, open(OUT, 'w'), indent=1)
print(f"numbers -> {OUT}")
