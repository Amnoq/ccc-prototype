"""exp2_merge_hook.py -- B2: extraction-against-registry merge hook test.

For each c12 concept: retrieve top-5 registry entities by TF-IDF, then
LLM-adjudicate each candidate pair. Merge decisions are scored against
the audited ground-truth labels (batch_C).
"""
import json, math, re
from collections import Counter

STOP = set("""a an the and or of to in on for with as at by is are was were be been
being it its this that these those from into over after such than then so no not
only own same which who whom whose what when where why how all any both each few
more most other some there their they them he she we you your his her our us vs via
per within without between through during under above below s t d ll m re ve don
does did doing can could shall should will would may might must""".split())

def toks(s):
    return [t for t in re.findall(r'[a-z0-9]+', s.lower()) if t not in STOP and len(t) > 1]

registry = json.load(open('corpus_runs/exp2_registry.json'))
concepts = []
for i in range(1, 13):
    ch = f'c{i:02d}'
    d = json.load(open(f'corpus_runs/r3/{ch}/extraction.json'))
    notes = {a['concept_id']: (a.get('note') or '') for a in d['anchors']}
    for c in d['concepts']:
        concepts.append({'chunk': ch, 'cid': c['id'], 'label': c['label'], 'note': notes.get(c['id'], '')})
c12con = [c for c in concepts if c['chunk'] == 'c12']

edocs = [toks(e['label'] + ' ' + ' '.join(e['notes']) + ' ' + ' '.join(e['aliases'])) for e in registry]
qdocs = [toks(c['label'] + ' ' + c['note']) for c in c12con]
df = Counter()
for doc in edocs + qdocs:
    for t in set(doc):
        df[t] += 1
N = len(edocs) + len(qdocs)
idf = {t: math.log(N / (1 + c)) for t, c in df.items()}

def vec(doc):
    tf = Counter(doc)
    v = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items() if t in idf}
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {t: x / n for t, x in v.items()}

rvecs = [vec(d) for d in edocs]
def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(t, 0.0) for t, v in a.items())

K = 5
adjudicate = []  # pairs for the LLM adjudicator
retrieval_rank_of_truth = {}  # c12 cid -> rank of its true entity (if in top-K)
for qi, c in enumerate(c12con):
    qv = vec(qdocs[qi])
    ranked = sorted(range(len(registry)), key=lambda ei: -cos(qv, rvecs[ei]))
    for rank, ei in enumerate(ranked[:K]):
        e = registry[ei]
        adjudicate.append({
            'hook_id': f'Q{qi:02d}R{rank}',
            'c12_cid': c['cid'],
            'c12_label': c['label'],
            'c12_note': c['note'],
            'cand_rank': rank,
            'entity_id': e['entity_id'],
            'entity_canonical': e['canonical'],
            'entity_label': e['label'],
            'entity_aliases': e['aliases'][:6],
            'entity_notes': e['notes'][:3],
        })
json.dump(adjudicate, open('corpus_runs/exp2_hook_candidates.json', 'w'), indent=1)
print(f'{len(c12con)} c12 concepts x top-{K} = {len(adjudicate)} candidate pairs for adjudication')
print('wrote corpus_runs/exp2_hook_candidates.json')
