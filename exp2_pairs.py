"""exp2_pairs.py -- mine cross-chunk concept pairs for the entity-resolution test set."""
import json, math, re
from collections import Counter, defaultdict

STOP = set("""a an the and or of to in on for with as at by is are was were be been
being it its this that these those from into over after such than then so no not
only own same which who whom whose what when where why how all any both each few
more most other some there their they them he she we you your his her our us vs via
per within without between through during under above below s t d ll m re ve don
does did doing can could shall should will would may might must""".split())

def toks(s):
    return [t for t in re.findall(r'[a-z0-9]+', s.lower()) if t not in STOP and len(t) > 1]

concepts = []  # (chunk, cid, label, kind, note)
for i in range(1, 13):
    ch = f'c{i:02d}'
    d = json.load(open(f'corpus_runs/r3/{ch}/extraction.json'))
    notes = {a['concept_id']: (a.get('note') or '') for a in d['anchors']}
    for c in d['concepts']:
        concepts.append((ch, c['id'], c['label'], c.get('kind', ''),
                         notes.get(c['id'], '')))

docs = [toks(label + ' ' + note) for _, _, label, _, note in concepts]
df = Counter()
for doc in docs:
    for t in set(doc):
        df[t] += 1
N = len(docs)
idf = {t: math.log(N / (1 + c)) for t, c in df.items()}

def vec(doc):
    tf = Counter(doc)
    v = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items() if t in idf}
    n = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {t: x / n for t, x in v.items()}

vecs = [vec(d) for d in docs]
def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(t, 0.0) for t, v in a.items())

pairs = []
for i in range(N):
    for j in range(i + 1, N):
        if concepts[i][0] == concepts[j][0]:
            continue
        s = cos(vecs[i], vecs[j])
        pairs.append((s, i, j))
pairs.sort(reverse=True)

print(f'{N} concepts, {len(pairs)} cross-chunk pairs')
print('similarity distribution (top 20 / at ranks):')
for r in [0, 9, 49, 99, 199, 399, 799]:
    print(f'  rank {r}: {pairs[r][0]:.3f}')
json.dump([{'sim': s,
            'a': {'chunk': concepts[i][0], 'cid': concepts[i][1],
                  'label': concepts[i][2], 'note': concepts[i][4]},
            'b': {'chunk': concepts[j][0], 'cid': concepts[j][1],
                  'label': concepts[j][2], 'note': concepts[j][4]}}
           for s, i, j in pairs[:600]],
          open('corpus_runs/exp2_candidate_pairs.json', 'w'), indent=1)
print('wrote corpus_runs/exp2_candidate_pairs.json (top 600)')
