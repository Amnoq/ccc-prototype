# Gate 4 / Tier A+B calibration battery — charter

Date: 2026-10-07. Pre-registered: this document is the plan; it does not
execute. One word from the router launches it.

## What the battery measures

Whether Tier A (mechanical) and Tier B (ladder-verdict grader) actually
discriminate — catch rates reported for each planted variant, **no credit
without separation**. This is the agreed next step after protocol v5
("the next step isn't v6, it's running the battery"), and its outcome is
the stop rule's first application: protocol review ends when rounds stop
producing verdict-changing defects; the battery says whether the gates
hold on real work.

## Corpus

- 480 anchors across the 30 one-shot R4 extractions
  (`corpus_runs/atlas/extractions/*.json`), the graded corpus behind the
  0/120 fabrication record.
- The 120 parity-probe records (`corpus_runs/r4/rescore_v7/`) as the
  human-graded reference.

## Step 0 — span attribution (prerequisite, non-optional)

The R4 extraction anchors carry note + status only — no verbatim spans.
Gate 4 cannot run without them. Before any grading: attach verbatim
source spans (chunk + start/end offsets) to every anchor. Distributed
support: spans are *jointly sufficient, each verbatim* (v2 defect 2,
integrated). Edge spans in the same pass (v3 defect 2, integrated).
This pass is mechanical authorship, not grading — it is the extractor's
job, not the critic's.

## Tier A — build

A rerunnable script over attributed spans: span exists verbatim in the
source chunk, non-empty; for exact, span must contain the derivation;
for computationally_verified, the recorded scope. Kills/supersessions
held to the same mechanical check. This catches fabricated spans — it
does not catch status inflation (v2 defect 1; that is Tier B's job).

## Tier B — build

The ladder-verdict grader protocol:

- Grader receives the span(s) plus the P1 definition of the status
  ladder, **never the claimed status**, never the chunk.
- Returns the highest rung the span supports: heuristic /
  conjectural / computationally_verified / exact / insufficient.
- Claimed above supported = inflation (hard flag); claimed below =
  logged deflation candidate; absence-defined rungs credited honestly
  as "not contradicted by the span" (v3 defect 1, integrated).
- Kills: refuted-exact / refuted-computational / refuted-heuristic /
  insufficient. Supersessions: span must contain heir + replacement
  relation. Edges: span + relation definition → supports/insufficient
  (v3 defect 2, integrated).

## Planted variants (the triad on the gate itself)

1. **Inflation** (polar opposite): each status raised one rung.
   Battery valid only if Tier B flags it.
2. **Deflation** (P7.3: same failure): each status lowered one rung;
   heuristic excluded (no rung below). Deflation catch measured as
   **excess over the originals' baseline** of honest under-claiming
   (v4 defect 3, integrated).
3. **Wrong relation**: planted wrong-rel edges (v3 defect 2).
4. **Fabricated kill**: a kill label on a span with no refutation
   (v4 defect 3 — a kill is the costliest fabrication; it builds a wall).

Null control: content-free chunk (boilerplate/TOC/references) →
zero anchors, zero edges; anything else is fabrication by construction
(v1 correction owned on the record). Polar-opposite control:
pure-definitions chunk → **zero anchors**, since definitions are
concepts, not claims (v2 defect 3, tightened past Claude's formulation).

## Reporting rule

- Catch rates for all four planted variants plus both controls.
- Every fabrication rate as k/n with the 95% upper bound; "zero
  fabrication" retired as a standing claim (0/120 → ≤2.5% at 95%,
  rule of three; v3 defect 3, integrated).
- Bounds computed with **chunks as the unit** (120 anchors from a few
  chunks are not independent draws; v4 defect 4).
- Planted-shift rates labeled as what they are: natural inflation is
  harder to catch than one-rung shifts; a grader from the extractor's
  model family has correlated errors (v4 defect 4).
- Sampling is a **tripwire, not a certificate**: a fabrication found
  in a sample voids that run and triggers full grading (v4 defect 4).

## Decision rule (pre-registered)

- If Tier A/B separate the planted variants from the originals with
  reported catch rates, the gates are credited and protocol review
  ends under the stop rule (defects stop being verdict-changing →
  review over).
- If Tier B cannot separate them, it is not a discriminating test and
  is not credited as a gate — the protocol goes back to design, not
  to more review.

## Out of scope

Rule 9 (selection audit / blind slot) is instrumentation of the router,
not of the gates; it rides along once dosing commissions resume but is
not part of this battery. The dosing protocol governs any future
critic involvement in the battery's grading; nothing here commissions
the critic.
