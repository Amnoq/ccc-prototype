# Prediction ledger

Date: 2026-10-07. Gives the router skin in the game at no cost:
one line per prediction, scored later. The only error-penalty
this setup can have is a record you can't quietly revise.

## Format

`ledger.csv`, one row per prediction, append-only:

```
date | artifact/claim | outcome_class | p_router | p_ai_1 | p_ai_2 | shown_first | result | notes
```

- **date**: YYYY-MM-DD.
- **artifact/claim**: what the prediction is about.
- **outcome_class**: fixed set — `exact`, `computationally_verified`,
  `killed`, `insufficient`, `pass`, `fail`. Every prediction names
  one class and a probability that *that class* occurs. No
  interpretation afterward.
- **p_router / p_ai_1 / p_ai_2**: probabilities in [0,1].
- **shown_first**: `blind` or `shown` — coin flip per item: was an
  AI probability visible before the router logged theirs? (The
  anchoring test. Leave empty if the test isn't running on
  that item.)
- **result**: `1` (the predicted class occurred), `0` (it didn't),
  empty (pending), or `skip` (logged skips, never silent omissions).
- **notes**: free text — e.g., which AI gave p_ai_1.

## Rules

1. **Log before the result exists.** The prediction is written
   before any computation, check, or critic verdict comes back.
   Results fill the `result` column later; a logged probability
   is never edited.
2. **Router logs blind to the AIs'.** Write p_router before
   seeing p_ai_*. The anchoring test (rule 5) measures what
   happens when this is violated.
3. **Paired.** AI probabilities go on the *same* items, same
   format, before the result. Paired comparison cancels
   item-difficulty noise.
4. **Don't act on it until n is large enough.** Noise sets the
   floor: per question class, no selection or termination
   authority shifts until n ≥ 50 **and** the paired difference
   exceeds twice its standard error. Below that, the ledger is
   a record, not a lever.
5. **Anchoring test.** On a random half of items, show an AI
   probability before logging; on the other half, log blind.
   Fit p_router = a + w·p_ai per arm. The blind arm is the
   baseline — shared evidence correlates forecasters even
   blind, so w_blind > 0 is not relay. **Anchoring is the
   difference w_shown − w_blind**, reported with a bootstrap
   interval. If blind scores better than shown, blind-first
   becomes the standing rule.
6. **Skips are logged.** A skipped item is a `skip` row, not an
   omission. The skip rate tells you when the format is too
   heavy for a hobby.
7. **No cherry-picking the question.** Always log the *modal*
   class — the outcome you consider most likely — not the
   class you're most confident about. And every commissioned
   artifact gets an entry: the item stream is the work stream,
   not a selection of favorites. (Full-distribution logging,
   scored with multiclass Brier, is the upgrade path if
   selection bias is suspected.)
8. **No peeking.** Pre-register n per question class and test
   once at the threshold. The 2-SE flag is per-comparison;
   across classes and AIs the family-wise error is higher, so
   treat non-primary comparisons as exploratory.

## Scoring

`score_ledger.py` (stdlib only) reports, over scored rows
(result 0/1):

- Per-agent Brier score: mean((p − outcome)²), lower is better.
- Base-rate reference: f = mean outcome, BS_ref = f(1−f);
  skill = 1 − BS/BS_ref (positive beats "just guess the base
  rate"; hedging at a fixed 0.5 earns *negative* skill unless
  f = 0.5 — at f = 0.2 it is −0.56; only hedging toward the
  base rate itself earns ~0).
- Per outcome_class breakdown.
- Paired router-vs-AI differences with standard errors and the
  2-SE significance flag.
- Anchoring: w_shown − w_blind with bootstrap interval (the
  blind arm is the baseline — shared evidence correlates even
  blind).
- Skip rate.

## Reading the result (per question class)

- Router beats AIs on judgment questions but not computational
  ones: "the human will be outperformed" holds only where a
  script can already decide.
- AIs lead everywhere: authority moves toward the arbiter plus
  the scripts; the router keeps selection and the stop call,
  which need no skill score.
- Poor calibration everywhere (flat reliability curve): shrink
  everyone's stated probabilities toward the base rate; don't
  change who decides.
- Asterisk, on the record: the router predicts their *own*
  research process, so beating the AIs partly reflects inside
  information, not just judgment. And calibration on outcome
  classes is adjacent to — not identical with —
  selection/termination skill.

## 2026-10-08: router withdrew as forecaster (standing change)

The router considered the loop and ruled: the machine needs no help
from him to make predictions. With immediate effect:

- No more `p_router` solicitation. New items get AI probabilities
  (`p_ai_1`, `p_ai_2` where applicable) logged before results, per
  rule 7 (every commissioned artifact gets an entry). The paired
  router-vs-AI comparison continues only on already-logged pairs;
  no new pairs are opened.
- The anchoring test (rule 5) is suspended — it needs both arms.
  `shown_first` is still recorded per item for the record.
- Outcomes the charter defined as "the router's verdict" (items 3,
  4) are rendered by the machine against the pre-registered bar,
  with delegation and rationale appended to the item's notes.
  Already-logged probabilities are never edited; only the
  result column is filled, which is the designed workflow.
- The router's word remains final: any machine-rendered outcome
  is overridden on his say-so, and the ledger notes the override.

First application, same day: item 4 (Atlas-4) rendered pass=1 by the
machine — 0 direct sky<->sky links, 4 split_links all on the LeCun-89
bridge, both seeded controls resolved, 0 merges/contradictions/false
merges; the report's own pre-verdict assessment called it consistent
with the narrow-links prediction. Scored: router (0.775) BS=0.0506,
ai_1 (0.70) BS=0.0900, n=1 — descriptive only, no significance
claimed. Item 3 left unscored: no probabilities were ever logged,
and the S2 control was void, so the run cannot speak to the claim;
the analytics<->geometry follow-up remains the real test.
