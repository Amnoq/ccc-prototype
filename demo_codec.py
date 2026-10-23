"""CCC codec demo: three sessions, measured in real tokens.

Session 1: registry synchronized once (the shared codebook -- the one
           transmission of raw content, amortized over all later sessions).
Session 2: structural message only (anchors/strands/edges/loops as prime
           products + packed pairs) over the codon wire format; decoded,
           rehydrated, probed for fidelity.
Session 3: two NEW concepts arrive (raw delta, transmitted once) plus a
           structural update -- the steady-state cost of novelty.

Baseline each session: retransmitting the raw content strings, i.e. what
you paste into an LLM today.

Token counts via tiktoken cl100k_base (proxy for the target LLM's
tokenizer, labeled as such).
"""
import json

import tiktoken
from ccc import Graph
from codec import (Registry, build_message, decode_struct, first_n_primes,
                   encode_message_bits as encode_message,
                   decode_message_bits as decode_message)

enc = tiktoken.get_encoding("cl100k_base")
TOK = lambda s: len(enc.encode(s))  # noqa: E731
print("tokenizer: tiktoken cl100k_base (proxy for target LLM)\n")

export = json.load(open("ccc_export.json"))

# --------------------------------------------------------------------------
# shared registry (deterministic order)
# --------------------------------------------------------------------------
reg = Registry()
content_of = {}
for a in export["anchors"]:
    content_of[a["id"]] = a["content"]
for s in export["strands"]:
    for m in s["nodes"]:
        content_of.setdefault(m["id"], m["content"])
for aid in [a["id"] for a in export["anchors"]]:
    reg.add(aid, content_of[aid])
strand_ids = {m["id"] for s in export["strands"] for m in s["nodes"]}
for nid in sorted(strand_ids - set(reg.names)):
    reg.add(nid, content_of[nid])
print(f"registry: {len(reg.names)} concepts -> indices 1..{len(reg.names)}")

# --------------------------------------------------------------------------
# session 1: one-time codebook sync
# --------------------------------------------------------------------------
reg_cost = TOK(reg.to_json())
print(f"\nsession 1 (codebook sync, once): {reg_cost} tokens")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def struct_to_export(struct, registry, base_export, default_stab=0.6):
    stab = {}
    for a in base_export["anchors"]:
        stab[a["id"]] = (a["stability"], "anchor")
    for s in base_export["strands"]:
        for m in s["nodes"]:
            stab.setdefault(m["id"], (m["stability"], m["zone"]))
    questions = {l["node"]: l["question"] for l in base_export["open_loops"]}

    def nd(nid, zone):
        s, z = stab.get(nid, (default_stab, zone))
        return {"id": nid, "content": registry.content[nid],
                "stability": s, "zone": z,
                "open_question": questions.get(nid, "")}

    return {
        "anchors": [nd(n, "anchor") for n in struct["anchors"]],
        "strands": [{"id": "strand:" + "+".join(srt),
                     "nodes": [nd(n, "memory") for n in srt],
                     "mean_stability": default_stab}
                    for srt in struct["strands"]],
        "constraints": [{"a": a, "b": b, "weight": 0.8,
                         "rule": f"{a} relates to {b}"}
                        for a, b in struct["edges"]],
        "open_loops": [{"node": n, "zone": "memory",
                        "question": questions.get(n, ""), "activation": 0.5}
                       for n in struct["loops"]],
        "reconstruction_rules": base_export["reconstruction_rules"],
    }


def settle(g, anchors):
    g.step({a: 0.6 for a in anchors})
    g.step({})
    return g


PROBES = ["what was the cython bug", "wheel density reduction",
          "scaling larger primorials findings", "toroidal draft verdict"]


def roundtrip_fidelity(export_a, export_b, anchors):
    ga = settle(Graph.rehydrate(export_a), anchors)
    gb = settle(Graph.rehydrate(export_b), anchors)
    return [(q, ga.probe(q), gb.probe(q)) for q in PROBES]


# --------------------------------------------------------------------------
# session 2: structural message only
# --------------------------------------------------------------------------
primes = first_n_primes(len(reg.names) + 16)
msg = build_message(export, reg, primes)
wire = encode_message(msg)
assert decode_message(wire) == msg, "wire round-trip failed"
struct = decode_struct(decode_message(wire), reg, primes)

