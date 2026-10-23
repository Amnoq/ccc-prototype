"""CCC codec v1 — prime-indexed context compression.

Three layers:

  registry  shared concept -> index map. Synchronized once (out of band),
            like DNA's universal codebook: both sides hold it, so content
            strings are never retransmitted. THIS is where the compression
            lives; everything below is wire format.

  structure sets (anchors, strands, open loops) as prime products:
            canonical, order-free, unambiguous by unique factorization.
            Edge pairs packed as small ints in canonical sorted order.
            (Godel-flavored: deterministic on both sides, no codebook sent.)

  wire      integers -> base-64 symbol frames:
              [LEN LEN][digits][PARITY]
            self-delimiting, parity-checked.
            (DNA-flavored: fixed frames + redundancy. The parity symbol is
            error *detection*, honestly labeled -- not true degeneracy.)
"""
from __future__ import annotations

import json
import math
import re

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
BASE = len(ALPHABET)  # 64 symbols, like codon's 64 values
_VAL = {c: i for i, c in enumerate(ALPHABET)}


# --------------------------------------------------------------------------
# primes
# --------------------------------------------------------------------------
def first_n_primes(n: int) -> list[int]:
    if n <= 0:
        return []
    if n < 6:
        bound = 16
    else:
        bound = int(n * (math.log(n) + math.log(math.log(n)))) + 16
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(bound ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = b"\x00" * ((bound - p * p) // p + 1)
    primes = [i for i, v in enumerate(sieve) if v]
    assert len(primes) >= n, "sieve bound too small"
    return primes[:n]


def factorize(n: int, primes: list[int]) -> dict[int, int]:
    """Trial division; callers pass a primes list covering all factors."""
    out: dict[int, int] = {}
    for p in primes:
        if p * p > n:
            break
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


# --------------------------------------------------------------------------
# wire layer: integers <-> framed symbol strings
# --------------------------------------------------------------------------
def int_to_syms(x: int) -> str:
    if x == 0:
        return ALPHABET[0]
    ds = []
    while x:
        ds.append(ALPHABET[x % BASE])
        x //= BASE
    return "".join(reversed(ds))


def syms_to_int(s: str) -> int:
    x = 0
    for c in s:
        x = x * BASE + _VAL[c]
    return x


def encode_frame(x: int) -> str:
    digits = int_to_syms(x)
    n = len(digits)
    assert n < BASE * BASE, "integer too large for 2-symbol length prefix"
    head = ALPHABET[n // BASE] + ALPHABET[n % BASE]
    parity = sum(_VAL[c] for c in head + digits) % BASE
    return head + digits + ALPHABET[parity]


def decode_frame(s: str, pos: int) -> tuple[int, int]:
    n = _VAL[s[pos]] * BASE + _VAL[s[pos + 1]]
    digits = s[pos + 2:pos + 2 + n]
    par = s[pos + 2 + n]
    if sum(_VAL[c] for c in s[pos:pos + 2 + n]) % BASE != _VAL[par]:
        raise ValueError(f"parity mismatch at frame offset {pos}")
    return syms_to_int(digits), pos + 2 + n + 1


def encode_message(ints: list[int]) -> str:
    return encode_frame(len(ints)) + "".join(encode_frame(x) for x in ints)


def decode_message(s: str) -> list[int]:
    count, pos = decode_frame(s, 0)
    out = []
    for _ in range(count):
        x, pos = decode_frame(s, pos)
        out.append(x)
    if pos != len(s):
        raise ValueError("trailing data after message")
    return out


# --------------------------------------------------------------------------
# wire layer v2: decimal-triple encoding (tokenizer-aware)
#
# cl100k_base holds single tokens for every 3-digit group 000-999, so
# base-1000 "triples" ride at ~1 token per 10 bits -- measured 0.33
# tok/char vs 0.54 for the base-64 frames. This layer is deliberately
# tokenizer-specific; the registry and prime layers above it are not.
# Format: [nn][cc ttt...]*[checksum] -- 2-digit int count, per int a
# 2-digit triple count + triples, then a 3-digit checksum (sum of all
# triple values and counts, mod 1000) as the redundancy symbol.
# --------------------------------------------------------------------------
def encode_message_triples(ints: list[int]) -> str:
    if len(ints) > 99:
        raise ValueError("triple wire supports <= 99 ints per message")
    body = ""
    cksum = len(ints)
    for x in ints:
        d = str(x)
        d = d.rjust(((len(d) + 2) // 3) * 3, "0")
        trips = [d[i:i + 3] for i in range(0, len(d), 3)]
        if len(trips) > 99:
            raise ValueError("int too large for triple wire")
        body += f"{len(trips):02d}" + "".join(trips)
        cksum += len(trips) + sum(int(t) for t in trips)
    return f"{len(ints):02d}" + body + f"{cksum % 1000:03d}"


def decode_message_triples(s: str) -> list[int]:
    pos = 0
    n = int(s[pos:pos + 2])
    pos += 2
    out = []
    cksum = n
    for _ in range(n):
        c = int(s[pos:pos + 2])
        pos += 2
        trips = [s[pos + 3 * k:pos + 3 * k + 3] for k in range(c)]
        pos += 3 * c
        cksum += c + sum(int(t) for t in trips)
        out.append(int("".join(trips)))
    expect = int(s[pos:pos + 3])
    pos += 3
    if pos != len(s):
        raise ValueError("trailing data after triple message")
    if expect != cksum % 1000:
        raise ValueError(f"checksum mismatch: {expect} != {cksum % 1000}")
    return out


# --------------------------------------------------------------------------
# wire layer v3: gamma-coded bitstream (variable length)
#
# Fixed-width triples spend tokens on padding zeros and per-int counts --
# both fully predictable. v3 transmits neither: each int is Elias-gamma-
# coded (x -> gamma(x+1), so 0 is encodable and the code self-delimits),
# the bitstream is packed 9 bits per decimal triple, and gamma decoding
# recovers the int list without any transmitted counts. Header:
# [nnn:03d][pad:1d], then triples, then a mod-1000 checksum triple over
# header + triple values. Every digit position has nonzero weight mod
# 1000, so any single-digit flip changes the checksum: single-symbol
# corruption is always detected.
# This is the text-channel version of "omit the predictable symbols":
# nothing predictable is transmitted; framing is reconstructed.
# --------------------------------------------------------------------------
def _gamma_enc(x: int) -> str:
    b = format(x + 1, "b")
    return "0" * (len(b) - 1) + b


def _gamma_dec(bits: str, pos: int) -> tuple[int, int]:
    n = 0
    while True:
        if pos >= len(bits):
            raise ValueError("truncated gamma code")
        if bits[pos] != "0":
            break
        n += 1
        pos += 1
    if pos + n + 1 > len(bits):
        raise ValueError("truncated gamma code")
    return int(bits[pos:pos + n + 1], 2) - 1, pos + n + 1


def encode_message_bits(ints: list[int]) -> str:
    bits = "".join(_gamma_enc(x) for x in ints)
    pad = (-len(bits)) % 9
    bits += "0" * pad
    trips = [f"{int(bits[i:i + 9], 2):03d}"
             for i in range(0, len(bits), 9)]
    if len(trips) > 999:
        raise ValueError("message too large for v3 header")
    cksum = (len(trips) + pad + sum(int(t) for t in trips)) % 1000
    return f"{len(trips):03d}{pad}" + "".join(trips) + f"{cksum:03d}"


def decode_message_bits(s: str) -> list[int]:
    nn, pad = int(s[:3]), int(s[3:4])
    body, expect = s[4:4 + 3 * nn], int(s[4 + 3 * nn:4 + 3 * nn + 3])
    if 4 + 3 * nn + 3 != len(s):
        raise ValueError("bad v3 header length")
    if (nn + pad + sum(int(body[i:i + 3])
                       for i in range(0, 3 * nn, 3))) % 1000 != expect:
        raise ValueError("v3 checksum mismatch")
    bits = "".join(f"{int(body[i:i + 3]):09b}"
                   for i in range(0, 3 * nn, 3))
    bits = bits[:-pad] if pad else bits
    out, pos = [], 0
    while pos < len(bits):
        x, pos = _gamma_dec(bits, pos)
        out.append(x)
    if pos != len(bits):
        raise ValueError("v3 bitstream not exactly consumed")
    return out


# --------------------------------------------------------------------------
# registry: the shared codebook
# --------------------------------------------------------------------------
class Registry:
    """Concept name -> 1-based index. Both sides hold an identical copy."""

    def __init__(self):
        self.names: list[str] = []
        self.content: dict[str, str] = {}

    def add(self, name: str, content: str = "") -> int:
        if name not in self.content:
            self.names.append(name)
            self.content[name] = content
        elif content and not self.content[name]:
            self.content[name] = content
        return self.names.index(name) + 1

    def index(self, name: str) -> int:
        return self.names.index(name) + 1

    def name(self, i: int) -> str:
        if not 1 <= i <= len(self.names):
            raise IndexError(f"concept index {i} out of range "
                             f"(registry holds {len(self.names)})")
        return self.names[i - 1]

    def to_json(self) -> str:
        return json.dumps({"names": self.names, "content": self.content})

    @staticmethod
    def from_json(s: str) -> "Registry":
        d = json.loads(s)
        r = Registry()
        r.names = d["names"]
        r.content = d["content"]
        return r


# --------------------------------------------------------------------------
# structural layer: export dict <-> integer message
# --------------------------------------------------------------------------
def set_product(indices: list[int], primes: list[int]) -> int:
    p = 1
    for i in indices:
        p *= primes[i - 1]
    return p


def build_message(export: dict, registry: Registry,
                  primes: list[int]) -> list[int]:
    """Message layout: [B, nS, S_1..S_nS, nE, c_1..c_nE, A, L]."""
    B = len(registry.names)
    known = set(registry.names)

    strand_prods = []
    for s in export["strands"]:
        idx = sorted(registry.index(m["id"]) for m in s["nodes"]
                     if m["id"] in known)
        strand_prods.append(set_product(idx, primes))

    pairs = set()
    for c in export["constraints"]:
        if c["a"] in known and c["b"] in known:
            i, j = registry.index(c["a"]), registry.index(c["b"])
            # 0-based: c = a*B + b with a,b < B round-trips exactly;
            # 1-based packing (i*B + j) is ambiguous when j == B.
            pairs.add((min(i, j) - 1, max(i, j) - 1))
    edge_ints = sorted(a * B + b for a, b in pairs)

    anchors = sorted(registry.index(a["id"]) for a in export["anchors"]
                     if a["id"] in known)
    loops = sorted(registry.index(l["node"]) for l in export["open_loops"]
                   if l["node"] in known)
    return ([B, len(strand_prods)] + strand_prods +
            [len(edge_ints)] + edge_ints +
            [set_product(anchors, primes), set_product(loops, primes)])


def decode_struct(ints: list[int], registry: Registry,
                  primes: list[int]) -> dict:
    """Integer message -> {strands, edges, anchors, loops} as names."""
    B, pos = ints[0], 1
    if not 1 <= B <= len(registry.names):
        raise ValueError(f"registry size {B} out of range "
                         f"(registry holds {len(registry.names)})")
    prime_to_index = {p: i + 1 for i, p in enumerate(primes)}

    def unproduct(x: int) -> list[str]:
        idx = sorted(prime_to_index[p] for p in factorize(x, primes))
        return [registry.name(i) for i in idx]

    nS = ints[pos]
    pos += 1
    strands = [unproduct(ints[pos + k]) for k in range(nS)]
    pos += nS
    nE = ints[pos]
    pos += 1
    edges = []
    for k in range(nE):
        c = ints[pos + k]
        a, b = c // B, c % B
        if not (0 <= a < B and 0 <= b < B):
            raise ValueError(f"edge int {c} out of range for B={B}")
        edges.append((registry.name(a + 1), registry.name(b + 1)))
    pos += nE
    anchors = unproduct(ints[pos])
    loops = unproduct(ints[pos + 1])
    return {"strands": strands, "edges": edges,
            "anchors": anchors, "loops": loops}


# --------------------------------------------------------------------------
# telomere framing: discoverability + context in the caps
#
# A naked wire assumes a clean channel. Embedded in prose (the realistic
# model-handoff case), the decoder must FIND the message. Telomeres are
# distinctive boundary markers -- impossible to collide with the
# digit-only v3 body -- carrying context (wire version, registry size,
# registry fingerprint, session) in the caps themselves, the way DNA
# telomeres cap a chromosome. Mirrored open/close markers give the
# strand directionality (5'/3'): open = "zz"+ctx, close = ctx+"ZZ".
# --------------------------------------------------------------------------
def registry_fingerprint(reg: "Registry") -> int:
    return sum(ord(c) for n in reg.names for c in n) % 100


def _telomere_ctx(version: int, reg_size: int, reg_fp: int,
                  session: int) -> str:
    assert 0 <= version <= 9 and 0 <= reg_size <= 99
    assert 0 <= reg_fp <= 99 and 0 <= session <= 99
    return f"{version:d}{reg_size:02d}{reg_fp:02d}{session:02d}"


def wrap_telomere(body: str, version: int, reg_size: int, reg_fp: int,
                  session: int) -> str:
    ctx = _telomere_ctx(version, reg_size, reg_fp, session)
    return f"zz{ctx}{body}{ctx}ZZ"


_TELOMERE_RE = re.compile(r"zz(\d{7})(.*?)(\d{7})ZZ", re.DOTALL)


def scan_telomeres(text: str):
    """Yield (ctx, body) for each telomere-wrapped message in text.

    ctx = {version, reg_size, reg_fp, session}. Caps with mismatched
    context are skipped (not a valid chromosome).
    """
    for m in _TELOMERE_RE.finditer(text):
        ctx_o, body, ctx_c = m.group(1), m.group(2), m.group(3)
        if ctx_o != ctx_c:
            continue
        yield ({"version": int(ctx_o[0]),
                "reg_size": int(ctx_o[1:3]),
                "reg_fp": int(ctx_o[3:5]),
                "session": int(ctx_o[5:7])}, body)


# --------------------------------------------------------------------------
# demo helper (not part of the codec proper)
# --------------------------------------------------------------------------
def demo_registry(export: dict) -> "Registry":
    """Deterministic registry from an export dict (demos/tests only)."""
    reg = Registry()
    content_of = {}
    for a in export["anchors"]:
        content_of[a["id"]] = a["content"]
    for s in export["strands"]:
        for m in s["nodes"]:
            content_of.setdefault(m["id"], m["content"])
    for aid in [a["id"] for a in export["anchors"]]:
        reg.add(aid, content_of[aid])
    sids = {m["id"] for s in export["strands"] for m in s["nodes"]}
    for nid in sorted(sids - set(reg.names)):
        reg.add(nid, content_of[nid])
    return reg


# --------------------------------------------------------------------------
# strict structural validation + multi-line transport
# --------------------------------------------------------------------------
def validate_message(ints: list[int], B: int,
                     primes: list[int]) -> bool:
    """Strict structural validation of a decoded integer message.

    Checks: registry size matches the known B, the layout
    [B, nS, strands..., nE, edges..., A, L] is consumed exactly, every
    set product factors into the first-B primes, every edge int unpacks
    into 0-based indices < B. Used to disambiguate error-correction
    candidates.
    """
    if not ints or ints[0] != B:
        return False
    p2i = {p: i + 1 for i, p in enumerate(primes)}

    def ok_product(x: int) -> bool:
        return x >= 1 and all(p in p2i and p2i[p] <= B
                              for p in factorize(x, primes))

    pos = 1
    if pos >= len(ints):
        return False
    nS = ints[pos]
    pos += 1
    if nS < 0 or pos + nS > len(ints):
        return False
    if not all(ok_product(ints[pos + k]) for k in range(nS)):
        return False
    pos += nS
    if pos >= len(ints):
        return False
    nE = ints[pos]
    pos += 1
    if nE < 0 or pos + nE + 2 != len(ints):
        return False
    if any(c < 0 or c // B >= B for c in ints[pos:pos + nE]):
        return False
    return all(ok_product(x) for x in ints[pos + nE:pos + nE + 2])


# --------------------------------------------------------------------------
# multi-line transport: order-independent parallel rehydration
#
# Split the integer message into k chunks; each line is self-describing
# (LL = line index, KK = total lines) and carries a full v4 wire of its
# chunk, so lines decode independently, in any order, in parallel.
# Per-line checksums localize corruption: only the bad line is
# re-examined (or re-requested) and the surviving lines still decode.
# Per-line overhead is constant (~7 tokens), so the economics favor
# scale; at toy scale it roughly doubles the wire.
# --------------------------------------------------------------------------
def _digit_checksum(digits: str) -> str:
    """3-digit mod-1000 checksum over a raw digit string (triple sums).

    Every position has nonzero weight mod 1000 (100/10/1), so any
    single-digit change alters the checksum: single-symbol corruption
    is always detected.
    """
    trips = [digits[i:i + 3] for i in range(0, len(digits), 3)]
    return f"{(len(trips) + sum(int(t) for t in trips)) % 1000:03d}"


def encode_lines(ints: list[int], k: int) -> list[str]:
    assert 1 <= k <= len(ints), "need 1 <= k <= len(ints)"
    n = (len(ints) + k - 1) // k
    lines = []
    for idx in range(k):
        chunk = ints[idx * n:(idx + 1) * n]
        # hcheck binds the header to the body: a corrupted header can no
        # longer masquerade as another line's (duplicate-idx ambiguity).
        core = f"{idx:02d}{k:02d}{encode_message_bits(chunk)}"
        lines.append(core + _digit_checksum(core))
    return lines


def decode_lines(lines: list[str]) -> list[int]:
    """Reassemble lines in any order into the full integer message.

    Each line is verified (header checksum + v4 checksum) and decoded
    independently; raises ValueError on missing/duplicate lines,
    mixed line counts, or failed checksums.
    """
    if not lines:
        raise ValueError("no lines to decode")
    parsed, k = {}, None
    for line in lines:
        if len(line) < 7 or not line[:4].isdigit():
            raise ValueError(f"bad line: {line[:12]!r}")
        idx, kk = int(line[:2]), int(line[2:4])
        k = kk if k is None else k
        if kk != k:
            raise ValueError("mixed line counts in one message")
        if not 0 <= idx < k:
            raise ValueError(f"line index {idx} out of range for k={k}")
        if idx in parsed:
            raise ValueError(f"duplicate line {idx}")
        core, hcheck = line[:-3], line[-3:]
        if _digit_checksum(core) != hcheck:
            raise ValueError(f"line {idx} header checksum mismatch")
        parsed[idx] = decode_message_bits(core[4:])  # independent per line
    missing = sorted(set(range(k)) - set(parsed))
    if missing:
        raise ValueError(f"missing lines: {missing}")
    return [i for idx in sorted(parsed) for i in parsed[idx]]


# --------------------------------------------------------------------------
# product code: a parity line over the data lines (2D error correction)
#
# The k data lines are the rows; the parity line carries, per column,
# P[c] = (-sum of data digits at c) mod 10, so (data sum + P[c]) % 10 == 0
# on every column. The parity line's header is 99KK (LL=99 is impossible
# for a data line since idx < k <= 99). Column order does not matter --
# addition commutes -- so the scheme stays order-independent.
#
# Correction is zero-search: the per-line checksums identify the bad
# ROW, the parity syndrome identifies the bad COLUMN, and the true
# digit is computed directly as (observed - syndrome) mod 10. No
# candidate enumeration. Corrects any single-digit error in a data
# line (body, header, or header-checksum digits); detects multi-digit
# errors and parity corruption.
# --------------------------------------------------------------------------
def parity_line(data_lines: list[str], k: int) -> str:
    width = max(len(l) for l in data_lines)
    padded = [l.ljust(width, "0") for l in data_lines]
    par = "".join(str((-sum(int(l[c]) for l in padded)) % 10)
                  for c in range(width))
    header = f"99{k:02d}"
    return header + par + _digit_checksum(header + par)


def encode_lines_balanced(ints: list[int], max_triples: int = 990) -> list[str]:
    """Multiline transport with weight-balanced chunks.

    encode_lines splits by int COUNT, which clusters heavy ints (strand
    prime-products all sit at the message head) into one overfull line.
    This packs contiguously by gamma-bit weight instead, so every line
    fits the v3 999-triple header regardless of int-size skew. Lines are
    still order-independent (decode_lines reassembles by index).
    """
    budget = max_triples * 9
    chunks, cur, curbits = [], [], 0
    for x in ints:
        b = len(_gamma_enc(x))
        if b > budget:
            raise ValueError(f"single int too large for one line "
                             f"({b} bits)")
        if cur and curbits + b > budget:
            chunks.append(cur)
            cur, curbits = [], 0
        cur.append(x)
        curbits += b
    if cur:
        chunks.append(cur)
    k = len(chunks)
    assert 1 <= k <= 99, "message exceeds 99-line transport"
    lines = []
    for idx, chunk in enumerate(chunks):
        core = f"{idx:02d}{k:02d}{encode_message_bits(chunk)}"
        lines.append(core + _digit_checksum(core))
    return lines


def encode_lines_parity(ints: list[int], k: int) -> list[str]:
    assert 1 <= k <= 99
    data = encode_lines(ints, k)
    return data + [parity_line(data, k)]


def _syndromes(data: list[str], pbody: str, width: int) -> list[int]:
    padded = [ln.ljust(width, "0") for ln in data]
    return [c for c in range(width)
            if (sum(int(p[c]) for p in padded) + int(pbody[c])) % 10]


def decode_lines_parity(lines: list[str]) -> list[int]:
    """Decode k data lines + 1 parity line; correct a single-digit error
    with zero search. Returns the full integer message.

    Correction is zero-search: the per-line header checksum identifies
    the bad ROW (binding header to body, so no duplicate-idx
    ambiguity), the parity syndrome identifies the bad COLUMN, and the
    true digit is computed directly as (observed - syndrome) mod 10 --
    no candidate enumeration. If the parity line itself is lost or
    corrupted while the data is clean, degrades gracefully to plain
    reassembly. Detects (but does not correct): multi-digit errors and
    data corruption without a usable parity line.
    """
    if not lines:
        raise ValueError("no lines to decode")
    parity, data = None, []
    for ln in lines:
        if len(ln) < 7 or not ln[:4].isdigit():
            raise ValueError(f"bad line: {ln[:12]!r}")
        if ln[:2] == "99":
            # parity candidate: the true parity line is the one whose
            # checksum verifies
            if _digit_checksum(ln[:4] + ln[4:-3]) == ln[-3:]:
                if parity is not None:
                    raise ValueError("duplicate parity line")
                parity = ln
            else:
                data.append(ln)  # corrupted data line, handled below
        else:
            data.append(ln)
    if parity is None:
        # parity lost or corrupted: decode the data lines without it
        return decode_lines([ln for ln in data if ln[:2] != "99"])
    if not data:
        raise ValueError("no data lines")
    k = int(parity[2:4])
    pbody, pcheck = parity[4:-3], parity[-3:]
    parity_ok = _digit_checksum(parity[:4] + pbody) == pcheck
    width = len(pbody)
    if parity_ok and width != max(len(l) for l in data):
        raise ValueError("parity width mismatch: corrupted framing")

    good, suspects = {}, []
    for ln in data:
        idx, kk = int(ln[:2]), int(ln[2:4])
        core, hcheck = ln[:-3], ln[-3:]
        header_ok = 0 <= idx < k and kk == k
        hcheck_ok = _digit_checksum(core) == hcheck
        try:
            ints = decode_message_bits(core[4:])
            body_ok = True
        except ValueError:
            ints, body_ok = None, False
        if header_ok and hcheck_ok and body_ok:
            if idx in good:
                raise ValueError(f"duplicate line {idx}")
            good[idx] = ints
        else:
            suspects.append(ln)

    if not suspects:
        if parity_ok:
            bad = _syndromes(data, pbody, width)
            if bad:
                raise ValueError(f"parity mismatch at columns {bad}: "
                                 f"multi-error detected")
        missing = sorted(set(range(k)) - set(good))
        if missing:
            raise ValueError(f"missing lines: {missing}")
        return [i for idx in sorted(good) for i in good[idx]]

    if len(suspects) == 1 and parity_ok:
        sln = suspects[0]
        bad = _syndromes(data, pbody, width)
        if len(bad) == 1:
            c = bad[0]
            if c >= len(sln):
                raise ValueError("syndrome points beyond line length")
            padded = [ln.ljust(width, "0") for ln in data]
            syndrome = (sum(int(p[c]) for p in padded)
                        + int(pbody[c])) % 10
            fixed = (sln[:c] + str((int(sln[c]) - syndrome) % 10)
                     + sln[c + 1:])
            fidx, fkk = int(fixed[:2]), int(fixed[2:4])
            if not (0 <= fidx < k and fkk == k):
                raise ValueError("parity correction produced "
                                 "invalid header")
            fcore, fhcheck = fixed[:-3], fixed[-3:]
            if _digit_checksum(fcore) != fhcheck:
                raise ValueError("parity correction failed header "
                                 "checksum")
            good[fidx] = decode_message_bits(fcore[4:])
            padded2 = [(fixed if ln is sln else ln).ljust(width, "0")
                       for ln in data]
            if any((sum(int(p[c2]) for p in padded2) + int(pbody[c2])) % 10
                   for c2 in range(width)):
                raise ValueError("parity correction failed verification")
            missing = sorted(set(range(k)) - set(good))
            if missing:
                raise ValueError(f"missing lines: {missing}")
            return [i for idx in sorted(good) for i in good[idx]]
        raise ValueError(f"{len(bad)} parity-mismatch columns: "
                         f"not a single error")
    raise ValueError(f"{len(suspects)} suspect lines "
                     f"(parity_ok={parity_ok}): detected, not correctable")


# --------------------------------------------------------------------------
# v5 message: closes the decode-test gaps (strand labels, typed directed
# edges, anchor status payloads). Clean break from v4, selected by the
# telomere version field (5). Wire layer unchanged (any int list).
#
# Layout:
#   [B, nS, L_1, S_1, ..., L_nS, S_nS, nE, c_1..c_nE, nA, p_1..p_nA, Lp]
# - L_i: 1-based registry index of the strand's label concept (0 = unlabeled)
# - S_i: prime product of member 1-based indices (as v4)
# - c_j = (a*B + b)*B + t, 0-based a,b,t < B; t = relation-TYPE concept.
#   Edges are DIRECTED as given in the export (v4 sorted them undirected).
# - p_k = s*B + c, 0-based status concept s and anchor concept c
# - Lp: prime product of open-loop indices (set, as v4)
# Types, labels, statuses are ordinary registry concepts: no side tables,
# the decoder needs nothing beyond the shared registry.
# --------------------------------------------------------------------------
def build_message_v5(export: dict, registry: Registry,
                     primes: list[int]) -> list[int]:
    B = len(registry.names)
    known = set(registry.names)
    out = [B]

    strands = export["strands"]
    out.append(len(strands))
    for s in strands:
        label = s.get("label")
        if label is not None and label not in known:
            raise ValueError(f"strand label {label!r} not in registry")
        li = registry.index(label) if label else 0
        idx = sorted(registry.index(m["id"]) for m in s["nodes"]
                     if m["id"] in known)
        out += [li, set_product(idx, primes)]

    edge_ints, seen = [], set()
    for c in export["constraints"]:
        a, b, t = c["a"], c["b"], c["type"]
        if a in known and b in known and t in known:
            ai, bi, ti = (registry.index(a) - 1, registry.index(b) - 1,
                          registry.index(t) - 1)
            if (ai, bi, ti) not in seen:
                seen.add((ai, bi, ti))
                edge_ints.append((ai * B + bi) * B + ti)
    out += [len(edge_ints)] + sorted(edge_ints)

    ap = []
    for a in export["anchors"]:
        if a["id"] in known and a["status"] in known:
            s = registry.index(a["status"]) - 1
            c_ = registry.index(a["id"]) - 1
            ap.append(s * B + c_)
    out += [len(ap)] + sorted(ap)

    loops = sorted(registry.index(l["node"]) for l in export["open_loops"]
                   if l["node"] in known)
    out.append(set_product(loops, primes))
    return out


def decode_struct_v5(ints: list[int], registry: Registry,
                     primes: list[int]) -> dict:
    """v5 integer message -> strands (labeled), typed directed edges,
    anchors (with status), loops, all as names."""
    B, pos = ints[0], 1
    if not 1 <= B <= len(registry.names):
        raise ValueError(f"registry size {B} out of range "
                         f"(registry holds {len(registry.names)})")
    prime_to_index = {p: i + 1 for i, p in enumerate(primes)}

    def unproduct(x: int) -> list[str]:
        idx = sorted(prime_to_index[p] for p in factorize(x, primes))
        return [registry.name(i) for i in idx]

    nS = ints[pos]
    pos += 1
    strands = []
    for _ in range(nS):
        li, code = ints[pos], ints[pos + 1]
        pos += 2
        if not 0 <= li <= B:
            raise ValueError(f"strand label index {li} out of range")
        strands.append({"label": registry.name(li) if li else None,
                        "members": unproduct(code)})

    nE = ints[pos]
    pos += 1
    edges = []
    for k in range(nE):
        c = ints[pos + k]
        t, ab = c % B, c // B
        a, b = ab // B, ab % B
        if not (0 <= a < B and 0 <= b < B and 0 <= t < B):
            raise ValueError(f"edge int {c} out of range for B={B}")
        edges.append((registry.name(a + 1), registry.name(t + 1),
                      registry.name(b + 1)))
    pos += nE

    nA = ints[pos]
    pos += 1
    anchors = []
    for k in range(nA):
        p = ints[pos + k]
        s, c_ = p // B, p % B
        if not (0 <= s < B and 0 <= c_ < B):
            raise ValueError(f"anchor int {p} out of range for B={B}")
        anchors.append((registry.name(c_ + 1), registry.name(s + 1)))
    pos += nA

    loops = unproduct(ints[pos])
    return {"strands": strands, "edges": edges,
            "anchors": anchors, "loops": loops}


def validate_message_v5(ints: list[int], B: int,
                        primes: list[int]) -> list[int]:
    """Structural validation for v5 (mirrors validate_message for v4)."""
    if not ints or ints[0] != B:
        raise ValueError("v5: bad B header")
    pos, nS = 1, ints[1]
    pos += 1
    for _ in range(nS):
        li = ints[pos]
        if not 0 <= li <= B:
            raise ValueError(f"v5: label index {li} out of range")
        pos += 2  # label + product (product validated on factor)
    nE = ints[pos]
    pos += 1
    for k in range(nE):
        c = ints[pos + k]
        if not 0 <= c < B ** 3:
            raise ValueError(f"v5: edge int {c} out of range")
    pos += nE
    nA = ints[pos]
    pos += 1
    for k in range(nA):
        if not 0 <= ints[pos + k] < B ** 2:
            raise ValueError("v5: anchor int out of range")
    pos += nA + 1  # anchors + loops product
    if pos != len(ints):
        raise ValueError("v5: trailing ints")
    return ints


# --------------------------------------------------------------------------
# v6 message: adds the anchor-note channel and status-annotated entities
# with temporal validity (decision tree Node 13, corpus_runs/V6_DESIGN.md).
# Clean break from v5, selected by the envelope version field (6).
#
# The message is an int stream PLUS a note text section. Notes are TEXT
# and ride as text: forcing them through the integer/triplet channel
# costs ~3.5x per byte (1 token per 9 bits vs ~1 per 32 as text) and
# blew the wire past the injection it was meant to undercut (measured
# BE_wire 3.21 with bit-packed notes vs 2.26 injection). Text-as-text
# is also simpler for independent decoders.
#
# Int stream layout:
#   [6, B, E, nS, L_1, S_1, ..., nE, c_1..c_nE, nA, a_1..a_nA,
#    nN, len_1..len_nN, nT, q_1..q_nT, Lp]
# - a_k = (s*B + c)*B + n: s = status enum 0..5 (STRUCTURAL, not a registry
#   concept), c = 0-based anchor concept, n = 1-based note index (0 = none)
# - len_m: CHARACTER length of note m (notes deduped first-seen)
# - q_r = ((s*E + f)*E + u)*B + c: s = status enum, f = valid-from epoch
#   (1..E-1), u = valid-until epoch (0 = unbounded), c = 0-based concept
# - E: epoch base, carried in the header
#
# Wire body: NNNN(4) + P(1) + triplets + NOTETEXT + cksum(3), where the
# triplets carry gamma(ints) pad-to-9, NOTETEXT is the concatenated note
# characters (sum(len_m) chars), and cksum covers triplets AND notetext:
#   cksum = (NNNN + P + sum(triplets) + sum(ord(c) for c in notetext)) % 1000
# The telomere envelope declares version 6, so the 4-digit header (v6
# raised the v3 999-triplet ceiling to 9999) is unambiguous.
# --------------------------------------------------------------------------

# v6 epistemic-status enum (structural; see V6_DESIGN.md)
V6_UNSTATED = 0
V6_HYPOTHESIZED = 1
V6_ASSERTED = 2
V6_VERIFIED = 3
V6_KILLED = 4
V6_SUPERSEDED = 5
V6_STATUS_NAMES = ("unstated", "hypothesized", "asserted",
                   "verified", "killed", "superseded")

# string -> enum map for pre-v6 exports (forward contract: the extractor
# emits enum-compatible statuses directly)
V6_STATUS_FROM_STRING = {
    "verified": V6_VERIFIED,
    "asserted": V6_ASSERTED,
    "open_question": V6_HYPOTHESIZED,
    "hypothesized": V6_HYPOTHESIZED,
    "superseded": V6_SUPERSEDED,
    "killed": V6_KILLED,
    "rejected": V6_KILLED,
    "refuted": V6_KILLED,
}


def v6_status_of(status_str) -> int:
    """Map a legacy status string to the v6 enum (0 if unknown)."""
    if isinstance(status_str, int) and 0 <= status_str <= 5:
        return status_str
    return V6_STATUS_FROM_STRING.get(status_str, V6_UNSTATED)


def _v6_entity_statuses(export: dict, epoch: int) -> list[tuple[int, int, int]]:
    """Derive per-concept (status, valid_from, valid_until) from the
    export's anchors. Terminal beats live; else strongest live wins.
    Returns [(concept_0based, s, f, u)] with u=0 (unbounded)."""
    per_concept: dict[int, list[int]] = {}
    # export anchors here carry 0-based concept index + enum status
    for c0, s in export["_anchor_pairs"]:
        per_concept.setdefault(c0, []).append(s)
    out = []
    for c0, ss in per_concept.items():
        term = [s for s in ss if s >= V6_KILLED]
        s = max(term) if term else max(ss)
        out.append((c0, s, epoch, 0))
    return out


def build_message_v6(export: dict, registry: Registry,
                     primes: list[int], epoch: int = 1):
    """v6 message -> (ints, notes). `export` is the v5 export shape plus
    `note` (str or None) on each anchor. `epoch` >= 1 is the validity
    epoch this message establishes (E = epoch + 1). `notes` is the
    deduped note table (str), first-seen order; anchors index it 1-based."""
    if epoch < 1:
        raise ValueError("v6: epoch must be >= 1")
    B = len(registry.names)
    E = epoch + 1
    known = set(registry.names)
    out = [6, B, E]

    strands = export["strands"]
    out.append(len(strands))
    for s in strands:
        label = s.get("label")
        if label is not None and label not in known:
            raise ValueError(f"strand label {label!r} not in registry")
        li = registry.index(label) if label else 0
        idx = sorted(registry.index(m["id"]) for m in s["nodes"]
                     if m["id"] in known)
        out += [li, set_product(idx, primes)]

    edge_ints, seen = [], set()
    for c in export["constraints"]:
        a, b, t = c["a"], c["b"], c["type"]
        if a in known and b in known and t in known:
            ai, bi, ti = (registry.index(a) - 1, registry.index(b) - 1,
                          registry.index(t) - 1)
            if (ai, bi, ti) not in seen:
                seen.add((ai, bi, ti))
                edge_ints.append((ai * B + bi) * B + ti)
    out += [len(edge_ints)] + sorted(edge_ints)

    # notes: dedupe first-seen, 1-based indices
    note_table: list[str] = []
    note_index: dict[str, int] = {}
    anchor_pairs = []  # (concept_0based, status_enum)
    anchor_ints = []
    for a in export["anchors"]:
        if a["id"] not in known:
            continue
        c0 = registry.index(a["id"]) - 1
        s = v6_status_of(a.get("status"))
        note = a.get("note")
        n = 0
        if note:
            if note not in note_index:
                note_index[note] = len(note_table) + 1
                note_table.append(note)
            n = note_index[note]
        anchor_pairs.append((c0, s))
        anchor_ints.append((s * B + c0) * B + n)
    export["_anchor_pairs"] = anchor_pairs
    out += [len(anchor_ints)] + sorted(anchor_ints)

    out += [len(note_table)]
    out += [len(w) for w in note_table]  # character lengths

    statuses = _v6_entity_statuses(export, epoch)
    out += [len(statuses)]
    for c0, s, f, u in sorted(statuses):
        out.append(((s * E + f) * E + u) * B + c0)

    loops = sorted(registry.index(l["node"]) for l in export["open_loops"]
                   if l["node"] in known)
    out.append(set_product(loops, primes))
    return out, note_table


def _encode_wire_body(ints: list[int], notes: list[str]) -> str:
    """Shared v6/v7 wire body: NNNN(4) + P(1) + triplets + NOTETEXT +
    cksum(3). The int-stream layout is version-selected by the stream's
    own first int; the body framing is identical."""
    bits = "".join(_gamma_enc(x) for x in ints)
    pad = (-len(bits)) % 9
    bits += "0" * pad
    trips = [f"{int(bits[i:i + 9], 2):03d}"
             for i in range(0, len(bits), 9)]
    if len(trips) > 9999:
        raise ValueError("message too large for v6/v7 triplet header")
    notetext = "".join(notes)
    cksum = (len(trips) + pad + sum(int(t) for t in trips)
             + sum(ord(c) for c in notetext)) % 1000
    return (f"{len(trips):04d}{pad}" + "".join(trips) + notetext
            + f"{cksum:03d}")


def encode_wire_v6(ints: list[int], notes: list[str]) -> str:
    """v6 int stream + note text -> wire body.

    body = NNNN(4) + P(1) + triplets + NOTETEXT + cksum(3).
    triplets = gamma(ints) padded to a multiple of 9 bits, 9 bits each.
    NOTETEXT = concatenated note characters (sum of in-stream len_m).
    cksum covers triplets AND notetext (notes are evidence; they get
    integrity too).
    """
    return _encode_wire_body(ints, notes)


def _decode_wire_body(body: str, version: int):
    """Shared v6/v7 wire-body decoder. Layout-aware: parse the 4-digit
    header, gamma-decode the int stream per the layout (counts
    nS/nE/nA/nN/nT are in-stream), then slice NOTETEXT using the
    in-stream character lengths, then verify total length and the
    checksum (which covers triplets and notetext)."""
    NNNN, P = int(body[0:4]), int(body[4])
    trip_end = 5 + 3 * NNNN
    trips = [int(body[5 + 3 * i:8 + 3 * i]) for i in range(NNNN)]
    bits = "".join(format(t, "09b") for t in trips)
    bits = bits[:len(bits) - P] if P else bits

    ints, pos = [], 0

    def rd():
        nonlocal pos
        x, pos = _gamma_dec(bits, pos)
        ints.append(x)
        return x

    assert rd() == version, f"v{version}: bad version header"
    B, E = rd(), rd()
    nS = rd()
    for _ in range(nS):
        rd()
        rd()
    nE = rd()
    for _ in range(nE):
        rd()
    nA = rd()
    for _ in range(nA):
        rd()
    nN = rd()
    lens = [rd() for _ in range(nN)]
    nT = rd()
    for _ in range(nT):
        rd()
    rd()  # Lp
    note_len = sum(lens)
    notetext = body[trip_end:trip_end + note_len]
    if len(notetext) != note_len:
        raise ValueError(f"v{version}: truncated note text")
    cksum = body[trip_end + note_len:]
    if len(body) != trip_end + note_len + 3:
        raise ValueError(f"v{version}: body length mismatch")
    expect = (NNNN + P + sum(trips)
              + sum(ord(c) for c in notetext)) % 1000
    if expect != int(cksum):
        raise ValueError(f"v{version}: checksum mismatch")
    notes = []
    p = 0
    for ln in lens:
        notes.append(notetext[p:p + ln])
        p += ln
    return ints, notes


def decode_wire_v6(body: str):
    """Wire body -> (ints, notes). Inverse of encode_wire_v6.

    Layout-aware: parse the 4-digit header, gamma-decode the int stream
    per the v6 layout (counts nS/nE/nA/nN/nT are in-stream), then slice
    NOTETEXT using the in-stream character lengths, then verify total
    length and the checksum (which covers triplets and notetext)."""
    return _decode_wire_body(body, 6)


def decode_struct_v6(ints: list[int], notes: list[str], registry: Registry,
                     primes: list[int]) -> dict:
    """v6 (ints, notes) -> strands, typed directed edges,
    anchors (concept, status-enum-name, note or None), entity statuses
    [(concept, status, valid_from, valid_until)], loops — as names."""
    if not ints or ints[0] != 6:
        raise ValueError("v6: bad version header")
    B, E, pos = ints[1], ints[2], 3
    if not 1 <= B <= len(registry.names):
        raise ValueError(f"registry size {B} out of range "
                         f"(registry holds {len(registry.names)})")
    if E < 1:
        raise ValueError(f"v6: bad epoch base {E}")
    prime_to_index = {p: i + 1 for i, p in enumerate(primes)}

    def unproduct(x: int) -> list[str]:
        idx = sorted(prime_to_index[p] for p in factorize(x, primes))
        return [registry.name(i) for i in idx]

    nS = ints[pos]
    pos += 1
    strands = []
    for _ in range(nS):
        li, code = ints[pos], ints[pos + 1]
        pos += 2
        if not 0 <= li <= B:
            raise ValueError(f"strand label index {li} out of range")
        strands.append({"label": registry.name(li) if li else None,
                        "members": unproduct(code)})

    nE = ints[pos]
    pos += 1
    edges = []
    for k in range(nE):
        c = ints[pos + k]
        t, ab = c % B, c // B
        a, b = ab // B, ab % B
        if not (0 <= a < B and 0 <= b < B and 0 <= t < B):
            raise ValueError(f"edge int {c} out of range for B={B}")
        edges.append((registry.name(a + 1), registry.name(t + 1),
                      registry.name(b + 1)))
    pos += nE

    nA = ints[pos]
    pos += 1
    anchor_ints = ints[pos:pos + nA]
    pos += nA

    nN = ints[pos]
    pos += 1
    if nN != len(notes):
        raise ValueError(f"v6: note count {nN} != {len(notes)} supplied")
    lens = ints[pos:pos + nN]
    for w, ln in zip(notes, lens):
        if len(w) != ln:
            raise ValueError("v6: note length mismatch")
    pos += nN

    anchors = []
    for ak in anchor_ints:
        n = ak % B
        s, c0 = divmod(ak // B, B)
        if not (0 <= s <= 5 and 0 <= c0 < B and 0 <= n <= nN):
            raise ValueError(f"v6: anchor int {ak} out of range")
        anchors.append({"concept": registry.name(c0 + 1),
                        "status": V6_STATUS_NAMES[s],
                        "note": notes[n - 1] if n else None})

    nT = ints[pos]
    pos += 1
    entity_status = []
    for k in range(nT):
        q = ints[pos + k]
        c0 = q % B
        q //= B
        u = q % E
        q //= E
        f = q % E
        s = q // E
        if not (0 <= s <= 5 and 1 <= f < E and 0 <= u < E
                and 0 <= c0 < B):
            raise ValueError("v6: status int out of range")
        entity_status.append({"concept": registry.name(c0 + 1),
                              "status": V6_STATUS_NAMES[s],
                              "valid_from": f,
                              "valid_until": u or None})
    pos += nT

    loops = unproduct(ints[pos])
    pos += 1
    if pos != len(ints):
        raise ValueError("v6: trailing ints")
    return {"strands": strands, "edges": edges, "anchors": anchors,
            "entity_status": entity_status, "loops": loops}


def validate_message_v6(ints: list[int], B: int, E: int,
                        primes: list[int]) -> list[int]:
    """Structural validation for the v6 int stream (note bytes validated
    against in-stream lengths by decode_struct_v6 / decode_wire_v6)."""
    if not ints or ints[0] != 6:
        raise ValueError("v6: bad version header")
    if ints[1] != B:
        raise ValueError("v6: bad B header")
    if ints[2] != E:
        raise ValueError("v6: bad E header")
    pos, nS = 3, ints[3]
    pos += 1
    for _ in range(nS):
        li = ints[pos]
        if not 0 <= li <= B:
            raise ValueError(f"v6: label index {li} out of range")
        pos += 2  # label + product (product validated on factor)
    nE = ints[pos]
    pos += 1
    for k in range(nE):
        c = ints[pos + k]
        if not 0 <= c < B ** 3:
            raise ValueError(f"v6: edge int {c} out of range")
    pos += nE
    nA = ints[pos]
    pos += 1
    anchor_start = pos
    pos += nA
    nN = ints[pos]
    pos += 1
    for k in range(nA):
        ak = ints[anchor_start + k]
        # ak = (s*B + c)*B + n: decompose exactly, as the decoder does
        n = ak % B
        s, c = divmod(ak // B, B)
        if not (0 <= ak and 0 <= s <= 5 and 0 <= c < B and 0 <= n <= nN):
            raise ValueError("v6: anchor int out of range")
    for k in range(nN):
        ln = ints[pos + k]
        if ln <= 0:
            raise ValueError("v6: note length out of range")
    pos += nN
    nT = ints[pos]
    pos += 1
    for k in range(nT):
        q = ints[pos + k]
        # q = ((s*E + f)*E + u)*B + c: decompose exactly
        c0 = q % B
        q //= B
        u = q % E
        q //= E
        f = q % E
        s = q // E
        if not (0 <= ints[pos + k] and 0 <= s <= 5 and 1 <= f < E
                and 0 <= u < E and 0 <= c0 < B):
            raise ValueError("v6: status int out of range")
    pos += nT + 1  # status records + loops product
    if pos != len(ints):
        raise ValueError("v6: trailing ints")
    return ints


def _v6_status_rank(s: int) -> int:
    """Merge-lattice rank: terminal beats live at equal epoch."""
    return s  # enum order already encodes it: 5>4>3>2>1>0


def apply_entity_status(table: dict, records: list[tuple]) -> dict:
    """Resident merge lattice (V6_DESIGN.md): fold per-message entity
    status records into the receiver's status table. `records` are
    (concept_name, status_enum, valid_from, valid_until_or_None).
    Newer epoch wins; ties break toward terminal, then stronger live.
    Returns the updated table."""
    for name, s, f, u in records:
        cur = table.get(name)
        if (cur is None or f > cur[1]
                or (f == cur[1] and _v6_status_rank(s) > _v6_status_rank(cur[0]))):
            table[name] = (s, f, u)
    return table


# --------------------------------------------------------------------------
# v7 message: status-enum alignment to the work's own epistemic labels
# (decision tree Node 17, corpus_runs/V7_STATUS_DESIGN.md). Clean break
# from v6, selected by the envelope version field (7).
#
# v6's invented enum (unstated/hypothesized/asserted/verified/killed/
# superseded) collapsed the work's sharpest distinction -- exact
# (theorem/identity, proof carried) vs computationally verified (numeric
# check passed, scope stated) -- into one "verified", and had no room
# for the genre half of his labels ("reframed, not a new theorem").
# v7 speaks his labels: strength is an ordinal (his four terms +
# unstated + two terminals); genre is a separate anchor-level field (it
# is not an ordinal: a reframing is neither stronger nor weaker than a
# numeric check, it is a different kind of claim).
#
# Int stream layout is v6's with two changes:
# - first int 7 (version);
# - anchors pack (strength, genre): a_k = ((s*G + g)*B + c)*B + n, G = 4.
# Entity-status records keep v6's shape (strength-only, so the merge
# lattice stays one-dimensional); s now ranges 0..6.
# Wire body framing is identical to v6 (shared _encode/_decode_wire_body).
# --------------------------------------------------------------------------

V7_UNSTATED = 0
V7_HEURISTIC = 1
V7_CONJECTURAL = 2
V7_VERIFIED_NUMERIC = 3
V7_EXACT = 4
V7_KILLED = 5
V7_SUPERSEDED = 6
V7_STATUS_NAMES = ("unstated", "heuristic", "conjectural",
                   "verified-numeric", "exact", "killed", "superseded")

V7_GENRE_NONE = 0
V7_GENRE_ORIGINAL = 1
V7_GENRE_REFRAMED = 2
V7_GENRE_IDENTIFICATION = 3
V7_GENRE_NAMES = ("none", "original", "reframed", "identification")
V7_NGENRES = 4

# legacy string -> v7 strength. Lossy-conservative by design (see
# V7_STATUS_DESIGN.md): "verified" maps to verified-numeric, never to
# exact -- the codec may not conclude more than was established.
# "open_question"/"hypothesized" map to unstated: questions are not
# claims, and v7 does not rank them on the strength ordinal (the
# question text rides in the note).
V7_STATUS_FROM_STRING = {
    "exact": V7_EXACT,
    "derived": V7_EXACT,
    "computationally_verified": V7_VERIFIED_NUMERIC,
    "computationally-verified": V7_VERIFIED_NUMERIC,
    "verified": V7_VERIFIED_NUMERIC,
    "conjectural": V7_CONJECTURAL,
    "asserted": V7_CONJECTURAL,
    "heuristic": V7_HEURISTIC,
    "superseded": V7_SUPERSEDED,
    "killed": V7_KILLED,
    "rejected": V7_KILLED,
    "refuted": V7_KILLED,
}

V7_GENRE_FROM_STRING = {
    "original": V7_GENRE_ORIGINAL,
    "reframed": V7_GENRE_REFRAMED,
    "identification": V7_GENRE_IDENTIFICATION,
}


def v7_status_of(status_str) -> int:
    """Map a legacy status string to the v7 strength enum (0 if unknown)."""
    if isinstance(status_str, int) and 0 <= status_str <= 6:
        return status_str
    return V7_STATUS_FROM_STRING.get(status_str, V7_UNSTATED)


def v7_genre_of(genre_str) -> int:
    """Map a genre string to the v7 genre enum (0 if unknown/absent)."""
    if isinstance(genre_str, int) and 0 <= genre_str < V7_NGENRES:
        return genre_str
    return V7_GENRE_FROM_STRING.get(genre_str, V7_GENRE_NONE)


def _v7_entity_statuses(export: dict, epoch: int) -> list[tuple[int, int, int]]:
    """Derive per-concept (strength, valid_from, valid_until) from the
    export's anchors. Terminal beats live; else strongest live wins.
    Returns [(concept_0based, s, f, u)] with u=0 (unbounded)."""
    per_concept: dict[int, list[int]] = {}
    for c0, s in export["_anchor_pairs"]:
        per_concept.setdefault(c0, []).append(s)
    out = []
    for c0, ss in per_concept.items():
        term = [s for s in ss if s >= V7_KILLED]
        s = max(term) if term else max(ss)
        out.append((c0, s, epoch, 0))
    return out


def build_message_v7(export: dict, registry: Registry,
                     primes: list[int], epoch: int = 1):
    """v7 message -> (ints, notes). `export` is the v6 export shape plus
    optional `genre` (str or None) on each anchor. `epoch` >= 1 is the
    validity epoch this message establishes (E = epoch + 1). `notes` is
    the deduped note table (str), first-seen order; anchors index it
    1-based."""
    if epoch < 1:
        raise ValueError("v7: epoch must be >= 1")
    B = len(registry.names)
    E = epoch + 1
    known = set(registry.names)
    out = [7, B, E]

    strands = export["strands"]
    out.append(len(strands))
    for s in strands:
        label = s.get("label")
        if label is not None and label not in known:
            raise ValueError(f"strand label {label!r} not in registry")
        li = registry.index(label) if label else 0
        idx = sorted(registry.index(m["id"]) for m in s["nodes"]
                     if m["id"] in known)
        out += [li, set_product(idx, primes)]

    edge_ints, seen = [], set()
    for c in export["constraints"]:
        a, b, t = c["a"], c["b"], c["type"]
        if a in known and b in known and t in known:
            ai, bi, ti = (registry.index(a) - 1, registry.index(b) - 1,
                          registry.index(t) - 1)
            if (ai, bi, ti) not in seen:
                seen.add((ai, bi, ti))
                edge_ints.append((ai * B + bi) * B + ti)
    out += [len(edge_ints)] + sorted(edge_ints)

    # notes: dedupe first-seen, 1-based indices
    note_table: list[str] = []
    note_index: dict[str, int] = {}
    anchor_pairs = []  # (concept_0based, strength_enum)
    anchor_ints = []
    for a in export["anchors"]:
        if a["id"] not in known:
            continue
        c0 = registry.index(a["id"]) - 1
        s = v7_status_of(a.get("status"))
        g = v7_genre_of(a.get("genre"))
        note = a.get("note")
        n = 0
        if note:
            if note not in note_index:
                note_index[note] = len(note_table) + 1
                note_table.append(note)
            n = note_index[note]
        anchor_pairs.append((c0, s))
        anchor_ints.append(((s * V7_NGENRES + g) * B + c0) * B + n)
    export["_anchor_pairs"] = anchor_pairs
    out += [len(anchor_ints)] + sorted(anchor_ints)

    out += [len(note_table)]
    out += [len(w) for w in note_table]  # character lengths

    statuses = _v7_entity_statuses(export, epoch)
    out += [len(statuses)]
    for c0, s, f, u in sorted(statuses):
        out.append(((s * E + f) * E + u) * B + c0)

    loops = sorted(registry.index(l["node"]) for l in export["open_loops"]
                   if l["node"] in known)
    out.append(set_product(loops, primes))
    return out, note_table


def encode_wire_v7(ints: list[int], notes: list[str]) -> str:
    """v7 int stream + note text -> wire body. Framing identical to v6."""
    return _encode_wire_body(ints, notes)


def decode_wire_v7(body: str):
    """Wire body -> (ints, notes). Inverse of encode_wire_v7."""
    return _decode_wire_body(body, 7)


def decode_struct_v7(ints: list[int], notes: list[str], registry: Registry,
                     primes: list[int]) -> dict:
    """v7 (ints, notes) -> strands, typed directed edges,
    anchors (concept, status-name, genre-name, note or None),
    entity statuses [(concept, status, valid_from, valid_until)],
    loops — as names."""
    if not ints or ints[0] != 7:
        raise ValueError("v7: bad version header")
    B, E, pos = ints[1], ints[2], 3
    if not 1 <= B <= len(registry.names):
        raise ValueError(f"registry size {B} out of range "
                         f"(registry holds {len(registry.names)})")
    if E < 1:
        raise ValueError(f"v7: bad epoch base {E}")
    prime_to_index = {p: i + 1 for i, p in enumerate(primes)}

    def unproduct(x: int) -> list[str]:
        idx = sorted(prime_to_index[p] for p in factorize(x, primes))
        return [registry.name(i) for i in idx]

    nS = ints[pos]
    pos += 1
    strands = []
    for _ in range(nS):
        li, code = ints[pos], ints[pos + 1]
        pos += 2
        if not 0 <= li <= B:
            raise ValueError(f"strand label index {li} out of range")
        strands.append({"label": registry.name(li) if li else None,
                        "members": unproduct(code)})

    nE = ints[pos]
    pos += 1
    edges = []
    for k in range(nE):
        c = ints[pos + k]
        t, ab = c % B, c // B
        a, b = ab // B, ab % B
        if not (0 <= a < B and 0 <= b < B and 0 <= t < B):
            raise ValueError(f"edge int {c} out of range for B={B}")
        edges.append((registry.name(a + 1), registry.name(t + 1),
                      registry.name(b + 1)))
    pos += nE

    nA = ints[pos]
    pos += 1
    anchor_ints = ints[pos:pos + nA]
    pos += nA

    nN = ints[pos]
    pos += 1
    if nN != len(notes):
        raise ValueError(f"v7: note count {nN} != {len(notes)} supplied")
    lens = ints[pos:pos + nN]
    for w, ln in zip(notes, lens):
        if len(w) != ln:
            raise ValueError("v7: note length mismatch")
    pos += nN

    anchors = []
    for ak in anchor_ints:
        # ak = ((s*G + g)*B + c)*B + n: decompose exactly, as the
        # decoder does
        n = ak % B
        w = ak // B
        c0 = w % B
        v = w // B
        g = v % V7_NGENRES
        s = v // V7_NGENRES
        if not (0 <= s <= 6 and 0 <= g < V7_NGENRES
                and 0 <= c0 < B and 0 <= n <= nN):
            raise ValueError(f"v7: anchor int {ak} out of range")
        anchors.append({"concept": registry.name(c0 + 1),
                        "status": V7_STATUS_NAMES[s],
                        "genre": V7_GENRE_NAMES[g],
                        "note": notes[n - 1] if n else None})

    nT = ints[pos]
    pos += 1
    entity_status = []
    for k in range(nT):
        q = ints[pos + k]
        c0 = q % B
        q //= B
        u = q % E
        q //= E
        f = q % E
        s = q // E
        if not (0 <= s <= 6 and 1 <= f < E and 0 <= u < E
                and 0 <= c0 < B):
            raise ValueError("v7: status int out of range")
        entity_status.append({"concept": registry.name(c0 + 1),
                              "status": V7_STATUS_NAMES[s],
                              "valid_from": f,
                              "valid_until": u or None})
    pos += nT

    loops = unproduct(ints[pos])
    pos += 1
    if pos != len(ints):
        raise ValueError("v7: trailing ints")
    return {"strands": strands, "edges": edges, "anchors": anchors,
            "entity_status": entity_status, "loops": loops}


def validate_message_v7(ints: list[int], B: int, E: int,
                        primes: list[int]) -> list[int]:
    """Structural validation for the v7 int stream (note bytes validated
    against in-stream lengths by decode_struct_v7 / decode_wire_v7)."""
    if not ints or ints[0] != 7:
        raise ValueError("v7: bad version header")
    if ints[1] != B:
        raise ValueError("v7: bad B header")
    if ints[2] != E:
        raise ValueError("v7: bad E header")
    pos, nS = 3, ints[3]
    pos += 1
    for _ in range(nS):
        li = ints[pos]
        if not 0 <= li <= B:
            raise ValueError(f"v7: label index {li} out of range")
        pos += 2  # label + product (product validated on factor)
    nE = ints[pos]
    pos += 1
    for k in range(nE):
        c = ints[pos + k]
        if not 0 <= c < B ** 3:
            raise ValueError(f"v7: edge int {c} out of range")
    pos += nE
    nA = ints[pos]
    pos += 1
    anchor_start = pos
    pos += nA
    nN = ints[pos]
    pos += 1
    for k in range(nA):
        ak = ints[anchor_start + k]
        # ak = ((s*G + g)*B + c)*B + n: decompose exactly
        n = ak % B
        w = ak // B
        c = w % B
        v = w // B
        g = v % V7_NGENRES
        s = v // V7_NGENRES
        if not (0 <= ak and 0 <= s <= 6 and 0 <= g < V7_NGENRES
                and 0 <= c < B and 0 <= n <= nN):
            raise ValueError("v7: anchor int out of range")
    for k in range(nN):
        ln = ints[pos + k]
        if ln <= 0:
            raise ValueError("v7: note length out of range")
    pos += nN
    nT = ints[pos]
    pos += 1
    for k in range(nT):
        q = ints[pos + k]
        # q = ((s*E + f)*E + u)*B + c: decompose exactly
        c0 = q % B
        q //= B
        u = q % E
        q //= E
        f = q % E
        s = q // E
        if not (0 <= ints[pos + k] and 0 <= s <= 6 and 1 <= f < E
                and 0 <= u < E and 0 <= c0 < B):
            raise ValueError("v7: status int out of range")
    pos += nT + 1  # status records + loops product
    if pos != len(ints):
        raise ValueError("v7: trailing ints")
    return ints


def _v7_status_rank(s: int) -> int:
    """Merge-lattice rank: terminal beats live at equal epoch. The v7
    strength enum order already encodes it: 6>5>4>3>2>1>0."""
    return s  # noqa: identity rank, as in v6


def apply_entity_status_v7(table: dict, records: list[tuple]) -> dict:
    """Resident merge lattice for v7 (V7_STATUS_DESIGN.md): fold
    per-message entity status records into the receiver's status table.
    `records` are (concept_name, strength_enum, valid_from,
    valid_until_or_None). Newer epoch wins; ties break toward terminal,
    then stronger live. Returns the updated table."""
    for name, s, f, u in records:
        cur = table.get(name)
        if (cur is None or f > cur[1]
                or (f == cur[1] and _v7_status_rank(s) > _v7_status_rank(cur[0]))):
            table[name] = (s, f, u)
    return table
