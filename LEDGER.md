# CCC Dead-End Ledger

**Purpose.** Every path this project closed, with the mechanism of
its failure and what it became. Dead ends to avoid are as valuable
as open avenues — this ledger exists so no future work (human or
agent) re-tries what the tree already killed, and so each killed
path's transfer is explicit.

**Rule.** A dead end is never deleted from this ledger. If a dead
end is ever re-opened, the re-opening is recorded here with its new
evidence — the original entry stands.

**Labels** follow the project's epistemic vocabulary: exact theorem /
computationally verified / conjectural / heuristic.

---

## D1. Zero-cost symbols (Node 1, 2026-09-27)
- **Tried:** universally zero-cost symbols in cl100k_base — zero-width
  chars, BOM, combining marks.
- **Failure mechanism:** all cost 1–2 tokens. Invisible ≠ free.
  [computationally verified]
- **Transfer:** zero *marginal* cost via BPE absorption
  (context-dependent) — the salvageable half of the idea.

## D2. Color channel on the text path (Node 1, 2026-09-27)
- **Tried:** omitting zeros/spaces via color (user idea).
- **Failure mechanism:** capacity zero on the text channel; the image
  path costs more than it saves. [computationally verified]
- **Transfer:** reborn as a separate thread — fiber WDM × polarization
  design. The vision survives; the text-channel formalization doesn't.

## D3. Model-as-parser, unaided (Node 3, 2026-09-28)
- **Tried:** the model decodes the wire itself (73 triples, 25 gamma
  ops, factoring 2.2e16, 73-term checksum; 1478-token spec).
- **Failure mechanism:** decisive Test A — DECODE_SPEC.md is complete
  (independent spec-only decoder reproduces the reference exactly),
  but the mechanical burden makes it implausible at scale and
  vulnerable to silent arithmetic errors. [computationally verified;
  the scale judgment is heuristic]
- **Transfer:** harness-parses adopted (product = harness + codec,
  never codec alone). Node 11 narrowed the closure: rejection covers
  *unaided* arithmetic only — tool-assisted orchestration passes 12/12.

## D4. Statistical second-stage compression (Node 4, 2026-09-27)
- **Tried:** Huffman / LZ77 / stacked statistical stages on top of the
  wire.
- **Failure mechanism:** all lose (0.63–0.98x); codebook/flag overhead
  exceeds savings at this granularity. [computationally verified]
- **Transfer:** the standing lesson — code the *structure*, not the
  statistics (adopted: cursor layer, 1.32x, 300/300 fuzz round-trips).

## D5. Checksum-free disambiguation (Node 5, 2026-09-27)
- **Tried:** resolving duplicate-index ambiguity without the per-line
  header checksum.
- **Failure mechanism:** PROVABLY unresolvable; attempted
  disambiguation picked wrong 50% of the time. [exact theorem]
- **Transfer:** the per-line header checksum is load-bearing — it
  stays through v6/v7.

