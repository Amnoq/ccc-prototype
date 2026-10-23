#!/usr/bin/env python3
"""Atlas-3 merge: three skies (algebra / geometry / bridge), each merged
within-sky (Pass 1), then mechanical cross-sky candidate generation for
the reviewed adjudication (Pass 2, done by the coordinator by hand).

Adapts corpus_runs/atlas2/merge_atlas2.py; MERGE_PLAN.md rules apply:
explicit alias map only, no silent fuzzy matching, over-merge worse
than under-merge, contradictions surfaced never adjudicated.

Reads:  atlas3/extractions/*.json, atlas3/alias_map.json
Writes: atlas3/graphs/<sky>_graph.json (per sky),
        atlas3/graphs/combined_graph.json,
        atlas3/candidates.json (cross-sky candidates for review)
"""
import json, glob, re, os, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
EXD = os.path.join(BASE, 'extractions')
GRAPHD = os.path.join(BASE, 'graphs')
ALIASF = os.path.join(BASE, 'alias_map.json')

SKIES = ['algebra', 'geometry', 'bridge']

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
        sky = d.get('sky', 'unknown')
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
        entry = {'id': sid, 'label': rep['label'], 'status': status,
                 'n_facets': len(facets), 'facets': facets,
                 'kill_notes': kill_notes if status == 'killed' else []}
        (standalone if len(facets) == 1 else subjects)[sid] = entry
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
        'such', 'than', 'then', 'also', 'when', 'where'}

def sig_tokens(label):
    return {t for t in normalize(label).split() if len(t) > 3 and t not in STOP}

def constants(text):
    out = set(re.findall(r'\d+\.\d{3,}', text or ''))
    out.update('F' + m for m in re.findall(r'\bF(\d{1,3})\b', text or ''))
    return out

def node_sigs(graph):
    sigs = {}
    for sid, s in {**graph['subjects'], **graph['standalone']}.items():
        toks, consts = set(), set()
        for fac in s['facets']:
            toks |= sig_tokens(fac.get('label', ''))
            consts |= constants((fac.get('label') or '') + ' ' + (fac.get('note') or ''))
        sigs[sid] = (toks, consts, s['label'], s['status'])
    return sigs

def main():
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
            combined['subjects'][f'{sky[0]}:{sid}'] = dict(s, sky=sky)
        for sid, s in g['standalone'].items():
            combined['standalone'][f'{sky[0]}:{sid}'] = dict(s, sky=sky)
        for e in g['edges']:
            combined['edges'].append(dict(e, a=f"{sky[0]}:{e['a']}",
                                          b=f"{sky[0]}:{e['b']}", sky=sky))
        for l in g['loops']:
            combined['loops'].append(dict(l, sky=sky))
    with open(os.path.join(GRAPHD, 'combined_graph.json'), 'w') as f:
        json.dump(combined, f, indent=1, ensure_ascii=False)

    # ---- cross-sky candidate generation (mechanical; reviewed Pass 2 by hand)
    sigs = {sky: node_sigs(g) for sky, g in sky_graphs.items()}
    pairs = [('algebra', 'geometry'), ('bridge', 'algebra'), ('bridge', 'geometry')]
    candidates = []
    for sa, sb in pairs:
        for sid, (ftoks, fconsts, flabel, fstatus) in sigs[sa].items():
            for psid, (ptoks, pconsts, plabel, pstatus) in sigs[sb].items():
                shared_consts = fconsts & pconsts
                shared_toks = ftoks & ptoks
                if shared_consts or len(shared_toks) >= 3:
                    candidates.append({
                        'pair': f'{sa}<->{sb}',
                        'a_sky': sa, 'a': sid, 'a_label': flabel[:160],
                        'a_status': fstatus,
                        'b_sky': sb, 'b': psid, 'b_label': plabel[:160],
                        'b_status': pstatus,
                        'shared_constants': sorted(shared_consts),
                        'shared_tokens': sorted(shared_toks)[:12],
                        'evidence_strength': ('constant' if shared_consts else
                                              'tokens-%d' % len(shared_toks))})
    candidates.sort(key=lambda c: (c['pair'],
                                   0 if c['shared_constants'] else 1,
                                   -len(c['shared_tokens'])))
    with open(os.path.join(BASE, 'candidates.json'), 'w') as f:
        json.dump(candidates, f, indent=1, ensure_ascii=False)
    by_pair = defaultdict(int)
    for c in candidates:
        by_pair[c['pair']] += 1
    print("cross-sky candidates:", dict(by_pair),
          "total:", len(candidates))

if __name__ == '__main__':
    main()
