#!/usr/bin/env python3
"""Build atlas8_interactive.html — the interactive constellation browser
for the Atlas-8 prime-distribution run, in the original template style
(corpus_runs/atlas/atlas_template.html): force-directed canvas, tap node
for facets/provenance, search, filters, clickable open loops. Cross-sky
split_links render GOLD; the 4 verified cracks render brighter gold."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, '..', 'atlas', 'atlas_template.html')) as f:
    TPL = f.read()

g = json.load(open(os.path.join(BASE, 'graphs', 'atlas8_raw.json')))
adj = json.load(open(os.path.join(BASE, 'atlas8_adjudications.json')))['adjudications']

CRACK_OF = {'A8-06': 'K8-1 · PNT = total weight 1',
            'A8-09': 'K8-2 · admissibility emerges',
            'A8-10': 'K8-2 · admissibility emerges',
            'A8-12': 'K8-2 · admissibility emerges',
            'A8-11': 'K8-3 · twin constant derived',
            'A8-13': 'K8-4 · independent sieve'}
SHORT_RD = {
    'A8-01': 'cited vs proved (Maynard→Zhang)',
    'A8-02': 'diagonalization lemma vs face form',
    'A8-03': 'Selberg inequality vs face form',
    'A8-04': 'working weights vs face reframing',
    'A8-05': 'y-diagonalization vs face form',
}

subjects = {}
for nid, n in g['nodes'].items():
    nid = nid if isinstance(nid, str) else n['id']
    sky = 'foreign literature' if nid.startswith('foreign') else 'circle sieve'
    subjects[nid] = {
        'display': n.get('label', nid)[:120],
        'status': n.get('status', 'open'),
        'facets': [{'chunk': n.get('file', ''), 'cid': n.get('cid', ''),
                    'label': n.get('label', nid)[:160],
                    'kind': n.get('kind', ''), 'status': n.get('status', 'open'),
                    'genre': n.get('genre', ''), 'note': (n.get('note', '') or '')[:600],
                    'subjects': []}],
        'status_note': None,
        'chunks': [n.get('file', '')],
        'killed_facets': 0,
        '_sky': sky,
    }

edges = []
for e in g['edges']:
    if e['a'] in subjects and e['b'] in subjects:
        edges.append({'a': e['a'], 'b': e['b'], 'rel': e.get('rel', 'related'),
                      'count': 1, 'gold': False, 'crack': None})
for x in adj:
    if x['verdict'] != 'split_link':
        continue
    a, b = x['a'], x['b']
    if a not in subjects or b not in subjects:
        continue
    crack = CRACK_OF.get(x['id'])
    rel = ('CRACK ' if crack else 'split_link · ') + (crack or SHORT_RD.get(x['id'], x.get('relation', '')))
    edges.append({'a': a, 'b': b, 'rel': rel[:140], 'count': 2,
                  'gold': True, 'crack': crack})

loops = [{'chunk': l.get('file', ''), 'label': (l.get('concept_id', '') or '')[:110]}
         for l in g.get('loops', [])]

GRAPH = {
    'subjects': {k: {kk: v[kk] for kk in
                 ('display', 'status', 'facets', 'status_note', 'chunks', 'killed_facets')}
                 for k, v in subjects.items()},
    'standalone': [],
    'edges': edges,
    'stats': {'subjects': len(subjects),
              'cross_edges': sum(1 for e in edges if e['gold']),
              'concepts': len(subjects)},
    'loops': loops,
}

html = TPL
html = html.replace(
    '<title>Lemma Atlas — prime-distribution research program</title>',
    '<title>Atlas-8 — the circle sieve meets the literature</title>')
html = html.replace('<div class="title">Lemma Atlas</div>',
    '<div class="title">Atlas-8 — the circle sieve meets the literature</div>')
html = html.replace(
    'epistemic-status map of the prime-distribution research program · tap a node for detail · drag to pan, pinch/scroll to zoom',
    'landmark prime literature vs the circle sieve · 4 cracks verified computationally · tap a node for detail · drag to pan, pinch/scroll to zoom')
# carry gold/crack flags through the edge mapping
html = html.replace(
    "let edges = GRAPH.edges.map(e => ({ a:e.a, b:e.b, rel:e.rel, w:e.count }))",
    "let edges = GRAPH.edges.map(e => ({ a:e.a, b:e.b, rel:e.rel, w:e.count, gold:!!e.gold, crack:e.crack||null }))")
# gold rendering for cross-sky links
html = html.replace(
    "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : 'rgba(139,148,158,.16)';",
    "ctx.strokeStyle = e.crack ? 'rgba(255,215,0,.95)' : e.gold ? 'rgba(255,215,0,.55)' : sel ? 'rgba(230,237,243,.5)' : 'rgba(139,148,158,.16)';")
html = html.replace(
    "ctx.lineWidth = sel ? Math.min(3, .6+e.w*.5) : 1;",
    "ctx.lineWidth = e.crack ? 3 : e.gold ? 1.8 : sel ? Math.min(3, .6+e.w*.5) : 1;")
# legend: add the gold entries
html = html.replace(
    "+ `<span class=\"li hint\">node size ∝ facet count</span>`;",
    "+ `<span class=\"li\"><span class=\"dot\" style=\"background:#ffd700\"></span>verified crack</span>`"
    "+ `<span class=\"li\"><span class=\"dot\" style=\"background:#8a7a2a\"></span>split_link</span>`"
    "+ `<span class=\"li hint\">node size ∝ facet count</span>`;")
# stats line: cross_edges are the gold links
html = html.replace('${st.cross_edges} relations', '${st.cross_edges} gold cross-sky links')

html = html.replace('/*__GRAPH__*/{}', json.dumps(GRAPH))

out = os.path.join(BASE, 'atlas8_interactive.html')
with open(out, 'w') as f:
    f.write(html)
print('wrote', out, len(html), 'bytes;',
      len(subjects), 'nodes,', len(edges), 'edges,',
      sum(1 for e in edges if e['crack']), 'crack edges')
