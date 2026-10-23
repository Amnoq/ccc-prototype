#!/usr/bin/env python3
"""Atlas-11 merge: three skies (analytics / geometry / bridge), each merged
within-sky (Pass 1), then mechanical cross-sky candidate generation for
the reviewed adjudication (Pass 2, done by a separate coordinator).

Adapts corpus_runs/atlas4/merge_atlas4.py; MERGE_PLAN.md rules apply:
explicit alias map only, no silent fuzzy matching, over-merge worse
than under-merge, contradictions surfaced never adjudicated.

Reads:  atlas11/extractions/*.json, atlas11/alias_map.json
Writes: atlas11/graphs/<sky>_graph.json (per sky),
        atlas11/graphs/combined_graph.json,
        atlas11/candidates.json (cross-sky candidates for review)
"""
import json, glob, re, os, unicodedata, datetime
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
PREFIX = {'analytics': 'ana', 'geometry': 'geo', 'bridge': 'bri'}
EXD = os.path.join(BASE, 'extractions')
GRAPHD = os.path.join(BASE, 'graphs')
ALIASF = os.path.join(BASE, 'alias_map.json')

SKIES = ['analytics', 'geometry', 'bridge']

# extraction-file prefix -> sky
def sky_of(fid):
    p = fid.split('_')[0]
    if p in ('a1', 'a2'):
        return 'analytics'
    if p in ('g1', 'g2'):
        return 'geometry'
    if p == 'b1':
        return 'bridge'
    return 'unknown'

STATUS_RANK = {'exact': 4, 'computationally_verified': 3,
               'conjectural': 2, 'heuristic': 1}

