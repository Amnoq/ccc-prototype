# CCC Session Summary — 2026-09-27 (transfer document)

Purpose: everything a fresh conversation needs to continue this work without
re-reading history. Covers the CCC prototype's state plus today's session:
two new layers built and measured, and the "archaeology" of the user's
original concept, piece by piece, with each piece assayed.

## 1. What CCC is (one paragraph)

CCC (context compression coding) compresses persistent LLM context more
efficiently than re-sending natural-language tokens. Architecture: a shared
registry (concept → integer, synced once) supplies most steady-state
compression; a prime structural layer gives canonicity (sets as prime
products, relations as packed pairs — shared recomputation, not entropy
reduction); the v4 wire (Elias-gamma bitstream, decimal triples ~1 token per
10 bits, mod-1000 checksum) is tokenizer-aware framing; telomeres give
discoverability in prose; multiline transport gives order-independent
parallel rehydration; a product/parity code gives zero-search single-error
correction. Hard boundary: application-layer prompt savings only — cannot
bypass a transformer's hard context window without model-side changes.

Prototype location: `~/workspace/ccc-prototype/`
(`codec.py`, `cursor.py`, `entropy.py`, demos, README.md).

## 2. Compression ledger (measured, cl100k_base proxy, toy scale unless noted)

- Registry sync: 274 tokens, once.
- Repeat session wire: 17 vs 192 tokens (~11.3×).
- Session with 2 novel concepts: 77 vs 236 (~3.1×).
- 3-session cumulative: 368 vs 428 (~1.16×); 10-session projection ~4.32×.
- Multilines (k=4): +18 tokens overhead (~4.5/line); parity line +~14 tokens.
- Wire efficiency: ~8.3 bits/token vs 16.6 theoretical max (100k vocab);
  the gap is the price of digit-only encoding (checksums + prose embedding).

## 3. Built TODAY (2026-09-27)

### 3a. Cursor layer (`cursor.py`, `demo_cursor.py`) — from the magician's-trick idea
Shared state = accumulated concept graph (nodes = registry indices, edges =
relations from all previous sessions), both sides in lockstep. A message is
an op sequence from a shared cursor: TARGET_WALK / REL_WALK (n hops as edge
indices into sorted neighbor lists), NEW_EDGE (add edge, record relation;
far endpoint absolute or via graph walk, whichever cheaper — encoder computes
both), NEW_NODE / ADD_NODE (jumps for unreachable targets). Encoder works
hard (greedy nearest-target walk cover); decoder just walks. Ops are
self-delimiting.
Measured at B=1000, 20×50 clustered history graph, 120 coherent messages
(10 strands + 7 new relations): **396 vs 522 bits/msg (1.318×)** vs the
actual v3 structural codec; wire tokens 47.5 vs 61.5 (1.295×). 300/300 fuzz
round-trips; encoder/decoder state lockstep verified per message.
Densification effect flat (0.96×): shorter paths offset by fatter degrees.

### 3b. Entropy stages (`entropy.py`) — the "zipped zip" question, honest negative
- Per-message canonical Huffman: 0.951× — transmitted codebook = 41% of total.
- Session-amortized Huffman (one codebook): 0.981× — v3 gamma already
  near-optimal for this distribution; only ~10% residual skew.
- LZ77 fixed-cost tokens: loses to raw cursor on every message.
- Profit-gated LZ77 (only strictly-saving matches): 0.826× vs raw cursor —
  one flag bit per literal (~15% overhead at ~60-int messages) exceeds
  short-match savings.
- Stacked LZ77+Huffman (gzip recipe): 0.630× — double overhead, worst.
Verdict: these second stages don't pay at this granularity (codebook/flag
overhead vs message size; gamma leaves little statistical redundancy). The
cursor's 1.32× comes from GRAPH structure, invisible to statistical coders.
Correct next form if pursued: zero-overhead adaptive coding (both sides
adapt in lockstep, no transmitted codebook) for the residual ~10%.

## 4. The original-concept archaeology (today's conversation)

The user reconstructed their original design vision piece by piece. Each was
assayed honestly. Summary map:

1. **"As many sentence types as notes"** → Closed inventories (e.g. Quirk's
   7 clause patterns ≈ 7 diatonic notes) belong in the registry as
   prime-indexed tokens. Design guidance; the specific claim is unverified
   (no standard published result found; ask user for the source if pursued).
