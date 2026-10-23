#!/usr/bin/env python3
"""Atlas-7 merge: BSD skies.

Skies: analytic (an1), algebraic (al1), computational (c1, c2).
Pass 1 (within-sky): light; exact-dup scan found ZERO duplicate labels,
so merges apply only via the explicit REVIEWED alias map below (empty
unless review of pass1_review.json finds genuine restatements).
Pass 2 (cross-sky): mechanical token-overlap candidates for reviewed
adjudication (analytic<->algebraic, analytic<->computational,
algebraic<->computational). Adjudications live in atlas7_adjudications.json,
verdicts: resolved / split (role-differences named) / missed / rejected.

RULES (Atlas-2..6): explicit alias map only, no silent fuzzy matching,
over-merge worse than under-merge, contradictions surfaced never adjudicated.
"""
import json, glob, re, os, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
EXD = os.path.join(BASE, 'extractions')
GRAPHD = os.path.join(BASE, 'graphs')
os.makedirs(GRAPHD, exist_ok=True)

SKY = {'an1': 'analytic', 'al1': 'algebraic', 'c1': 'computational',
       'c2': 'computational'}

STOP = set('''the a an of and or to in on for with as by is are was were be
been from that this it its at which who whom whose what when where how
all any both each few more most other some such no nor not only own same
so than too very can will just don should now into over after before
between through during above below up down out off again further then
once here there when where why how s t d ll m o y e.g i.e vs via per
curve curves point points group groups rank ranks field fields number
numbers set sets one two three form forms case cases
'''.split())

# domain-generic tokens that must not seed a candidate by themselves
GENERIC = {'formula', 'formulas', 'function', 'functions', 'theorem',
           'theory', 'theories', 'explicit', 'paper', 'result', 'results',
           'using', 'used', 'method', 'methods', 'conjecture', 'lemma',
           'proposition', 'corollary', 'proof', 'section', 'example',
           'application', 'applications', 'construction', 'definition',
           'remark', 'hypothesis', 'claim', 'strategy', 'algorithm',
           'computation', 'computations', 'computationa', 'elliptic',
           'rational', 'points', 'special', 'case', 'general'}

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

# Pass-1 explicit alias map: [keep_nid_prefix, drop_nid_prefix, reason]
# Populated ONLY from reviewed pass1_review.json items. Prefixes matched
# uniquely at apply time (assertion fails if ambiguous).
ALIASES = []

def load():
    nodes, edges = {}, []
    taken = set()
    anch_global = {}
    for path in sorted(glob.glob(os.path.join(EXD, '*_p*.json'))):
        fname = os.path.basename(path)[:-5]
        pfx = fname.split('_')[0]
        sky = SKY[pfx]
        d = json.load(open(path))
        anch = {a['concept_id']: a for a in d['anchors']}
        idmap = {}
        for c in d['concepts']:
            nid = f'{sky}:{pfx}:{slug(c["label"], taken)}'
            a = anch.get(c['id'], {})
            nodes[nid] = {
                'id': nid, 'sky': sky, 'paper': pfx,
                'file': fname, 'cid': c['id'],
                'label': c['label'], 'kind': c['kind'],
                'status': a.get('status', 'heuristic'),
                'genre': a.get('genre'), 'note': a.get('note', ''),
            }
            idmap[c['id']] = nid
            anch_global[nid] = a
        for e in d.get('edges', []):
            if e['a'] in idmap and e['b'] in idmap:
                edges.append({'a': idmap[e['a']], 'b': idmap[e['b']],
                              'rel': e['rel'], 'sky': sky, 'paper': pfx})
    return nodes, edges

def main():
    nodes, edges = load()
    print(f'loaded {len(nodes)} nodes, {len(edges)} within-file edges')
    by = defaultdict(int)
    for n in nodes.values():
        by[(n['sky'], n['paper'])] += 1
    print('by (sky,paper):', dict(by))
    json.dump({'nodes': nodes, 'edges': edges},
              open(os.path.join(GRAPHD, 'atlas7_raw.json'), 'w'),
              ensure_ascii=False, indent=1)

    toks = {nid: tokens(n['label'], n['note']) for nid, n in nodes.items()}
    ids = list(nodes)

    def shared_ab(a, b):
        s = (toks[a] & toks[b]) - GENERIC
        return sorted(s)

    # Pass 1 review: same sky, high overlap (>=4 shared non-generic tokens)
    p1 = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if nodes[a]['sky'] != nodes[b]['sky']:
                continue
            if nodes[a]['paper'] == nodes[b]['paper'] and \
               nodes[a]['file'] == nodes[b]['file']:
                continue
            sh = shared_ab(a, b)
            if len(sh) >= 4:
                p1.append({'a': a, 'b': b, 'shared': sh,
                           'la': nodes[a]['label'], 'lb': nodes[b]['label'],
                           'pa': nodes[a]['paper'], 'pb': nodes[b]['paper']})
    p1.sort(key=lambda c: -len(c['shared']))
    json.dump(p1, open(os.path.join(BASE, 'pass1_review.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'{len(p1)} within-sky high-overlap pairs -> pass1_review.json')

    # Pass 2: cross-sky candidates (>=2 shared non-generic tokens), per pair
    pairs = {}
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            sa, sb = nodes[a]['sky'], nodes[b]['sky']
            if sa == sb:
                continue
            key = '-'.join(sorted([sa, sb]))
            sh = shared_ab(a, b)
            if len(sh) >= 2:
                pairs.setdefault(key, []).append(
                    {'a': a, 'b': b, 'shared': sh,
                     'la': nodes[a]['label'], 'lb': nodes[b]['label'],
                     'pa': nodes[a]['paper'], 'pb': nodes[b]['paper'],
                     'sa': sa, 'sb': sb,
                     'na': nodes[a]['note'][:160], 'nb': nodes[b]['note'][:160]})
    for key in pairs:
        pairs[key].sort(key=lambda c: -len(c['shared']))
        json.dump(pairs[key],
                  open(os.path.join(BASE, f'candidates_{key}.json'), 'w'),
                  ensure_ascii=False, indent=1)
        print(f'{key}: {len(pairs[key])} candidates')
    tot = sum(len(v) for v in pairs.values())
    print(f'{tot} total cross-sky candidates')
    print('ALIAS map entries (reviewed):', len(ALIASES))

if __name__ == '__main__':
    main()
