#!/usr/bin/env python3
"""K8-3 verification: twin singular series as renormalized weight (A8-11).

Home claim (home:sieve2 D6): the Hardy-Littlewood twin constant is
DERIVED as renormalized total weight of the deformed sieve:
  S(z) = prod_{p<=z} (1 - |R_p|/p) / (1 - 1/p)^2  ->  2*C2 = 1.3203236...
with R_2 = {0} (|R|=1), R_p = {0,-2} for odd p (|R|=2).
The constant is classical (1923); the generative derivation is the
pilot's. We verify the product converges to 2*C2.

Pure computation; no sieve import needed.
"""
import math, sys
sys.path.insert(0, '/home/hatch/workspace/prime-sieve-geometry')
from deformed_sieve import primes_upto

C2x2 = 1.320323631693739  # 2 * 0.6601618158468695 (twin prime constant x2)

def S(z):
    prod = 1.0
    for p in primes_upto(z):
        r = 1 if p == 2 else 2
        prod *= (1 - r / p) / (1 - 1 / p) ** 2
    return prod

if __name__ == '__main__':
    print('K8-3: renormalized weight S(z) -> 2*C2 =', C2x2)
    ok = True
    for z in (7, 13, 100, 1000):
        s = S(z)
        print(f'  z={z:4d}  S(z)={s:.6f}  |S-2C2|={abs(s - C2x2):.6f}')
        if z == 1000 and abs(s - C2x2) > 0.01:
            ok = False
    print('VERDICT:', 'verified' if ok else 'FAILED')
