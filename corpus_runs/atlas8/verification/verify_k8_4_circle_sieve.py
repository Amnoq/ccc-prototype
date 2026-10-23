#!/usr/bin/env python3
"""K8-4 verification: the circle sieve independently produces the primes (A8-13).

Home claim (home:sieve1): the linear circle sieve — unit circles tile
[0,1],[1,2],...; at each n>=2 the point is checked against previously
spammed boundaries; unshared points are EXACTLY the primes (pilot:
verified N=30..2000 against a classical sieve). We re-verify
independently here, including larger N.

Imports sieve_complex (read-only); modifies nothing.
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/prime-sieve-geometry')
from sieve_complex import linear_circle_sieve, classic_primes

if __name__ == '__main__':
    print('K8-4: linear_circle_sieve unshared points == classical primes')
    ok = True
    for N in (30, 200, 2000, 10000):
        primes, _, _ = linear_circle_sieve(N)
        ref = classic_primes(N)
        match = (primes == ref)
        ok &= match
        print(f'  N={N:6d}  sieve primes={len(primes)}  classical={len(ref)}  match={match}')
    print('VERDICT:', 'verified' if ok else 'FAILED')
