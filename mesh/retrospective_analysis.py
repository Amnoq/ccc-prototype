#!/usr/bin/env python3
"""MESH-5 gate: retrospective — does D-wire record connectivity predict
human fidelity grades? Run: python3 retrospective_analysis.py
Outputs: printed tables + mesh/CONNECTIVITY_RETROSPECTIVE_DATA.json
"""
import json, re, math, random
from collections import Counter, defaultdict

BASE = '/home/hatch/workspace/ccc-prototype'
random.seed(20261008)

STOP = set("""the a an of to in and or for on with is are was were be by as at
from that this it its into than then so such no not are has have had but
which who whose when where what how why can could should would may might
must will shall do does did done being been over under between through
during before after above below up down out off again further once here
there all any both each few more most other some only own same too very
just don now per via e g i ie etc""".split())

def toks(s):
    return [t for t in re.findall(r'[a-z0-9]+', (s or '').lower()) if t not in STOP and len(t) > 2]

# ---------- 1. load wires: records + links (chunk-scoped) ----------
records = {}   # (chunk, id) -> dict
links = []     # (chunk, from, rel, to)
for c in range(1, 13):
    cn = f"c{c:02d}"
    raw = open(f'{BASE}/ccc2/wires/{cn}.wire').read()
    w = json.loads(raw.split('TELOMERE-CCC2-1:')[1].rsplit(':TELOMERE-CCC2-1', 1)[0])
    for r in w['records']:
        if r['type'] == 'L':
            links.append((cn, r['from'], r['rel'], r['to']))
        else:
            # full record text: D-items carry content in rule/generates/verified,
            # not just subtitle — dump everything except bookkeeping fields
            parts = []
            for k, v in r.items():
                if k in ('id', 'type', 'checksum'):
                    continue
                parts.append(json.dumps(v))
            text = ' '.join(parts)
            records[(cn, r['id'])] = {'type': r['type'], 'text': text,
                                      'label': r.get('honest_label') or r.get('status', '')}

# ---------- 2. load human grades ----------
probes = []  # (chunk, pid, score, miss_note)
for c in range(1, 13):
    cn = f"c{c:02d}"
    g = json.load(open(f'{BASE}/corpus_runs/r5/rescore_v7/{cn}.json'))
    miss = {m['id']: m.get('note', '') for m in g.get('misses', [])}
    for p in g['probes']:
        probes.append({'chunk': cn, 'pid': p['id'], 'score': p['score'],
                       'miss_note': miss.get(p['id'], '')})

# ---------- 3. load judge claim texts (mapping bridge) + Arm B labels ----------
claims = defaultdict(list)   # (chunk,pid) -> [claim texts]
blabels = defaultdict(list)  # (chunk,pid) -> [arm_b labels]
for j in range(1, 5):
    for c in range(1, 13):
        cn = f"c{c:02d}"
        try:
            jd = json.load(open(f'{BASE}/step4/judge_outputs/j{j}/{cn}.json'))
        except FileNotFoundError:
            continue
        for item in jd:
            pid = item['probe_id'].split('-')[1]
            b = item.get('arm_b') or {}
            if b.get('claim'):
                claims[(cn, pid)].append(b['claim'])
            if b.get('label'):
                blabels[(cn, pid)].append(b['label'])

# ---------- 4. probe -> record mapping (chunk-scoped content overlap) ----------
def overlap(a_toks, b_counter):
    return sum(1 for t in a_toks if b_counter.get(t, 0) > 0)

mapping = {}   # (chunk,pid) -> [(rec_id, score)]
unmapped = []
for p in probes:
    key = (p['chunk'], p['pid'])
    qtext = ' '.join(claims.get(key, [])) + ' ' + p['miss_note']
    qt = toks(qtext)
    if not qt:
        unmapped.append(key); continue
    cands = []
    for (cn, rid), r in records.items():
        if cn != p['chunk']:
            continue
        rc = Counter(toks(r['text']))
        ov = overlap(qt, rc)
        # normalize by geometric mean of lengths to avoid long-record bias
        denom = math.sqrt(len(qt) * max(1, sum(rc.values())))
        cands.append((ov / denom if denom else 0, ov, rid))
    cands.sort(reverse=True)
    best, best_raw, brid = cands[0]
    # threshold: need at least 2 content-token overlap AND normalized > 0.05
    if best_raw >= 2 and best > 0.05:
        # take all within 80% of best (multi-map), cap 3
        mapped = [(rid, s) for s, raw_ov, rid in cands[:3] if s >= 0.8 * best]
        mapping[key] = mapped
    else:
        unmapped.append(key)

