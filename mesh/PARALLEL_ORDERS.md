# PARALLEL ORDERS — 2026-10-08

Two self-contained work orders for the parallel accounts. Each account takes
ONE order. Neither order needs the router's grading or his word to execute;
both produce drafts/findings that come back through the router for his call.

Routing (his standing rule): parallel instances are data-starved; the main
account is the data hub. Everything here came from the main account through
him. Results return the same way. Nothing here authorizes contacting him
mid-run — finish the order, report back.

---

## ORDER 1 — Judge calibration study (step-4 data)

**Why:** Step 4 (step4/STEP4_REPORT.md) found the labeled arm's 16 "misses"
were all conjectural→QUEUE — judge under-confidence, not label failure —
with sharp judge variance (one judge 17 conjecturals in 30, another 2 in
30). The collapse spec's v1.1 candidate requires measuring judge
calibration on a graded sample first. This order produces that measurement
and the concrete procedure.

**Data (supplement zip, from the main account):**
- step4/step4_results.json — 120 probes: human grade + Arm A/B/C actions
  and labels per probe
- step4/judge_outputs/j1..j4/ — raw per-judge outputs (j1: c01–c03,
  j2: c04–c06, j3/j4: c07–c12; 30 probes each)
- step4/analyze_step4.py — the original analysis script (reference)

**Task:**
1. Per-judge label histograms and per-judge action distributions.
2. Calibration tables: P(human grade = 1.0 | judge label) per judge and
   pooled, for every label the judges emitted. This is the core measurement.
3. The 16 wrongly-queued full-fidelity probes: which judges produced them,
   under what labels, and whether a per-judge recalibration would have
   caught them.
4. Chunk-stratification check: c10–c12 (the under-confident judge's
   chunks) vs the rest — how much of the miscalibration is judge vs chunk.
5. Propose the concrete calibration procedure for COLLAPSE_SPEC v1.1:
   how a new judge is measured on a graded sample, what recalibration is
   applied, minimum sample size, and re-measurement cadence. Make it
   implementable, not aspirational.

**Rules:** analysis only — no re-grading, no new judgments, no contacting
the router. Epistemic labels on every finding (computationally verified /
conjectural / heuristic). Triadic where it fits: report what the data
supports, what would falsify it, and the null reading.

**Deliverable:** a calibration report (markdown), returned through the
router, ending with the proposed v1.1 procedure and its own chain.

---

## ORDER 2 — MESH-5 prospective pilot charter (draft)

**Why:** The connectivity retrospective
(mesh/CONNECTIVITY_RETROSPECTIVE.md) closed the gate on a design charter
but specified the chain: five prerequisites for a prospective pilot. This
order drafts that pilot's charter. Draft ONLY — execution needs his
go/no-go, which is parked with him.

**Inputs (already in your anchor bundle):**
- mesh/CONNECTIVITY_RETROSPECTIVE.md — §"What a design charter would
  need": the five prerequisites (denser link discipline ~3+/record with
  typed rels incl. contradicts; pre-registered metric M1 or M3;
  prospective test on new extractions vs human grades, chunk-stratified,
  judge fixed; Goodhart guard via held-out link audit with the extractor
  blind to the rule; hardened independence weighting, M4 scheme or better)
- mesh/DECISION_TREE.md (MESH-5), COLLAPSE_SPEC.md v1

**Task:** write the full pilot charter:
1. Objective and triadic fork — claim (connectivity-calibrated QUEUE
   beats judge-alone QUEUE on false-queue rate at fixed review load);
   polar opposite (connectivity adds nothing or degrades); null
   (shuffled-connectivity control).
2. Each of the five prerequisites operationalized: exact procedures,
   not slogans. Choose M1 or M3 with a stated reason (the retrospective
   names both as best carriers — pick one and defend it).
3. Link discipline spec: extraction rules that yield ~3+ typed
   links/record, with `contradicts` used as designed.
4. Goodhart guard design: the held-out link-audit, extractor blind to
   the calibration rule, pre-registered.
5. Sample-size rationale, chunk stratification, fixed-judge protocol,
   kill criteria (what stops the pilot), and what a "go" result would
   authorize vs what it would not.
6. Explicit non-goals: this charter does not authorize deployment, and
   the pilot does not re-litigate the retrospective.

**Rules:** follow METHODOLOGY.md (triadic forks, epistemic labels,
pre-registration discipline). Do not start the pilot. Do not contact the
router mid-draft except to report completion.

**Deliverable:** the charter (markdown), returned through the router for
his go/no-go.
