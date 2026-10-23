"""Atlas merge: 30 chunk extractions -> one unified lemma graph.

Implements corpus_runs/atlas/MERGE_PLAN.md.
Reads corpus_runs/atlas/extractions/*.json
Writes corpus_runs/atlas/atlas_graph.json
"""
import json, glob, re, os
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
EXD = os.path.join(BASE, 'extractions')

PATTERNS = [
    (r'node\s+(\d+[a-z]?)', lambda m: 'node' + m.group(1).lower()),
    (r'\bD(\d{1,2})[a-z]?\b', lambda m: 'd' + m.group(1)),
    (r'(?<![\w/])(\d{1,2}[a-z])\b', lambda m: 'node' + m.group(1).lower()),
    (r'interference theorem\s*\(([abc])\)', lambda m: 'interference-' + m.group(1)),
    (r'interference theorem(?!\s*\([abc]\))', lambda m: 'interference'),
    (r'lemma\s+(\d)(?:\s*[-\u2013]\s*(\d))?', lambda m: 'node16-lemmas'),
    (r'triple artifact', lambda m: 'triple-artifact'),
    (r'witness\s+(\d)', lambda m: 'witness' + m.group(1)),
    (r'\bCCM\b', lambda m: 'ccm'),
    (r'\bPNT\b', lambda m: 'pnt'),
    (r'\bGUE\b', lambda m: 'gue'),
    (r'\bxp branch\b', lambda m: 'xp-branch'),
    (r'\bDeninger\b', lambda m: 'deninger'),
    (r'\bFigueiredo\b', lambda m: 'figueiredo'),
    (r'\bLanglands\b', lambda m: 'langlands'),
    (r'\bBerry\b', lambda m: 'berry'),
    (r'\bzeta\b', lambda m: 'zeta'),
    (r'triadic fork', lambda m: 'triadic-fork'),
    (r'backward touch', lambda m: 'backward-touch'),
    (r'epistemic label', lambda m: 'epistemic-labels'),
    (r'dead[-\s]end ledger', lambda m: 'dead-end-ledger'),
    (r'decision tree', lambda m: 'decision-tree'),
    (r'circle sieve', lambda m: 'circle-sieve'),
    (r'self[-\s]deriving', lambda m: 'self-deriving'),
    (r'\bsieve\b', lambda m: 'sieve'),
]

def subjects_of(label, chunk=None):
    out = []
    for pat, fn in PATTERNS:
        for m in re.finditer(pat, label, re.I):
            s = fn(m)
            # namespace guard: archive_dead_ends.md has its own D1-D13
            # dead-end numbering, distinct from the decision-tree D-items
            # (D5 Figueiredo steer vs ledger D5 parallel wave). Keep apart.
            if chunk == 'archive_dead_ends' and re.fullmatch(r'd\d+', s):
                s = 'ledger-' + s
            if s not in out:
                out.append(s)
    return out

STATUS_RANK = {'exact': 4, 'computationally_verified': 3,
               'conjectural': 2, 'heuristic': 1}

