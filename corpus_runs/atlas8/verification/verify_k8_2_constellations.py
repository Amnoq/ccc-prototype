#!/usr/bin/env python3
"""K8-2 verification: admissible constellations as sieve output +
emergent admissibility obstruction (A8-09, A8-10, A8-12).

Home claims:
 (a) deformed_sieve survivors <= x are exactly the twin-prime lowers
     (pilot: verified to 2e5; we check at x=20000 here).
 (b) the non-admissible pattern {0,2,4} DIES: the only prime triple
     (n, n+2, n+4) is (3,5,7) — the admissibility obstruction emerges
     uninserted.

Imports deformed_sieve (read-only); modifies nothing.
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/prime-sieve-geometry')
from deformed_sieve import deformed_sieve, primes_upto

def twin_lowers_bruteforce(x):
    primes = set(primes_upto(x + 2))
    return [p for p in range(3, x + 1) if p in primes and p + 2 in primes]

if __name__ == '__main__':
    print('K8-2a: deformed-sieve survivors == twin lowers')
    X = 20000
    surv, _ = deformed_sieve(X)
    twins = twin_lowers_bruteforce(X)
    print(f'  x={X}: survivors={len(surv)}, brute-force twin lowers={len(twins)}, '
          f'match={surv == twins}')
    ok_a = (surv == twins)

    print('K8-2b: {0,2,4} dies — only (3,5,7)')
    primes = set(primes_upto(100000))
    triples = [(n, n + 2, n + 4) for n in range(2, 100000)
               if n in primes and n + 2 in primes and n + 4 in primes]
    print(f'  prime triples (n,n+2,n+4) below 1e5: {triples}')
    ok_b = (triples == [(3, 5, 7)])

    print('VERDICT:', 'verified' if (ok_a and ok_b) else 'FAILED')
