# CCC Wire Decoder Specification (v4)

Instructions for decoding a CCC context message from its wire form.
You need: the wrapped message text, and the shared registry
(an ordered list of concept names; both sides hold identical copies).

## Step 1 — Find the telomere-wrapped message

Scan the text for the pattern:

```
zzVRRFFSS <digits> VRRFFSSZZ
```

- It opens with literal `zz`, closes with literal `ZZ`.
- `V` = 1 digit: wire version. This spec covers version `4`.
- `RR` = 2 digits: registry size (number of concepts, 01–99).
- `FF` = 2 digits: registry fingerprint (00–99).
- `SS` = 2 digits: session number.
- The same 7-character context `VRRFFSS` appears after `zz` and before `ZZ`.
- `<digits>` is the wire body: decimal digits only.

Example: `zz4043601` `009638021...` `4043601ZZ` means version 4,
registry size 04, fingerprint 36, session 01, wire body starting
`009638021...`.

## Step 2 — Verify the registry fingerprint

Compute `sum(ord(c) for every character c of every registry name) mod 100`.
It must equal `FF`. If not, STOP — you hold the wrong registry.

Also check the registry length equals `RR`. If not, STOP.

## Step 3 — Verify the wire checksum

Let the body be `D`. Parse:
- `NNN` = integer value of `D[0:3]` (number of triples).
- `P` = integer value of `D[3]` (pad bits, 0–8).
- Triples: `D[4 : 4+3*NNN]`, each 3 digits = one triple value (0–999).
- `CK` = integer value of the final 3 digits.

Check `(NNN + P + sum of all triple values) mod 1000 == CK`.
The total body length must be exactly `4 + 3*NNN + 3` digits.
If either check fails, STOP — the wire is corrupted.

## Step 4 — Triples to bitstream

Each triple value `t` becomes exactly 9 bits: the binary of `t`,
left-padded with zeros to length 9 (most significant bit first).
Example: triple `005` → `000000101`.

Concatenate all `9*NNN` bits in order, then delete the last `P` bits.
(`P` is 0–8; if `P` is 0, delete nothing.)

## Step 5 — Gamma-decode the integers

Each integer `x >= 0` was stored as the Elias gamma code of `x+1`.
To decode, repeat at the current bit position:
1. Count leading `0` bits. Call the count `n`. (The first `1` bit ends
   the count; it is included in what follows.)
2. Read the next `n+1` bits *including that `1`* as a binary number `v`.
3. The integer is `x = v - 1`.
4. Advance past all bits consumed.

Worked example: bits `101000100` → zero leading zeros (n=0), read 1
bit: `1`, v=1, x=0. Next: bits `01000100` → one leading zero (n=1),
read 2 bits: `10`, v=2, x=1. Next: `00100` → n=2, read 3 bits `100`,
v=4, x=3. So `101000100` decodes to `[0, 1, 3]`.

Continue until every bit is consumed. If bits remain that do not form
a complete gamma code, STOP — corrupted.

## Step 6 — Parse the integer message

The integers have fixed layout:

```
[B, nS, S_1, ..., S_nS, nE, c_1, ..., c_nE, A, L]
```

- `B` = registry size (must match `RR` from Step 1).
- `nS` = number of strands. The next `nS` integers are strand codes.
- `nE` = number of relation edges. The next `nE` integers are edge codes.
- `A` = anchors code. `L` = open-loops code.

**Strand/anchor/loop codes** are products of primes: the code is the
product over the set's concepts of `p_i`, where `p_i` is the i-th prime
(2, 3, 5, 7, 11, 13, ...) and `i` is the concept's 1-based registry
index. To decode: factor the code into primes; each prime factor
`p_i` (the i-th prime) means concept index `i`. Each prime appears at
most once (it is a set). A code of `1` means the empty set.

Worked example: code `2*3*11 = 66`. Prime factors: 2 (1st prime),
3 (2nd prime), 11 (5th prime) → concept indices {1, 2, 5}.

**Edge codes** pack a pair: `c = a*B + b`, where `a` and `b` are
0-based concept indices (each `< B`). Decode: `a = c // B`
(integer division), `b = c mod B`. The 1-based registry indices are
`a+1` and `b+1`. If `a >= B` or `b >= B`, STOP — corrupted.

## Step 7 — Map indices to names

Registry index `i` (1-based) = the i-th name in the shared registry
list. Replace every index with its concept name. You now hold:
strands (sets of concept names), edges (related pairs), anchors
(established concepts), open loops (unresolved concepts).

## Worked miniature example

Registry (size 4): `[alpha, beta, gamma, delta]`. Fingerprint:
sum of ord values mod 100 (compute it).
Message integers: `[4, 1, 6, 1, 5, 1, 1]`.
- B=4. nS=1, strand code 6 = 2*3 → primes 1st,2nd → indices {1,2} →
  {alpha, beta}.
