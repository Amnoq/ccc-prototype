# MESH-5 Prospective Pilot — Charter (DRAFT)

**Date:** 2026-10-09. **Status:** DRAFT ONLY — execution needs the router's
go/no-go. This charter authorizes nothing beyond the pilot experiment it
describes.
**Parent:** MESH-5 (mesh/DECISION_TREE.md). **Gate:** the connectivity
retrospective (mesh/CONNECTIVITY_RETROSPECTIVE.md) did NOT open a design
charter; it specified five prerequisites for a prospective pilot. This
charter operationalizes all five. It does not re-litigate the retrospective.

## 1. Objective and triadic fork

**Objective:** test whether connectivity-calibrated QUEUE handling beats
judge-alone QUEUE handling on the step-4 failure mode: human-1.0 probes
wrongly queued by an under-confident judge (16/32 in the retrospective).

- **Claim:** the M3* rule (defined §3) promotes conjectural probes out of
  the queue with a lower false-promotion rate than both controls at a
  fixed promotion budget.
- **Polar opposite:** connectivity adds nothing or degrades — M3* performs
  equal to or worse than the controls.
- **Null:** shuffled-connectivity control — permuted M3* scores perform
  identically to real M3* (the graph carries no signal).

**Primary endpoint:** false-promotion rate among promoted probes
(promoted probe with human grade < 1.0 = false promotion), at fixed
promotion budget K = N_conj/2 (top half by M3*). The M3* rule must beat
BOTH controls (§5) at p < 0.05 (stratified permutation, one-sided for the
directional claim, two-sided reported) AND clear an absolute floor: ≥15
points lower false-promotion rate than the shuffled null. A significant
but trivial win does not authorize a charter.

## 2. The five prerequisites, operationalized

**P1 — Denser link discipline.** Extraction rules (typed rels: `supports`,
`implements`, `exemplifies`, `refines`, `contradicts`):
- Every verdict record MUST carry ≥3 typed links (in or out); `contradicts`
  is a first-class type with a definition: a record contradicts another iff
  it asserts the negation of a claim the other asserts (not mere
  difference of topic or method). The extractor's brief includes 5 worked
  contradicts examples and 5 near-miss non-examples.
- **Shakedown gate (kill criterion K1):** before the pilot corpus is
  extracted, a 20-record shakedown must show mean degree ≥ 3.0 AND
  contradicts ≥ 5% of all links. Failure → revise the discipline,
  re-shake. The pilot does not start on a sparse graph (the retrospective's
  0.32 links/record is the failure mode being fixed).

