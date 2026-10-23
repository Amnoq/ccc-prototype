# Step 4 Demonstration Charter — labeled vs binary judgments

**Date:** 2026-10-08. **Status:** AUTHORIZED (user's "proceed with
step four") — pre-registered before execution; this document is the
plan, not the result.
**Companions:** VERDICT_PACKET_SPEC.md v1.1, COLLAPSE_SPEC.md v1,
BENCHMARK_REPORT.md.

## Question

Do labeled verdicts (packet + collapse tiers) produce better
decisions than binary judgments on a real judgment task — or do
the labels add cost without decision value?

## Prediction (stated before computing)

The claim is expected to hold, but the test is honest: labeled
collapse should reduce false auto-acts, because partial-fidelity
extractions get queued for review instead of acted on. The live
alternative: if the judge's labels are noisy, Arm B just buys
review load with tokens. The value is the measurement, not the
hoped outcome.

## Task & corpus

For each of the 120 human-graded parity probes
(`corpus_runs/r5/rescore_v7/`, 12 chunks + controls; scores
0/0.5/1 with miss classes): given the extraction + source chunk,
judge fidelity and decide whether to ACT on the extraction
(deploy as faithful).

Ground-truth mapping (pre-registered):
- human 1.0 → ACT is correct; anything less is a missed act.
- human 0.0 → any ACT is a false auto-act.
- human 0.5 → QUEUE/surface is correct; auto-ACT is a false
  auto-act (partial fidelity must not gate action).

## Arms (same judge model throughout — isolates the label effect)

- **Arm A (binary — the PolicyLM mirror):** judge outputs
  faithful/unfaithful. Binary → act/don't-act directly. No
  labels, no tiers, no provenance.
- **Arm B (labeled):** judge outputs a verdict packet per
  VERDICT_PACKET_SPEC.md (claim + label + span + boundary,
  blind — the judge never sees human grades); collapse per
  COLLAPSE_SPEC.md tiers mechanically.
- **Arm C (null):** identical to B, but labels shuffled before
  collapse. Tests whether the labels carry information vs. the
  packet structure itself.

## Metrics (pre-registered)

- **False auto-acts:** acted where ground truth forbids
  (human 0.0, or 0.5 acted rather than queued).
- **Missed acts:** failed to act where human = 1.0.
- **Review load:** fraction queued (the cost of caution).
- **Token cost per decision** (benchmarked: B ≈ 150 tokens;
  measure A live).

## Decision rule (pre-registered)

- Labels earn their keep iff B has strictly fewer false
  auto-acts than A at no worse missed-act rate — or equal
  errors at lower review load.
- B ≈ A on errors → **polar opposite holds**: labels add cost
  without decision value. Record it; the specs do not survive
  as a decision instrument (they may survive as provenance).
- C ≈ B → **null holds**: the labels carry no information;
  structure without content. The judge's labels are noise.

## Triadic fork

1. **Claim:** labeled collapse beats binary — fewer false
   auto-acts, priced in tokens and review load.
2. **Polar opposite:** binary matches or beats labeled — the
   labels cost without deciding.
3. **Null:** shuffled labels match true labels — the labels
   carry no information.

## Controls & honest negatives (own same-exchange)

- Same judge, same probes, blind grades — the only difference
  between arms is the label machinery.
- Judge quality bounds everything: a bad judge's labels are
  noise, and the experiment measures the judge+labels system,
  not labels in the abstract. State the judge used.
- The 0.5→queue mapping is a design choice, stated above —
  not discovered.
- Token cost: B costs multiples of A. The experiment prices
  the gain; a win on errors at 10× cost is a qualified win.
- No tuning per arm after seeing results. Pre-registered or
  it didn't happen.

## Backward touch (specified for whoever runs it)

- VERDICT_PACKET_SPEC.md / COLLAPSE_SPEC.md — do the specs
  survive as a decision instrument, as provenance only, or
  not at all?
- The mesh plan (step 4 of the decision-model mesh) — does
  the demonstration validate the mesh point (derive here,
  apply there)?
- BENCHMARK_REPORT.md — fold the measured A-vs-B token ratio
  into the cost story.

## Cost

One subagent run under METHODOLOGY.md. No user input mid-run.
On the user's word ("proceed with step four"), this charter is
the brief.

---

## Results (2026-10-08) — the charter is now the record

**Verdict: all three pre-registered legs FAIL; the experiment
discriminated anyway — a precision/recall trade-off the charter
did not name.**

Per-arm errors (n=120; computationally verified):
- Arm A (binary): 17 false auto-acts, 0 missed, 0 queued.
- Arm B (labeled): 7 false auto-acts, 16 missed (all QUEUE),
  32 queued (26.7% review load).
- Arm C (shuffled): 17 false auto-acts, 26 missed.

Adjudication:
- **Claim fails as stated:** 7 < 17 on false auto-acts, but
  16 > 0 on missed acts — the "no worse missed-act rate"
  condition is not met.
- **Polar opposite fails:** B ≉ A (|10| and |16| > 2) — the
  arms are decisively different.
- **Null fails:** C ≉ B (|10| > 2 both metrics) — shuffled
  labels are strictly worse; **the labels carry real
  information.**

Finding: the label machinery is informative and moves the
operating point (precision 84.8%→91.9%, recall 100%→83.2%),
but the pre-registered collapse (conjectural→QUEUE) with these
judges is miscalibrated — 16 QUEUE-on-1.0 are all `conjectural`
(judge under-confidence; one judge emitted 17/30 conjectural
vs another's 2/30). B correctly queued 10 of A's 17 false
auto-acts. Token price measured: ~165 tokens/decision marginal
(~80× the binary output); time unmeasured here, free per the
benchmark. Full report: `step4/STEP4_REPORT.md`; per-probe
detail: `step4/step4_results.json`.

**Backward touch (this charter's § specified):**
- VERDICT_PACKET_SPEC.md — SURVIVES (well-formed packets,
  informative labels, rules honored).
- COLLAPSE_SPEC.md — SURVIVES AS FRAMEWORK, QUALIFIED AS
  CALIBRATION (tiers coherent; mapping miscalibrated for
  these judges; needs a calibration note, not a rewrite).
- Mesh plan step 4 — does NOT validate the mesh point as a
  strict win; validates its premise (labels informative, not
  noise). "Derive here, apply there" survives with the caveat
  that the apply side needs calibrated judges.
- BENCHMARK_REPORT.md — A-vs-B token ratio (~80× marginal)
  folds into the cost story.

**Why it ends here:** the pre-registered decision rule is
adjudicated; all three legs failed informatively.
**Its own chain:** judge calibration is the next load-bearing
question — the machinery works, the judges need tuning.
