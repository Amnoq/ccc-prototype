# Project brief: the epistemic instrument (successor to CCC)

## What this is

Infrastructure for *how things are known* — not storage, not compression.
The CCC context-compression charter was retired by measurement: the tool's
excellence is analytic, not compressive (parity 9.75/10 demonstrated;
deployment break-even structurally impossible at high fidelity). What
survived is the instrument: one-shot extraction of a text's epistemic
structure, merged into dependency graphs, illustrated as navigable atlases.
A prosthetic thinking structure — it does not think for you; it holds
verdicts, relations, and dead ends so thought accumulates instead of
evaporating.

## Core vocabulary (binding)

- **Statuses:** exact (derivation present in the text) /
  computationally_verified (the check AND its scope, in the note) /
  conjectural (precise claim, no proof) / heuristic (intuition, no
  derivation path stated) / killed (refuted, reason preserved in the note)
  / superseded (replaced; name the heir). Open questions go in loops,
  unanchored — never force a strength status onto a question.
- **Genres:** original / reframed / identification. Omit the key when none
  applies.
- **Edges:** supports, depends_on, bounds, refines, implements,
  exemplifies, contradicts, etc. Directed, no duplicates — fewer, truer
  edges over many speculative ones.

## Non-negotiable principles

1. **Never put the answer in by hand.** Mark only what the text
   establishes. Fail by omission, never by invention. Zero fabrication
   is the standing record across every battery run.
2. **Derive, don't invent.** Observe the text's own forms; no imposed
   taxonomies, no private jargon about the work.
3. **Dead ends are first-class.** Killed claims are kept with their
   reasons; they are the highest-density entries — each one is a wall
   no future agent walks into.
4. **The instrument and the subject share the same structure.** The
   method embodies the perspective; it is not an argument for it.

## Measured state

- One-shot R4 extraction validates clean repeatedly (physics paper,
  philosophical letter, theorem note, 30-chunk corpus pilot); v7 wires
  round-trip exactly; independent spec-decodes pass; 0/120
  fabricated (≤2.5% at 95%) across all probe batteries.
- Lemma-atlas pilot: 23 documents / ~43k words → 545 concepts /
  480 anchors / 421 edges / 45 loops → merged to 112 subjects + 193
  detail nodes, 344 relations; graded 10/13 against the author's
  independently recorded structure, divergences reviewed and defensible.
- **Known frontier:** derivation interiors thin under the density cap —
  the verdict-and-relation layer is excellent; proof steps are not fully
  carried. ArXiv-scale entity resolution (is Lemma 3.2 in paper A the
  same as Theorem 2 in paper B?) is the deep unsolved R&D problem.

## Working stance

Direct, unsweetened technical assessment. Sycophancy is a failure mode,
not politeness. When handed a discriminating task with a known answer,
hold the line — do not agree, do not upgrade, do not invent. Flag soft
calls unprompted. Correct hard and early; that is how the stance
transfers.
