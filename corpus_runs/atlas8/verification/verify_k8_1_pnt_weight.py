#!/usr/bin/env python3
"""K8-1 verification: PNT as total weight 1 (A8-06).

Home claim (home:sieve1 D4): w(S) = (-1)^{|S|+1} * log(prod S) / prod S
over nonempty faces S of the sieve complex; sum_{prod S <= X} w(S) -> 1
IS the Prime Number Theorem. Pilot verified to 2e6; we re-verify
independently here at smaller X (faces enumeration is exponential).

Imports sieve_complex (read-only); modifies nothing.
"""
import sys, math
sys.path.insert(0, '/home/hatch/workspace/prime-sieve-geometry')
from sieve_complex import linear_circle_sieve, faces_upto, prod_of

def face_weight_sum(X):
    primes, _, _ = linear_circle_sieve(X)
    faces = faces_upto(X, primes)
    total = 0.0
    for f in faces:
        if not f:
            continue
        p = prod_of(f, primes)
        # p <= X guaranteed by faces_upto
        total += ((-1) ** (len(f) + 1)) * math.log(p) / p
    return total

if __name__ == '__main__':
    print('K8-1: PNT as total weight 1 — sum_{faces} (-1)^{|S|+1} log(prod S)/prod S')
    ok = True
    for X in (1000, 5000, 20000):
        s = face_weight_sum(X)
        dev = abs(s - 1)
        print(f'  X={X:6d}  sum={s:.6f}  |sum-1|={dev:.6f}')
        if dev > 0.05:
            ok = False
    # PNT-equivalent: convergence is oscillatory (error-term-like); the check
    # is approach toward 1 at large X, matching the pilot's 0.999922 @5e5.
    print('VERDICT:', 'verified' if ok else 'FAILED')
