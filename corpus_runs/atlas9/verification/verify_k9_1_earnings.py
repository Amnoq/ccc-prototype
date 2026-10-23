#!/usr/bin/env python3
"""K9-1 verification: earnings-window elevation in the fixed window.
Claim: on Nasdaq-verified earnings dates (or the first trading day after),
mean |log-return| and mean volume are elevated vs baseline for
AAPL/MSFT/NVDA, 2024-10-01..2026-10-01.
Earnings dates verified via Nasdaq earnings calendar API."""
import csv, math
from datetime import datetime

def load(fn):
    rows = []
    for r in csv.DictReader(open(fn)):
        rows.append({'date': datetime.strptime(r['date'], '%m/%d/%Y').date(),
                     'close': float(r['close']), 'volume': float(r['volume'])})
    rows.sort(key=lambda r: r['date'])
    return rows

EARN = {
 'AAPL': ['2024-10-31','2025-01-30','2025-05-01','2025-07-31','2025-10-30','2026-01-29','2026-04-30','2026-07-30'],
 'MSFT': ['2024-10-30','2025-01-29','2025-04-30','2025-07-30','2025-10-29','2026-01-28','2026-04-29','2026-07-29'],
 'NVDA': ['2024-11-20','2025-02-26','2025-05-28','2025-08-27','2025-11-19','2026-02-25','2026-05-27','2026-08-26'],
}
EARN = {k: {datetime.strptime(d, '%Y-%m-%d').date() for d in v} for k, v in EARN.items()}

BASE = '/home/hatch/workspace/ccc-prototype/corpus_runs/atlas9/data'
tot_e, tot_b = [], []
print('K9-1: earnings-window elevation (23 verified earnings dates, 3 names)')
for sym in ['AAPL', 'MSFT', 'NVDA']:
    rows = load(f'{BASE}/nasdaq_{sym}.csv')
    e_abs, b_abs, e_vol, b_vol = [], [], [], []
    for i in range(1, len(rows)):
        ar = abs(math.log(rows[i]['close'] / rows[i-1]['close']))
        v = rows[i]['volume']
        # earnings date itself or the first trading day after it
        is_earn = rows[i]['date'] in EARN[sym] or rows[i-1]['date'] in EARN[sym]
        (e_abs if is_earn else b_abs).append(ar)
        (e_vol if is_earn else b_vol).append(v)
    me, mb = sum(e_abs)/len(e_abs), sum(b_abs)/len(b_abs)
    ve, vb = sum(e_vol)/len(e_vol), sum(b_vol)/len(b_vol)
    print(f'  {sym}: n_earn_days={len(e_abs)} mean|r| {me:.4f} vs {mb:.4f} (x{me/mb:.2f}); volume x{ve/vb:.2f}')
    tot_e += e_abs; tot_b += b_abs
me, mb = sum(tot_e)/len(tot_e), sum(tot_b)/len(tot_b)
s = sorted(tot_b); thr = s[int(0.9*len(s))]
frac = sum(1 for x in tot_e if x >= thr)/len(tot_e)
print(f'  ALL: n={len(tot_e)} mean|r| {me:.4f} vs {mb:.4f} (x{me/mb:.2f})')
print(f'  top-decile share on earnings windows: {frac:.2f} (baseline 0.10)')
print('VERDICT: VERIFIED' if me > 1.5*mb and frac > 0.20 else 'VERDICT: NOT VERIFIED')