**P2 — Pre-registered metric.** Primary: **M3\***, support-minus-contradict
with M4 independence weighting, defined exactly:
  M3*(r) = Σ_{s → r, rel ∈ {supports,implements,exemplifies,refines}} 1/outdeg(s)
         − Σ_{s → r, rel = contradicts} 1/outdeg(s),
  where outdeg(s) is the source's total out-degree over all rel types.
  (M4 ≈ M3 on the retrospective's sparse graph; they diverge on dense
  graphs — M3* is the hardened form, pre-registered here.)
  Secondary (pre-registered, non-decisive): M1 total degree — guards
  against M3* failing merely from contradicts-link sparsity.
  Not M5 (retrospective weakest, +0.10).
  **Choice rationale:** the pilot's claim is QUEUE-tier-specific, and the
  retrospective's QUEUE-tier pattern — the live thread — was carried by M3
  (wrongly-queued mean 0.344 vs correctly-queued 0.024, p≈0.05, n=16+14;
  Cohen's d ≈ 1.0 on the mapped data). M3 is the faithful
  operationalization of the proposal's relative-support mechanism; M1 does
  not implement it.

**P3 — Prospective test.** New extractions (never the step-4 corpus):
8 chunks × 15 probes = 120 probes, all judged by ONE fixed judge (j4 —
pre-registered; rationale §4). Candidate pool: probes j4 labels
`conjectural` (expected ~64 at j4's 53% conjectural rate). Analysis
stratified by chunk (stratified permutation test), which breaks the
retrospective's chunk/judge confound. Mapping gate (kill criterion K2):
≥90% of probes must map to D-wire records (retrospective: 95.8%).

**P4 — Goodhart guard.** Two extractors, pre-registered:
- E_blind extracts the full pilot corpus NEVER told the calibration rule
  or the promotion mechanism.
- E_told extracts a 40-record subset AFTER being told "high
  support-minus-contradict upgrades verdicts."
- Held-out link audit: an independent checker re-verifies every link on a
  held-out 40 records against the typed-rel definitions (pre-registered
  rubric), blind to which extractor produced them.
- **Kill criterion K3:** if E_told's mean degree exceeds E_blind's by
  >25%, OR >15% of audited links fail their type definitions → NO-GO
  regardless of the primary endpoint. The signal is contaminated; the
  pilot cannot distinguish calibration from inflation.

**P5 — Independence hardened.** M3* (§P2) is the hardened form,
specified before measurement. No post-hoc reweighting: the weight
1/outdeg(s) is fixed here, not tuned on the pilot data.

## 3. Fixed-judge protocol

Judge j4 is fixed for all 120 probes. Rationale: j4 has the largest
conjectural pool (16/30 ≈ 53% in step-4 data; j3 gives 5/30 — too few
for power) AND j4's under-confidence on conjectural (9 of 16
conjecturals were human-1.0) IS the target pathology: the false queues
M3* is supposed to rescue. j3 is better calibrated on conjectural, which
makes it the wrong instrument for testing a rescue mechanism.
Fallback (pre-registered): if j4 is unavailable, j3, with power
recomputed for its conjectural rate before starting.

## 4. Sample-size rationale

Powered on the retrospective QUEUE-tier effect (M3 means 0.344 vs 0.024,
pooled sd 0.315, d ≈ 1.0, n=16+14), discounted for winner's curse to
d = 0.7. Two-sample separation at d = 0.7, α = 0.05 two-sided, 80% power
needs ≈ 32 per group → **≈64 conjectural probes**. At j4's 53%
conjectural rate, 120 total probes (8×15, chunk-stratified) deliver it.
Assumptions stated: base rate of human-1.0 among conjecturals ≈ 50%
(retrospective: 16/30); the stratified permutation test recovers the
t-test's power up to the stratification gain. If the candidate pool
falls below 48 conjecturals, the pilot is underpowered → stop and
re-scope (kill criterion K4).

## 5. Controls and analysis

- **C1 (judge-alone):** top-K by j4's within-label confidence if emitted;
  else random-K. (Judge-alone QUEUE promotes nothing on its own; at a
  fixed review-load budget the comparison is against the judge's own
  ordering.)
- **C2 (null):** top-K by chunk-stratified shuffled M3* (1,000+
  permutations; destroys graph signal, keeps the score distribution).
- **Analysis:** stratified permutation test on (false-promotion rate:
  rule − control), one-sided α = 0.05 for the directional claim,
  two-sided reported. M3* must beat BOTH C1 and C2 AND clear the 15-point
  absolute floor (§1) for a GO.
- **Secondary (pre-registered):** the retrospective-derived absolute
  threshold k = 0.18 (midpoint of the retrospective QUEUE-tier means,
  declared retrospective-derived, not optimized): does "M3* ≥ 0.18 →
  promote" replicate? Non-decisive; reported.
- **Grade-skew kill (K5):** if >85% or <15% of the candidate pool grades
  1.0, separation is unmeasurable → stop, re-scope.

## 6. Kill criteria (any one stops the pilot)

- K1: link-discipline shakedown fails (mean degree < 3.0 or contradicts
  < 5%).
- K2: probe→record mapping < 90%.
- K3: Goodhart guard fails (E_told inflation >25% or audit failure
  >15%) → NO-GO regardless of primary.
- K4: candidate pool < 48 conjecturals (underpowered).
- K5: grade skew beyond 85%/15%.

## 7. What GO authorizes — and what it does not

- **GO authorizes:** drafting a DESIGN CHARTER for the connectivity-
  calibrated QUEUE tier, which itself goes through pre-registration and
  a versioned spec change. Nothing else.
- **GO does NOT authorize:** any change to COLLAPSE_SPEC tiers (Rule 2:
  QUEUE → ACT remains forbidden until a versioned spec change says
  otherwise); any production use of connectivity calibration; any
  relaxation of the derivation/application split (the router owns the
  tiers; this pilot measures, it does not re-tier).

## 8. Non-goals

- No deployment of any kind.
- Does not re-litigate the retrospective (its numbers stand as cited).
- Does not test MESH-5 beyond the QUEUE tier.

## Epistemic labels

| Claim | Status |
|---|---|
| Retrospective numbers cited (M3 0.344 vs 0.024, d≈1.0, j4 rates) | computationally verified (recomputed from mesh/CONNECTIVITY_RETROSPECTIVE_DATA.json 2026-10-09) |
| "Signal exists" | conjectural (lean-positive, unproved) |
| This charter's procedures (thresholds, n, guards) | heuristic (design judgment, pre-registered) |
| "M3* primary, M1 secondary" | design choice, defended in P2 |

*Draft only. Execution needs the router's go/no-go.*

## 9. Outcome (2026-10-09) — NO-GO on link discipline

The pilot ran to the K1 shakedown gate and stopped there, per charter §6.
Attempt 1 (Atlas-9 report, brief v1): mean degree 4.2 ✓, contradicts
1/42 = 2.4% ✗. Attempt 2 (a3_test report, brief v2 with limitation
records + scope-narrowing principle): mean degree 4.9 ✓, contradicts
2/49 = 4.1% ✗ (independently recomputed; both contradicts borderline —
against broad readings the source never asserted). Two failures exhaust
the one allowed revision. **Verdict: NO-GO.** Phase B never started; no
human grading was requested. The 5% contradicts bar assumed a dialectic
density the program's reports do not carry; forcing it would manufacture
false contradicts and poison M3*. MESH-5 stays OPEN. Run log:
mesh/mesh5_pilot/RUN_LOG.md.


## 10. Fallback (b) amendment (2026-10-09 — router's word)

The contradicts-vector branch
(mesh/mesh5_pilot/contradicts_branch/CONTRADICTS_BRANCH.md) earned the
dead end: five cells, 100 records, 237 links — raw contradicts rates moved
with the brief (0.0%→5.7%→6.7% on the same corpus) but independent
adjudication collapsed every a3_test cell to 0% genuine (pure definitional
inflation); the strict definition is not vacuous (2 genuine hits in the
step-4 cell, 4.1% < 5% bar). No cell cleared both pre-registered bars. The
support-vs-contradict "relative" vocabulary is untestable on this material.
The router chose fallback (b): relaunch with M3 as pure in-support. This
changes the pre-registered metric — recorded here with the router's
explicit word.

**Amended primary metric — M3_supp** (replaces M3* in §2-P2):
  M3_supp(r) = Σ_{s → r, rel ∈ {supports,implements,exemplifies,refines}} 1/outdeg(s),
  where outdeg(s) is the source's total out-degree over all rel types.
  (M3* minus the contradicts leg. Secondary stays M1 total degree.)
**Continuity:** the retrospective's M3 QUEUE-tier means (wrongly-queued
0.344 vs correctly-queued 0.024, p≈0.05) were already support-based in
practice — the retrospective data carried no contradicts
(CONNECTIVITY_RETROSPECTIVE.md: "reduces to in-support"). Fallback (b)
makes the pre-registration honest about what the retrospective measured.
The secondary threshold k = 0.18 (§5) is UNCHANGED — it was derived from
those same support-based means.

