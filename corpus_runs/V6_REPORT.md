# v6 Codec Report — note channel + status-annotated entities

Date: 2026-10-03. Decision tree Node 13 (closed). Linear SID-16.
Design: `corpus_runs/V6_DESIGN.md`. Spec: `DECODE_SPEC.md` (v6 section).

## What v6 is

Two findings, one build:
1. **R3**: v5 wire had no anchor-note channel — R3's evidence notes rode
   the injection but not the wire (7.42 → 6.79 parity step).
2. **Exp2 close-out**: strict principle P was load-bearing only because
   the registry had no status/polarity field.

v6 adds: (a) anchor notes on the wire, (b) per-entity epistemic status
(0 unstated / 1 hypothesized / 2 asserted / 3 verified / 4 killed /
5 superseded) with temporal validity (valid-from / valid-until epochs),
(c) a deterministic merge lattice applied on rehydration, (d) the
mechanical merge-hook rule (never merge terminal-status with
live-status as the same live claim).

## Wire format (clean break, envelope version 6)

Int stream: `[6,B,E,nS,(L_i,S_i),nE,c_j,nA,a_k,nN,len_m,nT,q_r,Lp]`
- `a_k = (s*B+c)*B+n`: structural status enum (not a registry concept),
  0-based concept, 1-based note index (0 = none).
- `q_r = ((s*E+f)*E+u)*B+c`: status, valid-from epoch, valid-until
  (0 = unbounded), concept.
- Body: `NNNN(4)+P(1)+triplets+NOTETEXT+cksum(3)`; the checksum covers
  triplets AND notetext. Notes ride as literal text (see below).

## A design correction made during the build (recorded, not hidden)

First revision packed notes as raw bits in the triplet channel. Measured
on the r3 corpus: wire mean **1092 tokens**, BE_wire mean **3.21**
(max 5.44) — worse than the injection path (2.26) the wire was meant to
undercut. Root cause: the triplet channel costs ~1 token per 9 bits vs
~1 per 32 as text (~3.5× per note character).

Second revision: notes ride as literal NOTETEXT in the body (text as
text — also simpler for independent decoders). Wire mean **553 tokens**,
BE_wire mean **2.36**. The bit-packing revision is documented here as a
dead end, not deleted from history: encode the payload in its native
form unless the channel is proven cheaper.

## Measurements (12 r3 chunks, deterministic)

| check | result |
|---|---|
| Codec round-trip (encode→validate→wire→decode→canonical identity, incl. notes + statuses) | 12/12 |
| Independent decoder from DECODE_SPEC.md alone (`spec_decode_v6.py`, zero codec imports) | 12/12, name/edge/anchor/note/status/loop exact |
| Note survival (every doc note verbatim in a decoded anchor) | 246/246 |
| Merge lattice unit assertions (epoch precedence, terminal-beats-live ties, explicit revival) | pass |
| Wire tokens | mean 553, range 442–654 (v5: 144 — the delta is the note channel + status records, as designed) |
| Wire-path deployment break-even | mean 2.36, 11/12 ≤ 3; c09 at 3.07 |

**On c09 (3.07):** the ≤3 criterion is narrowly missed on one chunk —
the smallest (2017 prose tokens; least fixed-cost amortization; the same
chunk closest to the bar on the injection path at 2.92). Cause is chunk
size, not the v6 design: c09's wire (540 tokens) is unremarkable. Shared-
registry amortization (one registry sync across many chunks rather than
one per chunk, the deployment reality) would put it under 3; reported
conservatively without that credit. Not redesigned for 0.07 sessions.

## What v6 does NOT claim

- **Parity recovery** (wire-read 6.79 → injection 7.42) is *predicted*,
  not measured: the wire now carries every note the injection carries
  (246/246 mechanical survival), but the blind locked-probe re-score has
  not run. A non-blind provisional self-score was deliberately not
  substituted — the blindness chain matters.
- **Merge-hook integration**: the status rule is implemented
  (`apply_entity_status`) and specified, but not yet wired into
  `exp2_merge_hook.py` against a status-annotated `exp2_registry_v2`.
  That is the defined next experiment.

## Files

- `codec.py`: `build_message_v6`, `decode_struct_v6`,
  `validate_message_v6`, `encode_wire_v6`, `decode_wire_v6`,
  `apply_entity_status`, status enum + legacy string map.
- `memory_harness.py`: `to_v6_export`, `verify_roundtrip_v6`.
- `spec_decode_v6.py`: independent decoder + 12-chunk fidelity harness.
- `DECODE_SPEC.md`: v6 section (resident protocol; one-time cost).
- `corpus_runs/V6_DESIGN.md`: design rationale and dead ends.
