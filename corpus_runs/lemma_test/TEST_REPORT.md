# Lemma test: interference theorem note

Date: 2026-10-06. Third analytic test: how does the R4/v7 pipeline
perform **analyzing a lemma** — a claim with a derivation and a
boundary — rather than compressing prose?

## Source

`prime-sieve-geometry/interference_theorem.md` (764 words): the
three-part interference theorem (rose graph, two sectors). Part (a)
Dirichlet phase — exact; part (b) vertex phase alternation —
derived exact (Node 16, Lemmas 1–4) with one precisely located open
sub-step (dither anti-alignment: computationally verified, not
derived); part (c) merged conclusion — exact given (a)(b);
corollary computationally verified at amplitude level (Node 11q)
with probe-blindness caveat; one killed alternative route
(scattering-factor powers); honest boundaries (pattern not
z-scores, r≥3 inconclusive, 11p gate verdict unchanged).

## Pipeline (one-shot, no second judge)

1. R4 extraction by a single drafter: 12 concepts (7 claim +
   5 result) · 12 anchors · 11 edges · 0 loops · 6 strands.
   `validate_extraction` → `[]`.
2. v7 wire build: 68 ints, 12 notes, 311 wire tokens.
3. Codec round-trip: exact.
4. Independent spec decode from DECODE_SPEC alone: PASS (12/12
   anchors with status+genre+note, 11/11 edges).

Status distribution: exact 8 · computationally_verified 3 ·
killed 1. Genres: original on c3, c4, c7, c8, c12; omitted
elsewhere.

## Grading against the recorded status structure

The note's epistemic structure was fixed by the author before the
test, so the extraction is graded against ground truth:

| Check | Result |
|---|---|
| (a) → exact | PASS (c2, "deterministic") |
| (b) → exact, derivation present | PASS (c3 + c4, Node 16, formulas in note) |
| Dither sub-step NOT upgraded | PASS (c6 computationally_verified, "verified not derived") |
| (c) → exact-conditional on (a),(b) | PASS (c7, depends_on c2/c3) |
| Corollary → computationally_verified with scope | PASS (c8, alignment numbers + additivity in note) |
| Scattering-factor route → killed | PASS (c5, superseded by c4) |
| Probe blindness → boundary, not dropped | PASS (c9 bounds c8, z-numbers in note) |
| Pattern-not-z-scores scope → boundary | PASS (c10 bounds c7) |
| r≥3 inconclusive → reported, not buried | PASS (c11 bounds c8) |
| 11p gate verdict unchanged | PASS (c12 note) |
| Second-witness relation (corollary → (b)) | PASS (c8 supports c3, as the text states) |

11/11. The trap held: the note wears its labels openly, and the
drafter still had to place the dither sub-step correctly
(verified-but-not-derived ≠ exact, ≠ loop) — it did, and flagged
its soft calls unprompted (c1 exact as stipulated framework;
c10/c11 exact as stated scope / reported negative — the same
"announced" category as fig_test's c12).

## Honest boundary found

The four lemmas merged into one derivation concept (c4) per
density rules; the lemma-to-lemma interior (Lemma 1 → 2 → 3 → 4)
survives as formulas in the note, not as structured edges. The
extraction captured the lemma's **role** in the argument
perfectly; its **internal** derivation steps thinned. This is the
measured mechanism frontier showing up exactly where predicted
(v7 MECHANISM 0.76): verdict-and-relation layer excellent,
derivation interior the cost.

## Answer to the posed question

For analyzing lemmas, the instrument performs excellently at the
level it was built for — status discrimination, dependency
structure, boundary preservation, honest failure — and thins at
exactly the known frontier: the inside of a derivation. A lemma's
standing (what's proved, what's checked, what's open, what died,
what bounds it) survives one-shot extraction intact; the
step-by-step interior needs the density cap lifted or a
derivation-grade note type (the R5 direction, still unauthorized).
