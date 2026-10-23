# v6 Codec Design — note channel + status-annotated entities

Date: 2026-10-03. Decision tree Node 13. Linear SID-16.

## Why v6 exists (two findings, one build)

1. **R3 (Node 11):** the v5 wire has no anchor-note channel. R3's evidence
   notes survive grouped injection but not v5 export — the 7.42 → 6.79
   parity step is a representation gap, not decode corruption. Notes must
   travel on the wire.
2. **Experiment 2 close-out (Node 12):** strict principle P (posit ≠
   resolution) is load-bearing only because the registry has no
   status/polarity field. Status-annotated entities make the looser
   principle Q (one investigation = one entity across its lifecycle) safe:
   under Q the same data read 0.962–0.974. v6 must make Q's safety
   **mechanical, not adjudicator-dependent**: a killed posit rehydrates as
   killed, never as live.

## Accounting (user's standing principle, 2026-10-03)

Extraction and decoding protocols are resident one-time costs, stored on
the receiving side previous to transmission. The wire carries only the
message. DECODE_SPEC.md's tokens do not count toward marginal break-even.
The v6 additions to DECODE_SPEC (status enum, note codec, merge lattice)
are one-time; only the per-message ints count.

## Wire layout (clean break from v5, selected by envelope version)

```
[6, B, E, nS, (L_i, S_i)×nS, nE, c_1..c_nE, nA, a_1..a_nA,
 nN, len_1..len_nN, nT, q_1..q_nT, Lp]
```

- `6`: version. (The telomere envelope also declares v6; the int-list
  version is belt-and-braces for the independent decoder.)
- `B`: registry size (as v5).
- `E`: epoch base. Validity epochs are 1..E−1; `u = 0` means unbounded.
- Strands `(L_i, S_i)`: as v5 (1-based label index, prime product of
  1-based member indices).
- Edges `c_j = (a*B + b)*B + t`: as v5 (0-based, directed, typed).
- Anchors `a_k = (s*B + c)*B + n`:
  - `s`: epistemic-status enum (below), 0-based. **Structural, not a
    registry concept** — this is the v5 status-as-concept hack retired.
  - `c`: 0-based anchor concept index.
  - `n`: 1-based index into the note table (`0` = no note).
- Notes: deduped across anchors, first-seen order. `len_m` = character
  length of note m; the note characters ride as a literal NOTETEXT
  section in the wire body (see Wire transport). Anchors reference notes
  1-based. No alphabet table, no byte-packing: text as text.
  Rationale for not word-coding: notes carry arbitrary evidence
  (numbers, formulas, non-ASCII like `5·10⁵`, `2C₂`); any fixed wordlist
  would silently fail on exactly the highest-value content. Measured
  note-word registry coverage was only 0.46 — not enough to justify a
  word tier in v6.
- Entity status `q_r = ((s*E + f)*E + u)*B + c`:
  - `s`: status enum; `f`: valid-from epoch (≥1); `u`: valid-until
    epoch (`0` = unbounded); `c`: 0-based concept index.
  - One record per concept whose status this message establishes.
- `Lp`: prime product of open-loop indices (as v5).

## Status enum

| code | name         | meaning                                  |
|------|--------------|------------------------------------------|
| 0    | unstated     | no status information                    |
| 1    | hypothesized | posed / open question                    |
| 2    | asserted     | advanced as a claim, not yet verified    |
| 3    | verified     | established                              |
| 4    | killed       | refuted / rejected (terminal)            |
| 5    | superseded   | replaced by a newer claim (terminal)     |

String → enum map for existing R3 exports: `verified`→3, `asserted`→2,
`open_question`→1, `hypothesized`→1, `superseded`→5,
`killed`/`rejected`/`refuted`→4, anything else →0. Forward contract: the
extractor emits enum-compatible statuses directly (R4 extractor change).

## Entity-status derivation (per message, deterministic)