**K1 revised:** mean degree ≥ 3.0 stays; the contradicts ≥ 5% bar is
DROPPED (the bar that killed the pilot; the branch proved it unmeetable
honestly). Extractor brief: v1 strict type discipline, contradicts
permitted when genuinely present but never forced, no quota, none of v2's
scope-narrowing/forcing language. One revision/retry still allowed; two
failures still stop the pilot.

**Unchanged:** the triadic fork (§1, now about M3_supp), fixed judge j4
(§3), sample-size rationale (§4), controls C1/C2 (§5, computed on
M3_supp), the GO bar (beat both controls one-sided p<0.05 AND the 15-point
false-promotion floor), K2/K3/K4/K5, §7's authorization limits. K3's
Goodhart guard still applies: E_told learns the promotion rule
(top-half by M3_supp).

**What the claim now is — and is not.** The pilot tests whether
*in-support connectivity* rescues faithful probes an under-confident judge
sends to QUEUE. It does NOT test the QUEUE tier's "relative"
(support-vs-contradict) vocabulary — that dead end is earned and stays
recorded. A GO here authorizes a design charter for *in-support*
connectivity calibration only, per §7.

New work lives under mesh/mesh5_pilot/fallback_b/. The §9 NO-GO record
stands as the pilot's first run; this is its second run under amendment.

