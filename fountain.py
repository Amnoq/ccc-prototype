"""Fountain / holographic redundancy layer over the multiline transport.

The parity line in codec.py is *surgical*: it locates one bad digit
(row from checksums, column from syndrome) and fixes it -- but it hits
provable ambiguity walls and handles nothing beyond a single error.

This layer is *statistical*, in the spirit of the holographic principle
(the whole is in the parts): each fountain line combines a random subset
of ALL data lines, so the decoder never locates errors. Lines that fail
their checksum are silently discarded as erasures; the LT peeling
decoder then recovers the missing data lines from whatever fountain
lines survive. The job changes from "find and fix" to "collect enough
good pieces and solve".

Design
------
* Source symbols: the k full data-line strings from
  ``codec.encode_lines`` (``LLKK`` header + v4 wire + 3-digit header
  checksum), padded on the right with ``"0"`` to the common width W =
  max line length. Zero-padding is the identity for XOR, so padding is
  free. True length is recovered deterministically: the v4 wire's own
  ``NNN`` triple-count field gives ``true_len = 14 + 3*NNN``; the
  framing checksum then re-validates the stripped line.
* Combination: decimal digit -> 4-bit nibble; fountain symbols are the
  nibble-wise XOR of a subset of source lines. XOR is enough -- LT
  peeling only needs an invertible group operation, no finite field.
* Subset: ``fountain_subset(seed, k)``. Degree ``d ~ 1 + Binomial(k-1,
  1/2)`` (shifted binomial), then a uniform random ``d``-subset via
  ``random.Random(seed)``. Both sides recompute it from the seed;
  nothing about the subset is transmitted. The shifted-binomial choice
  comes from a grid search over candidate degree distributions at k=8
  (uniform 1..k, ideal soliton, dense/sparse mixtures, fixed degrees):
  it won on the e<=f operating regime under random pool erasures.
  (Caveat: ``random.Random`` determinism is assumed on both sides --
  same Python/reimplementation.)
* Fountain line format: ``97SS`` + body + 3-digit checksum, where
  ``SS`` is the 2-digit seed (max 100 fountain lines per message) and
  the body is the XOR-result nibbles (0..15) as two decimal digits each
  (``00``..``15``). ``97`` collides with neither data headers
  (``LLKK``, LL < k <= 99... note LL=97 with k>97 is impossible since
  data idx < k and fountain tag is only read as fountain when... see
  note below) nor the parity header (``99KK``). The body stays
  digit-only, so the standard ``_digit_checksum`` applies and the
  triple-tokenizer property is preserved.
* Checksum: same 3-digit ``_digit_checksum`` over header+body. Any
  single-digit corruption is detected (nonzero weight per position),
  so corrupted fountain lines become erasures -- never silent
  mis-decodes. A corrupted seed therefore fails its checksum; the
  decoder never acts on a wrong subset.
* Encoder-side seed search ("the encoder does the searching; the
  decoder does the walking"): ``choose_seeds`` scans the 100-seed space
  in tiers. Tier 2 finds f consecutive seeds whose subsets jointly
  cover every data line -- then ANY single data-line erasure provably
  recovers (a surviving symbol has effective degree 1 on it). Tier 1
  (tried first when 2**f > k) additionally requires a *separating
  family* (every pair of data lines is split by some subset) plus
  double coverage (every line in >= 2 subsets) -- then ANY <= 2 pool
  erasures (data or fountain lines) provably recover by peeling; the
  proof is in the report/demo notes. Falls back down the tiers
  otherwise. The lines carry their actual seeds, so the decoder is
  unaffected.
* Fundamental small-block limit (proven, not just measured): with
  f=2, k=8, deterministic 2-erasure recovery is IMPOSSIBLE under
  peeling -- two subsets induce at most 4 incidence atoms on 8 points,
  so some pair is never separated and peeling cannot start. f >= 4
  (2**f > k) is the first regime where it becomes possible.
* Decoder: standard LT peeling. Intact data lines are degree-1
  symbols; surviving fountain lines are higher-degree symbols. Fully
  resolved symbols must have zero residual, and every recovered line
  is strip+checksum+wire re-validated before reassembly.

Header note: a data line header is ``LLKK`` with ``LL = idx < k``.
Fountain mode requires k <= 97, so a ``97SS`` header can never be a
data line -- the tag is unambiguous, and the decoder additionally
requires ``KK == k`` on data lines and a valid fountain checksum on
fountain lines.

Threat model: erasures (dropped lines) and detected corruption
(single-digit flips always detected by the checksum). Undetected
multi-digit checksum collisions are out of scope -- same as the base
scheme. Forged lines with recomputed checksums are out of scope.
"""
from __future__ import annotations

