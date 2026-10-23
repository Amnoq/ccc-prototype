# CCC-2 Wire Format Specification ("D-wire"), version 1

**Date:** 2026-10-06. **Project:** CCC-2 (charter: `CHARTER.md`).
**Status:** native format — derived from the paperwork's forms
(NATURAL_FORMS.md), not migrated from v1.

## 1. Design derivation (what comes from where)

Each component is labeled **[derived]** (new in CCC-2, from the
paperwork/methodology) or **[carried]** (settled v1 verdict, adopted
without re-derivation — re-deriving a settled verdict would be
theater, per the methodology's permanence rule).

| Component | Source | Status |
|---|---|---|
| D/G/V/B/C/L record types | NATURAL_FORMS.md encoding map (M1–M4) + F1–F4 | **[derived]** |
| D-item fields (rule/generates/verified/boundary/label) | DITEM_SPEC.md (F1) | **[derived]** |
| Epistemic labels as first language | the user's own vocabulary; methodology §2 | **[derived]** (values match v7's validated set — the *set* is carried, the *nativeness* is derived; no migration exists) |
| Honest boundary as format field + decoder stop-line | round-4 lesson (Node 16) | **[derived]** |
| Guardrails/verdicts/bridges as wire citizens | M2/M3/M4 (v1 left these off the wire — Node 16 chain OPEN) | **[derived]** |
| Per-record + wire checksums | D5 (exact theorem: duplicate-index ambiguity unresolvable without) | **[carried]** (mechanism), applied natively |
| Notes as literal text (NOTETEXT) | D14 (raw bits measured worse: BE 3.21 vs 2.36) | **[carried]** |
| JSON serialization, telomere wrap, registry index | v1 settled (wire loss +0.00, permanent verdict) | **[carried]** |
| Transport framing (multiline, order-independent) | v1 settled | **[carried]** |

## 2. Record types

Every record has `id` (unique within the wire; format `D3`, `G1`,
`V2`, `B1`, `C7`, `L12` — type letter + number) and `type` (one of
`D`,`G`,`V`,`B`,`C`,`L`).

### D — D-item (mechanism)
The native mechanism encoding. All fields required unless marked
optional.
- `subtitle`: what the mechanism is, in one line.
- `rule`: the generative rule as an equation or formal rule.
- `conventions` (optional): edge cases, polarity, scope parameters,
  axis/conventions. List of strings.
- `generates[]`: ordered stages. Each stage: `stage` (what unfolds)
  + `prescription` (how to derive it — never outcome values or
  theorem statements).
- `verified[]`: carried checks. Each: `check` (description) +
  `expected` (values to compare against). A check may be
  `pending` with a `criterion` instead of `expected`.
- `honest_boundary` (required): where the derivation STOPS; what is
  NOT claimed; explicit do-not-present instruction. A boundary that
  is merely a status word is malformed.
- `honest_label` (required): epistemic status, native (see §3).
- `genre` (optional): `original` | `reframed` | `identification`.

### G — guardrail (killed path)
- `title`, `verdict` (one-line), `tried`, `result` (with numbers
  where applicable), `transfer` (lesson moved to live work).

### V — verdict (status + consequence)
- `subject`, `status` (native label), `consequence` (what the
  status forces next).

### B — bridge (identification)
- `x`, `y` (the `X ⟷ Y` identification), `buys` (what it buys),
  `limits` (honesty about limits).

### C — claim (atomic content)
For content that is not a mechanism, guardrail, verdict, or bridge:
definitions, plain claims, open questions.
- `kind`: `claim` | `definition` | `question`.
- `label`: the content in one line.
- `status` (required): native label. Open questions take
  `unstated` (questions are not claims).
- `note` (optional): NOTETEXT literal — evidence, numbers,
  qualifiers. Text as text, never raw bits (D14).

