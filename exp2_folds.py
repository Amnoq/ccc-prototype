"""exp2_folds.py -- build 12-fold CV datasets for rigorous close-out.

Per held-out chunk h: registry from other 11 chunks (union-find over audited
SAME pairs excluding h), rank h-concepts x registry entities by TF-IDF,
emit top-150 pairs as ground-truth labeling batches (fold_h.json).
Also emits hook candidate batches (top-5 per concept) for later adjudication.
"""
import json, math, re, os
from collections import Counter, defaultdict

STOP = set("""a an the and or of to in on for with as at by is are was were be been
being it its this that these those from into over after such than then so no not
only own same which who whom whose what when where why how all any both each few
more most other some there their they them he she we you your his her our us vs via
per within without between through during under above below s t d ll m re ve don
does did doing can could shall should will would may might must""".split())
def toks(s):
    return [t for t in re.findall(r'[a-z0-9]+', s.lower()) if t not in STOP and len(t) > 1]

concepts = []
for i in range(1, 13):
    ch = f'c{i:02d}'
    d = json.load(open(f'corpus_runs/r3/{ch}/extraction.json'))
    notes = {a['concept_id']: (a.get('note') or '') for a in d['anchors']}
    for c in d['concepts']:
        concepts.append({'chunk': ch, 'cid': c['id'], 'label': c['label'], 'note': notes.get(c['id'], '')})
cidx = {(c['chunk'], c['cid']): n for n, c in enumerate(concepts)}

labels = []
for b in 'HML':
    labels += json.load(open(f'corpus_runs/exp2_batches/labels_{b}.json'))
batches = {b: {p['pair_id']: p for p in json.load(open(f'corpus_runs/exp2_batches/batch_{b}.json'))} for b in 'HML'}
same_pairs = []
for l in labels:
    if l['verdict'] != 'SAME':
        continue
    p = batches[l['pair_id'][0]][l['pair_id']]
    same_pairs.append(((p['a']['chunk'], p['a']['cid']), (p['b']['chunk'], p['b']['cid'])))

os.makedirs('corpus_runs/exp2_folds', exist_ok=True)

def build_registry(exclude_chunk):
    parent = list(range(len(concepts)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for (ca, cb) in same_pairs:
        if exclude_chunk in (ca[0], cb[0]):
            continue
        union(cidx[ca], cidx[cb])
    clusters = defaultdict(list)
    for n, c in enumerate(concepts):
        if c['chunk'] == exclude_chunk:
            continue
        clusters[find(n)].append(n)
    registry = []
    for root, members in clusters.items():
        members.sort(key=lambda n: (concepts[n]['chunk'], concepts[n]['cid']))
        canon = concepts[members[0]]
        registry.append({
            'entity_id': f"F{exclude_chunk[1:]}E{len(registry):03d}",
            'canonical': f"{canon['chunk']}/{canon['cid']}",
            'label': canon['label'],
            'aliases': [f"{concepts[m]['chunk']}/{concepts[m]['cid']}: {concepts[m]['label']}" for m in members[1:]],
            'notes': [concepts[m]['note'] for m in members if concepts[m]['note']],
        })
    registry.sort(key=lambda e: e['canonical'])
    for k, e in enumerate(registry):
        e['entity_id'] = f"F{exclude_chunk[1:]}E{k:03d}"
    return registry

def tfidf_rank(held, registry, top_n):
    edocs = [toks(e['label'] + ' ' + ' '.join(e['notes']) + ' ' + ' '.join(e['aliases'])) for e in registry]
    hcon = [c for c in concepts if c['chunk'] == held]
    qdocs = [toks(c['label'] + ' ' + c['note']) for c in hcon]
    df = Counter()
    for doc in edocs + qdocs:
        for t in set(doc): df[t] += 1
    N = len(edocs) + len(qdocs)
    idf = {t: math.log(N / (1 + c)) for t, c in df.items()}
    def vec(doc):
        tf = Counter(doc)
        v = {t: (1 + math.log(cc)) * idf[t] for t, cc in tf.items() if t in idf}
        n = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / n for t, x in v.items()}
    rvecs = [vec(d) for d in edocs]
    def cos(a, b):
        if len(a) > len(b): a, b = b, a
        return sum(v * b.get(t, 0.0) for t, v in a.items())
    pairs = []
    for qi, c in enumerate(hcon):
        qv = vec(qdocs[qi])
        ranked = sorted(range(len(registry)), key=lambda ei: -cos(qv, rvecs[ei]))
        for rank, ei in enumerate(ranked):
            pairs.append((cos(qv, rvecs[ei]), qi, ei, rank))
    pairs.sort(reverse=True)
    return hcon, pairs

for i in range(1, 13):
    held = f'c{i:02d}'
    registry = build_registry(held)
    hcon, pairs = tfidf_rank(held, registry, 150)
    truth = []
    for rank, (s, qi, ei, _r) in enumerate(pairs[:150]):
        c = hcon[qi]; e = registry[ei]
        truth.append({'pair_id': f'V{i:02d}_{rank:03d}', 'sim': round(s, 3),
                      'held_cid': c['cid'], 'held_label': c['label'], 'held_note': c['note'],
                      'entity_id': e['entity_id'], 'entity_canonical': e['canonical'],
                      'entity_label': e['label'], 'entity_aliases': e['aliases'][:4],
                      'entity_notes': e['notes'][:2]})
    json.dump(truth, open(f'corpus_runs/exp2_folds/fold_{held}_truth.json', 'w'), indent=1)
    hook = []
    seen = set()
    for (s, qi, ei, rank) in pairs:
        if rank >= 5 or (qi, ei) in seen:
            continue
        seen.add((qi, ei))
        c = hcon[qi]; e = registry[ei]
        hook.append({'hook_id': f'W{i:02d}_{qi:02d}R{rank}', 'held_cid': c['cid'],
                     'held_label': c['label'], 'held_note': c['note'],
                     'entity_id': e['entity_id'], 'entity_canonical': e['canonical'],
                     'entity_label': e['label'], 'entity_aliases': e['aliases'][:6],
                     'entity_notes': e['notes'][:3]})
    json.dump(hook, open(f'corpus_runs/exp2_folds/fold_{held}_hook.json', 'w'), indent=1)
    json.dump(registry, open(f'corpus_runs/exp2_folds/fold_{held}_registry.json', 'w'), indent=1)
    print(f'{held}: registry {len(registry)} entities, truth {len(truth)}, hook candidates {len(hook)}')
print('done')