import random

from codec import (_digit_checksum, decode_message_bits, encode_lines)

FOUNTAIN_TAG = "97"
MAX_FOUNTAIN_LINES = 100  # 2-digit seed space


# --------------------------------------------------------------------------
# deterministic subset sampling: shared recomputation, nothing transmitted
# --------------------------------------------------------------------------
def fountain_subset(seed: int, k: int) -> list[int]:
    """Subset of source indices {0..k-1} for the fountain line `seed`.

    Degree d ~ 1 + Binomial(k-1, 1/2), then a uniform random d-subset,
    all drawn from random.Random(seed). Deterministic on both sides.
    """
    if not 0 <= seed <= 99:
        raise ValueError(f"seed {seed} out of range 0..99")
    if not 1 <= k <= 97:
        raise ValueError(f"k={k} out of range 1..97")
    rng = random.Random(seed)
    d = 1 + sum(1 for _ in range(k - 1) if rng.random() < 0.5)
    return sorted(rng.sample(range(k), min(d, k)))


# --------------------------------------------------------------------------
# encoder-side seed search
# --------------------------------------------------------------------------
def _tier1_ok(subsets: list[set[int]], k: int) -> bool:
    """Separating family + covering + double coverage.

    Separating: every pair {i,j} is split by some subset (some symbol
    covers exactly one of them) -- this is what lets peeling *start*
    on any 2-erasure pattern. Covering + double coverage: every data
    line is in >= 2 subsets -- this survives one fountain-line erasure.
    Together: any <= 2 pool erasures peel deterministically. Possible
    only when 2**f > k (2**f incidence patterns minus the empty one
    must cover k points).
    """
    pts = set(range(k))
    if set().union(*subsets) != pts:
        return False
    count = [0] * k
    for s in subsets:
        for i in s:
            count[i] += 1
    if min(count) < 2:
        return False
    for i in range(k):
        for j in range(i + 1, k):
            if not any((i in s) != (j in s) for s in subsets):
                return False
    return True


def choose_seeds(seed: int, k: int, n_fountain: int):
    """Pick f consecutive seeds, best tier the seed space allows.

    Tier "tier1": separating + covering + double coverage (any <= 2
      pool erasures provably recover); tried when 2**n_fountain > k.
    Tier "tier2": full data-line coverage (any single erasure provably
      recovers).
    Tier "fallback": the requested seeds, no guarantees (probabilistic).
    Returns (seeds, tier). The chosen seeds are carried in the lines
    themselves, so decoding is unaffected.
    """
    if n_fountain >= 1 and 2 ** n_fountain > k:
        for t in range(100):
            cand = [(seed + t + j) % 100 for j in range(n_fountain)]
            subs = [set(fountain_subset(s, k)) for s in cand]
            if _tier1_ok(subs, k):
                return cand, "tier1"
    for t in range(100):
        cand = [(seed + t + j) % 100 for j in range(n_fountain)]
        covered = set()
        for s in cand:
            covered.update(fountain_subset(s, k))
        if len(covered) == k:
            return cand, "tier2"
    return [(seed + j) % 100 for j in range(n_fountain)], "fallback"


# --------------------------------------------------------------------------
# encoding
# --------------------------------------------------------------------------
def _nibbles_of_line(line: str, width: int) -> list[int]:
    nib = [ord(c) - 48 for c in line]
    if any(n < 0 or n > 9 for n in nib):
        raise ValueError("non-digit in data line")
    return nib + [0] * (width - len(nib))


