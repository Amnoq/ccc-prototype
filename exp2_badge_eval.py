"""exp2_badge_eval.py -- evaluate badge fusion variants on saved candidates.

Variants (all deterministic, no tuned weights):
- V0 tfidf: rank by TF-IDF cosine (baseline).
- V1 sum: tfidf_cos + badge_cos (naive equal-weight fusion).
- V2 cond: V1 iff query has >=1 badge else V0 (badges vote only when present).
- V3 rare-sum: tfidf_cos + rare_badge_cos (badges with df<=3 only).
- V4 rerank20: TF-IDF top-20, reranked by (rare_badge_cos desc, tfidf_cos desc).
- V5 rerank20-cond: V4 iff query has >=1 rare badge else V0.

Ground truth: 144 SAME pairs (pre-correction set; deltas are the finding).
"""
import json

res = json.load(open('corpus_runs/exp2_badge_cands.json'))

def rank_of(cands, true_ei, key):
    order = sorted(range(len(cands)), key=lambda k: -key(cands[k]))
    # map position -> entity index
    for pos, k in enumerate(order):
        if cands[k][0] == true_ei:
            return pos
    raise AssertionError('truth not in candidates')

def evaluate(variant):
    ranks = []
    for q in res:
        c = q['cands']
        true = q['true_ei']
        if variant == 'V0':
            r = rank_of(c, true, lambda x: x[1])
        elif variant == 'V1':
            r = rank_of(c, true, lambda x: x[1] + x[2])
        elif variant == 'V2':
            r = rank_of(c, true, lambda x: x[1] + x[2] if q['q_has_badge'] else x[1])
        elif variant == 'V3':
            r = rank_of(c, true, lambda x: x[1] + x[3])
        elif variant == 'V4':
            top20 = sorted(range(len(c)), key=lambda k: -c[k][1])[:20]
            # rerank top20 by rare-badge then tfidf; rest keep tfidf order after
            top20_sorted = sorted(top20, key=lambda k: (-c[k][3], -c[k][1]))
            rest = [k for k in sorted(range(len(c)), key=lambda k: -c[k][1]) if k not in set(top20)]
            order = top20_sorted + rest
            r = next(pos for pos, k in enumerate(order) if c[k][0] == true)
        elif variant == 'V5':
            if q['q_has_rare_badge']:
                top20 = sorted(range(len(c)), key=lambda k: -c[k][1])[:20]
                top20_sorted = sorted(top20, key=lambda k: (-c[k][3], -c[k][1]))
                rest = [k for k in sorted(range(len(c)), key=lambda k: -c[k][1]) if k not in set(top20)]
                order = top20_sorted + rest
                r = next(pos for pos, k in enumerate(order) if c[k][0] == true)
            else:
                r = rank_of(c, true, lambda x: x[1])
        ranks.append(r)
    n = len(ranks)
    return {'recall@1': sum(1 for r in ranks if r == 0) / n,
            'recall@5': sum(1 for r in ranks if r < 5) / n,
            'MRR': sum(1.0 / (r + 1) for r in ranks) / n,
            'ranks': ranks}

out = {}
for v in ['V0', 'V1', 'V2', 'V3', 'V4', 'V5']:
    m = evaluate(v)
    out[v] = m
    print(f"{v}: recall@1={m['recall@1']:.3f} recall@5={m['recall@5']:.3f} MRR={m['MRR']:.3f}")

# per-query deltas vs baseline for the best variant
base = out['V0']['ranks']
best = min(['V1', 'V2', 'V3', 'V4', 'V5'],
           key=lambda v: (-out[v]['recall@5'], -out[v]['MRR']))
print(f"\nbest variant: {best}")
better, worse = [], []
for q, rb, rv in zip(res, base, out[best]['ranks']):
    if rv < rb:
        better.append((rb - rv, q['chunk'], q['held_cid'], rb, rv, q['held_label']))
    elif rv > rb:
        worse.append((rv - rb, q['chunk'], q['held_cid'], rb, rv, q['held_label']))
print(f"better: {len(better)}, worse: {len(worse)}")
print("top wins:")
for d, ch, cid, rb, rv, lab in sorted(better, reverse=True)[:6]:
    print(f"  {ch}/{cid}: {rb}->{rv}  {lab[:60]}")
print("top losses:")
for d, ch, cid, rb, rv, lab in sorted(worse, reverse=True)[:6]:
    print(f"  {ch}/{cid}: {rb}->{rv}  {lab[:60]}")
json.dump({v: {k: m[k] for k in ('recall@1', 'recall@5', 'MRR')} for v, m in out.items()},
          open('corpus_runs/exp2_badge_eval.json', 'w'), indent=1)
