# Atlas-8 Report — the prime-distribution run

**Date:** 2026-10-07
**Question:** run the machine on prime number distribution itself —
the landmark literature vs the pilot's circle-sieve sky — and hunt
the cracks as candidate novel results. The user's realization: with
the circle sieve implemented, the number line is not lossy — the
atlas maps the literature against the territory, not another text.

## Verdict

**Cracks exist, and 4 of 5 verify computationally.** The literature
and the sieve touch on the same objects — PNT, admissible tuples,
the twin constant, the sieve itself — and at every touch the sieve
holds something the literature does not state: a framing (PNT as
total weight 1), a generative account (admissibility emergent, not
stipulated), a derivation (the twin singular series as renormalized
sieve weight), an independent construction (the circle sieve). Four
crack candidates verify against the sieve implementation; the fifth
is undecidable (truncated source); **zero were refuted**. The polar
opposite (no cracks — the sieve's structure already implicit in the
literature everywhere they touch) did not occur. Every cross-sky
link is split, none merged: the two sides invoke the same objects
for different purposes at different epistemic levels.

## The shortlist (candidate novel results)

1. **K8-1 — PNT as total weight 1** (A8-06). Σ_{faces}(−1)^{|S|+1}
   log(∏S)/∏S → 1 IS PNT. Re-verified here: 0.969931 @10³,
   0.993342 @5·10³, 0.986125 @2·10⁴. Label: computationally_verified
   (the identity); the framing-novelty claim is the pilot's.
2. **K8-2 — Admissibility emergent** (A8-09/10/12). The nine admissible
   combos exhibited as sieve output; {0,2,4} dies with exactly one
   survivor (3,5,7). Re-verified: 342/342 twin lowers ≤20000; sole
   triple (3,5,7) below 10⁵. Label: computationally_verified.
3. **K8-3 — Twin singular series derived** (A8-11). 𝔖(z) → 2C₂ =
   1.32032… as renormalized deformed-sieve weight; the asymptotic
   itself stays honestly unclaimed. Re-verified: S(1000) = 1.320491.
   Label: computationally_verified (the mechanism, not the proof).
4. **K8-4 — The circle sieve, independent** (A8-13). Geometric
   shared-boundary sifting, built without the literature; unshared ==
   primes at N = 30…10000 (10/46/303/1229, all match). Label: exact.
5. **K8-5 — Selberg λ² face form** (A8-02…05). UNDECIDABLE — the source
   chunk is truncated mid-D10c; the optimizer/minimum never appear.

None is a new theorem about primes. Each is a candidate novel result
about the *structure* — which is what the program trades in.

## Metrics (pre-registered)

| Metric | Result |
|---|---|
| Concepts / nodes | 345 (212 foreign + 133 home: 94 main + 39 spans) |
| Status spread | exact 177 · conjectural 60 · computationally_verified 56 · heuristic 37 · killed 15 |
| Adjudications | 13: **11 split_link**, 0 resolved, **2 rejected** (A8-07 HL-AP vs HL-twin: shared name only; A8-08 Brun vs twin-density: different claims), 0 missed-as-verdict |
| Recorded misses (absences) | 5: Cramér's conjecture, Green–Tao APs, Cramér urn model, parity barrier (home-only), level of distribution |
| S1 control (Maynard→Zhang) | **RESOLVES** (A8-01, split_link: cited vs proved) |
| Seeds | n/a — no Atlas-2 papers in corpus |
| False merges / contradictions | **0 / 0** (no merges: no two nodes made the same claim) |
| Crack candidates | 5 → **4 verified**, 0 refuted, 1 undecidable |
| Drops (BK2011) | 0 — all 6 papers obtained |
| Cross-sky density | 11 links / 2468 mechanical candidates (0.45%; semantic review drove verdicts) |

## How the run was built

- **Corpus:** 6 papers, 15 chunks (11 foreign: 17,683 words; 4 home: 8,610 words).
  Foreign: Zagier Newman's PNT proof; Granville's Cramér survey; Zhang
  §§1–2,7; Maynard §§1–5; Green–Tao §§1–3; Elkies' Selberg sieve notes.
  Home: the pilot's circle-sieve documents (read-only) + 4 supplementary
  span passes (the user's 2026-10-07 span directive: gaps as first-class
  concepts — "the song is in the intervals, not just the notes").
