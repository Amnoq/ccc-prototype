# Lemmatization as a standard pipeline stage

2026-10-08. Authorized by the router ("Let's do it" on the assembly lane).
Prior art: the one-off discriminating test `lemma_rerun.py` (archived;
untouched), which re-ran the exact mechanical candidate generation with
node text lemmatized via `lemma-db/form2lemma.json` before IDF scoring.

## What changed

**`merge_atlas11.py`** (only file modified):
- New `generate_candidates(texts, pairs=None, lemmatize=True, lem_db=None)` —
  the former inline candidate-generation block, extracted verbatim into a pure
  function (writes nothing; returns `(out_doc, by_pair_counts)`).
- New module section "lemmatization stage": lazy `_get_lemma_db()` loads
  `~/workspace/lemma-db/lemma_api.py` (`LemmaDB`) only when `lemmatize=True`,
  so `--no-lemmatize` runs never touch the bank. `lemmatize_text()` maps each
  token of the normalized node text through `LemmaDB.lemmatize(word, 'en')`;
  unknown forms pass through unchanged (honest gap, mirrors the experiment).
- `main()` takes `--lemmatize` (default: **on**) / `--no-lemmatize` (control
  baseline). `candidates.json` now carries a `lemmatization` block:
  `{enabled, bank, coverage}` — bank lists per-language form counts from
  `LemmaDB.languages()`; coverage is the empirical `LemmaDB.coverage()` over
  all normalized corpus tokens.
- `main()` records the stage in `manifest.json` under `candidate_generation`:
  `{lemmatization, lemma_bank, lemma_coverage, date, note}`.

`LEMMATIZE_DEFAULT = True` — future runs lemmatize unless explicitly told
not to. Nothing else in the merge logic changed.

## Verification (2026-10-08, pure function calls on the archived graphs)

- `lemmatize=False` reproduces `candidates.json` **exactly**: 381 candidates
  (123 / 151 / 107), pair-set identical. The refactor is faithful.
- `lemmatize=True` reproduces the experiment's rerun **exactly**: 532 total
  (202 / 196 / 134); 337 retained + 195 new (99 direct / 55 S1 / 41 S2) —
  the same 195 the adjudication reviewed. Recall direction confirmed.
- Empirical coverage on the Atlas-11 corpus: **0.624** (bank at verification
  time: ben=3,903, en=182,903, grc=30,234, lat=493,046, urd=5,683).
- No pipeline outputs were written during verification: `candidates.json`,
  `manifest.json`, adjudication records, and the prediction ledger are
  untouched (timestamps confirm). `lemma_rerun.py` and
  `adjud_lemma_rerun.json` were not modified.

## For future runs

Run `merge_atlas11.py` normally (lemmatization on, recorded in manifest).
For a control comparison against the pre-stage baseline:
`merge_atlas11.py --no-lemmatize`.