## D6. Prime-wavelength video claim, as stated (Node 6, 2026-09-27)
- **Tried:** prime-spaced channels avoid interference (user's vision).
- **Failure mechanism:** crest tracks bandwidth, not primality; prime
  sets ≈ random integer sets. [computationally verified]
- **Transfer:** the refined claim (incommensurable spacing suppresses
  nonlinear mixing) is true — but Golomb rulers beat primes ~1.7x on
  FWM products. Forked to a separate hardware/communications thread.

## D7. Count-based chunking past B~300 (Node 8, 2026-09-28)
- **Tried:** `encode_lines_balanced` (weight-based chunking;
  count-based header).
- **Failure mechanism:** count-based overflows the 999-triple v3
  header past B~300 when strand products cluster at the message
  head — surfaced by measurement, not review.
  [computationally verified]
- **Transfer:** weight-based chunking fix.

## D8. The cost play (Node 9, 2026-09-28)
- **Tried:** selling CCC on cheaper tokens (9a).
- **Failure mechanism:** prompt caching captures ~10x on the
  repeated-context workload; CCC saves ~$0.03/session at Sept-2026
  prices. The cost argument died with caching.
  [computationally verified]
- **Transfer:** reframed to capacity + integrity (9b, under test) and
  research contribution (9c, open).

## D9. R2 design space: ≥9/10 parity AND ≤3 break-even (Node 10, 2026-10-03)
- **Tried:** getting both high parity and low cost from the R2
  extractor design.
- **Failure mechanism:** measured frontier — (9/10, 5.28) vs (~5/10,
  ~2). The combination does not exist in this design space.
  [computationally verified]
- **Transfer:** forced R3 — attack the omission taxonomy instead of
  the cost/parity trade-off directly.

## D10. "v5 wire gap = decode corruption" (Node 11, 2026-10-03)
- **Tried:** explaining the 7.42→6.79 injection-to-wire parity step as
  decode corruption.
- **Failure mechanism:** same locked probes both sides — the gap
  isolates to representation (v5 has no anchor-note channel), not
  decoding. [computationally verified]
- **Transfer:** v6 note channel (Node 13).

## D11. Exp2 Phase-A 1.00 precision claim (Node 12, 2026-10-03)
- **Tried:** claiming the adjudicator at precision 1.00 (0 false in
  79 proposed merges).
- **Failure mechanism:** dual-judge replication found shared ontology
  bias — judge 1 and the audit both waved through
  question+verdict, verdict+evidence, result+control as SAME.
  Corrected to 73/78 = 0.936 under strict principle P.
  [computationally verified]
- **Transfer:** the strict adjudication standard; principle P
  (posit ≠ resolution) as the adopted bar.

## D12. Registry-in-prompt architecture (Node 12, 2026-10-03)
- **Tried:** B1 — registry in the extraction prompt.
- **Failure mechanism:** 8 reuses — 4 true, 4 granularity-borderline,
  0 clean-false; merges 2× as aggressively with half debatable, at
  ~5.5k prompt tokens/extraction. Operating point doesn't clear the
  bar. [computationally verified]
- **Transfer:** post-hoc merge hook adopted (blind extraction kept);
  recall lever is retrieval density, not adjudicator strictness.

## D13. TF-IDF alone as merge rule (Node 12, 2026-10-03)
- **Tried:** using TF-IDF ranking directly as the merge decision.
- **Failure mechanism:** peaks at 0.875 — the adjudicator, not the
  ranker, earns the bar. [computationally verified]
- **Transfer:** TF-IDF stays candidate generation; LLM adjudication
  decides.

## D14. Notes as raw bits in the triplet channel (Node 13, 2026-10-03)
- **Tried:** v6 notes riding as raw bits in the triplet channel.
- **Failure mechanism:** BE_wire 3.21 — worse than the injection path.
  [computationally verified]
- **Transfer:** re-cut as literal NOTETEXT (text as text) — BE_wire
  2.36. The polar opposite that lost, on record.

## D15. Badge-weighted ranker fusion (Node 14, 2026-10-03)
- **Tried:** fusing paraphrase-invariant badges (arXiv IDs, formulas,
  distinctive numbers) into the retrieval ranker.
- **Failure mechanism:** RANKING NEGATIVE — naive fusion hurts
  (recall@1 0.667→0.569, 27 losses vs 5 wins).
  [computationally verified]
- **Transfer:** do NOT fuse; DO surface shared rare badges as explicit
  adjudicator evidence (precision lifts 5×/4×/6× — the scoped
  positive). Explanation: badges identify TOPIC, not ENTITY — blind
  to epistemic role, exactly principle P's distinction. [heuristic]

## D16. D_log resolution via badges alone (Node 14, 2026-10-03)
- **Tried:** solving the D_log coreference with badge signals.
- **Failure mechanism:** entity text lacks the badge; needed full-text
  evidence (as B1 showed). [computationally verified]
- **Transfer:** exact-identifier retrieval (arXiv/formula) + full-text
  evidence for near-matches.

## D17. Five-opcode process taxonomy (Node 15, 2026-10-03)
- **Tried:** ITER / PIPE / BRIDGE / INVERT / +1 as the process-symbol
  set.
- **Failure mechanism:** user's redirect + reduction test — only the
  full perturbation shape earns its keep; PIPE/BRIDGE score in the
  restatement band where literal text does as well.
  [computationally verified]
- **Transfer:** collapsed to ONE operator — PERTURB(seed, binary-op,
  axis).

## D18. Restatement-band processes as process-symbols (Node 15, 2026-10-03)
- **Tried:** encoding processes whose formula IS the content (E049
  duality: 0.93×).
- **Failure mechanism:** break even or lose — restatement processes
  don't compress; literal text does as well.
  [computationally verified]
- **Transfer:** PERTURB + literal text + status tags is the complete
  process-symbol design; everything else stays words.

## D19. PERTURB triple syntax as the encoding (Nodes 15–16, 2026-10-03)
- **Tried:** the invented PERTURB triple syntax (spec v1–v2.1).
- **Failure mechanism:** Node 16 showed the paperwork already had the
  shapes — the D-item syntax preserves everything v2.1 carried
  (round-4 blind test: 8/8 stages, 6/6 checksums, 5/5 probes) and
  adds checksums as drift detectors plus the honest boundary as a
  stop-line. The syntax was invented; the content was not.
  [computationally verified]
- **Transfer:** D-item encoding (M1); findings kept (premise-
  completeness law, 9 audit requirements, fidelity method).

## D20. v6 status enum collapse (Node 17, 2026-10-03)
- **Tried:** v6's status enum
  (unstated/hypothesized/asserted/verified/killed/superseded).
- **Failure mechanism:** collapses the sharpest distinction — exact
  (theorem/identity, proof carried) vs computationally verified
  (numeric check, scope stated) — into one "verified"; no room for
  genre ("classical theorem, reframed — not a new theorem").
  [computationally verified gap analysis]
- **Transfer:** v7 strength ordinal (0–6) + 2-bit genre anchor;
  lossy-conservative migration (legacy "verified"→verified-numeric,
  never exact — the codec may not conclude more than was
  established).

## D21. Cross-protocol absolute parity comparison (Node 19, 2026-10-04)
- **Tried:** comparing absolute parity scores across scorer
  strictnesses (6.79 vs 7.42 vs 6.00).
- **Failure mechanism:** scorer drift — systematic 1.0→0.5 threshold
  shift (42/50 original full marks downgraded; ones-rate 5.8% vs
  41.7%). Absolutes are not comparable; only within-protocol deltas
  are. [computationally verified]
- **Transfer:** locked probes + calibrated scorers + ones-rate
  calibration before any comparison.

## D22. Wire design as the parity lever (Node 20, 2026-10-04)
- **Tried:** further parity gains from wire/codec design.
- **Failure mechanism:** wire loss +0.00 measured both directions
  (7.46 wire = 7.46 injection). The codec is done losing parity —
  there is nothing left for wire design to gain.
  [computationally verified]
- **Transfer:** extraction quality (R5, Node 21) is the *only*
  remaining lever.

## D23. Native richness without compression discipline (CCC2-4, 2026-10-06)
- **Tried:** the CCC-2 rebuild — D-wire v1 derived natively from the
  paperwork's forms (D/G/V/B/C/L records, epistemic labels as first
  language, honest boundary as format field), no migrations.