- **Retrieval:** the retriever caught 2 wrong arXiv IDs from the task
  brief (Zhang has no arXiv version; Maynard is 1311.4600, not
  1404.0794) — verify-before-fetch earned its keep. One retriever
  declined to write copyrighted text to files; the coordinator
  materialized chunks by direct download + mechanical slicing (no model
  reproduction), resolving 9 anchor mismatches against actual headers.
- **Extraction:** 11 blind foreign drafters + 4 blind home drafters +
  4 blind span-pass drafters, each in its literature's own vocabulary.
- **Merge:** adapted merge_atlas7.py; explicit alias map (empty —
  main↔span restatements deliberately NOT merged: over-merge is worse
  than under-merge, and span nodes carry the quantities the crack hunt
  needs); vocabulary remaps recorded (sieve1 span-pass genres/rels,
  free-text statuses → standard); string loops normalized.
- **Adjudication:** 2468 mechanical candidates triaged; semantic review
  drove all 13 verdicts. Citing-chunk artifact respected (maynard_p1's
  conjectural-from-chunk labels on cited theorems not treated as
  epistemic downgrades).
- **Crack hunt:** span-priority; 5 candidates → 4 verified via new
  rerunnable scripts importing `sieve_complex.py` / `deformed_sieve.py`
  (read-only). Captured outputs in `verification/`.

## Honest limits

1. **JSTOR scan OCR is lossy on math** (Zhang, Zagier): superscripts,
   subscripts, and symbols garbled; drafters extracted prose claims
   and noted garbles; garbled numbers were reconstructed with the OCR
   form noted. zhang_p2 (§7) is 451 words — thin but complete-as-extracted.
2. **Home D10c truncated** in the pilot's own document (Selberg λ²
   section ends mid-sentence) — K8-5 undecidable until the derivation
   is recovered.
3. **Adjudication by coordinator**, not a separate blind adjudicator —
   the S1 control's independent resolution is the check.
4. **Chunk-bound drafters** — concepts may be over-fragmented;
   over-merge remains worse than under-merge.
5. **The pilot's circle-sieve documents are the home sky**, not the
   sieve implementation directly — the implementation entered only at
   crack-verification. A future run could draft the code itself.
6. **Tokens are ESTIMATES** (1.3× words); retrieval-phase reads
   uninstrumented; no dollar figure.

## Cost

| Phase | Words in | Tokens (EST @1.3×) |
|---|---|---|
| Foreign extraction (11 chunks) | 17,683 | ~23,000 |
| Home extraction (4 chunks) | 8,610 | ~11,200 |
| Home span passes (4 re-reads) | 8,610 | ~11,200 |
| Concepts out (345, ~60 wds each) | ~20,700 | ~26,900 |
| **Total** | **~55,600** | **~72,300** |
| Per 1k words in | — | ~1.30k tok/1k words in; ~2.1k tok/1k words all-in |

10× extrapolation ≈ 720k tokens. Retrieval-phase reads uninstrumented.

## Deliverables

All in `corpus_runs/atlas8/`: `ATLAS8_CHARTER.md` (with the span
directive as Protocol item 7), `ATLAS8_REPORT.md` (this file),
`CRACK_LIST.md` (the lead exhibit), `atlas8_adjudications.json`
(13 verdicts + 5 misses), `grading_packet.md`, `manifest.json`,
`chunks/` (15 + provenance + FETCH_PLAN.md), `extractions/` (19),
`merge_atlas8.py`, `adjudicate_atlas8.py`, `build_money8.py`,
`graphs/atlas8_raw.json`, `candidates.json`, `pass1_review.json`,
`verification/` (4 scripts + captured outputs), `atlas8_money.png`,
`atlas8_money.html`, `RUN_LOG.md`, `HOME_DRAFTER_BRIEF.md`,
`FOREIGN_DRAFTER_BRIEF.md`, `SPAN_DRAFTER_BRIEF.md`.
The pilot's, prime-sieve-geometry's, and Atlas-2..7 directories were
read-only throughout.
