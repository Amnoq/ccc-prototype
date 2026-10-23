#!/usr/bin/env python3
"""Atlas-5 illustration: per-sky galaxy views (computation / proportion /
density) + the pilot's relational sky (read-only) + money view with
adjudicated cross-sky links. Reuses the Atlas-2/3/4 render-time patch
technique (galaxy layout, edges on, gold cross-links, clickable
loop-constellations) against the shared template (read-only).

Preprint discipline: nodes with preprint=True (Alpöge–Furman) carry a
visible preprint note; the label is never upgraded.

Shape conversion to what atlas_template.html expects:
  GRAPH.subjects: {id: {display, status, cluster, facets, ...}}
  GRAPH.standalone, GRAPH.edges, GRAPH.loops (with node for clicks),
  GRAPH.stats
"""
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, '..', 'atlas', 'atlas_template.html')) as f:
    TEMPLATE = f.read()

PREPRINT_NOTE = 'preprint — unrefereed as of 2026-10-07; ledger item 1 tracks its fate'

def conv_sky(g, sky, prefix=''):
    subjects = {}
    for sid, s in g['subjects'].items():
        facs = s.get('facets', [])
        pre = bool(s.get('preprint'))
        subjects[prefix + sid] = {
            'display': s.get('label', sid), 'status': s.get('status', 'heuristic'),
            'cluster': sky,
            'status_note': PREPRINT_NOTE if pre else None,
            'facets': [{'chunk': x.get('file', '?'), 'cid': x.get('cid', ''),
                        'label': x.get('label', ''), 'kind': x.get('kind', ''),
                        'status': x.get('status', 'heuristic'),
                        'genre': x.get('genre'), 'note': x.get('note', '')}
                       for x in facs],
            'chunks': sorted({x.get('file', '?') for x in facs}),
            'killed_facets': s.get('n_facets', 0) - len(facs)}
    standalone = []
    for sid, s in g['standalone'].items():
        facs = s.get('facets', [])
        f0 = facs[0] if facs else {}
        pre = bool(s.get('preprint'))
        standalone.append({'id': prefix + sid, 'display': s.get('label', sid),
                           'status': s.get('status', 'heuristic'),
                           'cluster': sky,
                           'status_note': PREPRINT_NOTE if pre else None,
                           'chunk': f0.get('file', '?'), 'kind': f0.get('kind', ''),
                           'genre': f0.get('genre'), 'note': f0.get('note', '')})
    edges = [{'a': prefix + e['a'], 'b': prefix + e['b'],
              'rel': e.get('rel', 'related'), 'count': e.get('count', 1)}
             for e in g.get('edges', [])]
    node_of = {}
    for nid, s in subjects.items():
        for x in s['facets']:
            node_of[(x['chunk'], x['cid'])] = nid
    for s in standalone:
        node_of[(s['chunk'], '')] = s['id']
    loops = []
    for l in g.get('loops', []):
        nid = node_of.get((l.get('file'), l.get('cid')))
        loops.append({'chunk': l.get('file', '?'),
                      'label': (subjects.get(nid, {}) or {}).get('display')
                               or l.get('subject', ''),
                      'node': (prefix + nid) if nid else None})
    st = g.get('stats', {})
    return {'subjects': subjects, 'standalone': standalone, 'edges': edges,
            'loops': loops,
            'stats': {'subjects': len(subjects), 'cross_edges': len(edges),
                      'concepts': st.get('occurrences', 0)}}

