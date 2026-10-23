# Natural forms in the paperwork → codec encoding types

Date: 2026-10-03. Methodology (user's steer): derive the codec's forms
from how the research paperwork is already naturally formed — do not
invent a taxonomy. Source: `~/workspace/prime-sieve-geometry/`
(DERIVATIONS.md D1–D8, DECISION_TREE.md, archive_dead_ends.md D1–D13).

## The catalog

### F1. D-item (DERIVATIONS.md) — the derivation form
Numbered title + descriptive subtitle ("D6. Deformation: the singular
series as renormalized total weight"). Body, in order:
1. **Rule** — the generative rule as an equation, + code ref + figure ref.
   ("prime p now marks residues R_p = {0} (p = 2), {0,−2} (p odd)")
2. **Staged generation** — what unfolds, in order ("separates markers
   from survivors" → "exact deformed identities" → "singular series,
   derived").
3. **Inline verification** — numerical checks with values ("verified:
   2160 ... checked against an independent primality sieve";
   "verified exact at (z,x) = (13, 50000) and (30, 200000)").
4. **Honest boundary** — where the derivation STOPS and what is NOT
   claimed ("the passage ... is the *unproven* twin prime conjecture...
   we verify the algebra, not the conjecture").
5. **Honest label** — epistemic status + what the reframing buys
   ("classical theorem, reframed"; "conceptual identification, not a
   new theorem").
Recurring sub-forms: "What this buys, and what it doesn't" /
"Have / Don't have"; "Precisely posed next questions";
"Resonance and gap".

### F2. Decision-tree node — the exploration form
Numbered, stable reference ("## 5. Methodological steer — 2026-09-29"):
Q (question), Decision, Evidence, Status (closed/open/forked).
"Numbers are stable references — cite them in future notes."

### F3. Dead-end entry (archive_dead_ends.md) — the guardrail form
Numbered ("## D1. DR9 pair affinity — endpoint artifact, not signal"):
Tried / Result (with numbers) / Transfer (lesson moved to live work).

### F4. Verdict — the status form
"Status: closed. Negative result, kept — it killed the naive hope and
forced node 4." = status + consequence. Node splits: "Node 9 splits:
9a (closed) / 9b (open) / 9c (open)".

### F5. Identification — the bridge form
"X is Y" / "X ⟷ Y" + what the identification buys + honesty about
limits (D5: "a conceptual identification, not a new theorem"; D2:
"Lehmer's φ-recursion IS the link recursion").

### F6. Maxim — the principle form
Standalone principle, then applied throughout: "never put the answer
in by hand — primality is never tested by a primality predicate, it
emerges from the shared/unshared rule, and everything downstream is
derived."

## Encoding map (paperwork form -> codec type)

| # | Paperwork form | Codec encoding | Replaces / extends |
|---|---|---|---|
| M1 | F1 D-item | **Mechanism encoding**: `D#[n]. [subtitle] / Rule: [eq] (code, fig) / Generates: [stages] / Verified: [checks] / Honest boundary: [stop-line] / Honest label: [status]` | Replaces the PERTURB triple syntax. Same information content (rule≈binary-op, stages≈axis-unfolding, verified≈computable observables, honest label≈@status) in his language, PLUS the honest boundary — which the triple lacked and which is load-bearing: it tells the decoder where unfolding must stop. |
| M2 | F3 guardrail | **Guardrail encoding**: `G#[n]. [title] — [one-line verdict] / Tried: / Result: [numbers] / Transfer: [lesson]` | New. Negative results ride the wire as guardrails, not dead weight. |
| M3 | F4 verdict | **Verdict encoding**: status + consequence | Extends v6 status enum: the status tag carries the consequence ("killed the naive hope, forced node 4"). |
| M4 | F5 identification | **Bridge encoding**: `X ⟷ Y` + what it buys + limits | The badge-adjudicator's "shared topic" plus the honesty qualifier. |
| M5 | F2 decision node | (context-level; not a wire entity type — noted) | The decision tree is the codec's *own* dev log, not wire content. |
| M6 | F6 maxim | (decoder-side principle, not wire content) | "Never put the answer in by hand" becomes the decoder's prime directive: derive, don't recall. |

## What transfers from the PERTURB work (findings kept, syntax replaced)

- The premise-completeness law (regeneration ⟺ premise-completeness;
  verdict by absent premise class).
- The 9 audit requirements (prescriptions, domain identifications,
  conventions, polarity, explicit axis, aggregation structure, name
  definitions, well-formedness, DERIVE/asserted).
- The fidelity method (pre-registered brief, calibrated decoder,
  anti-smuggling rule, gap log).
All three are about what information must be present, independent of
syntax. What changes: the SYNTAX is now the D-item form (M1), and the
family grows to M2–M4 from the paperwork.

## Immediate next step

Re-encode the tested mechanisms as D-items (M1 form) and re-run fidelity:
does the D-item syntax carry everything the v2.1 triple did? The honest
boundary becomes a scored observable (decoder must stop there).
