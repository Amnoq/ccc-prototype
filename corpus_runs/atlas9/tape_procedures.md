# Atlas-9 Tape Procedures (PRE-REGISTERED)

**Date:** 2026-10-07
**Status:** written BEFORE any tape data values were seen (connectivity
tests showed only row counts and first rows; no distributions inspected).
These procedures are the tape drafters' brief. No procedure may be added,
removed, or re-parameterized after data is seen. If a procedure cannot run
(e.g., missing field), record the concept as absent — do not substitute.

## Fixed universe and window

- **Window:** 2024-10-01 to 2026-10-01 (trading days only).
- **Index closes (FRED, daily):** SP500, NASDAQCOM, DJIA —
  `data/fred_{SP500,NASDAQCOM,DJIA}.csv` (columns: observation_date, value).
- **Volatility/rates/credit (FRED, daily):** VIXCLS, DGS10, BAMLH0A0HYM2 —
  `data/fred_{VIXCLS,DGS10,BAMLH0A0HYM2}.csv`.
- **Single names (Nasdaq API, OHLCV):** AAPL, MSFT, NVDA —
  `data/nasdaq_{AAPL,MSFT,NVDA}.csv`
  (columns: date, open, high, low, close, volume; date format MM/DD/YYYY).
- All series are price/index levels except where noted. Log returns:
  r_t = ln(P_t / P_{t-1}) on consecutive trading days.

## Blindness

The tape drafter NEVER reads the fundamentals or narrative chunks, the
charter's literature discussion, or any finance vocabulary beyond what
these procedures name. Labels must be structural and neutral
(e.g., "21-day rolling volatility regime classification"), never
interpretive (e.g., never "fear gauge", never "earnings effect").

## Procedures (fixed; run all that the fields allow)

**P1 — Trend regimes (all price series).**
Compute 50-day and 200-day simple moving averages of the level.
Classify each day: uptrend (50DMA > 200DMA), downtrend (50DMA < 200DMA).
Extract: fraction of window in each regime; the dated regime intervals;
max consecutive uptrend/downtrend run. kind: result.

**P2 — Volatility regimes (all price series + VIXCLS).**
Realized vol: 21-trading-day rolling std of r_t, annualized ×√252.
Classify each day by in-window tercile of realized vol
(low/mid/high). Extract: tercile cutoffs; fraction of days per tercile;
longest high-vol episode; the dates of the top-5 realized-vol days.
For VIXCLS additionally: mean, min, max, and dates of top-5 VIX prints.
kind: result.

**P3 — Volume–price relations (single names only: AAPL, MSFT, NVDA).**
(a) Pearson correlation of daily share volume with |r_t|.
(b) Mean volume on up days (r_t>0) vs down days (r_t<0), ratio.
(c) Volume spikes: days with volume > 2× trailing-20-day median volume;
count them; mean next-day return after spikes vs unconditional mean.
kind: result.

**P4 — Gap / overnight behavior (single names only).**
Overnight gap g_t = open_t / close_{t-1} − 1.
(a) Mean, std, and top-5 absolute gaps with dates.
(b) Gap-fill rate: fraction of days with |g_t| > 1% where the intraday
move (close_t/open_t − 1) has opposite sign to g_t.
(c) Overnight vs intraday contribution: Σ ln(open_t/close_{t-1}) vs
Σ ln(close_t/open_t) over the window (total log-return decomposition).
kind: result.

**P5 — Drawdown structures (all price series).**
From the level series: max drawdown (peak-to-trough % and dates);
count of drawdowns deeper than 5% and 10%; longest drawdown duration
in trading days; time to recover each 10%+ drawdown (trough to new high,
or "unrecovered at window end"). kind: result.

**P6 — Cross-series relations (fixed pairs).**
(a) Daily-return correlations: SP500–NASDAQCOM, SP500–DJIA,
NASDAQCOM–DJIA; AAPL–MSFT, AAPL–NVDA, MSFT–NVDA; each single name vs SP500.
(b) VIXCLS vs SP500: correlation of VIXCLS level with SP500 21-day
realized vol; correlation of daily VIXCLS changes with SP500 daily returns.
(c) DGS10 changes vs SP500 returns: correlation of daily DGS10 changes
with SP500 daily returns.
(d) BAMLH0A0HYM2 changes vs SP500 returns: correlation of daily spread
changes with SP500 daily returns.
kind: result.

**P7 — Tail structure (all price series).**
(a) Top-5 and bottom-5 single-day returns with dates.
(b) Fraction of days with |r_t| > 2% and > 3%.
(c) Skewness and excess kurtosis of daily r_t.
(d) Longest consecutive up-day and down-day streaks.
kind: result.

**P8 — Calendar structure (all price series).**
Mean daily return by weekday (Mon–Fri), with counts. Note any weekday
with |mean| > 2× the overall daily mean absolute return. kind: result.

## Output schema (same as the text drafters)

One JSON file per drafter at
`~/workspace/ccc-prototype/corpus_runs/atlas9/extractions/tape_<id>.json`
with exactly: `concepts` (list of {"id","kind","label"}; kind ∈
{claim, definition, method, result, conjecture, question}; labels in the
NEUTRAL STRUCTURAL vocabulary of these procedures), `anchors`
({"concept_id","genre","note","status"}; status ∈ {exact,
computationally_verified, conjectural, heuristic, killed}; computed
facts are computationally_verified; identities exact; every number that
appears goes in the note), `edges` (a,b,rel ∈ {supports, depends_on,
contradicts, refines, generalizes, illustrates} — only within-tape
relations the computations support), `loops` (open questions the
procedures leave open — e.g., a procedure that could not run), `strands`
(argumentative threads among the tape concepts).

## Output discipline

- Valid JSON; ids unique; every reference resolves. Validate with
  python3 -c "import json; json.load(open(...))".
- Final report: concepts/anchors/edges/loops/strands counts, series
  actually processed, any procedure that could not run and why.
- Do not narrate at length. Compute, extract, validate, report.
