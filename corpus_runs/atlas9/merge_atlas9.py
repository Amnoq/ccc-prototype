#!/usr/bin/env python3
"""Atlas-9 merge: tape vs fundamentals vs narrative skies.
Rules (Atlas-2..8): explicit alias map from REVIEWED candidates only,
no silent fuzzy matching, over-merge worse than under-merge,
contradictions surfaced never adjudicated."""
import json, os, re, glob, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
EXD = os.path.join(BASE, 'extractions')
GRAPHD = os.path.join(BASE, 'graphs')
os.makedirs(GRAPHD, exist_ok=True)

VALID_STATUS = {'exact', 'computationally_verified', 'conjectural', 'heuristic', 'killed'}
VALID_REL = {'supports', 'depends_on', 'contradicts', 'refines', 'generalizes', 'illustrates'}
STOP = {'the', 'and', 'for', 'with', 'that', 'this', 'from', 'are', 'was', 'were',
        'has', 'have', 'had', 'not', 'but', 'its', 'their', 'they', 'them',
        'which', 'when', 'where', 'than', 'then', 'into', 'over', 'under',
        'between', 'among', 'such', 'more', 'most', 'also', 'after', 'before',
        'using', 'given', 'known', 'follows', 'following', 'shows', 'show',
        'proved', 'prove', 'proves', 'let', 'assume', 'suppose', 'consider',
        'define', 'defined', 'each', 'both', 'either', 'while', 'during',
        'within', 'without', 'about', 'against', 'across', 'being', 'been'}
GENERIC = {'price', 'prices', 'stock', 'stocks', 'market', 'markets', 'return',
           'returns', 'firm', 'firms', 'news', 'effect', 'effects', 'result',
           'results', 'based', 'model', 'data', 'analysis', 'study', 'paper',
           'table', 'figure', 'section', 'evidence', 'sample', 'daily'}

def normalize(t):
    t = unicodedata.normalize('NFKD', t or '')
    t = ''.join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()

def tokens(label, note=''):
    return {w for w in normalize(label + ' ' + note).split()
            if w not in STOP and len(w) > 2}

def slug(label, taken):
    base = re.sub(r'[^a-z0-9]+', '-', normalize(label)).strip('-')[:52] or 'node'
    s, i = base, 2
    while s in taken:
        s = f'{base}-{i}'; i += 1
    taken.add(s)
    return s

def sky_of(fname):
    if fname.startswith('tape_'):
        return 'tape'
    if fname.startswith('fund_'):
        return 'fundamentals'
    if fname.startswith('narr_'):
        return 'narrative'
    raise ValueError(fname)

def paper_of(fname):
    # tape_indices | tape_names | fund_p<N> | narr_p<N>
    if fname.startswith('tape_'):
        return fname.split('_')[1]
    return fname  # fund_p1 / narr_p2 (single doc each)

def load():
    nodes, edges, loops = {}, [], []
    taken = set()
    for path in sorted(glob.glob(os.path.join(EXD, '*.json'))):
        fname = os.path.basename(path)[:-5]
        sky = sky_of(fname)
        paper = paper_of(fname)
        d = json.load(open(path))
        anch = {a['concept_id']: a for a in d['anchors']}
        idmap = {}
        for c in d['concepts']:
            nid = f'{sky}:{paper}:{slug(c["label"], taken)}'
            a = anch.get(c['id'], {})
            status = a.get('status', 'heuristic')
            if status not in VALID_STATUS:
                status = 'heuristic'
            nodes[nid] = {
                'id': nid, 'sky': sky, 'paper': paper,
                'file': fname, 'cid': c['id'],
                'label': c['label'], 'kind': c['kind'],
                'status': status, 'genre': a.get('genre'),
                'note': a.get('note', ''),
            }
            idmap[c['id']] = nid
        for e in d.get('edges', []):
            rel = e['rel'] if e['rel'] in VALID_REL else None
            if not rel or e['a'] not in idmap or e['b'] not in idmap:
                continue
            edges.append({'a': idmap[e['a']], 'b': idmap[e['b']],
                          'rel': rel, 'sky': sky, 'paper': paper})
        for l in d.get('loops', []):
            if isinstance(l, dict) and l.get('concept_id') in idmap:
                loops.append({'concept_id': idmap[l['concept_id']],
                              'sky': sky, 'paper': paper, 'file': fname})
            elif isinstance(l, str):
                loops.append({'concept_id': None, 'text': l,
                              'sky': sky, 'paper': paper, 'file': fname})
    return nodes, edges, loops

def main():
    nodes, edges, loops = load()
    print(f'loaded {len(nodes)} nodes, {len(edges)} within-file edges, {len(loops)} loops')
    by = defaultdict(int)
    for n in nodes.values():
        by[(n['sky'], n['paper'])] += 1
    print('by (sky,paper):', dict(by))

    toks = {nid: tokens(n['label'], n['note']) for nid, n in nodes.items()}
    ids = list(nodes)

    def shared(a, b):
        return sorted((toks[a] & toks[b]) - GENERIC)

    # Pass 1: within-sky merge candidates (same sky, different file, >=4 shared tokens)
    cands = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            na, nb = nodes[a], nodes[b]
            if na['sky'] != nb['sky'] or na['file'] == nb['file']:
                continue
            s = shared(a, b)
            if len(s) >= 4:
                cands.append({'a': a, 'b': b, 'shared': s,
                              'la': na['label'][:100], 'lb': nb['label'][:100]})
    json.dump(cands, open(os.path.join(BASE, 'merge_candidates.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'{len(cands)} within-sky merge candidates -> merge_candidates.json (REVIEW before applying)')

    # Cross-sky candidates: >=3 shared non-generic tokens, different skies
    xc = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            na, nb = nodes[a], nodes[b]
            if na['sky'] == nb['sky']:
                continue
            s = shared(a, b)
            if len(s) >= 3:
                xc.append({'a': a, 'b': b, 'pair': f"{na['sky']}-{nb['sky']}",
                           'shared': s, 'la': na['label'][:110], 'lb': nb['label'][:110]})
    json.dump(xc, open(os.path.join(BASE, 'cross_candidates.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'{len(xc)} cross-sky candidates -> cross_candidates.json')

    json.dump({'nodes': nodes, 'edges': edges, 'loops': loops},
              open(os.path.join(GRAPHD, 'atlas9_raw.json'), 'w'),
              ensure_ascii=False, indent=1)
    print('wrote graphs/atlas9_raw.json')

if __name__ == '__main__':
    main()
