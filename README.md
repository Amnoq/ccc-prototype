# CCC Minimum Working Prototype

Runnable implementation of the dynamical system specified in
`ccc_math_formalization_10_so6y.md`, plus the strand export / rehydration
loop specified in `ccc_ai_integration_3_0m15.md`.

## Files

- `ccc.py` — engine. Graph with node activation / interest / stability and
  edge weight / openness; closure density C(t); fragmentation load F(t);
  event detection (insight, conversion, anchor promotion, fragmentation,
  reconstruction); `export_state()` (strand compression to JSON);
  `Graph.rehydrate()` (rebuild working context in a fresh graph);
  `probe()` (keyword QA against graph state).
- `demo.py` — scripted 19-step research session (wheel-210 verification
  narrative): cues, a discovery, an interruption, anchor-cued
  reconstruction; then export → wipe → rehydrate → probe metrics.
- `ccc_export.json` — the export produced by the demo run.
- `codec.py` — codec v1: registry, prime structural layer, v2/v3/v4 wires,
  telomere framing, multi-line transport, product/parity code.
- `cursor.py` — cursor layer: shared accumulated concept graph, op-stream
  encode (greedy walk cover, cheapest absolute-vs-walk edge naming),
  trivial replay decode.
- `entropy.py` — second-stage coding experiments: canonical Huffman with
  transmitted codebook, LZ77 (fixed-cost and profit-gated), stacked
  LZ77+Huffman, v3-style bitstring wire framing.
- `demo_cursor.py` — scale simulation (B=1000, clustered history graph,
  120 coherent messages) measuring cursor + entropy stages vs the v3
  structural baseline in exact bits and cl100k_base tokens.

## What the demo shows

1. **Insight → conversion → anchor.** Repeatedly re-engaged concepts
   (`cython_bug`, `wheel210`, `jacobsthal`) cross stability/interest
   thresholds and become anchors; one-shot trivia (`gcc_trivia`) never
   stabilizes.
2. **Fragmentation / reconstruction.** An interruption spikes F, reopens
   edges, drops closure; re-cueing anchors recovers it (reconstruction
   event fires on load drop).
3. **Strand compression.** Export keeps anchors, strand membership,
   relational constraints (w ≥ 0.70 edges), open loops, and
   reconstruction rules — not the transcript. ~58% of transcript bytes
   in this run (the ratio improves with session length; the export grows
   with stable structure, the transcript with raw events).
4. **Rehydration fidelity.** 4/4 retention probes answer identically from
   the full and rehydrated graphs; the trivia probe is correctly
   unanswerable after rehydration (selective forgetting).

## Run it

```
python3 demo.py
```

Pure stdlib, no dependencies. Deterministic (scripted scenario, no RNG).

## Codec v1 (`codec.py`, `demo_codec.py`)

A real, measured context codec in three layers, built toward the actual
goal (a code more efficient than tokens for carrying meaning across LLM
sessions):

- **Registry** — shared concept→index codebook, synchronized once.
  Content strings never retransmit. This is where the compression lives.
- **Prime structural layer** — sets (anchors, strands, open loops) as
  prime products: canonical, order-free, unambiguous by unique
  factorization. Edge pairs packed as small ints in canonical sorted
  order. Deterministic on both sides; no codebook sent per session.
- **Codon wire layer** — integers → base-64 symbol frames
  `[LEN LEN][digits][PARITY]`: self-delimiting, parity-checked
  (single-symbol corruption is detected — verified live).

Run it (needs the venv for tiktoken):

```
.venv/bin/python demo_codec.py
```