def conv_relational(pilot_path):
    """Read-only conversion of the pilot atlas graph. Never modified."""
    with open(pilot_path) as f:
        pg = json.load(f)
    subjects = {}
    for sid, s in pg['subjects'].items():
        facs = s.get('facets', [])
        subjects['rel:' + sid] = {
            'display': s.get('display') or (facs[0].get('label', sid) if facs else sid),
            'status': s.get('status', 'open'), 'cluster': 'relational',
            'status_note': 'pilot-corpus node (analytic skies are cmp:/prp:/den:)',
            'facets': [{'chunk': 'PILOT:' + str(x.get('chunk', '?')), 'cid': x.get('cid', ''),
                        'label': x.get('label', ''), 'kind': x.get('kind', ''),
                        'status': x.get('status', 'open'),
                        'genre': x.get('genre'), 'note': x.get('note', '')}
                       for x in facs],
            'chunks': sorted({'PILOT:' + str(x.get('chunk', '?')) for x in facs}),
            'killed_facets': s.get('killed_facets', 0)}
    standalone = []
    sa = pg.get('standalone', [])
    items = sa.items() if isinstance(sa, dict) else [(s.get('id'), s) for s in sa if isinstance(s, dict)]
    for nid, s in items:
        standalone.append({'id': 'rel:' + nid, 'display': s.get('display', nid),
                           'status': s.get('status', 'open'), 'cluster': 'relational',
                           'status_note': 'pilot-corpus node',
                           'chunk': 'PILOT:' + str(s.get('chunk', '')),
                           'kind': s.get('kind', ''), 'genre': s.get('genre'),
                           'note': s.get('note', '')})
    edges = [{'a': 'rel:' + e['a'], 'b': 'rel:' + e['b'],
              'rel': e.get('rel', 'related'), 'count': e.get('count', 1)}
             for e in pg.get('edges', [])
             if 'rel:' + e['a'] in subjects and 'rel:' + e['b'] in subjects]
    # pilot loops are {chunk, ref, label}; resolve via facet (chunk, cid)
    node_of = {}
    for nid, s in subjects.items():
        for x in s['facets']:
            node_of[(x['chunk'].replace('PILOT:', ''), x['cid'])] = nid
    loops = []
    for l in pg.get('loops', []):
        nid = node_of.get((l.get('chunk'), l.get('ref')))
        loops.append({'chunk': 'PILOT:' + str(l.get('chunk', '?')),
                      'label': l.get('label', ''),
                      'node': nid})
    return {'subjects': subjects, 'standalone': standalone, 'edges': edges,
            'loops': loops,
            'stats': {'subjects': len(subjects), 'cross_edges': len(edges),
                      'concepts': pg.get('stats', {}).get('concepts', 0)}}