2. **Magician's trick** (finger on symbol, fixed move sequence, everyone
   lands together) → synchronizing words (reset sequences; Černý
   conjecture). Became the cursor layer (§3a). Shared grid = registry;
   move patter = wire; prediction envelope = checksum.
3. **"Zipped zip" (RAR-in-RAR)** → layered coding. Literally re-compressing
   a bitstream gains nothing (high entropy), but each layer removing a
   *different* redundancy is legitimate — CCC already is such a stack.
   Tested as §3b.
4. **Triangles (4 orientations) × colors** → Died on the text channel
   (color has zero capacity through text APIs — measured earlier; each
   ▲▼◀▶ is just a token; 2D symbol flattens to flat codepoints). REBORN as
   fiber: colors = wavelengths (WDM), orientations = polarization states —
   backbone internet technology. It was a physical-layer design all along.
   (Side note: DNA has 4 *bases*, 64 codons — corrected on the record.)
5. **Interference / holographic principle for broadcast** → the distributed-
   redundancy idea: every fragment contains the whole. Reference beam =
   shared registry/graph (wire alone is noise — already true of CCC).
6. **Prime wavelength per line** → parallel independent strand decode.
   Converges with our multiline transport (same decomposition: logic vs
   physics). Honest calibration: plain WDM already separates lines; PRIME
   spacing buys the second-order wins (four-wave-mixing products fall
   off-channel with incommensurable spacing — unequal-spacing literature
   exists; plus code-family properties). "Each strand sequence independent"
   per wavelength dissolves the "semantic fragment independence" todo.
7. **"Whole in the parts" → easier error correction** → surgical
   (locate-and-fix: our parity scheme, provably hits ambiguity walls) vs
   statistical (collect enough good pieces and solve: no error location).
   Real codes: fountain/LT/Raptor, Reed-Solomon. LT partial recovery ≈
   hologram fragment's blurrier image. Composition: our per-line checksums
   convert silent errors → erasures; fountain lines decode from survivors.
8. **Human-eye error checking via holographic display** → fail-visible vs
   fail-silent design axis. Digital incarnations exist (SSH randomart,
   visual hashes). On text channel, checksums are the machine substitute;
   the kept principle: never fail silent.
9. **Reconstruction space as security** → Wyner's wiretap channel
   (information-theoretic secrecy when the legit receiver's channel is
   better). Shared graph = CCC's "reconstruction space." Honest caveat:
   obfuscation, not encryption — pre-shared secret, no forward secrecy.

Overall verdict delivered to user: the original concept was a coherent
holographic fiber-optic communication system; nearly everything in it was
right; the pieces that "didn't work" were channel mismatches, not bad
thinking. The video shared today (prime spacings as trajectories pinching
at zero; user claims no constructive/destructive interference on
broadcast) belongs to the fiber-vision thread — the non-interference claim
is UNVERIFIED (visual observation only).

## 5. Token-system question (answered today)

