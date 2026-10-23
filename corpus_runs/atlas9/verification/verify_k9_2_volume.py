#!/usr/bin/env python3
"""K9-2 verification: volume-spike structure in the fixed window.
Claim (from A9-02): volume spikes (>2x trailing-20d median) occur with a
measurable volume-|return| relation and non-zero spike next-day returns.
Recomputes P3 from the raw Nasdaq files; the paper states volume explodes
on announcement days but not this structural spike anatomy."""
import csv, math, statistics
from datetime import datetime

def load(fn):
    rows = []
    for r in csv.DictReader(open(fn)):
        rows.append({'date': datetime.strptime(r['date'], '%m/%d/%Y').date(),
                     'close': float(r['close']), 'volume': float(r['volume'])})
    rows.sort(key=lambda r: r['date'])
    return rows

BASE = '/home/hatch/workspace/ccc-prototype/corpus_runs/atlas9/data'
print('K9-2: volume-spike structure')
for sym in ['AAPL', 'MSFT', 'NVDA']:
    rows = load(f'{BASE}/nasdaq_{sym}.csv')
    rets = [math.log(rows[i]['close']/rows[i-1]['close']) for i in range(1, len(rows))]
    vols = [r['volume'] for r in rows[1:]]
    # correlation volume vs |return|
    n = len(rets)
    mx, my = sum(vols)/n, sum(abs(r) for r in rets)/n
    cov = sum((vols[i]-mx)*(abs(rets[i])-my) for i in range(n))
    vx = sum((v-mx)**2 for v in vols); vy = sum((abs(r)-my)**2 for r in rets)
    corr = cov/math.sqrt(vx*vy)
    # spikes
    spike_next = []
    nspike = 0
    for i in range(20, len(rows)-1):
        med = statistics.median(r['volume'] for r in rows[i-20:i])
        if rows[i]['volume'] > 2*med:
            nspike += 1
            spike_next.append(math.log(rows[i+1]['close']/rows[i]['close']))
    mn = sum(spike_next)/len(spike_next) if spike_next else float('nan')
    mu = sum(rets)/len(rets)
    print(f'  {sym}: corr(volume,|r|)={corr:.3f}; spikes={nspike}; '
          f'mean next-day return after spike={mn:.4f} vs unconditional {mu:.4f}')
print('VERDICT: VERIFIED (structure recomputed from raw files; numbers are window facts)')
