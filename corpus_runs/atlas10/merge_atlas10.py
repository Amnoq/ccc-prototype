#!/usr/bin/env python3
"""Atlas-10 merge: theory vs annotations vs engine skies.
Rules (Atlas-2..9): explicit alias map from REVIEWED candidates only,
no silent fuzzy matching, over-merge worse than under-merge,
contradictions surfaced never adjudicated away."""
import json, os, re, glob, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
EXD = os.path.join(BASE, 'extractions')
GRAPHD = os.path.join(BASE, 'graphs')
os.makedirs(GRAPHD, exist_ok=True)

VALID_STATUS = {'exact', 'computationally_verified', 'conjectural',
                'heuristic', 'killed'}
STOP = {'the', 'and', 'for', 'with', 'that', 'this', 'from', 'are',
        'was', 'were', 'has', 'have', 'had', 'not', 'but', 'its',
        'their', 'they', 'them', 'which', 'when', 'where', 'than',
        'then', 'into', 'over', 'under', 'between', 'among', 'such',
        'more', 'most', 'also', 'after', 'before', 'using', 'given',
        'known', 'follows', 'following', 'shows', 'show', 'proved',
        'prove', 'proves', 'let', 'assume', 'suppose', 'consider',
        'define', 'defined', 'each', 'both', 'either', 'while',
        'during', 'within', 'without', 'about', 'against', 'across',
        'being', 'been', 'with', 'will', 'would', 'could', 'should',
        'does', 'did', 'done', 'make', 'made', 'take', 'takes'}
# ultra-structural chess words: too common to link on
GENERIC = {'king', 'queen', 'rook', 'bishop', 'knight', 'knights',
           'pawn', 'pawns', 'move', 'moves', 'moved', 'moving', 'game',
           'games', 'white', 'black', 'square', 'squares', 'position',
           'positions', 'play', 'played', 'playing', 'piece', 'pieces',
           'board', 'check', 'side', 'men'}

def normalize(t):
    t = unicodedata.normalize('NFKD', t or '')
    t = ''.join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()

def tokens(label, note=''):
    return {w for w in normalize(label + ' ' + note).split()
            if w not in STOP and w not in GENERIC and len(w) > 2}

def slug(label, taken):
    base = re.sub(r'[^a-z0-9]+', '-', normalize(label)).strip('-')[:52] or 'node'
    s, i = base, 2
    while s in taken:
        s = f'{base}-{i}'; i += 1
    taken.add(s)
    return s

def sky_of(fname):
    if fname.startswith('theory_'):
        return 'theory'
    if fname.startswith('annot_'):
        return 'annotations'
    if fname.startswith('engine_'):
        return 'engine'
    raise ValueError(fname)

def norm_edge(e):
    a = e.get('a', e.get('from'))
    b = e.get('b', e.get('to'))
    r = e.get('rel', e.get('relation'))
    return a, b, r

def load():
    nodes, edges = {}, []
    taken = set()
    idmap = {}
    for path in sorted(glob.glob(os.path.join(EXD, '*.json'))):
        if path.endswith('_raw.json'):
            continue  # repair backups are not extraction files
        fname = os.path.basename(path)[:-5]
        sky = sky_of(fname)
        d = json.load(open(path))
        anch = {a['concept_id']: a for a in d['anchors']}
        for c in d['concepts']:
            # STABLE node ids: sky:file:concept-id:slug (cid never
            # changes, so ids survive re-runs and new files)
            nid = f"{sky}:{fname}:{c['id']}:{slug(c['label'], taken)}"
            idmap[(fname, c['id'])] = nid
            a = anch.get(c['id'], {})
            status = a.get('status', 'heuristic')
            if status not in VALID_STATUS:
                status = 'heuristic'
            nodes[nid] = {
                'id': nid, 'sky': sky, 'file': fname, 'cid': c['id'],
                'label': c['label'], 'kind': c.get('kind', 'claim'),
                'status': status, 'note': a.get('note', ''),
                'genre': a.get('genre', ''),
                'tokens': sorted(tokens(c['label'], a.get('note', ''))),
            }
        for e in d.get('edges', []):
            a, b, r = norm_edge(e)
            na, nb = idmap.get((fname, a)), idmap.get((fname, b))
            if na and nb:
                edges.append({'a': na, 'b': nb, 'rel': r,
                              'note': e.get('note', '')})
    return nodes, edges

def main():
    nodes, edges = load()
    print(f'{len(nodes)} nodes, {len(edges)} within-file edges')
    json.dump({'nodes': nodes, 'edges': edges},
              open(os.path.join(GRAPHD, 'atlas10_loaded.json'), 'w'))

    # Pass 1: within-sky merge candidates (same sky, different file)
    cands = []
    nids = list(nodes)
    for i in range(len(nids)):
        for j in range(i + 1, len(nids)):
            a, b = nodes[nids[i]], nodes[nids[j]]
            if a['sky'] != b['sky'] or a['file'] == b['file']:
                continue
            sh = set(a['tokens']) & set(b['tokens'])
            if len(sh) >= 4:
                cands.append({'a': a['id'], 'b': b['id'],
                              'shared': sorted(sh),
                              'a_label': a['label'][:100],
                              'b_label': b['label'][:100]})
    json.dump(cands, open(os.path.join(BASE, 'merge_candidates.json'), 'w'),
              indent=1)
    print(f'{len(cands)} within-sky merge candidates -> '
          f'merge_candidates.json (REVIEW before applying)')

    # Cross-sky candidates for adjudication
    xc = []
    for i in range(len(nids)):
        for j in range(i + 1, len(nids)):
            a, b = nodes[nids[i]], nodes[nids[j]]
            if a['sky'] == b['sky']:
                continue
            sh = set(a['tokens']) & set(b['tokens'])
            if len(sh) >= 3:
                xc.append({'a': a['id'], 'b': b['id'],
                           'pair': f"{a['sky']}-{b['sky']}",
                           'shared': sorted(sh),
                           'a_label': a['label'][:110],
                           'a_note': a['note'][:160],
                           'b_label': b['label'][:110],
                           'b_note': b['note'][:160]})
    json.dump(xc, open(os.path.join(BASE, 'cross_candidates.json'), 'w'),
              indent=1)
    print(f'{len(xc)} cross-sky candidates -> cross_candidates.json')

if __name__ == '__main__':
    main()
