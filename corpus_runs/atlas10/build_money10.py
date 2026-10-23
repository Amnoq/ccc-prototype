#!/usr/bin/env python3
"""Atlas-10 money view: theory vs annotations vs engine skies.

Dark background, three galaxy clusters, gold adjudicated split_link
edges with short labels. Static PNG (Android-safe)."""
import json, math, os, random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BASE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, os.path.expanduser('~/workspace/ccc-prototype/.venv/lib/python3.12/site-packages'))
g = json.load(open(os.path.join(BASE, 'graphs', 'atlas10_merged.json')))
adj = json.load(open(os.path.join(BASE, 'atlas10_adjudications.json')))
nodes, edges = g['nodes'], g['edges']

COLORS = {'theory': '#5b9bd5', 'annotations': '#b57edc',
          'engine': '#70ad47'}
CENTERS = {'theory': (0.28, 0.55), 'annotations': (0.72, 0.55),
           'engine': (0.50, 0.22)}

SHORT = {
    'A10-01': 'C1: book rule vs engine mate-in-2',
    'A10-02': 'C2: "or resigning" vs mate-in-8',
    'A10-03': 'Q+K bound vs mate-in-1',
    'A10-04': 'R+K bound vs mate-in-1',
    'A10-05': 'doubled pawns: defect vs asset',
    'A10-06': 'gambit: used vs defined',
    'A10-07': 'McCutcheon: asserted vs open',
}

random.seed(10)
pos = {}
for nid, nd in nodes.items():
    cx, cy = CENTERS[nd['sky']]
    r = 0.15 * math.sqrt(random.random())
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
        ax.plot([x1, x2], [y1, y2], color='#3a3a44', lw=0.4, alpha=0.5,
                zorder=1)

for sky in ('theory', 'annotations', 'engine'):
    xs = [pos[n][0] for n, d in nodes.items() if d['sky'] == sky]
    ys = [pos[n][1] for n, d in nodes.items() if d['sky'] == sky]
    ax.scatter(xs, ys, s=11, c=COLORS[sky], alpha=0.85, zorder=2,
               edgecolors='none')

for x in adj:
    if x['verdict'] != 'split_link':
        continue
    a, b = x['a'], x['b']
    if a not in pos or b not in pos:
        continue
    (x1, y1), (x2, y2) = pos[a], pos[b]
    ax.plot([x1, x2], [y1, y2], color='#ffd700', lw=2.2, alpha=0.92,
            zorder=3)
    lab = SHORT.get(x['id'], '')
    if lab:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, lab, color='#ffd700',
                fontsize=7.5, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.25', fc='#141419',
                          ec='none', alpha=0.85), zorder=4)

counts = {s: sum(1 for d in nodes.values() if d['sky'] == s)
          for s in COLORS}
ax.text(0.5, 0.965, 'Atlas-10 — chess: theory vs annotations vs engine  '
        '(gold = 7 adjudicated split_links; both controls resolve)',
        color='white', fontsize=14, ha='center', va='center')
ax.text(0.5, 0.935, '2 of 2 crack candidates verify — the annotators\' '
        'judgments are directionally sound against Stockfish 17.1',
        color='#9a9aa5', fontsize=10.5, ha='center', va='center')
ax.text(0.28, 0.06, f"THEORY · Capablanca + Lasker\n({counts['theory']} concepts)",
        color='#5b9bd5', fontsize=10, ha='center', va='center')
ax.text(0.72, 0.06, f"ANNOTATIONS · Blue Book games\n({counts['annotations']} concepts)",
        color='#b57edc', fontsize=10, ha='center', va='center')
ax.text(0.50, 0.015, f"ENGINE · Stockfish 17.1 ({counts['engine']} concepts)",
        color='#70ad47', fontsize=10, ha='center', va='center')

leg = [Line2D([0], [0], marker='o', color='w',
              markerfacecolor=COLORS[s], markersize=9,
              label=f'{s} sky ({counts[s]})') for s in COLORS] + \
      [Line2D([0], [0], color='#ffd700', lw=2.5,
              label='adjudicated split_link')]
l = ax.legend(handles=leg, loc='lower right', facecolor='#1e1e26',
              edgecolor='#3a3a44', fontsize=10)
for t in l.get_texts():
    t.set_color('white')

out = os.path.join(BASE, 'atlas10_money.png')
plt.savefig(out, dpi=110, facecolor=fig.get_facecolor(),
            bbox_inches='tight')
print('saved', out)
