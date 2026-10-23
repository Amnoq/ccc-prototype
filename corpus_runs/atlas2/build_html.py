#!/usr/bin/env python3
"""Build atlas2.html (foreign corpus view) and atlas2_cross.html (the money view:
combined pilot+foreign graph with the reviewed cross-corpus links as edges).

Shape conversion from merge_atlas2.py's atlas2_graph.json to what
atlas_template.html expects:
  GRAPH.subjects: {id: {display, status, facets:[{chunk,cid,label,kind,status,genre,note}], status_note, chunks, killed_facets}}
  GRAPH.standalone: [{id, display, status, chunk, kind, genre, note}]
  GRAPH.edges: [{a,b,rel,count}]
  GRAPH.stats: {subjects, cross_edges, concepts}
  GRAPH.loops: [{chunk, label}]
"""
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, '..', 'atlas', 'atlas_template.html')) as f:
    TEMPLATE = f.read()

def paper_of(chunk_file):
    """sierra_s2 -> sierra; the galaxy a node belongs to."""
    f = (chunk_file or '').split('/')[-1]
    return f.split('_s')[0] if '_s' in f else (f or 'misc')


def resolve_loops(g, prefix=''):
    """Resolve each open loop to its merged node id -> clickable constellation.
    Works on the raw graph dicts (subjects/standalone with facets carrying
    file|chunk + cid). Unresolvable loops keep node=None (listed, not clickable)."""
    idx = {}
    for sid, s in g['subjects'].items():
        for f in s.get('facets', []):
            key = (f.get('file') or f.get('chunk'), f.get('cid'))
            if key[0] and key[1]:
                idx.setdefault(key, prefix + sid)
    sa = g['standalone']
    items = sa.items() if isinstance(sa, dict) else [
        (s.get('id'), s) for s in sa if isinstance(s, dict)]
    for nid, s in items:
        for f in s.get('facets', []):
            key = (f.get('file') or f.get('chunk'), f.get('cid'))
            if key[0] and key[1]:
                idx.setdefault(key, prefix + nid)
    # node display labels for nicer loop titles
    labels = {}
    for sid, s in g['subjects'].items():
        labels[prefix + sid] = s.get('label', sid)
    for nid, s in items:
        labels[prefix + nid] = s.get('label', nid)
    out = []
    for l in g.get('loops', []):
        key = (l.get('file') or l.get('chunk'), l.get('cid') or l.get('ref'))
        nid = idx.get(key)
        out.append({'chunk': l.get('file') or l.get('chunk', '?'),
                    'label': (labels.get(nid) if nid else None)
                             or l.get('label') or l.get('subject', ''),
                    'node': nid})
    return out


def conv_foreign(g):
    subjects = {}
    for sid, s in g['subjects'].items():
        facs = s.get('facets', [])
        chunks = sorted({x.get('file','?') for x in facs})
        papers = [paper_of(x.get('file','')) for x in facs]
        cluster = max(set(papers), key=papers.count) if papers else 'misc'
        subjects[sid] = {
            'display': s.get('label', sid), 'status': s.get('status','heuristic'),
            'cluster': cluster,
            'facets': [{'chunk': x.get('file','?'), 'cid': x.get('cid',''),
                        'label': x.get('label',''), 'kind': x.get('kind',''),
                        'status': x.get('status','heuristic'),
                        'genre': x.get('genre'), 'note': x.get('note','')}
                       for x in facs],
            'status_note': None, 'chunks': chunks,
            'killed_facets': s.get('n_facets',0) - len(facs),
        }
    standalone = []
    sa = g['standalone']
    items = sa.values() if isinstance(sa, dict) else sa
    for s in items:
        facs = s.get('facets', [])
        f0 = facs[0] if facs else {}
        standalone.append({'id': s.get('id'), 'display': s.get('label', s.get('id')),
                           'status': s.get('status','heuristic'),
                           'cluster': paper_of(f0.get('file','')),
                           'chunk': f0.get('file','?'), 'kind': f0.get('kind',''),
                           'genre': f0.get('genre'), 'note': f0.get('note','')})
    edges = [{'a': e['a'], 'b': e['b'], 'rel': e.get('rel','related'),
              'count': e.get('count',1)} for e in g.get('edges', [])]
    loops = resolve_loops(g)
    st = g.get('stats', {})
    return {'subjects': subjects, 'standalone': standalone, 'edges': edges,
            'loops': loops,
            'stats': {'subjects': st.get('subjects', len(subjects)),
                      'cross_edges': len(edges),
                      'concepts': st.get('occurrences', 0)}}

def conv_pilot(p):
    subjects = {}
    for sid, s in p['subjects'].items():
        facs = s.get('facets', [])
        chunks = sorted({x.get('chunk','?') for x in facs})
        first = facs[0] if facs else {}
        subjects['p:'+sid] = {
            'display': first.get('label', sid)[:160], 'status': first.get('status','open'),
            'cluster': 'pilot',
            'facets': [{'chunk': 'PILOT:'+x.get('chunk','?'), 'cid': x.get('cid',''),
                        'label': x.get('label',''), 'kind': x.get('kind',''),
                        'status': x.get('status','open'), 'genre': x.get('genre'),
                        'note': x.get('note','')} for x in facs],
            'status_note': 'pilot-corpus node (foreign corpus is f:-namespaced)',
            'chunks': ['PILOT:'+c for c in chunks], 'killed_facets': 0}
    standalone = []
    for s in p.get('standalone', []) or []:
        if not isinstance(s, dict): continue
        standalone.append({'id': 'p:'+s.get('id'), 'display': s.get('display', s.get('id')),
                           'status': s.get('status') or 'open', 'cluster': 'pilot',
                           'chunk': 'PILOT:'+str(s.get('chunk','')),
                           'kind': s.get('kind',''), 'genre': s.get('genre'),
                           'note': s.get('note','')})
    edges = [{'a': 'p:'+e['a'], 'b': 'p:'+e['b'], 'rel': e.get('rel','related'),
              'count': e.get('count',1)} for e in p.get('edges', [])
             if 'p:'+e['a'] in subjects and 'p:'+e['b'] in subjects]
    return subjects, standalone, edges

