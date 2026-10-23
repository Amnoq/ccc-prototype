# Badge-weighted retrieval — Experiment 2 follow-up

Date: 2026-10-03. Origin: the cups session (ten/10/X — badges vs
compressors). Decision tree Node 14.

## Hypothesis

Paraphrase-invariant tokens ("badges") — arXiv IDs, formula fragments,
distinctive numbers, author citations, structured identifiers like
`D_log` — are reliable cross-chunk identity signals that TF-IDF's
tokenizer destroys (`D_log` → `d` [stopword] + `log`).

## Method (locked folds, truth set untouched)

- Same 12 v1 fold registries + concepts as `exp2_folds.py`; TF-IDF
  reimplemented verbatim as baseline (reproduces reported numbers:
  recall@1 = 0.667, recall@5 = 0.938 on the 144 SAME pairs —
  vs reported 0.67/0.95 on the corrected 126).
- Badge patterns fixed a priori from the corpus's character (arXiv
  `\d{4}\.\d{4,5}`, `X_y` idents, `Name–Name` / `Name (YYYY)` cites,
  formula tokens with `=^_`/math chars/digit-letter mixes, distinctive
  numbers); matched exactly after lowercasing; badge-idf cosine.
- Variants: V0 TF-IDF; V1 naive sum; V2 conditional sum; V3 rare-badge
  (df≤3) sum; V4/V5 top-20 rerank. No tuned weights.
- Files: `exp2_badges.py` (extraction + candidates),
  `exp2_badge_eval.py` (variant eval), `exp2_badge_precision.py`
  (precision on labeled pairs).

## Result 1 — ranking: NEGATIVE

| variant | recall@1 | recall@5 | MRR |
|---|---|---|---|
| V0 TF-IDF (baseline) | 0.667 | 0.938 | 0.785 |
| V1 naive sum | 0.569 | 0.910 | 0.720 |
| V3 rare-badge sum (best) | 0.597 | 0.944 | 0.750 |

Naive fusion HURTS (27 losses vs 5 wins). Best variant trades
recall@1 (−0.07) and MRR for +1 recall@5 pair. Badges are too sparse
to rank with and too noisy to fuse: spurious shared numbers
("num:200000") demote good TF-IDF ranks.

## Result 2 — precision as evidence: POSITIVE but modest

Among human-labeled pairs sharing ≥1 rare badge:
- Truth pairs: SAME-precision 0.431 vs 0.081 base (**5× lift**;
  28 SAME / 37 DIFF, n=65).
- Hook candidates: MERGE-precision 0.377 vs 0.093 base (**4× lift**);
  23% of MERGE vs 3.8% of KEEP-SEPARATE share a badge (**6× enrichment**).
- By type: `ident` 4/0, `num` 0.67, `formula` 0.40–0.47, `arxiv` 2/2
  (small n; indicative only).

## Result 3 — rescue: 1 of 9

Of the 9 TF-IDF misses (true entity at rank ≥5), rare badges rescue
exactly one (c04/c18, via the `W(h_a)≥0` formula badge, rank 7→0).

## The D_log case is NOT solved by badges

