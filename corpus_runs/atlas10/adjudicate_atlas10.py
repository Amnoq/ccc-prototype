#!/usr/bin/env python3
"""Atlas-10 adjudication: coordinator-reviewed verdicts (STABLE node ids).
Verdicts: split_link (shared referent, different roles) /
rejected (with reason). Coordinator reviewed all 90 mechanical
cross-sky candidates individually (2026-10-08): 4 genuine, 86
spurious token overlap. Three further split_links added manually
(C2 control, Q+K and R+K mate claims vs engine outcomes) — the
engine drafters' neutral vocabulary yields no token overlap by
design, so engine<->literature links are earned by the crack hunt,
not the token matcher. Never invent a resolution."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
nodes = json.load(open(os.path.join(BASE, 'graphs',
                                    'atlas10_merged.json')))['nodes']

ADJ = [
 {
  "id": "A10-01", "verdict": "split_link", "control": "C1",
  "pair": "engine-theory",
  "a": "engine:engine_positions:c5:c1-control-verdict-resolved",
  "b": "theory:theory_capablanca:c41:control-c1-knight-bishop-mate-must-be-accomplished-w",
  "relation": "shares-claim",
  "role_difference": "theory: states the KBN forced-mate rule within the fifty-move limit as teachable knowledge (Capablanca ch. 15); engine: executes the claim on a fixed FEN, reporting mate-in-2 (<= 50 required)",
  "reason": "C1 CONTROL, pre-registered: the book's forced-mate claim resolves against the engine. Both verified independently before adjudication.",
  "crack": None,
 },
 {
  "id": "A10-02", "verdict": "split_link", "control": "C2",
  "pair": "engine-annotations",
  "a": "engine:engine_positions:c6:c2-control-readout-and-verdict-mate-in-8-99992-cp-wh",
  "b": "annotations:annot_p2:c72:25-f6-this-move-or-resigning-there-is-nothing-else",
  "relation": "shares-assessment",
  "role_difference": "annotations: the annotator's verdict 'this move, or resigning' on 25...f6 in Lasker-Tarrasch (Blue Book game 70); engine: depth-20 analysis of the fixed post-25...f6 FEN reporting mate-in-8 for White",
  "reason": "C2 CONTROL, pre-registered: the annotator's winning claim resolves against the engine — and the engine strengthens it (mate, not merely winning).",
  "crack": None,
 },
 {
  "id": "A10-03", "verdict": "split_link", "control": None,
  "pair": "engine-theory",
  "a": "engine:engine_positions:c3:f2-outcome-class-mate-in-1-99999-cp-white-relative",
  "b": "theory:theory_capablanca:c6:queen-king-vs-king-easiest-mate-under-ten-moves",
  "relation": "shares-claim",
  "role_difference": "theory: Q+K mates in under ten moves (a bound for the student); engine: mate-in-1 from the fixed FEN (the position was already terminal-adjacent)",
  "reason": "Same claim (Q+K forces mate), different roles: the book teaches the bound, the engine exhibits the instance. Not a merge: the book's 'under ten' is pedagogical, the engine's 'mate in 1' is positional.",
  "crack": None,
 },
 {
  "id": "A10-04", "verdict": "split_link", "control": None,
  "pair": "engine-theory",
  "a": "engine:engine_positions:c4:f3-outcome-class-mate-in-1-99999-cp-white-relative",
  "b": "theory:theory_capablanca:c3:rook-k-vs-k-mate-in-under-twenty-moves",
  "relation": "shares-claim",
  "role_difference": "theory: R+K mates in under twenty moves; engine: mate-in-1 from the fixed FEN",
  "reason": "Same claim, different roles, as A10-03.",
  "crack": None,
 },
 {
  "id": "A10-05", "verdict": "split_link", "control": None,
  "pair": "annotations-theory",
  "a": "annotations:annot_p1:c32:g08-tchigorin-pillsbury-8-ne7-something-like-a-leap-",
  "b": "theory:theory_lasker:c83:vs-the-b-kt5-pin-b-k3-the-doubled-pawn-is-no-harm",
  "relation": "shares-object",
  "role_difference": "annotations: the doubled pawn as a weakness to 'dissolve betimes' or compensate via the open file (game-specific, conditional); theory (Lasker): the doubled pawn 'in no way detrimental' — actively advantageous via the opened file (principled, unconditional)",
  "reason": "Same object (doubled pawns), genuinely different stances: the annotator treats them as a defect to manage, Lasker as an asset. Mild tension surfaced, not resolved.",
  "crack": None,
 },
 {
  "id": "A10-06", "verdict": "split_link", "control": None,
  "pair": "annotations-theory",
  "a": "annotations:annot_p2:c11:advance-the-g-pawn-and-sacrifice-the-n-as-in-the-muz",
  "b": "theory:theory_lasker:c8:gambit",
  "relation": "shares-concept",
  "role_difference": "annotations: invokes the Muzio Gambit as a concrete attacking model ('sacrifice your N, as in the Muzio'); theory: the dictionary definition ('an opening in which a pawn sacrifice is offered')",
  "reason": "Same concept, different roles: the annotator uses the gambit, the theorist defines it. Thin but genuine.",
  "crack": None,
 },
 {
  "id": "A10-07", "verdict": "split_link", "control": None,
  "pair": "annotations-theory",
  "a": "annotations:annot_p2:c65:6-nf3-the-best-line-against-the-mccutcheon-defence-s",
  "b": "theory:theory_lasker:c91:open-theoretical-questions-ruy-lopez-diag-26-continu",
  "relation": "shares-opening",
  "role_difference": "annotations: confident verdict — 6.Nf3 'the best line' vs the McCutcheon (citing Sjoberg-Giersing 1906); theory (Lasker): the McCutcheon 5.P-K5 verdict listed among OPEN theoretical questions",
  "reason": "Same opening, different epistemic stances: the annotator asserts, the theorist leaves open. A genuine narrow bridge between confident practice and honest theory.",
  "crack": None,
 },
]

# Bulk rejects: all mechanical candidates except the 4 genuine
# (indices 4, 45, 77, 89 in the regenerated cross_candidates.json).
xc = json.load(open(os.path.join(BASE, 'cross_candidates.json')))
GENUINE = {4, 45, 77, 89}
for i, c in enumerate(xc):
    if i in GENUINE:
        continue
    ADJ.append({
        "id": f"A10-R{i:02d}", "verdict": "rejected", "control": None,
        "pair": c['pair'], "a": c['a'], "b": c['b'],
        "relation": None, "role_difference": None,
        "reason": ("Spurious token overlap (" + ",".join(c['shared']) +
                   "); no shared referent on coordinator review of all " +
                   "90 candidates. Labels: " + c['a_label'][:60] + " // " +
                   c['b_label'][:60]),
        "crack": None,
    })

# validate every referenced id exists (fail loudly on stale refs);
# resolve merge aliases (a referenced node may have been merged away)
all_ids = set(nodes)
alias = {}
for nid, n in nodes.items():
    for m in n.get('merged_from') or []:
        alias[m] = nid
def resolve_id(x):
    return alias.get(x, x)

for a in ADJ:
    for k in ('a', 'b'):
        if a[k]:
            a[k] = resolve_id(a[k])
            assert a[k] in all_ids, f"STALE ADJ REF: {a['id']} {k} {a[k][:70]}"

json.dump(ADJ, open(os.path.join(BASE, 'atlas10_adjudications.json'), 'w'),
          indent=1)
v = [a['verdict'] for a in ADJ]
print(f"{len(ADJ)} adjudications: {v.count('split_link')} split_link, "
      f"{v.count('rejected')} rejected, {v.count('merge')} merge")
