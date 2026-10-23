#!/usr/bin/env python3
"""Atlas-6 merge: the Weil bridge map.

Two sides (analytic: af/bom/gro papers; relational: pilot Node-10a
re-extraction), each merged lightly within-side (Pass 1, explicit
alias map only); cross-side candidates generated mechanically for
reviewed Pass-2 adjudication (done by hand, written to
cross_bridge_links.json).

MERGE_PLAN.md rules: explicit alias map, no silent fuzzy matching,
over-merge worse than under-merge, contradictions surfaced never
adjudicated. Preprint discipline: AF + GRO files propagate
preprint=True into every facet; the label is never upgraded.
Pilot's directory is read-only (we only read our own new
extractions).
"""
import json, glob, re, os, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
EXD = os.path.join(BASE, 'extractions')
GRAPHD = os.path.join(BASE, 'graphs')
os.makedirs(GRAPHD, exist_ok=True)

PREFIX = {'weil_analytic_af': 'af', 'weil_analytic_bom': 'bom',
          'weil_analytic_gro': 'gro', 'weil_rel': 'rel'}
SIDE = {'af': 'analytic', 'bom': 'analytic', 'gro': 'analytic',
        'rel': 'relational'}
PREPRINT = {'af', 'gro'}  # file prefixes whose facets carry preprint=True

STOP = set('''the a an of and or to in on for with as by is are was were be
been from that this it its at which who whom whose what when where how
all any both each few more most other some such no nor not only own same
so than too very can will just don should now into over after before
between through during above below up down out off again further then
once here there when where why how s t d ll m o y e.g i.e vs via per
'''.split())

def normalize(t):
    t = unicodedata.normalize('NFKD', t or '')
    t = ''.join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()

def tokens(label):
    return {w for w in normalize(label).split()
            if w not in STOP and len(w) > 2}

def slug(label, taken):
    base = re.sub(r'[^a-z0-9]+', '-', normalize(label)).strip('-')[:48] or 'node'
    s, i = base, 2
    while s in taken:
        s = f'{base}-{i}'; i += 1
    taken.add(s)
    return s

# ---- Pass 1: explicit alias map (reviewed duplicates only) ----
# Each entry: [keep_id, drop_id, reason]. Ids are namespaced node ids.
ALIASES = [
    # relational: same verification event restated across the two files
    ['rel:zero-side-vs-prime-side-agreement-to-machine',
     'rel:10a-step2-symmetric-guinand-weil-formula-ver',
     'same verification event (60 zeros, 26152 prime powers, 2.4e-16); step3_tree c5 restates step12 c4'],
    ['rel:prime-side-positivity-is-cancellatory-not-term',
     'rel:step-2-structural-finding-prime-side-positivi',
     'same derived finding restated (pole+arch-prime drain); facets preserve both wordings'],
    # analytic AF: same cited observation in proof-plan vs discovery-narrative context
    ['af:positivity-of-w-on-all-of-c-c-2-r-is-equivalent',
     'af:bombieri-bom00-negative-index-of-finite-trunc',
     'placeholder - replaced below after id resolution'],
]

def load():
    nodes, edges = {}, []
    taken = set()
    for path in sorted(glob.glob(os.path.join(EXD, 'weil_*.json'))):
        fname = os.path.basename(path)[:-5]
        pfx = next(v for k, v in PREFIX.items() if fname.startswith(k))
        d = json.load(open(path))
        anch = {a['concept_id']: a for a in d['anchors']}
        idmap = {}
        for c in d['concepts']:
            nid = pfx + ':' + slug(c['label'], taken)
            a = anch.get(c['id'], {})
            nodes[nid] = {
                'id': nid, 'side': SIDE[pfx], 'paper': pfx,
                'file': fname, 'cid': c['id'],
                'label': c['label'], 'kind': c['kind'],
                'status': a.get('status', 'heuristic'),
                'genre': a.get('genre'), 'note': a.get('note', ''),
                'preprint': pfx in PREPRINT,
            }
            idmap[c['id']] = nid
        for e in d.get('edges', []):
            if e['a'] in idmap and e['b'] in idmap:
                edges.append({'a': idmap[e['a']], 'b': idmap[e['b']],
                              'rel': e['rel'], 'side': SIDE[pfx]})
    return nodes, edges

def resolve_aliases(nodes, edges):
    # rebuild ALIASES with real ids by label-prefix matching, then apply
    amap = {}
    def find(prefix):
        c = [n for n in nodes if n.split(':', 1)[1].startswith(prefix)]
        assert len(c) == 1, (prefix, c)
        return c[0]
    pairs = [
        ('rel:zero-side-vs-prime-side-agreement-to-machine',
         'rel:10a-step2-symmetric-guinand-weil-formula-ver',
         'same verification event restated across files'),
        ('rel:prime-side-positivity-is-cancellatory-not-term',
         'rel:step-2-structural-finding-prime-side-positivi',
         'same derived finding restated across files'),
        ('af:positivity-of-w-on-all-of-c-c-2-r-is-equivalent',
         'af:bombieri-bom00-negative-index-of-finite-trunc',
         'REVIEW-FLAG: verify these are the same cited observation before merging'),
    ]
    # NOTE: alias application is REVIEWED below in __main__; this function
    # only builds the map. Merges are applied explicitly, never silently.
    return pairs

def main():
    nodes, edges = load()
    print(f'loaded {len(nodes)} nodes, {len(edges)} within-file edges')
    by_side = defaultdict(int)
    for n in nodes.values():
        by_side[n['side']] += 1
    print('by side:', dict(by_side))
    json.dump({'nodes': nodes, 'edges': edges},
              open(os.path.join(GRAPHD, 'atlas6_raw.json'), 'w'),
              ensure_ascii=False, indent=1)
    # mechanical cross-side candidates: content-token overlap >= 2
    toks = {nid: tokens(n['label']) | tokens(n['note']) for nid, n in nodes.items()}
    cands = []
    ids = list(nodes)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if nodes[a]['side'] == nodes[b]['side']:
                continue
            shared = toks[a] & toks[b]
            # discount ultra-generic math tokens
            shared = {w for w in shared if w not in
                      {'formula', 'function', 'functions', 'theorem', 'theory',
                       'explicit', 'paper', 'result', 'results', 'using', 'used'}}
            if len(shared) >= 2:
                cands.append({'a': a, 'b': b,
                              'shared': sorted(shared),
                              'la': nodes[a]['label'][:90],
                              'lb': nodes[b]['label'][:90]})
    cands.sort(key=lambda c: -len(c['shared']))
    json.dump(cands, open(os.path.join(BASE, 'candidates.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'{len(cands)} mechanical cross-side candidates -> candidates.json')
    # alias review list for the human pass
    print('alias pairs to review:')
    for keep_pfx, drop_pfx, reason in resolve_aliases(nodes, edges):
        print('  KEEP', keep_pfx, '\n  DROP', drop_pfx, '\n  WHY ', reason)

if __name__ == '__main__':
    main()