Three-session simulation, tokens counted with tiktoken `cl100k_base`
(proxy for the target LLM's tokenizer): session-2 structural update
26 tokens vs 192 raw (7.4×; 4/4 probes agree after full wire round-trip,
integers exact); session 3 with 2 novel concepts 86 vs 236 (2.7×);
3-session cumulative 1.11× (codebook sync of 274 tokens still
amortizing — break-even lands around session 2); projected 10 sessions
3.6×. The win is steady-state: sync once, then structure-only updates.
Novel content still travels raw once (correct behavior, not a failure).

Wire v4 (`encode_message_bits`): gamma-coded bitstream — each int as
Elias gamma(x+1) (self-delimiting, so no per-int counts), packed 9 bits
per decimal triple, header [nnn][pad] + mod-1000 checksum triple.
Transmits no padding zeros and no counts: nothing predictable is sent,
framing is reconstructed. Every digit position has nonzero weight mod
1000, so any single-digit flip is always detected (300 random
round-trips + adversarial flip verified). v4 fixes the edge packing:
pairs are packed 0-based (`a*B + b`, `a,b < B`) — the v2/v3 1-based
packing `i*B + j` was ambiguous when `j == B` and silently decoded 2 of
7 edges wrong (caught by the repair trial below; the fidelity check now
compares edges, not just anchors/strands). The wire layer is
deliberately tokenizer-specific; the registry and prime layers are
not — profile the wire per deployment target.
Current ledger: session-2 wire 17 tokens vs 192 raw (11.3×; 4/4 probes
agree after full wire round-trip, integers exact, edges verified);
session 3 with 2 novel concepts 77 vs 236 (3.1×); 3-session cumulative
1.16× (codebook sync of 274 tokens still amortizing — break-even around
session 2); projected 10 sessions 4.32×.

Telomere framing (`wrap_telomere` / `scan_telomeres`, demo:
`demo_telomere.py`): a naked wire assumes a clean channel, but a
model-side handoff buries the message in prose. Telomeres are
distinctive boundary markers (`zz…zz` open, mirrored `…ZZ` close —
impossible to collide with the digit-only body) carrying context in
the caps: wire version, registry size, registry fingerprint, session.
The decoder scans arbitrary text, skips mismatched caps, verifies the
fingerprint against its registry (wrong-registry detection), and
decodes the body. Overhead: +6 tokens (17 → 23 for the session-2 wire).
Run: `.venv/bin/python demo_telomere.py`.

2D relations (same demo): the session-2 relation graph as an adjacency
matrix — position (i,j) literally is the relation, codon-style. Result:
17/64 cells nonzero (73% zeros). The matrix is the same information as
the prime encoding, less dense for sparse graphs — the prime products
already are the 2D relation structure in efficient 1D form. And the
wire layout itself is codon-like: each slot's meaning comes from its
position in `[B, nS, strands…, nE, edges…, A, L]`.

Repair — DNA's real 2D trick is the second strand (redundancy that
corrects, not just detects). True 2D parity would cost +56% tokens;
checksum + brute force + strict structural validation buys single-error
correction with zero wire cost: over 200 random single-digit
corruptions, 187 uniquely corrected, 13 narrowed to a small candidate
set always containing the true wire, 0 uncorrectable. (Detection alone
was already bulletproof.)

Multi-line transport (`encode_lines` / `decode_lines`,
`validate_message`, demo: `demo_lines.py`): the integer message is
split into k self-describing lines (`LLKK` header + a full v4 wire per
chunk + a 3-digit header checksum binding the header to the body).
Lines decode independently, in any order, in parallel (thread-pool
demo), and reassemble exactly — order-free rehydration. Per-line
checksums localize corruption: the bad line is identified by index,
the brute-force search is confined to it (3.6× fewer candidates
than whole-wire repair at k=4: 121 vs 441, truth always included), and
surviving lines still decode on their own (dropped line → `missing
lines: [2]`, 10/14 ints recovered). Lines compose with telomeres: each
line wrapped in caps, scattered out of order in prose, discovered and
reassembled. Cost is constant per line (~4.5 tokens here, +18 total at
toy scale: 35 vs 17) — the economics favor scale, where it amortizes
to a few percent.

Product code (`encode_lines_parity` / `decode_lines_parity`, demo:
`demo_parity.py`): one parity line over the rows (column-wise mod-10
sums, header `99KK`) unifies the 2D idea and the lines idea.
Single-digit correction is now zero-search — the bad row comes from
the per-line checksums, the bad column from the parity syndrome, the
true digit is computed directly as (observed − syndrome) mod 10, with
no candidate enumeration (5 decode calls, 0 candidates, vs 441 for
whole-wire brute force and 121 for localized search). The per-line
header checksum was load-bearing: without header–body binding, a
header corruption causing a duplicate line index is provably
ambiguous at the parity level (two reconstructions, both with zero
syndromes and valid checksums — column parities are
permutation-invariant, so no column function can distinguish them).
Measured: 500/500 random single-digit corruptions corrected exactly
(all positions — body, header, checksum digits), plus k=2 and k=8 at
200/200; double corruptions detected not corrected; a corrupted
parity line degrades gracefully (message decodes from data alone);
parity composes with telomeres and shuffled order. Cost: one extra
line (~14 tokens at toy scale: 49 vs 17 total; ~1/k overhead at
scale).

