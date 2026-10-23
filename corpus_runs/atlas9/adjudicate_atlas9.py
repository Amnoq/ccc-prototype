#!/usr/bin/env python3
"""Atlas-9 adjudication: reviewed verdicts for cross-sky candidates.
Verdicts: split_link (shared referent, different roles — D3) /
rejected (with reason) / miss (no counterpart). Never invent a resolution."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
g = json.load(open(os.path.join(BASE, 'graphs', 'atlas9_merged.json')))['nodes']

def lab(nid):
    n = g[nid]
    return n['label'][:90]

ADJ = [
 {
  "id": "A9-01", "verdict": "split_link", "control": "C1",
  "pair": "tape-fundamentals",
  "a": "fundamentals:fund_p1:jump-probability-exceeding-90-in-after-hours-session",
  "b": "tape:names:aapl-p3-daily-volume-vs-absolute-return-relation-and",
  "b_note": "representative P3 node; the verification used all three names",
  "relation": "shares-phenomenon",
  "role_difference": "fundamentals: proves the earnings-announcement jump phenomenon at tick resolution with causal attribution to announcements (paper's own 12-year sample); tape: measures 1.83x mean |return| and 1.53-1.86x volume on 23 Nasdaq-verified earnings dates in the fixed 2024-10/2026-10 window, without independent causal attribution",
  "reason": "C1 CONTROL: the paper's documented price response resolves against the tape. Verified: verification/verify_c1_earnings.py — 33% of earnings-window days in top decile of |return| vs 10% baseline.",
  "crack": "K9-1",
 },
 {
  "id": "A9-02", "verdict": "split_link", "control": None,
  "pair": "tape-fundamentals",
  "a": "fundamentals:fund_p1:after-hours-trading-activity-as-a-tale-of-two-market",
  "b": "tape:names:msft-p3-daily-volume-vs-absolute-return-relation-and",
  "b_note": "representative P3 node",
  "relation": "shares-object",
  "role_difference": "fundamentals: volume spikes attributed to earnings announcements (tale of two markets); tape: volume spikes defined structurally (>2x trailing-20d median) with volume-|return| correlation and spike next-day returns, no attribution",
  "reason": "Same object (trading-volume spike behavior), different epistemic roles.",
  "crack": "K9-2",
 },
 {
  "id": "A9-03", "verdict": "split_link", "control": None,
  "pair": "tape-fundamentals",
  "a": "fundamentals:fund_p16:apple-case-study-pre-averaged-realized-variance-spik",
  "b": "tape:indices:21-day-rolling-annualized-volatility-tercile-regime-",
  "relation": "shares-object",
  "role_difference": "fundamentals: realized variance measured event-conditionally (spikes on announcement days, Apple case); tape: realized volatility measured unconditionally as in-window tercile regimes with dated top-5 episodes",
  "reason": "Same object (realized volatility), different conditioning.",
  "crack": None,
 },
 {
  "id": "A9-04", "verdict": "split_link", "control": None,
  "pair": "tape-fundamentals",
  "a": "fundamentals:fund_p16:price-discovery-is-very-fast-with-close-to-70-of-the",
  "b": "tape:names:aapl-p4-overnight-gap-statistics-gap-fill-rate-overn",
  "relation": "shares-object",
  "role_difference": "fundamentals: price discovery measured intraday at tick resolution (~70% within 5 min, WPC); tape: overnight gap statistics, gap-fill rate after |gap|>1%, and overnight-vs-intraday log-return decomposition at daily resolution",
  "reason": "Shared object (price adjustment outside regular hours); different granularity and different halves of the phenomenon.",
  "crack": "K9-3",
 },
 {
  "id": "A9-05", "verdict": "rejected", "control": None,
  "pair": "tape-fundamentals",
  "a": "fundamentals:fund_p7:no-significant-pre-earnings-announcement-drift-ident",
  "b": None,
  "relation": None,
  "role_difference": None,
  "reason": "No tape counterpart: no procedure measured pre-event drift (P1-P8 have no event-relative windows). Different objects; not a touch.",
  "crack": None,
 },
 {
  "id": "A9-06", "verdict": "split_link", "control": "C2",
  "pair": "tape-narrative",
  "a": "narrative:narr_p1:positive-and-negative-news-about-firms-affects-their",
  "b": "tape:indices:single-day-return-tail-structure-moments-and-run-str",
  "relation": "shares-phenomenon",
  "role_difference": "narrative: documents news-driven price changes with pre/post disclosure attribution (FinBERT sentiment, 2003-2016 global sample); tape: measures large single-day moves and their clustering on specific dates in the fixed window with no news dates available, hence no attribution possible",
  "reason": "C2 CONTROL (weakly resolved, caveat recorded): shared phenomenon (event-concentrated large price moves); the tape cannot attribute moves to news in this window. The caveat is part of the verdict, not a footnote.",
  "crack": "K9-4",
 },
 {
  "id": "A9-07", "verdict": "miss", "control": None,
  "pair": "tape-narrative",
  "a": "narrative:narr_p2:pre-news-effect-reflects-diffusion-of-news-informati",
  "b": None,
  "relation": None,
  "role_difference": None,
  "reason": "Miss: no tape counterpart — no procedure measures pre-event price drift (would require news dates). Absence, not a touch.",
  "crack": None,
 },
 {
  "id": "A9-08", "verdict": "miss", "control": None,
  "pair": "tape-narrative",
  "a": "narrative:narr_p1:propagation-of-market-values-through-supply-chains",
  "b": None,
  "relation": None,
  "role_difference": None,
  "reason": "Miss: no supply-chain structure exists in the tape universe (9 series, no link data). Absence, not a touch.",
  "crack": None,
 },
 {
  "id": "A9-09", "verdict": "split_link", "control": None,
  "pair": "fundamentals-narrative",
  "a": "fundamentals:fund_p1:earnings-announcements-as-high-variance-draws-from-t",
  "b": "narrative:narr_p1:positive-and-negative-news-about-firms-affects-their",
  "relation": "shares-object",
  "role_difference": "fundamentals: scheduled fundamental information events (earnings) as high-variance draws; narrative: general news sentiment (FinBERT) as the information flow. Same object (information -> prices), different information kinds.",
  "reason": "Genuine shared referent with named role difference.",
  "crack": None,
 },
 {
  "id": "A9-10", "verdict": "split_link", "control": None,
  "pair": "fundamentals-narrative",
  "a": "fundamentals:fund_p1:post-earnings-announcement-trading-rule-returns-consis",
  "b": "narrative:narr_p1:net-effect-of-the-disclosure-of-positive-news-as-the",
  "relation": "shares-phenomenon",
  "role_difference": "fundamentals: post-announcement price dynamics measured via trading-rule returns (efficient after 2016); narrative: post-disclosure price adjustment measured as net effect (post minus pre). Different events, different estimators, same phenomenon (post-event price adjustment).",
  "reason": "Shared phenomenon with different operationalizations.",
  "crack": None,
 },
 {
  "id": "A9-11", "verdict": "split_link", "control": None,
  "pair": "fundamentals-narrative",
  "a": "fundamentals:fund_p2:price-discovery-as-the-process-by-which-new-public-i",
  "b": "narrative:narr_p2:pre-news-effect-reflects-diffusion-of-news-informati",
  "relation": "shares-question",
  "role_difference": "Same question (how does information enter prices?), opposite answers: fundamentals: fast public impounding after announcement (~70% in 5 min); narrative: slow private diffusion before disclosure (pre-news drift via unofficial channels).",
  "reason": "The contrast is the finding: two documented mechanisms pulling in opposite temporal directions.",
  "crack": None,
 },
 {
  "id": "A9-12", "verdict": "split_link", "control": None,
  "pair": "fundamentals-narrative",
  "a": "fundamentals:fund_p1:jump-spillover-to-non-announcing-firms-and-the-marke",
  "b": "narrative:narr_p1:propagation-of-market-values-through-supply-chains",
  "relation": "shares-phenomenon",
  "role_difference": "fundamentals: cross-firm transmission via industry proximity (jump co-movement); narrative: cross-firm transmission via supply-chain links (sentiment propagation). Same phenomenon (information shocks cross firm boundaries), different channels.",
  "reason": "Genuine shared phenomenon with named channel difference.",
  "crack": None,
 },
 {
  "id": "A9-13", "verdict": "rejected", "control": None,
  "pair": "tape-fundamentals",
  "a": "fundamentals:fund_p1:noise-robust-jump-test-generalizing-the-barndorff",
  "b": None,
  "relation": None,
  "role_difference": None,
  "reason": "Rejected: no tape counterpart. The paper's econometric jump-test instrument and the tape's descriptive tail statistics are different objects; sharing the word 'jump' is not sharing a referent (Atlas-5 GUE precedent).",
  "crack": None,
 },
 {
  "id": "A9-14", "verdict": "rejected", "control": None,
  "pair": "tape-narrative",
  "a": "narrative:narr_p1:level-of-positiveness-and-negativeness-of-each-news-art",
  "b": None,
  "relation": None,
  "role_difference": None,
  "reason": "Rejected: no tape counterpart. FinBERT sentiment measurement has no structural analogue in P1-P8.",
  "crack": None,
 },
]

# attach labels for the report
for x in ADJ:
    for side in ('a', 'b'):
        nid = x.get(side)
        x[side + '_label'] = g[nid]['label'][:100] if nid and nid in g else None

json.dump(ADJ, open(os.path.join(BASE, 'atlas9_adjudications.json'), 'w'),
          ensure_ascii=False, indent=1)
v = {}
for x in ADJ:
    v[x['verdict']] = v.get(x['verdict'], 0) + 1
print('adjudications:', len(ADJ), v)
print('controls:', [(x['id'], x['control'], x['verdict']) for x in ADJ if x['control']])
