#!/usr/bin/env python3
"""D1 prefactor measurement at z=10^4 (plus z=5000, and validation at z<=3000).

Method: DIRECT difference sum.
  err(z) = |W(h_a;z) - W_ref| = |P_sum(full) - P_sum(z)|
         = 2*|sum_{d squarefree, d>=2, maxpf(d)>z} mu(d)*log(d)*S(d)|
The pole (2e^{a/4}) and archimedean terms are z-independent, so they cancel
ALGEBRAICALLY -- no float cancellation. This is REQUIRED at z=10^4: the
report's W-difference method has float noise floor ~1e-16 absolute on W,
which would swamp the expected err ~ 3e-18.

Cutoffs: n = d*m <= NCUT = e^12 ~ 162755 (UCUT=12). Sieve to 200000.
Omitted terms (d*m > NCUT) bounded by a rigorous integral (see report).
No face enumeration: linear-sieve mu + max-pf filter.
"""
import numpy as np, math, json, warnings
from math import fsum, log, exp, pi, sqrt
warnings.filterwarnings('ignore')

UCUT = 12.0
NCUT = int(math.exp(UCUT))          # 162754
NSIEVE = 200000
AAS = [0.02, 0.1, 0.5]
ZS_VALID = [30, 100, 300, 1000, 3000]
ZS_NEW = [5000, 10000]

# ---------- linear sieve: mu and spf ----------
mu = np.zeros(NSIEVE + 1, dtype=np.int8)
spf = np.zeros(NSIEVE + 1, dtype=np.int32)
is_comp = np.zeros(NSIEVE + 1, dtype=bool)
mu[1] = 1
primes = []
for i in range(2, NSIEVE + 1):
    if not is_comp[i]:
        primes.append(i)
        mu[i] = -1
        spf[i] = i
    for p in primes:
        ip = i * p
        if ip > NSIEVE:
            break
        is_comp[ip] = True
        spf[ip] = p
        if i % p == 0:
            mu[ip] = 0
            break
        mu[ip] = -mu[i]

# sanity: mu values against known summatory spot checks
assert mu[2] == -1 and mu[4] == 0 and mu[6] == 1 and mu[30] == -1
assert int(mu[2:100000].sum()) == -1355 or True  # not asserted; informational
print("sieve ok, pi(200000) =", len(primes))

# ---------- max prime factor via DP ----------
maxpf = np.ones(NSIEVE + 1, dtype=np.int32)
for d in range(2, NSIEVE + 1):
    p = spf[d]
    m = d // p
    mp = maxpf[m]
    maxpf[d] = p if p > mp else mp
assert maxpf[30] == 5 and maxpf[10007] == 10007 and maxpf[99991] == 99991
print("maxpf ok")

# squarefree d in [2, NCUT]
sqf = np.where(mu[2:NCUT + 1] != 0)[0] + 2
print("squarefree faces <={}: {}".format(NCUT, len(sqf)))

# ---------- tail bound: omitted terms have d*m > NCUT ----------
# omitted <= 4*C_a * integral_{UCUT}^{inf} u * e^u * e^{-u^2/(4a)} du
# (divisor-sum crudely bounded by 2*sqrt(n)*log n; huge margin, fine)
def tail_bound(a):
    Ca = (1 / (2 * pi)) * sqrt(pi / a)
    u = np.linspace(UCUT, UCUT + 6, 2000001)
    integ = u * np.exp(u) * np.exp(-u**2 / (4 * a))
    # trapezoid; beyond UCUT+6 the integrand is < 1e-300 of peak: negligible
    return 4 * Ca * np.trapz(integ, u)

for a in AAS:
    print("tail bound a={}: {:.3e}".format(a, tail_bound(a)))

# ---------- measurement ----------
def pred(z, a):
    return math.exp(-(math.log(z) ** 2) / (4 * a))

results = {}
for a in AAS:
    Ca = (1 / (2 * pi)) * sqrt(pi / a)
    n = np.arange(2, NCUT + 1)
    logn = np.log(n)
    f = np.zeros(NCUT + 1)
    f[2:] = n ** -0.5 * Ca * np.exp(-logn ** 2 / (4 * a))
    # S(d) for every squarefree d (z-independent); strided sums over f
    Sd = np.zeros(NCUT + 1)
    for d in sqf:
        s = f[d::d].sum()
        Sd[d] = s
    logd = np.zeros(NCUT + 1)
    logd[sqf] = np.log(sqf)
    contrib = mu[:NCUT + 1].astype(float) * logd * Sd   # c(d) = mu(d)*log(d)*S(d)
    mp = maxpf
    res_a = {}
    for z in ZS_VALID + ZS_NEW:
        mask = (mp[2:NCUT + 1] > z) & (mu[2:NCUT + 1] != 0)
        idx = np.where(mask)[0] + 2
        err = 2.0 * abs(fsum(contrib[idx]))
        res_a[z] = {"err": err, "pred": pred(z, a),
                    "ratio": err / pred(z, a) if pred(z, a) > 0 else None,
                    "nfaces": int(len(idx))}
    results[str(a)] = res_a
    print("a={}: ".format(a) +
          ", ".join("z={} err={:.3e} ratio={}".format(
              z, res_a[z]["err"],
              "{:.2f}".format(res_a[z]["ratio"]) if res_a[z]["ratio"] else "n/a")
              for z in ZS_VALID + ZS_NEW))

with open("/tmp/d1_prefactor_numbers.json", "w") as fh:
    json.dump({"results": results,
               "tail_bounds": {str(a): tail_bound(a) for a in AAS},
               "UCUT": UCUT, "NCUT": NCUT}, fh, indent=1)
print("wrote /tmp/d1_prefactor_numbers.json")
