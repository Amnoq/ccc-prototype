# M2 report — extractor prompt + repair loop (2026-09-28)

## What was built

`extractor.py`:
- `EXTRACTOR_PROMPT` — self-contained prompt: strict schema, all three fixed
  vocabularies (12 relations, 4 statuses, 6 kinds), extraction rules, JSON-only
  output contract. 642 tokens (cl100k_base).
- `REPAIR_PROMPT` — previous output + verifier failure list + schema reminder,
  JSON-only correction. 72 tokens + payload.
- `extract_with_repair(chunk, llm_fn, max_repairs=2)` — driver: extract,
  `validate_extraction`, on failure feed the deterministic failure list back,
  retry. Returns doc, repairs_used, warnings, token counts.
- `extract_json_from_response` — balanced-brace JSON recovery from chatty
  output. `count_tokens` — cl100k_base accounting from the first call.

## Corpus

Three real transcript chunks from the CCC session arc (pulled verbatim from
the conversation record, 2026-09-27/28):

| chunk | content | source tokens |
|---|---|---|
| 1 `chunk1_cursor.txt` | cursor layer: state-of-play, sentence-types, magician/synchronizing word, cursor proposal, zipped-zip | 2852 |
| 2 `chunk2_decodetest.txt` | decode test (A+B), v5 build, 1.75x→1.27x correction | 924 |
| 3 `chunk3_scaleecon.txt` | scale test (2.2x), product economics, cost-play verdict | 1041 |

## Protocol

The author served as the LLM (see caveats). Discipline: attempt 1 written
fresh per chunk; validated exactly once; at most one repair pass addressing
only the reported failures. The acceptance bar from scope §3.6: 3 consecutive
clean extractions, ≤1 repair each.

## Results

| chunk | concepts | edges | anchors | strands | loops | repairs | warnings | extraction tok (in/out) |
|---|---|---|---|---|---|---|---|---|
| 1 | 37 | 28 | 13 | 5 | 1 | 1 | 0 | 5772 / 3096 |
| 2 | 28 | 20 | 14 | 4 | 2 | 0 | 0 | 1566 / 1248 |
| 3 | 29 | 20 | 11 | 5 | 2 | 0 | 0 | 1683 / 1251 |

Driver-faithful cost for chunk 1 (repair prompt actually rendered):
attempt 1 in=3494 out=1558; repair in=2278 out=1538; **total 8868**.

Verifier pass rate: **3/3 within ≤1 repair. M2 acceptance met.**

The single failure: chunk 1 attempt 1 used `"note": null` on five anchors;
the verifier rejects non-string notes. The repair was mechanical (drop null
notes), no restructuring. The schema strictness did exactly its job.

Round-trip check: every accepted extraction passes `verify_roundtrip`
(v5 encode/validate/decode identity) — chunk 1: 57 ints, B=53; chunk 2:
47 ints, B=44; chunk 3: 46 ints, B=45.

## Token-economics preview (chunk 1, not the M3 verdict)

- Source prose: 2852 tok. Extraction cost: 8868 tok.
- Grouped injection of the extracted structure: **337 tok**
  (+ 527 tok one-time legend for B=53).
- Per-session saving vs prose: ~2515 tok → **break-even ≈ 3.5 sessions**.

That sits right at the M4 GO threshold (≤3 sessions). Whether it holds
depends on M3's probe parity — a cheap extraction that loses the argument
is worthless at any break-even.

## Caveats (honest)

1. **Self-extraction.** The prompt's author was the extractor — the best
   case, not the average case. Grading bias is nil (the verifier is
   deterministic; nothing was hand-waved through), but extractor-skill
   bias is real. A naive-model trial is still required before any claim
   about "an LLM can do this" generalizes.
2. **Corpus is home turf.** Dense, well-structured technical prose the
   extractor was designed around. Messier dialogue (half-finished
   thoughts, corrections, voice-dictation artifacts) is untested.
3. **Chunk sizes 0.9–2.9k tokens**, below the 2–4k target — the transcript's
   natural discussion units, not padded.

## Status

**M2 done.** Next: M3 — probe parity on a held-out chunk
(`chunk4`, the memory-system discussion, reserved and not yet extracted).
Probes written blind to extraction output; answers compared source-prose
vs grouped injection; omissions/hallucinations/parity/amortization
measured against the M4 thresholds.
