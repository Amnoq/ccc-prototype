"""Generate test material for the model-side decode experiment.

Builds a realistic small research context (prime-distribution investigation),
encodes it with codec.py, and emits:
  - wire.txt        : v4 wire (naked)
  - wrapped.txt     : telomere-wrapped wire
  - legend.json     : index -> concept name for indices used
  - struct.json     : decode_struct output (the harness-parsed form)
  - prose.txt       : information-equivalent natural-language version
  - probes.json     : questions + ground truth
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from codec import (Registry, first_n_primes, build_message, decode_struct,
                   encode_message_bits, wrap_telomere, registry_fingerprint)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "decode_test_material")
os.makedirs(OUT, exist_ok=True)

CONCEPTS = [
    "prime_gaps", "maximal_prime_gap", "jacobsthal_function",
    "primorial_wheel", "wheel_210", "gap_residues", "mod9_analysis",
    "zeta_zeros", "gue_statistics", "berry_tones", "number_variance",
    "odlyzko_computation", "lattice_echo", "finite_T_correction",
    "rmt_limit", "hardy_littlewood", "singular_series", "sieve_methods",
    "explicit_formula", "mobius_function", "euler_product", "prime_zeta",
    "twin_primes", "riemann_hypothesis",
    "ccc_codec", "registry_sync", "cursor_layer", "fountain_code",
    "context_compression", "llm_context_window", "token_budget",
    "prompt_caching",
]

STRANDS = [
    ["prime_gaps", "maximal_prime_gap", "jacobsthal_function",
     "primorial_wheel", "wheel_210", "gap_residues", "mod9_analysis"],
    ["zeta_zeros", "gue_statistics", "berry_tones", "number_variance",
     "odlyzko_computation", "lattice_echo", "finite_T_correction",
     "rmt_limit"],
    ["hardy_littlewood", "singular_series", "sieve_methods",
     "explicit_formula", "mobius_function", "euler_product", "prime_zeta"],
    ["ccc_codec", "registry_sync", "cursor_layer", "fountain_code",
     "context_compression", "llm_context_window", "token_budget",
     "prompt_caching"],
]

EDGES = [
    ("prime_gaps", "zeta_zeros"),
    ("jacobsthal_function", "maximal_prime_gap"),
    ("primorial_wheel", "wheel_210"),
    ("berry_tones", "number_variance"),
    ("lattice_echo", "finite_T_correction"),
    ("gue_statistics", "rmt_limit"),
    ("singular_series", "hardy_littlewood"),
    ("sieve_methods", "twin_primes"),
    ("explicit_formula", "zeta_zeros"),
    ("prime_zeta", "euler_product"),
    ("ccc_codec", "context_compression"),
    ("cursor_layer", "ccc_codec"),
    ("fountain_code", "ccc_codec"),
    ("token_budget", "llm_context_window"),
    ("prompt_caching", "token_budget"),
    ("registry_sync", "ccc_codec"),
]

ANCHORS = ["wheel_210", "lattice_echo", "singular_series"]
LOOPS = ["riemann_hypothesis", "twin_primes"]

PROSE = """Research status: prime distribution investigation. Four active threads.

(1) Gap analysis: prime_gaps, maximal_prime_gap, jacobsthal_function,
primorial_wheel, wheel_210, gap_residues, mod9_analysis. The wheel_210
case is verified (established). The jacobsthal_function bounds
maximal_prime_gap.

(2) Spectral statistics: zeta_zeros, gue_statistics, berry_tones,
number_variance, odlyzko_computation, lattice_echo, finite_T_correction,
rmt_limit. Berry_tones were measured in the number_variance; the
lattice_echo is closed as a finite_T_correction (established);
gue_statistics is the rmt_limit.

(3) Analytic machinery: hardy_littlewood, singular_series,
sieve_methods, explicit_formula, mobius_function, euler_product,
prime_zeta. The hardy_littlewood singular_series is validated to 0.1%
(established). Sieve_methods attack twin_primes; the explicit_formula
sums over zeta_zeros; prime_zeta comes from the euler_product
logarithm.

(4) CCC project: ccc_codec, registry_sync, cursor_layer, fountain_code,
context_compression, llm_context_window, token_budget, prompt_caching.
The ccc_codec implements context_compression; cursor_layer and
fountain_code are layers of the ccc_codec; registry_sync is overhead of
the ccc_codec; token_budget is constrained by the llm_context_window;
prompt_caching eases token_budget pressure.

Cross-thread: prime_gaps and zeta_zeros both probe prime distribution.

Open loops (unresolved): riemann_hypothesis (unproven), twin_primes
(open)."""

PROBES = [
    {"q": "Which concepts are established (anchors)?",
     "a": ["wheel_210", "lattice_echo", "singular_series"]},
    {"q": "Is wheel_210 an anchor?",
     "a": "yes"},
    {"q": "Are berry_tones and number_variance directly related?",
     "a": "yes"},
    {"q": "Which thread contains both prime_gaps and wheel_210?",
     "a": "gap analysis (thread 1)"},
    {"q": "What is the status of twin_primes?",
     "a": "open loop (unresolved)"},
    {"q": "Is mobius_function in the spectral statistics thread?",
     "a": "no (it is in analytic machinery, thread 3)"},
    {"q": "Is there a direct relation between prompt_caching and ccc_codec?",
     "a": "no"},
    {"q": "Name all open loops.",
     "a": ["riemann_hypothesis", "twin_primes"]},
    {"q": "What bounds maximal_prime_gap?",
     "a": "jacobsthal_function"},
    {"q": "Which thread contains prime_zeta, and what is prime_zeta related to?",
     "a": "analytic machinery (thread 3); related to euler_product"},
]


def main():
    reg = Registry()
    for c in CONCEPTS:
        reg.add(c)
    B = len(reg.names)
    primes = first_n_primes(B)

    export = {
        "strands": [{"nodes": [{"id": n} for n in s]} for s in STRANDS],
        "constraints": [{"a": a, "b": b} for a, b in EDGES],
        "anchors": [{"id": a} for a in ANCHORS],
        "open_loops": [{"node": l} for l in LOOPS],
    }
    ints = build_message(export, reg, primes)
    wire = encode_message_bits(ints)
    fp = registry_fingerprint(reg)
    wrapped = wrap_telomere(wire, 4, B, fp, 1)

    # sanity: full round trip
    from codec import decode_message_bits, scan_telomeres
    found = list(scan_telomeres("xx " + wrapped + " yy"))
    assert len(found) == 1
    assert decode_message_bits(found[0][1]) == ints
    struct = decode_struct(ints, reg, primes)

    used = set()
    for s in struct["strands"]:
        used.update(reg.index(n) for n in s)
    for a, b in struct["edges"]:
        used.add(reg.index(a))
        used.add(reg.index(b))
    for n in struct["anchors"]:
        used.add(reg.index(n))
    for n in struct["loops"]:
        used.add(reg.index(n))
    legend = {i: reg.name(i) for i in sorted(used)}

    def w(name, s):
        with open(os.path.join(OUT, name), "w") as f:
            f.write(s)

    w("wire.txt", wire)
    w("wrapped.txt", wrapped)
    w("legend.json", json.dumps(legend, indent=1))
    w("struct.json", json.dumps(struct, indent=1))
    w("prose.txt", PROSE)
    w("probes.json", json.dumps(PROBES, indent=1))
    w("ints.txt", " ".join(map(str, ints)))
    print(f"B={B} n_ints={len(ints)} wire_digits={len(wire)} "
          f"fingerprint={fp}")
    print("struct:", json.dumps(struct)[:200], "...")


if __name__ == "__main__":
    main()