### L — link (typed relation)
- `from`, `to`: record ids.
- `rel`: `supports` | `contradicts` | `bounds` | `generalizes` |
  `implements` | `depends_on` | `causes` | `measures` |
  `defines` | `exemplifies` | `refines` | `supersedes` |
  (carried over from v1's validated relation vocabulary).

## 3. Labels (first language)

Values: `exact` | `computationally_verified` | `conjectural` |
`heuristic` | `killed` | `superseded` | `unstated`.
`unstated` is reserved for questions (kind `question` on C records)
— it marks "no epistemic claim is being made." A claim or
definition carrying `unstated` is malformed: every claim on the
wire carries its epistemic status; that is what "labels as first
language" means.
The codec may not conclude more than was established: a label may
only weaken along any processing step, never strengthen (D20's
lesson, applied prospectively — no migration needed because there
is nothing to migrate from).

## 4. Wire object

```json
{
  "format": "ccc2-wire/1",
  "chunk": "c01",
  "records": [ ... ],
  "registry": { "<id>": "<type>", ... },
  "wire_checksum": "<hex>"
}
```

- `records`: the D/G/V/B/C/L records in id order.
- `registry`: id → type index (carried over from v1's design).
- Checksums: each record carries `checksum` = SHA-256 hex of its
  canonical serialization (JSON, keys sorted, no whitespace,
  `checksum` field itself excluded). `wire_checksum` = SHA-256 hex
  of the concatenation of record checksums in id order. (D5:
  tamper-evidence is load-bearing.)
- Telomere wrap: the serialized wire is wrapped as
  `TELOMERE-CCC2-1:<payload>:TELOMERE-CCC2-1` (carried over).

## 5. Decoder procedure (normative)

An independent implementation from this spec alone must:

1. **Parse** the wire object; check `format == "ccc2-wire/1"`.
2. **Wire checksum**: recompute from record checksums; mismatch →
   WIRE-CHECKSUM-MISMATCH (reject the wire).
3. **Per record**: recompute `checksum`; mismatch →
   RECORD-CHECKSUM-MISMATCH (report the record id exactly).
4. **Well-formedness**: every required field present per §2;
   `honest_boundary` must state a stop-line (not a bare status
   word); every `generates` stage must have a `prescription`;
   `rel` values from the §2 list; labels from the §3 list.
   Violation → MALFORMED (report field + record id).
5. **D-items**: DERIVE each `generates` stage per its prescription
   (code where needed); CHECKSUM each `verified` check by
   recomputation → CHECKSUM-MATCH / CHECKSUM-MISMATCH /
   UNVERIFIED (for `pending`); BOUNDARY: restate the honest
   boundary and list the conclusions it forbids; LABEL carried
   verbatim (never upgraded).
6. **G/V/B/C/L**: carry fields verbatim; labels verbatim.

## 6. Worked example (D-item)

```json
{
  "id": "D1",
  "type": "D",
  "subtitle": "Deformation: the singular series as renormalized total weight",
  "rule": "p marks residues R_p = {0} (p=2), {0,−2} (p odd); n marked iff p|n or p|(n+2)",
  "conventions": ["p marks only n>p", "polarity mark=remove", "primes in order, finite z"],
  "generates": [
    {"stage": "markers-vs-survivors split", "prescription": "run the marking rule to z; characterize survivors structurally (no p|n and no p|(n+2))"},
    {"stage": "exact identities", "prescription": "mu-identity for unmarked counts via inclusion-exclusion over the marking rule; m(S)=∏|R_p|; δ(z)=∏(1−|R_p|/p) via CRT independence"},
    {"stage": "singular series", "prescription": "renormalize δ(z) ÷∏_{p≤z}(1−1/p)² → 𝔖(z); take z→∞; compute the limit"}
  ],
  "verified": [
    {"check": "survivors ≤200000", "expected": "2160 twin lowers"},
    {"check": "mu-identity", "expected": "exact at (z,x)=(13,50000) and (30,200000)"},
    {"check": "𝔖(z) values", "expected": "1.367187, 1.344116, 1.330277, 1.322754 at z=7,13,30,100; limit 1.32032"}
  ],
  "honest_boundary": "We verify the algebra (local factors assemble to 𝔖). The passage to π₂(x) ~ 𝔖·x/(log x)² is the unproven twin prime conjecture — NOT derived here. Do not present the asymptotic as established.",
  "honest_label": "computationally_verified",
  "checksum": "<computed>"
}
```

---

*Spec v1, 2026-10-06. Derived, not migrated. An independent decoder
built from this document alone must reproduce the reference decode
exactly — that is the fidelity gate.*
