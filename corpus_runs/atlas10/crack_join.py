#!/usr/bin/env python3
"""Atlas-10 crack hunt: positional join of annotator judgments
(annot_p2, games G28/G42) with engine per-ply data (engine_raw.json).
For each judged played move: engine rank, loss, and eval swing.
Output: crack_join.json for coordinator adjudication."""
import json, re, os

BASE = os.path.expanduser("~/workspace/ccc-prototype/corpus_runs/atlas10")
raw = json.load(open(os.path.join(BASE, 'engine_raw.json')))
ann = json.load(open(os.path.join(BASE, 'extractions', 'annot_p2.json')))

# game tag -> engine game id
GMAP = {'Lasker-Tarrasch': 'g1_lasker_tarrasch',
        'Zukertort-Steinitz': 'g2_zukertort_steinitz'}

def move_to_ply(movestr):
    """'25...f6' -> 50 ; '9.Qxc3' -> 17 (1-based ply of the move)."""
    m = re.match(r'(\d+)(\.\.\.|\.)', movestr.strip())
    n = int(m.group(1))
    return 2 * n if m.group(2) == '...' else 2 * n - 1

rows = []
for a in ann['anchors']:
    note = a['note']
    m = re.match(r'G\d+\s+([A-Za-z\-]+),\s+(\d+(?:\.\.\.|\.)[A-Za-z0-9+\-=]+)',
                 note)
    if not m:
        continue
    game_tag, movestr = m.group(1), m.group(2)
    if game_tag not in GMAP:
        continue
    # skip variation fragments
    if 'variation' in note or 'fragment' in note:
        continue
    gid = GMAP[game_tag]
    ply = move_to_ply(movestr)  # 1-based ply of the played move
    pos = raw['games'][gid]['positions']
    # position where the move was played = index ply-1 (ply 0 = initial)
    before = pos[ply - 1] if ply - 1 < len(pos) else None
    after = pos[ply] if ply < len(pos) else None
    j = re.search(r'["\u201c](.*)["\u201d]\s*$', note, re.S)
    judgment = (j.group(1) if j else note)[:220]
    loss = (before.get('played_loss_cp_mover') if before else None)
    rows.append({
        'game': gid, 'move': movestr, 'ply': ply,
        'judgment': judgment,
        'engine_rank': before.get('played_rank') if before else None,
        'engine_loss_cp': loss,
        'engine_swing_cp': after.get('swing_cp_wrel') if after else None,
        'engine_best_cp_after': after.get('best_cp_wrel') if after else None,
    })

json.dump(rows, open(os.path.join(BASE, 'crack_join.json'), 'w'), indent=1)
for r in rows:
    print(f"{r['game'][:2]} {r['move']:10s} rank={r['engine_rank']} "
          f"loss={r['engine_loss_cp']} swing={r['engine_swing_cp']}")
    print(f"    annot: {r['judgment'][:110]}")
print(len(rows), 'joined judgments')
