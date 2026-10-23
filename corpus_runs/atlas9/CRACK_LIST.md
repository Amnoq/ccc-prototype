# Atlas-9 Crack List — candidate findings

**Date:** 2026-10-07
**Question asked of every adjudicated link:** does the other sky state
what this sky holds? Every unstated touch is a crack candidate.
**Standing caveat (charter):** verification here means "holds in the
fixed window (2024-10-01–2026-10-01)," NEVER "true of markets."
**Standing:** this is a mapping run, NOT investment advice. Nothing
here recommends any position.

---

## K9-1 — Earnings-window elevation (from A9-01) ✅ VERIFIED

- **Fundamentals claim:** earnings announcements trigger price jumps
  (>90% jump probability in after-hours sessions with announcements;
  volume explodes on announcement days). Paper's own 12-year tick sample.
- **Tape structure it touches:** P3/P7-level measurement on 23
  Nasdaq-verified earnings dates (AAPL/MSFT/NVDA × 8 quarters):
  mean |log-return| 1.88× baseline (AAPL 1.41×, MSFT 3.34×,
  NVDA 1.35×); volume 1.51–2.04× baseline; 27% of earnings-window
  days in the top decile of |return| vs 10% baseline.
- **What is unstated:** the paper proves the phenomenon in its own
  sample; it does not state these window-specific magnitudes, and
  the tape holds them without any causal attribution of its own.
- **Epistemic label:** computationally_verified (holds in fixed window).
- **Verification:** `verification/verify_k9_1_earnings.py`
  → `verify_k9_1_earnings_output.txt`. **VERIFIED.**

## K9-2 — Volume-spike next-day structure (from A9-02) ✅ VERIFIED

- **Fundamentals claim:** "tale of two markets" — volume explodes on
  earnings-announcement days (attributed).
- **Tape structure it touches:** P3 structural spike anatomy, no
  attribution: corr(volume, |return|) = 0.600/0.635/0.628
  (AAPL/MSFT/NVDA); 25/27/8 spikes (>2× trailing-20d median);
  mean next-day return after spikes: AAPL +0.75%, MSFT +0.38%,
  NVDA −1.82% vs unconditional +0.08%/+0.04%/+0.14%.
- **What is unstated:** the paper attributes volume explosions to
  announcements; it does not state the spike next-day return
  structure, which differs by name (NVDA's negative post-spike
  drift is a window fact the paper's sample cannot speak to).
- **Epistemic label:** computationally_verified (holds in fixed window).
- **Verification:** `verification/verify_k9_2_volume.py`
  → `verify_k9_2_volume_output.txt`. **VERIFIED.**

## K9-3 — Overnight gap-fill and overnight/intraday decomposition (from A9-04) ✅ VERIFIED

- **Fundamentals claim:** price discovery is very fast (~70% within
  5 minutes, WPC) — measured intraday at tick resolution.
- **Tape structure it touches:** P4 daily gap anatomy: |gap|>1% on
  81/107/237 days (AAPL/MSFT/NVDA) with fill rates 0.56/0.56/0.50;
  total log-return decomposition — AAPL overnight −0.243 vs
  intraday +0.621; MSFT +0.026 vs +0.172; NVDA overnight +0.848
  vs intraday −0.169 (NVDA's entire 2-year drift came overnight).
- **What is unstated:** the paper's discovery measure is intraday;
  it does not state the daily overnight/intraday split, and
  NVDA's overnight-dominated drift is a structural fact about the
  window that neither text sky contains.
- **Epistemic label:** computationally_verified (holds in fixed window).
- **Verification:** `verification/verify_k9_3_gaps.py`
  → `verify_k9_3_gaps_output.txt`. **VERIFIED.**

## K9-4 — Tail-date / news attribution (from A9-06) ❓ UNDECIDABLE

- **Narrative claim:** news sentiment moves prices with documented
  pre/post disclosure associations (FinBERT, 2003–2016 global sample).
- **Tape structure it touches:** P7 tail structure — large single-day
  moves occur and cluster on specific dates in the fixed window.
- **What is unstated / missing:** attributing the tape's specific
  tail dates to news would require news dates in the window, which
  the tape universe does not contain. The shared phenomenon
  (event-concentrated large moves) is adjudicated as a split_link;
  the attribution half cannot be tested by this instrument.
- **Epistemic label:** heuristic (undecidable-by-this-instrument).
- **Verification:** none possible — recorded, not forced.

---

## Summary

| Crack | Other sky states it? | Label | Verification |
|---|---|---|---|
| K9-1 earnings-window elevation | No (magnitudes) | computationally_verified | ✅ verified |
| K9-2 volume-spike next-day structure | No | computationally_verified | ✅ verified |
| K9-3 overnight gap-fill / decomposition | No | computationally_verified | ✅ verified |
| K9-4 tail-date news attribution | — | heuristic | ❓ undecidable |

**3 of 4 crack candidates verify against the tape. 0 refuted.**
Every verified crack is a window fact — a structural measurement the
text skies do not contain — not a claim about markets in general and
not investment advice. The tape is an executable ground truth, not a
clean one: noisy, adversarial, non-stationary.
