# ATLAS-9 REPORT — the market atlas

**Date:** 2026-10-07/08 · **Coordinator:** Atlas-9 subagent
**Skies:** tape (43 concepts) · fundamentals (126) · narrative (48) — 217 nodes after 8 reviewed merges
**Standing:** this is a MAPPING RUN, not investment advice. Nothing in it recommends any position.

---

## Verdict (first)

**INTERWEAVE — but split, not merged.** Unlike Atlas-2..7, where the
skies barely touch, the market's three skies interleave: **9
adjudicated cross-sky links, every one a split_link, zero merges.**
The shared object is information→prices, approached from three
epistemic roles the instrument refused to collapse:

- the fundamentals sky *proves* a phenomenon (earnings announcements
  trigger jumps; >90% jump probability) at tick resolution with causal
  attribution in its own sample;
- the tape sky *measures* the same phenomenon in the fixed window
  (1.88× mean |return|, 1.51–2.04× volume on 23 verified earnings
  dates) with no attribution of its own;
- the narrative sky *documents associations* (news sentiment moves
  prices, pre/post disclosure) it cannot re-measure, and the tape
  measures large moves it cannot attribute.

The tape is an executable ground truth, not a clean one. 3 of 4 crack
candidates verify against it; 0 are refuted; 1 is honestly undecidable
(no news dates in the tape universe, so news attribution is untestable
by this instrument). The thinnest pair is tape↔narrative (1 link, 2
misses) — the wall there is not disagreement but *incommensurable
measurement*: the tape has no news dates, the paper has no tick tape.

The walls that exist are about *attribution and granularity*, not
about the phenomena: the phenomena (jumps on news, volume spikes,
cross-firm transmission, post-event adjustment) are shared; the
epistemic roles never coincide. The most load-bearing finding is
A9-11: both text skies ask *how information enters prices* and give
opposite answers — fast public impounding (fundamentals) vs slow
private diffusion (narrative). The instrument surfaces the tension;
it does not resolve it.

---

## Metrics

| Metric | Value |
|---|---|
| Concepts (post-merge) | 217 (tape 43 / fund 126 / narr 48) |
| Statuses | computationally_verified 127 · exact 55 · conjectural 21 · heuristic 14 |
| Within-sky edges | 196 |
| Reviewed merges | 8 (0 false merges; bar met) |
| Contradictions | 0 (bar met) |
| Adjudications | 14: 9 split_link · 3 rejected · 2 misses |
| tape↔fundamentals | 4 split / 2 rejected |
| tape↔narrative | 1 split / 1 rejected / 2 misses |
| fundamentals↔narrative | 4 split |
| Controls | C1 RESOLVED (verified) · C2 RESOLVED weakly (caveat) |
| Crack candidates | 4: 3 verified ✅ · 0 refuted · 1 undecidable ❓ |
| Drops | 2 (Stooq: JS wall; Yahoo: policy block) — recorded in manifest.json |

**Controls.** C1 (earnings-announcement price response): resolved —
split_link A9-01, verified by `verification/verify_k9_1_earnings.py`
(23 Nasdaq-verified earnings dates: 1.88× mean |return|, 27% of
earnings-window days in the top |return| decile vs 10% baseline).
C2 (news-event price impact): resolved weakly — split_link A9-06 with
the recorded caveat that the tape contains no news dates, so
attribution cannot be tested; the shared phenomenon
(event-concentrated large moves) is what resolves. A weak resolution
is reported as weak, not as a pass.

**Cracks (CRACK_LIST.md).** K9-1 earnings-window elevation ✅ ·
K9-2 volume-spike next-day structure ✅ · K9-3 overnight gap-fill /
overnight-vs-intraday decomposition ✅ (NVDA's entire 2-year drift
came overnight: +0.848 vs −0.169 intraday — a window fact neither
text sky states) · K9-4 tail-date news attribution ❓ undecidable.

---

## Honest limits

1. **Pilot scale.** One paper per text sky, 9 series, one 2-year
   window. The window contains a genuine stress episode (SP500
   −18.9% drawdown Feb–Apr 2025, VIX 52.33 on 2026-04-08), which is
   good for structure but means nothing here generalizes.
2. **Data availability.** Stooq and Yahoo both dropped (BK2011);
   the universe is what FRED + the Nasdaq API actually served.
   Daily bars only — the paper's tick-level phenomena (jump tests,
   5-minute price discovery) cannot be re-measured, only
   coarse-grained.
3. **Attribution asymmetry.** The tape measures without attributing;
   the text skies attribute without re-measuring. This is why C2 is
   weak and K9-4 undecidable — a structural property of the design,
   not a bug to tune away.
4. **Mechanical candidates were noisy.** Token overlap collapsed
   same-procedure-different-series pairs (tape) and procedure
   vocabulary (the P1-P8 method node matched everything). Semantic
   review did the real work; the merge script is a candidate
   generator, not an adjudicator.
5. **Every "holds" below means "holds in the fixed window,"**
   never "true of markets." Verification labels are window-bound
   by charter.

---

## Grade of the quantitative-sky adaptation (the instrument under test)

| Component | Grade | Basis |
|---|---|---|
| Pre-registered procedures (before data) | **A** | P1–P8 written before any values seen; no changes after; produced 43 neutral concepts |
| Blind quantitative drafters | **A−** | Neutral vocabulary held; every number computed, not asserted; one drafter's edge honestly did not fire |
| C1 control | **A** | Resolved and verified with independently-obtained earnings dates |
| C2 control | **C+** | Resolved only weakly; the tape universe structurally lacks news dates |
| Crack hunt vs the tape | **A−** | 3/4 verify, 0 refuted, 1 honestly undecidable; rerunnable scripts + captured outputs |
| Merge/adjudication | **B+** | Rules held (0 false merges, 0 contradictions), but mechanical candidates needed heavy manual review |
| **Overall** | **B+/A−** | **The adaptation is viable and produced genuine verified cracks. The load-bearing limitation is attribution: a tape sky without event dates can measure structure but cannot meet a causal sky halfway. Pre-registration + blind drafters + verify-against-tape is a sound pipeline; the next run should include event dates (earnings/news calendars) in the tape universe from the start.** |

---

## Cost (per phase, ESTIMATE — reconstructed, 1.3× words→tokens)

| Phase | Est. tokens |
|---|---|
| Data-availability probes (BK2011) | ~10k |
| Corpus selection + live ID verification | ~8k |
| Pre-registration (tape_procedures.md) | ~7k |
| Data download + manifest | ~5k |
| Text download + chunking | ~4k |
| Drafters (14 subagents) | ~52k |
| Merge + adjudication | ~33k |
| Controls + crack verification | ~30k |
| Illustration (money PNG + HTML) | ~8k |
| Report + grading packet | ~13k |
| **Total** | **~170k** |

**Extrapolation:** a full-scale run (2 papers/sky, 15–20 names, event
dates in the universe) ≈ 2.5–3× this pilot, ~450–500k tokens
ESTIMATE. The drafter phase dominates (~30%); it parallelizes.

---

## Deliverables

- `manifest.json` — per-series provenance + drops with routes tried
- `tape_procedures.md` — pre-registered extraction procedures
- `extractions/` — 14 blind extractions (validated)
- `merge_atlas9.py`, `adjudicate_atlas9.py`, `atlas9_adjudications.json`
- `CRACK_LIST.md` + `verification/` (3 rerunnable scripts + captured outputs)
- `atlas9_money.png` · `atlas9_interactive.html`
- `grading_packet.md` — sampled triples + ALL adjudications + ALL merges
- `ATLAS9_REPORT.md` — this file
