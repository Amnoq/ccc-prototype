# CCC Corpus Evaluation — SID-15 (Linear)

Date: 2026-10-03. Extractor revision: R2 density (`extractor_rev1.py`, `EXTRACTOR_PROMPT_R2` verbatim for all chunks).
Corpus: 12 chunks carved from real research notes (`corpus/c01`…`c12`), 2–4k tokens each.
Pipeline per chunk: probewriter (10 why/how probes + locked prose answers) → blind extractor → deterministic
verifier (`validate_extraction`, ≤2 repair attempts) → blind scorer (legend+injection only) → cost accounting.
Outputs: `corpus_runs/<chunk>/{probes.yaml, extraction.json, injection.txt, report.json}`.

## 1. Parity distribution (probe parity, /10 per chunk, n=120 probes)

| chunk | file | parity | omission ids |
|---|---|---|---|
| c01 | c01_completemap.txt | 3/10 | P1 P2 P3 P5 P8 P9 P10 |
| c02 | c02_deriv_d1_d5.txt | 6/10 | P4 P5 P9 P10 |
| c03 | c03_deriv_d6_d8.txt | 6/10 | P5 P6 P7 P8 |
| c04 | c04_deriv_d9_d10a12.txt | 8/10 | P2 P7 |
| c05 | c05_deriv_d10a3_d10c.txt | 6/10 | P3 P4 P8 P9 |
| c06 | c06_deriv_d10de_n14.txt | 7/10 | P3 P7 P8 |
| c07 | c07_dtree_nodes0_9.txt | 4/10 | P5 P6 P7 P8 P9 P10 |
| c08 | c08_dtree_node10.txt | 6/10 | P3 P6 P8 P9 |
| c09 | c09_dtree_node11.txt | 3/10 | P1 P2 P3 P4 P6 P7 P9 |
| c10 | c10_dtree_nodes12_13.txt | 3/10 | P1 P2 P3 P4 P5 P7 P10 |
| c11 | c11_dtree_d6gen_priorart_n14_11f.txt | 1/10 | P1 P3 P4 P5 P6 P7 P8 P9 P10 |
| c12 | c12_operator_audit.txt | 5/10 | P2 P4 P6 P8 P9 |

List: **[3, 6, 6, 8, 6, 7, 4, 6, 3, 3, 1, 5]** — mean **4.83/10**, range **1–8**.
Total omissions: 62/120. Total hallucinations: **0/120**.

## 2. Break-even distributions (sessions to recover extraction cost)

LAB convention = (prompt + chunk prose + output) / savings; DEPLOYMENT = (chunk + output) / savings.
Savings/session = prose tokens − injected tokens. cl100k_base throughout.

| chunk | prose | prompt | output | injected | savings | BE lab | BE deploy |
|---|---|---|---|---|---|---|---|
| c01 | 2597 | 819 | 1611 | 237 | 2360 | 2.13 | 1.78 |
| c02 | 2525 | 819 | 1724 | 267 | 2258 | 2.24 | 1.88 |
| c03 | 2667 | 819 | 1556 | 207 | 2460 | 2.05 | 1.72 |
| c04 | 2704 | 819 | 1780 | 245 | 2459 | 2.16 | 1.82 |
| c05 | 2921 | 819 | 1539 | 221 | 2700 | 1.96 | 1.65 |
| c06 | 2755 | 819 | 1578 | 201 | 2554 | 2.02 | 1.70 |
| c07 | 3005 | 819 | 1576 | 236 | 2769 | 1.95 | 1.65 |
| c08 | 2460 | 819 | 1588 | 248 | 2212 | 2.20 | 1.83 |
| c09 | 2017 | 819 | 1287 | 203 | 1814 | 2.27 | 1.82 |
| c10 | 2656 | 819 | 1566 | 193 | 2463 | 2.05 | 1.71 |
| c11 | 3295 | 819 | 1520 | 209 | 3086 | 1.83 | 1.56 |
| c12 | 3872 | 819 | 1473 | 224 | 3648 | 1.69 | 1.47 |

