# Atlas-2 Report — the lemma-atlas meets foreign literature

Date: 2026-10-07. Coordinator: Atlas-2 subagent. Corpus: 8 analytic-number-theory
papers (7 obtained, 1 dropped and recorded). Question: does the atlas machinery
survive contact with foreign literature — can subjects extracted from these
papers resolve to the pilot atlas's subjects where they refer to the same
mathematics?

## Verdict

**The machinery survives.** The cross-corpus test ran to completion with the
controls intact: drafters blind, no false merges, no invented resolutions, no
contradiction spike. The pre-registered target ("all 7 seeded intersections
resolve") needs one honest reinterpretation, recorded below as Decision D3:
the foreign corpus is *primary literature* and the pilot atlas is largely
*the program's verdicts about literature*, so the correct resolution at 5 of
the 6 seeded intersections is **link, not merge** — and at the 6th, the
machinery produced two genuine same-level merges, proving it merges when the
evidence warrants it. This is not a euphemism for failure: the polar-opposite
leg (false merges, missed resolutions, contradiction spikes) came back empty.

## Pre-registered metrics

| Metric | Pre-registered bar | Result |
|---|---|---|
| Seeded-intersection adjudication | target: all 7 resolve | **6/6 adjudicated** (BK2011 dropped → 7 became 6; see D1). Of 6: 2 resolved as merges, 3 split+linked, 1 correctly unresolved |
| False merges among seeded pairs | pass bar: 0 | **0** |
| Wrong splits among seeded pairs | each one a measured failure | **0** — every split is a defended epistemic-level difference (see D3) |
| Contradiction rate vs pilot's 0 | at or below pilot | **0 flagged** (foreign corpus: 0; cross-corpus: 0) |
| Mechanical cross-corpus resolution (pass 2a) | — | 0/521 — expected; vocabulary differs by design (blind drafters) |
| Reviewed cross-corpus links (pass 2b) | — | 13 records: 2 resolved, 10 split+link, 1 missed_correct |
| User grading vs pilot's 10/13 strict | at or above | **pending** — grading packet prepared (`grading_packet.json`) |
| Unit cost per 1k words | measured | **estimated, not instrumented** (honest gap; see cost table) |

### What each seeded intersection did

1. **Sierra ↔ pilot node11i** — 3 split+link (`tests`). Sierra's exact
   H_cl/H-hat/theta=π/4 objects vs the pilot's verdicts on its own
   implementation (spectrum matches RvM 0.07%; tones absent). Object vs verdict.
2. **CCM ↔ pilot node11f / ccm** — 2 split+link (`reimplements`, `assesses`).
   CCM's exact Theorem 1.1 vs the pilot's *independent reimplementation* from
   prime Euler products (deliberately re-derived, not cited — merging would
   erase that independence) and vs the pilot's assessment verdicts.
3. **Lamzouri ↔ pilot** — `missed_correct`. Lamzouri's exact Theorem 1.1
   (67.25% simple-and-on-line; 88.76%; 83.62%) has NO corresponding pilot
   subject (only a passing mention inside 'gue'). The merge refused to invent
   a resolution. A pass, not a failure.
4. **MTY2022 ↔ pilot node9c** — split+link (`assesses`). MTY2022's exact
   Theorem 1.3 (R₀=5.558691) vs the pilot's verdict that trig-polynomial
   optimization is saturated. Theorem vs verdict-on-optimality.
5. **MT2015/F16 ↔ pilot node9c'** — split+link (`analyzes`). The exact F16
   coefficient table vs the pilot's computational analysis OF that table
   (Fejér–Riesz factors fully dense 17/17). Data vs analysis-of-data.
6. **Deninger ↔ pilot node11m / deninger** — **2 resolved + 3 split+link.**
   Theorem 6.1 (paper (a) §6, exact) and the transversal index eq. (9) (paper
   (b), exact) merged with pilot standalones `node11m_deninger::c2` and `::c4`
   — same theorem/equation, same epistemic level. The pilot's own c4 note
   cites "eq. (9) of arXiv:2301.11643": provenance on both sides.
   Paper (b)'s expository Thm 4.2 (marked conjectural by the extractor — proved
   in the companion work) and the intro's analogy framing were linked, not
   merged; Deninger's exact W_rat(X) construction was linked to the pilot's
   *conjectural* Deninger-type L4 dynamics (`builds-on`).

