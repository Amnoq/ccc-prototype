# Arbiter design (prophylactic)

Date: 2026-10-07. Design for a third, well-calibrated, isolated AI
on standby to resolve gridlock between builder and critic.
**Status: prophylactic, not active.** Six courier rounds ran with
no gridlock and near-total convergence; the arbiter solves a
problem we have not had. It activates on genuine disagreement or
at operational scale — not before.

## The problem it addresses

"AI + AI = AI" narrowed: a second AI adds checking but not a
different error distribution. Correlated errors mean the builder
and critic can agree and both be wrong — the quietest form of
the failure, which no disagreement-triggered mechanism ever
sees.

## The four holes (from the critic's own review)

1. **Correlated agreement never triggers it.** Gridlock-only
   arbitration misses shared blind spots.
2. **Compilation bias.** Whoever phrases the combined problem
   chooses what the conflict is; stylistic fingerprints survive
   attribution-stripping.
3. **"Well-calibrated" untested.** Under P7.1 the arbiter is
   credited only after a test that could have come out the
   other way.
4. **"The human will be outperformed" untested** on the human's
   non-computational roles (ground truth, termination).

## Controls (all required before the arbiter holds authority)

- **Model separation.** The arbiter comes from a different model
  family than builder and critic. Report its measured agreement
  rate with each; very high agreement with either means it adds
  little independence.
- **Agreement audit.** Sample a fixed fraction of cases where
  the two AIs agreed (the blind-slot mechanism, applied to
  consensus) and send them to the arbiter anyway. Its dissent
  rate from consensus estimates shared-blind-spot frequency.
- **Neutral compilation.** Each side writes its position in a
  fixed template (claim, evidence, what would change its mind).
  The human strips attribution, checks completeness,
  randomizes order. Test the anonymization: a separate model
  guesses which side wrote each position — if it beats chance,
  the compilation leaks source and needs normalizing.
- **Calibration battery.** Gridlocks with known answers
  (planted, plus real past disputes later settled by
  computation). Include "undetermined" cases — an arbiter that
  always picks a side is not calibrated. Report accuracy and
  abstention rate before it holds authority.
- **Binding scope.** On exact-grade or computationally checkable
  questions the arbiter is advisory and the script decides. Its
  ruling binds only on judgment questions that can't be
  computed.

## Activation

Two tiers, not one. "Inactive" cannot rest on convergence alone,
since convergence is indistinguishable from correlated agreement
— the quietest form of the failure this design exists for:

- **Agreement audit (runs on schedule, audit-only).** Sample a
  fixed fraction of consensus cases and send them to the
  arbiter anyway; its dissent rate estimates shared-blind-spot
  frequency. Audit-only: it measures, it does not rule, and it
  needs no gridlock to run. Requires a third model family;
  until one is on standby this is specified but not runnable
  (human spot-checks are a weaker interim).
- **Full authority (on gridlock or scale).** Genuine
  builder–critic gridlock the dosing protocol's two-round cap
  cannot resolve, or deployment at a scale where the router
  cannot personally terminate every loop.