"Can a token be reduced to a number and retain its relations?" — No: BPE
token IDs are arbitrary labels (merge order); adjacency in ID space is
meaningless. Relations live in the embedding matrix (model) and merge tree
(tokenizer), not the numbers. BUT the tokenizer itself is a free shared
deterministic codebook = CCC layer 0 (lexical, given); our registry is the
semantic layer on top. Channel constraint: no API accepts raw token IDs —
everything re-enters as digit strings, which is why the triple wire is the
optimized form. Relations are encoded structurally (cursor walks), which
beats any index-proximity scheme (1D proximity can't hold graph structure).

## 6. Open next steps (prioritized)

1. **Model-side decode test** (biggest untested item, predates today): give
   a live model registry+schema+lines; test shuffle/corruption/missing;
   count instruction overhead + semantic failures. Validates or kills
   the concept as usable savings.
2. **Equal-budget benchmark**: CCC vs raw transcript vs prose summary vs
   RAG on factual/relational/constraint fidelity + downstream accuracy.
3. **Fountain layer** (offered, user hasn't said yes): random-combination
   redundancy lines over the multiline transport; measure recovery rate vs
   surviving-line fraction, head-to-head vs current parity scheme.
4. **Prime-code crosstalk measurement** (offered, user hasn't said yes):
   prime-spaced vs uniform channel plans; measure mixing products /
   cross-correlation; tests the video's non-interference claim
   computationally.
5. Semantic fragment independence (typed fragments w/ schema+deps).
6. Scale realism (does ~4.3× projection survive real registry sizes?).
7. Framing hardening (registry-fingerprint auto-rejection still
   unimplemented; 2-digit fingerprint weak; multi-error correction).
8. Zero-overhead adaptive coding for the residual ~10% (§3b).

## 7. Working notes about the user

- Communicates by voice dictation; clarify suspected transcription errors
  before acting ("error correction" once heard as "air correction").
- Values direct, unsweetened technical assessment; honest negative results
  build trust (explicitly contrasted with sycophantic experience elsewhere).
- Do not treat "Brandon" as a confirmed name. Manuscripts use
  Sidney R. Watts / S. Watts — also unconfirmed; address neutrally.
- Research program spans 1+ years: CCC, PETI, Circle CEIVE, CEII, SBU.
  Old drafts are archaeology, not live claims — ask before treating an
  old thread as active.
- Primorial-wheel paper verified and completed in `~/workspace/primorial-wheel/`.
- When they say "Yes" to a build, build it fully and measure honestly,
  including negative results.

## 8. Addendum — both offered builds completed (2026-09-27, after the summary)

### 8a. Fountain layer (`fountain.py`, `demo_fountain.py`) — BUILT and measured
LT-style erasure code over the multiline transport. Each redundancy line =
nibble-wise XOR of a pseudorandom subset of ALL data lines; `97SS` seed
headers (both sides recompute subsets from the seed — shared determinism);
per-line checksums convert silent corruption into erasures; decoder = LT
peeling (collect-and-solve, no error location). Data lines byte-identical
to the plain scheme. Encoder searches seed space: tier-2 (full data-line
coverage → any single erasure PROVABLY recovers), tier-1 (separating family
+ double coverage when 2^f > k → any ≤2 pool erasures provably recover).
Nibbles serialize as two decimal digits → digit-only property, telomere
regex, and triple tokenization all survive.
Measured (k=8, 300 trials/cell, pool erasures + shuffle): f=1: e=1→1.000;
f=2: e=2→0.657; f=4: e=3→0.873, e=4→0.427; f=6: e=5→0.593, e=6→0.250;
e>f always 0.000. Theorems: single-erasure 1600/1600 exact; two-erasure
2800/2800 exact under tier-1 (f=4). Head-to-head vs parity (200 trials):
1-digit corruption both 1.000; 1-line erasure parity 0/200 (raises — it
handles corruption, not erasure), fountain(f=2) 1.000; 2-line erasure
parity raises, fountain(f=4) 1.000. Mixed flips → erasures via checksums,
f=4 absorbs 2 flips at 1.000. 6/6 tampered fountain lines dropped as
erasures, never silently mis-decoded; ~10k successful decodes all asserted
exact. Cost: fountain line ≈2× parity line (24 vs 13 tok toy scale);
f lines ≈ 2f/k of message. Honest negatives: loses to parity when
single-digit corruption is the only threat; f=2 can't deterministically
handle 2 erasures (structural, not tuning); e>f always fails; ≤100
fountain lines, k≤97 tag limit.

### 8b. Prime-channel tests (`channels.py`, `demo_channels.py`) — MEASURED
- Video claim (prime spacings don't interfere on broadcast): FALSE as
  stated. Prime tone sets ≈ random integer sets on crest factor; crest
  tracks bandwidth, harmonic peaks lowest; P(|s|>2rms)≈0.044 for ALL sets
  (Gaussian tail). Impression was periodicity + bandwidth, not primes.
- FWM product placement (16ch, matched span): prime cuts on-channel hits
  ~1.9× vs uniform; Golomb rulers beat prime by another ~1.7×.
- Linear worst-case cross-correlation: uniform best, prime middle.
- End-to-end 16ch BPSK, 3.2M bits, independent demod: BER wash at
  realistic rates; prime's exact-null wins fragile under freq jitter.
Verdict: parallel-decode requirement satisfiable under either plan;
primes genuinely help vs nonlinear mixing but Golomb is the right
formalization. Not modeled: dispersion, phase noise, EDFA noise,
SPM/XPM, PMD/PDL, Raman/Brillouin, real filters, THz carriers.

### 8c. Remaining open (unchanged from §6)
Model-side decode test (biggest untested), equal-budget benchmark,
semantic fragment independence, scale realism, framing hardening,
zero-overhead adaptive coding.
