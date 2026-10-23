# Decision-Model Mesh — Decision Tree

**Project:** meshing the codec/methodology with decision-model
infrastructure (PolicyLM-1.7B et al.). Derivation here, application
there.
**Method:** `~/workspace/prime-sieve-geometry/METHODOLOGY.md`.
**Nodes:** namespaced MESH-N. Started 2026-10-08.

---

## MESH-0. The mesh plan — 2026-10-08
**Q:** What must exist for the project to mesh with the
decision-model field, and in what order?
**Decision:** five steps — (1) verdict packet spec, (2) collapse
spec, (3) benchmark the application half, (4) labeled-vs-binary
demonstration, (5) paper (user's timing). Ledger-as-provenance
deferred until a consumer exists (no speculative infrastructure).
**Evidence:** the plan as laid out and authorized ("let's
proceed").
**Status:** executed — steps 1–4 complete; step 5 open.
**Labels:** the plan is **heuristic** (strategy); the mesh point
(derive here / apply there) is **conjectural** (precise, unproved
until step 4).
**Why it ends here:** the plan was authorized and run to step 4.
**Its own chain:** MESH-1 through MESH-5 below; step 5 (paper)
remains the user's call.

---

## MESH-1. Verdict packet spec — 2026-10-08
**Q:** What crosses the derivation/application boundary?
**Decision:** the verdict packet v1.1 — claim + epistemic label +
verbatim span + one-line honest boundary + record pointer +
checksum. A header, not the carriage; ≤200 token budget.
**Evidence:** VERDICT_PACKET_SPEC.md. Budget was pre-registered at
≤120; the benchmark measured 73% of faithful packets over budget
(structural: ~66 tokens fixed overhead) → revised to 200
explicitly, reason recorded (ledger rule: no silent changes).
**Status:** closed (spec stands; survived step 4's backward touch).
**Labels:** the spec is **conjectural** (precise, unproved until
deployed); the budget revision is **computationally verified**.
**Triadic:** packet+labels (claim) / silent binary collapse, the
field's status quo (polar opposite) / no boundary format at all
(null).
**Backward touch:** step 4 (MESH-4) — spec survives as decision
instrument.
**Why it ends here:** spec written, measured, revised, standing.
**Its own chain:** the packet is what step 4's Arm B emits; any
future deployment's audit unit.

---

## MESH-2. Collapse spec — 2026-10-08
**Q:** What does the application layer do when a packet arrives?
**Decision:** COLLAPSE_SPEC.md v1 — pre-registered label→action
tiers: exact ACT; computationally_verified ACT with spot-check;
conjectural QUEUE; heuristic SURFACE; killed BLOCK; superseded
FOLLOW the heir; unstated NO ACTION. Caution permitted
downstream, confidence never. Every collapsed action logs its
packet.
**Evidence:** the spec file; pre-registered before any deployment.
**Status:** closed as framework; QUALIFIED by MESH-4 — survives
with a calibration note (v1.1 candidate): deployments must
measure judge calibration on a graded sample before treating
QUEUE volume as pure signal.
**Labels:** the tier mapping is **conjectural**; the
labels-only-weaken rule is **derived** (D20).
**Backward touch:** MESH-4 — the qualification comes from the
demonstration, not from armchair revision.
**Why it ends here:** spec written and pre-registered; its first
empirical qualification recorded.
**Its own chain:** the tiers are what step 4's Arm B collapses
through; the calibration note is MESH-5's starting problem.

---

## MESH-3. Application-half benchmark — 2026-10-08
**Q:** What does the packet machinery cost, in the field's units?
**Decision:** measured live (tiktoken cl100k_base; 5 warm-up + 30
timed reps/chunk).
**Evidence:** BENCHMARK_REPORT.md. Per-verdict: v7 0.041ms /
51 tokens; D-wire 0.020ms / 167 tokens; packet build+verify+lookup
0.025ms / 149 tokens. End-to-end ≈0.045ms, ≈149 tokens.
**Verdict:** TIME IS NOT THE CONSTRAINT — 10–1700× under the
50ms decision-model bar; the machinery adds ~0.03ms/verdict.
TOKENS BIND. Honest frame: mechanical decode + lookup, no model
inference measured — the claim is "provenance is nearly free in
time," not "we beat PolicyLM."
**Status:** closed.
**Labels:** **computationally verified** (with the stated frame).
**Why it ends here:** numbers measured, reported, folded into the
spec (MESH-1 budget) and the step-4 pricing.
**Its own chain:** the cost story step 4 prices its gains against.

---

## MESH-4. Labeled-vs-binary demonstration — 2026-10-08
**Q:** Do labeled verdicts produce better decisions than binary
judgments, or do labels add cost without decision value?
**Decision:** ran pre-registered (STEP4_DEMONSTRATION_CHARTER.md):
120 human-graded parity probes; Arm A binary (PolicyLM mirror);
Arm B labeled (blind packets + mechanical collapse); Arm C null
(shuffled labels). Same judge throughout.
**Evidence:** step4/STEP4_REPORT.md; step4_results.json; judge
outputs; analysis script.
**Verdict:** ALL THREE LEGS FAIL AS STATED — and the experiment
discriminated anyway. A: 17 false auto-acts / 0 missed. B: 7
false / 16 "missed" (ALL conjectural→QUEUE — judge
under-confidence; calibration variance 16/30 vs 2/30 across
judges [corrected 2026-10-08: said 17/30; raw data 16]) / 26.7% review load. C: 17 false / 26 missed. Null
FAILS decisively (labels carry real information); polar opposite
FAILS (arms decisively different); claim FAILS as stated
(miss-rate condition not met). Actual finding: a
precision/recall trade-off the charter didn't name — B buys −10
false auto-acts for +16 queued full-fidelity probes; the "misses"
are delayed-to-review, not lost (post-hoc, marked as
interpretation: under perfect review, effective errors 7 vs 17).
Token price: ~165 tokens/decision marginal (~80× binary).
**Status:** closed. Load-bearing follow-up: judge calibration.
**Labels:** the error tables **computationally verified**; the
under-review interpretation **heuristic** (marked post-hoc).
**Deviations (recorded):** mid-run materials error caught by the
method itself (wrong file → re-judged fresh, blind intact); the ≈
tolerance fixed at analysis time pre-results, recorded not
smuggled.
**Backward touch:** MESH-1 (packet spec survives); MESH-2
(collapse spec survives + calibration note); MESH-3 (token ratio
folded in).
**Why it ends here:** the demonstration ran to verdict; its
follow-up is a new node, not a continuation.
**Its own chain:** MESH-5 — the QUEUE tier's cost is what the
user's connectivity proposal answers.

---

## MESH-4a. Judge calibration study — 2026-10-08 (parallel account, Order 1)
**Q:** the load-bearing follow-up from MESH-4 — can judge
miscalibration be measured and corrected, and what procedure
does the collapse spec v1.1 need?
**Decision:** ran on the main account's step-4 data via a parallel
account (Order 1); verified on the main account against raw outputs.
**Evidence:** per-judge calibration tables from step4_results.json +
judge_outputs/j1..j4.
**Verdict:** calibration is per-judge × per-label, not one caution
dial. j3 over-confident on cv (4 of the 7 false acts,
P(1.0|cv)=0.73) but well-calibrated on conjectural; j4 perfect on cv
but under-confident on conjectural (9 of its 16 conjecturals were
human-1.0). No per-judge conjectural→ACT remap is a clean win
(~1:1 trade of caught queues for new false acts; the spec forbids
it anyway). Chunk/judge confound is total (chunks nested in
judges); c12 (all ten probes human-1.0, 50% conjectural rate)
favors a judge effect. Proposed v1.1 procedure: 360-probe graded
samples (97 emissions per decision-relevant label), Wilson-CI
acceptance bands on lower bounds, re-briefing (never remapping) on
failure, two-strikes retirement, drift spot-checks.
**Status:** ADOPTED 2026-10-09 (router's wheel) — COLLAPSE_SPEC.md v1.1
promotes the calibration note to the adopted judge-calibration procedure
(360-probe samples, Wilson-CI bands, re-briefing never remapping,
two-strikes retirement, drift spot-checks). Tiers unchanged; no verdict
changes; procedure governs future judge calibration only. Labels: the
tables **computationally verified**; the procedure **heuristic**
(design judgment, adopted).
**Backward touch:** MESH-4 — the same study caught transcription
errors in STEP4_REPORT.md's prose (label distribution 32/39/43/6 →
42/44/32/2; "6 of 16" → "9 of 16"; "17/30" → "16/30"); correction
note appended to the report 2026-10-08, verdict and error tables
re-verified unchanged. MESH-2 — the calibration note now has a
concrete candidate procedure awaiting adoption.
**Labels:** the tables **computationally verified**; the v1.1
procedure **heuristic** (design judgment, unadopted).

---

## MESH-5. Connectivity-based auto-calibration — PILOT RELAUNCHED, FALLBACK (b) (2026-10-09)

**Status:** Run 2 NO-GO — two gates fired (2026-10-09). K1 PASSED (22
records, mean degree 3.73, contradicts an honest 0/41). Phase B: 120
records, 255 links, j4 rendered 120 judgments but only 5 conjecturals
(4.2%) — K4 FAILED (<48; the step-4 53% conjectural rate didn't transfer:
fidelity judgments vs settled record claims). K3 FAILED independently:
held-out audit 35/140 links fail = 25% > 15% (told arm 38.2% vs blind
12.5% — the Goodhart signature: rule-knowledge corrupted link quality,
duplicates + fabricated bases, not quantity). Claim UNTESTED, not
refuted; no grading was requested. MESH-5 stays OPEN. Re-scope needs
charter amendment + router word: (a) corpus/probe design yielding
conjecturals at rate, (b) link discipline hardened against the told-arm
defect pattern. Full log: mesh/mesh5_pilot/fallback_b/RUN_LOG.md. §9
NO-GO stands as run 1.
**Q (user's):** instead of human review for the QUEUE tier (too
slow, too costly), can judgments be made automatically — likely
from relative connections per node?
**Proposal:** the QUEUE tier auto-resolves from the record graph's
own structure: a verdict node's relative connections (supporting
vs contradicting links, independence-weighted) calibrate it —
high independent support promotes toward ACT; contradiction or
isolation holds at QUEUE or demotes toward SURFACE. Calibration
from the graph, not from a human: derive, don't invent, applied
to the calibration problem.
**Standing caveats (pre-registered before analysis):** the
measure must be defined before it is measured (which relation
types count; how independence is weighted); Goodhart risk (once
the extractor knows connectivity upgrades verdicts, the
incentive is to over-link) belongs in the design.
**First move:** retrospective — does D-wire record connectivity
predict the 120 human fidelity grades? The data already exists
(Step 4 grades + the link graph); no new experiment before this
question is answered.
**Status:** PILOT NO-GO AT K1 (2026-10-09 — router GO on the draft charter).
Phase A failed the link-discipline shakedown twice: attempt 1 (Atlas-9
report): mean degree 4.2 ✓, contradicts 2.4% ✗; attempt 2 (revised brief
v2, a3_test report): mean degree 4.9 ✓, contradicts 4.1% ✗ (both
borderline; true rate ~0–2% on a strict reading). Per charter §6: STOP,
Phase B never started, no human grading requested. Finding: the 5%
contradicts bar assumed a dialectic density the program's reports don't
carry (genuine negations run ~2–4%); forcing it would manufacture false
contradicts and poison M3*. MESH-5 stays OPEN. Fallback inventory (needs
charter amendment + router word): (a) redesign around M1; (b) M3-as-
in-support as the retrospective did; (c) record the dead end. Full log:
mesh/mesh5_pilot/RUN_LOG.md.
**Branch 2026-10-09 (router's move):** contradicts-vector diagnostic
(mesh/mesh5_pilot/contradicts_branch/CONTRADICTS_BRANCH.md) — when the
K1 gate killed on the missing contradicts, forked a triadic run on that
exact vector. 5 cells (100 records, 237 links): raw contradicts rate
moves with the brief (0.0% strict → 5.7% v2 → 6.7% limitation-variant
on a3_test; 0% on atlas-5; 4.1% on step-4), but fresh adjudication
against the strict definition collapses every a3_test cell to 0%
genuine; only cell (v2 × step-4) yields genuine hits (2/2, numerical
corrections) — 4.1% share, below the bar. No cell clears both bars
(≥5% + >80% genuine). **Verdict: CLAIM HOLDS — material scarcity; the
dead end is EARNED.** The pilot does not unblock. Fallback inventory
stands for the router's word.
**Retrospective verdict:** signal SUGGESTIVE but not established.
115/120 probes mapped (95.8%; one mapping bug caught and fixed
pre-analysis). All five metrics correlate positively with human
grades (Spearman +0.10–+0.19) but none clears significance after
correction (perm p 0.07–0.61). Best: M1 total degree (+0.171,
p=0.067). Most proposal-relevant: M3 support-minus-contradict —
among 32 queued probes, the 16 wrongly-queued (human 1.0, judge
conjectural) map to MORE-connected records than the 16
correctly-queued (0.34 vs 0.02, p≈0.05) — connectivity sides with
the humans over the under-confident judge, exactly the mechanism
proposed. But: n small, grade skew (93/115 at 1.0), graph too
sparse (48% isolated, 0.32 links/record), ZERO contradicts links
(half the "relative" vocabulary untested). Triadic: claim weak
support (not met); polar opposite not eliminated; null not
rejected. M5 (relative share — the user's "relative" phrasing)
weakest (+0.10): raw degree beats normalization in this data.
**Recommendation:** not a design charter — a PROSPECTIVE PILOT,
scoped by five pre-registered prerequisites (denser link
discipline; pre-registered M1/M3; prospective test on new
extractions; Goodhart guard; hardened independence weighting).
**Labels:** the correlations **computationally verified**; "signal
exists" **conjectural** (lean-positive); the pilot prerequisites
**heuristic**.
**Why it stays open:** the QUEUE-tier pattern is the live thread —
the pilot, not the charter, is the next warranted move.
**Its own chain:** prospective pilot when link discipline exists
to support it; until then the human-review cost problem stands as
MESH-4 stated it. **Update 2026-10-09:** the Order-2 draft charter that
never returned from the parallel account has been drafted on the main
account: mesh/MESH5_PILOT_CHARTER.md (draft only). M3* primary (M3 with
M4 independence weighting, exact formula pre-registered), M1 secondary;
fixed judge j4; 8×15 chunk-stratified; kill criteria K1–K5; GO authorizes
a design charter draft only. Awaiting the router's go/no-go.
**Update 2026-10-09 (pilot LAUNCHED on router GO → NO-GO at K1):**
the link-discipline shakedown failed twice — attempt 1 (Atlas-9,
brief v1): degree 4.2 ✓, contradicts 2.4% ✗; attempt 2 (a3_test
report, brief v2): degree 4.9 ✓, contradicts 4.1% ✗ (both borderline,
against unasserted broad readings). Per charter §6: STOP, do not
proceed to Phase B. NO-GO on discipline: the 5% bar assumed a
dialectic density the reports don't carry; forcing it would poison
M3*. MESH-5 stays OPEN; fallback inventory in
mesh/mesh5_pilot/RUN_LOG.md (M1-redesign, M3-as-in-support, or record
the dead end — all need charter amendment + router word).
**Labels:** the proposal is **conjectural** (precise, untested).
**Why it is open:** the retrospective is the gate — signal or no
signal decides whether a design charter is warranted.
**Its own chain:** if signal → design charter for the
connectivity-calibrated QUEUE tier (with the Goodhart guard);
if no signal → ledger entry (graph shape doesn't carry that
signal) and the human-review cost problem stands.
**Update 2026-10-09 (contradicts-vector diagnostic branch — CLOSED):**
the K1 gate failure became a decision node, not a dead end (the
router's correction: this is reiteration of the method, not a new
move). Triadic fork, pre-registered before extraction: claim = the
contradicts scarcity is MATERIAL (program reports genuinely lack
negations); polar opposite = EXTRACTOR BLINDNESS (some discipline
recovers ≥5% contradicts with >80% adjudicated-genuine, pilot
unblocks with it); null = DEFINITIONAL NOISE (broader briefs only
manufacture borderline hits). Verdict rule: any cell clears ≥5% AND
>80% genuine → unblock; else the dead end is EARNED. Five cells, 100
records, 237 links (report:
mesh/mesh5_pilot/contradicts_branch/CONTRADICTS_BRANCH.md): raw
contradicts moved with the BRIEF on the same corpus (0.0% strict →
5.7% v2 → 6.7% limitation-as-contradicts), but independent
adjudication (fresh subagent, strict definition: asserts-negation
only) collapsed every a3_test cell to 0% genuine — pure definitional
inflation (null leg confirmed on this corpus). The strict definition
is not vacuous: 2 genuine hits in the step-4 cell (mutually exclusive
numerical corrections), 4.1% < 5% bar. All 7 borderline links shared
one failure mode: denying a broader reading the target never
asserted — validating the router's standing rule (2026-10-09):
avoid inserting anything when unsure, at any level; uncertainty
defaults to the weaker claim. No cell cleared both bars →
**CLAIM HOLDS: dead end earned.** MESH-5 does not unblock; the
fallback inventory ((a) redesign around M1, (b) M3-as-in-support,
(c) record the dead end) now rests on a verdict, not a guess —
charter amendment + router word still required.
**Labels:** fork + verdict rule pre-registered (design record);
extraction counts and adjudication rates **computationally
verified**; the verdict follows the pre-registered rule.
**Why it is closed:** every leg adjudicated; the scarcity is
material. **Backward touch:** reframes the K1 NO-GO — the 5% bar did
not assume wrong about the material, the material itself lacks the
dialectic density; sharpens the no-insertion standing rule from
convention to independently validated principle.
