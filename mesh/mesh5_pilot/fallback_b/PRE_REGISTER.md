# MESH-5 Pilot, Run 2 (Fallback b) — Pre-registration

**Date:** 2026-10-09. **Amendment:** charter §10 (router's word).
**Work dir:** mesh/mesh5_pilot/fallback_b/. Atlas records read-only.
Written BEFORE any extraction for this run.

## Amendment — dual primary (charter §11, router's word 2026-10-09)

The single-primary fork below is AMENDED, not replaced: fallback (a)
joins as **co-primary M1** on the same corpus, same graph, single
grading session — not a second run. Nothing already extracted changes
(the extractor pulls typed links; M1 counts every link regardless of
type). This amendment is recorded here explicitly; the run does not
proceed on the old registration.

**M1(r)** = total degree (in + out, all rel types), unweighted — the
retrospective's definition.

**Per-metric machinery** (each metric gets the full triadic treatment):
- Triadic fork per metric: claim / polar opposite / null.
- C1 (judge-alone top-K) and C2 (chunk-stratified shuffled) per metric.
- GO bar per metric: beat both controls one-sided p<0.05 AND the
  15-point absolute false-promotion floor (§1).
- Secondary threshold for M1: k_M1 = 0.625 — midpoint of the
  retrospective's M1 QUEUE-tier means (correctly-queued 0.458 vs
  wrongly-queued 0.792), retrospective-derived, not optimized;
  non-decisive, reported. Density-transfer caveat: the retrospective
  graph was sparse (mean M1 ≈ 1.09); the pilot graph is dense by K1
  design, so the absolute threshold may not transfer — the top-half
  rule (§1) is the density-invariant decision rule.

**Multiplicity, disclosed not hidden:** two pre-registered primaries
on one corpus, each tested at α=0.05 against its own controls. There
is NO combined "pilot GO" claim — verdicts are per-metric, and the
family-wise false-GO rate exceeds 5%. Reported plainly in the verdict.

**Per-metric GO authorization:**
- M3_supp GO → §10's authorization (design charter for in-support
  connectivity calibration).
- M1 GO → a finding that raw connectivity calibrates the judge. NOT a
  QUEUE-tier mechanism charter — M1 doesn't implement the QUEUE-tier
  mechanism (the retrospective's QUEUE-tier pattern was carried by M3,
  not M1). Mechanism work needs a separate design.

**K3** now covers both metrics: E_told learns both promotion rules
(top-half by M3_supp, top-half by M1); inflation >25% on either →
NO-GO.

## Triadic fork — M3_supp (primary 1)

- **Claim:** in-support connectivity (M3_supp, the retrospective's
  M3/M4 measure) rescues faithful probes that the under-confident
  judge j4 sends to QUEUE: at a fixed top-half promotion budget among
  conjectural probes, M3_supp shows a lower false-promotion rate than
  both controls.
- **Polar opposite:** connectivity adds nothing or degrades —
  M3_supp performs equal to or worse than judge-alone and the
  shuffled null.
- **Null:** chunk-stratified shuffled M3_supp scores perform
  identically to real M3_supp (the graph carries no signal).

## Triadic fork — M1 (primary 2)

- **Claim:** raw connectivity (M1 total degree) rescues faithful
  probes that the under-confident judge j4 sends to QUEUE: at a
  fixed top-half promotion budget among conjectural probes, M1 shows
  a lower false-promotion rate than both controls.
- **Polar opposite:** raw degree adds nothing or degrades — M1
  performs equal to or worse than judge-alone and the shuffled null.
- **Null:** chunk-stratified shuffled M1 scores perform identically
  to real M1 (the graph carries no signal).

## Verdict rule (pre-registered, per metric)

M3_supp = Σ_{s → r, rel ∈ {supports,implements,exemplifies,refines}}
1/outdeg(s). M1 = total degree (in + out, all rel types), unweighted.
Analysis per metric: stratified permutation test on
(false-promotion rate: rule − control), one-sided α = 0.05 for the
directional claim (two-sided reported).

**GO (per metric)** iff: the metric beats C1 (judge-alone top-K) AND
C2 (shuffled) one-sided p < 0.05 AND clears the 15-point
false-promotion floor vs the shuffled null. Significant-but-trivial
does not authorize a charter. NO combined "pilot GO" — verdicts are
per-metric with the two-shot multiplicity disclosed.
**NO-GO** otherwise, or on any kill gate. A GO authorizes ONLY what
§11's per-metric authorization says — never deployment or tier
changes.
Secondary (non-decisive), reported: k = 0.18 threshold replication
for M3_supp (derived from the retrospective's support-based
QUEUE-tier means); k_M1 = 0.625 for M1 (midpoint of retrospective
M1 QUEUE-tier means 0.458/0.792, with the density-transfer caveat:
retrospective mean M1 ≈ 1.09 on a sparse graph; the pilot graph is
dense by K1 design, so the absolute threshold may not transfer —
the top-half rule is the density-invariant decision rule).

## Kill gates (charter §6 + §10)

- **K1:** 20-record shakedown, mean degree ≥ 3.0 ONLY. No contradicts
  bar (dropped per §10; the contradicts-vector branch earned that dead
  end). One revision/retry allowed; two failures → STOP, NO-GO.
- **K2:** probe→record mapping ≥ 90%.
- **K3:** Goodhart guard — E_told mean degree ≤ E_blind + 25% on
  EITHER metric's promotion rule AND held-out audit fail ≤ 15%;
  else NO-GO regardless of primary. E_told learns BOTH promotion
  rules: "top-half by M3_supp" and "top-half by M1."
- **K4:** candidate pool ≥ 48 conjecturals.
- **K5:** human-1.0 rate in the candidate pool within [15%, 85%].

## What this run does NOT test

The QUEUE tier's "relative" (support-vs-contradict) vocabulary —
that dead end is earned (CONTRADICTS_BRANCH.md) and stays recorded.
This run tests in-support connectivity (M3_supp) and raw
connectivity (M1) only. An M1 GO is a raw-connectivity finding, NOT
a QUEUE-tier mechanism — mechanism work needs a separate design.

## Mandatory stop

After Phase B judging, BEFORE primary analysis: build the grading
harness, report the conjectural candidate-pool size, and STOP.
The router grades the candidates himself. Analysis resumes only
after his grades arrive.