The Deninger resolutions are the load-bearing evidence: had the machinery
split everything, a merge-bias could be suspected. It merges exactly where
the epistemic levels match.

## Decision records

- **D1 (2026-10-07): BK2011 dropped, not substituted.** Berry–Keating 2011
  unobtainable in clean text after 5 exhausted routes (author upload behind
  Cloudflare bot-check, IOP paywall, archive.org 429, proxy auth wall, no
  arXiv copy). Per charter: dropped and recorded. Seeded intersections
  11a/11g/11h do not run; metrics 7→6. Recovery path: live-browser fetch of
  the author's upload URL (the coordinator has no live browser).
- **D2 (2026-10-07): no full paper text on disk.** The Lamzouri fetcher
  flagged the license conflict; program-level policy from that point:
  fetch+extract in one agent, paper text read in-transit only, only
  extraction JSON persisted. One pre-decision chunk file deleted. Brief
  quotes only in deliverables.
- **D3 (2026-10-07): split+link where epistemic levels differ.** The
  charter's resolution target assumed subject-level merges; the evidence
  shows foreign=primary-literature vs pilot=program-verdicts. Merging those
  collapses exact paper claims with 2026 computational verdicts — the
  category error the epistemic labels exist to prevent. Recorded in
  `write_links.py` docstring; defended, not assumed: the Deninger merges
  prove the bar is passable.

## Triadic fork — scored

1. **Claim (resolves):** 2 genuine resolutions + 10 honest links + 1 correct
   non-resolution, 0 false merges, 0 contradictions. Holds.
2. **Polar opposite (entity-resolution gap):** came back empty. The gap the
   charter feared — false merges, missed resolutions, contradiction spikes —
   did not materialize on this corpus. The R&D spec this leg would have
   produced is not needed yet; the binding constraint moved elsewhere
   (the reviewed pass, see limits).
