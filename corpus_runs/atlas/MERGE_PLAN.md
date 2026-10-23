# Atlas merge plan

Date: 2026-10-06. The extraction fan-out produces 30 per-chunk
extractions. The merge builds one unified lemma graph. This is the
hard step; the design:

## 1. Entity resolution (same concept, many chunks)

- Drafters were instructed to use canonical identifiers as labels
  (Node 11l, D5, "interference theorem (b)"). First pass: exact
  label match after normalization (case, whitespace, punctuation).
- Second pass: alias map for known variants, built by hand and
  recorded here (e.g., "11l" vs "Node 11l"; "the rose graph
  mechanism" vs "Node 11l"). No silent fuzzy matching — every
  alias is an explicit, reviewable entry.
- Unmatched labels stay as their own nodes. Over-merging is worse
  than under-merging; the atlas can show "possibly same as X" as
  a weak edge rather than collapsing.

## 2. Status reconciliation (chunk-local honesty)

R4 calibration rule: the same identity may be exact where derived
and computationally_verified where only checked — the merge layer
reconciles, it does not average. Rule:
- Keep the *strongest honestly earned* status per concept, with
  provenance (which chunk earned it).
- A killed status anywhere wins if the kill is a verdict about the
  concept itself (not about one chunk's reading of it); record the
  kill reason and its source chunk.
- Conflicting statuses that are both honest (derived in one doc,
  merely cited in another) keep the stronger + a note naming the
  weaker occurrence. Nothing is silently dropped: every
  chunk-concept survives either as the merged node or as a
  cited occurrence.

## 3. Edge union

- Union all edges, remapped to merged node ids.
- Duplicate (a, b, rel) triples collapse to one, with provenance
  count.
- Contradictory edges (a supports b in one chunk, a contradicts b
  in another) are kept as a flagged pair for human review — the
  merge never adjudicates; it surfaces.

## 4. Loops and strands

- Loops union (open questions are program-level assets).
- Strands: keep per-chunk strands as "views"; the atlas also
  builds program-level strands from the merged graph (connected
  components under depends_on/supports, labeled by the highest-
  status node).

## 5. Output

`atlas_graph.json`: nodes (id, canonical label, status, genre,
note, provenance chunks, occurrences), edges (a, b, rel,
provenance, count), loops, plus the alias map and the flagged
contradictions. This file is the atlas's single source of truth;
the illustration reads only this file.
