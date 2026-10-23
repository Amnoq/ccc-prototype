"""build_wires_r3.py -- deterministic v5 wire packages for all 12 R3 chunks.

Reads corpus_runs/r3/cNN/extraction.json, builds registry, v5 ints,
gamma-bitstream wire, telomere wrap. Saves corpus_runs/r3/cNN/wire.json
with wrapped wire + ordered registry names + expected struct (for the
coordinator's fidelity check; rehydrators must NOT see expected_struct).
"""
import json, sys
sys.path.insert(0, '/home/hatch/workspace/ccc-prototype')
from memory_harness import build_registry, to_v5_export
from codec import (first_n_primes, build_message_v5, encode_message_bits,
                   wrap_telomere, registry_fingerprint, decode_struct_v5,
                   validate_message_v5)

for n in range(1, 13):
    ch = f'c{n:02d}'
    base = f'/home/hatch/workspace/ccc-prototype/corpus_runs/r3/{ch}'
    doc = json.load(open(f'{base}/extraction.json'))
    reg = build_registry(doc)
    B = len(reg.names)
    primes = first_n_primes(B)
    export = to_v5_export(doc)
    ints = build_message_v5(export, reg, primes)
    validate_message_v5(ints, B, primes)
    bits = encode_message_bits(ints)
    fp = registry_fingerprint(reg)
    wrapped = wrap_telomere(bits, 5, B, fp, 1)
    struct = decode_struct_v5(ints, reg, primes)
    json.dump({
        'chunk': ch,
        'wrapped_wire': wrapped,
        'registry_names': reg.names,
        'registry_size': B,
        'fingerprint': fp,
        'num_ints': len(ints),
        'wire_chars': len(wrapped),
        'expected_struct': struct,
    }, open(f'{base}/wire.json', 'w'), indent=1)
    print(ch, 'B=', B, 'ints=', len(ints), 'wire_chars=', len(wrapped))
