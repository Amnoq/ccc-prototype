#!/usr/bin/env python3
"""Step 4 demonstration: three-arm analysis.
Collapse is MECHANICAL per COLLAPSE_SPEC.md v1. Arm C shuffle is
seeded (seed=42), single pre-registered draw. No tuning.
"""
import json, glob, hashlib, random, os, sys
from collections import Counter, defaultdict

STEP4 = '/home/hatch/workspace/ccc-prototype/step4'
RESCORE = '/home/hatch/workspace/ccc-prototype/corpus_runs/r5/rescore_v7'

COLLAPSE = {
    'exact': 'ACT',
    'computationally_verified': 'ACT',   # spot-check noted; counts as ACT
    'conjectural': 'QUEUE',
    'heuristic': 'SURFACE',
    'killed': 'BLOCK',
    'superseded': 'MALFORMED',          # not emittable; flagged if seen
    'unstated': 'NO ACTION',
}
ALLOWED_LABELS = set(COLLAPSE) - {'superseded'}

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))

def checksum_packet(pkt):
    body = {k: v for k, v in pkt.items() if k != 'packet_checksum'}
    return hashlib.sha256(canon(body).encode()).hexdigest()

# ---- load judge outputs ----
judgments = {}  # probe_id -> {arm_a, arm_b{...}}
for f in sorted(glob.glob(f'{STEP4}/judge_outputs/j*/*.json')):
    for rec in json.load(open(f)):
        pid = rec['probe_id']
        assert pid not in judgments, f'duplicate {pid} in {f}'
        judgments[pid] = rec

print(f'judged probes: {len(judgments)}')
assert len(judgments) == 120, f'expected 120, got {len(judgments)}'

# validate
bad = []
for pid, rec in judgments.items():
    if rec['arm_a'] not in ('faithful', 'unfaithful'):
        bad.append((pid, 'arm_a', rec['arm_a']))
    lab = rec['arm_b']['label']
    if lab not in ALLOWED_LABELS:
        bad.append((pid, 'label', lab))
    for k in ('claim', 'span', 'boundary'):
        if k not in rec['arm_b']:
            bad.append((pid, 'missing', k))
if bad:
    print('VALIDATION FAILURES:', bad); sys.exit(1)
print('validation: all 120 probes well-formed')

# ---- ground truth (human grades; judges were blind to these) ----
truth = {}
for f in sorted(glob.glob(f'{RESCORE}/c*.json')):
    if 'control' in f:
        continue
    d = json.load(open(f))
    chunk = d['chunk']
    for p in d['probes']:
        truth[f'{chunk}-{p["id"]}'] = p['score']
assert len(truth) == 120 and set(truth) == set(judgments), 'truth/judgment id mismatch'
print('ground truth loaded:', Counter(truth.values()))

# ---- arms ----
def collapse_action(label):
    return COLLAPSE[label]

results = {}  # pid -> {A_action, B_label, B_action, C_label, C_action}
b_labels = []
for pid in sorted(judgments):
    rec = judgments[pid]
    a_action = 'ACT' if rec['arm_a'] == 'faithful' else 'NO ACT'
    b_label = rec['arm_b']['label']
    b_labels.append(b_label)
    results[pid] = {
        'A_action': a_action,
        'B_label': b_label,
        'B_action': collapse_action(b_label),
    }

# Arm C: seeded shuffle of B labels, then mechanical collapse
rng = random.Random(42)
shuffled = b_labels[:]
rng.shuffle(shuffled)
for pid, clab in zip(sorted(judgments), shuffled):
    results[pid]['C_label'] = clab
    results[pid]['C_action'] = collapse_action(clab)

# add checksums to packets (spec compliance; judges emitted fields)
for pid, rec in judgments.items():
    pkt = {
        'format': 'verdict-packet/1',
        'claim': rec['arm_b']['claim'],
        'label': rec['arm_b']['label'],
        'span': rec['arm_b']['span'],
        'boundary': rec['arm_b']['boundary'],
        'record_ref': f'v7-wire:{pid}',
    }
    rec['arm_b']['packet_checksum'] = checksum_packet(pkt)