Free-symbol hunt (measured, cl100k_base): no universally zero-cost
symbols exist. Zero-width chars (U+200B/U+200C/U+200D/U+2060), BOM,
combining marks, soft hyphen all cost 1–2 tokens each — invisible does
not mean free. Zero *marginal* cost is real but context-dependent: BPE
absorption (e.g. 's' after "dog" → "dogs", one token). Toy scale;
model-side decode (an LLM actually reading the wire) is future work.

Cursor layer (`cursor.py`, demo: `demo_cursor.py`) — the magician's
trick as a compression layer. Shared state is the accumulated concept
graph (nodes = registry indices, edges = relations from all previous
sessions); both sides hold identical copies evolving in lockstep. A
message is a sequence of ops from a shared cursor (walk to strand
targets via a greedy nearest-target cover; position + add each NEW
relation, naming the far endpoint absolutely or by graph walk,
whichever is cheaper — the encoder computes both). The decoder just
walks. Unreachable targets fall back to jumps, so walking is an
optimization, never a requirement. Measured at B=1000, 20×50 clustered
history graph, 120 coherent messages (10 strands + 7 new relations):
396 vs 522 bits/message (1.32×) vs the actual v3 structural codec
(prime products + packed pairs); wire tokens 47.5 vs 61.5 (1.30×).
Round-trip fuzz: 300/300, encoder/decoder state lockstep verified per
message. Densification is flat (first-20 vs last-20: 0.96×) — shorter
paths are offset by fatter degrees raising per-hop cost.

Second-stage coding (`entropy.py`) — the "zipped zip" question,
measured honestly. Per-message canonical Huffman on the op stream:
0.95× — the transmitted codebook is 41% of the total; loses.
Session-amortized Huffman (one codebook, ~free): 0.98× — the v3 gamma
wire is already near-optimal for this symbol distribution, leaving
only ~10% residual skew. LZ77 with fixed-cost tokens: wins on no
message vs raw cursor; profit-gated LZ77 (matches taken only when they
strictly save): 0.83× vs raw cursor — one flag bit per literal (~15%
overhead at ~60-int messages) exceeds what short matches save.
Stacked LZ77+Huffman (the gzip recipe): 0.63× — double overhead, worst
of all. Verdict: these second stages don't pay at this granularity,
and the measurement says why — codebook/flag overhead vs message
size, and gamma leaving little statistical redundancy. The cursor's
1.32× comes from GRAPH structure, which statistical coders can't see:
stacking is the right principle, but the next statistical stage needs
zero-overhead adaptive coding (both sides adapting in lockstep, no
transmitted codebook) to capture the residual ~10%.

Fountain / holographic layer (`fountain.py`, demo: `demo_fountain.py`) —
the "whole in the parts" as an erasure code. Each redundancy line is a
nibble-wise XOR combination of a pseudorandom subset of ALL data lines
(LT-style; the peeling decoder needs only an invertible group op, no
field), so the decoder's job changes from surgical locate-and-fix to
collect-and-solve: no error location, corrupted pieces are outvoted by
abundance. Data lines are byte-identical to the plain scheme; fountain
lines carry `97SS` headers (SS = seed, both sides recompute the subset
from it — shared determinism, nothing transmitted) plus per-line
checksums that convert silent corruption into erasures. Digits 0–9 map
to 4-bit nibbles, combined nibbles serialize as two decimal digits, so
the digit-only property, telomere regex, and triple tokenization all
survive. The encoder searches seed space: tier-2 seeds give full
data-line coverage (any single erasure *provably* recovers), tier-1
seeds (when 2^f > k) form a separating family with double coverage
(any ≤2 pool erasures provably recover).
Measured at k=8, 300 trials/cell, pool erasures + shuffle — success
fraction: f=1: e=1 → 1.000; f=2: e=2 → 0.657; f=4: e=3 → 0.873, e=4 →
0.427; f=6: e=5 → 0.593, e=6 → 0.250; e>f always 0.000 (clean
threshold). Theorems, asserted not sampled: single-erasure 1600/1600
exact (all 8 positions × 200 msgs); two-erasure 2800/2800 exact under
tier-1 seeds at f=4. Head-to-head vs parity (200 trials): 1-digit
corruption — both 1.000; 1-line erasure — parity decodes 0/200 (raises;
it handles corruption, not erasure), fountain(f=2) 1.000; 2-line
erasure — parity raises, fountain(f=4) 1.000. Mixed flips: checksums
convert to erasures, f=4 absorbs 2 flips at 1.000. Adversarial: 6/6
tampered fountain lines failed checksum and were dropped, never
silently mis-decoded; every one of ~10k successful trial decodes
asserted exact equality. Cost: fountain line ≈ 2× a parity line (24
vs 13 tokens at toy scale, cl100k_base); f lines ≈ 2f/k of message.
Honest negatives: fountain loses to parity whenever single-digit
corruption is the only threat (parity does that at half the price) —
its win is strictly the erasure/multi-error regime; f=2 cannot
deterministically handle 2 erasures (structural: 2 subsets induce ≤4
incidence atoms on 8 points, some pair is never separated — measured
0.65 is near the ceiling); e>f always fails; ≤100 fountain lines
(2-digit seed), k ≤ 97 for tag unambiguity.

