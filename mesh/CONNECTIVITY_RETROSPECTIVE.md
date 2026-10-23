# MESH-5 Gate: Connectivity Retrospective — Full Report

**Date:** 2026-10-08. **Gate for:** MESH-5 (connectivity-based
auto-calibration of the QUEUE tier — the user's proposal).
**Status:** complete; verdict adjudicated below.
**Method:** `~/workspace/prime-sieve-geometry/METHODOLOGY.md`.
**Analysis script (rerunnable):**
`~/workspace/ccc-prototype/mesh/retrospective_analysis.py`.
**Data:** `~/workspace/ccc-prototype/mesh/CONNECTIVITY_RETROSPECTIVE_DATA.json`.

## Question (MESH-5's gate)

Does D-wire record connectivity predict human fidelity grades?
The proposal being tested is **conjectural** until this analysis
says otherwise. Correlation is not calibration — even a strong
correlation would warrant a design charter, not a deployment.

## The mapping problem (stated honestly)

Probes are per-chunk fidelity judgments (P1..P10 × 12 chunks);
records are D/G/V/B/C/L extractions. They are NOT 1:1 by
construction, and the probes judge the *v7* extraction while the
records are the *CCC-2* extraction — two different extractions of
the same source chunks.

**Mapping method:** chunk-scoped content overlap. For each probe,
evidence text = the Step 4 judges' Arm-B claim texts (4 judges,
blind) + the human miss note. For each same-chunk non-L record,
text = full record dump (subtitle/label/title/subject/note/rule/
generates/verified/boundary — D-items carry content in
rule/generates/verified, not just the subtitle; an early version
of this script missed that and mapped only 75/120 — caught and
fixed before analysis). Score = token overlap normalized by
geometric mean of lengths; mapped if ≥2 content tokens overlap
and normalized score > 0.05; multi-map (≤3 records within 80% of
best), aggregated by mean (primary) and max (sensitivity).

**Coverage: 115/120 probes mapped (95.8%); 5 unmapped.**
Unmapped probes are a finding, not a failure — they are real
content probes whose vocabulary diverged from the D-wire
records'. No mappings forced.

## The link graph (what the instrument actually is)

- 171 non-L records, 54 links (0.32 links/record).
- **82/171 records (48%) have degree 0.** The graph is sparse —
  the extractor was never instructed to link densely.
- Rel vocabulary in data: supports 25, refines 6, bounds 6,
  depends_on 5, implements 4, defines 4, causes 3, exemplifies 1.
- **Zero `contradicts` links.** The "relative" in "relative
  connections" is half-untested in this data.

## Metric definitions (fixed before computing — all reported)