def normalize(label):
    t = unicodedata.normalize('NFKD', label or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r'[^a-z0-9]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def slug(label, taken):
    base = re.sub(r'[^a-z0-9]+', '-', normalize(label)).strip('-')[:48] or 'node'
    s, i = base, 2
    while s in taken:
        s = f"{base}-{i}"; i += 1
    taken.add(s)
    return s

def load_aliases():
    if os.path.exists(ALIASF):
        with open(ALIASF) as f:
            return json.load(f)
    return {"aliases": [], "notes": "empty; fill after candidate review"}

def collect(files):
    occs, edges_raw, loops_raw, strands_raw = [], [], [], []
    for path in files:
        fid = os.path.splitext(os.path.basename(path))[0]
        with open(path) as f:
            d = json.load(f)
        sky = sky_of(fid)
        if sky == 'unknown':
            print(f"WARN: unknown sky for file {fid}")
        cmap = {c['id']: c for c in d.get('concepts', [])}
        amap = defaultdict(list)
        for a in d.get('anchors', []):
            amap[a['concept_id']].append(a)
        for cid, c in cmap.items():
            for a in amap.get(cid, [{}]):
                occs.append({'file': fid, 'sky': sky, 'cid': cid,
                             'kind': c.get('kind'), 'label': c.get('label', ''),
                             'genre': a.get('genre'), 'note': a.get('note', ''),
                             'status': a.get('status', 'heuristic')})
        for e in d.get('edges', []):
            edges_raw.append({'file': fid, 'sky': sky, 'a': e['a'],
                              'b': e['b'], 'rel': e['rel']})
        for l in d.get('loops', []):
            loops_raw.append({'file': fid, 'sky': sky, 'cid': l['concept_id']})
        for s in d.get('strands', []):
            strands_raw.append({'file': fid, 'sky': sky, 'sid': s.get('id'),
                                'label': s.get('label', ''),
                                'cids': s.get('concept_ids', [])})
    return occs, edges_raw, loops_raw, strands_raw

def merge_sky(sky, occs, edges_raw, loops_raw, strands_raw, aliases):
    taken = set()
    groups = defaultdict(list)
    for o in occs:
        groups[normalize(o['label'])].append(o)
    norm_of = {norm: norm for norm in groups}
    for al in aliases:
        pat = re.compile(al['pattern'], re.I)
        for norm in list(groups.keys()):
            if norm_of[norm] == norm and pat.search(norm):
                norm_of[norm] = al['target']
    merged = defaultdict(list)
    for norm, occ_list in groups.items():
        merged[norm_of[norm]].extend(occ_list)
    subjects, standalone = {}, {}
    for norm, occ_list in merged.items():
        rep = max(occ_list, key=lambda o: len(o['label'] or ''))
        sid = slug(rep['label'], taken)
        best, best_rank = 'heuristic', 0
        kill_notes = []
        for o in occ_list:
            st = o['status']
            if st == 'killed':
                kill_notes.append((o['file'], o['note']))
                continue
            r = STATUS_RANK.get(st, 0)
            if r > best_rank:
                best, best_rank = st, r
        status = best
        kill_about_concept = [n for _, n in kill_notes
                              if n and not re.search(r'citat|cited|assum|hypothes|for contradiction', n, re.I)]
        if kill_about_concept:
            status = 'killed'
        facets = [{'file': o['file'], 'cid': o['cid'], 'label': o['label'],
                   'kind': o['kind'], 'status': o['status'],
                   'genre': o['genre'], 'note': o['note']} for o in occ_list]
        # a "merged" subject means distinct chunk-concepts resolved to one
        # node; multiple anchors on one concept do NOT make a merge
        n_concepts = len({(f['file'], f['cid']) for f in facets})
        entry = {'id': sid, 'label': rep['label'], 'status': status,
                 'n_facets': len(facets), 'n_concepts': n_concepts,
                 'facets': facets,
                 'kill_notes': kill_notes if status == 'killed' else []}
        (subjects if n_concepts > 1 else standalone)[sid] = entry
    remap = {}
    for sid, s in {**subjects, **standalone}.items():
        for f in s['facets']:
            remap[(f['file'], f['cid'])] = sid
    edge_counts, edge_prov = defaultdict(int), defaultdict(list)
    for e in edges_raw:
        a = remap.get((e['file'], e['a'])); b = remap.get((e['file'], e['b']))
        if not a or not b:
            continue
        key = (a, b, e['rel'])
        edge_counts[key] += 1
        edge_prov[key].append(e['file'])
    edges = [{'a': a, 'b': b, 'rel': r, 'count': c, 'files': edge_prov[(a, b, r)]}
             for (a, b, r), c in edge_counts.items()]
    pair_rels = defaultdict(set)
    for (a, b, r) in edge_counts:
        pair_rels[tuple(sorted((a, b)))].add(r)
    flagged = [{'a': a, 'b': b, 'rels': sorted(rels),
                'note': 'contradictory edges surfaced, not adjudicated'}
               for (a, b), rels in pair_rels.items()
               if 'supports' in rels and 'contradicts' in rels]
    loops = [{'file': l['file'], 'subject': remap.get((l['file'], l['cid'])),
              'cid': l['cid']} for l in loops_raw
             if remap.get((l['file'], l['cid']))]
    return {'sky': sky, 'subjects': subjects, 'standalone': standalone,
            'edges': edges, 'flagged': flagged, 'loops': loops,
            'strands': [{'file': s['file'], 'sid': s['sid'], 'label': s['label'],
                         'subjects': [remap.get((s['file'], c)) for c in s['cids']]}
                        for s in strands_raw],
            'stats': {'occurrences': len(occs), 'subjects': len(subjects),
                      'standalone': len(standalone), 'edges': len(edges),
                      'flagged': len(flagged), 'loops': len(loops)}}

STOP = {'the', 'and', 'for', 'with', 'from', 'that', 'this', 'are',
        'was', 'were', 'has', 'have', 'which', 'their', 'its', 'into',
        'such', 'than', 'then', 'also', 'when', 'where', 'between',
        'under', 'over', 'both', 'each', 'other', 'some', 'more'}
# Drafter meta-discourse about the extraction itself (not mathematical
# content); excluded from candidate scoring so boilerplate like
# "cited, not proved here" cannot drive matches.
META = {'cited', 'prove', 'proves', 'proved', 'proving', 'here', 'there',
        'paper', 'papers', 'states', 'stated', 'brief', 'phrase', 'phrases',
        'identifying', 'claim', 'claims', 'says', 'gives', 'given', 'follows',
        'following', 'section', 'sections', 'chunk', 'chunks', 'drafter',
        'extracted', 'extraction', 'note', 'notes', 'word', 'words',
        'exact', 'heuristic', 'conjectural', 'mention', 'mentions',
        'mentioned', 'discusses', 'discussed', 'describes', 'described',
        'sketch', 'proof', 'theorem', 'proposition', 'lemma', 'corollary'}

def wtokens(t):
    return [w for w in t.split()
            if len(w) > 3 and w not in STOP and w not in META]

def wgrams(t, n):
    ws = t.split()
    return [' '.join(ws[i:i+n]) for i in range(len(ws)-n+1)
            if all(len(w) > 2 and w not in STOP and w not in META
                   for w in ws[i:i+n])]

def constants(text):
    out = set(re.findall(r'\d+\.\d{3,}', text or ''))
    out.update('F' + m for m in re.findall(r'\bF(\d{1,3})\b', text or ''))
    return out

def node_texts(graph):
    """sid -> (normalized full text over labels+notes, label, status, note0)."""
    out = {}
    for sid, s in {**graph['subjects'], **graph['standalone']}.items():
        parts = [s.get('label', '')]
        note0 = ''
        for fac in s['facets']:
            parts.append(fac.get('label', '') or '')
            nz = fac.get('note', '') or ''
            parts.append(nz)
            if not note0 and nz:
                note0 = nz
        out[sid] = (normalize(' '.join(parts)), s['label'],
                    s['status'], note0[:400])
    return out

# ---- lemmatization stage (default-on since 2026-10-08) ----
# Node label+note text is lemmatized via lemma-db's LemmaDB before IDF
# scoring. Authorized after the 2026-10-08 discriminating test
# (lemma_rerun.py): identical scoring/thresholds, lemmatized input ->
# 195 new candidates (recall up), 0 new adjudicated links (verdicts
# unchanged). --no-lemmatize reproduces the pre-stage mechanical
# baseline for control comparisons.
LEMMATIZE_DEFAULT = True
LEMMA_API_PATH = os.path.expanduser('~/workspace/lemma-db/lemma_api.py')

_lemma_db = None

def _get_lemma_db():
    """Lazy LemmaDB (lemma-db/lemma_api.py). Loaded only when lemmatize=True,
    so --no-lemmatize runs never touch the bank."""
    global _lemma_db
    if _lemma_db is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location('lemma_api',
                                                      LEMMA_API_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _lemma_db = mod.LemmaDB()
    return _lemma_db

def lemmatize_text(text, db):
    """Token-wise form->lemma over normalized text; unknown forms pass
    through unchanged (honest gap, mirrors the 2026-10-08 experiment)."""
    return ' '.join(db.lemmatize(w, 'en') or w for w in text.split())

def generate_candidates(texts, pairs=None, lemmatize=True, lem_db=None):
    """Mechanical cross-sky candidate generation (Pass 1 output; every
    candidate reviewed in Pass 2 separately).

    IDF-weighted token + bigram overlap over node label+note text.
    Thresholds: >=8 on the direct analytics<->geometry arm (discovery
    measurement -> recall-favoring), >=10 on the two seeded-control arms
    (known positives; control vocabulary verified to score >=10, so the
    higher bar loses no control signal while cutting reviewer noise).

    texts: {sky: {sid: (text, label, status, note0)}} as from node_texts().
    lemmatize=True (default): node text lemmatized via LemmaDB before
      scoring; lem_db lets callers inject a bank (tests), else lazy-load.
    Pure function: writes nothing. Returns (out_doc, by_pair_counts).
    out_doc['lemmatization'] records the stage setting + empirical bank
    coverage on the corpus, so every run is self-describing.
    """
    import math
    if pairs is None:
        # Atlas-11 test arms: direct analytics<->geometry, plus the two
        # seeded-control arms bridge<->analytics (S1) and bridge<->geometry (S2)
        pairs = [('analytics', 'geometry', 8.0),
                 ('bridge', 'analytics', 10.0),
                 ('bridge', 'geometry', 10.0)]
    lem_info = {'enabled': bool(lemmatize), 'bank': None, 'coverage': None}
    if lemmatize:
        db = lem_db if lem_db is not None else _get_lemma_db()
        raw_toks = [w for tmap in texts.values()
                    for (t, _l, _s, _n) in tmap.values()
                    for w in t.split()]
        lem_info['bank'] = ('LemmaDB ' + ', '.join(
            f'{lang}={n}' for lang, (_name, n)
            in sorted(db.languages().items())))
        lem_info['coverage'] = round(db.coverage(raw_toks, 'en'), 4)
        texts = {sky: {sid: (lemmatize_text(t, db), la, sta, na0)
                       for sid, (t, la, sta, na0) in tmap.items()}
                 for sky, tmap in texts.items()}
    n_nodes = sum(len(t) for t in texts.values())
    toksets, gramsets, constsets = {}, {}, {}
    df_tok, df_gram = defaultdict(int), defaultdict(int)
    for sky, tmap in texts.items():
        for sid, (t, _label, _status, _note0) in tmap.items():
            ts, gs = set(wtokens(t)), set(wgrams(t, 2))
            toksets[(sky, sid)] = ts
            gramsets[(sky, sid)] = gs
            constsets[(sky, sid)] = constants(t)
            for x in ts:
                df_tok[x] += 1
            for x in gs:
                df_gram[x] += 1
    idf_tok = {x: math.log((n_nodes + 1) / (d + 1)) + 1.0
               for x, d in df_tok.items()}
    idf_gram = {x: math.log((n_nodes + 1) / (d + 1)) + 1.0
                for x, d in df_gram.items()}
    candidates = []
    for sa, sb, tau in pairs:
        for sida, (ta, la, sta, na0) in texts[sa].items():
            tsa, gsa, csa = (toksets[(sa, sida)], gramsets[(sa, sida)],
                             constsets[(sa, sida)])
            for sidb, (tb, lb, stb, nb0) in texts[sb].items():
                tsb, gsb, csb = (toksets[(sb, sidb)], gramsets[(sb, sidb)],
                                 constsets[(sb, sidb)])
                shared_t = tsa & tsb
                shared_g = gsa & gsb
                shared_c = csa & csb
                score = (sum(idf_tok[x] for x in shared_t)
                         + 2.5 * sum(idf_gram[x] for x in shared_g)
                         + (8.0 if shared_c else 0.0))
                if score >= tau or shared_c:
                    top_t = sorted(shared_t, key=lambda x: -idf_tok[x])[:12]
                    top_g = sorted(shared_g, key=lambda x: -idf_gram[x])[:8]
                    candidates.append({
                        'pair': f'{sa}<->{sb}',
                        'threshold': tau,
                        'a_sky': sa, 'a': f'{PREFIX[sa]}:{sida}',
                        'a_label': la[:200], 'a_status': sta,
                        'a_note': na0[:300],
                        'b_sky': sb, 'b': f'{PREFIX[sb]}:{sidb}',
                        'b_label': lb[:200], 'b_status': stb,
                        'b_note': nb0[:300],
                        'shared_constants': sorted(shared_c),
                        'shared_tokens': top_t,
                        'shared_bigrams': top_g,
                        'score': round(score, 2)})
    candidates.sort(key=lambda c: (c['pair'], -c['score']))
    out_doc = {
        'method': ('IDF-weighted token+bigram overlap over normalized '
                   'node label+note text; drafter meta-discourse stopwords '
                   'excluded; score = sum idf(shared tokens) + 2.5 * sum '
                   'idf(shared bigrams) + 8 if shared constants. '
                   'Mechanical only; every candidate reviewed in Pass 2.'),
        'lemmatization': lem_info,
        'thresholds': {'analytics<->geometry': 8.0,
                       'bridge<->analytics': 10.0,
                       'bridge<->geometry': 10.0},
        'threshold_rationale': ('Direct arm is a discovery measurement: '
                                'recall-favoring bar. Control arms are known '
                                'positives: control vocabulary (langlands, '
                                'automorphic, hecke, eisenstein, cuspidal, '
                                'hitchin, moduli) verified >= 10 in both arms, '
                                'so the higher bar loses no control signal.'),
        'date': datetime.date.today().isoformat(),
        'candidates': candidates}
    by_pair = defaultdict(int)
    for c in candidates:
        by_pair[c['pair']] += 1
    return out_doc, by_pair

def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(
        description='Atlas-11 merge: within-sky merge + cross-sky candidates.')
    ap.add_argument('--lemmatize', dest='lemmatize', action='store_true',
                    default=LEMMATIZE_DEFAULT,
                    help='lemmatize node text via LemmaDB before IDF scoring '
                         '(default: on)')
    ap.add_argument('--no-lemmatize', dest='lemmatize', action='store_false',
                    help='reproduce the pre-stage mechanical baseline '
                         '(control comparisons)')
    args = ap.parse_args(argv)
    os.makedirs(GRAPHD, exist_ok=True)
    files = sorted(glob.glob(os.path.join(EXD, '*.json')))
    assert files, "no extraction files"
    alias_doc = load_aliases()
    aliases = alias_doc.get('aliases', [])
    occs, edges_raw, loops_raw, strands_raw = collect(files)

    sky_graphs = {}
    for sky in SKIES:
        so = [o for o in occs if o['sky'] == sky]
        se = [e for e in edges_raw if e['sky'] == sky]
        sl = [l for l in loops_raw if l['sky'] == sky]
        ss = [s for s in strands_raw if s['sky'] == sky]
        g = merge_sky(sky, so, se, sl, ss, aliases)
        g['alias_map'] = alias_doc
        sky_graphs[sky] = g
        with open(os.path.join(GRAPHD, f'{sky}_graph.json'), 'w') as f:
            json.dump(g, f, indent=1, ensure_ascii=False)
        st = g['stats']
        print(f"{sky}: occ={st['occurrences']} subjects={st['subjects']} "
              f"standalone={st['standalone']} edges={st['edges']} "
              f"flagged={st['flagged']} loops={st['loops']}")

    # combined graph (namespaced ids) for the money view
    combined = {'subjects': {}, 'standalone': {}, 'edges': [], 'loops': []}
    for sky, g in sky_graphs.items():
        for sid, s in g['subjects'].items():
            combined['subjects'][f'{PREFIX[sky]}:{sid}'] = dict(s, sky=sky)
        for sid, s in g['standalone'].items():
            combined['standalone'][f'{PREFIX[sky]}:{sid}'] = dict(s, sky=sky)
        for e in g['edges']:
            combined['edges'].append(dict(e, a=f"{PREFIX[sky]}:{e['a']}",
                                          b=f"{PREFIX[sky]}:{e['b']}", sky=sky))
        for l in g['loops']:
            combined['loops'].append(dict(l, sky=sky))
    with open(os.path.join(GRAPHD, 'combined_graph.json'), 'w') as f:
        json.dump(combined, f, indent=1, ensure_ascii=False)

    # ---- cross-sky candidate generation (mechanical; reviewed Pass 2 separately)
    texts = {sky: node_texts(g) for sky, g in sky_graphs.items()}
    out_doc, by_pair = generate_candidates(texts, lemmatize=args.lemmatize)
    with open(os.path.join(BASE, 'candidates.json'), 'w') as f:
        json.dump(out_doc, f, indent=1, ensure_ascii=False)
    print("cross-sky candidates:", dict(by_pair),
          "total:", len(out_doc['candidates']),
          "lemmatize:", args.lemmatize)

    # record the stage in the run manifest (self-describing runs)
    mf = os.path.join(BASE, 'manifest.json')
    man = json.load(open(mf))
    man['candidate_generation'] = {
        'lemmatization': args.lemmatize,
        'lemma_bank': out_doc['lemmatization']['bank'],
        'lemma_coverage': out_doc['lemmatization']['coverage'],
        'date': out_doc['date'],
        'note': ('Lemmatization is a default-on pipeline stage (2026-10-08): '
                 'node label+note text lemmatized via lemma-db LemmaDB before '
                 'IDF scoring. --no-lemmatize reproduces the pre-stage '
                 'mechanical baseline for control comparisons.'),
    }
    json.dump(man, open(mf, 'w'), indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()
