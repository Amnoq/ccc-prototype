"""build_wires_v7.py -- deterministic v7 wire packages for all 12 R4 chunks.

Reads corpus_runs/r4/cNN/extraction.json (v7-native statuses + genres),
builds registry, v7 ints (status+genre annotated anchors), wire body
with notes as literal text, telomere wrap. Saves
corpus_runs/r4/cNN/wire_v7.json and rehydrated_v7.json (for the blind
parity re-measurement: scorers see ONLY rehydrated_v7.json).
Also reports wire tokens and deployment break-even per chunk.
"""
import json
import sys

sys.path.insert(0, '/home/hatch/workspace/ccc-prototype')
import tiktoken
from memory_harness import (build_registry, to_v7_export,
                            validate_extraction)
from codec import (first_n_primes, build_message_v7, encode_wire_v7,
                   decode_wire_v7, decode_struct_v7, wrap_telomere,
                   registry_fingerprint)

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

results = []
for n in range(1, 13):
    ch = f'c{n:02d}'
    cbase = f'{base}/corpus_runs/r4/{ch}'
    doc = json.load(open(f'{cbase}/extraction.json'))
    assert not validate_extraction(doc), ch
    reg = build_registry(doc)
    primes = first_n_primes(len(reg.names))
    ints, notes = build_message_v7(to_v7_export(doc), reg, primes,
                                   epoch=n)
    body = encode_wire_v7(ints, notes)
    wrapped = wrap_telomere(body, 7, len(reg.names),
                            registry_fingerprint(reg), 1)
    # rehydrate through the wire (what the blind scorer sees)
    ints2, notes2 = decode_wire_v7(body)
    assert ints2 == ints and notes2 == notes, ch
    struct = decode_struct_v7(ints2, notes2, reg, primes)
    json.dump({'chunk': ch, 'wrapped': wrapped,
               'registry': reg.names},
              open(f'{cbase}/wire_v7.json', 'w'))
    json.dump(struct, open(f'{cbase}/rehydrated_v7.json', 'w'),
              default=str)
    # costs (R3-identical conventions; wire path)
    prose_tokens = len(enc.encode(open(f'{base}/{CHUNK_FILES[ch]}').read()))
    output_tokens = len(enc.encode(json.dumps(doc)))
    wire_tokens = len(enc.encode(wrapped))
    savings = prose_tokens - wire_tokens
    be_dep = (prose_tokens + output_tokens) / savings
    results.append((ch, len(reg.names), len(notes), wire_tokens,
                    round(be_dep, 2)))
    print(ch, 'ok', len(reg.names), 'concepts,', len(notes), 'notes,',
          wire_tokens, 'wire tokens, BE_dep=%.2f' % be_dep)

wires = [r[3] for r in results]
bes = [r[4] for r in results]
print(f'\nwire tokens: mean {sum(wires)/len(wires):.0f}, '
      f'range {min(wires)}-{max(wires)}')
print(f'BE_dep: mean {sum(bes)/len(bes):.2f}, '
      f'{sum(1 for b in bes if b <= 3)}/12 <= 3')
print('done')
