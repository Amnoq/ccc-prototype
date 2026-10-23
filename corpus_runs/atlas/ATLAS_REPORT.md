# Lemma Atlas — pilot report

Date: 2026-10-06/07. The real capability test: mass-extract a
research corpus one-shot and illustrate its epistemic structure.

## Pipeline

1. **Chunk**: 23 docs / 43,365 words → 30 chunks (~2.5k words).
2. **Extract**: coordinator fanned out 30 one-shot R4 drafters
   (batches of 6–8). 30/30 files written, no drafter needed
   redirection. Totals: **545 concepts · 480 anchors · 421 edges ·
   45 loops**.
3. **Validate**: 28/30 clean on arrival; 2 had malformed loop
   entries (bare id strings instead of objects) — repaired
   mechanically to `{"concept_id": id}`, revalidated clean.
   Aggregate statuses: exact 232 · computationally_verified 127 ·
   killed 41 · heuristic 54 · conjectural 26.
4. **Merge** (`merge_atlas.py`, implements MERGE_PLAN.md):
   canonical-ID subject grouping → **112 subjects + 193
   standalone nodes · 344 cross-subject edges · 45 loops ·
   0 flagged contradictions · 0 dangling edges**.
   - Status reconciliation: strongest honestly earned wins, killed
     facets never kill a live subject, provenance recorded.
   - One genuine over-merge caught and fixed: archive_dead_ends
     D1–D13 (dead-end ledger numbering) vs decision-tree D-items
     (D5 Figueiredo steer) — split into `ledger-d<n>` namespace
     by source, recorded as explicit split for review.
   - Known hard case reconciled correctly: interference theorem
     (b) was computationally_verified in the 11q chunk (written
     before Node 16) and exact in the lemma chunks — merge keeps
     exact with the temporal provenance note.
5. **Illustrate**: `atlas.html` — self-contained interactive
   force-directed graph. Node color = epistemic status, size ∝
   facet count; killed nodes red; open (unanchored) nodes hollow
   white. Click any node for facets, notes, merge notes,
   provenance chunks, relations. Search, status filters,
   detail-node toggle, open-loops panel (45).

## Grading vs known program structure

13 spot-checks against the decision tree / complete map: **10/13
strict pass**. The 3 divergences were inspected and judged
defensible under the stated reconciliation rule (facets, not
subjects, carry the nuance; the detail panel shows them):
- node11n → exact (not computationally_verified): the exact
  facets are exact *about* 11n's role/consequence (three-witness
  structure; prime-independence as theorem consequence), not
  claims that the experiment was a proof. Weaker statuses
  recorded in the merge note.
- node11p → exact: "puzzle resolved" facets are exact (the
  explanation is exact given the theorem); the PARTIAL gate
  verdict facet stays computationally_verified in the panel.
- xp-branch → heuristic: no drafter marked the branch itself
  killed; its death is recorded distributively (node11g "CLOSED
  negative" exact; "operator deaths" killed). Not hand-upgraded.

## Honest limitations

- Lemma interiors thin under the density cap (the measured
  mechanism frontier): the atlas shows standings and relations,
  not proof steps.
- Entity resolution is ID-regex + explicit namespace split; at
  arXiv scale this is the deep R&D problem, not a solved one.
- 3 chunks carried drafter-flagged soft calls into the merge
  (EXPERIMENT_REPORT c8 possibly underrated; tones_signchange c8
  weakest exact; FRAMEWORK p2 practices left anchorless) —
  recorded in the coordinator report, surfaced in facet notes,
  not silently fixed.

## Verdict

The pilot passes: one-shot extraction held across 30 varied
chunks (28/30 clean first try, 2 mechanically repaired), the
merge preserved the program's known epistemic structure
including its traps, and the illustration makes the distinction
visible — knowledge as relations with standings — instead of
arguing it.
