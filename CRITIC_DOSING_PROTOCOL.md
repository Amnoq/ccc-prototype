# Critic dosing protocol

Date: 2026-10-07. How to maximally benefit from Claude's rigorous
critique without it running away with the project. The critic is
medicine in measured doses, poison as environment. This is the
dosing mechanism.

## The shape

Builder (Muse, the environment) — Critic (Claude, the dose) —
Router (the user, who decides). The triad made explicit for the
AI team: the builder makes the claim, the critic is the polar
opposite, the router holds the verdict.

## Rules

1. **Checkpoints, not streams.** The critic only ever sees
   finished, formed artifacts. Never drafts, never work in
   progress, never "what do you think of this direction."
   Seedlings stay in the environment; only formed claims go to
   the critic.

2. **One question per dose.** Each commission carries a single
   verdict-scoped question — e.g., "find defects in this
   protocol that would change a verdict," "grade this extraction
   against the recorded structure." Never "review this."

3. **Two rounds max per commission — with precedence.**
   Round 1: the critique (verdict + defects + proposals).
   Round 2: the critic reviews the *diff* between the artifact
   it saw and the amended one — covering both faithfulness (did
   the amendments land as proposed?) and defects *introduced
   by* the amendments (a faithful copy of a flawed amendment
   still fails; the v3 Tier B regression is the standing
   example). Anything outside the diff is out of scope unless
   it becomes a new commission. Then the router decides:
   accept, or commission anew. The critic never self-renews;
   continuation is always the router's explicit call.
   **Precedence:** the review ends at the *earlier* of two
   rounds or a round with zero verdict-changing findings — a
   clean round 1 closes the commission without a pointless
   round 2, and a live round 2 still hits the cap.

4. **Propose, don't author.** The critic's output is verdicts
   and proposals. Integration is the builder's job. The critic
   never edits the artifact — authorship is how a critic runs
   away with a project.

5. **The stop rule in the brief, upfront — defined
   operationally.** Every commission states the exit before the
   critic starts, and "verdict-changing" has a definition: a
   defect counts iff fixing it would change a status label, a
   gate's pass/fail, or a promotion decision. Findings that are
   only wording or style are logged but do not count toward
   continuation. The critic knows the dose is finite — and
   exactly what "finite" means — before its first word.

6. **Batch the doses.** Accumulate two or three formed artifacts,
   then commission one pass — one verdict-scoped question per
   artifact, with the round cap applying to the dose as a whole.
   Fewer, denser doses — less courier overhead, less surface
   for runaway.

7. **Play to the strength.** Commission the critic for:
   pre-mortems on finished designs ("try to break this"),
   calibration-battery design, grading against known answers,
   constructing the strongest counter-case, and trajectory
   checks ("is this project drifting off on a tangent?") —
   drift *detection*, not direction *setting*. Never for:
   direction-setting, early-stage ideas, open-ended
   exploration. Harshness is a finishing tool, not a
   starting one. The trajectory check is preventive: a tangent
   caught early is cheap, caught late it is time-consuming and
   resource-intensive to correct — which is the economic
   rationale for the check-in itself.

8. **Open-defects ledger.** When the router closes a commission
   with defects still open, they do not vanish: the commission
   record lists each open defect with the router's reason for
   accepting anyway. A later commission on the same artifact
   opens by reading the ledger. Closing over a defect is a
   decision on the record — the review process gets the
   no-silent-drops discipline too.

