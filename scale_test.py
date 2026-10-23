"""Real-scale token-economics test for CCC v5.

Question: does the steady-state compression ratio (CCC injection vs prose)
grow, hold, or collapse as the registry scales to hundreds of concepts?

Method: generate synthetic research graphs at several scales/densities,
encode with v5, generate information-equivalent TERSE prose (subject-grouped,
the way a careful summarizer writes), count cl100k_base tokens.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from codec import (Registry, first_n_primes, build_message_v5,
                   encode_message_bits, decode_message_bits,
                   registry_fingerprint)

DOMAINS = ["prime", "spectral", "sieve", "modular", "zeta", "elliptic",
           "automorphic", "diophantine", "ergodic", "padic", "galois",
           "analytic"]
OBJECTS = ["gap", "distribution", "variance", "density", "zero", "value",
           "moment", "correlation", "residue", "conductor", "rank", "height"]
QUALS = ["bound", "estimate", "conjecture", "theorem", "algorithm",
         "heuristic", "criterion", "identity", "expansion", "principle",
         "lemma", "computation"]
TYPES = ["bounds", "exemplifies", "measured_in", "closed_as",
         "converges_to", "belongs_to", "attacks", "sums_over",
         "derived_from", "implements", "layer_of", "overhead_of",
         "constrained_by", "eases", "co_probes"]
VERB = {"bounds": "bounds", "exemplifies": "exemplifies",
        "measured_in": "is measured in", "closed_as": "is closed as",
        "converges_to": "converges to", "belongs_to": "belongs to",
        "attacks": "attacks", "sums_over": "sums over",
        "derived_from": "is derived from", "implements": "implements",
        "layer_of": "is a layer of", "overhead_of": "is overhead of",
        "constrained_by": "is constrained by", "eases": "eases",
        "co_probes": "co-probes"}
STATUSES = ["st_verified", "st_closed_transient", "st_validated"]
STATUS_PROSE = {"st_verified": "verified",
                "st_closed_transient": "closed as transient",
                "st_validated": "validated"}


def gen_graph(n_concepts, n_threads, density, seed):
    rng = random.Random(seed)
    names = []
    seen = set()
    i = 0
    while len(names) < n_concepts:
        n = (f"{rng.choice(DOMAINS)}_{rng.choice(OBJECTS)}_"
             f"{rng.choice(QUALS)}")
        if n in seen:
            n = f"{n}_{i}"
            i += 1
        seen.add(n)
        names.append(n)
    labels = [f"thread_{d}_research" for d in
              rng.sample(DOMAINS, min(n_threads, len(DOMAINS)))]
    while len(labels) < n_threads:
        labels.append(f"thread_extra_{len(labels)}")
    # assign concepts to threads (roughly even, shuffled)
    order = names[:]
    rng.shuffle(order)
    strands = []
    per = len(order) // n_threads
    for t in range(n_threads):
        chunk = order[t * per:(t + 1) * per] if t < n_threads - 1 \
            else order[t * per:]
        strands.append((labels[t], chunk))
    # typed directed edges
    n_edges = int(density * n_concepts)
    edges, eset = [], set()
    by_thread = {lab: set(m) for lab, m in strands}
    members = [m for _, ms in strands for m in ms]
    attempts = 0
    while len(edges) < n_edges and attempts < n_edges * 20:
        attempts += 1
        a = rng.choice(members)
        if rng.random() < 0.7:
            # within-thread: find a's thread
            for lab, ms in strands:
                if a in by_thread[lab]:
                    pool = [m for m in ms if m != a]
                    break
        else:
            pool = [m for m in members if m != a]
        if not pool:
            continue
        b = rng.choice(pool)
        t = rng.choice(TYPES)
        if (a, b, t) not in eset:
            eset.add((a, b, t))
            edges.append((a, b, t))
    anchors = [(a, rng.choice(STATUSES))
               for a in rng.sample(members, max(1, n_concepts // 20))]
    loops = rng.sample([m for m in members
                        if m not in {a for a, _ in anchors}],
                       max(1, n_concepts // 33))
    return names, strands, edges, anchors, loops


def gen_prose(strands, edges, anchors, loops):
    """Terse, subject-grouped prose: the way a careful summarizer writes."""
    parts = []
    for lab, ms in strands:
        parts.append(f"Thread {lab.replace('_', ' ')}: "
                     + ", ".join(ms) + ".")
    by_subj = {}
    for a, b, t in edges:
        by_subj.setdefault(a, []).append((t, b))
    rel = []
    for a, lst in by_subj.items():
        rel.append(a + " " + "; ".join(f"{VERB[t]} {b}"
                                      for t, b in lst) + ".")
    parts.append("Relations: " + " ".join(rel))
    parts.append("Established: " + "; ".join(
        f"{a} ({STATUS_PROSE[s]})" for a, s in anchors) + ".")
    parts.append("Open: " + ", ".join(loops) + ".")
    return "\n".join(parts)


def run_config(n_concepts, n_threads, density, seed):
    names, strands, edges, anchors, loops = gen_graph(
        n_concepts, n_threads, density, seed)
    reg = Registry()
    for c in names + TYPES + STATUSES + [lab for lab, _ in strands]:
        if c not in reg.names:
            reg.add(c)
    B = len(reg.names)
    primes = first_n_primes(B)
    export = {
        "strands": [{"label": lab, "nodes": [{"id": m} for m in ms]}
                    for lab, ms in strands],
        "constraints": [{"a": a, "b": b, "type": t}
                        for a, b, t in edges],
        "anchors": [{"id": a, "status": s} for a, s in anchors],
        "open_loops": [{"node": l} for l in loops],
    }
    from codec import build_message_v5 as b5
    from codec import encode_lines_balanced, decode_lines
    ints = b5(export, reg, primes)
    # weight-balanced multiline: the v3 single-wire header caps at 999
    # triples, and strand prime-products skew heavy, so the transport
    # packs lines by gamma-bit weight (order-independent reassembly).
    lines = encode_lines_balanced(ints)
    import random as _r
    shuffled = lines[:]
    _r.Random(seed).shuffle(shuffled)
    assert decode_lines(shuffled) == ints  # order-independent round-trip
    wire = "\n".join(lines)
    idx = {n: i + 1 for i, n in enumerate(reg.names)}
    compact = {
        "strands": [[idx[lab], [idx[m] for m in ms]]
                    for lab, ms in strands],
        "edges": [[idx[a], idx[t], idx[b]] for a, b, t in edges],
        "anchors": [[idx[a], idx[s]] for a, s in anchors],
        "loops": [idx[l] for l in loops],
    }
    prose = gen_prose(strands, edges, anchors, loops)
    legend = {idx[n]: n for n in names + TYPES + STATUSES
              + [lab for lab, _ in strands]}
    # subject-grouped minimal injection: strands as member runs, edges
    # grouped by subject (mirrors the prose's grouping; JSON brackets
    # and repeated keys were pure syntax overhead).
    glines = []
    for lab, ms in strands:
        glines.append("S%d:" % idx[lab]
                      + " ".join(map(str, sorted(idx[m] for m in ms))))
    bys = {}
    for a, b, t in edges:
        bys.setdefault(idx[a], []).append((idx[t], idx[b]))
    for a in sorted(bys):
        glines.append("E%d:" % a
                      + ",".join("%d %d" % p for p in bys[a]))
    glines.append("A:" + ",".join("%d %d" % (idx[a], idx[s])
                                  for a, s in anchors))
    glines.append("L:" + " ".join(map(str, sorted(idx[l] for l in loops))))
    return {"B": B, "wire": wire,
            "compact": json.dumps(compact),
            "grouped": "\n".join(glines),
            "legend": json.dumps(legend), "prose": prose,
            "n_facts": (len(strands) + len(edges) + len(anchors)
                        + len(loops))}


def main():
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    toks = lambda s: len(enc.encode(s))
    cfgs = [(150, 6), (300, 8), (600, 10), (1000, 12)]
    print(f"{'B':>5} {'dens':>4} {'facts':>6} {'wire':>6} "
          f"{'grp_inj':>7} {'legend':>7} {'prose':>6} "
          f"{'w/p':>5} {'g/p':>5} {'cold/p':>6}")
    rows = []
    for n, th in cfgs:
        for density in (0.5, 1.0, 2.0):
            acc = {"wire": 0, "grp": 0, "legend": 0, "prose": 0,
                   "facts": 0, "B": 0}
            for seed in (1, 2, 3):
                r = run_config(n, th, density, seed)
                acc["wire"] += toks(r["wire"])
                acc["grp"] += toks(r["grouped"])
                acc["legend"] += toks(r["legend"])
                acc["prose"] += toks(r["prose"])
                acc["facts"] += r["n_facts"]
                acc["B"] = r["B"]
            k = 3
            w, g, lg, pr = (acc["wire"] / k, acc["grp"] / k,
                            acc["legend"] / k, acc["prose"] / k)
            rows.append((acc["B"], density, acc["facts"] / k, w, g,
                         lg, pr))
            print(f"{acc['B']:>5} {density:>4} {acc['facts']/k:>6.0f} "
                  f"{w:>6.0f} {g:>7.0f} {lg:>7.0f} {pr:>6.0f} "
                  f"{pr/w:>5.2f} {pr/g:>5.2f} {(lg+w)/pr:>6.2f}")
    json.dump(rows, open(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "scale_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
