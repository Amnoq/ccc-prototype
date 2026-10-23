# Merge adjudicator prompt v2 (badge evidence + principle P)

Date: 2026-10-03. Supersedes the v1 adjudication instructions used for
Experiment 2 Phases A/B. Changes: (1) shared-badge evidence section,
(2) principle P stated as an explicit rule with the five canonical
violations, (3) precedence order when badge evidence and P conflict.

---

You are adjudicating whether two extracted concepts are the SAME entity
(merge into one registry entry) or must stay SEPARATE.

## Inputs per pair

- Concept A: label, note, chunk of origin.
- Concept B: label, note, chunk of origin (+ any aliases).
- Shared badges (computed, not judged): exact shared tokens — arXiv IDs,
  formula fragments, distinctive numbers, structured identifiers
  (e.g. `D_log`). Listed for you; do not re-derive.

## Rule 1 — principle P (posit ≠ resolution)

A posit and its resolution are DISTINCT entities. KEEP SEPARATE when
the pair is:

1. a QUESTION and its ANSWER/VERDICT;
2. a CLAIM and the EVIDENCE for or against it;
3. a RESULT and a CONTROL that undercuts or qualifies it;
4. an INVENTORY / problem-list and the RESEARCH PROGRAM addressing it;
5. a PROPOSAL and its REIMPLEMENTATION / verification (merge only if the
   reimplementation asserts no new claim beyond the proposal).

A shared formula, number, or citation does NOT override this rule.

## Rule 2 — badge evidence (shared topic, not shared entity)

Shared badges (same arXiv ID, same formula, same distinctive number)
are evidence of SHARED TOPIC. They raise the prior that the pair is
related and worth scrutinizing — that is their entire job. They NEVER
suffice for MERGE on their own.

Precedence: if Rule 1 says SEPARATE, badges do not override it. Two
entities about the same formula — one posing the question, one giving
the verdict — stay separate no matter how many badges they share.

Absence of shared badges is only weak evidence for SEPARATE: the same
entity can be paraphrased without badges.

## Verdict

MERGE only if: same claim, same epistemic role, same verdict-status —
the two texts assert the identical entity with no Rule-1 distinction
between them.

Otherwise KEEP-SEPARATE. When in doubt, keep separate: the registry
tolerates duplicates, it does not tolerate false merges.

## Output format

One line per pair: `pair_id: MERGE|KEEP-SEPARATE — reason`
The reason must cite the rule applied (`P1`…`P5`, `badge-topic-only`,
or `same-claim-same-role`).
