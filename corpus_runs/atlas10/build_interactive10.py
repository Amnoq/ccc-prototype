#!/usr/bin/env python3
"""Build atlas10_interactive.html — the interactive constellation browser
for the Atlas-10 chess run, in the original template style
(corpus_runs/atlas/atlas_template.html): force-directed canvas, tap node
for facets/provenance, search, filters, clickable open loops. Cross-sky
split_links render GOLD; the 2 verified cracks render brighter gold."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, '..', 'atlas', 'atlas_template.html')) as f:
    TPL = f.read()

g = json.load(open(os.path.join(BASE, 'graphs', 'atlas10_merged.json')))
adj = json.load(open(os.path.join(BASE, 'atlas10_adjudications.json')))
cracks = json.load(open(os.path.join(BASE, 'crack_join.json')))

CRACK_OF = {}  # cracks are game-level findings, not single edges here
SHORT_RD = {
    'A10-01': 'C1: book rule vs engine mate-in-2',
    'A10-02': 'C2: "or resigning" vs mate-in-8',
    'A10-03': 'Q+K bound vs mate-in-1',
    'A10-04': 'R+K bound vs mate-in-1',
    'A10-05': 'doubled pawns: defect vs asset',
    'A10-06': 'gambit: used vs defined',
    'A10-07': 'McCutcheon: asserted vs open',
}

SKY_NAME = {'theory': 'theory', 'annotations': 'annotations',
            'engine': 'engine'}

subjects = {}
for nid, n in g['nodes'].items():
    nid = nid if isinstance(nid, str) else n['id']
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
        '_sky': SKY_NAME.get(n.get('sky', ''), n.get('sky', '')),
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
    rel = ('CRACK ' if crack else 'split_link \u00b7 ') + (crack or SHORT_RD.get(x['id'], x.get('relation', '')))
    edges.append({'a': a, 'b': b, 'rel': rel[:140], 'count': 2,
                  'gold': True, 'crack': crack})

GRAPH = {
    'subjects': {k: {kk: v[kk] for kk in
                 ('display', 'status', 'facets', 'status_note', 'chunks', 'killed_facets')}
                 for k, v in subjects.items()},
    'standalone': [],
    'edges': edges,
    'stats': {'subjects': len(subjects),
              'cross_edges': sum(1 for e in edges if e['gold']),
              'concepts': len(subjects)},
    'loops': [],
}

html = TPL
html = html.replace(
    '<title>Lemma Atlas \u2014 prime-distribution research program</title>',
    '<title>Atlas-10 \u2014 chess: theory vs annotations vs engine</title>')
html = html.replace('<div class="title">Lemma Atlas</div>',
    '<div class="title">Atlas-10 \u2014 theory vs annotations vs engine</div>')
html = html.replace(
    'epistemic-status map of the prime-distribution research program \u00b7 tap a node for detail \u00b7 drag to pan, pinch/scroll to zoom',
    'Capablanca + Lasker vs Blue Book annotations vs Stockfish 17.1 \u00b7 2 cracks verified \u00b7 tap a node for detail \u00b7 drag to pan, pinch/scroll to zoom')
html = html.replace(
    "let edges = GRAPH.edges.map(e => ({ a:e.a, b:e.b, rel:e.rel, w:e.count }))",
    "let edges = GRAPH.edges.map(e => ({ a:e.a, b:e.b, rel:e.rel, w:e.count, gold:!!e.gold, crack:e.crack||null }))")
html = html.replace(
    "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : 'rgba(139,148,158,.16)';",
    "ctx.strokeStyle = e.crack ? 'rgba(255,215,0,.95)' : e.gold ? 'rgba(255,215,0,.55)' : sel ? 'rgba(230,237,243,.5)' : 'rgba(139,148,158,.16)';")
html = html.replace(
    "ctx.lineWidth = sel ? Math.min(3, .6+e.w*.5) : 1;",
    "ctx.lineWidth = e.crack ? 3 : e.gold ? 1.8 : sel ? Math.min(3, .6+e.w*.5) : 1;")
html = html.replace(
    "+ `<span class=\"li hint\">node size \u221d facet count</span>`;",
    "+ `<span class=\"li\"><span class=\"dot\" style=\"background:#ffd700\"></span>verified crack</span>`"
    "+ `<span class=\"li\"><span class=\"dot\" style=\"background:#8a7a2a\"></span>split_link</span>`"
    "+ `<span class=\"li hint\">node size \u221d facet count</span>`;")
html = html.replace('${st.cross_edges} relations', '${st.cross_edges} gold cross-sky links')

html = html.replace('/*__GRAPH__*/{}', json.dumps(GRAPH))

out = os.path.join(BASE, 'atlas10_interactive.html')
with open(out, 'w') as f:
    f.write(html)
print('wrote', out, len(html), 'bytes;',
      len(subjects), 'nodes,', len(edges), 'edges,',
      sum(1 for e in edges if e['gold']), 'gold')