| ID | definition |
|---|---|
| M1 | total degree (in + out, all rels) |
| M2 | in-degree (all rels) |
| M3 | support-minus-contradict = incoming `supports/implements/exemplifies/refines` − incoming `contradicts` (reduces to in-support: no contradicts in data) |
| M4 | independence-weighted in-support = Σ 1/out_degree(source) over incoming support links (down-weights promiscuous linkers) |
| M5 | relative share = node total degree / chunk total links (the user's "relative connections" phrasing) |

## Results 1: connectivity vs human grades (n=115 mapped)

Grade skew (stated loudly): 93× 1.0, 21× 0.5, 1× 0.0. The
effective sample for the key comparison is **22 sub-1.0**.

| metric | Spearman | perm. p (10k) | mean\|grade=1.0 (n=93) | mean\|grade<1.0 (n=22) |
|---|---|---|---|---|
| M1 total degree | +0.171 | 0.0666 | 0.855 | 0.606 |
| M2 in-degree | +0.095 | 0.3177 | 0.407 | 0.379 |
| M3 support−contradict | +0.155 | 0.1021 | 0.283 | 0.106 |
| M4 indep-weighted | +0.154 | 0.1045 | 0.276 | 0.106 |
| M5 relative share | +0.100 | 0.2893 | 0.185 | 0.166 |

Sensitivity (max instead of mean): M1_max +0.194, p=0.0309 —
the only p<0.05 among 10 tested variants; does **not** survive
multiple-comparison correction (Bonferroni 0.005). Reported, not
claimed.

**Reading:** direction consistently positive across all metrics
and both aggregations (15/15 positive), but no metric clears a
significance bar once multiplicity is accounted for. **Suggestive,
not established** (computationally verified as a measurement;
conjectural as a signal).

## Results 2: the calibration question (the proposal's real test)

Within QUEUE/SURFACE-actioned probes (conjectural→QUEUE per the
collapse spec), does connectivity separate human-1.0 (wrongly
queued — judge under-confidence) from human-0.5 (correctly
queued)? n=32 mapped (16 + 16).

| metric | correctly-queued mean (n=16) | wrongly-queued mean (n=16) | Mann-Whitney p |
|---|---|---|---|
| M1 | 0.458 | 0.792 | 0.1051 |
| M2 | 0.208 | 0.406 | 0.2351 |
| M3 | 0.021 | 0.344 | **0.0523** |
| M4 | 0.021 | 0.344 | **0.0523** |
| M5 | 0.122 | 0.162 | 0.2503 |

**This is the right shape for the proposal:** the wrongly-queued
probes (humans said full fidelity; judge said conjectural) map to
*more*-connected records. Connectivity agrees with the humans
over the under-confident judge — which is exactly the mechanism
the proposal needs (high support → promote toward ACT).
But: n=16+16, p≈0.05 marginal, chunk and judge entangled (each
chunk judged once — c10/c12's under-confident judge coincides
with above-median chunk density; inseparable in this data).

## Results 3: connectivity vs judge labels (secondary)

Modal Arm-B label per probe (each probe judged once — "modal" is
trivial, stated not hidden): exact (n=42): mean M1 1.09;
computationally_verified (n=41): 0.66; conjectural (n=30): 0.57;
heuristic (n=2): 1.50. Judges' `exact` labels land on the most
connected records — consistent with Results 1, same confounds.

## Verdict: does the signal exist?

**Not established. Suggestive, insufficient — the gate does not
open the design charter.** Triadically:

- **Claim (signal warrants charter): WEAK SUPPORT, not met.**
  Consistent positive direction, marginal p-values, the
  QUEUE-tier pattern has exactly the needed shape — but nothing
  survives multiplicity, n is small, and confounds are
  inseparable.
- **Polar opposite (no signal): NOT eliminated.** The
  permutation nulls do not exclude it; the data are compatible
  with no signal.
- **Null (permutation): not rejected** at any defensible
  threshold.

**Best metric if signal is pursued: M1 (total degree)**, with M3
(support-based) the most proposal-relevant (M3 carried the
QUEUE-tier pattern at p≈0.05). M5 (relative share) is weakest —
the user's "relative" phrasing does not outperform raw degree in
this data. M4 ≈ M3 here (out-degrees too small to diverge);
they would separate on a denser graph.

## Honest negatives (owned same-exchange)

1. **Mapping is approximate.** Content overlap, not identity;
   5/120 unmapped; multi-maps averaged. A different mapping
   could move the numbers.
2. **Grade skew is severe.** 93/115 mapped probes are 1.0; the
   key comparisons rest on n=22 (primary) and n=16+16
   (QUEUE-tier). Small-n fragility throughout.
3. **Retrospective, not prospective.** The links were made by the
   same pipeline family being evaluated — correlation is not
   calibration, and this analysis cannot authorize deployment.
4. **Multiple comparisons.** 10 primary variants + 5 QUEUE-tier;
   the single p<0.05 does not survive correction. All variants
   reported (no p-hacking by omission).
5. **Zero contradicts.** M3's contradict leg and the "relative"
   (support-vs-contradict) framing are untested — half the
   proposal's vocabulary has no data.
6. **Graph too sparse to be the instrument.** 48% of records
   isolated; 0.32 links/record. The proposal needs a link
   discipline an order of magnitude denser before connectivity
   can calibrate anything.
7. **Chunk/judge entanglement.** Each chunk judged once; the
   under-confident judge (c10–c12) coincides with denser chunks.
   Inseparable in this data.
8. **Goodhart risk unmeasured** (pre-registered in MESH-5): once
   the extractor knows connectivity upgrades verdicts, the
   incentive is to over-link. Nothing here tests that.

## What a design charter would need (the gate's chain)

The retrospective scopes the real test; it does not substitute
for it. A charter is warranted only after:

1. **A denser link discipline** — extraction rules that produce
   ~3+ links/record with typed rels used as designed (including
   `contradicts`), so the instrument isn't blunt.
2. **Pre-registered metric: M1 or M3** (not M5) — the
   retrospective's best carriers, fixed before the prospective
   run.
3. **Prospective test** — the calibration rule (e.g. "conjectural
   + in_support ≥ k → promote toward ACT") tested on *new*
   extractions against human grades, chunk-stratified, with the
   judge held fixed.
4. **The Goodhart guard** — a held-out link-audit: does the
   signal survive when the extractor is blind to the
   calibration rule?
5. **Independence hardened** — M4's weighting scheme (or better)
   specified before measurement, since M3/M4 diverge only on
   dense graphs.

**Why it ends here:** the gate question is answered —
signal not established; pattern suggestive; the path to a
decision is specified. **Its own chain:** the five charter
prerequisites above; MESH-5 stays OPEN pending a prospective
pilot, not a design charter.

---

*Labels: the measurements are **computationally verified**;
"signal exists" is **conjectural** (lean-positive, unproved);
the charter prerequisites are **heuristic** (design judgment).
No claim here authorizes deployment.*
