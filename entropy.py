"""Second-stage coding for CCC -- the "zip the zip" question, answered honestly.

Re-compressing the final bitstream with a generic compressor gains
nothing (high-entropy output). What CAN gain: exploiting residual
structure in the cursor op stream that the graph layer leaves behind:

  A. skew: small ints (opcodes, short hop counts, low edge indices)
     dominate. Canonical Huffman with a transmitted codebook.
  B. motifs: repeated walk patterns (anchor traversals, common paths).
     LZ77 over the integer stream with fixed-cost tokens.
  C. stacked: LZ77 then Huffman over the token stream (the gzip recipe).

All bit counts are exact and include every overhead (codebooks, flag
bits, counts). Nothing is hidden.
"""
from __future__ import annotations
import heapq

from codec import _gamma_enc, _gamma_dec


# --------------------------------------------------------------------------
# canonical Huffman over an integer alphabet; codebook is transmitted
# --------------------------------------------------------------------------
def _huffman_lengths(freq: dict[int, int]) -> dict[int, int]:
    import itertools
    ctr = itertools.count()
    heap = [(f, next(ctr), s) for s, f in freq.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        return {heap[0][2]: 1}
    while len(heap) > 1:
        f1, _, p1 = heapq.heappop(heap)
        f2, _, p2 = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(ctr), (p1, p2)))
    lengths: dict[int, int] = {}

    def walk(node, d: int):
        if isinstance(node, tuple):
            walk(node[0], d + 1)
            walk(node[1], d + 1)
        else:
            lengths[node] = d

    walk(heap[0][2], 0)
    return lengths


def _canonical_codes(lengths: dict[int, int]) -> dict[int, str]:
    ordered = sorted(lengths, key=lambda s: (lengths[s], s))
    codes: dict[int, str] = {}
    code, prev = 0, 0
    for s in ordered:
        ln = lengths[s]
        code <<= ln - prev
        prev = ln
        codes[s] = format(code, f"0{ln}b")
        code += 1
    return codes


def huffman_encode(ints: list[int]) -> tuple[str, int]:
    """-> (full bitstring, header bit length).

    Layout: gamma(n_ints) gamma(n_syms) [gamma(sym) gamma(codelen)]* data.
    The decoder reads n_ints first, so the data needs no terminator.
    """
    n = len(ints)
    freq: dict[int, int] = {}
    for v in ints:
        freq[v] = freq.get(v, 0) + 1
    lengths = _huffman_lengths(freq)
    codes = _canonical_codes(lengths)
    head = _gamma_enc(n) + _gamma_enc(len(freq))
    for s in sorted(freq):
        head += _gamma_enc(s) + _gamma_enc(lengths[s])
    return head + "".join(codes[v] for v in ints), len(head)


def huffman_decode(bits: str) -> list[int]:
    n, pos = _gamma_dec(bits, 0)
    nsym, pos = _gamma_dec(bits, pos)
    lengths: dict[int, int] = {}
    for _ in range(nsym):
        s, pos = _gamma_dec(bits, pos)
        ln, pos = _gamma_dec(bits, pos)
        lengths[s] = ln
    codes = _canonical_codes(lengths)
    trie: dict = {}
    for s, c in codes.items():
        node = trie
        for ch in c:
            node = node.setdefault(ch, {})
        node["$"] = s
    out: list[int] = []
    node = trie
    while len(out) < n:
        node = node[bits[pos]]
        pos += 1
        if "$" in node:
            out.append(node["$"])
            node = trie
    return out


# --------------------------------------------------------------------------
# LZ77 over integer streams
# --------------------------------------------------------------------------
def lz77_encode(ints: list[int], window: int = 4096, min_match: int = 3,
                max_match: int = 258) -> list[tuple]:
    """-> [('L', value) | ('M', dist, length)]. Greedy longest match."""
    toks: list[tuple] = []
    i, n = 0, len(ints)
    while i < n:
        best_len, best_dist = 0, 0
        for j in range(max(0, i - window), i):
            if ints[j] != ints[i]:
                continue
            ln = 0
            while (ln < max_match and i + ln < n
                   and ints[j + ln] == ints[i + ln]):
                ln += 1
            if ln > best_len:
                best_len, best_dist = ln, i - j
                if best_len == max_match:
                    break
        if best_len >= min_match:
            toks.append(("M", best_dist, best_len))
            i += best_len
        else:
            toks.append(("L", ints[i]))
            i += 1
    return toks


