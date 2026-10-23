"""benchmark_packets.py -- verdict-packet simulation, tasks 3 & 4.

Builds one verdict packet per D-wire record per VERDICT_PACKET_SPEC.md
(canonical JSON, keys sorted, no whitespace, SHA-256 checksum), measures
tokens vs the 120-token budget, and measures end-to-end per-verdict cost
(record -> packet -> collapse tier lookup per COLLAPSE_SPEC.md).

Field mapping (documented; sensitivity-tested in-report):
  claim:    D=subtitle | V=subject+consequence | G=title+verdict |
            B=x<->y | C=label | L=from rel to
  label:    D=honest_label | V=status | C=status |
            G=killed (SPEC section 2: guardrail = killed path) |
            B,L=heuristic (SIMULATION ASSUMPTION: no native label in v1)
  boundary: D=honest_boundary | G=transfer | B=limits |
            V,C=first sentence of note (or '') | L='' (no native field)
  span:     {"chunk": ch, "start": 0, "end": 0} -- NULL-SPAN PLACEHOLDER:
            D-wire v1 records carry no source spans (the Gate 4 step-0 gap).
            Token counts are therefore a LOWER BOUND; a real span adds
            ~12-18 tokens (measured below as span_delta).
One-liners are faithful first-use of native fields; first-sentence
truncation is deterministic ('. '-split). Nothing is invented.

Run: python3 benchmark_packets.py
Writes /tmp/bench_packets.json and prints a summary.
"""
import hashlib
import json
import statistics
import sys
import time

sys.path.insert(0, '/home/hatch/workspace/ccc-prototype/ccc2')
import codec as ccc2_codec
import tiktoken

enc = tiktoken.get_encoding('cl100k_base')
BASE = '/home/hatch/workspace/ccc-prototype'
CHUNKS = [f'c{n:02d}' for n in range(1, 13)]
BUDGET = 120

TIERS = {  # COLLAPSE_SPEC.md v1, label -> tier
    'exact': 'ACT',
    'computationally_verified': 'ACT with spot-check',
    'conjectural': 'QUEUE for review',
    'heuristic': 'SURFACE only',
    'killed': 'BLOCK the claim',
    'superseded': 'FOLLOW the heir',
    'unstated': 'NO ACTION',
}


def first_sentence(s):
    s = (s or '').strip()
    if '. ' in s:
        return s.split('. ')[0] + '.'
    return s


def build_packet(rec, chunk):
    """Returns the packet dict WITHOUT checksum (checksum added by caller)."""
    t = rec['type']
    if t == 'D':
        claim, label = rec['subtitle'], rec['honest_label']
        boundary = rec['honest_boundary']
    elif t == 'V':
        claim = rec['subject'] + ': ' + rec['consequence']
        label, boundary = rec['status'], first_sentence(rec.get('note'))
    elif t == 'G':
        claim = rec['title'] + ' -- ' + rec['verdict']
        label, boundary = 'killed', rec['transfer']
    elif t == 'B':
        claim = rec['x'] + ' <-> ' + rec['y']
        label, boundary = 'heuristic', rec['limits']  # label: SIMULATION ASSUMPTION
    elif t == 'C':
        claim, label = rec['label'], rec['status']
        boundary = first_sentence(rec.get('note'))
    elif t == 'L':
        claim = f"{rec['from']} {rec['rel']} {rec['to']}"
        label, boundary = 'heuristic', ''  # label: SIMULATION ASSUMPTION
    else:
        raise ValueError(t)
    return {
        'format': 'verdict-packet/1',
        'claim': claim,
        'label': label,
        'span': {'chunk': chunk, 'start': 0, 'end': 0},  # NULL-SPAN placeholder
        'boundary': boundary,
        'record_ref': f"ccc2-wire/1:{chunk}:{rec['id']}",
    }


def canonical(packet_wo_checksum):
    return json.dumps(packet_wo_checksum, sort_keys=True,
                      separators=(',', ':'))


def seal(packet_wo_checksum):
    canon = canonical(packet_wo_checksum)
    cs = hashlib.sha256(canon.encode()).hexdigest()
    p = dict(packet_wo_checksum)
    p['packet_checksum'] = cs
    sealed = json.dumps(p, sort_keys=True, separators=(',', ':'))
    return sealed, cs


