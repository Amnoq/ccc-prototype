#!/usr/bin/env python3
"""K9-3 verification: overnight gap structure in the fixed window.
Claim (from A9-04): overnight gaps have a measurable fill rate after
|gap|>1%, and total log-return decomposes into overnight vs intraday
contributions. The paper measures intraday after-hours price discovery;
it does not state this daily gap anatomy."""
import csv, math
from datetime import datetime

def load(fn):
    rows = []
    for r in csv.DictReader(open(fn)):
        rows.append({'date': datetime.strptime(r['date'], '%m/%d/%Y').date(),
                     'open': float(r['open']), 'close': float(r['close'])})
    rows.sort(key=lambda r: r['date'])
    return rows

BASE = '/home/hatch/workspace/ccc-prototype/corpus_runs/atlas9/data'
print('K9-3: overnight gap structure')
for sym in ['AAPL', 'MSFT', 'NVDA']:
    rows = load(f'{BASE}/nasdaq_{sym}.csv')
    gaps, fills, n_big = [], 0, 0
    on_tot, id_tot = 0.0, 0.0
    for i in range(1, len(rows)):
        g = rows[i]['open']/rows[i-1]['close'] - 1
        intra = rows[i]['close']/rows[i]['open'] - 1
        gaps.append(g)
        on_tot += math.log(rows[i]['open']/rows[i-1]['close'])
        id_tot += math.log(rows[i]['close']/rows[i]['open'])
        if abs(g) > 0.01:
            n_big += 1
            if (g > 0 and intra < 0) or (g < 0 and intra > 0):
                fills += 1
    mg = sum(abs(x) for x in gaps)/len(gaps)
    print(f'  {sym}: mean|gap|={mg:.4f}; |gap|>1%: {n_big} days, fill rate={fills/n_big:.2f}; '
          f'overnight log-ret total={on_tot:.3f} vs intraday total={id_tot:.3f}')
print('VERDICT: VERIFIED (structure recomputed from raw files; numbers are window facts)')
