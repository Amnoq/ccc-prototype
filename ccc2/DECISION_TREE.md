# CCC-2 Decision Tree

Second-generation codec, chartered 2026-10-06. The method runs from
node 0. Nodes are namespaced CCC2-N. Parent project:
`~/workspace/ccc-prototype/` (v1 tree + LEDGER.md). Charter:
`./CHARTER.md`.

---

## CCC2-0. Charter — 2026-10-06
**Q:** Rebuild the codec from the correct principles, with the
ledger as foundation and v7/R5 as the control arm?
**Decision:** yes — user's "let's run it." Second-generation build;
v7/R5 stays running as reference.
**Principles (native):** D-items as encoding form; epistemic labels
as wire's first language; honest boundaries built in; R5 derivation
rules from the first extractor; methodology from node 0; no lossy
migrations.
**Control arm benchmarks (v7/R5, same corpus + blind protocol):**
parity 8.92/10, wire loss +0.00, BE_dep ≤3 mean, fabrication 0.
**Triadic frame:** claim (CCC-2 meets/beats) / polar opposite
(v7/R5 stands; convergence validates the current design as derived)
/ null (ledger alone). No losing leg.
**Status:** chartered. Next: CCC2-1 — native wire format derivation.
**Methodology layer:**
- Labels: the charter is a founding document — **heuristic**
  (principles) + **computationally verified** (benchmarks quoted
  from measurement).
- Fork: none — single charter decision.
- Why it ends here: the build is authorized; its terms are set.
- Its own chain: the entire CCC-2 tree below.

---

## CCC2-1. Native wire format ("D-wire" v1) — 2026-10-06
**Q:** What goes on the wire, derived from first principles with no
migrations?
**Derivation:** from NATURAL_FORMS.md's encoding map (M1–M4) and the
paperwork's forms (F1–F4), checked against LEDGER.md before each
choice. Record types: D (D-item: rule/generates/verified/honest
boundary/honest label — M1), G (guardrail — M2), V (verdict:
status+consequence — M3), B (bridge: X⟷Y+buys+limits — M4),
C (claim/definition/question), L (typed link). Labels are the
epistemic vocabulary as first language (right the first time —
D20 applied prospectively, no migration). Honest boundary is a
format field with decoder enforcement (round-4 lesson built in).
Transport carried over from v1 and labeled: JSON, telomere wrap,
registry index, per-record + wire SHA-256 checksums (D5's
load-bearing discipline), NOTETEXT literal notes (D14).
**Triadic fork:** claim (this native format) / polar opposite
(v7's wire stands — the transport layer IS this leg, carried over;
convergence validates v7) / null (LEDGER.md: raw-bits notes D14,
checksum-free D5, statistical stages D4, invented taxonomies D19 —
all already killed).
**Deliverables:** `ccc2/SPEC.md` (normative, incl. decoder
procedure §5 + worked example), `ccc2/codec.py` (encoder/decoder;
self-test: round-trip ok, tamper caught).
**Status:** specified + implemented. Next: CCC2-2 — native extractor.
**Methodology layer:**
- Labels: the format design — **heuristic** (design, pre-validation);
  carried-over transport (checksums, telomeres, NOTETEXT) —
  **computationally verified** (v1's measurements: wire loss +0.00,
  BE 3.21 vs 2.36); codec self-test — **computationally verified**.
- Fork: as above; the opposite leg (v7 transport) is load-bearing —
  it is what makes "carried over, labeled" honest instead of
  re-derivation theater.
- Why it ends here: the format is specified and the codec
  implements it; the self-test passes.
- Its own chain: CCC2-2 (extractor emits these records natively);
  the independent spec-only decoder (fidelity gate) will work
  from SPEC.md alone.

---

