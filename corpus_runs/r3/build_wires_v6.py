"""build_wires_v6.py -- deterministic v6 wire packages for all 12 R3 chunks.

Reads corpus_runs/r3/cNN/extraction.json, builds registry, v6 ints
(with notes + entity statuses), gamma-bitstream wire body, telomere
wrap. Saves corpus_runs/r3/cNN/wire_v6.json with wrapped wire +
ordered registry names, and rehydrated_v6.json with the decoded struct
(for the blind rescore: scorers see ONLY rehydrated_v6.json).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from memory_harness import (build_registry, to_v6_export,
                            validate_extraction)
from codec import (first_n_primes, build_message_v6, encode_wire_v6,
                   decode_wire_v6, decode_struct_v6, wrap_telomere,
                   registry_fingerprint)

base = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
for n in range(1, 13):
    ch = f"c{n:02d}"
    cbase = f"{base}/corpus_runs/r3/{ch}"
    doc = json.load(open(f"{cbase}/extraction.json"))
    assert not validate_extraction(doc), ch
    reg = build_registry(doc)
    primes = first_n_primes(len(reg.names))
    ints, notes = build_message_v6(to_v6_export(doc), reg, primes,
                                   epoch=n)
    body = encode_wire_v6(ints, notes)
    wrapped = wrap_telomere(body, 6, len(reg.names),
                            registry_fingerprint(reg), 1)
    # rehydrate through the wire (what the blind scorer sees)
    ints2, notes2 = decode_wire_v6(body)
    assert ints2 == ints and notes2 == notes
    struct = decode_struct_v6(ints2, notes2, reg, primes)
    json.dump({"chunk": ch, "wrapped": wrapped,
               "registry": reg.names},
              open(f"{cbase}/wire_v6.json", "w"))
    json.dump(struct, open(f"{cbase}/rehydrated_v6.json", "w"),
              default=str)
    print(ch, "ok", len(reg.names), "concepts,",
          len(notes), "notes")
print("done")
