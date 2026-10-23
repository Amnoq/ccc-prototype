"""exp2_rebuild.py -- rebuild registries under principle P (strict), corrected truth.

Principle P (decided 2026-10-03): a posit and its resolution are distinct
entities (question!=verdict, hypothesis!=killing-theorem, proposal!=closure).
Corrections to judge-1 SAMEs:
  REMOVE (false merges): H037 H047 H053 H107 H038 H111 M002 H054
  ADD (missed merges):   H060 M008
B2 validated hook merges (kept): c12/c7->E122 (Deninger), c12/c3->E058 (Weil)
Outputs:
  corpus_runs/exp2_registry_v2.json      (main registry, all 12 chunks)
  corpus_runs/exp2_folds/fold_cXX_registry_v2.json
  corpus_runs/exp2_folds/fold_cXX_hook_v2.json   (regenerated top-5 candidates)
  corpus_runs/exp2_folds/hook_v2_diff.json       (candidates needing fresh audit)
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

# ---- corrected SAME pairs ----
REMOVE = {'H037','H047','H053','H107','H038','H111','M002','H054'}
ADD = {'H060','M008'}
labels = []
for b in 'HML':
    labels += json.load(open(f'corpus_runs/exp2_batches/labels_{b}.json'))
batches = {b: {p['pair_id']: p for p in json.load(open(f'corpus_runs/exp2_batches/batch_{b}.json'))} for b in 'HML'}
same_pairs = []
for l in labels:
    pid = l['pair_id']
    want = (l['verdict'] == 'SAME' and pid not in REMOVE) or (pid in ADD)
    if not want:
        continue
    p = batches[pid[0]][pid]
    same_pairs.append(((p['a']['chunk'], p['a']['cid']), (p['b']['chunk'], p['b']['cid'])))
print(f'corrected SAME pairs: {len(same_pairs)} (j1 79 - 8 removed + 2 added = 73)')

# B2 validated merges, as concept pairs (resolved via registry v1 canonicals)
# c12/c7 -> E122 (Deninger program), c12/c3 -> E058 (Weil criterion)
regv1 = {e['entity_id']: e for e in json.load(open('corpus_runs/exp2_registry.json'))}
b2 = []
for target_eid, held in [('E122', ('c12','c7')), ('E058', ('c12','c3'))]:
    canon = regv1[target_eid]['canonical']
    ch, cid = canon.split('/')
    b2.append((held, (ch, cid)))
print('B2 merges:', b2)

def build_registry(exclude_chunk, extra_pairs, id_prefix):
    parent = list(range(len(concepts)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for (ca, cb) in same_pairs + extra_pairs:
        if exclude_chunk and exclude_chunk in (ca[0], cb[0]):
            continue
        union(cidx[ca], cidx[cb])
    clusters = defaultdict(list)
    for n, c in enumerate(concepts):
        if exclude_chunk and c['chunk'] == exclude_chunk:
            continue
        clusters[find(n)].append(n)
    registry = []
    members_of = {}
    for root, members in clusters.items():
        members.sort(key=lambda n: (concepts[n]['chunk'], concepts[n]['cid']))
        canon = concepts[members[0]]
        ent = {
            'entity_id': f"{id_prefix}{len(registry):03d}",
            'canonical': f"{canon['chunk']}/{canon['cid']}",
            'label': canon['label'],
            'aliases': [f"{concepts[m]['chunk']}/{concepts[m]['cid']}: {concepts[m]['label']}" for m in members[1:]],
            'notes': [concepts[m]['note'] for m in members if concepts[m]['note']],
        }
        registry.append(ent)
        members_of[ent['entity_id']] = frozenset((concepts[m]['chunk'], concepts[m]['cid']) for m in members)
    registry.sort(key=lambda e: e['canonical'])
    # reassign ids after sort, rebuild member map
    new_members = {}
    for k, e in enumerate(registry):
        new_id = f"{id_prefix}{k:03d}"
        new_members[new_id] = members_of[e['entity_id']]
        e['entity_id'] = new_id
    return registry, new_members

# ---- main registry v2 (all 12 chunks) ----
main_reg, main_members = build_registry(None, b2, 'E')
json.dump(main_reg, open('corpus_runs/exp2_registry_v2.json', 'w'), indent=1)
multi = sum(1 for e in main_reg if e['aliases'])
print(f'main registry v2: {len(main_reg)} entities, {multi} with aliases')

# ---- fold registries v2 + hook candidates v2 ----
def tfidf_rank(held, registry):
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

diff_needed = []
for i in range(1, 13):
    held = f'c{i:02d}'
    # B2 pairs excluded when c12 held out (they involve c12)
    registry, members = build_registry(held, b2, f'F{i:02d}E')
    json.dump(registry, open(f'corpus_runs/exp2_folds/fold_{held}_registry_v2.json', 'w'), indent=1)
    hcon, pairs = tfidf_rank(held, registry)
    hook2 = []
    seen = set()
    for (s, qi, ei, rank) in pairs:
        if rank >= 5 or (qi, ei) in seen:
            continue
        seen.add((qi, ei))
        c = hcon[qi]; e = registry[ei]
        hook2.append({'hook_id': f'W{i:02d}_{qi:02d}R{rank}', 'held_cid': c['cid'],
                      'held_label': c['label'], 'held_note': c['note'],
                      'entity_id': e['entity_id'], 'entity_canonical': e['canonical'],
                      'entity_label': e['label'], 'entity_aliases': e['aliases'][:6],
                      'entity_notes': e['notes'][:3],
                      '_members': sorted(members[e['entity_id']])})
    json.dump(hook2, open(f'corpus_runs/exp2_folds/fold_{held}_hook_v2.json', 'w'), indent=1)
    # diff vs v1: reuse v1 adjudication iff identical (held_cid, entity member-set)
    v1 = json.load(open(f'corpus_runs/exp2_folds/fold_{held}_hook.json'))
    v1lab = {l['hook_id']: l['verdict'] for l in json.load(open(f'corpus_runs/exp2_folds/fold_{held}_hook_labels.json'))}
    v1reg = {e['entity_id']: e for e in json.load(open(f'corpus_runs/exp2_folds/fold_{held}_registry.json'))}
    def v1members(eid):
        e = v1reg[eid]
        ms = [(e['canonical'].split('/')[0], e['canonical'].split('/')[1])]
        for a in e['aliases']:
            p = a.split(':')[0]; ms.append((p.split('/')[0], p.split('/')[1]))
        return frozenset(ms)
    v1keys = {}
    for c in v1:
        v1keys[(c['held_cid'], v1members(c['entity_id']))] = v1lab[c['hook_id']]
    n_reuse = 0
    for c in hook2:
        key = (c['held_cid'], frozenset(map(tuple, c['_members'])))
        if key in v1keys:
            n_reuse += 1
        else:
            diff_needed.append({'fold': held, 'hook_id': c['hook_id'],
                                'held_cid': c['held_cid'], 'held_label': c['held_label'],
                                'held_note': c['held_note'], 'entity_id': c['entity_id'],
                                'entity_canonical': c['entity_canonical'],
                                'entity_label': c['entity_label'],
                                'entity_aliases': c['entity_aliases'], 'entity_notes': c['entity_notes']})
    print(f'{held}: registry v2 {len(registry)} entities, hook v2 {len(hook2)} candidates, reuse {n_reuse}, fresh audit {len(hook2)-n_reuse}')

json.dump(diff_needed, open('corpus_runs/exp2_folds/hook_v2_diff.json', 'w'), indent=1)
print(f'\nTOTAL fresh audits needed: {len(diff_needed)}')
