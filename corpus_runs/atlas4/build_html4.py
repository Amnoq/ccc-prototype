#!/usr/bin/env python3
"""Atlas-4 illustration: per-sky galaxy views + money view with
adjudicated cross-sky links. Reuses the Atlas-2 render-time patch
technique (galaxy layout, edges on, gold cross-links, clickable
loop-constellations) against the shared template (read-only).

Shape conversion from graphs/<sky>_graph.json to what
atlas_template.html expects:
  GRAPH.subjects: {id: {display, status, cluster, facets, ...}}
  GRAPH.standalone, GRAPH.edges, GRAPH.loops (with node for clicks),
  GRAPH.stats
"""
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, '..', 'atlas', 'atlas_template.html')) as f:
    TEMPLATE = f.read()

def conv_sky(g, sky, prefix=''):
    subjects = {}
    for sid, s in g['subjects'].items():
        facs = s.get('facets', [])
        subjects[prefix + sid] = {
            'display': s.get('label', sid), 'status': s.get('status', 'heuristic'),
            'cluster': sky,
            'facets': [{'chunk': x.get('file', '?'), 'cid': x.get('cid', ''),
                        'label': x.get('label', ''), 'kind': x.get('kind', ''),
                        'status': x.get('status', 'heuristic'),
                        'genre': x.get('genre'), 'note': x.get('note', '')}
                       for x in facs],
            'status_note': None,
            'chunks': sorted({x.get('file', '?') for x in facs}),
            'killed_facets': s.get('n_facets', 0) - len(facs)}
    standalone = []
    for sid, s in g['standalone'].items():
        facs = s.get('facets', [])
        f0 = facs[0] if facs else {}
        standalone.append({'id': prefix + sid, 'display': s.get('label', sid),
                           'status': s.get('status', 'heuristic'),
                           'cluster': sky,
                           'chunk': f0.get('file', '?'), 'kind': f0.get('kind', ''),
                           'genre': f0.get('genre'), 'note': f0.get('note', '')})
    # no pre-filtering: the template keeps edges whose endpoints exist
    # (subjects + standalone both become nodes)
    edges = [{'a': prefix + e['a'], 'b': prefix + e['b'],
              'rel': e.get('rel', 'related'), 'count': e.get('count', 1)}
             for e in g.get('edges', [])]
    # loops -> clickable constellations: resolve to node id
    node_of = {}
    for nid, s in {**subjects}.items():
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

# --- the Atlas-2 render-time patch block, verbatim ---
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

SKIES = ['symbolic', 'connectionist', 'statistical', 'neuro', 'bridge']
PREFIX = {'symbolic': 'sym:', 'connectionist': 'con:', 'statistical': 'sta:',
          'neuro': 'neu:', 'bridge': 'bri:'}
SKY_TITLES = {
    'symbolic': ('Atlas-4 — symbolic sky',
                 'McCarthy 1959 (Programs with Common Sense / Advice Taker), extracted blind'),
    'connectionist': ('Atlas-4 — connectionist sky',
                      'Rumelhart–Hinton–Williams 1986 (PDP ch.8, error propagation), extracted blind'),
    'statistical': ('Atlas-4 — statistical sky',
                    'Cortes & Vapnik 1995 (Support-Vector Networks), extracted blind'),
    'neuro': ('Atlas-4 — neuroscience sky',
              'Hubel & Wiesel 1959 (receptive fields, cat striate cortex), extracted blind — 1962 paper unobtainable, substituted per charter'),
    'bridge': ('Atlas-4 — bridge sky',
               "LeCun et al. 1989 (Backpropagation Applied to Handwritten Zip Code Recognition), extracted blind"),
}

def main():
    views = {}
    for sky in SKIES:
        with open(os.path.join(BASE, 'graphs', f'{sky}_graph.json')) as f:
            g = json.load(f)
        views[sky] = conv_sky(g, sky)
        title, sub = SKY_TITLES[sky]
        render(views[sky], title, sub,
               os.path.join(BASE, f'atlas4_{sky}.html'))

    # money view: combined + adjudicated cross-sky links as gold edges
    with open(os.path.join(BASE, 'graphs', 'combined_graph.json')) as f:
        cg = json.load(f)
    with open(os.path.join(BASE, 'cross_sky_links.json')) as f:
        links = json.load(f)['records']
    subjects, standalone, edges, loops = {}, [], [], []
    for sky in SKIES:
        v = views[sky]
        pre = PREFIX[sky]
        for sid, s in v['subjects'].items():
            subjects[pre + sid] = s
        for s in v['standalone']:
            standalone.append(dict(s, id=pre + s['id']))
        for e in v['edges']:
            edges.append(dict(e, a=pre + e['a'], b=pre + e['b']))
        for l in v['loops']:
            loops.append(dict(l, node=(pre + l['node']) if l['node'] else None))
    xedges = []
    for r in links:
        if r['verdict'] in ('missed_correct', 'control_void', 'rejected'):
            continue
        a, b = r['a'], r['b']  # already sky-prefixed in the adjudication records
        if a not in subjects and not any(s['id'] == a for s in standalone):
            continue
        if b not in subjects and not any(s['id'] == b for s in standalone):
            continue
        xedges.append({'a': a, 'b': b,
                       'rel': 'cross:%s:%s' % (r['verdict'], r['relation'] or '-'),
                       'count': 1})
    graph = {'subjects': subjects, 'standalone': standalone,
             'edges': edges + xedges, 'loops': loops,
             'stats': {'subjects': len(subjects), 'cross_edges': len(xedges),
                       'concepts': sum(v['stats']['concepts'] for v in views.values())}}
    render(graph, 'Atlas-4 money view — the skies of AI',
           'sym: = symbolic · con: = connectionist · sta: = statistical · neu: = neuroscience · bri: = bridge (LeCun 1989) · gold = adjudicated cross-sky links',
           os.path.join(BASE, 'atlas4_cross.html'))

if __name__ == '__main__':
    main()
