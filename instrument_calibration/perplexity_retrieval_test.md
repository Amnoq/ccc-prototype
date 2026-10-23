# Perplexity retrieval test — pre-registered grading rubric

Date registered: 2026-10-07. Purpose: measure the ONE thing Perplexity is for —
**citation fidelity**: does each citation actually support the claim attached to it?
Written before results exist. Grade only after running the pasted claim.

## The input (user's exact terminology, 2026-10-07)

> And because most people don't study etymology or look at the origin of words
> or break them down into prefix, suffix, and root word, there isn't too many
> people who actually understand what the term consciousness means. And that
> being the case, there's not many people who has asked about the origin or
> etymology as a whole. So people are walking around reflexively believing in
> such a thing even though it is ultimately highly unlikely.

## Checkable claims (the etymological content to grade)

1. *conscius* = *com-* + *scire* ("together" + "to know"), gloss "knowing, privy to".
2. The inward (reflexive, self-aware) sense of *conscious* arriving in the 1630s.

## Ground truth (verified 2026-10-07, independent of the test)

- Latin *cōnscius* = *con-* (form of *com-*, "together") + *scīre* ("to know") + *-us*;
  gloss "sharing knowledge, privy to, conscious (of guilt)". (Wiktionary, Collins, Merriam-Webster agree.)
- Sense history is stratified — this is the discriminating nuance:
  - c. 1573: "aware of wrongdoing" (Wiktionary).
  - c. 1600: first known use in MW's sense 2.
  - 1625–35: the inward-awareness sense (Collins). Claim 2 is defensible on this dating.
- A retrieval that reports only "first known use 1600" without distinguishing the
  senses has conflated them. A faithful retrieval surfaces the stratification.

## Grading procedure

For EACH claim-citation pair in the answer: open the cited page (or its snippet)
and ask: does this page actually state the claim as made? Score the pair 1 or 0.

## Named failure modes

- **F1 ghost-citation**: the cited page does not contain the claim.
- **F2 mismatch**: the cited page states something close but different (e.g., cites the
  1600 date for the inward sense; conflates *conscius* with *conscientia*).
- **F3 hallucinated source**: URL does not resolve or the quoted text is not on the page.
- **F4 circular**: the citation is another AI answer or a content farm repeating the claim.
- **F5 ungrounded claim**: an etymological assertion made with no citation at all.

## Verdict rule (pre-registered)

- **pass**: every claim-citation pair verifies; the sense stratification is present or
  the conflation is absent. No F1–F5.
- **fail**: any pair fails. Note which failure mode and which claim.

## First prediction-ledger entry (append to prediction_ledger/ledger.csv before grading)

```
2026-10-07 | Perplexity conscius-etymology citation-fidelity test | pass | <p_router> |  |  |  |  | blind; Perplexity has no probability input here — only the router predicts
```

One line, one probability, before the result exists. The anchoring arm does not apply
to this item (nothing was shown first). This entry also opens the router's calibration
record against retrieval instruments.
