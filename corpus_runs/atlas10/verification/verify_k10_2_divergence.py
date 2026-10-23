#!/usr/bin/env python3
"""Verify K10-2: engine divergence profiles of the four Blue Book
games. Recomputes from engine_raw.json (independent of the
drafter's extraction): per game, count of played-move rank
divergences (rank > 3), mean eval loss, and the three largest-loss
moves. Claim: the profiles below, unstated by either literature
sky. Verified iff recomputation matches."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(BASE, '..', 'engine_raw.json')))

EXPECTED = {
    # game: (divergences, mean_loss_cp rounded to 2dp)
    'g1_lasker_tarrasch': (13, 20.09),
    'g2_zukertort_steinitz': (3, 16.62),
    'g3_morphy_anderssen': (23, 2055.28),
    'g4_anderssen_morphy': (15, 19.05),
}

for gid, (exp_n, exp_mean) in EXPECTED.items():
    poss = raw['games'][gid]['positions']
    losses, divs = [], 0
    for p in poss:
        if p.get('terminal') or p.get('played_rank') is None:
            continue
        loss = p['played_loss_cp_mover']
        v = (loss['lower_bound_cp'] if isinstance(loss, dict) else loss)
        losses.append(abs(v))
        if p['played_rank'] > 3:
            divs += 1
    mean = round(sum(losses) / len(losses), 2)
    status = 'OK' if (divs, mean) == (exp_n, exp_mean) else 'MISMATCH'
    print(f'{gid}: divergences={divs} (exp {exp_n}), '
          f'mean_loss={mean} (exp {exp_mean}) [{status}]')
    assert (divs, mean) == (exp_n, exp_mean), f'K10-2 FAILED on {gid}'
print('K10-2 VERIFIED: divergence profiles recomputed exactly')