# ---------- 5. metrics (DEFINED BEFORE COMPUTING) ----------
SUPPORT = {'supports', 'implements', 'exemplifies', 'refines'}
CONTRADICT = {'contradicts'}

indeg = Counter(); outdeg = Counter()
in_sup = Counter(); in_con = Counter()
outdeg_src = Counter()
chunk_links = Counter()
for cn, fr, rel, to in links:
    chunk_links[cn] += 1
    outdeg[(cn, fr)] += 1
    indeg[(cn, to)] += 1
    outdeg_src[(cn, fr)] += 1
    if rel in SUPPORT:
        in_sup[(cn, to)] += 1
    if rel in CONTRADICT:
        in_con[(cn, to)] += 1

def metrics(cn, rid):
    key = (cn, rid)
    tot = indeg[key] + outdeg[key]
    m1 = tot
    m2 = indeg[key]
    m3 = in_sup[key] - in_con[key]
    # M4: independence-weighted in-support: sum 1/outdeg(source)
    m4 = 0.0
    for (lcn, fr, rel, to) in links:
        if lcn == cn and to == rid and rel in SUPPORT:
            m4 += 1.0 / max(1, outdeg_src[(lcn, fr)])
    m5 = tot / max(1, chunk_links[cn])
    return {'M1_total_degree': m1, 'M2_in_degree': m2,
            'M3_support_minus_contradict': m3,
            'M4_indep_weighted_support': round(m4, 3),
            'M5_relative_share': round(m5, 3)}

METRIC_NAMES = ['M1_total_degree', 'M2_in_degree', 'M3_support_minus_contradict',
                'M4_indep_weighted_support', 'M5_relative_share']

# ---------- 6. per-probe aggregation ----------
rows = []
for p in probes:
    key = (p['chunk'], p['pid'])
    ms = mapping.get(key)
    if not ms:
        continue
    agg = {}
    for mn in METRIC_NAMES:
        vals = [metrics(p['chunk'], rid)[mn] for rid, _ in ms]
        agg[mn] = sum(vals) / len(vals)
        agg[mn + '_max'] = max(vals)
    # modal judge label
    labs = blabels.get(key, [])
    modal = Counter(labs).most_common(1)[0][0] if labs else None
    rows.append({'probe': key, 'grade': p['score'], 'n_mapped': len(ms),
                 'modal_label': modal, **agg})

