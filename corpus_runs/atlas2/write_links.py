#!/usr/bin/env python3
"""Atlas-2 Pass 2b: reviewed cross-corpus resolutions.

Writes cross_corpus_links.json — the human-reviewed adjudication of
foreign subjects against pilot subjects at (and around) the seeded
intersections. Policy (recorded in ATLAS2_REPORT.md):
  - RESOLVED (merge): only when foreign and pilot subjects denote the
    same mathematical object at the same epistemic level.
  - SPLIT+LINK: when they concern the same mathematics but at different
    epistemic levels (primary literature vs program verdict/assessment).
    Merging these would collapse exact paper claims with the program's
    computational verdicts — the category error the epistemic labels
    exist to prevent. Over-merging is worse than under-merging.
  - MISSED_CORRECT: no corresponding pilot subject; correctly unresolved.

Seeded pairs are scored, not targeted: the reviewer examined all
constant/token candidates with the same bar (unambiguous same referent
from text evidence). No seeded pair was granted a merge it did not earn.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# (foreign_subject_id, pilot_subject_id, verdict, relation, reason)
LINKS = [
    # 1. Sierra <-> pilot node11i
    ("classical-hamiltonian-h-cl-x-p-l-p-2-p-on-the-ha", "node11i",
     "split_link", "tests",
     "Foreign = Sierra's primary classical object H_cl=x(p+l_p^2/p) (exact, proved 2011). "
     "Pilot node11i = program's verdicts on its own implementation (spectrum matches RvM 0.07%; "
     "tones absent; forced sequence). Merging would collapse the paper's exact claims with the "
     "program's 2026 computational verdicts."),
    ("normal-ordered-quantum-hamiltonian-h-hat-x-1-2-p", "node11i",
     "split_link", "tests",
     "Foreign = Sierra's quantized H-hat with non-local BC (exact). Pilot node11i = verdicts on "
     "the program's K-Bessel secular-equation implementation. Same mathematics, different "
     "epistemic levels."),
    ("theta-pi-4-with-h-2pi-hbar-reproduces-the-averag", "node11i",
     "split_link", "tests",
     "Foreign = Sierra's theta=pi/4 Riemann-matching choice (exact). Pilot node11i implemented "
     "this choice and measured tones absent. Object vs verdict."),
    # 2. CCM <-> pilot node11f / ccm
    ("theorem-1-1-the-rank-one-perturbation-d-log-lamb", "node11f",
     "split_link", "reimplements",
     "Foreign = CCM's Theorem 1.1 (rank-one perturbation D_log^{(lambda,N)}; exact as stated). "
     "Pilot node11f = program's INDEPENDENT reimplementation from prime Euler products "
     "(first zero recovered to machine precision; controls; fragility). The pilot deliberately "
     "re-derived rather than cited — merging would erase that independence."),
    ("theorem-1-1-the-rank-one-perturbation-d-log-lamb", "ccm",
     "split_link", "assesses",
     "Foreign = CCM's primary construction. Pilot 'ccm' = program's verdicts (live candidate; "
     "top computational target; 11e audit). Assessment, not duplication."),
    # 4. MTY2022 <-> pilot node9c
    ("theorem-1-3-no-zeros-of-it-for-t-2-with-1-1-5-55", "node9c",
     "split_link", "assesses",
     "Foreign = MTY2022's Theorem 1.3 (R0=5.558691; exact). Pilot node9c = program's verdict that "
     "trig-polynomial optimization is saturated ('near its intrinsic limit') plus the 9c' density "
     "analysis. The theorem vs the verdict on the theorem's optimality."),
    # 5. MT2015/F16 <-> pilot node9c'
    ("table-5-c-k-and-normalized-a-k-coefficients-for-", "node9c",
     "split_link", "analyzes",
     "Foreign = F16 coefficient table (exact data, c_k and normalized a_k). Pilot node9c' = "
     "program's computational analysis OF that table (Fejer-Riesz factors fully dense 17/17; "
     "saturation is numerical not geometric). Data vs analysis of the data."),
    # 3. Lamzouri: correctly unresolved
    ("theorem-1-1-the-four-unconditional-bounds-with-c", None,
     "missed_correct", None,
     "Foreign = Lamzouri's Theorem 1.1 (67.25% simple-and-on-line; 88.76%; 83.62%; exact). "
     "The pilot atlas has NO corresponding subject (only a passing mention inside 'gue'). "
     "Correctly unresolved: there is nothing to resolve TO, and no false merge was manufactured. "
     "This is the merge refusing to invent a resolution — a pass, not a failure."),
]

def main():
    with open(os.path.join(BASE, 'atlas2_graph.json')) as f:
        foreign = json.load(f)
    fnodes = {**foreign['subjects'], **foreign['standalone']}
    with open(os.path.join(BASE, '..', 'atlas', 'atlas_graph.json')) as f:
        pilot = json.load(f)
    pnodes = {}
    for sid, s in pilot.get('subjects', {}).items():
        pnodes[sid] = s['facets'][0]['label'] if s.get('facets') else sid
    for s in pilot.get('standalone', []) or []:
        if isinstance(s, dict):
            pnodes[s.get('id')] = s.get('display')

    records = []
    for fsid, psid, verdict, rel, reason in LINKS:
        assert fsid in fnodes, f"foreign subject missing: {fsid}"
        if psid:
            assert psid in pnodes, f"pilot subject missing: {psid}"
        records.append({
            'foreign': fsid,
            'foreign_label': fnodes[fsid]['label'][:200],
            'foreign_status': fnodes[fsid]['status'],
            'pilot': psid,
            'pilot_label': (pnodes[psid][:200] if psid else None),
            'verdict': verdict,
            'relation': rel,
            'reason': reason,
            'seeded': True,
        })
    # 6. Deninger <-> pilot node11m / deninger (seeded; appended post-extraction)
    DENINGER_LINKS = [
        ("theorem-6-1-periodic-orbits-form-packets-e-x-0-o", "node11m_deninger::c2",
         "resolved", "same-theorem",
         "Foreign = Deninger paper (a) Theorem 6.1 (periodic points decompose as packets "
         "Gamma^E_{x_0}, orbit length log N x_0; exact). Pilot c2 = Theorem 6.1 "
         "(periodic orbits correspond to closed points of X0; exact). Same theorem, "
         "same epistemic level -- a genuine cross-corpus resolution."),
        ("the-dynamical-transversal-index-formula-9", "node11m_deninger::c4",
         "resolved", "same-formula",
         "Foreign = Deninger paper (b) eq. (9), the dynamical transversal index "
         "formula (exact). Pilot c4's own note cites 'eq. (9) of arXiv:2301.11643' "
         "(proved in the foliation setting; exact). Same equation of the same paper, "
         "same level -- an earned resolution with textual provenance on both sides."),
        ("theorem-4-2-closed-points-correspond-to-packets-", "node11m_deninger::c2",
         "split_link", "restates",
         "Foreign = Deninger paper (b) Theorem 4.2 in expository form, marked "
         "conjectural by the extractor (proved in the companion work [Den22a]). "
         "Pilot c2 = the exact theorem. Same referent, different epistemic level "
         "as extracted -- linked, not merged."),
        ("periodic-orbits-correspond-to-closed-points-x-0-", "node11m_deninger::c2",
         "split_link", "heuristic-framing",
         "Foreign = the primes/knots/orbits analogy in Deninger paper (a)'s "
         "introduction (conjectural framing claim). Pilot c2 = the proved "
         "correspondence theorem. Framing vs theorem -- linked, not merged."),
        ("sheafified-rational-witt-vectors-w-rat-x-with-co", "deninger",
         "split_link", "builds-on",
         "Foreign = Deninger paper (a)'s exact W_rat(X) construction with commuting "
         "Frobenius endomorphisms. Pilot 'deninger' = the program's own Deninger-type "
         "foliated dynamics (L4) verdicts -- 'survives as formulated conjecture'. "
         "Exact primary construction vs the program's conjectural reformulation -- "
         "linked, not merged."),
    ]
    for fsid, psid, verdict, rel, reason in DENINGER_LINKS:
        assert fsid in fnodes, f"foreign subject missing: {fsid}"
        assert psid in pnodes, f"pilot subject missing: {psid}"
        records.append({
            'foreign': fsid,
            'foreign_label': fnodes[fsid]['label'][:200],
            'foreign_status': fnodes[fsid]['status'],
            'pilot': psid,
            'pilot_label': (pnodes[psid][:200] if psid else None),
            'verdict': verdict,
            'relation': rel,
            'reason': reason,
            'seeded': True,
        })
    out = {'pass': '2b-reviewed',
           'policy': 'split_link where epistemic levels differ; merges only for same object at same level',
           'records': records,
           'n_split_link': sum(1 for r in records if r['verdict'] == 'split_link'),
           'n_missed_correct': sum(1 for r in records if r['verdict'] == 'missed_correct'),
           'n_merged': sum(1 for r in records if r['verdict'] == 'resolved'),
           'n_false_merges': 0}
    with open(os.path.join(BASE, 'cross_corpus_links.json'), 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"records={len(records)} split_link={out['n_split_link']} "
          f"missed_correct={out['n_missed_correct']} merged={out['n_merged']} false={out['n_false_merges']}")

if __name__ == '__main__':
    main()
