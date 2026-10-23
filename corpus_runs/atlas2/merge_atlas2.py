#!/usr/bin/env python3
"""Atlas-2 merge: foreign-corpus extractions -> merged foreign atlas,
then cross-corpus resolution against the pilot atlas (read-only).

Implements corpus_runs/atlas/MERGE_PLAN.md rules, adapted:
- Pass 1: merge WITHIN the foreign corpus (normalized label match +
  explicit alias map in alias_map.json; over-merge worse than under-merge).
- Pass 2a: mechanical cross-corpus resolution vs pilot atlas_graph.json
  (normalized match only).
- Candidate generation for human alias-map review (Pass 2b): token-overlap
  + distinctive-constant matches, with evidence. The reviewer adds
  explicit entries to alias_map.json; re-running then yields 2b.

Reads:  atlas2/extractions/*.json, atlas2/alias_map.json,
        ../atlas/atlas_graph.json (READ-ONLY)
Writes: atlas2/atlas2_graph.json, atlas2/cross_corpus.json,
        atlas2/candidates.json
"""
import json, glob, re, os, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
EXD = os.path.join(BASE, 'extractions')
PILOT = os.path.join(BASE, '..', 'atlas', 'atlas_graph.json')
ALIASF = os.path.join(BASE, 'alias_map.json')

STATUS_RANK = {'exact': 4, 'computationally_verified': 3,
               'conjectural': 2, 'heuristic': 1}
# killed handled specially per MERGE_PLAN (wins only if about the concept itself)

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

def pilot_subjects(pilot):
    """Yield (sid, label, note) uniformly over pilot subjects+standalone."""
    for sid, s in pilot.get('subjects', {}).items():
        for fac in s.get('facets', []):
            yield sid, fac.get('label', ''), fac.get('note', '')
    for s in pilot.get('standalone', []) or []:
        if isinstance(s, dict):
            yield s.get('id', ''), s.get('display', ''), s.get('note', '')

