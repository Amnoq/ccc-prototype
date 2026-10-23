#!/usr/bin/env python3
"""CCC-2 parity gate harness (node CCC2-4).

1. Rehydrates all 12 CCC-2 wires through the wire (codec.decode) and writes
   the blind-scorer input: parity_gate/rehydrated_ccc2_cNN.json
   (record dicts with transport checksums stripped — semantic content only).
2. Computes break-even accounting with R3-identical conventions (tiktoken
   cl100k_base): prose tokens (source chunk text), output tokens
   (extraction.json), wire tokens (wrapped .wire file), savings,
   be_dep = (prose_tokens + output_tokens) / savings.

Wire integrity: validate.py already ran 12/12 OK; decode() enforces
checksums — any failure aborts loudly, no silent repair.
"""
import json
import sys

sys.path.insert(0, '/home/hatch/workspace/ccc-prototype/ccc2')
import codec
import tiktoken

CHUNK_FILES = {
    'c01': 'corpus/c01_completemap.txt',
    'c02': 'corpus/c02_deriv_d1_d5.txt',
    'c03': 'corpus/c03_deriv_d6_d8.txt',
    'c04': 'corpus/c04_deriv_d9_d10a12.txt',
    'c05': 'corpus/c05_deriv_d10a3_d10c.txt',
    'c06': 'corpus/c06_deriv_d10de_n14.txt',
    'c07': 'corpus/c07_dtree_nodes0_9.txt',
    'c08': 'corpus/c08_dtree_node10.txt',
    'c09': 'corpus/c09_dtree_node11.txt',
    'c10': 'corpus/c10_dtree_nodes12_13.txt',
    'c11': 'corpus/c11_dtree_d6gen_priorart_n14_11f.txt',
    'c12': 'corpus/c12_operator_audit.txt',
}

enc = tiktoken.get_encoding('cl100k_base')
base = '/home/hatch/workspace/ccc-prototype'
gate = f'{base}/ccc2/parity_gate'
import os
os.makedirs(gate, exist_ok=True)

results = []
for n in range(1, 13):
    ch = f'c{n:02d}'
    wire_str = open(f'{base}/ccc2/wires/{ch}.wire').read()
    records, report = codec.decode(wire_str)  # checksum-enforced; aborts on tamper
    # strip transport checksums: scorer sees semantic content only
    clean = []
    for r in records:
        r2 = {k: v for k, v in r.items() if k != 'checksum'}
        clean.append(r2)
    json.dump({'chunk': ch, 'format': 'ccc2-wire/1', 'records': clean},
              open(f'{gate}/rehydrated_ccc2_{ch}.json', 'w'),
              ensure_ascii=False, indent=1)
    types = {}
    for r in clean:
        types[r['type']] = types.get(r['type'], 0) + 1
    # break-even accounting (R3-identical conventions)
    prose_tokens = len(enc.encode(open(f'{base}/{CHUNK_FILES[ch]}').read()))
    output_tokens = len(enc.encode(open(
        f'{base}/ccc2/corpus/{ch}/extraction.json').read()))
    wire_tokens = len(enc.encode(wire_str))
    savings = prose_tokens - wire_tokens
    be_dep = (prose_tokens + output_tokens) / savings
    results.append((ch, len(clean), types, wire_tokens, round(be_dep, 2)))
    print(ch, 'ok', len(clean), 'records', types,
          wire_tokens, 'wire tokens, BE_dep=%.2f' % be_dep)

wires = [r[3] for r in results]
bes = [r[4] for r in results]
print(f'\nwire tokens: mean {sum(wires)/len(wires):.0f}, '
      f'range {min(wires)}-{max(wires)}')
print(f'BE_dep: mean {sum(bes)/len(bes):.2f}, '
      f'{sum(1 for b in bes if b <= 3)}/12 <= 3')
json.dump([{'chunk': r[0], 'records': r[1], 'types': r[2],
            'wire_tokens': r[3], 'be_dep': r[4]} for r in results],
          open(f'{gate}/cost_table.json', 'w'), indent=1)
print('done')