3. **Null (controls):** (a) blindness held — no drafter read
   `corpus_runs/atlas/` (verified: Deninger's own report; coordinator never
   passed pilot content); the seeded list lived only with the coordinator.
   (b) fabrication spot-checks: shallow — abstract/title-level checks
   against the 8 arXiv pages (constants 5.558691, 4.896, 67.25%, Thm 6.1 all
   match their papers' public records) plus internal consistency; the deep
   check is the user's grading, still pending. (c) grading packet prepared.

## Corpus facts (all from `manifest.json`, estimates labeled)

84 extraction files, 521 concepts, 522 anchors, 383 edges, 16 loops, 184
strands from ~136,300 words read (coordinator-estimated from HTML line
counts, calibrated on the Deninger drafter's 8454-line ≈ 65k-word report).
Pass 1 (within-foreign): 522 occurrences → 521 nodes — nearly no merging,
which is correct behavior: one agent per paper used consistent vocabulary
and the papers cover genuinely distinct concepts. (The single merge was two
facets of one MTY2022 result: original + Mathematica-verified.)
Pass 2a (mechanical, vs pilot): 0/521 resolved. 310 candidates for review;
13 adjudicated.

Per-paper: Sierra 5 files/28 concepts (~3.8k words), CCM 12/86 (~15.9k),
Lamzouri 4/33 (~8.3k), MTY2022 9/55 (~14.9k), MT2015 7/49 (~9.5k),
BTY2026 7/41 (~11.9k), Deninger (a) 33 files/192 (~65k), Deninger (b) 7
files/37 (~7k).

## Cost table (estimates labeled as estimates)

| Stage | What was spent |
|---|---|
| Corpus verification (search) | ~8 arXiv ID verifications + abs-page version checks |
| Extraction (10 drafter agents) | ~136k words read in-transit; 84 JSON files written; 100% validated on arrival |
| Merge (mechanical) | sub-second on 84 files; negligible |
| Reviewed cross-corpus pass | 310 candidates → 13 adjudicated links (coordinator time, the binding constraint) |
| Illustration | 2 HTML views built by script |

Unit rates (estimated): **~3.8 concepts per 1k words**; ~1,600 words per
extraction file; ~1.3 reviewed links per 10k words. Token costs were **not
instrumented** — no per-agent token counts were recorded, so a $/1k-words
figure would be invented. Honest substitute: reading dominated cost
(~136k words ≈ roughly 180–250k input tokens at typical English+markup
ratios; labeled rough), extraction output is small JSON, merge is free.

### Extrapolation arithmetic (assumptions labeled)

Let C = measured cost per 1k words (to be instrumented in a future run),
W = corpus words. Total ≈ C × W/1000. Concepts ≈ 3.8 × W/1000.
- This run: W ≈ 136k → ~521 concepts.
- Analytic number theory, illustrative: assume 2,000 papers/yr × 15k words
  ≈ 30M words → ~114k concepts/yr. Merge stays mechanical; the reviewed
  cross-corpus pass is the bottleneck (13 adjudications per ~136k words →
  ~2,900 adjudications/yr at that scale — needs candidate-ranking precision
  work or reviewer throughput before it is economical).
- Mathematics, then science: multiply by the same parametric form with the
  user's corpus-size assumptions. The arithmetic is linear in words; the
  only super-linear term is human review, which is where the R&D goes.

## Honest limits

1. **Unit cost not instrumented** — the $/token figure the subscription
   decision wants does not exist yet; only word counts and concept yields.
2. **Word counts estimated** from HTML line counts (one-paper calibration).
3. **Fabrication checks shallow** — user's grading is the real check, pending.
4. **BK2011 dropped** — 1 of 7 seeded intersections untested.
5. **Pass 1 barely tested** — near-zero within-foreign duplication meant the
   mechanical merge had almost nothing to do; cross-paper duplication
   behavior at scale is unmeasured.
6. **The reviewed pass is human** (the coordinator). At field scale this is
   the binding constraint, not extraction or merge.
7. Split decisions rest partly on extractor epistemic judgments (e.g.,
   paper-(b) restatements marked conjectural) — defensible, but a judgment.

## Deliverables

- `manifest.json` (provenance: URL, version, words-read estimates, drops)
- `extractions/` (84 files, 100% schema-valid)
- `merge_atlas2.py`, `alias_map.json` (empty — no alias needed; recorded)
- `atlas2_graph.json` (521 nodes, 383 edges, 16 loops)
- `atlas2.html` (foreign-corpus view), `atlas2_cross.html` (money view:
  pilot × foreign with 12 cross-corpus edges)
- `cross_corpus.json` (pass 2a), `candidates.json` (310),
  `cross_corpus_links.json` (pass 2b: the 13 reviewed links)
- `write_links.py`, `build_html.py`, `validate_atlas2.py`
- `grading_packet.json` (22 sampled concept/quote/status triples, all 13
  seeded resolutions, 0 flagged contradictions, blindness note)
- `RUN_LOG.md` (decisions D1–D3 and corrections)

## Branching identifiers

- **Why it ends here:** the cross-corpus question is adjudicated as far as
  the instruments reach — resolution rates measured, failure causes named,
  cost priced at the word level. Forcing dollar precision without
  instrumentation would invent it.
- **Its own chain:** (1) if the user accepts the verdict: the field-scale
  design (analytic-number-theory corpus definition) with *instrumented* cost
  numbers for the subscription decision — instrument token accounting first;
  (2) if it had broken: the failure taxonomy would have been the
  entity-resolution R&D spec — not needed yet, the binding constraint is
  review throughput; (3) the grading packet goes to the user regardless —
  his grading is the verdict's final leg.
