#!/usr/bin/env python3
"""Atlas-8 merge: prime-distribution literature (foreign) vs circle-sieve sky (home).

Skies: home (home_sieve1..4 + home_sieve1..4_spans), foreign
(foreign_pnt/cramer/zhang/maynard/greentao/sieve).
Pass 1 (within-sky): light; high-overlap pairs go to pass1_review.json
for reviewed alias-map merges only.
Pass 2 (cross-sky): mechanical token-overlap candidates (home<->foreign)
for reviewed adjudication. Adjudications live in
atlas8_adjudications.json, verdicts: resolved / split (role-differences
named per Atlas-2 D3) / missed / rejected.

RULES (Atlas-2..7): explicit alias map only, no silent fuzzy matching,
over-merge worse than under-merge, contradictions surfaced never
adjudicated. Never invent a resolution.

Schema normalizations (recorded, 2026-10-07):
- home_sieve1_spans.json used non-standard genres/rels (drafter was
  correctly blind to the main brief's vocabularies). Remapped:
  experiment_report->verified, paper_outline->original,
  derives-from->depends_on, quantifies->supports.
- String-valued loop entries (3 span-pass files) normalized to
  {"concept_id": None, "text": <string>}.
- Citing-chunk artifact (maynard_p1): claims cited without proof were
  marked conjectural per calibration even when established theorems;
  adjudication must treat this as a chunk artifact, not an epistemic
  downgrade.
"""
import json, glob, re, os, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
EXD = os.path.join(BASE, 'extractions')
GRAPHD = os.path.join(BASE, 'graphs')
os.makedirs(GRAPHD, exist_ok=True)

GENRE_REMAP = {'experiment_report': 'verified', 'paper_outline': 'original',
                 'derivation': 'original', 'structural': 'reframed',
                 'computation': 'verified', 'open': None, 'home': None}
STATUS_REMAP = {
    'computationally verified': 'computationally_verified',
    'derived': 'exact',
    'exact identities': 'exact',
    "open (literature saturated per experts' own assessment)": 'heuristic',
    'exact algebra; computationally verified': 'computationally_verified',
    'conjectural / unclaimed': 'conjectural',
    'definition': 'exact',
    'reframing; verified': 'computationally_verified',
    'negative result (exact kill)': 'killed',
    'computationally verified (negative probes)': 'killed',
    'exact; verified computationally at every tested cutoff': 'computationally_verified',
    'exact specification': 'exact',
    'exact; verified computationally': 'computationally_verified',
    'reframing; verified through 60': 'computationally_verified',
    'computed; fully explained': 'computationally_verified',
    'algebra verified; framing appears new': 'computationally_verified',
    'conjectural \u2014 explicitly not claimed': 'conjectural',
    'classical identities, new framing; verified as labeled': 'exact',
    'verified as labeled': 'computationally_verified',
    'verified as labeled, with caveats': 'computationally_verified',
}
# rel remap: value = (new_rel, flip_direction)
REL_REMAP = {'derives-from': ('depends_on', False),
             'quantifies': ('supports', False),
             'enables': ('depends_on', True),   # a enables b <=> b depends_on a
             'limits': ('refines', False),
             'qualifies': ('refines', False),
             'instantiates': ('illustrates', False),
             'parallels': ('supports', False),
             'relates': ('supports', False),
             'contrasts_with': ('contradicts', False),
             'extends': ('generalizes', False),
             'constrains': ('refines', False)}
VALID_GENRE = {'original', 'reframed', 'identification', 'verified', 'killed'}
VALID_STATUS = {'exact', 'computationally_verified', 'conjectural', 'heuristic', 'killed'}
VALID_REL = {'supports', 'depends_on', 'contradicts', 'refines', 'generalizes', 'illustrates'}

STOP = set('''the a an of and or to in on for with as by is are was were be
been from that this it its at which who whom whose what when where how
all any both each few more most other some such no nor not only own same
so than too very can will just don should now into over after before
between through during above below up down off again further then
once here there when where why how s t d ll m o y e.g i.e vs via per
one two three form forms case cases set sets number numbers let
also well even much many like within without under over each
'''.split())

# domain-generic tokens that must not seed a candidate by themselves.
# NOTE (span directive): prime/primes/gap/gaps/sieve/twin/zero/interval
# are LOAD-BEARING in this run and are deliberately NOT generic.
GENERIC = {'formula', 'formulas', 'function', 'functions', 'theorem',
           'theory', 'theories', 'explicit', 'paper', 'result', 'results',
           'using', 'used', 'method', 'methods', 'conjecture', 'lemma',
           'lemmas', 'proposition', 'corollary', 'proof', 'section',
           'example', 'application', 'applications', 'construction',
           'definition', 'remark', 'hypothesis', 'claim', 'strategy',
           'algorithm', 'computation', 'computations', 'chapter',
           'introduction', 'outline', 'bound', 'bounds', 'estimate',
           'estimates', 'note', 'notes', 'survey', 'approach', 'general',
           'using', 'given', 'known', 'follows', 'following', 'shows',
           'show', 'showed', 'proved', 'prove', 'proves', 'let',
           'assume', 'suppose', 'consider', 'define', 'defined'}

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
    if fname.startswith('home_'):
        return 'home'
    if fname.startswith('foreign_'):
        return 'foreign'
    raise ValueError(fname)

