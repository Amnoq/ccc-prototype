# Atlas-8 Charter — the prime-distribution run

**Date:** 2026-10-07
**Status:** chartered; launched on the user's tap
("Charter Atlas-8 — the prime-distribution run").
**Parent:** Atlas-7 (corpus_runs/atlas7/) — COMPLETE (the BSD wall
and bridge). Grandparent: Atlas-2 (corpus_runs/atlas2/) — the
pilot-scale version of this exact run.
**Question:** run the machine on prime number distribution itself —
the landmark prime-distribution literature as the foreign sky,
the pilot's circle-sieve sky as the home sky — and hunt the
cracks as candidate novel results. The user's realization that
motivates it: the number line is not lossy with the circle
sieve implemented, so the atlas maps the literature against the
territory, not against another text.

## Why this run is different from Atlas-2

Atlas-2 mapped papers against papers (7 analytic-NT papers vs
the pilot's documents). Atlas-8 maps the literature against the
territory: the pilot side is grounded in the implemented circle
sieve (~/workspace/prime-sieve-geometry/ — the number line in
relational form, executable). Every crack the adjudication
finds — a place where the literature's prime distribution
touches the sieve's structure in a way the literature does not
state — is then computationally checked against the sieve
implementation. A verified crack is a candidate novel result
with an epistemic label, not just a link.

## Triadic fork

1. **Claim:** cracks exist — the literature and the sieve
   touch in places the literature does not state — and at
   least one verifies computationally against the sieve.
   The crack list is the deliverable: candidate novel results.
2. **Polar opposite:** no cracks — the landmark literature
   and the sieve say the same things everywhere they touch;
   the wall is total and the sieve's structure is already
   (implicitly) in the literature. That is a finding about
   the program, recorded with the same rigor.
3. **Null / controls:** (a) drafters BLIND per sky. (b)
   POSITIVE CONTROLS: documented within-lineage pairs in the
   foreign sky (e.g., Maynard building on Zhang/GPY) MUST
   resolve — else method failure, reported plainly. (c) If
   the corpus includes any Atlas-2 paper, its adjudicated
   links are SEEDS and must reproduce. (d) fabrication
   spot-checks; the user's grading packet is the final leg.

## Corpus

- **Foreign sky (5–7 landmark papers, coordinator selects +
  verifies every ID by live retrieval, never guesses):**
  directions — PNT (a clean modern proof), the Cramér model,
  Zhang's bounded gaps, Maynard (gaps), Green–Tao (APs in
  primes), the sieve lineage (Selberg / Bombieri–Vinogradov).
  BK2011: unobtainable primary → dropped and recorded.
- **Home sky:** the pilot's circle-sieve documents
  (corpus_runs/atlas/ and prime-sieve-geometry/, READ-ONLY)
  PLUS the sieve implementation as ground truth for crack
  verification (the coordinator locates the runnable sieve
  code and uses it; verification scripts land in atlas8/).

## Protocol

1. Extract: one-shot R4 drafters, blind per sky, each
   literature's own vocabulary (drafter brief:
   corpus_runs/atlas2/DRAFTER_BRIEF.md).
2. Merge + adjudicate per Atlas-2..7 rules (explicit alias
   map, over-merge worse than under-merge, contradictions
   surfaced never adjudicated, role-differences named per D3).
3. **Crack hunt:** for every adjudicated link, ask the
   discriminating question — does the literature state what
   the sieve side holds here? Every unstated touch becomes a
   crack candidate with: the literature claim, the sieve
   structure it touches, exactly what is unstated, and the
   epistemic label it currently earns.
4. **Crack verification:** each crack candidate is checked
   against the sieve implementation (new scripts in
   atlas8/, rerunnable, captured output). Verified /
   refuted / undecidable-by-this-instrument — recorded
   plainly either way.
5. Illustrate: the money view (foreign sky vs sieve sky,
   gold cracks) + the crack list as the lead exhibit.
6. Grade + cost: grading packet (sampled triples + ALL
   adjudications + the crack list); token accounting.
7. **Span directive (2026-10-07, the user's standing
   instruction):** in extraction AND adjudication, treat the
   SPANS BETWEEN primes (gaps) as first-class concepts, not
   background. His words: like music — if we want to hear the
   song the zeta zeros are singing, we must pay attention to
   the spans in between; the song is in the intervals, not
   just the notes. Concretely: drafters capture gap-structure
   claims wherever they appear (prime gaps, zero spacings,
   orbit-length intervals, rests between tones); the crack
   hunt gives the spans priority — for each crack candidate,
   check what the literature states about the spans vs what
   the sieve shows. The spans are where novel results are
   most likely to live. Implemented as: supplementary
   span-pass extractions on all home chunks
   (SPAN_DRAFTER_BRIEF.md), the span directive in every
   foreign-sky drafter brief, and span-priority ordering in
   the crack hunt.

## Discriminating metrics (pre-registered)

- Sky↔sky link counts + density in Atlas-2..7 units.
- Crack candidates: count, and per-crack epistemic label.
- Verified cracks (computationally checked against the
  sieve): count — the novel-results shortlist.
- Controls resolved / method-failure. Seeds reproduced.
- False merges bar 0. Contradictions 0. Drops recorded.
- Cost per 1k words per phase, extrapolation shown.

## Records

corpus_runs/atlas8/: this charter, manifest.json, chunks/,
extractions/, merge script, adjudications, crack list +
verification scripts/outputs, graphs, HTML views,
ATLAS8_REPORT.md, grading packet. The pilot's,
prime-sieve-geometry/, and Atlas-2..7 directories are
read-only throughout (verification scripts may IMPORT
sieve code, never modify it).

## Branching identifiers

- **Why it ends here:** the literature has been mapped
  against the territory as far as the instruments reach;
  the crack list is complete and every crack has its label.
- **Its own chain:** (1) verified cracks → the shortlist
  goes to the prime program as its next nodes (his call
  how to work them); (2) no cracks → the total-wall finding
  bounds the program's novelty claims honestly; (3)
  controls fail → R&D spec; (4) grading packet regardless.
- Ledger: no new item unasked.

## Span directive (user, 2026-10-07; sent to coordinator mid-run)

In extraction and adjudication, treat the SPANS BETWEEN primes
(gaps) as first-class concepts, not background. Like music: to
hear the song the zeta zeros sing, attend to the spans in
between — the song is in the intervals, not just the notes.
Drafters capture gap-structure claims wherever they appear
(prime gaps, zero spacings, orbit-length intervals, rests
between tones). The crack hunt gives the spans priority: for
each crack candidate, check what the literature states about
the spans vs what the sieve shows. The spans are where novel
results are most likely to live.