def encode_lines_fountain(ints: list[int], k: int, n_fountain: int,
                          seed: int = 0) -> list[str]:
    """k data lines (identical to codec.encode_lines) + n_fountain lines.

    Fountain line seeds come from choose_seeds: f consecutive seeds
    with full data-line coverage when the seed space allows (so any
    single data-line erasure provably recovers). Data lines come first,
    fountain lines after -- same convention as encode_lines_parity.
    """
    if not 1 <= k <= 97:  # 97 keeps the fountain tag unambiguous
        raise ValueError(f"k={k} out of range 1..97")
    if not 0 <= n_fountain <= MAX_FOUNTAIN_LINES:
        raise ValueError(f"n_fountain={n_fountain} exceeds seed space "
                         f"{MAX_FOUNTAIN_LINES}")
    if not 0 <= seed <= 99:
        raise ValueError(f"seed={seed} out of range 0..99")
    data = encode_lines(ints, k)
    if n_fountain == 0:
        return data
    width = max(len(ln) for ln in data)
    src = [_nibbles_of_line(ln, width) for ln in data]
    seeds, _covering = choose_seeds(seed, k, n_fountain)
    lines = list(data)
    for s in seeds:
        sub = fountain_subset(s, k)
        acc = [0] * width
        for i in sub:
            row = src[i]
            for t in range(width):
                acc[t] ^= row[t]
        assert all(n <= 15 for n in acc)  # XOR of decimal nibbles
        core = f"{FOUNTAIN_TAG}{s:02d}" + "".join(f"{n:02d}" for n in acc)
        lines.append(core + _digit_checksum(core))
    return lines


# --------------------------------------------------------------------------
# decoding: LT peeling over nibble-XOR symbols
# --------------------------------------------------------------------------
def _strip_data_line(digits: str, k: int) -> tuple[int, list[int]]:
    """Recover (idx, ints) from a padded digit string of a data line.

    True length comes from the v4 wire's own NNN field
    (line = LLKK + [NNN pad triples... checksum] + hcheck, so
    true_len = 14 + 3*NNN); the header checksum and wire checksum then
    re-validate. Raises ValueError on any inconsistency.
    """
    if len(digits) < 14 or not digits[:7].isdigit():
        raise ValueError("padded line too short to frame")
    nnn = int(digits[4:7])
    true_len = 14 + 3 * nnn
    if len(digits) < true_len:
        raise ValueError("padded line shorter than its framed length")
    line = digits[:true_len]
    idx, kk = int(line[:2]), int(line[2:4])
    if not (0 <= idx < k and kk == k):
        raise ValueError(f"stripped line header {line[:4]} invalid "
                         f"for k={k}")
    core, hcheck = line[:-3], line[-3:]
    if _digit_checksum(core) != hcheck:
        raise ValueError(f"line {idx} header checksum mismatch "
                         f"after peeling")
    return idx, decode_message_bits(core[4:])