- nE=1, edge code 5: a = 5//4 = 1, b = 5%4 = 1 → 0-based (1,1) →
  1-based (2,2) → (beta, beta). (Self-loop edge.)
- A=1 → empty anchors. L=1 → empty loops.

---

## Version 5 changes

Version 5 closes three expressiveness gaps (strand labels, typed edges,
anchor statuses). The telomere, checksum, triples, and gamma steps
(Steps 1–5) are unchanged; only the integer-message layout (Step 6) and
the naming step (Step 7) change. Set `V=5` in the caps.

### Step 6 (v5) — Parse the integer message

```
[B, nS, L_1, S_1, ..., L_nS, S_nS, nE, c_1, ..., c_nE, nA, p_1, ..., p_nA, Lp]
```

- `B` = registry size (must match `RR`).
- `nS` = number of strands. Each strand is TWO integers: `L_i` then `S_i`.
  - `L_i` = 1-based registry index of the strand's label concept.
    `0` means unlabeled.
  - `S_i` = prime product of member indices (decoded exactly as in v4).
- `nE` = number of edges. Each edge code packs THREE 0-based indices:
  `c = (a*B + b)*B + t`, where `a`, `b` are the endpoint concepts and `t`
  is the relation-TYPE concept (all `< B`). Decode:
  `t = c mod B`; `ab = c // B` (integer division);
  `a = ab // B`; `b = ab mod B`.
  If any of `a`, `b`, `t` is `>= B`, STOP — corrupted.
  Edges are DIRECTED: `(a, t, b)` reads "a <t> b". Unlike v4, endpoints
  are not sorted.
- `nA` = number of anchors. Each anchor is ONE integer packing TWO
  0-based indices: `p = s*B + c`, where `s` is the status concept and `c`
  the anchor concept. Decode: `s = p // B`; `c = p mod B`.
- `Lp` = prime product of open-loop indices (as in v4).

### Step 7 (v5) — Map indices to names

As in v4, with: strand labels (index 0 → no label), edges as
`(subject, relation-type, object)` triples of names, anchors as
`(concept, status)` pairs of names.

### Worked miniature example (v5)

Registry (size 6): `[a, b, c, lbl, bounds, st_ok]`
(fingerprint computed as in Step 2).
Message integers: `[6, 1, 4, 6, 1, 10, 1, 32, 2]`.
- B=6. nS=1: L_1=4 → `lbl`; S_1=6=2*3 → indices {1,2} → {a, b}.
- nE=1: c=10. t=10%6=4; ab=10//6=1; a=1//6=0; b=1%6=1.
  0-based (0, t=4, 1) → 1-based (1, 5, 2) → (a, bounds, b).
- nA=1: p=32. s=32//6=5; c=32%6=2 → 1-based (3, 6) → anchor (c, st_ok).
- Lp=2 → {a}.

---

## Version 6 changes

Version 6 adds the anchor-note channel and status-annotated entities with
temporal validity. Set `V=6` in the telomere caps. Steps 1–2 (telomere
scan, fingerprint) are unchanged. Steps 3–6 change as below.

Design note: notes are TEXT and ride as text. Forcing them through the
integer/triplet channel costs ~3.5× per character, so the v6 body carries
a dedicated note-text section after the triplets.

### Step 3 (v6) — Verify the wire checksum (4-digit header + notetext)

Version 6 raised the v3 999-triplet ceiling. The body is

```
NNNN(4) P(1) <triplets> <NOTETEXT> CK(3)
```

- `NNNN` = integer value of `D[0:4]` (number of triples, up to 9999).
- `P` = integer value of `D[4]` (pad bits, 0–8).
- Triples: `D[5 : 5+3*NNNN]`, each 3 digits = one triple value (0–999).
- `NOTETEXT` starts right after the last triple. Its length is not in
  the header — it comes from the integer message (Step 6): the sum of
  the `nN` note character-lengths `len_1 … len_nN`.
- `CK` = integer value of the final 3 digits.

Check `(NNNN + P + sum of all triple values + sum of ord(c) for every
character c of NOTETEXT) mod 1000 == CK`. The checksum covers the notes
too — they are evidence and get integrity. The total body length must
be exactly `5 + 3*NNNN + sum(len_m) + 3` digits-and-characters.
If either check fails, STOP — the wire is corrupted.

### Step 4 (v6) — Triples to bitstream

Unchanged, with `NNNN` in place of `NNN`: each triple → 9 bits,
concatenate, delete the last `P` bits. (NOTETEXT is not bits; it is
read as characters in Step 5.)

### Step 5 (v6) — Gamma-decode the integers, then slice the notes