def paper_of(fname):
    # foreign_<paper>_p<N> | home_sieve<N> | home_sieve<N>_spans
    parts = fname.split('_')
    if fname.startswith('foreign_'):
        return parts[1]
    return 'sieve' + parts[1].replace('sieve', '')

ALIASES = []  # populated ONLY from reviewed pass1_review.json
remap_counts = defaultdict(int)

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
            genre = a.get('genre')
            if genre in GENRE_REMAP:
                remap_counts[f'genre:{genre}'] += 1
                genre = GENRE_REMAP[genre]
            if genre not in VALID_GENRE:
                if genre is not None:
                    remap_counts[f'genre:DROP:{genre}'] += 1
                genre = None
            status = a.get('status', 'heuristic')
            if status in STATUS_REMAP:
                remap_counts[f'status:{status}'] += 1
                status = STATUS_REMAP[status]
            if status not in VALID_STATUS:
                remap_counts[f'status:DROP:{status}'] += 1
                status = 'heuristic'
            nodes[nid] = {
                'id': nid, 'sky': sky, 'paper': paper,
                'file': fname, 'cid': c['id'],
                'label': c['label'], 'kind': c['kind'],
                'status': status, 'genre': genre,
                'note': a.get('note', ''),
            }
            idmap[c['id']] = nid
        for e in d.get('edges', []):
            rel = e['rel']
            rel_orig = rel
            flip = False
            if rel in REL_REMAP:
                remap_counts[f'rel:{rel}'] += 1
                rel, flip = REL_REMAP[rel]
            if rel not in VALID_REL:
                remap_counts[f'rel:DROP:{rel}'] += 1
                continue
            if e['a'] in idmap and e['b'] in idmap:
                ea, eb = idmap[e['a']], idmap[e['b']]
                if flip:
                    ea, eb = eb, ea
                edges.append({'a': ea, 'b': eb,
                              'rel': rel, 'rel_orig': rel_orig,
                              'sky': sky, 'paper': paper})
        for l in d.get('loops', []):
            if isinstance(l, str):
                loops.append({'concept_id': None, 'text': l,
                              'sky': sky, 'paper': paper, 'file': fname})
                remap_counts['loop:string'] += 1
            elif isinstance(l, dict) and l.get('concept_id') in idmap:
                loops.append({'concept_id': idmap[l['concept_id']],
                              'sky': sky, 'paper': paper, 'file': fname})
    return nodes, edges, loops

def main():
    nodes, edges, loops = load()
    print(f'loaded {len(nodes)} nodes, {len(edges)} within-file edges, {len(loops)} loops')
    print('remaps:', dict(remap_counts))
    by = defaultdict(int)
    for n in nodes.values():
        by[(n['sky'], n['paper'])] += 1
    print('by (sky,paper):', dict(by))
    json.dump({'nodes': nodes, 'edges': edges, 'loops': loops},
              open(os.path.join(GRAPHD, 'atlas8_raw.json'), 'w'),
              ensure_ascii=False, indent=1)

    toks = {nid: tokens(n['label'], n['note']) for nid, n in nodes.items()}
    ids = list(nodes)

    def shared_ab(a, b):
        return sorted((toks[a] & toks[b]) - GENERIC)

    # Pass 1: same sky, different file, >=4 shared non-generic tokens
    p1 = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            if nodes[a]['sky'] != nodes[b]['sky']:
                continue
            if nodes[a]['file'] == nodes[b]['file']:
                continue
            sh = shared_ab(a, b)
            if len(sh) >= 4:
                p1.append({'a': a, 'b': b, 'shared': sh,
                           'la': nodes[a]['label'], 'lb': nodes[b]['label'],
                           'pa': nodes[a]['paper'], 'pb': nodes[b]['paper'],
                           'fa': nodes[a]['file'], 'fb': nodes[b]['file']})
    p1.sort(key=lambda c: -len(c['shared']))
    json.dump(p1, open(os.path.join(BASE, 'pass1_review.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'{len(p1)} within-sky high-overlap pairs -> pass1_review.json')

    # Pass 2: cross-sky candidates (home<->foreign), >=2 shared tokens
    cand = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            sa, sb = nodes[a]['sky'], nodes[b]['sky']
            if sa == sb:
                continue
            sh = shared_ab(a, b)
            if len(sh) >= 2:
                cand.append({'a': a, 'b': b, 'shared': sh,
                             'la': nodes[a]['label'], 'lb': nodes[b]['label'],
                             'pa': nodes[a]['paper'], 'pb': nodes[b]['paper'],
                             'sa': sa, 'sb': sb,
                             'ka': nodes[a]['status'], 'kb': nodes[b]['status'],
                             'na': nodes[a]['note'][:200], 'nb': nodes[b]['note'][:200]})
    cand.sort(key=lambda c: -len(c['shared']))
    json.dump(cand, open(os.path.join(BASE, 'candidates.json'), 'w'),
              ensure_ascii=False, indent=1)
    print(f'{len(cand)} home<->foreign candidates -> candidates.json')
    print('ALIAS map entries (reviewed):', len(ALIASES))

if __name__ == '__main__':
    main()