# ---- metrics ----
def metrics(arm):
    fa = ma = q = 0
    dist = Counter()
    for pid, r in results.items():
        act = r[f'{arm}_action']
        dist[act] += 1
        h = truth[pid]
        is_act = (act == 'ACT')
        if is_act and h in (0.0, 0.5):
            fa += 1
        if not is_act and h == 1.0:
            ma += 1
        if act == 'QUEUE':
            q += 1
    return {'false_auto': fa, 'missed': ma, 'queued': q,
            'review_load': q / 120, 'dist': dict(dist)}

M = {arm: metrics(arm) for arm in ('A', 'B', 'C')}
for arm in ('A', 'B', 'C'):
    m = M[arm]
    print(f"Arm {arm}: false_auto={m['false_auto']} missed={m['missed']} "
          f"queued={m['queued']} review_load={m['review_load']:.3f} dist={m['dist']}")

# ---- token costs (tiktoken cl100k_base, marginal output cost per decision) ----
try:
    import tiktoken
    enc = tiktoken.get_encoding('cl100k_base')
    ta = [len(enc.encode(judgments[pid]['arm_a'])) for pid in judgments]
    tb = [len(enc.encode(canon(judgments[pid]['arm_b']))) for pid in judgments]
    import statistics as st
    print(f"Arm A marginal tokens/decision: mean={st.mean(ta):.1f}")
    print(f"Arm B packet tokens/decision: mean={st.mean(tb):.1f} "
          f"p90={sorted(tb)[int(0.9*len(tb))]} max={max(tb)}")
    tok = {'A_mean': st.mean(ta), 'B_mean': st.mean(tb),
           'B_p90': sorted(tb)[int(0.9*len(tb))], 'B_max': max(tb)}
except ImportError:
    print('tiktoken unavailable — token costs skipped')
    tok = None

# ---- decision rule (pre-registered operationalization) ----
faA, maA = M['A']['false_auto'], M['A']['missed']
faB, maB = M['B']['false_auto'], M['B']['missed']
faC, maC = M['C']['false_auto'], M['C']['missed']

def approx(x, y, tol=2):
    return abs(x - y) <= tol

print('\n--- decision rule ---')
claim_win = (faB < faA and maB <= maA) or \
    (faB == faA and maB == maA and M['B']['review_load'] < M['A']['review_load'])
print(f'claim (B beats A): {claim_win}')
polar = approx(faB, faA) and approx(maB, maA) and not claim_win
print(f'polar opposite holds (B≈A, labels add cost without decision value): {polar}')
null = approx(faC, faB) and approx(maC, maB)
print(f'null holds (C≈B, labels carry no information): {null}')

# per-probe detail for the report
detail = []
for pid in sorted(judgments):
    r = results[pid]
    detail.append({'probe': pid, 'human': truth[pid],
                   'A': r['A_action'], 'B_label': r['B_label'],
                   'B': r['B_action'], 'C_label': r['C_label'],
                   'C': r['C_action']})

out = {
    'n': 120,
    'ground_truth_dist': {str(k): v for k, v in Counter(truth.values()).items()},
    'metrics': {arm: {k: v for k, v in m.items() if k != 'dist'}
                for arm, m in M.items()},
    'action_dist': {arm: M[arm]['dist'] for arm in M},
    'label_dist_B': dict(Counter(b_labels)),
    'label_dist_C': dict(Counter(shuffled)),
    'tokens': tok,
    'decision': {'claim_win': claim_win, 'polar_opposite': polar, 'null': null},
    'detail': detail,
}
os.makedirs(f'{STEP4}', exist_ok=True)
json.dump(out, open(f'{STEP4}/step4_results.json', 'w'), indent=1)
print(f'\nwrote {STEP4}/step4_results.json')

# confusion detail: where did B's QUEUEs land?
print('\nB action x human grade:')
ct = Counter((results[pid]['B_action'], truth[pid]) for pid in results)
for k in sorted(ct):
    print(f'  {k}: {ct[k]}')
print('A action x human grade:')
ct = Counter((results[pid]['A_action'], truth[pid]) for pid in results)
for k in sorted(ct):
    print(f'  {k}: {ct[k]}')