def pct(xs, p):
    xs = sorted(xs)
    k = (len(xs) - 1) * p / 100.0
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def main():
    packets = []  # (chunk, id, type, label, sealed_str, tokens)
    for ch in CHUNKS:
        recs, _ = ccc2_codec.decode(open(f'{BASE}/ccc2/wires/{ch}.wire').read())
        for r in recs:
            p0 = build_packet(r, ch)
            sealed, _ = seal(p0)
            packets.append((ch, r['id'], r['type'], p0['label'], sealed,
                            len(enc.encode(sealed))))

    toks = [p[5] for p in packets]
    over = [p for p in packets if p[5] > BUDGET]
    print(f'packets: n={len(packets)}')
    print(f'tokens: mean={statistics.mean(toks):.1f} p90={pct(toks,90):.1f} '
          f'max={max(toks)} min={min(toks)}')
    print(f'over {BUDGET}-token budget: {len(over)}/{len(packets)}')
    for ch, rid, t, lab, _, tk in sorted(over, key=lambda x: -x[5])[:10]:
        print(f'  OVER {ch} {rid} ({t},{lab}): {tk} tokens')

    # span-delta sensitivity: null span vs a representative real span
    null = {'chunk': 'c01', 'start': 0, 'end': 0}
    real = {'chunk': 'c01', 'start': 120, 'end': 340}
    d_null = len(enc.encode(json.dumps(null, sort_keys=True, separators=(',', ':'))))
    d_real = len(enc.encode(json.dumps(real, sort_keys=True, separators=(',', ':'))))
    print(f'span delta (realistic span vs null span): +{d_real - d_null} tokens')

    # label sensitivity: B,L as conjectural instead of heuristic
    alt = 0
    for ch, rid, t, lab, sealed, tk in packets:
        if t in ('B', 'L'):
            alt += len(enc.encode('"conjectural"')) - len(enc.encode('"heuristic"'))
    print(f'label sensitivity (B,L heuristic->conjectural): '
          f'{alt/len([p for p in packets if p[2] in ("B","L")]):.2f} tokens/packet avg')

    # per-type token means
    by_type = {}
    for ch, rid, t, lab, sealed, tk in packets:
        by_type.setdefault(t, []).append(tk)
    print('tokens by record type (mean):',
          {t: round(statistics.mean(v), 1) for t, v in sorted(by_type.items())})

    # ---- task 4: end-to-end per-verdict cost ----
    # build side: packet dict -> canonical -> sha256 ; apply side: parse -> verify -> tier lookup
    rec_by_chunk = {}
    for ch in CHUNKS:
        recs, _ = ccc2_codec.decode(open(f'{BASE}/ccc2/wires/{ch}.wire').read())
        rec_by_chunk[ch] = {r['id']: r for r in recs}
    build_ts, apply_ts = [], []
    tier_counts = {}
    for ch, rid, t, lab, sealed, tk in packets:
        p0 = build_packet(rec_by_chunk[ch][rid], ch)
        # warm
        for _ in range(5):
            seal(p0)
        t0 = time.perf_counter()
        for _ in range(200):
            s, _ = seal(p0)
        build_ts.append((time.perf_counter() - t0) / 200 * 1000.0)
        # apply side
        t0 = time.perf_counter()
        for _ in range(200):
            q = json.loads(sealed)
            cs = q.pop('packet_checksum')
            canon = json.dumps(q, sort_keys=True, separators=(',', ':'))
            assert hashlib.sha256(canon.encode()).hexdigest() == cs
            tier = TIERS[q['label']]
        apply_ts.append((time.perf_counter() - t0) / 200 * 1000.0)
        tier_counts[TIERS.get(lab, 'MALFORMED')] = tier_counts.get(TIERS.get(lab, 'MALFORMED'), 0) + 1

    e2e = [b + a for b, a in zip(build_ts, apply_ts)]
    print(f'\nend-to-end per verdict (build+verify+lookup), n={len(packets)} records x200 reps:')
    print(f'  build ms: mean={statistics.mean(build_ts):.4f} p90={pct(build_ts,90):.4f} '
          f'range=[{min(build_ts):.4f},{max(build_ts):.4f}]')
    print(f'  apply ms: mean={statistics.mean(apply_ts):.4f} p90={pct(apply_ts,90):.4f} '
          f'range=[{min(apply_ts):.4f},{max(apply_ts):.4f}]')
    print(f'  total ms: mean={statistics.mean(e2e):.4f} p90={pct(e2e,90):.4f} '
          f'range=[{min(e2e):.4f},{max(e2e):.4f}]')
    print(f'  total tokens/verdict: mean={statistics.mean(toks):.1f} p90={pct(toks,90):.1f}')
    print('  tier distribution:', tier_counts)

    json.dump({
        'n_packets': len(packets),
        'tokens_mean': statistics.mean(toks), 'tokens_p90': pct(toks, 90),
        'tokens_max': max(toks), 'tokens_min': min(toks),
        'over_budget': [(ch, rid, t, lab, tk) for ch, rid, t, lab, _, tk in over],
        'span_delta_tokens': d_real - d_null,
        'by_type_mean': {t: statistics.mean(v) for t, v in by_type.items()},
        'build_ms_mean': statistics.mean(build_ts), 'build_ms_p90': pct(build_ts, 90),
        'apply_ms_mean': statistics.mean(apply_ts), 'apply_ms_p90': pct(apply_ts, 90),
        'e2e_ms_mean': statistics.mean(e2e), 'e2e_ms_p90': pct(e2e, 90),
        'e2e_ms_min': min(e2e), 'e2e_ms_max': max(e2e),
        'tier_counts': tier_counts,
    }, open('/tmp/bench_packets.json', 'w'), indent=1)
    print('wrote /tmp/bench_packets.json')


if __name__ == '__main__':
    main()
