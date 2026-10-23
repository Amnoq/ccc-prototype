# Collapse Specification, v1.1 — label → action tiers

**Date:** 2026-10-08 (v1) → 2026-10-09 (v1.1). **Status:** v1.1 adopted —
the v1 tiers are unchanged; v1.1 adds the judge calibration procedure
(MESH-4a) that v1's calibration note called for.
**Companion:** VERDICT_PACKET_SPEC.md (what crosses the boundary);
this document says what the application layer does when it arrives.

## Why this exists

Every deployment surface collapses a rich verdict to act or
don't-act. The field does it silently (binary judgment, provenance
discarded). This spec does it explicitly: the label travels with
the action, and the tier it lands in was written down before the
first judgment was ever issued. The derivation earns the label;
the router sets the tiers; the mapping between them is
pre-registered and auditable. That is the derivation/application
split, honored at the boundary.

## The tiers

| label | tier | action | rationale |
|---|---|---|---|
| `exact` | **ACT** | act immediately, no further check | proved — no numerics needed, nothing left to check |
| `computationally_verified` | **ACT with spot-check** | act; the check is rerunnable and logged | verified live with controls; the rerun is the audit trail |
| `conjectural` | **QUEUE for review** | never auto-act; a human or stronger instrument decides | precise but unproved — the statement is sharp, the earning isn't done |
| `heuristic` | **SURFACE only** | display, never gate | suggestive, not precise — may inform, may not decide |
| `killed` | **BLOCK the claim** | the claim must not drive action; any reference to it is flagged | the claim died by verdict — acting on it is the D-ledger's failure mode |
| `superseded` | **FOLLOW the heir** | redirect to the heir record; the heir's label governs | supersession is a verdict with a successor — the packet carries the heir ref |
| `unstated` | **NO ACTION** | questions carry no action, ever | no epistemic claim is being made — there is nothing to collapse |

## Rules (load-bearing, not guidance)

1. **Pre-registered, not tuned.** These tiers are set before
   deployment and change only by a new version of this spec, with
   the change recorded (the ledger rule: no silent changes).
2. **Labels only weaken downstream** (D20). The application layer
   may treat a verdict *more* cautiously than its tier (ACT →
   QUEUE on external grounds) but never *less* (QUEUE → ACT is
   forbidden). Caution is always permitted; confidence never is.
3. **Every collapsed action logs its packet.** The action and the
   packet are stored together — the audit trail is the pair, not
   the action alone. A decision log without packets is a
   PolicyLM-style silent collapse and fails this spec.
4. **Killed claims are load-bearing.** A `killed` packet arriving
   at the boundary means something downstream still references a
   dead claim — that is flagged, not silently dropped. The
   dead-end ledger exists so the dead stay dead; the BLOCK tier
   is its enforcement arm.
5. **Supersession chains resolve.** If the heir is itself
   superseded, follow the chain to the live record. A chain that
   does not terminate in a live label is malformed — flag it.
6. **The router owns the tiers; the derivation owns the labels.**
   Neither side may rewrite the other's half. A deployment that
   needs a different mapping writes a new spec version — it does
   not edit labels, and the derivation does not edit tiers.

## What this does not do

- It does not set policy content (what *should* be done) — only
  how earned confidence maps to action. Policy is the router's;
  this spec is the machinery's.
- It does not replace the demonstration (step 4 of the plan):
  whether labeled collapse beats binary judgment on a real task
  is measured, not asserted here.

---

*Spec v1, 2026-10-08. Pre-registered. The collapse is explicit so
the field's silent one is never the default.*

## Backward touch — Step 4 demonstration (2026-10-08)

SURVIVES AS FRAMEWORK, QUALIFIED AS CALIBRATION. The tiers
applied mechanically across 120 probes and produced a real,
discriminating operating point (precision 84.8%→91.9% vs binary).
But: the conjectural→QUEUE mapping combined with cautious judges
queued 16 human-1.0 probes (all `conjectural` — judge
under-confidence, with large inter-judge variance: 2 vs 17
conjectural per 30 probes). Rule 2 (caution permitted,
confidence never) is validated by the error direction. The
spec needs a calibration note, not a rewrite:

**Calibration procedure (v1.1, adopted 2026-10-09).** The collapse tiers
assume calibrated judges. Deployments MUST run this procedure before
treating QUEUE volume as pure signal — an over-cautious judge population
turns the QUEUE tier into a review-load sink. The mapping is pre-registered;
the judges are the variable. (Status of this procedure: design/heuristic —
adopted on the MESH-4a evidence, revisable by a new spec version.)

1. **Measure per-judge × per-label.** Calibration is not one caution dial
   (MESH-4a: j3 over-confident on `computationally_verified`, well-calibrated
   on `conjectural`; j4 perfect on cv but under-confident on conjectural).
   Grade a 360-probe sample (97 emissions per decision-relevant label) and
   build the label×grade cross-tab per judge.
2. **Wilson-CI acceptance bands.** A judge passes a label iff the Wilson
   confidence interval on the label's grade lower bound clears the band.
   Bands are set in the deployment's calibration plan, recorded before
   measurement.
3. **Re-briefing, never remapping, on failure.** A judge that fails a band
   is re-briefed on that label and re-measured. Per-judge label→tier
   remapping is forbidden — it trades caught queues for new false acts
   ~1:1 (MESH-4a) and violates Rule 2's direction (caution permitted,
   confidence never).
4. **Two-strikes retirement.** A judge failing the same band twice is
   retired from that label. (Chunk/judge confound is total — chunks nest
   in judges — so a persistent failure reads as a judge effect.)
5. **Drift spot-checks.** Re-run a small graded sample periodically;
   a judge drifting out of band returns to step 3.

## Version history

- v1 (2026-10-08): tiers pre-registered; calibration note as candidate.
- v1.1 (2026-10-09): tiers unchanged; calibration note promoted to the
  adopted procedure above (MESH-4a). No verdict changes; the procedure
  governs future judge calibration only.