def main():
    docs = {}
    for f in sorted(glob.glob(os.path.join(EXD, '*.json'))):
        cid = os.path.basename(f)[:-5]
        docs[cid] = json.load(open(f))

    subjects = {}   # sid -> dict
    standalone = {} # node id -> dict
    subj_edges = Counter()   # (a,b,rel) -> count
    edge_prov = defaultdict(set)
    internal_edges = 0
    flagged = []

    def subj_node(sid):
        if sid not in subjects:
            subjects[sid] = {'id': sid, 'facets': [], 'label_variants': Counter(),
                             'chunks': set(), 'killed_facets': 0}
        return subjects[sid]

    # pass 1: assign concepts
    for cid, doc in docs.items():
        anchors = {a['concept_id']: a for a in doc['anchors']}
        for c in doc['concepts']:
            ss = subjects_of(c['label'], cid)
            a = anchors.get(c['id'], {})
            facet = {'chunk': cid, 'cid': c['id'], 'label': c['label'],
                     'kind': c['kind'], 'status': a.get('status'),
                     'genre': a.get('genre'), 'note': a.get('note'),
                     'subjects': ss}
            if not ss:
                nid = f"{cid}::{c['id']}"
                standalone[nid] = {'id': nid, 'facet': facet}
            else:
                for s in ss:
                    n = subj_node(s)
                    n['facets'].append(facet)
                    n['label_variants'][c['label']] += 1
                    n['chunks'].add(cid)
                    if a.get('status') == 'killed':
                        n['killed_facets'] += 1

    def node_of(cid, concept_id, doc_anchors_unused=None):
        # resolve a chunk concept ref to a graph node id
        for sid, n in subjects.items():
            for f in n['facets']:
                if f['chunk'] == cid and f['cid'] == concept_id:
                    return ('subject', sid)
        nid = f"{cid}::{concept_id}"
        if nid in standalone:
            return ('standalone', nid)
        return (None, None)

    # pass 2: edges
    for cid, doc in docs.items():
        for e in doc['edges']:
            na = node_of(cid, e['a'])
            nb = node_of(cid, e['b'])
            if na[0] is None or nb[0] is None:
                flagged.append({'type': 'dangling_edge', 'chunk': cid,
                                'edge': e})
                continue
            ka, kb = na[1], nb[1]
            if ka == kb:
                internal_edges += 1
                continue
            key = (ka, kb, e['rel'])
            subj_edges[key] += 1
            edge_prov[key].add(cid)

    # contradiction flags: same pair, supports vs contradicts
    pair_rels = defaultdict(set)
    for (a, b, rel) in subj_edges:
        pair_rels[(a, b)].add(rel)
    for (a, b), rels in pair_rels.items():
        if 'supports' in rels and 'contradicts' in rels:
            flagged.append({'type': 'contradictory_edges', 'a': a, 'b': b,
                            'rels': sorted(rels)})

    # pass 3: status reconciliation per subject
    for sid, n in subjects.items():
        live = [f for f in n['facets'] if f['status'] != 'killed']
        if not live:
            n['status'] = 'killed'
            n['status_note'] = 'all facets killed'
        else:
            best = max(live, key=lambda f: STATUS_RANK.get(f['status'], 0))
            n['status'] = best['status']
            weaker = {f['status'] for f in live} - {best['status']}
            if weaker:
                n['status_note'] = (
                    f"strongest honestly earned: {best['status']} "
                    f"({best['chunk']}/{best['cid']}); also recorded as "
                    f"{', '.join(sorted(w for w in weaker if w))} elsewhere")
            else:
                n['status_note'] = None
        # canonical display label: most common variant, shortened
        n['display'] = n['label_variants'].most_common(1)[0][0]
        if len(n['display']) > 64:
            n['display'] = n['display'][:61] + '...'
        n['chunks'] = sorted(n['chunks'])
        # drop Counter for JSON
        n['label_variants'] = [{'label': l, 'n': c}
                               for l, c in n['label_variants'].most_common(5)]

    # standalone nodes
    sa_nodes = []
    for nid, s in standalone.items():
        f = s['facet']
        sa_nodes.append({'id': nid, 'display': f['label'][:64],
                         'status': f['status'], 'kind': f['kind'],
                         'genre': f['genre'], 'note': f['note'],
                         'chunk': f['chunk'], 'standalone': True})

    graph = {
        'subjects': subjects,
        'standalone': sa_nodes,
        'edges': [{'a': a, 'b': b, 'rel': r, 'count': c,
                   'chunks': sorted(edge_prov[(a, b, r)])}
                  for (a, b, r), c in sorted(subj_edges.items())],
        'internal_edges_dropped': internal_edges,
        'flagged': flagged,
        'loops': [],
        'stats': {
            'chunks': len(docs),
            'concepts': sum(len(d['concepts']) for d in docs.values()),
            'subjects': len(subjects),
            'standalone_nodes': len(sa_nodes),
            'cross_edges': len(subj_edges),
        },
    }
    # loops: open questions program-wide
    for cid, doc in sorted(docs.items()):
        lab = {c['id']: c['label'] for c in doc['concepts']}
        for l in doc.get('loops', []):
            ref = l.get('concept_id') if isinstance(l, dict) else l
            graph['loops'].append({'chunk': cid, 'ref': ref,
                                   'label': lab.get(ref, ref)})

    out = os.path.join(BASE, 'atlas_graph.json')
    json.dump(graph, open(out, 'w'), indent=1)
    print('subjects:', len(subjects), '| standalone:', len(sa_nodes),
          '| cross edges:', len(subj_edges), '| flagged:', len(flagged),
          '| loops:', len(graph['loops']))
    # status distribution of subjects
    print(Counter(n['status'] for n in subjects.values()))
    return graph

if __name__ == '__main__':
    main()