def lz77_decode(toks: list[tuple]) -> list[int]:
    out: list[int] = []
    for t in toks:
        if t[0] == "L":
            out.append(t[1])
        else:
            _, dist, ln = t
            for _ in range(ln):
                out.append(out[-dist])
    return out


def lz77_fixed_bits(toks: list[tuple]) -> str:
    """Stage B: fixed-cost tokens. Literal: 0+gamma(v);
    match: 1+gamma(dist)+gamma(length)."""
    parts = []
    for t in toks:
        if t[0] == "L":
            parts.append("0" + _gamma_enc(t[1]))
        else:
            _, dist, ln = t
            parts.append("1" + _gamma_enc(dist) + _gamma_enc(ln))
    return "".join(parts)


def lz77_fixed_decode(bits: str) -> list[int]:
    """Stage B decode: parse flag-prefixed tokens until bits are exhausted,
    then resolve matches. (Framing via pack_bits gives the exact length.)"""
    toks: list[tuple] = []
    pos = 0
    while pos < len(bits):
        flag = bits[pos]
        pos += 1
        if flag == "0":
            v, pos = _gamma_dec(bits, pos)
            toks.append(("L", v))
        elif flag == "1":
            dist, pos = _gamma_dec(bits, pos)
            ln, pos = _gamma_dec(bits, pos)
            toks.append(("M", dist, ln))
        else:
            raise ValueError("bad token flag")
    return lz77_decode(toks)


def lz77_tokens_to_ints(toks: list[tuple]) -> list[int]:
    """Stage C alphabet mapping (invertible): literal v -> 2v;
    match(dist, len) -> 2*(dist*512 + len) + 1 (len < 512)."""
    out = []
    for t in toks:
        if t[0] == "L":
            out.append(2 * t[1])
        else:
            _, dist, ln = t
            assert ln < 512
            out.append(2 * (dist * 512 + ln) + 1)
    return out


def ints_to_lz77_tokens(ints: list[int]) -> list[tuple]:
    toks = []
    for v in ints:
        if v % 2 == 0:
            toks.append(("L", v // 2))
        else:
            m = (v - 1) // 2
            toks.append(("M", m // 512, m % 512))
    return toks


# --------------------------------------------------------------------------
# bitstring <-> digit wire (v3-style framing: [nnn][pad] triples [cksum])
# --------------------------------------------------------------------------
def pack_bits(bits: str) -> str:
    pad = (-len(bits)) % 9
    bits += "0" * pad
    trips = [f"{int(bits[i:i + 9], 2):03d}"
             for i in range(0, len(bits), 9)]
    if len(trips) > 999:
        raise ValueError("message too large for wire header")
    cksum = (len(trips) + pad + sum(int(t) for t in trips)) % 1000
    return f"{len(trips):03d}{pad}" + "".join(trips) + f"{cksum:03d}"


def unpack_bits(s: str) -> str:
    nn, pad = int(s[:3]), int(s[3:4])
    body, expect = s[4:4 + 3 * nn], int(s[4 + 3 * nn:4 + 3 * nn + 3])
    if 4 + 3 * nn + 3 != len(s):
        raise ValueError("bad wire header length")
    if (nn + pad + sum(int(body[i:i + 3])
                       for i in range(0, 3 * nn, 3))) % 1000 != expect:
        raise ValueError("wire checksum mismatch")
    bits = "".join(f"{int(body[i:i + 3]):09b}"
                   for i in range(0, 3 * nn, 3))
    return bits[:-pad] if pad else bits
