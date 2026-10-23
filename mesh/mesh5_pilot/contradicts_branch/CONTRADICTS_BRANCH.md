# Contradicts-vector diagnostic branch — REPORT

**Date:** 2026-10-09. **Parent:** MESH-5 pilot NO-GO at K1 (mesh5_pilot/RUN_LOG.md).
**Trigger:** the router's methodological move — when a gate kills on a specific
missing piece, fork a diagnostic run on exactly that vector instead of only
logging the dead end.
**Work dir:** mesh/mesh5_pilot/contradicts_branch/. Atlas records read-only.

## 0. Context

The MESH-5 pilot died at the K1 shakedown gate: link discipline reached mean
degree 4.2–4.9 but contradicts only 2.4% (Atlas-9 report, strict brief) and
4.1% (a3_test report, v2 brief with scope-narrowing) — both below the 5% bar,
with the v2 hits honest-downgraded to ~0–2% on a strict reading. The question
this branch answers: is the contradicts scarcity MATERIAL, EXTRACTOR
BLINDNESS, or DEFINITIONAL NOISE?

## 1. PRE-REGISTERED TRIADIC FORK (recorded BEFORE any extraction)

- **Claim (material scarcity):** the program's reports — written in a
  consistent, self-correcting voice — genuinely lack negations. The
  contradicts rate holds ~2–4% across extractor variants and corpora of
  this kind. The "relative" (support-vs-contradict) vocabulary is
  untestable on this material; the dead end is earned, not assumed.
- **Polar opposite (extractor blindness):** a better operationalization
  recovers genuine contradicts density ≥5% on some (extractor, corpus)
  cell, with >80% of the hits adjudicated-genuine under the strict
  definition. The pilot unblocks with exactly that discipline.
- **Null (definitional noise):** broader definitions only manufacture
  borderline hits (like the v2 shakedown's 4.1%, honest-downgraded to
  ~0–2%). Nothing clears 5% genuinely; the rate differences across
  variants are inflation, not signal.

## 2. PRE-REGISTERED VERDICT RULE

Any (extractor-variant, corpus) cell with contradicts ≥ 5% of all links
AND >80% adjudicated-genuine (probe 3, strict definition) →
**POLAR OPPOSITE HOLDS**: the pilot unblocks with that exact discipline
(named below). Otherwise → **CLAIM HOLDS**: dead end earned — record as
a verdict with the fallback inventory ((a) redesign around M1, (b)
M3-as-in-support, (c) record the dead end) for the router's word.

Adjudication standard (strict): a contradicts link is GENUINE iff record
A asserts the negation of a claim record B asserts. Borderline =
manufactured (a miss, not a hit). The v2 shakedown's honest downgrades
are the standard.

## 3. Probe design

**Probe 1 — same corpus, three extractor variants** (corpus:
corpus_runs/atlas6/a3_test/REPORT.md; 20 records each; ≥3 typed
links/record; extractors blind to the hypothesis):
- (a) STRICT: mesh5_pilot/EXTRACTOR_BRIEF.md (v1) as-is — contradicts =
  asserts-negation only, no scope-narrowing, no limitation records.
- (b) V2: mesh5_pilot/EXTRACTOR_BRIEF_V2.md as-is (scope-narrowing
  principle + limitation records). Partial replication of the pilot's
  v2 shakedown (4.1%) with a fresh extractor.
- (c) LIMITATION-AS-CONTRADICTS: contradicts_branch/CELL_c_BRIEF.md —
  v2 plus the explicit instruction that downgrades, limitations, open
  items, and "not yet met" verdicts COUNT as contradicts against the
  corresponding positive/unqualified claim. Designed to inflate; the
  adjudicator measures how much is genuine.

**Probe 2 — same extractor (variant b = v2 brief), three corpora**
(20 records each):
- (a) a3_test/REPORT.md — reuses probe-1b output (no re-extraction).
- (b) corpus_runs/atlas5/ATLAS5_REPORT.md — adversarial literatures.
  Note: 11 atlas runs found 0 contradictions; this tests whether that
  is extraction or material.
- (c) step4/STEP4_REPORT.md — genuinely adversarial pick: three
  experimental arms with different outcomes plus an appended correction
  note contradicting the original prose. If any corpus clears 5%,
  this is the best candidate.

**Probe 3 — independent adjudication:** a FRESH subagent (none of the
extractors) grades EVERY proposed contradicts link from all cells
against the strict definition, given both records' claims + spans +
the link reason. Reports per cell: proposed count, genuine count,
TRUE rate, MANUFACTURED rate.

