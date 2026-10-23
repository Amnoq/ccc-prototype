# Atlas-2 Charter — cross-corpus entity resolution on foreign analytic number theory

**Date:** 2026-10-07
**Status:** chartered; launched on the user's "proceed."
**Parent:** the lemma-atlas pilot (corpus_runs/atlas/ATLAS_REPORT.md) — PASSED.
**Question:** does the atlas machinery survive contact with foreign
literature — specifically, can subjects extracted from papers the
program did not write resolve to the pilot atlas's subjects where
they refer to the same mathematics, or does entity resolution break?

## Why this is the next move (the analysis)

The pilot validated mass one-shot extraction, status-preserving
merge, and illustration — on the program's own documents, whose
labels were designed for mergeability (Node 11l, D5). The named
deep R&D problem — arXiv-scale entity resolution ("hand-built
alias maps do not survive contact with arXiv") — is untested.
This run tests it on the smallest honest foreign corpus: papers
the user has engaged with deeply enough to grade the extraction
himself, several of which intersect the pilot atlas at known
points. It also measures the true unit cost (dense foreign papers,
not home documents) for the subscription/extrapolation decision:
his corpus → analytic number theory → mathematics → science.

## Triadic fork

1. **Claim:** foreign-extracted subjects resolve to pilot subjects
   at the seeded intersections (below), with contradiction rates
   at or below the pilot's (0 flagged), zero false merges among
   seeded pairs, and the user's grading at or above the pilot's
   10/13 strict.
2. **Polar opposite:** the merge produces false merges, missed
   resolutions, or contradiction spikes at the intersections —
   the entity-resolution gap quantified on real material. This
   outcome is the informative one: it maps exactly where the
   deep R&D bites, before any subscription is bought.
3. **Null (controls):** (a) drafters are BLIND to the pilot atlas
   during extraction — paper text only, no access to
   corpus_runs/atlas/; the seeded intersections are known to the
   coordinator for merge/grading, never to the drafters.
   (b) fabrication spot-checks: sampled extracted claims checked
   against paper text. (c) the user's own grading (packet
   prepared, same 13-spot-check spirit as the pilot).

## Corpus (8 papers, bounded, gradable, intersecting)

All are primary sources the program actually used; the user has
engaged each and can grade extraction fidelity. The coordinator
verifies every arXiv ID (search, don't guess) and records
provenance (source URL, version) per chunk:

1. Sierra & Rodriguez-Laguna, arXiv:1102.5356 (xp regularization)
   — intersects pilot Node 11i.
2. Connes-Consani-Moscovici, arXiv:2511.22755 (zeta spectral
   triples) — intersects pilot Nodes 11e/11f/11j/11k.
3. Lamzouri, arXiv:2609.02882 (67.25% simple-and-on-line bound)
   — intersects the user's reviewed split verdict.
4. Mossinghoff-Trudgian-Yang 2022 (zero-free region R=5.558691;
   ID to verify) — intersects pilot Node 9c.
5. Mossinghoff-Trudgian 2015 (F16 optimizer, Table 5; ID to
   verify) — intersects pilot Node 9c'.
6. Deninger, arXiv:1807.06400 (+ expository arXiv:2301.11643)
   — intersects pilot Node 11m.
7. Berry-Keating 1999, "H=xp and the Riemann zeros" (may not be
   on arXiv; coordinator finds the best obtainable primary text
   and records the substitution) — intersects pilot 11a/11g/11h.
8. Bellotti-Trudgian-Yang 2026 (1/(4.896 log|t|); ID to verify)
   — intersects pilot Node 9c.

Substitutions (unobtainable text, wrong version) are recorded,
never silent. If a paper proves unobtainable in clean text, drop
it and record the drop — do not substitute a secondary summary.

## Protocol

1. **Fetch → text → chunk** (~2.5k words/chunk, pilot scale).
   Record per-chunk provenance.
2. **Extract:** coordinator fans out one-shot R4 drafters (same
   schema as the pilot: concepts/anchors/edges/loops/strands;
   file: corpus_runs/atlas/extractions/COMPLETE_MAP.json for the
   exact JSON shape). Drafters use the papers' own vocabulary —
   NO canonical pilot labels; the merge earns resolutions, the
   drafters don't insert them. 100% validation on arrival;
   mechanical repairs only, recorded.
3. **Merge** (new script, corpus_runs/atlas2/merge_atlas2.py;
   reuse corpus_runs/atlas/MERGE_PLAN.md rules: explicit alias
   map, no silent fuzzy matching, over-merge worse than
   under-merge, contradictions surfaced never adjudicated):
   - Pass 1: merge WITHIN the foreign corpus (same rules as
     the pilot).
   - Pass 2: cross-corpus resolution against the pilot atlas
     (corpus_runs/atlas/atlas_graph.json, read-only — never
     modify the pilot's files). Attempt resolution at every
     plausible intersection; record each as
     resolved / split (kept separate, reason) / missed.
   - The seeded intersections are the scored set; unseeded
     resolutions are bonus, recorded with provenance.
4. **Illustrate:** atlas2.html (same template as the pilot's
   atlas_template.html) for the foreign atlas, PLUS the money
   view: cross-corpus edges drawn against the pilot graph
   (same mathematics, two corpora, one picture).
5. **Grade + cost:** prepare the user's grading packet
   (sampled concept/paper-quote/status triples, all seeded
   resolutions, all flagged contradictions, all splits); record
   token/cost accounting per chunk and per stage (estimates
   labeled as estimates); compute unit cost per 1k words and
   the honest extrapolation to field scale.

## Discriminating metrics (pre-registered)

- Seeded-intersection resolution rate (target: all 7 resolve).
- False merges among seeded pairs (pass bar: 0 — e.g.,
  Sierra-xp merged into BK-xp would be catastrophic).
- Wrong splits among seeded pairs (each one is a measured
  resolution failure with a named cause).
- Contradiction rate vs the pilot's 0 flagged.
- User grading vs the pilot's 10/13 strict.
- Unit cost per 1k words (foreign) vs pilot (home), with the
  extrapolation arithmetic shown.

## Records

corpus_runs/atlas2/: this charter, manifest.json (with
provenance), chunks/, extractions/, merge_atlas2.py,
atlas2_graph.json, atlas2.html, cross-corpus edge file,
ATLAS2_REPORT.md (verdict first, honest limits, cost table,
extrapolation), grading packet for the user. The pilot's
directory is read-only throughout.

## Branching identifiers

- **Why it ends here:** the cross-corpus question is adjudicated
  as far as the instruments reach — resolution rates measured,
  failure causes named, cost priced. Forcing further invents
  precision.
- **Its own chain:** (1) if resolution holds: the field-scale
  design (analytic number theory corpus definition) with real
  cost numbers for the subscription decision; (2) if it breaks:
  the failure taxonomy IS the entity-resolution R&D spec —
  the exact problem to solve before any scale-up; (3) the
  grading packet goes to the user regardless — his grading is
  the verdict's final leg.
