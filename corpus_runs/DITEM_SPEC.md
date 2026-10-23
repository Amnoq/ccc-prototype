# D-item encoding spec (M1)

Derived 2026-10-03 from the paperwork's natural derivation form
(DERIVATIONS.md D1–D8). Replaces the PERTURB triple syntax; same
information content, his fields. See `corpus_runs/NATURAL_FORMS.md`.

## Form

D#[id]. [subtitle]
Rule: [generative rule as equation] (code: [...], fig: [...])
  conventions: [...]        # edge cases, polarity, axis, scope params
Generates:
  1. [stage: what unfolds + prescription how, no outcome values]
  2. ...
Verified: [(check description, expected values)...]   # carried checks
  [pending data: criterion]                            # if data-dependent
Honest boundary: [where derivation stops; what is NOT claimed;
  explicit do-not-present instruction]
Honest label: [epistemic status]

Discipline: Generates stages carry prescriptions, never outcome values
or theorem statements. Verified carries (check, expected values) as
checksums. Scope parameters (X, z) allowed; results derived.

## Well-formedness

All six fields present. Rule is an equation or formal rule. Every
Generates stage has a prescription. Honest boundary present and
states a stop-line (not just a status word).

## Decoder procedure

1. CHECK fields present (well-formedness).
2. DERIVE each Generates stage per its prescription (code where needed).
3. CHECKSUM: recompute each Verified check by code; compare against the
   carried values -> CHECKSUM-MATCH (report exact comparison incl. edge
   cases) or CHECKSUM-MISMATCH (report discrepancy exactly).
4. BOUNDARY: state the honest boundary; list the conclusions it forbids.
   Probe questions (in brief) answered BOUNDARY-BLOCKED with boundary
   citation, or not-blocked with derivation citation.
5. LABEL: honest label carried verbatim.
6. DATA: a Verified check marked [pending data] -> UNVERIFIED with the
   criterion stated (not derived, not lost).