def render(graph, title, subtitle, path):
    page = TEMPLATE.replace(
        '<title>Lemma Atlas — prime-distribution research program</title>',
        '<title>'+html.escape(title)+'</title>')
    page = page.replace('const GRAPH = /*__GRAPH__*/{};',
                        'const GRAPH = /*__GRAPH__*/' + json.dumps(graph, ensure_ascii=False) + ';')
    page = page.replace('<div class="title">Lemma Atlas</div>',
                        '<div class="title">'+html.escape(title)+'</div>', 1)
    page = page.replace(
        '<div class="sub">epistemic-status map of the prime-distribution research program · tap a node for detail · drag to pan, pinch/scroll to zoom</div>',
        '<div class="sub">'+html.escape(subtitle)+' · tap a node for detail · drag to pan, pinch/scroll to zoom</div>', 1)
    # --- universe-of-thought layout: clustered galaxies, edges visible ---
    # 1. thread cluster through node construction
    page = page.replace(
        "r: 7 + Math.min(13, Math.sqrt(s.facets.length) * 4), subject:true });",
        "r: 7 + Math.min(13, Math.sqrt(s.facets.length) * 4), subject:true, cluster:s.cluster||'misc' });")
    page = page.replace(
        "note:null, chunks:[s.chunk], killedFacets:0, r:4.5, subject:false });",
        "note:null, chunks:[s.chunk], killedFacets:0, r:4.5, subject:false, cluster:s.cluster||'misc' });")
    # 2. cluster-aware init: galaxies on a ring, golden-spiral fill
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
    # 3. gentle gravity toward each node's galaxy center
    page = page.replace(
        "a.vx += -a.x*0.004; a.vy += -a.y*0.004;",
        """a.vx += -a.x*0.004; a.vy += -a.y*0.004;
    const cc = clusterC[a.cluster||'misc'];
    if (cc){ a.vx += (cc.x-a.x)*0.03; a.vy += (cc.y-a.y)*0.03; }""")
    # 4. edges visible by default — relations are the picture
    page = page.replace(
        '<input type="checkbox" id="f-edges">',
        '<input type="checkbox" id="f-edges" checked>')
    # 5. cross-corpus bridges drawn gold
    page = page.replace(
        "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : 'rgba(139,148,158,.16)';",
        "ctx.strokeStyle = sel ? 'rgba(230,237,243,.5)' : (e.rel.indexOf('cross:')===0 ? 'rgba(255,215,0,.6)' : 'rgba(139,148,158,.16)');")
    # 6. open loops become clickable constellations (select node + relations)
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
    print('wrote', path, len(page)//1024, 'KB')

def main():
    with open(os.path.join(BASE, 'atlas2_graph.json')) as f:
        fg = json.load(f)
    fview = conv_foreign(fg)
    render(fview, 'Atlas-2 — foreign literature corpus',
           '8 analytic-number-theory papers, extracted blind',
           os.path.join(BASE, 'atlas2.html'))

    # ---- money view: combined pilot + foreign, cross links as edges ----
    with open(os.path.join(BASE, '..', 'atlas', 'atlas_graph.json')) as f:
        pg = json.load(f)
    psubs, pstand, pedges = conv_pilot(pg)
    fsubs = {'f:'+k: dict(v) for k, v in fview['subjects'].items()}
    fstand = [dict(s, id='f:'+s['id']) for s in fview['standalone']]
    fedges = [dict(e, a='f:'+e['a'], b='f:'+e['b']) for e in fview['edges']]
    # remap foreign edges that touch merged subjects — both namespaces already merged internally
    with open(os.path.join(BASE, 'cross_corpus_links.json')) as f:
        links = json.load(f)['records']
    xedges = []
    for r in links:
        if not r['pilot']: continue
        xedges.append({'a': 'f:'+r['foreign'], 'b': 'p:'+r['pilot'],
                       'rel': 'cross:%s:%s' % (r['verdict'], r['relation'] or '-'),
                       'count': 1})
    subjects = {**fsubs, **psubs}
    standalone = fstand + pstand
    edges = fedges + pedges + xedges
    ploops = resolve_loops(pg, 'p:')
    floops = resolve_loops(fg, 'f:')
    graph = {'subjects': subjects, 'standalone': standalone, 'edges': edges,
             'loops': floops + ploops,
             'stats': {'subjects': len(subjects), 'cross_edges': len(xedges),
                       'concepts': fview['stats']['concepts'] + pg.get('stats',{}).get('concepts',0)}}
    render(graph, 'Atlas-2 money view — pilot × foreign, cross-corpus links',
           'f: = foreign literature · p: = pilot program · cross: = reviewed resolutions',
           os.path.join(BASE, 'atlas2_cross.html'))

if __name__ == '__main__':
    main()
