"""benchmark_wires.py -- application-half benchmarks, tasks 1 & 2.

Pure measurement: v7 and D-wire decode wall-clock, wire tokens
(tiktoken cl100k_base), per-record tokens and per-record decode ms.
No tuning. Run: python3 benchmark_wires.py
Writes JSON results to /tmp/bench_wires.json and prints a summary.
"""
import json
import statistics
import sys
import time

sys.path.insert(0, '/home/hatch/workspace/ccc-prototype')
sys.path.insert(0, '/home/hatch/workspace/ccc-prototype/ccc2')

import tiktoken
# v7 codec lives at the prototype root; ccc2/codec.py shadows the name
# 'codec', so load the v7 one explicitly by path.
import importlib.util as _ilu
_v7spec = _ilu.spec_from_file_location(
    'codec_v7', '/home/hatch/workspace/ccc-prototype/codec.py')
codec_v7 = _ilu.module_from_spec(_v7spec)
_v7spec.loader.exec_module(codec_v7)
Registry, first_n_primes = codec_v7.Registry, codec_v7.first_n_primes
scan_telomeres = codec_v7.scan_telomeres
decode_wire_v7, decode_struct_v7 = (codec_v7.decode_wire_v7,
                                    codec_v7.decode_struct_v7)
import codec as ccc2_codec

enc = tiktoken.get_encoding('cl100k_base')
BASE = '/home/hatch/workspace/ccc-prototype'
CHUNKS = [f'c{n:02d}' for n in range(1, 13)]
WARM, REPS = 5, 30


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return float('nan')
    k = (len(xs) - 1) * p / 100.0
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def timeit(fn, warm=WARM, reps=REPS):
    for _ in range(warm):
        fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append((time.perf_counter() - t0) * 1000.0)
    return ts


# ---------------- v7 ----------------
def v7_decode_path(ch):
    """Full application-half decode path for one v7 chunk."""
    def run():
        wire = json.load(open(f'{BASE}/corpus_runs/r5/{ch}/wire_v7.json'))
        wrapped, names = wire['wrapped'], wire['registry']
        found = list(scan_telomeres(wrapped))
        assert len(found) == 1, ch
        ctx, body = found[0]
        assert ctx['version'] == 7, ch
        ints, notes = decode_wire_v7(body)
        reg = Registry()
        for nm in names:
            reg.add(nm)
        primes = first_n_primes(len(names))
        struct = decode_struct_v7(ints, notes, reg, primes)
        return struct
    return run


def bench_v7():
    out = {}
    for ch in CHUNKS:
        wire = json.load(open(f'{BASE}/corpus_runs/r5/{ch}/wire_v7.json'))
        wrapped = wire['wrapped']
        wire_tokens = len(enc.encode(wrapped))
        ts = timeit(v7_decode_path(ch))
        struct = v7_decode_path(ch)()
        n_anchors = len(struct.get('anchors', []))
        n_notes = len(struct.get('anchors', []))
        out[ch] = {
            'wire_tokens': wire_tokens,
            'decode_ms_mean': statistics.mean(ts),
            'decode_ms_p90': pct(ts, 90),
            'decode_ms_min': min(ts),
            'decode_ms_max': max(ts),
            'n_anchors': n_anchors,
            'per_record_tokens_amortized': wire_tokens / n_anchors if n_anchors else None,
            'per_record_decode_ms': statistics.mean(ts) / n_anchors if n_anchors else None,
        }
    return out


# ---------------- D-wire ----------------
def dwire_decode_path(ch):
    def run():
        s = open(f'{BASE}/ccc2/wires/{ch}.wire').read()
        return ccc2_codec.decode(s)
    return run


def bench_dwire():
    out = {}
    for ch in CHUNKS:
        s = open(f'{BASE}/ccc2/wires/{ch}.wire').read()
        wire_tokens = len(enc.encode(s))
        ts = timeit(dwire_decode_path(ch))
        recs, _ = ccc2_codec.decode(s)
        n = len(recs)
        per_rec_tok = [len(enc.encode(ccc2_codec.canonical(r))) for r in recs]
        out[ch] = {
            'wire_tokens': wire_tokens,
            'decode_ms_mean': statistics.mean(ts),
            'decode_ms_p90': pct(ts, 90),
            'decode_ms_min': min(ts),
            'decode_ms_max': max(ts),
            'n_records': n,
            'per_record_tokens_mean': statistics.mean(per_rec_tok),
            'per_record_tokens_p90': pct(per_rec_tok, 90),
            'per_record_tokens_max': max(per_rec_tok),
            'per_record_decode_ms': statistics.mean(ts) / n,
        }
    return out


def main():
    v7 = bench_v7()
    dw = bench_dwire()
    json.dump({'v7': v7, 'dwire': dw},
              open('/tmp/bench_wires.json', 'w'), indent=1)

    def agg(d, k):
        xs = [d[ch][k] for ch in CHUNKS if d[ch][k] is not None]
        return statistics.mean(xs), pct(xs, 90), min(xs), max(xs)

    print('=== v7 (per chunk, n=12) ===')
    for k, lbl in [('wire_tokens', 'wire tokens'), ('decode_ms_mean', 'decode ms (mean of reps)'),
                   ('per_record_tokens_amortized', 'per-anchor tokens (amortized)'),
                   ('per_record_decode_ms', 'per-anchor decode ms')]:
        m, p90, mn, mx = agg(v7, k)
        print(f'  {lbl}: mean={m:.3f} p90={p90:.3f} range=[{mn:.3f},{mx:.3f}]')
    print('  anchors/chunk mean:', statistics.mean(v7[ch]['n_anchors'] for ch in CHUNKS))

    print('=== D-wire (per chunk, n=12) ===')
    for k, lbl in [('wire_tokens', 'wire tokens'), ('decode_ms_mean', 'decode ms (mean of reps)'),
                   ('per_record_tokens_mean', 'per-record tokens'),
                   ('per_record_decode_ms', 'per-record decode ms')]:
        m, p90, mn, mx = agg(dw, k)
        print(f'  {lbl}: mean={m:.3f} p90={p90:.3f} range=[{mn:.3f},{mx:.3f}]')
    print('  records/chunk mean:', statistics.mean(dw[ch]['n_records'] for ch in CHUNKS))
    print('wrote /tmp/bench_wires.json')


if __name__ == '__main__':
    main()
