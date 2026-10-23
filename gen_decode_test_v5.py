"""v5 test material: labels, typed directed edges, anchor statuses."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from codec import (Registry, first_n_primes, build_message_v5,
                   decode_struct_v5, validate_message_v5,
                   encode_message_bits, decode_message_bits, wrap_telomere,
                   registry_fingerprint, scan_telomeres)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "decode_test_material_v5")
os.makedirs(OUT, exist_ok=True)

BASE = [
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
TYPES = ["bounds", "exemplifies", "measured_in", "closed_as",
         "converges_to", "belongs_to", "attacks", "sums_over",
         "derived_from", "implements", "layer_of", "overhead_of",
         "constrained_by", "eases", "co_probes"]
STATUSES = ["st_verified", "st_closed_transient", "st_validated"]
LABELS = ["thread_gap_analysis", "thread_spectral_stats",
          "thread_analytic_machinery", "thread_ccc_project"]

STRANDS = [
    ("thread_gap_analysis",
     ["prime_gaps", "maximal_prime_gap", "jacobsthal_function",
      "primorial_wheel", "wheel_210", "gap_residues", "mod9_analysis"]),
    ("thread_spectral_stats",
     ["zeta_zeros", "gue_statistics", "berry_tones", "number_variance",
      "odlyzko_computation", "lattice_echo", "finite_T_correction",
      "rmt_limit"]),
    ("thread_analytic_machinery",
     ["hardy_littlewood", "singular_series", "sieve_methods",
      "explicit_formula", "mobius_function", "euler_product",
      "prime_zeta"]),
    ("thread_ccc_project",
     ["ccc_codec", "registry_sync", "cursor_layer", "fountain_code",
      "context_compression", "llm_context_window", "token_budget",
      "prompt_caching"]),
]

EDGES = [
    ("jacobsthal_function", "maximal_prime_gap", "bounds"),
    ("wheel_210", "primorial_wheel", "exemplifies"),
    ("berry_tones", "number_variance", "measured_in"),
    ("lattice_echo", "finite_T_correction", "closed_as"),
    ("gue_statistics", "rmt_limit", "converges_to"),
    ("singular_series", "hardy_littlewood", "belongs_to"),
    ("sieve_methods", "twin_primes", "attacks"),
    ("explicit_formula", "zeta_zeros", "sums_over"),
    ("prime_zeta", "euler_product", "derived_from"),
    ("ccc_codec", "context_compression", "implements"),
    ("cursor_layer", "ccc_codec", "layer_of"),
    ("fountain_code", "ccc_codec", "layer_of"),
    ("registry_sync", "ccc_codec", "overhead_of"),
    ("token_budget", "llm_context_window", "constrained_by"),
    ("prompt_caching", "token_budget", "eases"),
    ("prime_gaps", "zeta_zeros", "co_probes"),
]

ANCHORS = [("wheel_210", "st_verified"),
           ("lattice_echo", "st_closed_transient"),
           ("singular_series", "st_validated")]
LOOPS = ["riemann_hypothesis", "twin_primes"]

# why/how probes: only answerable because v5 carries labels/types/statuses
PROBES_WHY = [
    {"q": "What is the label of the thread containing prime_gaps?",
     "a": "thread_gap_analysis"},
    {"q": "How does jacobsthal_function relate to maximal_prime_gap?",
     "a": "bounds"},
    {"q": "Why is lattice_echo established?",
     "a": "st_closed_transient (closed as a finite_T_correction)"},
    {"q": "What does prompt_caching do to token_budget?",
     "a": "eases"},
    {"q": "In what way is explicit_formula related to zeta_zeros?",
     "a": "sums_over"},
    {"q": "What kind of relation connects sieve_methods and twin_primes?",
     "a": "attacks"},
    {"q": "What is the status of singular_series?",
     "a": "st_validated (validated to 0.1%)"},
    {"q": "What is cursor_layer's relationship to ccc_codec?",
     "a": "layer_of"},
    {"q": "How do prime_gaps and zeta_zeros relate?",
     "a": "co_probes (both probe prime distribution)"},
    {"q": "Which thread is wheel_210 in, and what does its anchor status mean?",
     "a": "thread_gap_analysis; st_verified (verified)"},
]

# original structural probes (regression)
PROBES_STRUCT = [
    {"q": "Which concepts are established (anchors)?",
     "a": ["wheel_210", "lattice_echo", "singular_series"]},
    {"q": "Is wheel_210 an anchor?", "a": "yes"},
    {"q": "Are berry_tones and number_variance directly related?",
     "a": "yes"},
    {"q": "Which thread contains both prime_gaps and wheel_210?",
     "a": "thread_gap_analysis"},
    {"q": "What is the status of twin_primes?",
     "a": "open loop (unresolved)"},
    {"q": "Is mobius_function in the spectral statistics thread?",
     "a": "no (analytic machinery)"},
    {"q": "Is there a direct relation between prompt_caching and ccc_codec?",
     "a": "no"},
    {"q": "Name all open loops.",
     "a": ["riemann_hypothesis", "twin_primes"]},
]


def main():
    reg = Registry()
    for c in BASE + TYPES + STATUSES + LABELS:
        reg.add(c)
    B = len(reg.names)
    primes = first_n_primes(B)

    export = {
        "strands": [{"label": lab, "nodes": [{"id": n} for n in members]}
                    for lab, members in STRANDS],
        "constraints": [{"a": a, "b": b, "type": t} for a, b, t in EDGES],
        "anchors": [{"id": a, "status": s} for a, s in ANCHORS],
        "open_loops": [{"node": l} for l in LOOPS],
    }
    ints = build_message_v5(export, reg, primes)
    validate_message_v5(ints, B, primes)
    wire = encode_message_bits(ints)
    fp = registry_fingerprint(reg)
    wrapped = wrap_telomere(wire, 5, B, fp, 1)

    found = list(scan_telomeres("xx " + wrapped + " yy"))
    assert len(found) == 1 and found[0][0]["version"] == 5
    assert decode_message_bits(found[0][1]) == ints
    struct = decode_struct_v5(ints, reg, primes)

    used = set()
    for s in struct["strands"]:
        if s["label"]:
            used.add(reg.index(s["label"]))
        used.update(reg.index(n) for n in s["members"])
    for a, t, b in struct["edges"]:
        used.update([reg.index(a), reg.index(t), reg.index(b)])
    for a, s in struct["anchors"]:
        used.update([reg.index(a), reg.index(s)])
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
    w("probes_why.json", json.dumps(PROBES_WHY, indent=1))
    w("probes_struct.json", json.dumps(PROBES_STRUCT, indent=1))
    w("ints.txt", " ".join(map(str, ints)))
    # v5 struct for the harness-injected indices form
    idx_of = {n: i + 1 for i, n in enumerate(reg.names)}
    compact = {
        "strands": [[idx_of[s["label"]] if s["label"] else 0,
                     [idx_of[n] for n in s["members"]]]
                    for s in struct["strands"]],
        "edges": [[idx_of[a], idx_of[t], idx_of[b]]
                  for a, t, b in struct["edges"]],
        "anchors": [[idx_of[a], idx_of[s]] for a, s in struct["anchors"]],
        "loops": [idx_of[n] for n in struct["loops"]],
    }
    w("compact.json", json.dumps(compact))
    print(f"B={B} n_ints={len(ints)} wire_digits={len(wire)} fp={fp}")
    print("max int:", max(ints))


if __name__ == "__main__":
    main()