## 4. Results

### 4.1 Rate table (raw extraction)

| cell | extractor | corpus | records | links | mean deg | contradicts | share |
|---|---|---|---|---|---|---|---|
| 1a | strict (v1) | a3_test | 20 | 36 | 3.6 | 0 | 0.0% |
| 1b | v2 | a3_test | 20 | 53 | 5.3 | 3 | 5.7% |
| 1c | limitation | a3_test | 20 | 60 | 3.0 | 4 | 6.7% |
| 2b | v2 | atlas5 | 20 | 39 | 3.9 | 0 | 0.0% |
| 2c | v2 | step4 | 20 | 49 | 4.9 | 2 | 4.1% |

### 4.2 Adjudication (strict definition)

| cell | proposed | genuine | TRUE rate | MANUFACTURED rate | genuine share of all links |
|---|---|---|---|---|---|
| 1a | 0 | 0 | — (none proposed) | — | 0.0% |
| 1b | 3 | 0 | 0% | 100% | 0.0% |
| 1c | 4 | 0 | 0% | 100% | 0.0% |
| 2b | 0 | 0 | — (none proposed) | — | 0.0% |
| 2c | 2 | 2 | 100% | 0% | 4.1% |

Adjudication pattern: all 7 borderline links (1b ×3, 1c ×4) shared one
failure mode — a downgrade/limitation/open-item claim affirming the
target's ACTUAL stated scope while denying a broader reading the target
never asserted. The 2 genuine links (both in 2c) were numerical-correction
pairs asserting mutually exclusive factual values (label distribution
32/39/43/6 vs 42/44/32/2; "6 of 16" vs "9 of 16" judge counts).

## 5. Verdict

**CLAIM HOLDS — dead end earned, not assumed** (2026-10-09).

No (extractor, corpus) cell satisfies both pre-registered bars
(≥5% contradicts AND >80% adjudicated-genuine):

- 1a (strict × a3_test): 0.0% raw — fails the 5% bar.
- 1b (v2 × a3_test): 5.7% raw, 0% genuine — fails the genuine bar.
- 1c (limitation × a3_test): 6.7% raw, 0% genuine — fails the genuine bar.
- 2b (v2 × atlas-5): 0.0% raw — fails the 5% bar.
- 2c (v2 × step-4): 4.1% raw (below bar), 100% genuine — fails the 5% bar.

Findings:

1. **The rate moves with the brief, not the material.** On the same
   corpus (a3_test): 0.0% → 5.7% → 6.7% across strict → v2 →
   limitation-as-contradicts. Adjudication collapses every a3_test
   cell to 0% genuine. The movement was pure definitional inflation —
   the NULL leg, confirmed on this corpus.
2. **The strict definition is not vacuous.** Cell 2c produced 2
   genuine contradicts (mutually exclusive factual values) at 100%
   true rate — but 4.1% share, below the bar. Genuine negation exists;
   the density does not.
3. **One failure mode, seven times.** Every borderline link denied a
   broader reading its target never asserted. This validates the v2
   shakedown's honest downgrades and the standing convention: under
   uncertainty, default to the weaker claim (refines), never upgrade
   to contradicts.
4. **Atlas-5 at 0% under v2** is consistent with the program's thesis
   (disjointness, not disagreement): no engagement, no negation.

**Chain:** the MESH-5 pilot does not unblock — no discipline clears
both bars. Fallback inventory for the router's word: (a) redesign the
pilot around M1 (no contradicts needed — but M1 does not implement the
QUEUE-tier relative mechanism); (b) run M3 as pure in-support, as the
retrospective did (changes the pre-registered metric); (c) record the
dead end: the "relative" (support-vs-contradict) vocabulary is
untestable on this material — now an EARNED verdict, not a guess.

## Epistemic labels

| Claim | Status |
|---|---|
| Fork + verdict rule pre-registered before extraction | design record (this file, §1–§2, timestamped) |
| Extraction counts per cell (5 cells, 100 records, 237 links) | computationally verified |
| Adjudication true/manufactured rates (9 links, fresh adjudicator) | computationally verified |
| Rate moves with brief (0.0→5.7→6.7%), collapses to 0% genuine | computationally verified |
| Strict definition satisfiable (2c: 2 genuine at 100%) | computationally verified |
| CLAIM HOLDS — material scarcity, dead end earned | verdict (per pre-registered rule) |
