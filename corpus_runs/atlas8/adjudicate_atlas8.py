#!/usr/bin/env python3
"""Atlas-8 adjudication: reviewed cross-sky verdicts.

Verdicts: resolved / split (role-difference named per Atlas-2 D3) /
missed / rejected (with reason). Never invent a resolution.
S1 control: Maynard's citation of Zhang [9] must resolve to Zhang's
Theorem 1 — else method failure.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
N = json.load(open(os.path.join(BASE, 'graphs', 'atlas8_raw.json')))['nodes']

def nd(nid):
    n = N[nid]
    return {'id': nid, 'sky': n['sky'], 'paper': n['paper'],
            'label': n['label'], 'kind': n['kind'],
            'status': n['status'], 'note': n['note'][:280]}

ADJ = [
 {
  'id': 'A8-01', 'verdict': 'split_link', 'control': 'S1',
  'a': 'foreign:maynard:zhang-s-bounded-gaps-breakthrough-liminf-p-n-1-p-n-7',
  'b': 'foreign:zhang:theorem-1-admissible-h-with-k-0-3-5-10-6-yields-infi',
  'relation': 'cites',
  'role_difference': ('foreign/maynard: cites Zhang\'s bounded-gaps breakthrough '
   '(liminf <= 70,000,000) as the enabling prior result [9], status conjectural-from-this-chunk '
   '(citing-chunk artifact); foreign/zhang: proves Theorem 1 (admissible H, k0 > 3.5e6 -> '
   'liminf < 7e7), status exact. Same theorem, citing vs proving roles.'),
  'reason': ('S1 POSITIVE CONTROL RESOLVES: Maynard §1 explicitly cites Zhang [9] and frames '
   'the paper as a GPY refinement; Zhang §1 proves the cited theorem. The link is earned, '
   'not inserted — both sides name the same result.'),
 },
 {
  'id': 'A8-02', 'verdict': 'split_link',
  'a': 'foreign:sieve:the-diagonalization-lemma-optimal-lambda-d-with-lamb',
  'b': 'home:sieve4:selberg-s-lambda-2-sieve-as-an-optimized-quadratic-f',
  'relation': 'shares-method',
  'role_difference': ('foreign/sieve (Elkies): proves the classical diagonalization lemma '
   '(optimal lambda_d, min Q = 1/S(D,z), exact); home/sieve4: reframes Selberg\'s lambda^2 '
   'as an optimized quadratic form Q(lam) on faces (computationally_verified, truncated '
   'mid-derivation). Same optimization, proved-classical vs face-native-reframing roles.'),
  'reason': 'Shared referent (the Selberg lambda-optimization); different epistemic roles.',
 },
 {
  'id': 'A8-03', 'verdict': 'split_link',
  'a': 'foreign:sieve:selberg-s-inequality-a-d-a-s-d-z-r-d-z',
  'b': 'home:sieve4:selberg-s-lambda-2-sieve-as-an-optimized-quadratic-f',
  'relation': 'shares-method',
  'role_difference': ('foreign/sieve: proves Selberg\'s upper-bound inequality A(D) <= A/S(D,z) + R(D,z) '
   '(exact); home/sieve4: reframes the lambda^2 method as a quadratic form on faces, engaging '
   'the optimization rather than the bound as such (computationally_verified, truncated). '
   'Theorem vs method-reframing.'),
  'reason': 'Shared method (Selberg\'s sieve); the home node reframes the machinery, not the bound.',
 },
 {
  'id': 'A8-04', 'verdict': 'split_link',
  'a': 'foreign:maynard:selberg-k-dimensional-weights',
  'b': 'home:sieve4:selberg-s-lambda-2-sieve-as-an-optimized-quadratic-f',
  'relation': 'shares-method',
  'role_difference': ('foreign/maynard: k-dimensional Selberg weights w_n = (sum lambda_d)^2 as the '
   'working engine of bounded gaps (exact, reframed); home/sieve4: lambda^2 as an optimized '
   'quadratic form on faces (computationally_verified, truncated). Working engine vs '
   'structural reframing of the same Selberg idea.'),
  'reason': 'Shared referent (Selberg weights); different roles (engine vs reframing).',
 },
 {
  'id': 'A8-05', 'verdict': 'split_link',
  'a': 'foreign:maynard:lemma-5-1-s1-in-diagonal-y-form-with-error-o-y-max-2',
  'b': 'home:sieve4:selberg-s-lambda-2-sieve-as-an-optimized-quadratic-f',
  'relation': 'shares-method',
  'role_difference': ('foreign/maynard: diagonalizes the k-dimensional Selberg form via the '
   'y-change-of-variables to evaluate S1 (exact, proved); home/sieve4: the lambda^2 form '
   'as a positive-definite quadratic form on faces (computationally_verified, truncated). '
   'Same diagonalization move, analytic-evaluation vs geometric-reframing roles.'),
  'reason': 'The diagonalization of the Selberg quadratic form is the shared move.',
 },
 {
  'id': 'A8-06', 'verdict': 'split_link',
  'a': 'foreign:pnt:the-prime-number-theorem-the-number-of-primes-x-is-a',
  'b': 'home:sieve1:d4-the-weighted-infinite-complex-bare-limit-triviali',
  'relation': 'shares-theorem',
  'role_difference': ('foreign/pnt (Zagier/Newman): proves pi(x) ~ x/log x by Tauberian contour '
   'argument (exact); home/sieve1: PNT as the identity sum w(S) -> 1 (total weight 1) on the '
   'weighted infinite complex, verified to 2e6 (computationally_verified), framing stated as '
   'appearing new. Same theorem, analytic-proof vs combinatorial-identity roles.'),
  'reason': 'The strongest same-theorem-different-grounding pair in the run.',
 },
 {
  'id': 'A8-07', 'verdict': 'rejected',
  'a': 'foreign:greentao:hardy-littlewood-1923-conjecture-the-number-of-k-ter',
  'b': 'home:sieve2:d6-deformed-marking-rule-survivors-200000-exactly-th',
  'relation': 'shared-name',
  'role_difference': None,
  'reason': ('REJECTED per the Atlas-5 GUE precedent: these are DIFFERENT Hardy-Littlewood '
   'conjectures — the foreign node conjectures the count of k-term prime ARITHMETIC '
   'PROGRESSIONS (singular series C_k), the home node derives the TWIN-prime constant '
   '2C_2 as renormalized weight. Shared name and singular-series shape, not a shared '
   'claim. The 5 shared tokens (1923, hardy, littlewood, log, prime) are the name, not '
   'the referent.'),
 },
 {
  'id': 'A8-08', 'verdict': 'rejected',
  'a': 'foreign:sieve:brun-s-theorem-the-sum-of-reciprocals-of-twin-primes',
  'b': 'home:sieve2:twin-density-2-x-sx-log-x-2-remains-unproven-honest-',
  'relation': 'shared-object',
  'role_difference': None,
  'reason': ('REJECTED: different claims about the shared object (twin primes) — the foreign '
   'node proves convergence of the twin-reciprocal sum (exact), the home node derives the '
   'twin density weight while leaving the asymptotic explicitly unproven (honest boundary). '
   'No shared claim; a shared object is not a shared result.'),
 },
 {
  'id': 'A8-09', 'verdict': 'split_link',
  'a': 'foreign:zhang:theorem-1-admissible-h-with-k-0-3-5-10-6-yields-infi',
  'b': 'home:sieve2:k-tuple-constellations-as-gap-patterns-nine-admissib',
  'relation': 'shares-object',
  'role_difference': ('foreign/zhang: admissible tuples H as the engine of a PROVED bounded-gaps '
   'theorem (exact); home/sieve2: admissible k-tuple "combos" (twins, cousins, sexy, triplets, '
   'quad, quint, sext + {0,2,4} control) as EXHIBITED sieve-output gap patterns (exact '
   'definition). Same combinatorial object (admissible constellations), theorem-engine vs '
   'pattern-exhibition roles. SPAN-PRIORITY pair.'),
  'reason': ('The admissible tuple is the shared referent; Zhang uses it to prove gaps are '
   'bounded, the sieve exhibits it as output. Crack candidate: does the literature state '
   'the sieve\'s exhibited pattern inventory?'),
 },
 {
  'id': 'A8-10', 'verdict': 'split_link',
  'a': 'foreign:maynard:admissible-set-h-h1-hk',
  'b': 'home:sieve2:admissibility-obstruction-emerges-from-the-machine-u',
  'relation': 'shares-object',
  'role_difference': ('foreign/maynard: admissibility as an INPUT CONDITION on H (exact definition — '
   'for every p some residue class is missed); home/sieve2: admissibility obstruction as an '
   'EMERGENT property — the non-admissible {0,2,4} dies in the machine uninserted '
   '(computationally_verified). Same property, stipulated-input vs emergent-output roles. '
   'SPAN-PRIORITY pair.'),
  'reason': ('Admissibility is the shared referent; the literature stipulates it, the sieve '
   'generates it. Crack candidate: the generative account of admissibility is unstated in '
   'the literature.'),
 },
 {
  'id': 'A8-11', 'verdict': 'split_link',
  'a': 'foreign:maynard:prime-k-tuples-conjecture',
  'b': 'home:sieve2:twin-density-2-x-sx-log-x-2-remains-unproven-honest-',
  'relation': 'conjecture-vs-boundary',
  'role_difference': ('foreign/maynard: the prime k-tuples conjecture stated as the open horizon '
   '(conjectural, reframed; no k>1 case known); home/sieve2: the twin-density asymptotic '
   'explicitly UNCLAIMED — the sieve derives the weight mechanism (2C_2) but marks the '
   'passage to pi_2(x) ~ Sx/(log x)^2 as an honest open boundary (conjectural). The home '
   'side holds the mechanism without the claim; the literature holds the claim without '
   'the mechanism.'),
  'reason': ('Shared horizon (prime constellations infinitely often); complementary epistemic '
   'postures. Crack candidate: the derived weight mechanism is unstated in the literature.'),
 },
 {
  'id': 'A8-12', 'verdict': 'split_link',
  'a': 'foreign:maynard:theorem-1-2-a-positive-proportion-of-admissible-m-tu',
  'b': 'home:sieve2:d6-generalized-k-tuple-sweep-nine-constellations-0-2',
  'relation': 'shares-object',
  'role_difference': ('foreign/maynard: PROVES a positive proportion of admissible m-tuples occur '
   'infinitely often (exact); home/sieve2: EXHIBITS nine constellations with survivors '
   'matching independent enumeration exactly at x=1e6 (computationally_verified). Proved '
   'proportion vs exhibited census of the same constellations. SPAN-PRIORITY pair.'),
  'reason': 'Same constellations; analytic proof vs computational exhibition.',
 },
 {
  'id': 'A8-13', 'verdict': 'split_link',
  'a': 'foreign:sieve:the-general-sieve-setup-sifted-set-s-multiplicative-',
  'b': 'home:sieve1:the-linear-circle-sieve-unit-circles-tile-0-1-1-2-at',
  'relation': 'shares-method',
  'role_difference': ('foreign/sieve (Elkies): the classical sieve setup — sifted set, multiplicative '
   'density, Eratosthenes as the naive prototype (exact definition); home/sieve1: the linear '
   'circle sieve — geometric shared-boundary sifting, built from first principles without the '
   'literature, verified against Eratosthenes at every tested N (exact specification). Same '
   'job (produce the primes by elimination), divisibility vs shared-boundary mechanisms.'),
  'reason': ('The sieve itself is the shared referent; the home side independently re-derived '
   'a sieve and checked it against the classical one. The independence (built without the '
   'literature) is the finding.'),
 },
]

MISSES = [
 {'id': 'M8-1', 'claim': "Cramér's conjecture (max gap ~ log^2 x)",
  'note': 'No home-sky counterpart: the pilot has no maximal-gap claim. Recorded miss, not a link.'},
 {'id': 'M8-2', 'claim': 'Green–Tao: arbitrarily long prime APs (Theorem 1.1)',
  'note': 'No home-sky counterpart: the pilot states no AP theorem. Recorded miss, not a link.'},
 {'id': 'M8-3', 'claim': "Cramér's urn model (probabilistic)",
  'note': 'No home-sky counterpart: the pilot is deterministic throughout. Recorded miss, not a link.'},
 {'id': 'M8-4', 'claim': 'Selberg parity barrier (home, cited theorem)',
  'note': 'No foreign-sky counterpart in these chunks: none of the 6 papers\' extracted sections state the parity barrier. Recorded miss, not a link.'},
 {'id': 'M8-5', 'claim': "Level of distribution (Maynard's theta)",
  'note': 'No home-sky counterpart: the pilot has no level-of-distribution concept. Recorded miss, not a link.'},
]

def main():
    recs = []
    for a in ADJ:
        for side in ('a', 'b'):
            n = nd(a[side])
            a[side + '_node'] = n
        recs.append(a)
    totals = {'split_link': sum(1 for a in ADJ if a['verdict'] == 'split_link'),
              'resolved': sum(1 for a in ADJ if a['verdict'] == 'resolved'),
              'rejected': sum(1 for a in ADJ if a['verdict'] == 'rejected'),
              'missed': sum(1 for a in ADJ if a['verdict'] == 'missed')}
    totals['links'] = totals['split_link'] + totals['resolved']
    out = {'adjudications': recs, 'misses': MISSES, 'totals': totals,
           'method': ('Reviewed adjudication by the Atlas-8 coordinator. Mechanical candidates '
                      '(2468 token-overlap) were triaged; semantic review drove the verdicts. '
                      'S1 control resolves (A8-01). No merges: no two nodes made the same claim. '
                      'Citing-chunk artifact respected: maynard_p1\'s conjectural-from-chunk labels '
                      'on cited theorems were not treated as epistemic downgrades.')}
    json.dump(out, open(os.path.join(BASE, 'atlas8_adjudications.json'), 'w'),
              ensure_ascii=False, indent=1)
    print('adjudications:', totals)
    print('misses:', len(MISSES))
    s1 = [a for a in ADJ if a.get('control') == 'S1'][0]
    print('S1 control verdict:', s1['verdict'], '-', s1['id'])

if __name__ == '__main__':
    main()