LAB list: **[2.13, 2.24, 2.05, 2.16, 1.96, 2.02, 1.95, 2.20, 2.27, 2.05, 1.83, 1.69]** —
mean **2.05**, range **1.69–2.27**.

DEPLOYMENT list: **[1.78, 1.88, 1.72, 1.82, 1.65, 1.70, 1.65, 1.83, 1.82, 1.71, 1.56, 1.47]** —
mean **1.72**, range **1.47–1.88**.

All 12 chunks break even well under the M4 ≤3 bar, under both conventions. Injected bodies run
~190–270 tokens against ~2–4k-token prose: savings/session ≈ 90% of prose.

## 3. Verifier pass rate and pipeline failures

- **Verifier: 12/12 chunks passed `validate_extraction` on the first attempt. Repairs used: 0.**
  No chunk required the repair pass; no chunk exhausted its 2-attempt budget.
- **Pipeline failures: none.** All 12 chunks completed all six stages; no chunk was dropped or partial.
- Anomalies (coordination-side, caught and fixed; see notes below):
  - c12's extractor emitted a non-schema `edges_note` key; stripped before save/validation.
  - c10: coordinator dropped the extractor's `c6→c1 refines` edge during manual transcription,
    caught it on review, restored it, re-validated (10 edges, still 0 repairs).

## 4. Omission-pattern notes (what kind of content gets dropped at R2 density)

The injection consistently preserves **relation-level verdicts** (which claims kill, support, refine,
or bound which; anchor statuses verified/asserted/open_question; verbatim open questions) and
**verdict-about-verdict reasoning**. Probes answerable at that grain reach parity. What does not
survive, in decreasing order of frequency across the 62 omissions:

1. **Numerical evidence.** Every requested number is gone: ψ(x) convergence tables (c04 P7),
   E-values at t=14.1347 (c03 P8), zero-recovery ε_N values (c11 P10), exact spectra (c09 P9),
   control data (c11 P8), recovery numbers (c11 P10), 13e test parameters (c10 P10).
2. **Mechanistic "why" content.** Proof mechanisms survive as relation skeletons but the mechanism
   itself drops: residue-quantization argument for the 14a obstruction (c06 P7), Selberg splitting
   argument (c05 P8), Weyl counting argument (c10 P1), Deninger foliation mechanics (c10 P2),
   Fock-diagonality as the Poisson rationale (c10 P7), trig-identity mechanics (c03 P5/P6),
   explicit-formula minus-sign explanation (c12 P2).
3. **Replacement-form concepts.** The surviving/refined form after a kill is dropped while the
   closure verdict survives: 14b/14c derivative refinements (c01 P8), Deninger's surviving form
   (c01 P9), the Li/Weil face-sum distinction (c01 P5).
4. **Concepts absent from the extraction itself.** Where the extractor never coined the concept,
   no probe about it can answer: D12, rank-one perturbation, prime-orbit/rational-prime type
   error, Jaksch fractal-error finding, Deninger labeling rule (c12 P4/P6/P8/P9).
5. **Cross-chunk bridges.** Content whose context lives in another chunk drops: the D8 energy
   dictionary (c05 P4), explicit-formula derivation detail (c02-adjacent).

Parity held where the legend label contained the "why" at headline grain (c10 P6 H₂ commuting
terms; c10 P8/P9 13d claim + caveats; c04 P1 the two-kill argument; c02 P2/P3 the identity and
bijection labels). **No probe in any chunk was answered wrongly from the structure —
0 hallucinations across 120 probes.**

## 5. Methodology caveats

