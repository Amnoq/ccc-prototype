# v7 Status Alignment — the work's own labels on the wire

Date: 2026-10-03. Decision tree Node 17.
Standing principle behind it (user, same day, for the record): "self-deriving
system" refers to prime number distribution ITSELF, not the codec — and the
codec work got over the hump when we stopped treating "this" (codec) as
different from "that" (primes). The instrument and the subject are the same
structure. So the codec must speak the work's own epistemic language, not an
invented one.

## The gap (why v6's enum has to go)

v6: 0 unstated / 1 hypothesized / 2 asserted / 3 verified / 4 killed /
5 superseded.

His labels (prime-sieve-geometry/DECISION_TREE.md, DERIVATIONS.md D1–D6,
corpus_runs/DITEM_ITEMS.md): **exact / computationally verified /
conjectural / heuristic**, plus claim-genres **classical-reframed**,
**conceptual-identification**, **reformulation-analogy** — each glossed
with what the label does NOT claim ("not a new theorem", "not new prime
information").

Two load-bearing mismatches:

1. v6 collapses his sharpest distinction — **exact** (theorem/identity,
   proof carried) vs **computationally verified** (numeric check passed,
   scope stated) — into one "verified". His entire honest-label practice
   turns on this distinction.
2. v6 has no room for the genre half of his labels. "Classical theorem
   (Möbius inversion), reframed" is not just "verified": the "reframed,
   not a new theorem" qualifier is the honesty. Dropping it is a fidelity
   loss of exactly the kind the codec exists to prevent.

Genre is not an ordinal (a reframing is not "stronger" or "weaker" than a
numeric check — it is a different kind of claim), so it cannot join the
strength enum. It goes on the anchor (the claim this message makes), not
on the entity (Möbius inversion is exact, period; the reframing was one
message's contribution).

## v7 strength enum (replaces v6 0–5; wire version 7)

| code | name            | his term                 | meaning                                    |
|------|-----------------|--------------------------|--------------------------------------------|
| 0    | unstated        | —                        | no status information                      |
| 1    | heuristic       | heuristic                | intuition/analogy, no derivation path      |
| 2    | conjectural     | conjectural              | precise claim, boundary stated, no proof   |
| 3    | verified-numeric| computationally verified | numeric/computational check passed         |
| 4    | exact           | exact                    | theorem/identity; proof or derivation carried |
| 5    | killed          | closed negative          | refuted / rejected (terminal)              |
| 6    | superseded      | superseded               | replaced by a newer claim (terminal)       |

The scope of a verified-numeric claim ("at z=30, x=200000", "to 2·10⁶")
rides in the note, as v6 already provides. "Derived" (his D-item usage:
"derived (rule→series)") maps to exact — the derivation is the proof —
with the rule cited in the note; the extractor must ensure the premises
support it.

## v7 genre (anchor-level, new 2-bit field; NOT on entity-status records)

| code | name           | meaning                                                        |
|------|----------------|----------------------------------------------------------------|
| 0    | none           | no genre information / not applicable                          |
| 1    | original       | new claim advanced in this message                             |
| 2    | reframed       | classical result, new framing — "not a new theorem"            |
| 3    | identification | X⟷Y bridge — "not a new theorem"                              |

"Reformulation and analogy" (his D8 label) files under reframed; the note
carries the nuance. Entity-status records stay strength-only, so the merge
lattice remains one-dimensional and deterministic.

## Merge lattice (mechanics unchanged from v6)

rank: 6 > 5 > 4 > 3 > 2 > 1 > 0. Newer valid-from epoch always wins; ties
break toward terminal, then stronger live. Terminal = {killed,
superseded}; live = {heuristic, conjectural, verified-numeric, exact}.
Merge-hook rule unchanged: never merge two concepts as the same live
claim when exactly one side is terminal.

## Wire changes (clean break → version 7)

- Telomere version field: 7. First int of the stream: 7.
- Anchor: `a_k = ((s*G + g)*B + c)*B + n`, G = 4.
  Decode: `n = a_k % B`; `w = a_k // B`; `c = w % B`; `v = w // B`;
  `g = v % G`; `s = v // G`. Validate `s ≤ 6`, `g ≤ 3`.
- Entity status `q = ((s*E + f)*E + u)*B + c`: shape unchanged, `s ≤ 6`.
- Everything else (strands, edges, notes, NOTETEXT, checksum, telomere
  framing) is byte-identical to v6.

## Migration map (legacy strings → v7; lossy-conservative, documented)

| legacy string                          | v7 | rationale |
|----------------------------------------|----|-----------|
| "verified"                             | 3 verified-numeric | conservative: never upgrade to exact without evidence. A theorem labeled verified-numeric is still true; a numeric check labeled exact is false. The codec's prime directive (Exp2: zero hallucinations) forbids concluding more than established. |
| "asserted"                             | 2 conjectural | "advanced as a claim, not yet verified", precise → conjectural |
| "open_question", "hypothesized"        | 0 unstated | questions are not claims; v7 does not rank them on the strength ordinal. The question text rides in the note. |
| "exact", "derived"                     | 4 exact | |
| "computationally_verified", "computationally-verified" | 3 verified-numeric | |
| "heuristic"                            | 1 heuristic | |
| "conjectural"                          | 2 conjectural | |
| "killed", "rejected", "refuted"        | 5 killed | |
| "superseded"                           | 6 superseded | |
| anything else                          | 0 unstated | |

Legacy anchors carry genre 0 (none). Forward contract (R4 extractor
change, as v6 did): the extractor emits (strength, genre) directly.

## Validation

Mirror of the v6 independent-decode test: build v7 wires for all 12
corpus chunks from extraction.json via the migration map, decode with an
independent spec_decode_v7.py written from DECODE_SPEC.md's v7 section
alone (no codec imports), require 12/12 field-exact match including
status names, genre names, notes, and entity-status records.

## Success criteria

1. 12/12 independent v7 decode fidelity (as above).
2. Wire-path deployment break-even stays ≤3 on all 12 chunks (the genre
   field adds one small multiply per anchor; gamma cost delta negligible).
3. Every legacy status string in the 12 extractions maps without raising
   (no silent 0s except open_question/hypothesized, which are logged).