- **Failure mechanism:** unconstrained native richness expanded past
  the source: 12/12 wires larger than their prose (1.004×–1.695×,
  mean 1.437×; 48,104 vs 33,474 tokens). Deployment break-even is
  undefined — the wire never pays for itself; each session costs
  more than reading the prose. The parity gate confirmed the
  quality leg (9.75/10, MECHANISM 0.983, 0 fabrication) and
  eliminated the economics leg. A codec that expands is not a
  codec. [computationally verified]
- **Transfer:** the D-wire is validated as a high-fidelity
  annotation/enrichment format, not a compression codec; v7/R5
  stands as the codec (charter kill criterion fired on economics).
  Any future native-format attempt needs a compression discipline
  (denser D-items, shorter boundaries, selective carriage) or must
  declare the annotation role upfront. The D-item SHAPE is the
  right shape for mechanism carriage; v7's terseness is the right
  size for compression — different objectives, different optima.

---

## Superseded designs (iterations, not failures)

Wire versions v1→v4 were each superseded on measured token cost
(v1 base-64 frames → v2 decimal triples → v3 Elias-gamma → v4
telomeres/multiline → v5 labels/typed edges). These were iterations,
not dead ends — each was the best known wire at its time. They are
listed here only so nobody mistakes "tried and replaced" for
"tried and failed."

---

*Ledger opened 2026-10-06. 23 entries. No entry is ever deleted;
re-openings are recorded beneath the original entry.*
