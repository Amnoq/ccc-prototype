#!/usr/bin/env python3
"""Atlas-6 bridge map: the Weil bridge at high resolution.

Converts graphs/atlas6_graph.json to the shared template shape, with
paper-clusters (af/bom/gro/rel), gold adjudicated bridge edges, and
role-difference labels drawn at bridge-edge midpoints. Reuses the
Atlas-2/3/4/5 render-time patch technique against the shared template
(read-only). Preprint facets (AF, GRO) carry the visible badge.
"""
import json, os, html, glob

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, '..', 'atlas', 'atlas_template.html')) as f:
    TEMPLATE = f.read()

PREPRINT_NOTE = 'preprint — unrefereed as of 2026-10-07'
CLUSTER_NAMES = {'af': 'analytic · Alpöge–Furman (preprint)',
                 'bom': 'analytic · Bombieri 2000',
                 'gro': 'analytic · Groskin (preprint)',
                 'rel': 'relational · pilot Node 10a'}

def build():
    g = json.load(open(os.path.join(BASE, 'graphs', 'atlas6_graph.json')))
    links = json.load(open(os.path.join(BASE, 'cross_bridge_links.json')))
    nodes = g['nodes']
    subjects, standalone = {}, []
    for nid, n in nodes.items():
        facs = [{'chunk': n['file'], 'cid': n['cid'], 'label': n['label'],
                 'kind': n['kind'], 'status': n['status'],
                 'genre': n['genre'], 'note': n['note']}]
        for mf in n.get('merged_facets', []):
            facs.append({'chunk': mf['file'], 'cid': '', 'label': mf['label'],
                         'kind': n['kind'], 'status': n['status'],
                         'genre': n['genre'],
                         'note': 'merged facet: ' + mf['note']})
        subjects[nid] = {
            'display': n['label'], 'status': n['status'],
            'cluster': CLUSTER_NAMES[n['paper']],
            'status_note': PREPRINT_NOTE if n['preprint'] else None,
            'facets': facs, 'chunks': sorted({x['chunk'] for x in facs}),
            'killed_facets': 0}
    edges = [{'a': e['a'], 'b': e['b'], 'rel': e.get('rel', 'related'),
              'count': 1} for e in g['edges']
             if e['a'] in subjects and e['b'] in subjects]
    for r in links['records']:
        if r['verdict'] == 'split_link':
            edges.append({'a': r['a'], 'b': r['b'],
                          'rel': 'bridge:' + r['relation'], 'count': 3,
                          'adj_id': r['id']})
    # loops for clickable constellations: resolve via (file, cid)
    node_of = {}
    for nid, s in subjects.items():
        for x in s['facets']:
            node_of[(x['chunk'], x['cid'])] = nid
    loops = []
    for path in sorted(glob.glob(os.path.join(BASE, 'extractions', 'weil_*.json'))):
        d = json.load(open(path))
        fname = os.path.basename(path)[:-5]
        for l in d.get('loops', []):
            nid = node_of.get((fname, l.get('concept_id')))
            if nid:
                loops.append({'chunk': fname, 'label': subjects[nid]['display'][:120],
                              'node': nid})
    return {'subjects': subjects, 'standalone': standalone, 'edges': edges,
            'loops': loops,
            'stats': {'subjects': len(subjects),
                      'cross_edges': len(links['cross_edges']),
                      'concepts': len(subjects)}}

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
    # gold bridge edges + role-difference labels at midpoints
    page = page.replace(
        "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : 'rgba(139,148,158,.16)';",
        "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : (e.rel.indexOf('bridge:')===0 ? 'rgba(255,215,0,.65)' : 'rgba(139,148,158,.16)');")
    page = page.replace(
        "      ctx.lineWidth = sel ? Math.min(3, .6+e.w*.5) : 1;",
        """      ctx.lineWidth = sel ? Math.min(3, .6+e.w*.5) : (e.rel.indexOf('bridge:')===0 ? 2.2 : 1);
      if (e.rel.indexOf('bridge:')===0){
        const mx=(cx+a.x*z+cx+b.x*z)/2, my=(cy+a.y*z+cy+b.y*z)/2;
        ctx.fillStyle='rgba(255,215,0,.85)'; ctx.font='10px sans-serif'; ctx.textAlign='center';
        ctx.fillText(e.rel.slice(7).replace(/-/g,' '), mx, my-5);
      }""")
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

if __name__ == '__main__':
    graph = build()
    render(graph, 'Atlas-6 — the Weil bridge map',
           'analytic (AF preprint · Bombieri 2000 · Groskin preprint) × relational (pilot Node 10a) · gold = adjudicated bridge links with role-differences labeled',
           os.path.join(BASE, 'atlas6_bridge.html'))
