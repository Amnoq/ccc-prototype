#!/usr/bin/env python3
"""Atlas-6 adjudication: apply reviewed merges, build the bridge graph,
write cross_bridge_links.json with every adjudication record.

Reviewed merges (same referent, same epistemic level, restated across
files — verified by hand against full labels/notes):
  M1: rel step12 c4 KEEPS, rel step3_tree c5 drops (same verification event)
  M2: rel step12 c6 KEEPS, rel step3_tree c6 drops (same derived finding)
  M3: af w1 c12 KEEPS, af n1 c6 drops (same cited Bom00 observation)
Facets of dropped nodes are preserved on the kept node.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(BASE, 'graphs', 'atlas6_raw.json')))
nodes, edges = g['nodes'], g['edges']

MERGES = [
    ('rel:zero-side-vs-prime-side-agreement-to-machine-pre',
     'rel:10a-step2-symmetric-guinand-weil-formula-verifie',
     'same verification event (60 zeros, 26152 prime powers, 2.4e-16) restated across the two relational files'),
    ('rel:prime-side-positivity-is-cancellatory-not-termwi',
     'rel:step-2-structural-finding-prime-side-positivity-',
     'same derived structural finding restated across the two relational files'),
    ('af:bombieri-s-bom00-negative-index-observation-the-',
     'af:bombieri-bom00-negative-index-of-finite-truncati',
     'same cited Bom00 negative-index observation in proof-plan vs discovery-narrative context'),
]

alias_log = []
for keep, drop, reason in MERGES:
    assert keep in nodes and drop in nodes, (keep, drop)
    kn, dn = nodes[keep], nodes[drop]
    kn.setdefault('merged_facets', []).append(
        {'file': dn['file'], 'cid': dn['cid'], 'label': dn['label'],
         'note': dn['note']})
    # rewire edges
    for e in edges:
        if e['a'] == drop:
            e['a'] = keep
        if e['b'] == drop:
            e['b'] = keep
    del nodes[drop]
    alias_log.append({'keep': keep, 'drop': drop, 'reason': reason})

# drop self-loops created by rewiring, dedupe edges
seen, clean = set(), []
for e in edges:
    if e['a'] == e['b']:
        continue
    k = (e['a'], e['b'], e['rel'])
    if k not in seen:
        seen.add(k)
        clean.append(e)
edges = clean

# ---- reviewed cross-side adjudications ----
ADJ = [
 {
  'id': 'S0', 'verdict': 'split_link', 'seed': True,
  'a': 'af:a-w-f-g-m-f-conj-g-1-2-i-weil-s-hermitian-form-o',
  'b': 'rel:symmetric-guinand-weil-formula-with-square-test-',
  'relation': 'shares-classical-object',
  'reason': ('SEED CHECK — REPRODUCES. Same named classical referent: Weil\'s explicit '
             'formula / Hermitian form. AF defines W(f,g)=Σ m_ρ f̂(γ_ρ)·conj(ĝ(γ̄_ρ)) at §1.2 as the '
             'engine of the 2/3 bound (preprint; the positivity⟺RH equivalence cited to [Wei52,Bom00], '
             'not proved). The pilot presents the symmetric Guinand–Weil formula with normalization '
             'confirmed by its own numerics (exact) and verified zero-side vs prime-side to 2e-16 '
             '(computationally_verified). Different constructions (Hermitian form on C_c² vs symmetric '
             'Guinand–Weil with square test functions), different epistemic status, different purposes '
             '(proportion bound vs floor exhibition). Link, not merge (D3). The Atlas-5 Weil split_link '
             're-derives under focused blind re-extraction.')},
 {
  'id': 'A1', 'verdict': 'split_link',
  'a': 'bom:weil-s-rh-positivity-criterion-restated-local-ro',
  'b': 'rel:weil-s-criterion-w-h-0-for-all-admissible-square',
  'relation': 'shares-cited-criterion',
  'reason': ('Both cite Weil 1952\'s criterion (positivity ⟺ RH). BOM restates it as the platform for its '
             'proved strengthening (Theorem 1, exact); the pilot cites it as its honesty boundary '
             '(conjectural-from-this-text: what was derived is the prime-side presentation, not the '
             'criterion). Same cited referent, different roles — platform-for-proof vs honesty-boundary. '
             'Link, not merge.')},
 {
  'id': 'A2', 'verdict': 'split_link',
  'a': 'bom:li-s-criterion-as-used-in-the-proof-local-role-b',
  'b': 'rel:10b-li-s-criterion-via-the-face-sum-rh-n-0-n-n-e',
  'relation': 'shares-criterion',
  'reason': ('Both invoke Li\'s criterion (RH ⟺ λ_n ≥ 0). BOM uses it as the lemma for Theorem 1\'s converse '
             '(cited via Bombieri–Lagarias, conjectural-from-this-text); the pilot computed λ_n via the D1 '
             'face-sum as the most computable positivity criterion (heuristic/programmatic, D10b). Same '
             'criterion, different uses — proof-lemma vs computational program. Link, not merge.')},
 {
  'id': 'A3', 'verdict': 'split_link',
  'a': 'gro:prior-lineage-the-autocorrelation-mechanism-g-f-',
  'b': 'rel:square-dictionary-weil-s-h-h-2-corresponds-to-ou',
  'relation': 'lineage-cited-vs-independently-derived',
  'reason': ('Same generative move: squares manufacture positivity (Weil\'s g=f∗f̃ autocorrelation). GRO cites '
             'it as prior lineage (Weil [29], conjectural-from-this-text, preprint); the pilot DERIVED the '
             'square dictionary independently (h=|H|² ↔ P=|Q|², exact). Cited lineage vs independent '
             'derivation of the same move. Link, not merge. Strongest same-shape-independent-discovery pair '
             'in the run.')},
 {
  'id': 'A4', 'verdict': 'rejected',
  'a': 'gro:the-truncated-weil-quadratic-form-as-explicit-2n',
  'b': 'rel:the-prime-side-zero-detector-h-t0-w-sum-of-squar',
  'relation': None,
  'reason': ('Thematic resonance but no shared referent. GRO\'s object is a (2N+1)×(2N+1) Galerkin-matrix '
             'truncation of the form (preprint, exact definition); the pilot\'s is a sum-of-squares test '
             'function with exact Fourier pair used as a zero detector (exact). "Finite window on positivity" '
             'is shared framework, not shared referent (the Atlas-5 GUE near-miss pattern). Rejected.')},
 {
  'id': 'A5', 'verdict': 'split_link',
  'a': 'bom:theorem-8-negative-eigenvalues-of-h-gamma-t-dist',
  'b': 'af:bombieri-s-bom00-negative-index-observation-the-',
  'relation': 'proved-source-vs-cited-use',
  'reason': ('Same mathematical fact: negative index of truncations counts off-line pairs. BOM proves it '
             '(Theorem 8, exact, by deformation + induction); AF cites it ([Bom00] §1.3) as the observation '
             'behind its Pontryagin-index route (conjectural-from-this-text, preprint). Proved source vs '
             'cited use. Link, not merge. Within analytic side.')},
 {
  'id': 'A6', 'verdict': 'split_link',
  'a': 'af:b-weil-s-explicit-formula-as-one-of-the-paper-s-',
  'b': 'rel:the-explicit-formula-grounded-in-our-objects-psi',
  'relation': 'shared-input-different-grounding',
  'reason': ('Both take the explicit formula as input, grounded differently. AF lists it among its arithmetic '
             'inputs (§1.1, exact-as-listed, preprint); the pilot re-ground it in its own objects — ψ computed '
             'from the D1 face-sum, zeros regulating the face-sum error (computationally_verified). Cited input '
             'vs re-grounded input. Link, not merge.')},
 {
  'id': 'A7', 'verdict': 'rejected',
  'a': 'gro:theorem-2-5-finite-guinand-weil-dictionary-every',
  'b': 'rel:zero-side-vs-prime-side-agreement-to-machine-pre',
  'relation': None,
  'reason': ('Closest near-miss after A4. GRO proves its truncated dictionary\'s values equal exact zero sums '
             '(exact theorem, preprint); the pilot numerically verifies prime-side vs zero-side agreement to '
             '2e-16 (computationally_verified). Different objects (truncated Galerkin dictionary vs symmetric '
             'Guinand–Weil formula); what is shared is the verification *pattern*, which is framework, not '
             'referent (Atlas-5 GUE precedent). Rejected.')},
 {
  'id': 'A8', 'verdict': 'split_link',
  'a': 'bom:weil-s-rh-positivity-criterion-restated-local-ro',
  'b': 'af:a-w-f-g-m-f-conj-g-1-2-i-weil-s-hermitian-form-o',
  'relation': 'object-vs-criterion-about-it',
  'reason': ('AF defines the object (W(f,g), exact definition, preprint); BOM restates the criterion about '
             'that object\'s positivity (conjectural-from-this-text as restatement; its Theorem 1 strengthening '
             'is proved). The defined form vs the positivity claim about it. Charts the analytic neighborhood: '
             'what AF connects TO Weil. Link, not merge. Within analytic side.')},
 {
  'id': 'A9', 'verdict': 'rejected',
  'a': 'af:lemma-2-2-montgomery-vaughan-bilinear-form-for-t',
  'b': 'rel:10e-tools-large-sieve-positivity-of-quadratic-fo',
  'relation': None,
  'reason': ('Shared name, not shared referent. AF\'s Lemma 2.2 is a specific bilinear-form estimate for '
             'prime-side frequencies (exact); the pilot\'s 10e is a programmatic tools mention (large sieve, '
             'Montgomery\'s zero-density engine, heuristic). "Montgomery" as common ancestor is not a shared '
             'object. Rejected.')},
 {
  'id': 'A10', 'verdict': 'rejected',
  'a': 'rel:thesis-toward-weil-w-f-f-is-a-weighted-integral-',
  'b': 'af:a-w-f-g-m-f-conj-g-1-2-i-weil-s-hermitian-form-o',
  'relation': None,
  'reason': ('Covered by the seed (S0). The pilot\'s thesis (W as weighted integral of face-sum error, '
             'heuristic/programmatic) and AF\'s working engine share only the formula already adjudicated in '
             'S0; no independent referent. Rejected as duplicate-of-seed.')},
 {
  'id': 'A11', 'verdict': 'split_link',
  'a': 'gro:weil-positivity-rh-as-framing-positivity-of-the-',
  'b': 'af:a-positivity-of-w-on-all-of-c-c-2-r-is-equivalen',
  'relation': 'shared-cited-equivalence',
  'reason': ('Both cite the same equivalence (positivity ⟺ RH, [Wei52]/[Bom00]), both conjectural-from-this-text. '
             'Different roles: GRO\'s framing for its finite-rank program (preprint); AF\'s engine motivation '
             '(preprint). Same cited referent, different uses. Link, not merge. Within analytic side.')},
 {
  'id': 'A12', 'verdict': 'split_link',
  'a': 'bom:the-guinand-1942-weil-1952-lineage-local-role-d-',
  'b': 'rel:the-guinand-weil-explicit-formula-as-the-bridge-',
  'relation': 'lineage-account-vs-working-use',
  'reason': ('Both name the Guinand–Weil formula. BOM gives the historiographic lineage (Guinand 1942 → Weil 1952, '
             'exact-as-history); the pilot uses the symmetric formula as its working bridge (exact). Lineage '
             'account vs working use of the same named formula. Link, not merge.')},
]

# validate ids
for r in ADJ:
    assert r['a'] in nodes, r['a']
    assert r['b'] in nodes, r['b']

# cross-side edges for the bridge graph
xedges = []
for r in ADJ:
    if r['verdict'] == 'split_link':
        xedges.append({'a': r['a'], 'b': r['b'],
                       'rel': 'bridge:' + r['relation'], 'id': r['id']})

json.dump({'nodes': nodes, 'edges': edges, 'merges': alias_log},
          open(os.path.join(BASE, 'graphs', 'atlas6_graph.json'), 'w'),
          ensure_ascii=False, indent=1)
json.dump({'records': ADJ, 'cross_edges': xedges},
          open(os.path.join(BASE, 'cross_bridge_links.json'), 'w'),
          ensure_ascii=False, indent=1)
n_split = sum(1 for r in ADJ if r['verdict'] == 'split_link')
n_rej = sum(1 for r in ADJ if r['verdict'] == 'rejected')
print(f'nodes: {len(nodes)} (after {len(alias_log)} merges), '
      f'adjudications: {len(ADJ)} ({n_split} split_link incl. seed, {n_rej} rejected)')
print('seed S0 reproduces: YES')
