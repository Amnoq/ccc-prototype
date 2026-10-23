#!/usr/bin/env python3
"""TAIL_CHECK: validate the 300-zero tail-correction methodology of WORKED_N1/N2.

1. Truncation ladder: S(T_k)+tail at k = 100,150,200,250,300 for n=1 and n=2,
   using an ANALYTIC smooth-density tail (closed form, no integration cutoff).
2. Observed-vs-predicted gap: S(300)-S(150) vs analytic integral over [T150,T300].
3. Residual decomposition: reproduce the original scripts' numerical tail
   (log-spaced trapz to T*50 / T*100) to isolate their integration-cutoff bias;
   show the boundary oscillatory term f(T_k)*S(T_k) explicitly.

Zero-side terms (exact, symmetric rho<->rhobar pairing):
  n=1: term(g) = 1/(1/4+g^2)
  n=2: term(g) = 4g^2/(1/4+g^2)^2
Smooth tail model: integral of term_smooth(g)*dN_smooth,
  dN_smooth = (1/2pi)*ln(g/2pi)*dg, term_smooth = 1/g^2 (n=1), 4/g^2 (n=2).
Closed forms: A1(T) = (1/2pi)*(ln(T/2pi)+1)/T ; A2(T) = (2/pi)*(ln(T/2pi)+1)/T.
"""
import math, json, os
import numpy as np

LI_DIR = os.path.dirname(os.path.abspath(__file__))
zeros = [complex(*p) for p in json.load(open(os.path.join(LI_DIR, 'zeros_cache.json')))]
gammas = sorted(z.imag for z in zeros if z.imag > 0)
assert len(gammas) == 300

n2nums = json.load(open(os.path.join(LI_DIR, 'worked_n2_numbers.json')))
import mpmath
mpmath.mp.dps = 50
lam1_exact = 1 + float(mpmath.euler)/2 - 0.5*math.log(4*math.pi)
lam2_keiper = n2nums['keiper_taylor']['lambda_2']

TWO_PI = 2*math.pi

def term1(g): return 1.0/(0.25+g*g)
def term2(g): return 4*g*g/((0.25+g*g)**2)
def A1(T):  return (math.log(T/TWO_PI)+1)/(TWO_PI*T)          # analytic tail n=1
def A2(T):  return (2.0/math.pi)*(math.log(T/TWO_PI)+1)/T     # analytic tail n=2

def smooth_N(T):  # (T/2pi)(ln(T/2pi)-1) + 7/8
    return (T/TWO_PI)*(math.log(T/TWO_PI)-1) + 0.875

def numeric_tail_original(T, term, mult):
    """Reproduce the original scripts' tail: log-spaced trapz of
    term(g)*(1/2pi)ln(g/2pi) on [T, T*mult]."""
    N = 20000
    gs = np.exp(np.linspace(math.log(T), math.log(T*mult), N))
    vals = np.array([term(g) for g in gs])*(1.0/TWO_PI)*np.log(gs/TWO_PI)
    return float(np.trapz(vals, gs))

out = {}
print("="*78)
print("1. TRUNCATION LADDER (analytic smooth-density tail)")
print("="*78)
for name, term, A, ref in [("n=1", term1, A1, lam1_exact),
                           ("n=2", term2, A2, lam2_keiper)]:
    print(f"\n--- {name}: reference = {ref:.12f} ---")
    print(f"{'k':>5} {'T_k':>10} {'S(T_k)':>14} {'A(T_k)':>12} {'S+A':>14} "
          f"{'(S+A)-ref':>12} {'S_osc(T_k)':>10} {'f(T)S_osc':>10}")
    rows = []
    for k in [100, 150, 200, 250, 300]:
        gs = gammas[:k]
        Tk = gs[-1]
        S = math.fsum(term(g) for g in gs)
        a = A(Tk)
        tot = S + a
        Sosc = k - smooth_N(Tk)          # boundary oscillatory piece
        fS = term(Tk)*Sosc
        rows.append((k, Tk, S, a, tot, tot-ref, Sosc, fS))
        print(f"{k:>5} {Tk:>10.2f} {S:>14.10f} {a:>12.3e} {tot:>14.10f} "
              f"{tot-ref:>+12.2e} {Sosc:>+10.3f} {fS:>+10.2e}")
    corr = [r[4] for r in rows]
    spread = max(corr)-min(corr)
    print(f"  ladder spread of S+A: {spread:.2e}")
    out[name] = dict(rows=rows, spread=spread)

print()
print("="*78)
print("2. OBSERVED-vs-PREDICTED GAP  S(300)-S(150) vs integral over [T150,T300]")
print("="*78)
for name, term, A in [("n=1", term1, A1), ("n=2", term2, A2)]:
    g150, g300 = gammas[:150], gammas[:300]
    obs = math.fsum(term(g) for g in g300) - math.fsum(term(g) for g in g150)
    pred = A(gammas[149]) - A(gammas[299])
    rel = abs(obs-pred)/obs
    print(f"{name}: observed = {obs:.10e}  predicted = {pred:.10e}  "
          f"|obs-pred|/obs = {rel:.2e}  (~{-math.log10(rel):.1f} sig figs)")

print()
print("="*78)
print("3. RESIDUAL DECOMPOSITION at k=300")
print("="*78)
for name, term, A, ref, mult in [("n=1", term1, A1, lam1_exact, 50),
                                 ("n=2", term2, A2, lam2_keiper, 100)]:
    gs = gammas[:300]; T = gs[-1]
    S = math.fsum(term(g) for g in gs)
    true_tail = ref - S
    num_tail = numeric_tail_original(T, term, mult)   # as the scripts did
    ana_tail = A(T)
    print(f"\n--- {name} (T={T:.1f}) ---")
    print(f"  S(300)              = {S:.10f}")
    print(f"  true tail (ref - S) = {true_tail:.6e}")
    print(f"  script-style tail   = {num_tail:.6e}   (trapz to T*{mult})")
    print(f"  analytic tail       = {ana_tail:.6e}   (closed form, no cutoff)")
    print(f"  cutoff bias (ana-num)= {ana_tail-num_tail:+.3e}")
    print(f"  oscillatory resid   = {true_tail-ana_tail:+.3e}  (= true - analytic)")
    print(f"  reported residual   = {S+num_tail-ref:+.3e}")
    print(f"  analytic residual   = {S+ana_tail-ref:+.3e}")

json.dump({k: {'rows': v['rows'], 'spread': v['spread']}
           for k, v in out.items()},
          open(os.path.join(LI_DIR, 'tail_check_numbers.json'), 'w'), indent=1)
print("\nnumbers -> tail_check_numbers.json")
