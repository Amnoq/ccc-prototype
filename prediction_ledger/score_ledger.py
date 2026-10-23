#!/usr/bin/env python3
"""Score the prediction ledger. Stdlib only.

Usage: python3 score_ledger.py [ledger.csv]
Reports Brier scores, skill vs base rate, per-class breakdown,
paired router-vs-AI comparisons with standard errors, the
passivity index, and the skip rate.
"""
import csv, math, random, statistics, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else 'ledger.csv'
AGENTS = [('router', 'p_router'), ('ai_1', 'p_ai_1'), ('ai_2', 'p_ai_2')]

def fnum(x):
    try:
        v = float(x)
        return v if 0.0 <= v <= 1.0 else None
    except (TypeError, ValueError):
        return None

rows = list(csv.DictReader(open(PATH)))
scored = [r for r in rows if r.get('result') in ('0', '1')]
for r in scored:
    r['_y'] = int(r['result'])
skips = [r for r in rows if r.get('result') == 'skip']

print(f"rows: {len(rows)}  scored: {len(scored)}  pending: {len(rows)-len(scored)-len(skips)}  skips: {len(skips)}")
if skips or rows:
    denom = len(rows) or 1
    print(f"skip rate: {len(skips)/denom:.2%}")
if not scored:
    print("no scored entries yet.")
    sys.exit(0)

f = statistics.mean(r['_y'] for r in scored)
bs_ref = f * (1 - f)
print(f"\nbase rate f={f:.3f}  BS_ref={bs_ref:.4f}")

def brier(rs, key):
    ps = [(fnum(r[key]), r['_y']) for r in rs]
    ps = [(p, y) for p, y in ps if p is not None]
    if not ps:
        return None, 0
    return statistics.mean((p - y) ** 2 for p, y in ps), len(ps)

print("\n-- Brier scores (lower is better) --")
scores = {}
for name, key in AGENTS:
    bs, n = brier(scored, key)
    scores[name] = (bs, n)
    if bs is None:
        print(f"{name:8s} n={n:4d}  no probabilities logged")
    else:
        skill = 1 - bs / bs_ref if bs_ref > 0 else float('nan')
        print(f"{name:8s} n={n:4d}  BS={bs:.4f}  skill={skill:+.3f}")

print("\n-- per outcome_class (router) --")
classes = sorted({r['outcome_class'] for r in scored if r.get('outcome_class')})
for c in classes:
    rs = [r for r in scored if r['outcome_class'] == c]
    bs, n = brier(rs, 'p_router')
    if bs is not None:
        print(f"{c:28s} n={n:4d}  BS={bs:.4f}")

print("\n-- paired router vs AI (same items) --")
for name, key in AGENTS[1:]:
    pairs = [(fnum(r['p_router']), fnum(r[key]), r['_y']) for r in scored]
    pairs = [(pr, pa, y) for pr, pa, y in pairs if pr is not None and pa is not None]
    n = len(pairs)
    if n < 2:
        print(f"router vs {name}: n={n} (need >=2)")
        continue
    diffs = [(pr - y) ** 2 - (pa - y) ** 2 for pr, pa, y in pairs]
    md = statistics.mean(diffs)
    se = statistics.pstdev(diffs) / math.sqrt(n) if n > 1 else float('nan')
    sig = "SIGNIFICANT" if abs(md) > 2 * se else "not significant"
    print(f"router vs {name}: n={n:4d}  mean_diff={md:+.4f}  SE={se:.4f}  {sig}  (negative favors router)")

print("\n-- anchoring: w_shown - w_blind --")
print("blind arm is the baseline (shared evidence correlates even blind);")
print("anchoring = excess correlation in the shown arm.")
def slope(pairs):
    if len(pairs) < 2:
        return None
    xs = [x for x, _ in pairs]; ys = [y for _, y in pairs]
    vx = statistics.pvariance(xs)
    if vx == 0:
        return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in pairs) / len(pairs)
    return cov / vx

def arm_pairs(arm):
    rs = [r for r in scored if r.get('shown_first') == arm]
    ps = [(fnum(r['p_ai_1']), fnum(r['p_router'])) for r in rs]
    return [(a, b) for a, b in ps if a is not None and b is not None]

arms = {a: arm_pairs(a) for a in ('blind', 'shown')}
for a, ps in arms.items():
    w = slope(ps)
    bs, _ = brier([r for r in scored if r.get('shown_first') == a], 'p_router')
    s = f"w={w:.3f} (n={len(ps)})" if w is not None else "insufficient data"
    if bs is not None:
        s += f"  router_BS={bs:.4f}"
    print(f"arm {a:6s}: {s}")
if all(len(ps) >= 2 for ps in arms.values()):
    wb, ws = arms['blind'], arms['shown']
    diffs = []
    for _ in range(1000):
        rb = [random.choice(wb) for _ in wb]
        rs_ = [random.choice(ws) for _ in ws]
        b, s_ = slope(rb), slope(rs_)
        if b is not None and s_ is not None:
            diffs.append(s_ - b)
    if diffs:
        diffs.sort()
        lo, hi = diffs[int(0.025 * len(diffs))], diffs[int(0.975 * len(diffs))]
        wdiff = slope(ws) - slope(wb)
        print(f"anchoring w_shown - w_blind = {wdiff:.3f}  95% bootstrap CI [{lo:.3f}, {hi:.3f}]")
        print("CI above 0 = anchoring detected; CI covering 0 = no evidence of anchoring")
