# Atlas-9 Grading Packet

**Date:** 2026-10-07/08 · **Run:** market atlas (tape / fundamentals / narrative)
**Bar:** 0 false merges, 0 contradictions.
**Standing:** mapping run, NOT investment advice.

## ALL adjudications (14)

### A9-01 — `split_link` (CONTROL C1)
- **pair:** tape-fundamentals
- **a:** [fund_p1/c5] `computationally_verified` — jump probability exceeding 90% in after-hours sessions with earnings announcements versus 2.95% in the regular session and 3.67% in after-ho
- **b:** [tape_names/R-P3-AAPL] `computationally_verified` — AAPL: P3: daily volume vs absolute-return relation and volume-spike structure
- **role difference (D3):** fundamentals: proves the earnings-announcement jump phenomenon at tick resolution with causal attribution to announcements (paper's own 12-year sample); tape: measures 1.83x mean |return| and 1.53-1.86x volume on 23 Nasdaq-verified earnings dates in the fixed 2024-10/2026-10 window, without independent causal attribution
- **reason:** C1 CONTROL: the paper's documented price response resolves against the tape. Verified: verification/verify_c1_earnings.py — 33% of earnings-window days in top decile of |return| vs 10% baseline.
- **crack:** K9-1

### A9-02 — `split_link` 
- **pair:** tape-fundamentals
- **a:** [fund_p1/c9] `computationally_verified` — after-hours trading activity as a tale of two markets: volume explodes on announcement days
- **b:** [tape_names/R-P3-MSFT] `computationally_verified` — MSFT: P3: daily volume vs absolute-return relation and volume-spike structure
- **role difference (D3):** fundamentals: volume spikes attributed to earnings announcements (tale of two markets); tape: volume spikes defined structurally (>2x trailing-20d median) with volume-|return| correlation and spike next-day returns, no attribution
- **reason:** Same object (trading-volume spike behavior), different epistemic roles.
- **crack:** K9-2

### A9-03 — `split_link` 
- **pair:** tape-fundamentals
- **a:** [fund_p16/c6] `computationally_verified` — Apple case study: pre-averaged realized variance spikes on announcement days and almost all price jumps coincide with earnings announcements
- **b:** [tape_indices/t_p2_sp500] `computationally_verified` — 21-day rolling annualized volatility tercile regime classification: SP500
- **role difference (D3):** fundamentals: realized variance measured event-conditionally (spikes on announcement days, Apple case); tape: realized volatility measured unconditionally as in-window tercile regimes with dated top-5 episodes
- **reason:** Same object (realized volatility), different conditioning.

### A9-04 — `split_link` 
- **pair:** tape-fundamentals
- **a:** [fund_p16/c2] `computationally_verified` — price discovery is very fast, with close to 70% of the post-announcement price discovered within five minutes
- **b:** [tape_names/R-P4-AAPL] `computationally_verified` — AAPL: P4: overnight-gap statistics, gap-fill rate, overnight vs intraday log-return decomposition
- **role difference (D3):** fundamentals: price discovery measured intraday at tick resolution (~70% within 5 min, WPC); tape: overnight gap statistics, gap-fill rate after |gap|>1%, and overnight-vs-intraday log-return decomposition at daily resolution
- **reason:** Shared object (price adjustment outside regular hours); different granularity and different halves of the phenomenon.
- **crack:** K9-3

### A9-05 — `rejected` 
- **pair:** tape-fundamentals
- **a:** [fund_p7/c8] `computationally_verified` — No significant pre-earnings announcement drift identified in the data
- **b:** (none)
- **reason:** No tape counterpart: no procedure measured pre-event drift (P1-P8 have no event-relative windows). Different objects; not a touch.

### A9-06 — `split_link` (CONTROL C2)
- **pair:** tape-narrative
- **a:** [narr_p1/c1] `conjectural` — positive and negative news about firms affects their stock prices and the stock prices of their suppliers and clients
- **b:** [tape_indices/t_p7_sp500] `computationally_verified` — single-day return tail structure, moments, and run streaks: SP500
- **role difference (D3):** narrative: documents news-driven price changes with pre/post disclosure attribution (FinBERT sentiment, 2003-2016 global sample); tape: measures large single-day moves and their clustering on specific dates in the fixed window with no news dates available, hence no attribution possible
- **reason:** C2 CONTROL (weakly resolved, caveat recorded): shared phenomenon (event-concentrated large price moves); the tape cannot attribute moves to news in this window. The caveat is part of the verdict, not a footnote.
- **crack:** K9-4

### A9-07 — `miss` 
- **pair:** tape-narrative
- **a:** [narr_p2/c8] `heuristic` — pre-news effect reflects diffusion of news information through private channels (financial-company suggestions, SNS posts, word of mouth) be
- **b:** (none)
- **reason:** Miss: no tape counterpart — no procedure measures pre-event price drift (would require news dates). Absence, not a touch.

### A9-08 — `miss` 
- **pair:** tape-narrative
- **a:** [narr_p1/c4] `computationally_verified` — propagation of market values through supply chains
- **b:** (none)
- **reason:** Miss: no supply-chain structure exists in the tape universe (9 series, no link data). Absence, not a touch.

### A9-09 — `split_link` 
- **pair:** fundamentals-narrative
- **a:** [fund_p1/c1] `conjectural` — earnings announcements as high-variance draws from the public news process that, in efficient markets, should almost surely trigger jumps in
- **b:** [narr_p1/c1] `conjectural` — positive and negative news about firms affects their stock prices and the stock prices of their suppliers and clients
- **role difference (D3):** fundamentals: scheduled fundamental information events (earnings) as high-variance draws; narrative: general news sentiment (FinBERT) as the information flow. Same object (information -> prices), different information kinds.
- **reason:** Genuine shared referent with named role difference.

### A9-10 — `split_link` 
- **pair:** fundamentals-narrative
- **a:** [fund_p1/c7] `computationally_verified` — post-earnings announcement trading-rule returns consistent with efficient price formation after 2016
- **b:** [narr_p1/c5] `computationally_verified` — net effect of the disclosure of positive news as the positive difference between the post- and pre-news effects
- **role difference (D3):** fundamentals: post-announcement price dynamics measured via trading-rule returns (efficient after 2016); narrative: post-disclosure price adjustment measured as net effect (post minus pre). Different events, different estimators, same phenomenon (post-event price adjustment).
- **reason:** Shared phenomenon with different operationalizations.

### A9-11 — `split_link` 
- **pair:** fundamentals-narrative
- **a:** [fund_p2/c2] `exact` — price discovery as the process by which new public information gets impounded into the efficient price
- **b:** [narr_p2/c8] `heuristic` — pre-news effect reflects diffusion of news information through private channels (financial-company suggestions, SNS posts, word of mouth) be
- **role difference (D3):** Same question (how does information enter prices?), opposite answers: fundamentals: fast public impounding after announcement (~70% in 5 min); narrative: slow private diffusion before disclosure (pre-news drift via unofficial channels).
- **reason:** The contrast is the finding: two documented mechanisms pulling in opposite temporal directions.

### A9-12 — `split_link` 
- **pair:** fundamentals-narrative
- **a:** [fund_p1/c6] `computationally_verified` — jump spillover to non-announcing firms and the market index, related to industry proximity and after-hours liquidity
- **b:** [narr_p1/c4] `computationally_verified` — propagation of market values through supply chains
- **role difference (D3):** fundamentals: cross-firm transmission via industry proximity (jump co-movement); narrative: cross-firm transmission via supply-chain links (sentiment propagation). Same phenomenon (information shocks cross firm boundaries), different channels.
- **reason:** Genuine shared phenomenon with named channel difference.

### A9-13 — `rejected` 
- **pair:** tape-fundamentals
- **a:** [fund_p1/c2] `exact` — noise-robust jump test generalizing the Barndorff-Nielsen and Shephard 2006 bipower variation-based jump test
- **b:** (none)
- **reason:** Rejected: no tape counterpart. The paper's econometric jump-test instrument and the tape's descriptive tail statistics are different objects; sharing the word 'jump' is not sharing a referent (Atlas-5 GUE precedent).

### A9-14 — `rejected` 
- **pair:** tape-narrative
- **a:** [narr_p1/c7] `exact` — level of positiveness and negativeness of each news article determined by FinBERT
- **b:** (none)
- **reason:** Rejected: no tape counterpart. FinBERT sentiment measurement has no structural analogue in P1-P8.

## ALL merges (8, reviewed)

- MERGE `fundamentals:fund_p8:comparison-with-gregoire-and-martineau-2022-92-66`
  INTO `fundamentals:fund_p1:post-earnings-transaction-price-at-6-30pm-outside`
  shared claim: post-earnings transaction price at 6:30pm outside the pre-an
- MERGE `fundamentals:fund_p8:noise-robust-pre-averaged-jump-test-generalizing-`
  INTO `fundamentals:fund_p1:noise-robust-jump-test-generalizing-the-barndorff`
  shared claim: noise-robust jump test generalizing the Barndorff-Nielsen an
- MERGE `narrative:narr_p4:positive-news-raises-stock-prices-of-the-firms-suppl`
  INTO `narrative:narr_p1:propagation-of-market-values-through-supply-chains`
  shared claim: propagation of market values through supply chains
- MERGE `narrative:narr_p4:larger-post-news-effect-than-pre-news-effect-in-gene`
  INTO `narrative:narr_p1:net-effect-of-the-disclosure-of-positive-news-as-the`
  shared claim: net effect of the disclosure of positive news as the positiv
- MERGE `fundamentals:fund_p8:jump-spillover-effect-earnings-announcements-rais`
  INTO `fundamentals:fund_p1:jump-spillover-to-non-announcing-firms-and-the-ma`
  shared claim: jump spillover to non-announcing firms and the market index,
- MERGE `fundamentals:fund_p8:post-earnings-announcement-trading-profits-declin`
  INTO `fundamentals:fund_p7:speed-up-of-price-discovery-average-returns-large`
  shared claim: Speed-up of price discovery: average returns larger and more
- MERGE `narrative:narr_p4:supply-chain-identification-financial-statements-sup`
  INTO `narrative:narr_p1:identifying-supply-chains-via-financial-statements-f`
  shared claim: identifying supply chains via financial statements (FactSet,
- MERGE `narrative:narr_p4:for-japanese-firms-the-post-news-effect-on-suppliers`
  INTO `narrative:narr_p1:the-post-news-effect-on-suppliers-and-clients-in-jap`
  shared claim: the post-news effect on suppliers and clients in Japan is sm

## Sampled triples for the grader (12)

Each triple: (adjudication, verdict, what to check).

- **A9-01** (`split_link`): key control — verification script ran; earnings dates Nasdaq-verified
- **A9-06** (`split_link`): weak control — is the attribution caveat adequate, or reject?
- **A9-11** (`split_link`): same question, opposite answers — does the contrast hold?
- **A9-12** (`split_link`): industry-spillover vs supply-chain propagation — same phenomenon?
- **A9-04** (`split_link`): intraday discovery vs daily gaps — shared object or stretch?
- **A9-03** (`split_link`): event-conditional vs unconditional volatility
- **A9-02** (`split_link`): attributed vs structural volume spikes
- **A9-09** (`split_link`): scheduled vs general news — same information→prices object?
- **A9-10** (`split_link`): post-event adjustment in both skies
- **A9-05** (`rejected`): no tape counterpart for pre-announcement drift — right?
- **A9-13** (`rejected`): jump test vs tail stats — right to reject the word-overlap?
- **A9-08** (`miss`): supply-chain propagation has no tape counterpart — right?

## Drops (BK2011)
- Stooq daily CSV: JS-verification wall. Yahoo chart API: domain policy-blocked, not retried.
- Universe fixed to FRED + Nasdaq API data; recorded in manifest.json.

## Controls
- C1 RESOLVED (split_link A9-01, verified). C2 RESOLVED WEAKLY (split_link A9-06, caveat recorded).