def decode_lines_fountain(lines: list[str], k: int):
    """Decode k data lines + any fountain lines; LT peeling recovery.

    Returns (ints, report). Lines failing checksums are discarded as
    erasures and listed in the report; unrecoverable input raises
    ValueError describing what is missing. Never returns wrong ints:
    every recovered line is strip+checksum+wire re-validated.
    """
    if not lines:
        raise ValueError("no lines to decode")
    if not 1 <= k <= 97:  # 97 keeps the fountain tag unambiguous
        raise ValueError(f"k={k} out of range 1..97")

    data_raw: dict[int, str] = {}
    fountain_syms: list[tuple[int, list[int], list[int]]] = []
    width: int | None = None
    report: dict = {"k": k, "erased_data": [], "erased_fountain": [],
                    "erased_other": [], "recovered_via_peeling": [],
                    "peeling_rounds": 0}

    for ln in lines:
        if len(ln) < 7 or not ln[:4].isdigit():
            raise ValueError(f"bad line: {ln[:12]!r}")
        tag, core, hcheck = ln[:2], ln[:-3], ln[-3:]
        if tag == FOUNTAIN_TAG:
            s = int(ln[2:4])
            body = core[4:]
            vals = []
            ok = (_digit_checksum(core) == hcheck and len(body) >= 2
                  and len(body) % 2 == 0)
            if ok:
                vals = [int(body[t:t + 2])
                        for t in range(0, len(body), 2)]
                ok = all(v <= 15 for v in vals)
            if not ok:
                # corrupted seed or body: checksum (or nibble range)
                # fails -> erasure, never acted upon
                report["erased_fountain"].append(f"97{s:02d}")
                continue
            w = len(body) // 2
            if width is None:
                width = w
            elif w != width:
                raise ValueError("fountain width mismatch: lines from "
                                 "different messages?")
            fountain_syms.append((s, fountain_subset(s, k), vals))
        elif tag == "99":
            # A single-digit corruption always breaks _digit_checksum
            # (nonzero weight per position), so a passing checksum here
            # means a genuine parity line mixed in: unsupported, loud.
            if _digit_checksum(core) == hcheck:
                raise ValueError("parity (99..) line mixed into "
                                 "fountain decode")
            report["erased_other"].append(ln[:4])
        else:
            idx, kk = int(ln[:2]), int(ln[2:4])
            try:
                valid = (0 <= idx < k and kk == k
                         and _digit_checksum(core) == hcheck)
                decode_message_bits(core[4:]) if valid else None
            except ValueError:
                valid = False
            if valid:
                if idx in data_raw:
                    raise ValueError(f"duplicate line {idx}")
                data_raw[idx] = ln
            else:
                report["erased_data"].append(ln[:4])

    if len(data_raw) < k and not fountain_syms:
        missing = sorted(set(range(k)) - set(data_raw))
        raise ValueError(f"missing lines {missing} and no fountain "
                         f"symbols to recover from; {report}")

    if width is None:  # no fountain lines at all
        width = max(len(ln) for ln in data_raw.values())

    # known source nibble arrays (zero-padded to width: XOR identity)
    known: dict[int, list[int]] = {}
    for idx, raw in data_raw.items():
        known[idx] = _nibbles_of_line(raw, width)

    # init symbol residuals: XOR out already-known sources
    # each symbol: [neighbor set, residual nibble list]
    syms = []
    for s, sub, vals in fountain_syms:
        nb = set(sub)
        res = list(vals)
        for i in list(nb):
            if i in known:
                row = known[i]
                res = [a ^ b for a, b in zip(res, row)]
                nb.discard(i)
        syms.append([nb, res])
    for nb, res in syms:
        if not nb and any(res):
            raise ValueError("inconsistent fountain symbols: "
                             "checksum-passing lines disagree")

    # peeling
    while True:
        progressed = False
        for nb, res in syms:
            if len(nb) == 1:
                i = next(iter(nb))
                if i in known:
                    nb.clear()
                    continue
                if any(n > 9 for n in res):
                    raise ValueError(
                        f"peeling yielded non-digit nibbles for line "
                        f"{i}: fountain data inconsistent")
                known[i] = list(res)
                report["recovered_via_peeling"].append(i)
                nb.clear()
                for nb2, res2 in syms:
                    if i in nb2:
                        nb2.discard(i)
                        row = known[i]
                        for t in range(len(res2)):
                            res2[t] ^= row[t]
                progressed = True
        report["peeling_rounds"] += 1
        if not progressed:
            break

    missing = sorted(set(range(k)) - set(known))
    if missing:
        raise ValueError(
            f"fountain decode stuck: unrecoverable lines {missing}; "
            f"{len(fountain_syms)} fountain symbols seen, "
            f"{len(report['recovered_via_peeling'])} recovered by "
            f"peeling; {report}")

    # every line through the single strip+validate path (never trust
    # peeling output without re-validation)
    chunks = {}
    for i in range(k):
        digits = "".join(str(n) for n in known[i])
        ii, ints = _strip_data_line(digits, k)
        if ii != i:
            raise ValueError(f"line index mismatch after peeling: "
                             f"{ii} != {i}")
        chunks[i] = ints

    # no peeling was needed: cross-check fountain symbols against the
    # intact data (catches encoder/decoder disagreement loudly)
    if not report["recovered_via_peeling"]:
        for s, sub, vals in fountain_syms:
            acc = [0] * width
            for i in sub:
                row = known[i]
                for t in range(width):
                    acc[t] ^= row[t]
            if acc != vals:
                raise ValueError(f"fountain line 97{s:02d} inconsistent "
                                 f"with data lines")

    report["data_present"] = sorted(data_raw)
    report["fountain_seen"] = len(fountain_syms)
    out = [x for i in range(k) for x in chunks[i]]
    return out, report