## CCC2-2. Native extractor — 2026-10-06
**Q:** How does extraction emit D/G/V/B/C/L records natively, with
R5's derivation rules from the start?
**Design:** `ccc2/EXTRACTOR_PROMPT.md` — record types with native
rules: derivation preservation (premises→steps→conclusion+
prescription, ~25 words for mechanism notes), derive marking,
domain identification, restatement-band restraint (D18), honest
boundary stating what's missing instead of inventing (fabrication
is the unforgivable failure), native labels with ties-go-weaker
(D20 prospective), questions take unstated.
**Run:** 4 blind extractors × 3 chunks (12-chunk corpus), blind
protocol (prompt + chunk text only). Result: 225 records
(D×48, G×27, V×36, B×17, C×43, L×54).
**Repair pass (v1's ≤2-attempt rule):** first validation caught 16
malformed records — 4 hollow D-items (reclassified honestly:
D2→C4 definition, D5→C5 claim, D3→B4 bridge; one D5 supplied
sourced verified[]), 12 V-records with tree-status "closed"
(re-labeled to native epistemic values, ties go weaker, no
upgrades). The prompt itself was strengthened (V.status native-only;
D requires generates+verified) — the instrument fixed, not just
the output.
**Resistance honored:** c12 (literature survey) emitted zero
D-items — mechanisms carried in G/B/C/V with honest boundaries
rather than fabricated; c01's thin ledger items declined rather
than invented; cited-but-not-derived literature labeled
`conjectural` with notes (native set has no "cited" value —
recorded as a format observation, spec unchanged mid-run).
**Triadic fork:** claim (native D-item extraction) / polar opposite
(R5's JSON extraction stands — the control the fidelity gate will
be measured against at parity time) / null (LEDGER.md: invented
taxonomies D19, restatement bloat D18).
**Status:** extracted + repaired. Next: CCC2-3 — fidelity validation.
**Methodology layer:**
- Labels: the prompt design — **heuristic**; the 225-record run +
  repair — **computationally verified** (files on disk, re-runnable
  validation); "no fabrication" — **computationally verified**
  (declined extractions on record).
- Fork: as above.
- Why it ends here: all 12 chunks extracted natively, malformations
  repaired, prompt strengthened.
- Its own chain: CCC2-3 (wire build + 12/12 round-trip +
  independent decode).

---

## CCC2-3. Fidelity validation — 2026-10-06
**Q:** Does the native wire survive the fidelity gate — 12/12
round-trip plus independent spec-only decode?
**Method:** `ccc2/validate.py` — encode each chunk's extraction via
`codec.py`, write wire, decode, field-by-field compare (id-ordered).
Then the v6/v7 control: an independent decoder written by a blind
child subagent from SPEC.md alone (zero codec imports, never saw a
wire while writing) — `ccc2/independent_decode.py` — run on all 12
wires, output compared record-by-record against the reference
decode.
**Repair cycle (the gate working as designed):** first validation
caught 16 malformed extraction records (repaired; prompt
strengthened). The independent decoder then exposed 3 further
spec-conformance gaps: (a) `unstated` on two claim records — spec
clarified (§3: unstated reserved for questions; the sharper design,
prevents status-field erosion per D20's lesson), records re-labeled
`heuristic` on source basis; (b) D-item `conventions` as bare
string — spec already required a list; record repaired; (c)
pending `verified` check missing its `check` description — spec
requires check+criterion; supplied from record context. Each fix
was a clarification or record repair — never a silent relaxation.
**Results:**
- Round-trip (reference codec): **12/12 exact**, 225 records
  (D×48, G×27, V×36, B×17, C×43, L×54).
- Independent decode: **12/12 MATCH** — identical record sets on
  all chunks. The six spec ambiguities the independent author
  documented (non-ASCII encoding, id sort order, boundary thinness
  test, unstated scope, rejection ordering, registry/L-link
  strictness) all resolved without divergence after the
  clarifications above.
- Tamper-evidence: codec self-test catches payload tampering via
  checksums (computationally verified).
**Triadic fork:** claim (native wire is faithful) / polar opposite
(v7 wire stands — the parity gate, not this run, adjudicates which
carries more) / null (LEDGER.md alternatives already killed).
**Status:** FIDELITY GATE PASSED. Stopping here per scope — parity
measurement is the next gate, not this run.
**Methodology layer:**
- Labels: 12/12 round-trip — **computationally verified**;
  12/12 independent match — **computationally verified**;
  tamper-evidence — **computationally verified**; "wire is
  faithful" — **computationally verified** (at the fidelity level;
  parity/carriage is the next gate's question).
- Fork: as above.
- Why it ends here: both halves of the fidelity gate pass; the
  scope explicitly stops before parity.
- Its own chain: the parity gate (next run): blind rescore of
  CCC-2 wires vs the v7/R5 control arm on the locked probes.

---

## CCC2-4. Parity gate — 2026-10-06
**Q:** Does CCC-2's extra carriage earn its cost — parity ≥8.92 at
acceptable break-even, parity gains that justify the cost, or
neither? (Charter adjudication.)
**Method:** blind protocol replicated exactly from R5 (4 scorers ×
3 chunks, 10 locked probes, 0/0.5/1 rubric, scorers saw only
rehydrated D-wire records + probes.yaml); 2 drift controls (S1→R5
c02, S2→R5 c06), same as R5. Wire integrity verified first
(validate.py 12/12 OK; no repairs). Break-even by R3-identical
conventions (tiktoken cl100k_base; be_dep=(prose+output)/savings).
**Results:**
- Parity **9.75/10** (R5 8.92, +0.83); per-class NUMBER 0.967 /
  VERDICT 0.933 / MECHANISM 0.983 (highest measured); 11/12 chunks
  gained or held (c12 −0.5: Connes absorption mechanism reduced to
  a guardrail parenthetical); zero fabrication (0/120, all misses
  OMISSION).
- Cost: every wire LARGER than its prose — 1.004×–1.695×, mean
  1.437× (48,104 vs 33,474 tokens). Savings negative 12/12 →
  BE_dep undefined: the wire never breaks even. Structural miss,
  not marginal.
- Strictness: ones-rate 95.0% (R5: 79.2%) — reckoned via controls.
  S1 −0.5 drift (within ±1.5 variance); S2 −4.0 (very strict) yet
  scored CCC-2 10.0×3 while giving the R5 wire 5.5. Within-scorer
  wire deltas: +0.5 (c02), +4.5 (c06) — the rigorous core; both
  favor CCC-2. Absolute cross-battery delta carries the known
  between-scorer caveat.
**Verdict vs charter benchmarks:** parity ≥8.92 MET and exceeded;
wire loss +0.00 HELD (CCC2-3, not re-litigated); BE_dep ≤3 MISSED
(structurally — never breaks even); fabrication 0 HELD.
**Central question answered: neither — with the quality leg
confirmed.** The parity gains are real, but no parity gain can
justify the cost in deployment terms: the wire is strictly
dominated by the prose, bigger every session forever. The rebuild
proved the native D-item form is the highest-fidelity mechanism
carrier measured AND that unconstrained native richness is
incompatible with compression. CCC-2 is an enrichment/annotation
format wearing a codec's telomeres — not a compression codec.
**Triadic reading:** (1) claim confirmed on quality, eliminated on
economics; (2) polar opposite (v7/R5 stands as the codec)
confirmed — charter kill criterion fires on the economics leg; the
rebuild overshot rather than converged, so the weaker validation
holds: D-item shape = right shape for carriage, v7 terseness =
right size for compression, different objectives; (3) null: ledger
+1 (D23).
**Backward touch:** CCC2-1/2/3 — the 2.78× flag is now a verdict
(1.437× prose); open design question (compression discipline vs
declared annotation role), not a patch. v1 Node 21 / M4 base:
R5's numbers stand; sharpening — the mechanism frontier is not
exhausted at 0.906 (CCC-2: 0.983) but further gains live off the
compression curve; R5 remains the best measured
compression-quality point. This prices M4's alternatives without
moving the decision.
**Status:** GATE COMPLETE. v7/R5 stands as the codec; D-wire
validated as high-fidelity annotation format. Full report:
`ccc2/PARITY_REPORT.md`.
**Methodology layer:**
- Labels: parity 9.75 / per-class / cost table / within-scorer
  deltas — **computationally verified**; cross-battery absolute —
  verified numbers with the stated between-scorer caveat;
  "wire effect genuine" — **computationally verified** via the
  strict-scorer control; "never breaks even" — **computationally
  verified** (token counts, 12/12 negative savings).
- Fork: claim (CCC-2 profile) / polar opposite (v7/R5 as the bar
  it must beat) / null (ledger alone). The opposite leg is
  load-bearing: without the R5 controls this reads "9.75, great";
  with them it reads "9.75 on quality, disqualified on economics."
- Why it ends here: all four charter benchmarks adjudicated; the
  central question answered; kill criterion fired and recorded.
- Its own chain: LEDGER.md D23 (the dead end with its mechanism);
  the open design question (compression discipline for any future
  native format); the M4 decision, now with priced alternatives.