# ---------- 7. correlations + permutation null ----------
def spearman(xs, ys):
    n = len(xs)
    rx = _rank(xs); ry = _rank(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0

def _rank(xs):
    s = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and xs[s[j + 1]] == xs[s[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[s[k]] = avg
        i = j + 1
    return r

def perm_p(xs, ys, n_perm=10000):
    obs = abs(spearman(xs, ys))
    cnt = 0
    ys = list(ys)
    for _ in range(n_perm):
        random.shuffle(ys)
        if abs(spearman(xs, ys)) >= obs:
            cnt += 1
    return (cnt + 1) / (n_perm + 1), obs

grades = [r['grade'] for r in rows]
print(f"=== MESH-5 retrospective: connectivity vs human grades ===")
print(f"probes total: {len(probes)}, mapped: {len(rows)}, unmapped: {len(unmapped)}")
print(f"grade distribution (mapped): {dict(Counter(grades))}")
print(f"\nlink graph: {len(records)} records, {len(links)} links "
      f"({len(links)/len(records):.2f} links/record)")
print(f"records with degree 0: {sum(1 for k in records if indeg[k]+outdeg[k]==0)}/{len(records)}")
print(f"\nrel vocabulary in data: {dict(Counter(rel for _,_,rel,_ in links))}")
print("NOTE: zero 'contradicts' links in the data — M3 reduces to in_support.")

results = {}
for mn in METRIC_NAMES:
    xs = [r[mn] for r in rows]
    p, obs = perm_p(xs, grades)
    # group means
    g1 = [x for x, gr in zip(xs, grades) if gr == 1.0]
    g05 = [x for x, gr in zip(xs, grades) if gr < 1.0]
    results[mn] = {'spearman': round(obs if spearman(xs, grades) >= 0 else -obs, 3)
                   if False else round(spearman(xs, grades), 3),
                   'perm_p': round(p, 4),
                   'mean_grade1': round(sum(g1)/len(g1), 3) if g1 else None,
                   'mean_grade_sub1': round(sum(g05)/len(g05), 3) if g05 else None,
                   'n1': len(g1), 'nsub1': len(g05)}
    print(f"{mn}: spearman={results[mn]['spearman']:+.3f} perm_p={p:.4f} "
          f"mean|grade=1.0: {results[mn]['mean_grade1']} (n={len(g1)}) "
          f"mean|grade<1.0: {results[mn]['mean_grade_sub1']} (n={len(g05)})")

# sensitivity: max instead of mean
print("\nsensitivity (max of mapped records instead of mean):")
for mn in METRIC_NAMES:
    xs = [r[mn + '_max'] for r in rows]
    p, _ = perm_p(xs, grades)
    print(f"{mn}_max: spearman={spearman(xs, grades):+.3f} perm_p={p:.4f}")

# ---------- 8. secondary: connectivity vs judge labels ----------
print("\n=== secondary: metric by modal Arm-B judge label ===")
by_label = defaultdict(list)
for r in rows:
    if r['modal_label']:
        by_label[r['modal_label']].append(r)
for lab in sorted(by_label):
    rs = by_label[lab]
    m1s = [x['M1_total_degree'] for x in rs]
    m3s = [x['M3_support_minus_contradict'] for x in rs]
    print(f"{lab}: n={len(rs)} mean_M1={sum(m1s)/len(m1s):.2f} mean_M3={sum(m3s)/len(m3s):.2f}")

# judge-label coverage note: each probe was judged by exactly ONE judge
# (4 judges x 30 probes = 120), so "modal" = that judge's label; there is
# no inter-judge agreement to measure. Stated, not hidden.
n_judges_per_probe = Counter(len(set(v)) for v in blabels.values())
print(f"labels-per-probe distribution: {dict(n_judges_per_probe)} "
      f"(each probe judged once -> modal is trivial)")

# ---------- 8b. THE calibration question: within QUEUE-actioned probes,
# does connectivity separate human-1.0 (wrongly queued) from human-0.5
# (correctly queued)? Tier mapping per COLLAPSE_SPEC.md v1.
TIER = {'exact': 'ACT', 'computationally_verified': 'ACT',
        'conjectural': 'QUEUE', 'heuristic': 'SURFACE',
        'killed': 'BLOCK', 'superseded': 'FOLLOW_HEIR', 'unstated': 'NO_ACTION'}
queued_rows = [r for r in rows
               if r['modal_label'] and TIER.get(r['modal_label']) in ('QUEUE', 'SURFACE')]
q_right = [r for r in queued_rows if r['grade'] < 1.0]   # correctly queued
q_wrong = [r for r in queued_rows if r['grade'] == 1.0]   # wrongly queued (delayed)
print(f"\n=== QUEUE-tier sorting: correctly queued (grade<1.0) vs wrongly queued (grade=1.0) ===")
print(f"queued probes mapped: {len(queued_rows)} (correct: {len(q_right)}, wrong: {len(q_wrong)})")
for mn in METRIC_NAMES:
    a = [r[mn] for r in q_right]; b = [r[mn] for r in q_wrong]
    ma = sum(a) / len(a) if a else None
    mb = sum(b) / len(b) if b else None
    # Mann-Whitney U (two-sided) via rank sums
    if a and b:
        xs = [(x, 0) for x in a] + [(x, 1) for x in b]
        xs.sort(key=lambda t: t[0])
        rsum = [0.0, 0.0]; ns = [len(a), len(b)]
        i = 0
        while i < len(xs):
            j = i
            while j + 1 < len(xs) and xs[j+1][0] == xs[i][0]: j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j+1): rsum[xs[k][1]] += avg
            i = j + 1
        u1 = rsum[0] - ns[0]*(ns[0]+1)/2
        # normal approx
        mu = ns[0]*ns[1]/2; sd = math.sqrt(ns[0]*ns[1]*(ns[0]+ns[1]+1)/12)
        z = (u1 - mu) / sd if sd else 0
        p_mw = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    else:
        p_mw = None
    pstr = f"{p_mw:.4f}" if p_mw is not None else "n/a"
    print(f"{mn}: correctly-queued mean={ma} (n={len(a)}) vs "
          f"wrongly-queued mean={mb} (n={len(b)}) MW p={pstr}")

# ---------- 9. save ----------
json.dump({'n_probes': len(probes), 'n_mapped': len(rows),
           'unmapped': [f"{c}-{p}" for c, p in unmapped],
           'mapping': {f"{c}-{p}": [rid for rid, _ in v] for (c, p), v in mapping.items()},
           'results': results,
           'rows': [{'probe': f"{c}-{p}", 'grade': r['grade'],
                     'modal_label': r['modal_label'],
                     **{m: r[m] for m in METRIC_NAMES}}
                    for r in rows for (c, p) in [r['probe']]]},
          open(f'{BASE}/mesh/CONNECTIVITY_RETROSPECTIVE_DATA.json', 'w'), indent=1)
print("\nsaved mesh/CONNECTIVITY_RETROSPECTIVE_DATA.json")
