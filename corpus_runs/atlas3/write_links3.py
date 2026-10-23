#!/usr/bin/env python3
"""Atlas-3 Pass 2: reviewed cross-sky adjudication (coordinator-reviewed).

Policy (charter + Atlas-2 D3):
  - resolved (merge): same mathematical object, same epistemic level.
  - split_link: genuine relationship but not the same object
    (different objects, different levels, or shared discipline).
  - rejected: mechanical candidate with no genuine link (spurious
    token match or false friend) — recorded, not silently dropped.
  - control_void: a seeded control that cannot pass as designed.

Direct test: algebra<->geometry. Controls: S1 bridge<->algebra,
S2 bridge<->geometry.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def nodes(sky):
    with open(os.path.join(BASE, 'graphs', f'{sky}_graph.json')) as f:
        g = json.load(f)
    return {**g['subjects'], **g['standalone']}

def rec(a_sky, a, b_sky, b, verdict, relation, reason, control):
    A, B = nodes(a_sky), nodes(b_sky)
    assert a in A, f"{a_sky} node missing: {a}"
    assert b in B, f"{b_sky} node missing: {b}"
    return {'a_sky': a_sky, 'a': a, 'a_label': A[a]['label'][:200],
            'a_status': A[a]['status'],
            'b_sky': b_sky, 'b': b, 'b_label': B[b]['label'][:200],
            'b_status': B[b]['status'],
            'verdict': verdict, 'relation': relation, 'reason': reason,
            'control': control}

RECORDS = [
    # ---- S1: bridge <-> algebra (positive control) ----
    rec('bridge', 'automorphic-representations-irreducible-represen',
        'algebra', 'iti-kg-resp-its-kg-a-set-of-representatives-of-t',
        'split_link', 'shares-discipline',
        "S1 WEAK PASS. Genuine field-level relationship: the bridge's core "
        "subject (automorphic representations of GL_n(A_F)) and the algebra "
        "sky's core subject (modular representation theory of finite groups) "
        "are both representation theory. Different objects (adelic groups vs "
        "finite groups in characteristic p), so linked as shared discipline, "
        "NOT merged. Found ONLY by semantic review — the mechanical "
        "token-overlap pass missed it (R&D finding: mechanical recall fails "
        "across domain vocabularies).",
        'S1'),
    rec('bridge', 'galois-representation-sigma-e-ell-from-the-first',
        'algebra', '5-for-fixed-k-in-delta-the-members-of-e-w-over-k',
        'rejected', None,
        "Mechanical candidate (shared tokens 'galois','sigma') correctly "
        "rejected by review: FALSE FRIEND. Bridge = continuous representation "
        "of Gal(Qbar/Q) on l-adic etale cohomology (arithmetic). Algebra = "
        "(K,V^sigma) for sigma in Aut(K/F), field automorphisms acting on "
        "module structures. Same word, different referents.",
        'S1'),
    rec('bridge', 'taniyama-shimura-conjecture-proved-by-wiles-and-',
        'algebra', 'example-4-9-the-surjection-s-x-x-2-s-with-s-not-',
        'rejected', None,
        "Mechanical candidate (shared generic tokens 'between','implies',"
        "'over','theorem') correctly rejected: unrelated referents "
        "(Taniyama-Shimura bijection vs a Gorenstein ring-theory example). "
        "Spurious token match.",
        'S1'),
    # ---- direct test: algebra <-> geometry ----
    rec('algebra', 'example-4-9-the-surjection-s-x-x-2-s-with-s-not-',
        'geometry', 'u00a77-3-alternative-proof-of-a-weakened-no-loca',
        'rejected', None,
        "Mechanical candidate (shared generic tokens 'corollary','local',"
        "'theorem') correctly rejected: unrelated referents (ring-theory "
        "example vs Ricci-flow proof technique). Spurious token match. "
        "Direct A<->G test: no genuine links found by mechanical OR semantic "
        "review.",
        'direct'),
    # ---- S2: bridge <-> geometry (positive control) ----
    {'a_sky': 'bridge', 'a': None, 'a_label': 'geometric Langlands content (Hecke eigensheaves, Bun_G, moduli of bundles)',
     'a_status': None, 'b_sky': 'geometry', 'b': None,
     'b_label': 'differential-geometry sky (Ricci flow, minimal surfaces)',
     'b_status': None, 'verdict': 'control_void', 'relation': None,
     'reason': "S2 VOID (misseeded, not method failure). Geometric Langlands "
               "touches COMPLEX-ALGEBRAIC geometry (holomorphic bundles, "
               "D-modules on Bun_G); the geometry sky as built is "
               "DIFFERENTIAL geometry (Ricci flow, minimal surfaces). No "
               "shared objects exist at node level at this chunk depth — the "
               "method correctly found nothing because there is nothing at "
               "node level. R&D spec: positive controls must be seeded "
               "against the right subfield; 'geometry' is not one sky.",
     'control': 'S2'},
]

def main():
    out = {'pass': '2-reviewed',
           'policy': 'resolved only for same object at same level; '
                     'split_link for genuine non-identity relationships; '
                     'rejected candidates recorded, never silently dropped',
           'records': RECORDS,
           'n_split_link': sum(1 for r in RECORDS if r['verdict'] == 'split_link'),
           'n_rejected': sum(1 for r in RECORDS if r['verdict'] == 'rejected'),
           'n_merged': sum(1 for r in RECORDS if r['verdict'] == 'resolved'),
           'n_control_void': sum(1 for r in RECORDS if r['verdict'] == 'control_void'),
           'n_false_merges': 0,
           'direct_links': 0}
    with open(os.path.join(BASE, 'cross_sky_links.json'), 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"records={len(RECORDS)} split_link={out['n_split_link']} "
          f"rejected={out['n_rejected']} merged={out['n_merged']} "
          f"void={out['n_control_void']} direct_links={out['direct_links']}")

if __name__ == '__main__':
    main()