## 11. Fallback (a) as co-primary (2026-10-09 — router's word)

The router: "like usual I would like to see both." Fallback (a) joins
fallback (b) as a **co-primary** on a single corpus, single graph, single
grading session — not a second run. Rationale: one grading burden on the
router instead of two, and same graph/labels gives the cleanest comparison
of where the signal lives (M1 GO without M3_supp GO → the signal is raw
connectivity, not support structure; both GO → support structure adds
nothing beyond degree; neither GO → connectivity doesn't calibrate).

**M1(r)** = total degree (in + out, all rel types) — the retrospective's
definition, unweighted (no invented weighting). The extractor still pulls
typed links (M3_supp needs types); M1 counts every link regardless of type.

**Per-metric machinery** (each metric gets the full triadic treatment):
- Claim / polar opposite / null fork per metric; C1 (judge-alone top-K)
  and C2 (chunk-stratified shuffled) computed per metric.
- GO bar per metric: beat both controls one-sided p<0.05 AND the 15-point
  absolute false-promotion floor (§1).
- Secondary threshold for M1: k_M1 = 0.625 — midpoint of the
  retrospective's M1 QUEUE-tier means (correctly-queued 0.458 vs
  wrongly-queued 0.792), declared retrospective-derived, not optimized;
  non-decisive, reported. Density-transfer caveat: the retrospective graph
  was sparse (mean M1 ≈ 1.09); the pilot graph is dense by K1 design, so
  the absolute threshold may not transfer — the top-half rule (§1) is the
  density-invariant decision rule.

**Multiplicity, disclosed not hidden:** two pre-registered primaries on
one corpus, each tested at α=0.05 against its own controls. There is no
combined "pilot GO" claim — verdicts are per-metric, and the family-wise
false-GO rate exceeds 5%. Reported plainly in the verdict.

**Per-metric GO authorization:**
- M3_supp GO → §10's authorization (design charter for in-support
  connectivity calibration).
- M1 GO → a finding that raw connectivity calibrates the judge. It does
  NOT authorize a QUEUE-tier mechanism charter — M1 doesn't implement the
  QUEUE-tier mechanism (the retrospective's QUEUE-tier pattern was carried
  by M3, not M1). Mechanism work needs a separate design.

**Unchanged:** K1/K2/K4/K5 (§10 versions); K3's Goodhart guard now applies
to both metrics (E_told learns both promotion rules — top-half by
M3_supp, top-half by M1; inflation >25% on either → NO-GO); §7 limits.
The router's single grading session serves both analyses.