9. **Selection audit: the blind slot.** Rule 1's filter —
   only formed artifacts reach the critic — puts selection in the
   router's hands on prior judgment. That is structurally the
   gatekeeping failure in miniature, and it was untested. The
   analogy is real but incentive-different: peer-review
   gatekeepers are third parties who *kill* ideas; the router is
   the work's author, whose incentive is its truth, and the filter
   *delays* criticism on observed evidence of seedling-smashing.
   Neither point removes the need for measurement. The
   dose-versus-environment boundary becomes an empirical quantity:

   - The router logs every artifact considered but held back, with
   the reason — the decision tree's discipline, applied to
   selection.
   - Each batch reserves one blind slot: an artifact chosen by
   fixed rule (oldest unreviewed), not by router judgment,
   reviewed regardless of readiness assessment.
   - Track the verdict-flip rate on blind-slot artifacts versus
   routed ones. Similar rates: the filter removes nothing —
   loosen it. Much lower blind rate: the filter is doing real
   work. Higher blind rate: the filter is hiding defects —
   recalibrate.
   - The cost is priced explicitly: the blind-slot artifact is a
   seedling deliberately exposed to the smasher, one per batch,
   as the price of calibration. Its findings go to the
   open-defects ledger whether or not the router acts on them.

   Incentive provenance, on the record: this proposal expands the
   critic's access and comes from the critic. It is a fair test
   because the outcome can vindicate the filter — but the
   provenance is stated, not laundered.

10. **Verdict format: established first.** Every critic verdict
    follows a fixed order: (1) the verdict line; (2) what is
    established — only what the span or computation supports,
    held to the same standard as the defects (no compliment
    sandwich: the established section is evidence, not praise);
    (3) defects; (4) proposals. This is a formatting rule, not
    a change of standard — hopes are set by the evidence first
    and challenged second, defects stay exactly as strict. The
    builder follows the same format.

## Critic calibration: the likelihood ratio of flags

Harshness counts only as much as its LR. P7.4 names the failure:
flags at the same rate regardless of the artifact's quality are
performative skepticism, however strong they sound. The test:

- Build 20+ artifacts per arm: half with planted
  verdict-changing defects (the router knows where), half
  known-clean (e.g., sections that computation already
  verified). 5 per arm is underpowered — at H=0.8, F=0.2 the
  95% interval on LR is roughly 0.7–24; at 20 per arm it is
  about 1.6–10.
- Commission the critic blind: one verdict-scoped question per
  artifact, no indication of which are planted. **Run on a
  fresh instance** with no access to the design thread — a
  critic that has read the test's design cannot take it blind.
- The unit is the artifact: H = fraction of planted artifacts
  where the planted defect was found; F = fraction of clean
  artifacts drawing a verdict-changing flag.
- A flag on a "known-clean" artifact goes to the router as
  adjudicator: if the defect is real, the artifact wasn't clean
  (not counted in F, recorded as a find); if not, it counts in
  F.
- LR = (H+0.5)/(F+0.5) per question class, cell-smoothed (F=0
  would otherwise make it infinite), reported with its 95%
  interval.
- Reading: LR ≈ 1 → the flags are noise, however strong they
  sound. LR = 4 → a flag moves a 20% prior to ~50%, not to
  certainty. A flag's weight in router decisions is its LR —
  strong pushback becomes a measured weight.
- Re-run periodically. The critic's LR is a standing
  measurement, not a one-time certificate.

The LR test itself is commissioned through this protocol —
bounded, single-question, router-terminated like any other
dose.

## Why this works — and what it claims

Four courier rounds produced genuine improvements (source-span
anchoring, the ladder-verdict grader, the bounded reporting
rule, the promotion pipeline), so the evidence does not separate
"productive tightening" from "runaway" — every round changed
something real. The protocol is prophylactic, not diagnostic:
it bounds a structural risk (a harsh critic with no stop
condition can loop indefinitely); it does not assert the loop
*was* unproductive. What it keeps: the rigor, which the rounds
proved. What it removes: the unboundedness, which no round
could disprove. Bounded rounds, router-held termination,
authorship retained by the builder — and now an open-defects
ledger, so closing over a defect is a decision on the record
rather than a silent drop.

## Applicability

The four completed protocol-review rounds are pre-protocol
history — they motivated these rules and are grandfathered
under them. The two-round cap and the stop rule take effect on
the next commission.