Decode integers one at a time *following the v6 layout* (Step 6), which
tells you exactly how many integers to read (every count `nS, nE, nA,
nN, nT` is read from the stream itself). Gamma-decoding is identical
to v5 Step 5.

When the layout is fully read, STOP: the integers are done. Read the
note section: `NOTETEXT` = the next `sum(len_m)` characters of the body
(`len_m` are the in-stream note lengths). Split it into notes in order:
note 1 = first `len_1` characters, note 2 = next `len_2`, and so on.
Then verify the body length and checksum per Step 3.

### Step 6 (v6) — Parse the integer message

```
[6, B, E, nS, L_1, S_1, ..., L_nS, S_nS, nE, c_1, ..., c_nE,
 nA, a_1, ..., a_nA, nN, len_1, ..., len_nN, nT, q_1, ..., q_nT, Lp]
```

- First integer must be `6` (version). `B` = registry size (must match
  `RR`). `E` = epoch base (≥ 1; validity epochs run 1 … E−1).
- Strands: as in v5 (`L_i` label index, `S_i` prime product of members).
- Edges: as in v5 (`c = (a*B + b)*B + t`, directed, typed).
- Anchors: each `a_k` packs a status, a concept, and a note reference:
  `a_k = (s*B + c)*B + n`. Decode: `n = a_k mod B`;
  `s, c = divmod(a_k // B, B)` (s = quotient, c = remainder).
  - `s` = epistemic status, 0–5 (see table). NOT a registry concept.
  - `c` = 0-based anchor concept index (`< B`).
  - `n` = 1-based note number (`0` = no note; else `1 … nN`).
- `nN` = number of distinct notes; `len_m` = character length of note m
  (`≥ 1`). The note texts come from the Step-5 NOTETEXT section, in order.
- `nT` = number of entity-status records. Each `q_r` packs
  `q = ((s*E + f)*E + u)*B + c`. Decode: `c = q mod B`; `q //= B`;
  `u = q mod E`; `q //= E`; `f = q mod E`; `s = q // E`.
  - `s` = status 0–5; `f` = valid-from epoch (1 … E−1);
    `u` = valid-until epoch (`0` = unbounded, still valid);
    `c` = 0-based concept index.
- `Lp` = prime product of open-loop indices (as in v4/v5).

### Epistemic-status codes (v6)

| code | name         | meaning                               |
|------|--------------|---------------------------------------|
| 0    | unstated     | no status information                 |
| 1    | hypothesized | posed / open question                 |
| 2    | asserted     | advanced as a claim, not yet verified |
| 3    | verified     | established                           |
| 4    | killed       | refuted / rejected (terminal)         |
| 5    | superseded   | replaced by a newer claim (terminal)  |

### Step 7 (v6) — Map indices to names, apply the merge lattice

Replace indices with registry names as in v5. Anchors become
`(concept, status-name, note-or-None)` triples. Entity statuses become
`(concept, status-name, valid-from, valid-until-or-None)` records.

**Merge lattice (apply on every rehydration):** keep one status record
per concept. For each incoming record `(concept, s, f, u)`:
newer `valid-from` epoch `f` always wins; on equal `f`, the higher
status code wins (5 > 4 > 3 > 2 > 1 > 0 — terminal beats live).
This is what makes cross-session status safe: a killed posit rehydrates
as killed unless a strictly newer epoch explicitly revives it.

**Merge-hook rule:** never merge two concepts as the same live claim
when exactly one side has terminal status (killed/superseded) and the
other has live status (hypothesized/asserted/verified). A
question→verdict lifecycle is a status *transition* on one entity,
not a merge of two entities.

### Worked miniature example (v6)

Registry (size 4): `[alpha, beta, rel, lbl]` (fingerprint as in Step 2).
Epoch 1, so E = 2. Integer stream:

```
[6, 4, 2, 1, 4, 6, 1, 6, 1, 53, 1, 2, 1, 57, 1]
```

- version 6; B=4 (matches RR); E=2.
- nS=1: L_1=4 → `lbl`; S_1=6 = 2·3 → 1st, 2nd primes → {alpha, beta}.
- nE=1: c=6. t = 6 mod 4 = 2 → `rel`; ab = 6 // 4 = 1;
  a = 1 // 4 = 0 → `alpha`; b = 1 mod 4 = 1 → `beta`.
  Edge: (alpha, rel, beta).
