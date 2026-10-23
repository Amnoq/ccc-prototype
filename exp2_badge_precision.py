"""exp2_badge_precision.py -- are shared rare badges high-precision
SAME evidence? Uses the 1,800 human-labeled pairs (locked truth labels).

For each fold: extract badges (same fixed patterns), compute badge df,
then among LABELED pairs sharing >=1 rare badge (df<=3), measure
precision = SAME / (SAME + DIFFERENT). Baseline: overall labeled
precision. Also split by badge type.
"""
import json, glob, re
from collections import Counter, defaultdict
import sys
sys.path.insert(0, '/home/hatch/workspace/ccc-prototype')
from exp2_badges import badges, toks, idf_weights, vec, cos, concepts, entity_text

for i in range(1, 13):
    held = f'c{i:02d}'
    registry = json.load(open(f'corpus_runs/exp2_folds/fold_{held}_registry.json'))
    eid2e = {e['entity_id']: e for e in registry}
    hcon = {c['cid']: c for c in concepts if c['chunk'] == held}
    batch = {p['pair_id']: p for p in
             json.load(open(f'corpus_runs/exp2_folds/fold_{held}_truth.json'))}
    labels = json.load(open(f'corpus_runs/exp2_folds/fold_{held}_truth_labels.json'))

    ebadges = [badges(entity_text(e)) for e in registry]
    qbmap = {cid: badges(c['label'] + ' ' + c['note']) for cid, c in hcon.items()}
    bdf = Counter()
    for doc in ebadges + list(qbmap.values()):
        for b in set(doc):
            bdf[b] += 1
    rare = {b for b, c in bdf.items() if c <= 3}
    emap = {e['entity_id']: set(b for b in eb if b in rare) for e, eb in zip(registry, ebadges)}
    qmap = {cid: set(b for b in qb if b in rare) for cid, qb in qbmap.items()}

    tot_s = tot_d = 0
    hit_s = hit_d = 0
    by_type = defaultdict(lambda: [0, 0])  # type -> [same, diff]
    hit_pairs = []
    for l in labels:
        p = batch[l['pair_id']]
        v = l['verdict']
        if v == 'UNCERTAIN':
            continue
        shared = qmap[p['held_cid']] & emap[p['entity_id']]
        if v == 'SAME':
            tot_s += 1
        else:
            tot_d += 1
        if shared:
            if v == 'SAME':
                hit_s += 1
            else:
                hit_d += 1
            t = shared.pop().split(':')[0] if len(shared) == 1 else 'multi'
            # attribute to all shared types
            for b in (qmap[p['held_cid']] & emap[p['entity_id']]):
                by_type[b.split(':')[0]][0 if v == 'SAME' else 1] += 1
            hit_pairs.append((v, p['held_cid'], p['entity_id'], sorted(shared)[:3]))
    prec_all = tot_s / (tot_s + tot_d)
    prec_hit = hit_s / (hit_s + hit_d) if (hit_s + hit_d) else 0
    print(f"{held}: labeled SAME {tot_s}/{tot_s+tot_d} (base prec {prec_all:.3f}) | "
          f"with shared rare badge: SAME {hit_s}, DIFF {hit_d} (prec {prec_hit:.3f}, n={hit_s+hit_d})")
    globals().setdefault('agg', defaultdict(lambda: [0, 0]))
    globals().setdefault('aggt', [0, 0, 0, 0])
    agg['__all__'][0] += hit_s
    agg['__all__'][1] += hit_d
    aggt[0] += tot_s
    aggt[1] += tot_d
    for t, (s, d) in by_type.items():
        agg[t][0] += s
        agg[t][1] += d

print(f"\nPOOLED: base precision {aggt[0]/(aggt[0]+aggt[1]):.3f} ({aggt[0]}/{aggt[0]+aggt[1]})")
s, d = agg.pop('__all__')
print(f"POOLED with shared rare badge: precision {s/(s+d):.3f} ({s} SAME / {d} DIFF, n={s+d})")
print("\nby badge type:")
for t, (s, d) in sorted(agg.items(), key=lambda x: -(x[1][0] + x[1][1])):
    print(f"  {t:8} prec {s/(s+d):.3f}  ({s}/{d}, n={s+d})")
