#!/usr/bin/env python3
"""Atlas-8 money view: foreign sky vs home (circle-sieve) sky.

Dark background, two galaxy clusters, gold adjudicated split_link edges
with short role-difference labels. Static PNG (Android-safe).
"""
import json, math, os, random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BASE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(BASE, 'graphs', 'atlas8_raw.json')))
adj = json.load(open(os.path.join(BASE, 'atlas8_adjudications.json')))
nodes, edges = g['nodes'], g['edges']

COLORS = {'foreign': '#5b9bd5', 'home': '#70ad47'}
CENTERS = {'foreign': (0.30, 0.52), 'home': (0.70, 0.52)}

SHORT = {
    'A8-01': 'cited vs proved (S1)',
    'A8-02': 'proved lemma vs face reframing',
    'A8-03': 'proved inequality vs reframing',
    'A8-04': 'working weights vs reframing',
    'A8-05': 'diagonalization vs face form',
    'A8-06': 'Tauberian proof vs weight identity',
    'A8-09': 'tuples as engine vs as output',
    'A8-10': 'stipulated vs emergent',
    'A8-11': 'conjectured vs mechanism-only',
    'A8-12': 'proved proportion vs census',
    'A8-13': 'classical vs geometric sieve',
}

random.seed(8)
pos = {}
for nid, nd in nodes.items():
    cx, cy = CENTERS[nd['sky']]
    r = 0.17 * math.sqrt(random.random())
    th = random.random() * 2 * math.pi
    pos[nid] = (cx + r * math.cos(th) * 1.25, cy + r * math.sin(th))

fig, ax = plt.subplots(figsize=(17, 12))
fig.patch.set_facecolor('#141419')
ax.set_facecolor('#141419')
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

random.seed(12)
for e in random.sample(edges, min(len(edges), 500)):
    a, b = e['a'], e['b']
    if a in pos and b in pos:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1, x2], [y1, y2], color='#3a3a44', lw=0.4, alpha=0.5, zorder=1)

for sky in ('foreign', 'home'):
    xs = [pos[n][0] for n, d in nodes.items() if d['sky'] == sky]
    ys = [pos[n][1] for n, d in nodes.items() if d['sky'] == sky]
    ax.scatter(xs, ys, s=11, c=COLORS[sky], alpha=0.85, zorder=2, edgecolors='none')

for x in adj['adjudications']:
    if x['verdict'] != 'split_link':
        continue
    a, b = x['a'], x['b']
    if a not in pos or b not in pos:
        continue
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.plot([x1, x2], [y1, y2], color='#ffd700', lw=2.0, alpha=0.92, zorder=3)
    lab = SHORT.get(x['id'], '')
    if lab:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, lab, color='#ffd700', fontsize=8,
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.25', fc='#141419', ec='none', alpha=0.85),
                zorder=4)

ax.text(0.5, 0.965, 'Atlas-8 — prime distribution: literature vs the circle sieve  '
        '(gold = 11 adjudicated split_links; S1 control resolves)',
        color='white', fontsize=14.5, ha='center', va='center')
ax.text(0.5, 0.935, '4 of 5 crack candidates verify computationally — the sieve holds what the literature does not state',
        color='#9a9aa5', fontsize=10.5, ha='center', va='center')
ax.text(0.30, 0.06, 'FOREIGN · landmark prime literature\n(Zagier, Granville, Zhang, Maynard, Green–Tao, Elkies)',
        color='#5b9bd5', fontsize=10, ha='center', va='center')
ax.text(0.70, 0.06, 'HOME · circle-sieve sky\n(133 concepts, spans first-class)',
        color='#70ad47', fontsize=10, ha='center', va='center')

leg = [Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['foreign'],
              markersize=9, label='foreign sky (212 concepts)'),
       Line2D([0], [0], marker='o', color='w', markerfacecolor=COLORS['home'],
              markersize=9, label='home sky (133 concepts)'),
       Line2D([0], [0], color='#ffd700', lw=2.5, label='adjudicated split_link')]
l = ax.legend(handles=leg, loc='lower right', facecolor='#1e1e26',
              edgecolor='#3a3a44', fontsize=10)
for t in l.get_texts():
    t.set_color('white')

out = os.path.join(BASE, 'atlas8_money.png')
plt.savefig(out, dpi=110, facecolor=fig.get_facecolor(), bbox_inches='tight')
print('saved', out)
