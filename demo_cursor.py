"""Measure the cursor layer + entropy stages vs the v3 structural baseline.

Setup: B=1000 registry, shared graph = 20 clusters of 50 concepts
(intra-cluster p=0.22, backbone + bridges for connectivity) modeling
accumulated session history. Each message: 10 coherent strand concepts
(8 in-topic + 2 drift) and 7 NEW relations among them. The cursor
persists across messages -- the shared graph densifies as sessions
accumulate, so we also track cost over time.

Baseline is the ACTUAL current codec: build_message ints (prime set
products + packed 0-based edge pairs), gamma-coded. All paths measured
in exact bits; wire cost via pack_bits + cl100k_base tokens.
"""
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tiktoken
from codec import Registry, build_message, first_n_primes, _gamma_enc
import cursor
import entropy

B = 1000
NCL = 20
CLSIZE = B // NCL
NMSG = 120

rng = random.Random(20260927)
enc_tok = tiktoken.get_encoding("cl100k_base")


def gamma_bits(ints):
    return "".join(_gamma_enc(x) for x in ints)


# --- shared registry / primes (both sides hold these) ---
reg = Registry()
names = [f"c{i}" for i in range(B)]
for nm in names:
    reg.add(nm)
primes = first_n_primes(B)


# --- shared history graph: clustered + backbone + bridges ---
def build_graph():
    edges = set()
    for c in range(NCL):
        members = list(range(c * CLSIZE, (c + 1) * CLSIZE))
        for ii in range(len(members)):
            for jj in range(ii + 1, len(members)):
                if rng.random() < 0.22:
                    a, b = members[ii], members[jj]
                    edges.add((min(a, b), max(a, b)))
        if c < NCL - 1:  # backbone keeps the whole graph connected
            edges.add((c * CLSIZE + CLSIZE - 1, (c + 1) * CLSIZE))
    for _ in range(200):
        a, b = rng.randrange(B), rng.randrange(B)
        if a != b:
            edges.add((min(a, b), max(a, b)))
    return edges


edges = build_graph()
enc_st = cursor.CursorState(B)
dec_st = cursor.CursorState(B)
for a, b in edges:
    enc_st.add_edge(a, b)
    dec_st.add_edge(a, b)
e0 = len(edges)


def gen_message(st):
    c = rng.randrange(NCL)
    members = list(range(c * CLSIZE, (c + 1) * CLSIZE))
    S = set(rng.sample(members, 8)) | {rng.randrange(B) for _ in range(2)}
    R, tries = [], 0
    Sl = list(S)
    while len(R) < 7 and tries < 300:
        tries += 1
        a, b = rng.sample(Sl, 2)
        if b in st.adj[a] or (a, b) in R or (b, a) in R:
            continue
        R.append((a, b))
    return S, R


def export_of(S, R):
    return {
        "strands": [{"nodes": [{"id": names[i], "content": ""} for i in S]}],
        "constraints": [{"a": names[a], "b": names[b]} for a, b in R],
        "anchors": [],
        "open_loops": [],
    }


tot = {"base": 0, "cursor": 0, "huff": 0, "lz": 0, "stack": 0}
tok = {"base": 0, "best": 0}
early, late = [], []
n_huff_win = n_lz_win = n_stack_win = 0

for msg in range(NMSG):
    S, R = gen_message(enc_st)

    # baseline: the real current codec path
    base_ints = build_message(export_of(S, R), reg, primes)
    base_bits = gamma_bits(base_ints)

    # cursor layer
    ops = cursor.encode_ops(set(S), list(R), enc_st)
    cur_bits = gamma_bits(ops)

    # entropy stages on the op stream
    h_bits, _ = entropy.huffman_encode(ops)
    toks = entropy.lz77_encode(ops)
    lz_bits = entropy.lz77_fixed_bits(toks)
    s_bits, _ = entropy.huffman_encode(entropy.lz77_tokens_to_ints(toks))

    # decode + lockstep check
    S2, R2 = cursor.decode_ops(ops, dec_st)
    assert S2 == set(S), f"msg {msg}: strands differ"
    assert R2 == list(R), f"msg {msg}: relations differ"
    assert enc_st.snapshot() == dec_st.snapshot(), f"msg {msg}: state drift"

    for k, b in (("base", base_bits), ("cursor", cur_bits), ("huff", h_bits),
                 ("lz", lz_bits), ("stack", s_bits)):
        tot[k] += len(b)
    best_bits = min(cur_bits, h_bits, lz_bits, s_bits, key=len)
    if len(h_bits) < len(cur_bits):
        n_huff_win += 1
    if len(lz_bits) < len(cur_bits):
        n_lz_win += 1
    if len(s_bits) < len(cur_bits):
        n_stack_win += 1
    tok["base"] += len(enc_tok.encode(entropy.pack_bits(base_bits)))
    tok["best"] += len(enc_tok.encode(entropy.pack_bits(best_bits)))
    (early if msg < 20 else late if msg >= NMSG - 20 else []).append(len(cur_bits))

print(f"messages: {NMSG}  B={B}  initial shared edges: {e0}  "
      f"final edges: {sum(len(v) for v in enc_st.adj.values()) // 2}")
print()
print("mean bits/message:")
for k in ("base", "cursor", "huff", "lz", "stack"):
    print(f"  {k:6s} {tot[k] / NMSG:8.1f}   "
          f"ratio vs baseline {tot['base'] / tot[k]:.3f}x")
print()
print(f"cursor bits: first-20 msgs {sum(early) / len(early):.1f}, "
      f"last-20 msgs {sum(late) / len(late):.1f} "
      f"(graph densifies -> walks shorten: "
      f"{sum(early) / sum(late):.3f}x)")
print(f"entropy stage beats raw cursor: huffman {n_huff_win}/{NMSG}, "
      f"lz77 {n_lz_win}/{NMSG}, stacked {n_stack_win}/{NMSG}")
print()
print(f"wire tokens/message: baseline {tok['base'] / NMSG:.1f}, "
      f"best cursor path {tok['best'] / NMSG:.1f} "
      f"({tok['base'] / tok['best']:.3f}x)")
