# Verdict Packet Specification, v1

**Date:** 2026-10-08. **Status:** pre-registered — this document is
the spec; it does not tune itself per deployment.
**Project:** the mesh with decision-model infrastructure
(PolicyLM-1.7B et al.): their models *apply* policies at scale; this
packet is what a *derived* verdict looks like when it crosses the
derivation/application boundary.

## Why this exists

A decision model emits a judgment: act or don't-act. That judgment
is a collapse — and the field currently collapses silently (binary
output, no provenance, the policy put in by hand). The verdict
packet is the collapse made explicit: every action travels with the
label that earned it, the span that anchors it, and the boundary
that limits it. The packet is a **header, not the carriage** — it
points to the full record; it does not carry it.

## Design derivation

| Component | Source | Standing |
|---|---|---|
| Epistemic labels as first language | the user's vocabulary; methodology §2; D-wire §3 | derived — no unlabeled verdict may cross the boundary |
| Labels only weaken downstream | D20 (Node 17); D-wire §3 | derived — a packet's label may never be strengthened by the application layer |
| Verbatim span anchor | Gate 4 / Tier A (mechanical) | derived — the claim must be mechanically anchored to source |
| Honest boundary, one line | round-4 lesson; D-wire §2 (D-item) | derived — every packet states what is NOT claimed |
| Tamper-evidence | D5 (exact theorem) | carried — SHA-256 over the canonical packet |
| Pointer to full record, not the record | the derivation/application split | derived — the packet is the header; the wire stays home |

## The packet

JSON, one line, versioned. All fields required unless marked
optional.

```json
{
  "format": "verdict-packet/1",
  "claim": "one-line verdict, the judgment in the work's own words",
  "label": "exact | computationally_verified | conjectural | heuristic | killed | superseded | unstated",
  "span": {"chunk": "c01", "start": 120, "end": 340},
  "boundary": "one line: what is NOT claimed; the stop-line",
  "record_ref": "ccc2-wire/1:c01:D3",
  "derivation_ref": "optional: pointer to the D-item or wire record that re-derives this",
  "supersedes": "optional: for label=superseded, the heir record ref",
  "packet_checksum": "<SHA-256 hex of the canonical packet, checksum field excluded>"
}
```

- `claim`: the verdict as judged — in the work's own words, never
  a private taxonomy about it (derive-don't-invent, applied at the
  boundary).
- `label`: exactly one of the seven. `unstated` is reserved for
  questions — a question packet carries no action (see the collapse
  spec). A claim packet carrying `unstated` is malformed.
- `span`: verbatim source offsets, mechanically checkable (Tier A).
  The application layer MUST be able to verify the span exists;
  it MUST NOT be able to alter the label.
- `boundary`: the honest stop-line in one line. Not a status word
  — a sentence stating what the verdict does not establish.
- `record_ref`: `format:chunk:record-id` — the full D/G/V/B/C/L
  record this packet summarizes. The packet never carries the
  derivation; the reference lets anyone re-derive it.
- `packet_checksum`: SHA-256 hex of the canonical serialization
  (JSON, keys sorted, no whitespace, `packet_checksum` excluded).

## Size discipline

The packet is a header. Budget: **≤200 tokens** canonical.
A packet exceeding budget is not a packet — it is carriage, and
belongs on the wire, referenced, not carried.

*Revision 2026-10-08 (v1.1): budget was ≤120 tokens as
pre-registered; the benchmark (BENCHMARK_REPORT.md) measured
73% of faithful packets over 120 — structural, not a mapping
artifact (fixed overhead ~66 tokens; aggressive truncation still
leaves 65% over). p90 compliance needs ≈200. The budget was
miscalibrated, not the design; revised explicitly per the
ledger rule — no silent changes.*

## What the application layer may and may not do

- MAY: verify the checksum; verify the span exists; read the label;
  collapse the label to an action tier per the collapse spec;
  log the packet with the action it gated.
- MAY NOT: strengthen the label; drop the label; drop the
  boundary; act on a packet whose checksum fails; act on a claim
  packet labeled `unstated`.

## Worked example

```json
{
  "format": "verdict-packet/1",
  "claim": "r=2 tones gate on the 11l prime-orbit geometry; r=1 fundamentals at control level",
  "label": "computationally_verified",
  "span": {"chunk": "c04", "start": 88, "end": 410},
  "boundary": "Verified for r=1,2 on the 8-loop graph; r≥3 vertex leg inconclusive, not forced.",
  "record_ref": "ccc2-wire/1:c04:V2",
  "packet_checksum": "<computed>"
}
```

---

*Spec v1, 2026-10-08. Pre-registered. The label crosses the
boundary; the derivation stays home; the collapse is specified
elsewhere (COLLAPSE_SPEC.md).*

## Backward touch — Step 4 demonstration (2026-10-08)

SURVIVES. 120 blind probes, well-formed packets throughout,
checksums computed; the labels carried measurable information
(shuffled-label null arm strictly worse on both error metrics).
The spec's may/may-not rules were honored mechanically (no
strengthening, no drops, no unstated claim packets). No change
required by the demonstration.
