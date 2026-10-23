#!/usr/bin/env python3
"""WORKED_N1: lambda_1 = W(h_1) two-sided numerical check.

(a) Zero side: lambda_1 = sum_{gamma>0} 1/(1/4+gamma^2), vs exact
    1 + euler/2 - (1/2)log(4pi).
(b) W side: regularized g_{1,eps} (C^3 smoothstep truncation+smoothing),
    W_eps = Phi_eps(0)+Phi_eps(1)+A_eps-P_eps via the pilot's verified
    explicit formula (even-h form, h(r)=Re[Phi(1/2+ir)]).
    Show W_eps -> lambda_1 as eps -> 0.
"""
import math, json, os, sys
import mpmath
mpmath.mp.dps = 50

LI_DIR = os.path.dirname(os.path.abspath(__file__))
ZCACHE = '/tmp/zeros_n1.json'

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

# ---------- Part (a): zero side ----------
print("=" * 70)
print("Part (a): zero side  lambda_1 = sum_{gamma>0} 1/(1/4+gamma^2)")
print("=" * 70)
lam1_exact = 1 + float(mpmath.euler)/2 - 0.5*math.log(4*math.pi)
print(f"exact 1+gamma/2-(1/2)log(4pi) = {lam1_exact:.12f}")

zeros = get_zeros(300)
gammas = sorted(z.imag for z in zeros if z.imag > 0)
T = gammas[-1]
S = math.fsum(1.0/(0.25+g*g) for g in gammas)
# tail estimate: integral of (1/g^2) dN, N(g)~(g/2pi)log(g/2pi)
def tail_est(T):
    f = lambda g: (1.0/(2*math.pi))*math.log(g/(2*math.pi))/ (g**2)
    # integrate numerically
    N = 20000
    a, b = T, T*50
    # log-spaced
    import numpy as np
    gs = np.exp(np.linspace(math.log(a), math.log(b), N))
    vals = (1.0/(2*math.pi))*np.log(gs/(2*math.pi))/(gs**2)
    return float(np.trapz(vals, gs))
te = tail_est(T)
print(f"N zeros: {len(gammas)}, T = {T:.1f}")
print(f"partial sum S(T) = {S:.10f}")
print(f"tail estimate    = {te:.3e}")
print(f"S(T)+tail        = {S+te:.10f}")
print(f"|S(T)+tail-exact|= {abs(S+te-lam1_exact):.2e}")
print(f"|S(T)-exact|     = {abs(S-lam1_exact):.2e}  (raw truncation error)")

# ---------- Part (b): W side ----------
print()
print("=" * 70)
print("Part (b): W side via regularized g_{1,eps}")
print("=" * 70)

from math import comb
def tpoly_to_xpoly(d, x0, w):
    deg = len(d)-1
    c = [mpmath.mpf(0)]*(deg+1)
    for j, dj in enumerate(d):
        if dj == 0: continue
        for m in range(j+1):
            c[m] += mpmath.mpf(dj) * comb(j, m) * ((-x0)**(j-m)) / (mpmath.mpf(w)**j)
    return c

def F_eps_pieces(eps):
    eps = mpmath.mpf(eps)
    d_ss = [mpmath.mpf(0)]*8
    d_ss[4]=35; d_ss[5]=-84; d_ss[6]=70; d_ss[7]=-20
    d_fall = [mpmath.mpf(1),0,0,0,-35,84,-70,20]
    return [
        (eps, 2*eps, tpoly_to_xpoly(d_ss, eps, eps)),
        (2*eps, 1-eps, [mpmath.mpf(1)]),
        (1-eps, mpmath.mpf(1), tpoly_to_xpoly(d_fall, 1-eps, eps)),
    ]

def Phi_eps(s, pieces):
    s = mpmath.mpc(s)
    tot = mpmath.mpc(0)
    for a, b, c in pieces:
        for m, cm in enumerate(c):
            if cm == 0: continue
            tot += cm * (mpmath.power(b, s+m) - mpmath.power(a, s+m)) / (s+m)
    return tot

def F_eps_val(x, pieces):
    x = mpmath.mpf(x)
    for a, b, c in pieces:
        if a <= x <= b:
            return sum(cm*(x**m) for m, cm in enumerate(c))
    return mpmath.mpf(0)

def prime_powers(N):
    bs = bytearray(b"\x01")*(N+1); bs[0:2]=b"\x00\x00"
    for i in range(2, int(N**0.5)+1):
        if bs[i]: bs[i*i:N+1:i] = b"\x00"*(((N-i*i)//i)+1)
    out=[]
    for p in range(2, N+1):
        if bs[p]:
            q=p
            while q<=N:
                out.append((q, math.log(p))); q*=p
    out.sort(); return out

def compute_W(eps):
    pieces = F_eps_pieces(eps)
    # Phi(0), Phi(1) by quadrature (smooth)
    Phi0 = mpmath.quad(lambda x: F_eps_val(x, pieces)/x, [eps, 1])
    Phi1 = mpmath.quad(lambda x: F_eps_val(x, pieces), [eps, 1])
    # h(r) = Re Phi(1/2+ir) via closed form
    def h(r):
        return mpmath.re(Phi_eps(mpmath.mpc(0.5, r), pieces))
    # archimedean: (1/pi) int_0^inf h(r)[Re psi(1/4+ir/2)-log pi] dr
    logpi = mpmath.log(mpmath.pi)
    def arch_integrand(r):
        return h(r)*(mpmath.re(mpmath.digamma(mpmath.mpc(0.25, 0.5*r))) - logpi)
    A = mpmath.quad(arch_integrand, [0, mpmath.inf]) / mpmath.pi
    # prime sum: sum_{n>=2} (Lambda(n)/n) F(1/n), nonzero for n<=1/eps
    Nmax = int(math.ceil(1.0/eps))
    PP = prime_powers(Nmax)
    P = mpmath.mpf(0)
    for n, lp in PP:
        f = F_eps_val(mpmath.mpf(1)/n, pieces)
        if f != 0:
            P += mpmath.mpf(lp)/n * f
    W = Phi0 + Phi1 + A - P
    return dict(eps=eps, Phi0=float(Phi0), Phi1=float(Phi1), A=float(A),
                P=float(P), W=float(W), pieces=pieces)

results = []
for eps in [0.2, 0.1, 0.05, 0.025]:
    print(f"\neps = {eps}: computing...", flush=True)
    r = compute_W(eps)
    results.append(r)
    print(f"  Phi(0)={r['Phi0']:.8f}  Phi(1)={r['Phi1']:.8f}  A={r['A']:.8f}  P={r['P']:.8f}")
    print(f"  W_eps = {r['W']:.10f}   |W_eps - exact| = {abs(r['W']-lam1_exact):.2e}")

print()
print("=" * 70)
print("Convergence table: W_eps -> lambda_1")
print("=" * 70)
print(f"{'eps':>8} {'W_eps':>16} {'|W_eps-lam1|':>14}")
for r in results:
    print(f"{r['eps']:>8} {r['W']:>16.10f} {abs(r['W']-lam1_exact):>14.2e}")
print(f"{'exact':>8} {lam1_exact:>16.10f}")

json.dump([{k: v for k, v in r.items() if k != 'pieces'} for r in results],
          open(os.path.join(LI_DIR, 'worked_n1_numbers.json'), 'w'), indent=1)
print("\nnumbers saved to worked_n1_numbers.json")