Prime-wavelength channel tests (`channels.py`, demo:
`demo_channels.py`) — the fiber-vision claim, measured. The user's
video showed prime-spacing waveforms with the observation of "no
constructive/destructive interference on broadcast." Quantified
(N=16 tones, 200 phase trials): prime sets behave like random integer
sets — same crest factors, same constructive-event rates; crest tracks
bandwidth, not primality, and the harmonic set actually peaks lowest.
P(|s|>2rms) ≈ 0.044 for every set — the Gaussian tail; every set is a
Gaussian-ish phasor sum. The video impression was periodicity (true of
any integer set) plus bandwidth, not a prime property: claim FALSE as
stated. The deeper intuition — incommensurable spacing suppresses
nonlinear mixing — IS real: counting four-wave-mixing products
fᵢ+fⱼ−fₖ landing on live carriers (16 channels, matched span), prime
spacing cuts hits ~1.9× vs uniform (the textbook bad case), though
Golomb rulers (the classical "all differences distinct" tool) beat
prime by another ~1.7×. Linear worst-case cross-correlation: uniform
wins, prime middle, Golomb worst — max-min separation is the robust
linear property. End-to-end: 16 independent BPSK channels, 3.2M bits,
no joint processing — BER is a wash at realistic symbol rates under
either plan; prime's exact-null wins at aggressive rates evaporate
under frequency jitter. Verdict: the parallel-decode requirement is
satisfiable (linear crosstalk negligible at sane rates either way),
just not because of primes; the right formalization of the user's
instinct is Golomb spacing, not prime spacing. Modeled: ideal
carriers, AWGN, combinatorial FWM proxy, static plans. Not modeled:
dispersion, laser phase noise, EDFA noise, SPM/XPM moving the FWM
products, PMD/PDL, Raman/Brillouin, real filter shapes, THz-scale
carriers — the proxy counts placement, not power.

## 2026-09-28 — harness M1 (memory_harness.py)

M1 of HARNESS_MVP_SCOPE.md is done: strict extraction schema
(concepts/strands/typed directed edges/anchors/loops), deterministic
verifier (reference resolution, fixed rel/status/kind vocabularies,
no duplicate edges, v5 codec round-trip identity), SQLite store,
phase-1 entity resolution (exact-label reuse; normalized near-matches
inserted as new AND surfaced for human adjudication), self-contained
checkpoints (telomere-wrapped balanced multiline v5 wire + registry
snapshot + fingerprint), order-independent restore, grouped compact
injection (scale-test syntax). test_m1.py: 14/14 (happy path incl.
shuffled-line restore, fingerprint determinism, re-merge dedup;
orphan warns; 11 verifier negatives reject). Refinement vs scope 3.2:
loops reference concepts (usually kind "open_question") instead of
free text, because the v5 wire only carries registry indices.

## 2026-09-28 — harness M2 (extractor.py)

M2 of HARNESS_MVP_SCOPE.md is done: self-contained extractor prompt
(schema + all three fixed vocabularies + rules, 642 tok) and the
`extract_with_repair` driver (verifier-gated repair, ≤2 attempts,
token accounting from the first call). Acceptance run: 3 real
transcript chunks from the CCC arc (cursor layer 2852 tok / decode
test 924 tok / scale economics 1041 tok), author serving as the LLM
under a disciplined protocol (fresh attempt, validate once, ≤1
repair). Repairs used: 1/0/0 — the one failure was `"note": null`
on five anchors, caught by the verifier and fixed mechanically.
All three pass v5 round-trip identity (57/47/46 ints, B=53/44/45).
Full results in M2_REPORT.md. Caveats: extractor-skill bias (prompt
author = extractor; naive-model trial still required), home-turf
corpus, chunks 0.9–2.9k tok. Economics preview on chunk 1:
extraction 8868 tok vs ~2515 tok/session saving → break-even ≈3.5
sessions, right at the M4 GO boundary — M3's probe parity decides.
M3 corpus reserved: `m2_chunks/chunk4_memorysys_HELDOUT.txt`
(memory-system discussion, not yet extracted; probes to be written
blind).
