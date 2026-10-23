#!/usr/bin/env python3
"""Atlas-10 merge application: applies pass1_review.json verdicts
(keyed on STABLE node-id pairs, not positional indices) to
graphs/atlas10_loaded.json -> graphs/atlas10_merged.json."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(BASE, 'graphs', 'atlas10_loaded.json')))
nodes, edges = g['nodes'], g['edges']
review = json.load(open(os.path.join(BASE, 'pass1_review.json')))['verdicts']

# validate every reviewed id exists (fail loudly on stale refs)
all_ids = set(nodes)
for r in review:
    for k in ('a', 'b'):
        assert r[k] in all_ids, f"STALE REVIEW REF: {r[k][:70]}"

parent = {nid: nid for nid in nodes}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra

for r in review:
    if r['v'] == 'merge':
        union(r['a'], r['b'])

groups = {}
for nid in nodes:
    groups.setdefault(find(nid), []).append(nid)

merged_nodes, alias = {}, {}
for root, members in groups.items():
    if len(members) == 1:
        merged_nodes[root] = nodes[root]
        continue
    members.sort(key=lambda m: len(nodes[m]['label']), reverse=True)
    prim = nodes[members[0]]
    notes = ' // '.join(f"[{nodes[m]['file']}:{nodes[m]['cid']}] {nodes[m]['note'][:200]}"
                        for m in members if nodes[m]['note'])
    merged_nodes[root] = dict(prim)
    merged_nodes[root]['merged_from'] = members
    merged_nodes[root]['note'] = notes[:1200]
    for m in members:
        alias[m] = root

new_edges = []
for e in edges:
    a, b = alias.get(e['a'], e['a']), alias.get(e['b'], e['b'])
    if a == b:
        continue
    new_edges.append({'a': a, 'b': b, 'rel': e['rel'], 'note': e['note']})

n_merged = sum(1 for v in groups.values() if len(v) > 1)
print(f'{len(nodes)} -> {len(merged_nodes)} nodes '
      f'({n_merged} merged groups), {len(new_edges)} edges')
weak = [f"{r['a'][:40]}+{r['b'][:40]}" for r in review
        if r['v'] == 'merge' and r.get('weak')]
print('weak merges flagged:', weak)
json.dump({'nodes': merged_nodes, 'edges': new_edges,
           'review': review},
          open(os.path.join(BASE, 'graphs', 'atlas10_merged.json'), 'w'))