# --- the Atlas-2/3/4 render-time patch block, verbatim ---
def render(graph, title, subtitle, path):
    page = TEMPLATE.replace(
        '<title>Lemma Atlas — prime-distribution research program</title>',
        '<title>' + html.escape(title) + '</title>')
    page = page.replace('const GRAPH = /*__GRAPH__*/{};',
                        'const GRAPH = /*__GRAPH__*/' + json.dumps(graph, ensure_ascii=False) + ';')
    page = page.replace('<div class="title">Lemma Atlas</div>',
                        '<div class="title">' + html.escape(title) + '</div>', 1)
    page = page.replace(
        '<div class="sub">epistemic-status map of the prime-distribution research program · tap a node for detail · drag to pan, pinch/scroll to zoom</div>',
        '<div class="sub">' + html.escape(subtitle) + ' · tap a node for detail · drag to pan, pinch/scroll to zoom</div>', 1)
    page = page.replace(
        "r: 7 + Math.min(13, Math.sqrt(s.facets.length) * 4), subject:true });",
        "r: 7 + Math.min(13, Math.sqrt(s.facets.length) * 4), subject:true, cluster:s.cluster||'misc' });")
    page = page.replace(
        "note:null, chunks:[s.chunk], killedFacets:0, r:4.5, subject:false });",
        "note:null, chunks:[s.chunk], killedFacets:0, r:4.5, subject:false, cluster:s.cluster||'misc' });")
    # thread status_note through node construction so the preprint badge shows
    page = page.replace(
        "subject:true, cluster:s.cluster||'misc' });",
        "subject:true, cluster:s.cluster||'misc', note:s.status_note||null });")
    page = page.replace(
        "subject:false, cluster:s.cluster||'misc' });",
        "subject:false, cluster:s.cluster||'misc', note:s.status_note||null });")
    page = page.replace(
        """  const R = Math.min(W,H) * 0.36;
  nodes.forEach((n,i) => {
    const a = (i / nodes.length) * Math.PI * 2;
    const jitter = ((i*7919) % 60) - 30;
    n.x = Math.cos(a)*(R+jitter); n.y = Math.sin(a)*(R+jitter);
    n.vx = 0; n.vy = 0;
  });""",
        """  const clusters = [...new Set(nodes.map(n => n.cluster||'misc'))].sort();
  const R = Math.min(W,H) * 0.30;
  clusters.forEach((c, ci) => {
    const a = (ci / clusters.length) * Math.PI * 2 - Math.PI/2;
    clusterC[c] = { x: Math.cos(a)*R, y: Math.sin(a)*R };
  });
  const per = {};
  nodes.forEach((n) => {
    const c = n.cluster || 'misc';
    const cc = clusterC[c];
    const k = (per[c] = (per[c]||0) + 1);
    const a = k * 2.39996, r = 16 * Math.sqrt(k);
    n.x = cc.x + Math.cos(a)*r; n.y = cc.y + Math.sin(a)*r;
    n.vx = 0; n.vy = 0;
  });""")
    page = page.replace(
        "let inited = false;",
        "let inited = false;\nconst clusterC = {};")
    page = page.replace(
        "a.vx += -a.x*0.004; a.vy += -a.y*0.004;",
        """a.vx += -a.x*0.004; a.vy += -a.y*0.004;
    const cc = clusterC[a.cluster||'misc'];
    if (cc){ a.vx += (cc.x-a.x)*0.03; a.vy += (cc.y-a.y)*0.03; }""")
    page = page.replace(
        '<input type="checkbox" id="f-edges">',
        '<input type="checkbox" id="f-edges" checked>')
    page = page.replace(
        "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : 'rgba(139,148,158,.16)';",
        "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : (e.rel.indexOf('cross:')===0 ? 'rgba(255,215,0,.6)' : 'rgba(139,148,158,.16)');")
    page = page.replace(
        """document.getElementById('looplo').innerHTML = GRAPH.loops.map(l=>
  `<div class="loop"><b>${esc(l.chunk)}</b> — ${esc(l.label)}</div>`).join('');""",
        """document.getElementById('looplo').innerHTML = GRAPH.loops.map(l=>
  `<div class="loop"${l.node?` data-node="${esc(l.node)}" title="trace this constellation" style="cursor:pointer"`:''}><b>${esc(l.chunk)}</b> — ${esc(l.label)}</div>`).join('');
document.getElementById('looplo').addEventListener('click', e=>{
  const t = e.target.closest('[data-node]');
  if (t){ const n = nodeById[t.getAttribute('data-node')]; if (n) select(n); }
});""")
    with open(path, 'w') as f:
        f.write(page)
    print('wrote', path, len(page) // 1024, 'KB')

SKIES = ['computation', 'proportion', 'density']
PREFIX = {'computation': 'cmp:', 'proportion': 'prp:', 'density': 'den:'}
SKY_TITLES = {
    'computation': ('Atlas-5 — computation sky',
                    'RH zero-computation records, extracted blind'),
    'proportion': ('Atlas-5 — proportion sky',
                   'zeros-on-the-line proportion results incl. the Alpöge–Furman preprint (labeled), extracted blind'),
    'density': ('Atlas-5 — density sky',
                'zero-density estimates, extracted blind'),
}

def main():
    views = {}
    for sky in SKIES:
        with open(os.path.join(BASE, 'graphs', f'{sky}_graph.json')) as f:
            g = json.load(f)
        views[sky] = conv_sky(g, sky)
        title, sub = SKY_TITLES[sky]
        render(views[sky], title, sub,
               os.path.join(BASE, f'atlas5_{sky}.html'))
    views['relational'] = conv_relational(os.path.join(BASE, '..', 'atlas', 'atlas_graph.json'))
    render(views['relational'], 'Atlas-5 — relational sky (pilot, read-only)',
           'the pilot program atlas: Node 8 bridge, Berry tones, interference theorem · rel: = pilot',
           os.path.join(BASE, 'atlas5_relational.html'))

    # money view: all skies + adjudicated cross-sky links as gold edges
    with open(os.path.join(BASE, 'cross_sky_links.json')) as f:
        links = json.load(f)['records']
    subjects, standalone, edges, loops = {}, [], [], []
    for sky in ['computation', 'proportion', 'density', 'relational']:
        v = views[sky]
        pre = PREFIX.get(sky, 'rel:')
        for sid, s in v['subjects'].items():
            key = sid if sid.startswith(pre) else pre + sid
            subjects[key] = s
        for s in v['standalone']:
            sid = s['id']
            key = sid if sid.startswith(pre) else pre + sid
            standalone.append(dict(s, id=key))
        for e in v['edges']:
            a = e['a'] if e['a'].startswith(pre) else pre + e['a']
            b = e['b'] if e['b'].startswith(pre) else pre + e['b']
            edges.append(dict(e, a=a, b=b))
        for l in v['loops']:
            node = l['node']
            if node and not node.startswith(pre):
                node = pre + node
            loops.append(dict(l, node=node))
    have = set(subjects) | {s['id'] for s in standalone}
    xedges = []
    for r in links:
        if r['verdict'] in ('missed_correct', 'control_void', 'rejected'):
            continue
        a, b = r['a'], r['b']  # sky-prefixed in the adjudication records
        if a not in have or b not in have:
            continue
        xedges.append({'a': a, 'b': b,
                       'rel': 'cross:%s:%s' % (r['verdict'], r['relation'] or '-'),
                       'count': 1})
    graph = {'subjects': subjects, 'standalone': standalone,
             'edges': edges + xedges, 'loops': loops,
             'stats': {'subjects': len(subjects), 'cross_edges': len(xedges),
                       'concepts': sum(v['stats']['concepts'] for v in views.values())}}
    render(graph, 'Atlas-5 money view — the constellations around RH',
           'cmp: = computation · prp: = proportion · den: = density · rel: = relational (pilot) · gold = adjudicated cross-sky links',
           os.path.join(BASE, 'atlas5_cross.html'))

if __name__ == '__main__':
    main()
