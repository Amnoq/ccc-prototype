#!/usr/bin/env python3
"""Atlas-7 illustration: BSD skies.

Adapts the Atlas-6 build technique (read-only atlas_template.html +
render-time string patches): sky-clustered galaxy layout, gold
adjudicated split_link edges with adj_id labels at midpoints, clickable
loop-constellations. Produces per-sky views + the money view.
"""
import json, os, html, glob

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, '..', 'atlas', 'atlas_template.html')) as f:
    TEMPLATE = f.read()

CLUSTER_NAMES = {
    'an1': 'analytic · Shu–Yin explicit Gross–Zagier (arXiv:1708.05266)',
    'al1': 'algebraic · Sweeting Kolyvagin systems (arXiv:2012.11771)',
    'c1': 'computational · Fisher 6/12-descent (arXiv:0711.3774)',
    'c2': 'computational · Elkies–Klagsbrun rank records (arXiv:2003.00077)',
}
SKY_OF = {'an1': 'analytic', 'al1': 'algebraic', 'c1': 'computational',
          'c2': 'computational'}


def build(skies=None):
    g = json.load(open(os.path.join(BASE, 'graphs', 'atlas7_merged.json')))
    adj = json.load(open(os.path.join(BASE, 'atlas7_adjudications.json')))
    nodes = g['nodes']
    keep = lambda nid: (skies is None) or (nodes[nid]['sky'] in skies)
    subjects, standalone = {}, []
    ghost = set()
    if skies is not None:
        for x in adj['adjudications']:
            if x['verdict'] != 'split':
                continue
            sa, sb = nodes[x['a']]['sky'], nodes[x['b']]['sky']
            if (sa in skies) != (sb in skies):
                ghost.add(x['b'] if sa in skies else x['a'])
    for nid, n in nodes.items():
        if 'merged_into' in n:
            continue
        if not keep(nid) and nid not in ghost:
            continue
        subjects[nid] = {
            'display': n['label'], 'status': n['status'],
            'cluster': CLUSTER_NAMES[n['paper']] +
                       (' · (bridge counterpart)' if nid in ghost else ''),
            'status_note': 'bridge counterpart from another sky' if nid in ghost else None,
            'facets': [{'chunk': n['file'], 'cid': n['cid'], 'label': n['label'],
                         'kind': n['kind'], 'status': n['status'],
                         'genre': n['genre'], 'note': n['note']}],
            'chunks': [n['file']], 'killed_facets': 0}
    edges = [{'a': e['a'], 'b': e['b'], 'rel': e.get('rel', 'related'),
              'count': 1} for e in g['edges']
             if e['a'] in subjects and e['b'] in subjects]
    for x in adj['adjudications']:
        if x['verdict'] == 'split' and x['a'] in subjects and x['b'] in subjects:
            if skies is not None and not (nodes[x['a']]['sky'] in skies or
                                          nodes[x['b']]['sky'] in skies):
                continue
            edges.append({'a': x['a'], 'b': x['b'],
                          'rel': 'bridge:' + x['id'], 'count': 3,
                          'role': x.get('role_difference') or ''})
    node_of = {}
    for nid, s in subjects.items():
        for x in s['facets']:
            node_of[(x['chunk'], x['cid'])] = nid
    loops = []
    for path in sorted(glob.glob(os.path.join(BASE, 'extractions', '*_p*.json'))):
        d = json.load(open(path))
        fname = os.path.basename(path)[:-5]
        for l in d.get('loops', []):
            nid = node_of.get((fname, l.get('concept_id')))
            if nid:
                loops.append({'chunk': fname,
                              'label': subjects[nid]['display'][:120],
                              'node': nid})
    return {'subjects': subjects, 'standalone': standalone, 'edges': edges,
            'loops': loops,
            'stats': {'subjects': len(subjects),
                      'cross_edges': sum(1 for e in edges
                                         if e['rel'].startswith('bridge:')),
                      'concepts': len(subjects)}}


def bridge_legend():
    adj = json.load(open(os.path.join(BASE, 'atlas7_adjudications.json')))
    rows = []
    for x in adj['adjudications']:
        if x['verdict'] != 'split':
            continue
        rows.append(
            f"<div class='bridge'><b>{html.escape(x['id'])}</b> "
            f"({html.escape(x['pair'])}) — "
            f"{html.escape(x['role_difference'] or x['relation'])}</div>")
    return ('<div id="bridgelegend" style="position:fixed;right:12px;bottom:12px;'
            'max-width:380px;max-height:40vh;overflow:auto;background:rgba(13,17,23,.92);'
            'border:1px solid #30363d;border-radius:8px;padding:10px 12px;'
            'font-size:11px;color:#c9d1d9;z-index:5">'
            '<b style="color:#ffd700">Adjudicated bridge links</b>' +
            ''.join(rows) + '</div>')


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
    page = page.replace(
        "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : 'rgba(139,148,158,.16)';",
        "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : (e.rel.indexOf('bridge:')===0 ? 'rgba(255,215,0,.65)' : 'rgba(139,148,158,.16)');")
    page = page.replace(
        "      ctx.lineWidth = sel ? Math.min(3, .6+e.w*.5) : 1;",
        """      ctx.lineWidth = sel ? Math.min(3, .6+e.w*.5) : (e.rel.indexOf('bridge:')===0 ? 2.2 : 1);
      if (e.rel.indexOf('bridge:')===0){
        const mx=(cx+a.x*z+cx+b.x*z)/2, my=(cy+a.y*z+cy+b.y*z)/2;
        ctx.fillStyle='rgba(255,215,0,.9)'; ctx.font='bold 11px sans-serif'; ctx.textAlign='center';
        ctx.fillText(e.rel.slice(7), mx, my-6);
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
    page = page.replace('</body>', bridge_legend() + '\n</body>')
    with open(path, 'w') as f:
        f.write(page)
    print('wrote', path, len(page) // 1024, 'KB')


if __name__ == '__main__':
    views = [
        (None, 'atlas7_money.html', 'Atlas-7 — the money view',
         'all three BSD skies · gold = adjudicated split_links with role-differences in the legend'),
        ({'analytic'}, 'atlas7_analytic.html', 'Atlas-7 — analytic sky',
         'Shu–Yin explicit Gross–Zagier · gold = links out to other skies'),
        ({'algebraic'}, 'atlas7_algebraic.html', 'Atlas-7 — algebraic sky',
         'Sweeting Kolyvagin systems · gold = links out to other skies'),
        ({'computational'}, 'atlas7_computational.html', 'Atlas-7 — computational sky',
         'Fisher 6/12-descent × Elkies–Klagsbrun rank records · gold = links out to other skies'),
    ]
    for skies, fname, title, sub in views:
        render(build(skies), title, sub, os.path.join(BASE, fname))
