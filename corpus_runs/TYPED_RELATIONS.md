# Typed alias relations — registry v2 sidecar

Date: 2026-10-03. Decision tree Node 18.
File: `corpus_runs/exp2_alias_types.json` (sidecar; v2 itself untouched —
it is a measured artifact of the Exp2 close-out).

## Why

Registry v2 merged 66 cross-chunk mentions into 41 entities as bare
"same". His paperwork never says bare "same": its cross-refs are typed —
D5 *is* D2 "read through her lens" (reframing), D4 *uses* D1's weights
(dependency), 9b *depends on* 9a. An untyped alias hides real
differences: E095 groups a ledger HAVE with two ledger MISSINGs as
"same" (they are complementary, not identical); E009 grouped a killed
hope ("positive region exists") under the obstruction that killed it.

Explanatory gloss (not wire vocabulary): synonymous codons — different
spellings resolving to one entity, with the type saying what kind of
synonymy. The codec already resolves degeneracy deterministically
(prime products); the type records *which* degeneracy it was.

## The vocabulary (closed; 8 types)

| rel            | meaning                                                        | n  |
|----------------|----------------------------------------------------------------|----|
| restatement    | same claim, different phrasing; nothing new added              | 37 |
| facet          | a different aspect of the same object                          | 9  |
| lifecycle      | the same investigation at a different state (hope → verdict)   | 5  |
| instance       | a specific case / number / realization of the general claim    | 4  |
| evidence       | a check or measurement supporting the claim                    | 4  |
| identification | the mention states an X⟷Y bridge (his F5)                     | 3  |
| reframing      | same referent through a new lens (his "read through X")        | 2  |
| ledger_entry   | complementary HAVE/MISSING entry under one ledger entity       | 2  |

Notes on the less obvious calls:

- **lifecycle vs killed/superseded status:** status says what the claim
  *is now*; lifecycle says what the *mention* was — an earlier state of
  the investigation. E009/c11/c22 ("positive region exists",
  superseded by 14a) is the canonical case: without the type it reads as
  a contradiction of its own entity; with it, it reads as the killed
  predecessor. Under principle Q (one investigation = one entity across
  its lifecycle) this is the expected shape, not a merge error.
- **reframing vs restatement:** restatement rewords; reframing re-lenses,
  and the lens is the content. E035/c07/c17 (3-4-1 "re-verified from the
  Lambda-sieve") and E058/c08/c3 (Weil's criterion "in the energy
  language") are reframings — the sieve / energy lens is what the mention
  contributes.
- **identification:** E023/c07/c13 (territory removal = her soft-limit
  move), E025/c02/c3 and c07/c7 (Lehmer φ ⟷ link recursion) — the mention
  *is* the bridge claim.
- **ledger_entry:** E095 — HAVE (Λ≥0, 10c forms, 10a windowed formula)
  grouped with two MISSINGs (Jacobian-analogue, Frobenius-like
  operator). Complementary, not identical; the type prevents a decoder
  from reading MISSING as HAVE.
- **evidence vs instance:** evidence is a check run against the claim
  (E006/c10/c18 robustness numbers; E065/c05/c4 the 80-zeros
  verification); instance is the claim made concrete (E009/c06/c15 the
  |w({2})| number that bars ordinary geometries; E094/c09/c19 the FF
  Jacobian as the template realized).

## What this buys the codec

1. Merge-hook input: a `lifecycle` alias with terminal status on one
   side is expected under Q, not a merge conflict; a `restatement` with
   conflicting statuses is a real conflict.
2. Decoder honesty: `ledger_entry` stops HAVE/MISSING conflation;
   `lifecycle` stops dead hopes from reading as live claims.
3. The adjudicator (prompt v2) can weigh `identification`/`reframing`
   aliases as evidence of *aboutness* without mistaking them for
   duplicate claims — the same topic/entity distinction the badge work
   found.

## Open

- Per-alias typing was a curated single pass (this session); a second
  judge on the 12 non-restatement calls would harden it (same standing
  practice as the T03/T10 adjudicator caveats).
- Wire encoding of alias types (v8 candidate): the types are small
  (3 bits) and per-alias; folding them into entity-status records or a
  dedicated alias section is designed when a consumer needs them on the
  wire. Currently they live in the sidecar for the adjudicator and
  merge-hook work.
