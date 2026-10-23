#!/usr/bin/env python3
"""Build Atlas-10 grading_packet.md: sampled triples + ALL
adjudications + drops + controls, for the user's grade."""
import json, os, random

BASE = os.path.dirname(os.path.abspath(__file__))
nodes = json.load(open(os.path.join(BASE, 'graphs',
                                    'atlas10_merged.json')))['nodes']
adj = json.load(open(os.path.join(BASE, 'atlas10_adjudications.json')))

def lab(nid):
    n = nodes[nid]
    return f"[{n['file']}/{n['cid']}] `{n['status']}` — {n['label'][:150]}"

L = []
L.append("# Atlas-10 Grading Packet\n")
L.append("**Date:** 2026-10-08 · **Run:** chess atlas "
         "(theory / annotations / engine)")
L.append("**Bar:** 0 false merges, 0 contradictions.")
L.append("**Corpus:** Capablanca *Chess Fundamentals* (Gutenberg #33870), "
         "Lasker *Chess Strategy* (#5614), Blue Book of Chess (#16377, "
         "85 annotated games); Stockfish 17.1, 4 games + 3 FENs.\n")

L.append("## Controls (both resolved)\n")
L.append("- **C1 (theory↔engine):** Capablanca ch. 15 KBN forced mate "
         "within fifty moves → engine mate-in-2. RESOLVED.")
L.append("- **C2 (annotations↔engine):** Blue Book game 70 note at "
         "25...f6 ('This move, or resigning') → engine mate-in-8 "
         "White. RESOLVED and strengthened.\n")

L.append("## Sampled triples (12: 4 per sky)\n")
random.seed(10)
for sky in ('theory', 'annotations', 'engine'):
    L.append(f"### {sky}")
    ids = [nid for nid, n in nodes.items() if n['sky'] == sky]
    for nid in random.sample(ids, min(4, len(ids))):
        L.append(f"- {lab(nid)}")
    L.append("")

L.append(f"## ALL adjudications ({len(adj)})\n")
for a in adj:
    ctl = f" (CONTROL {a['control']})" if a['control'] else ""
    L.append(f"### {a['id']} — `{a['verdict']}`{ctl}")
    L.append(f"- **pair:** {a['pair']}")
    if a['a']:
        L.append(f"- **a:** {lab(a['a'])}")
    if a['b']:
        L.append(f"- **b:** {lab(a['b'])}")
    if a.get('role_difference'):
        L.append(f"- **role difference:** {a['role_difference'][:400]}")
    L.append(f"- **reason:** {a['reason'][:500]}")
    if a.get('crack'):
        L.append(f"- **crack:** {a['crack']}")
    L.append("")

L.append("## Merges applied (9 reviewed)\n")
L.append("- 6 merged groups (blindfold-context notes ×4 pairs→1 group; "
         "two-knights theorem; B+Kt corner rule; general-plan doctrine; "
         "opposite-bishops draw; piece-value=mobility [FLAGGED WEAK]).")
L.append("- 31 within-sky candidates rejected as spurious token overlap.\n")
L.append("## Drops\n")
L.append("- None. All three skies produced. "
         "(E4 segment never began in 3/4 games; E5 found zero — "
         "recorded as procedure limitations, not drops.)\n")
L.append("## Cracks\n")
L.append("- K10-1 ✅ verified (annotator–engine directional agreement 9/9; "
         "exploratory comparison, labeled as such)")
L.append("- K10-2 ✅ verified (divergence profiles recomputed exactly)")
L.append("- 0 refuted · 0 undecidable\n")
L.append("## Method incidents (for the grade)\n")
L.append("- annot_p1 drafter wrote status words into label fields; "
         "repaired mechanically from its own anchor notes "
         "(backup: extractions/annot_p1_raw.json).")
L.append("- Two runner bugs caught by background runs (multipv=1 list "
         "shape; <3-legal-move PV count); fixed, logged.")
L.append("- Node-id instability caught by the adjudication validator "
         "(slug collisions across re-runs); fixed with cid-keyed stable "
         "ids + alias resolution. The validator now fails loudly on any "
         "stale reference.")
L.append("- One VM restart killed a background run; text extractions "
         "survived, engine leg re-ran cleanly.\n")

out = os.path.join(BASE, 'grading_packet.md')
open(out, 'w').write('\n'.join(L))
print('wrote', out, f'({len(adj)} adjudications)')