- nA=1: a_1=53. n = 53 mod 4 = 1 → note #1;
  s, c = divmod(53 // 4, 4) = divmod(13, 4) = (3, 1) →
  status 3 (verified), concept index 1 → `beta`.
  Anchor: (beta, verified, note #1).
- nN=1: len_1=2. The Step-5 note block's first 16 bits are the 2 bytes
  of note #1; here they decode (UTF-8) to `ok`.
- nT=1: q=57. c = 57 mod 4 = 1 → `beta`; 57 // 4 = 14;
  u = 14 mod 2 = 0 → unbounded; 14 // 2 = 7; f = 7 mod 2 = 1;
  s = 7 // 2 = 3 → verified.
  Entity status: (beta, verified, valid-from 1, valid-until unbounded).
- Lp=1 → no open loops.

Rehydrated: strand `lbl:{alpha, beta}`, edge (alpha, rel, beta),
anchor (beta, verified, "ok"), beta verified since epoch 1.

---

## Version 7 changes

Version 7 aligns the status enum with the work's own epistemic labels
(decision tree Node 17, `corpus_runs/V7_STATUS_DESIGN.md`). Set `V=7` in
the telomere caps. The wire body framing (4-digit header, triplets,
NOTETEXT, checksum) is byte-identical to v6; only the integer-message
layout (Step 6) and the status tables change.

### Why v7 exists

v6's enum (unstated / hypothesized / asserted / verified / killed /
superseded) was invented for the codec. It collapses the work's sharpest
distinction — **exact** (theorem/identity, proof carried) vs
**computationally verified** (numeric check passed, scope stated) — into
one "verified", and it has no room for the genre half of the work's
labels ("classical theorem, reframed — not a new theorem"). v7 speaks
the work's own labels. Strength is an ordinal; genre is a separate
anchor-level field (a reframing is neither stronger nor weaker than a
numeric check — it is a different kind of claim).

### Step 6 (v7) — Parse the integer message

```
[7, B, E, nS, L_1, S_1, ..., L_nS, S_nS, nE, c_1, ..., c_nE,
 nA, a_1, ..., a_nA, nN, len_1, ..., len_nN, nT, q_1, ..., q_nT, Lp]
```

First integer must be `7`. Strands, edges, notes, `nN`/`len_m`,
`NOTETEXT`, and `Lp` are exactly as in v6. Two changes:

- **Anchors** pack a strength AND a genre:
  `a_k = ((s*G + g)*B + c)*B + n`, with `G = 4`.
  Decode: `n = a_k mod B`; `w = a_k // B`; `c = w mod B`;
  `v = w // B`; `g = v mod G`; `s = v // G`.
  - `s` = epistemic strength, 0–6 (table below). NOT a registry concept.
  - `g` = claim genre, 0–3 (table below). NOT a registry concept.
  - `c` = 0-based anchor concept index (`< B`).
  - `n` = 1-based note number (`0` = no note; else `1 … nN`).
- **Entity-status records** keep v6's shape
  `q = ((s*E + f)*E + u)*B + c`, with `s` now 0–6 (strength only — genre
  is per-message and does not fold into the status table).

### Epistemic-strength codes (v7)

| code | name             | meaning                                              |
|------|------------------|------------------------------------------------------|
| 0    | unstated         | no status information                                |
| 1    | heuristic        | intuition/analogy, no derivation path                |
| 2    | conjectural      | precise claim, boundary stated, no proof             |
| 3    | verified-numeric | numeric/computational check passed (scope in note)   |
| 4    | exact            | theorem/identity; proof or derivation carried        |
| 5    | killed           | refuted / rejected (terminal)                        |
| 6    | superseded       | replaced by a newer claim (terminal)                 |

### Claim-genre codes (v7, anchor-level only)

| code | name           | meaning                                             |
|------|---------------|------------------------------------------------------|
| 0    | none           | no genre information / not applicable               |
| 1    | original       | new claim advanced in this message                  |
| 2    | reframed       | classical result, new framing — "not a new theorem" |
| 3    | identification | X⟷Y bridge — "not a new theorem"                   |

### Step 7 (v7) — Map indices to names, apply the merge lattice

As in v6, with anchors as `(concept, status-name, genre-name,
note-or-None)` and entity statuses carrying strength names.

**Merge lattice (apply on every rehydration):** one status record per
concept. For each incoming record `(concept, s, f, u)`: newer
`valid-from` epoch `f` always wins; on equal `f`, the higher strength
code wins (6 > 5 > 4 > 3 > 2 > 1 > 0 — terminal beats live).

**Merge-hook rule:** never merge two concepts as the same live claim
when exactly one side has terminal status (killed/superseded) and the
other has live status (heuristic/conjectural/verified-numeric/exact).

### Legacy string → v7 strength (migration, lossy-conservative)

For pre-v7 exports: `exact`/`derived`→4; `computationally_verified`
(either spelling)→3; `verified`→3 (conservative: never upgrade to exact
without evidence — the codec may not conclude more than established);
`conjectural`/`asserted`→2; `heuristic`→1; `superseded`→6;
`killed`/`rejected`/`refuted`→5; `open_question`/`hypothesized` and
anything else→0 (questions are not claims; the question text rides in
the note). Legacy anchors carry genre `none`. Forward contract: the
extractor emits (strength, genre) directly.