# structural fidelity: names must match exactly (anchors, strands, EDGES)
def canon_edges(pairs):
    return sorted(tuple(sorted(p)) for p in pairs)

orig_names = (sorted(a["id"] for a in export["anchors"]),
              sorted(tuple(sorted(m["id"] for m in s["nodes"]))
                     for s in export["strands"]),
              canon_edges((c["a"], c["b"]) for c in export["constraints"]))
rt_names = (sorted(struct["anchors"]),
            sorted(tuple(sorted(s)) for s in struct["strands"]),
            canon_edges(struct["edges"]))
assert orig_names == rt_names, "structural round-trip mismatch"

export_rt = struct_to_export(struct, reg, export)
fidelity = roundtrip_fidelity(
    export, export_rt, [a["id"] for a in export["anchors"]])
agree = sum(1 for _, a, b in fidelity
            if (a is None) == (b is None) and (a is None or a == b))

wire_tok = TOK(wire)
retained = [reg.content[n] for n in reg.names]
base2_tok = TOK("\n\n".join(retained))
print(f"\nsession 2 (structural update, gamma-bit wire):")
print(f"  wire message: {len(msg)} ints -> {len(wire)} symbols -> "
      f"{wire_tok} tokens   e.g. {wire[:64]}...")
print(f"  baseline (raw retransmit {len(retained)} concepts): "
      f"{base2_tok} tokens")
print(f"  fidelity after wire round-trip: {agree}/{len(PROBES)} probes agree")

# --------------------------------------------------------------------------
# session 3: novelty arrives (2 new concepts) + structural update
# --------------------------------------------------------------------------
NEW = {
    "manifold": ("Manifold hypothesis: high-dimensional data concentrates "
                 "near low-dimensional manifolds; relevant to "
                 "coarse-graining questions."),
    "codec_v1": ("CCC codec v1: prime-indexed registry, Godel set products, "
                 "codon wire frames with parity."),
}
for nid, text in NEW.items():
    reg.add(nid, text)
delta_raw = "\n".join(f"[{reg.index(n)}] {n} :: {t}"
                      for n, t in NEW.items())
delta_tok = TOK(delta_raw)

export3 = json.loads(json.dumps(export))  # deep copy
export3["strands"].append({
    "id": "strand:codec_v1+manifold",
    "nodes": [{"id": n, "content": t, "stability": 0.6, "zone": "memory",
               "open_question": ""} for n, t in NEW.items()],
    "mean_stability": 0.6})
export3["constraints"].append({"a": "codec_v1", "b": "ccc", "weight": 0.8,
                               "rule": "codec_v1 relates to ccc"})

primes3 = first_n_primes(len(reg.names) + 16)
msg3 = build_message(export3, reg, primes3)
wire3 = encode_message(msg3)
assert decode_message(wire3) == msg3
wire3_tok = TOK(wire3)
touched = retained + list(NEW.values())
base3_tok = TOK("\n\n".join(touched))
print(f"\nsession 3 (2 novel concepts + structural update):")
print(f"  codec: delta raw {delta_tok} tok + wire {wire3_tok} tok = "
      f"{delta_tok + wire3_tok} tokens")
print(f"  baseline (raw retransmit {len(touched)} concepts): "
      f"{base3_tok} tokens")

# --------------------------------------------------------------------------
# ledger
# --------------------------------------------------------------------------
codec_total = reg_cost + wire_tok + delta_tok + wire3_tok
base_total = base2_tok + base3_tok   # session 1 had no baseline (cold start)
print("\n" + "=" * 64)
print("TOKEN LEDGER (3 sessions)")
print("=" * 64)
print(f"  codec:    sync {reg_cost} + s2 wire {wire_tok} + "
      f"s3 delta {delta_tok} + s3 wire {wire3_tok} = {codec_total}")
print(f"  baseline: s2 {base2_tok} + s3 {base3_tok} = {base_total} "
      f"(session 1 cold start excluded for both)")
print(f"  ratio after 3 sessions: {base_total / codec_total:.2f}x")
# steady-state projection: per-session structural cost ~ wire_tok
steady = wire_tok
base_session = base2_tok
n = 10
proj_codec = reg_cost + n * steady
proj_base = n * base_session
print(f"  projected to 10 sessions: codec {proj_codec} vs "
      f"baseline {proj_base} = {proj_base / proj_codec:.2f}x")
print("=" * 64)