- **Probe-difficulty variance is a real confound.** Parity is a joint product of (a) what the
  density-limited injection retains and (b) how mechanism/number-demanding each chunk's 10
  probes are. c11 (1/10) probes exact formulas and numeric recovery data; c04 (8/10) probes
  headline-grain verdicts. Same density revision, different ask. The mean (4.83) should be read
  as "parity under adversarial-detail probes of dense research notes," not as an intrinsic
  property of the injection format.
- **Corpus is real research notes, not transcript.** Chunks are carved from dense technical
  writing (decision trees, derivation ledgers, audit reports); prose-to-structure compression
  ratios here (~10:1) may not transfer to ordinary conversational transcript.
- **Scorers are LLM judges under strict blindness.** They never saw chunk prose (enforced by
  file access rules), answered only from legend+injection, and marked "UNANSWERABLE FROM
  STRUCTURE" honestly. But parity/omission line calls at the margin are judgment calls; the
  counts are computationally recorded, not theorem-certified.
- Epistemic status: distributions are computationally verified; the omission-pattern
  taxonomy is heuristic (synthesized from scorer notes); the M4 implications below are
  interpretive.

## 6. Implications for the M4 decision

- **Cost bar: met decisively.** All 12 chunks break even ≤2.27 lab / ≤1.88 deployment — under
  the ≤3 bar on every chunk, mean 2.05/1.72. The R2 density revision delivers cost headroom
  with margin.
- **Parity bar: the corpus distribution is well below the M3/M3R single-chunk numbers.**
  M3 reached 9/10 (held-out chunk 4, looser density), M3R 7/10 (gray-zone boundary, n=1).
  At R2 density across 12 chunks: mean 4.83, range 1–8, with mechanism/numbers systematically
  dropping. The trade-off isolated in M3R is now quantified: R2 density buys ~2-session
  break-even at the price of mechanistic justification — the failure mode is omission, not
  fabrication (0/120 hallucinations).
- **Verdict-quality survives; derivation-quality does not.** If the read path needs
  *which claims hold and how they relate* (verdicts, open questions, closure logic), R2
  injections carry it. If the read path needs *why they hold* (proofs, numbers, identities),
  R2 injections do not — and will not, by construction ("when in doubt, cut").
- **Pipeline reliability: high.** 12/12 first-pass validation, 0 repairs, 0 chunk failures,
  0 hallucinations. The machinery is sound; the limits are in the density, not the plumbing.

## 7. Per-chunk notes (from individual report.json)

- c01 (3/10): injection preserves verdicts but drops all numerical evidence, identities, and
  replacement-form concepts; verdict-about-verdict probes reach parity, mechanism probes omit.
- c02 (6/10): mathematical core well supported; omissions are her-side representations absent
  from extraction and downstream-consequence claims.
- c03 (6/10): D6/D7 verdicts survive; D8 energy-translation strand collapses on proof mechanism
  and numbers.
- c04 (8/10): argumentative skeletons (kill/support/refine/bound) and verbatim open questions
  preserved; omissions only where the probe explicitly demanded numbers/derivations.
- c05 (6/10): conclusions and verdict labels survive; proof mechanisms and cross-chunk bridges drop.
- c06 (7/10): formulas, verdicts, statuses retained; omissions are dropped mechanistic
  explanations (residue quantization, O(π(z)) payoff).
- c07 (4/10): program macro-arc preserved; computational-detail layer (D7, 9b, 9c, boundaries)
  systematically dropped.
- c08 (6/10): label-granularity mechanisms survive; omissions cluster on quantitative/derivative
  content.
- c09 (3/10): verdicts and dependency chains survive; R1-R6 definitions, correction stories,
  killed-candidate defects all dropped.
- c10 (3/10): headline facts survive; Weyl/Deninger/Fock mechanisms dropped. Parity exactly
  where the legend label contained the "why."
- c11 (1/10): only the epistemic-status probe (asserted-not-verified + verified panels) reaches
  parity; every number/formula/explanation drops.
- c12 (5/10): split verdicts and priority reasoning survive; guardrail concepts absent from
  extraction cannot be probed.