c12/c4 ("D_log spectral triples…" → true entity "CCM zeta spectral
triples arXiv:2511.22755…"): TF-IDF rank 5, badge rank 112. The entity
text contains no literal `D_log` — the connection needed full-text
arXiv evidence (what B1 used). Badges operate on extraction text;
this miss lives below that surface.

## Why: badges identify TOPIC, not ENTITY

The sharp version of the cups moral. A shared formula/number/arxiv-ID
says "same topic" — and under principle P, topic-similar pairs
(question vs verdict about the same formula) are DIFFERENT entities.
The badge is blind to epistemic role, which is exactly the distinction
P was created to enforce. "rq can't be confused with 10" tells the
difference between *notations*; entity identity needs the *arrangement*
(status), which badges cannot see.

## Recommendation (scoped)

- DO NOT fuse badges into the ranker.
- DO surface shared rare badges as explicit evidence in the merge
  adjudicator prompt ("shared badges: arxiv:2405.09608, formula:…"):
  4–5× precision lift where present, available in ~1/4 of true merges.
  May also steady weak judges (c09's over-merge) when paired with the
  P-rule: shared topic ≠ same entity.
- Candidate-expansion (union of TF-IDF top-5 + badge top-5) rescues
  ~1/9 retrieval misses at 2× adjudication cost — marginal; not
  recommended unless misses concentrate further.

## Prompt v2 validation (2026-10-03)

The v2 adjudicator prompt (`corpus_runs/ADJUDICATOR_PROMPT_V2.md`: badge
evidence + explicit principle-P rules + precedence clause) was tested on
8 pairs with certain ground truth, executed mechanically:

**Negative controls — must stay SEPARATE (all share badges AND violate P):**
- H037: question ("do optimizers have small-support structure?") vs
  verdict ("saturation is numerical") → P1 → KEEP-SEPARATE (badges:
  "degree-16", "small-support" — topic only, overridden). ✓
- H047: question vs verdict (same 9c topic, reversed sides) → P1. ✓
- H053: verdict ("Li Dirichlet-native") vs supporting evidence (λ_n
  finite-parts mechanism) → P2. ✓
- H107: result (13d GUE-like, ⟨r⟩=0.528) vs undercutting control
  (shuffled also GUE — generic chaos) → P3. ✓
- M002: inventory (ledger MISS 3) vs research program (Deninger) → P4. ✓

**Positive controls — must MERGE (same claim, same epistemic role):**
- H004: deformation derives 2C₂=1.32032 (both sides) → MERGE. ✓
- H007: twin conjecture unproven (both sides) → MERGE. ✓
- H009: positivity blind left of Re(s)=1 (both sides) → MERGE. ✓

**8/8.** The load-bearing check was the tension: every negative control
shares badges (same topic) yet violates P. A prompt treating badges as
merge evidence without the precedence clause would merge H037/H047/H053/
H107 — the exact failure the close-out caught. The precedence clause
("if Rule 1 says SEPARATE, badges do not override") resolves all five.

Caveat: the tester knew the expected answers; what was tested is that
the prompt *as a procedure* resolves the badge-vs-P tension correctly,
not that a blind judge would. A blind re-adjudication of the c09
over-merges remains the stronger (unrun) test.

## Prompt v2 blind-ish test on c09 hook cases (2026-10-03)

Ran the v2 prompt on 10 real c09 hook candidates: the 5 old-judge MERGEs
(the reported over-merges) + 5 old-judge KEEP-SEPARATE controls, verdicts
written to `corpus_runs/exp2_prompt_v2_blind10.json`.

**Ex-MERGE cases (old judge: all MERGE):**
- W09_10R1 (T02): paper vs D_log construct → KEEP-SEPARATE (P5; secondary
  unverified construct makes new numerical claims; badges overridden). OVERTURNED.
- W09_10R0 (T03): paper vs reimplementation → KEEP-SEPARATE (P5, borderline;
  reimplementation carries own provenance: bug fix, equation checks). OVERTURNED.
- W09_09R0 (T09): adele SPACE vs trace FORMULA → KEEP-SEPARATE (distinct
  objects; shared Connes/adele badges are topic only). OVERTURNED.
- W09_21R2 (T08): Deninger status verdicts → MERGE (same claim, same role;
  corroborated by independent Phase-B audit decision Q06R0). KEPT.
- W09_18R0 (T10): FF Jacobian "the template itself" vs template anatomy →
  MERGE (same-claim-same-role; less certain than T08). KEPT.

**Controls (old judge: all KEEP-SEPARATE):** v2 kept all 5 separate
(T01, T04, T05, T06, T07) — no over-flipping toward separation.

**Result:** v2 overturned exactly the 3 D_log/Connes over-merges the
close-out flagged, kept the 2 legitimate merges (Deninger, Weil template),
and left all 5 correct separations untouched. 10/10 consistent with the
corrected assessment.

**Honesty notes:** (1) the tester knew the 5 ex-MERGE ids and the
close-out's aggregate finding, so this is blind-ish, not blind — what it
tests is that the prompt *as written procedure* reproduces the corrected
judgments, including the badge-vs-P tension on real hook data; (2) T03
(P5 borderline) and T10 (less-certain keep) are the two judgment calls a
second judge should re-check; (3) per-pair corrected hook verdicts were
never written to disk (only aggregates), so scoring against the close-out
is by consistency, not by exact match.