For each concept with ≥1 anchor in this export:
- if any anchor maps to terminal (4/5): status = max terminal present
  (5 beats 4 — superseded names the heir, more informative);
- else: status = max live level (3 > 2 > 1 > 0).
- `f` = message epoch, `u` = 0.

Epoch for the 12-chunk corpus: chunk index (1–12). In deployment: session
counter. `E` = max epoch ever used + 1, carried in the header.

## Merge lattice (resident decode protocol, deterministic)

Applied to the receiver's status table on every rehydration:

```
for (c, s, f, u) in records:
    cur = table.get(c)
    if cur is None or f > cur.f or (f == cur.f and rank(s) > rank(cur.s)):
        table[c] = (s, f, u)

rank: 5 > 4 > 3 > 2 > 1 > 0   (terminal beats live at equal epoch)
```

Newer epoch always wins — a re-verification at a later epoch can revive a
killed claim, but only explicitly, never by accident.

## Merge-hook rule (mechanical P-safety)

The entity-resolution merge hook MUST consult the status table and refuse
to merge concept X with concept Y as the same live claim when exactly one
side has terminal status (4/5) and the other has live status (1/2/3).
Under principle Q, question→verdict is a status *transition* on one
entity, not a merge of two entities. This is the failure the strict-P
ruling guarded against (Exp2 false merges H037/H047/H053/H107/M002);
v6 makes the guard structural.

Wiring this into exp2_merge_hook.py (against a status-annotated
exp2_registry_v2) is the defined next experiment, not part of v6 MVP.

## Wire transport

The v6 message is an int stream plus a note-text section. Notes are TEXT
and ride as text — an earlier revision packed them as raw bits in the
triplet channel, which measured ~3.5× per character and pushed the wire
past the injection it was meant to undercut (BE_wire 3.21 vs BE_inj
2.26 on the same data). Text-as-text is also simpler for independent
decoders.

- Int stream: gamma-coded, layout `[6,B,E,nS,…]` as above.
- Body: `NNNN(4) + P(1) + triplets + NOTETEXT + cksum(3)`.
  Triplets carry gamma(ints) padded to a multiple of 9 bits.
  NOTETEXT is the concatenated note characters (`sum(len_m)` chars).
- Checksum covers triplets AND notetext:
  `(NNNN + P + sum(triplets) + sum(ord(c) for c in notetext)) % 1000`
  — notes are evidence and get integrity.
- Decode: read envelope version → parse 4-digit header → gamma-decode
  the int stream layout-aware (counts nS/nE/nA/nN/nT are in-stream) →
  slice NOTETEXT by `len_m` → verify total length and checksum.
- The 4-digit triplet count raises v3's 999-triplet ceiling to 9999;
  the envelope declares version 6 so the header width is unambiguous.

v7 levers (not taken): 6-bit note alphabet (~22% saving, interop cost),
zlib on NOTETEXT (~40% saving, opaque to eyeball verification).

## Validation (mirrors v5, extended)

- Header: first int 6; `1 ≤ B`; `E ≥ 1`.
- Strand/edge/loop sections: as v5.
- Anchors: `s < 6`, `c < B`, `n ≤ nN`.
- Notes: `len_m >= 1` (non-empty text); NOTETEXT length = sum(len_m).
- Status records: `s < 6`, `f < E`, `u < E`, `c < B`.
- No trailing ints after `Lp`.

## Success criteria

1. Independent decoder from DECODE_SPEC.md alone: 12/12 fidelity
   (name-for-name, edge-for-edge, anchor-for-anchor **with notes**,
   status-for-status, loop-for-loop).
2. Wire-path deployment break-even stays ≤3 on all 12 chunks.
3. Mechanical: every note the R3 injection carries is present verbatim in
   the rehydrated struct (note-survival 211/211).
4. Parity: predicted recovery of wire-read parity toward injection parity
   (6.79 → 7.42). **Not claimed until a blind re-score runs** — a
   non-blind provisional self-score may be reported with that label.