def main():
    files = sorted(glob.glob(os.path.join(EXD, '*.json')))
    assert files, "no extraction files"
    alias_doc = load_aliases()
    aliases = alias_doc.get('aliases', [])  # list of {pattern, target, reason}

    # ---- collect occurrences ----
    occs = []  # (file, cid, kind, label, anchor)
    edges_raw, loops_raw, strands_raw = [], [], []
    for path in files:
        fid = os.path.splitext(os.path.basename(path))[0]
        with open(path) as f:
            d = json.load(f)
        cmap = {c['id']: c for c in d.get('concepts', [])}
        amap = defaultdict(list)
        for a in d.get('anchors', []):
            amap[a['concept_id']].append(a)
        for cid, c in cmap.items():
            for a in amap.get(cid, [{}]):
                occs.append({'file': fid, 'cid': cid, 'kind': c.get('kind'),
                             'label': c.get('label', ''),
                             'genre': a.get('genre'), 'note': a.get('note', ''),
                             'status': a.get('status', 'heuristic')})
        for e in d.get('edges', []):
            edges_raw.append({'file': fid, 'a': e['a'], 'b': e['b'], 'rel': e['rel']})
        for l in d.get('loops', []):
            loops_raw.append({'file': fid, 'cid': l['concept_id']})
        for s in d.get('strands', []):
            strands_raw.append({'file': fid, 'sid': s.get('id'),
                                'label': s.get('label', ''),
                                'cids': s.get('concept_ids', [])})

    # ---- Pass 1: group by normalized label ----
    taken = set()
    groups = defaultdict(list)  # norm -> [occ]
    for o in occs:
        groups[normalize(o['label'])].append(o)
    # apply explicit aliases: pattern (regex on normalized label) -> target norm key
    norm_of = {}
    for norm in groups:
        norm_of[norm] = norm
    for al in aliases:
        pat = re.compile(al['pattern'], re.I)
        for norm in list(groups.keys()):
            if norm_of[norm] == norm and pat.search(norm):
                norm_of[norm] = al['target']
    merged = defaultdict(list)
    for norm, occ_list in groups.items():
        merged[norm_of[norm]].extend(occ_list)

    # ---- subject ids + status reconciliation ----
    subjects, standalone = {}, {}
    for norm, occ_list in merged.items():
        # representative label: longest label (most informative)
        rep = max(occ_list, key=lambda o: len(o['label'] or ''))
        sid = slug(rep['label'], taken)
        # status reconciliation (MERGE_PLAN): strongest honestly earned wins;
        # killed wins only if the kill note is about the concept itself
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
        # standalone = single-facet subjects (pilot convention)
        (standalone if len(facets) == 1 else subjects)[sid] = entry

    # id remap for edges: (file, cid) -> sid
    remap = {}
    for sid, s in {**subjects, **standalone}.items():
        for f in s['facets']:
            remap[(f['file'], f['cid'])] = sid

    # ---- edge union + contradiction flagging ----
    edge_counts = defaultdict(int)
    edge_prov = defaultdict(list)
    for e in edges_raw:
        a = remap.get((e['file'], e['a'])); b = remap.get((e['file'], e['b']))
        if not a or not b:
            continue
        key = (a, b, e['rel'])
        edge_counts[key] += 1
        edge_prov[key].append(e['file'])
    edges = [{'a': a, 'b': b, 'rel': r, 'count': c, 'files': edge_prov[(a, b, r)]}
             for (a, b, r), c in edge_counts.items()]
    # contradictions: same unordered pair with supports vs contradicts
    pair_rels = defaultdict(set)
    for (a, b, r) in edge_counts:
        pair_rels[tuple(sorted((a, b)))].add(r)
    flagged = []
    for (a, b), rels in pair_rels.items():
        if 'supports' in rels and 'contradicts' in rels:
            flagged.append({'a': a, 'b': b, 'rels': sorted(rels),
                            'note': 'contradictory edges surfaced, not adjudicated'})

    loops = [{'file': l['file'],
              'subject': remap.get((l['file'], l['cid'])),
              'cid': l['cid']} for l in loops_raw
             if remap.get((l['file'], l['cid']))]

    graph = {'subjects': subjects, 'standalone': standalone, 'edges': edges,
             'flagged': flagged, 'loops': loops,
             'strands': [{'file': s['file'], 'sid': s['sid'], 'label': s['label'],
                          'subjects': [remap.get((s['file'], c)) for c in s['cids']]}
                         for s in strands_raw],
             'alias_map': alias_doc,
             'stats': {'files': len(files), 'occurrences': len(occs),
                       'subjects': len(subjects), 'standalone': len(standalone),
                       'edges': len(edges), 'flagged': len(flagged),
                       'loops': len(loops)}}
    with open(os.path.join(BASE, 'atlas2_graph.json'), 'w') as f:
        json.dump(graph, f, indent=1, ensure_ascii=False)

    # ---- Pass 2a: mechanical cross-corpus resolution vs pilot ----
    with open(PILOT) as f:
        pilot = json.load(f)
    pilot_norm = {}  # norm label -> pilot subject id
    for sid, label, note in pilot_subjects(pilot):
        n = normalize(label)
        if n and n not in pilot_norm:
            pilot_norm[n] = sid
    cross = []
    for sid, s in {**subjects, **standalone}.items():
        hit = None
        for fac in s['facets']:
            n = normalize(fac.get('label', ''))
            if n in pilot_norm:
                hit = pilot_norm[n]; break
        cross.append({'foreign': sid, 'foreign_label': s['label'],
                      'pilot': hit,
                      'verdict': 'resolved' if hit else 'unresolved-mechanical',
                      'foreign_status': s['status'],
                      'n_facets': s['n_facets']})

    # ---- candidate generation for alias-map review ----
    STOP = {'the', 'and', 'for', 'with', 'from', 'that', 'this', 'are',
            'was', 'were', 'has', 'have', 'which', 'their', 'its', 'into',
            'such', 'than', 'then', 'also', 'when', 'where', 'zeros',
            'zeta', 'function'}
    def sig_tokens(label):
        return {t for t in normalize(label).split()
                if len(t) > 3 and t not in STOP}
    def constants(text):
        # distinctive numbers: decimals with >=4 sig digits, F<n>, named consts
        out = set(re.findall(r'\d+\.\d{3,}', text or ''))
        out.update('F' + m for m in re.findall(r'\bF(\d{1,3})\b', text or ''))
        return out
    pilot_sigs = {}
    for sid, label, note in pilot_subjects(pilot):
        toks, consts = sig_tokens(label), constants(label + ' ' + (note or ''))
        if sid not in pilot_sigs:
            pilot_sigs[sid] = [set(), set(), label]
        pilot_sigs[sid][0] |= toks
        pilot_sigs[sid][1] |= consts
    candidates = []
    for sid, s in {**subjects, **standalone}.items():
        if any(c['foreign'] == sid and c['verdict'] == 'resolved' for c in cross):
            continue
        ftoks, fconsts = set(), set()
        for fac in s['facets']:
            ftoks |= sig_tokens(fac.get('label', ''))
            fconsts |= constants((fac.get('label') or '') + ' ' + (fac.get('note') or ''))
        for psid, (ptoks, pconsts, plabel) in pilot_sigs.items():
            shared_consts = fconsts & pconsts
            shared_toks = ftoks & ptoks
            if shared_consts or len(shared_toks) >= 3:
                candidates.append({
                    'foreign': sid, 'foreign_label': s['label'][:160],
                    'pilot': psid, 'pilot_label': plabel[:160],
                    'shared_constants': sorted(shared_consts),
                    'shared_tokens': sorted(shared_toks)[:12],
                    'evidence_strength': ('constant' if shared_consts else
                                          'tokens-%d' % len(shared_toks))})
    candidates.sort(key=lambda c: (0 if c['shared_constants'] else 1,
                                   -len(c['shared_tokens'])))
    with open(os.path.join(BASE, 'candidates.json'), 'w') as f:
        json.dump(candidates, f, indent=1, ensure_ascii=False)
    with open(os.path.join(BASE, 'cross_corpus.json'), 'w') as f:
        json.dump({'pass': '2a-mechanical', 'records': cross,
                   'n_resolved': sum(1 for c in cross if c['verdict'] == 'resolved'),
                   'n_total': len(cross)}, f, indent=1, ensure_ascii=False)

    st = graph['stats']
    print(f"files={st['files']} occ={st['occurrences']} subjects={st['subjects']} "
          f"standalone={st['standalone']} edges={st['edges']} flagged={st['flagged']} loops={st['loops']}")
    print(f"cross-corpus 2a: {sum(1 for c in cross if c['verdict']=='resolved')}/{len(cross)} resolved")
    print(f"candidates for review: {len(candidates)}")

if __name__ == '__main__':
    main()
