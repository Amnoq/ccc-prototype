# CCC Decision Tree

The documented path of decisions and forks in this exploration, kept
so we know where to go back to. Each node: date, the question,
options considered, the decision, the evidence, and status
(closed / open / forked). Numbers are stable references — cite them
in future notes (e.g. "reopening node 4").

---

## 0. Root — 2026-09-27
**Q:** Can prime patterns as a shared deterministic codebook
(both sides recompute, nothing transmitted) beat LLM token
constraints for context compression?
**Decision:** Pursue. User: "the best thing that could come from all of this."
**Status:** closed (the program this tree records).
**Methodology layer (2026-10-06):**
- Labels: the decision to pursue is a charter, not a claim. The underlying hypothesis (shared deterministic codebook beats token constraints) was **heuristic** at adoption.
- Fork: none — single go/no-go decision, not triadic.
- Why it ends here: the program was adopted; its terms were set.
- Its own chain: the entire tree below.

## 1. Representation strategy — 2026-09-27
**Q:** How do symbols get cheaper than tokens?
- **1a. Zero-cost symbols** (user idea) -> TESTED -> **DEAD**.
  No universally zero-cost symbols in cl100k_base; zero-width chars,
  BOM, combining marks all cost 1-2 tokens. Invisible != free.
  Salvage: zero *marginal* cost via BPE absorption (context-dependent).
- **1b. Color channel** (user idea: omit zeros/spaces via color) ->
  **DEAD on the text channel** (capacity zero; image path costs more
  than it saves) -> **FORK**: reborn as fiber WDM x polarization
  design. Physical-layer thread, separate from the codec.
- **1c. Structural codec** -> **ADOPTED**. Registry + prime products
  + gamma wire. Rationale fixed early: primes give *canonicity and
  shared computability*, not entropy reduction.
**Status:** closed.
**Methodology layer (2026-10-06):**
- Labels: 1a dead and 1b dead-on-text-channel — **computationally verified** (tokenizer costs measured); 1b's fiber rebirth — **heuristic** (new thread, untested here); 1c adopted — **computationally verified** as the working choice (the codec built on it).
- Fork (already triadic): 1a zero-cost symbols / 1b color channel / 1c structural codec — three candidates, one question, each tested.
- Why it ends here: the representation strategy is fixed; primes-as-canonicity (not entropy reduction) is the rationale.
- Its own chain: wire evolution (Node 2); the fiber fork (separate thread).

## 2. Wire evolution — 2026-09-27/28
**Q:** What goes on the wire?
v1 (base-64 frames + parity) -> v2 (decimal triples, tokenizer-aware)
-> v3 (Elias-gamma bitstream; no counts, no padding zeros transmitted)
-> v4 (telomeres, multiline transport, product code) ->
v5 (labels, typed directed edges, anchor statuses).
**Decision:** wire layer is tokenizer-specific (profile per
deployment); registry + prime layers are tokenizer-independent
(durable). Multiline transport is the large-message path
(order-independent, checksummed per line).
**Status:** closed (v5 current).
**Methodology layer (2026-10-06):**
- Labels: per-version token costs — **computationally verified**; the tokenizer-specific vs tokenizer-independent layering — **heuristic** (design judgment, well-grounded).
- Fork: sequential elimination (v1→v5), not triadic — each version superseded on measured cost.
- Why it ends here: v5 is the stable wire; the layering decision is fixed.
- Its own chain: Node 7 (v5 features), Node 13 (v6), Node 17 (v7).

## 3. Architecture: who parses? — 2026-09-28
**Q:** Does the model decode the wire itself?
- **3a. Model-as-parser** -> TESTED (decisive Test A) -> **REJECTED**.
  DECODE_SPEC.md is complete (independent spec-only decoder reproduces
  the reference exactly), but the mechanical burden (73 triples,
  25 gamma ops, factoring 2.2e16, 73-term checksum; 1478-token spec)
  makes it implausible at scale and vulnerable to silent arithmetic
  errors.
- **3b. Harness-parses** -> **ADOPTED**. Deterministic harness
  validates; the model receives a compact structured injection.
**Status:** closed. Consequence: the product is harness + codec, never
codec alone.
**Methodology layer (2026-10-06):**
- Labels: Test A rejection of 3a — **computationally verified**; "implausible at scale" — **heuristic** (judgment on the measured burden).
- Fork: claim (3a model parses) / polar opposite (3b harness parses) / control (spec-only decoder reproduces the reference exactly — isolates the failure to the model, not the spec).
- Why it ends here: the architecture question is settled by the decisive test.
- Its own chain: the harness product framing; Node 11's correction below.
- Backward touch: Node 11 narrowed this closure — the rejection covered *unaided* model arithmetic only; tool-assisted orchestration passes 12/12. What changed: the scope of "rejected." What didn't: the harness-parses architecture.

## 4. Second-stage compression — 2026-09-27
**Q:** Do statistical stages stack on top?
- **Cursor layer** (user's magician-trick idea: shared graph, message
  as cursor ops) -> **ADOPTED**. 1.32x via graph structure; 300/300
  fuzz round-trips; densification flat.
- **Huffman / LZ77 / stacked** -> TESTED -> **REJECTED**. All lose
  (0.63-0.98x); codebook/flag overhead exceeds savings at this
  granularity. Lesson: code the *structure*, not the statistics.
**Status:** closed.
**Methodology layer (2026-10-06):**
- Labels: cursor 1.32x + 300/300 fuzz — **computationally verified**; Huffman/LZ rejection (0.63–0.98x) — **computationally verified**.
- Fork: structural (cursor, adopted) / statistical (Huffman/LZ, the polar opposite approach) / control (fuzz round-trips show the adopted path is sound).
- Why it ends here: the stacking question is settled — code the structure, not the statistics.
- Its own chain: the "structure over statistics" lesson recurs in Node 15's law (consequence closure, not restatement).

## 5. Error-correction regime — 2026-09-27
**Q:** Parity or fountain?
- **Parity/product code** -> **ADOPTED for single-digit corruption**.
  Zero-search correction; the per-line header checksum is load-bearing
  (without it, duplicate-index ambiguity is PROVABLY unresolvable;
  attempted disambiguation picked wrong 50% of the time).
- **Fountain/LT layer** (user's whole-in-parts idea) -> **ADOPTED for
  erasure/multi-error regime**. 1-2 line erasures: 1.000 (parity: 0).
  Costs ~2x parity per line.
**Rule:** parity for corruption, fountain for erasure. Not competitors.
**Status:** closed.
**Methodology layer (2026-10-06):**
- Labels: the regime rule + measured correction rates — **computationally verified**; duplicate-index ambiguity unresolvable without the header checksum — **exact theorem** (stated as proved).
- Fork: parity (corruption) / fountain (erasure) / the provability result (the exact leg that makes the checksum load-bearing).
- Why it ends here: the error regime is partitioned by rule, not by competition.
- Its own chain: wire error-correction design; the per-line checksum stays load-bearing through v6/v7.

## 6. Prime wavelength / fiber — 2026-09-27
**Q:** Do prime-spaced channels avoid interference? (user's vision)
- Video claim as stated -> TESTED -> **FALSE** (crest tracks bandwidth,
  not primality; prime sets ~= random integer sets).
- Deeper claim (incommensurable spacing suppresses nonlinear mixing)
  -> **TRUE but Golomb rulers beat primes ~1.7x** on FWM products.
- End-to-end 16ch BPSK 3.2M-bit sim: BER wash at realistic rates.
**Decision:** **FORK** to a separate hardware/communications research
thread. Primes are not the right formalization (Golomb is). Parallel
decoding requirement satisfiable either way.
**Status:** forked, not pursued here.
**Methodology layer (2026-10-06):**
- Labels: video claim FALSE, deeper claim TRUE, Golomb beats primes ~1.7x, BER wash — all **computationally verified** (sim results).
- Fork (already triadic): the claim as stated (false) / the refined claim (true) / the polar-opposite formalization (Golomb rulers — the alternative that wins).
- Why it ends here: primes are not the right formalization for the vision; the thread forks out rather than dying — the vision survives, the formalization doesn't.
- Its own chain: separate hardware/communications thread; the "right formalization" lesson.

## 7. Expressiveness gaps — 2026-09-28
**Q:** Test B found the wire carries the skeleton without the meat
(strand labels, relation types, anchor rationale don't survive).
**Decision:** v5 closes them inside the integer/prime architecture
(label concept index; `c=(a*B+b)*B+t` typed DIRECTED edges;
`p=s*B+c` anchor statuses; all as ordinary registry concepts,
version-selected). 10/10 why/how probes reach parity with prose.
**Honest correction recorded:** the 1.75x steady-state figure was
information-asymmetric (v4 structure omitted what the prose
contained). Apples-to-apples v5 toy number: 1.27x.
**Status:** closed.
**Methodology layer (2026-10-06):**
- Labels: v5 closes the gaps (10/10 probes) — **computationally verified**; the 1.75x→1.27x honest correction — **computationally verified** (information asymmetry identified and re-measured).
- Fork: none — gap closure verified against the fixed probe set.
- Why it ends here: expressiveness is closed inside the integer/prime architecture.
- Its own chain: v5 as the stable wire for the M-series; the honest-correction practice (recur in Nodes 12, 19).

## 8. Scale economics — 2026-09-28
**Q:** Does the ratio grow, hold, or collapse at real scale?
**Tested:** synthetic research graphs, B=174-1030, densities 0.5-2.0,
terse subject-grouped prose, cl100k_base, 3 seeds/cell.
**Result:** steady-state ~**2.2x, flat across 6x scale-up**. No
collapse, no unbounded growth. Toy 1.27x was JSON-injection
pessimism; grouped minimal injection converges to wire size.
Cold start amortizes in ~2-3 sessions.
**Fell out:** `encode_lines_balanced` (weight-based chunking;
count-based overflows the 999-triple v3 header past B~300 when strand
products cluster at the message head).
**Status:** closed. Durable number: ~2.2x at equal information.
**Methodology layer (2026-10-06):**
- Labels: 2.2x flat across 6x scale-up (3 seeds/cell) — **computationally verified**; `encode_lines_balanced` fallout — **computationally verified** (bug surfaced by measurement, not review).
- Fork: scale-up cells (the fork is parametric: B=174–1030 × densities 0.5–2.0); the opposite under test was collapse-or-growth, both eliminated — flat is the finding.
- Why it ends here: the scale question is settled; the durable number is fixed.
- Its own chain: feeds Node 9's framing; the weight-based chunking fix.

## 9. Product framing — 2026-09-28
**Q:** Is 2.2x worth building for?
- **9a. Cost play** ("cheaper tokens") -> **REJECTED**. Prompt caching
  captures ~10x on the repeated-context workload; CCC saves ~$0.03/
  session at Sept-2026 prices. The cost argument died with caching.
- **9b. Capacity + integrity play** -> **ADOPTED (under test)**.
  2.2x effective *structured* memory in-window (caching can't extend
  the window) + tamper-evident wire. Levers: OpenAI's 272K 2x price
  cliff; deferring lossy summarization.
- **9c. Research contribution** -> **OPEN**. Publishable regardless of
  product economics.
**Status:** 9a closed, 9b open, 9c open. Decision brief artifact:
`ccc-decision-brief` (goal files).
**Methodology layer (2026-10-06):**
- Labels: 9a rejected (caching captures ~10x; $0.03/session) — **computationally verified**; 9b adopted-under-test — **heuristic** (the "under test" is doing the work); 9c open — no claim.
- Fork (already triadic): 9a cost play (dead) / 9b capacity+integrity (live, under test) / 9c research contribution (open).
- Why it ends here: the framing is fixed — 9a closed by arithmetic, 9b/9c open by design.
- Its own chain: Node 10's MVP scope is the test 9b was adopted under.

## 10. Memory-system reframing — 2026-09-28 (current)
**Q:** What is CCC, as a product?
**Decision:** a memory **codec + transport**, not a memory system.
Complements Zep/Letta/Mem0 (stores with retrieval, no portable
exchange format). Stack: registry (store) -> v5 wire (verifiable
checkpoint/transport) -> harness (parse/inject); cursor layer as
session-local working memory.
**Hard problems, ranked:** extractor (gating) > entity resolution >
read-path retrieval (CCC meets RAG) > registry evolution >
time/conflict (v6: temporal validity on edges).
**Gating experiments:** extractor probe-parity per dollar;
entity-resolution accuracy.
**Status:** OPEN — MVP scoped 2026-09-28 (HARNESS_MVP_SCOPE.md):
build only the extractor gating experiment (M1–M4); retrieval,
evolution, and temporal work explicitly deferred; kill criteria
written down in advance. **M1 DONE 2026-09-28** (`memory_harness.py`:
schema, verifier, SQLite store, phase-1 ER, telomere-wrapped v5
checkpoints, order-independent restore, grouped injection;
`test_m1.py` 14/14). **M2 DONE 2026-09-28** (`extractor.py`:
self-contained prompt + `extract_with_repair` driver, repair ≤2;
`M2_REPORT.md`: 3 real transcript chunks, repairs 1/0/0, all v5
round-trip clean; author-as-LLM is the open caveat, naive-model trial
still required; economics preview: extraction 8868 tok vs ~2515
tok/session saving → break-even ≈3.5 sessions). **M3 DONE 2026-10-03**
(`M3_REPORT.md`): 10 why/how probes written blind with prose answers locked
before extraction; extraction as a separate subagent pass (never saw probes)
— 34 concepts, verifier PASS attempt 1 (0 repairs), v5 round-trip clean.
**Parity 9/10, zero hallucinations** (sole partial omission: P6, the
vector-store competitive contrast — anchor notes are extracted but dropped by
the grouped injection, a read-path finding). **Break-even 5.28 sessions** on
the 1.2k-token chunk (below the 2–4k target): extraction JSON (2586 tok) runs
2.1× the prose; the 3.3× compression (1210→369) comes from the v5 codec +
injection, not extraction. Against M4 §3.6: parity/hallucination/verifier
bars met, cost bar missed. **M3R DONE 2026-10-03** (gray-zone provision:
one revision + one re-run, `M3R_REPORT.md`, `extractor_rev1.py`): density
revision (12–22 concepts, labels ≤10 words, notes ≤8 words, cut-on-doubt
edges) re-run on chunk 1 (2852 tok, target band, fresh to R2) with 10 new
blind probes — verifier clean, **parity 7/10** (misses are mechanistic
justifications: mappings, rationales, caveats; claims/relations intact),
zero hallucinations, **break-even 2.03 lab / 1.71 deployment** (≤3 bar met
under both conventions; output/prose 2.14→0.56). Trade-off isolated: density
buys cost at the price of why-depth. **M4 DECIDED 2026-10-03: provisional GO.**
Rationale: cost bar met under both conventions with the revision working as
targeted; parity at gray-zone boundary with zero hallucinations; n=1 per
condition cannot settle fluctuation — the decision will be revisited once
distributions across a chunk corpus exist. Kill criteria remain armed: if the
corpus distribution settles below the bars, the harness stops. Next: corpus
evaluation (R2 extractor across ~10 chunks, 2–4k tok each; parity + break-even
distributions). Corpus material not yet in hand — all four existing chunks used.
**CORPUS DONE 2026-10-03** (SID-15, `corpus_runs/CORPUS_REPORT.md`): 12 chunks
from map/derivations/decision-tree/operator-audit; full blind pipeline per chunk
(separate probewriter + extractor agents, blind scorer, deterministic costs).
**Break-even: mean 2.05 lab / 1.72 deployment, range 1.69–2.27 / 1.47–1.88 —
all 12 under the ≤3 bar (tight distribution: the reliable finding). Verifier
12/12 first-pass, 0 repairs. Hallucinations 0/120.** **Parity: mean 4.83/10,
range 1–8** — confounded by probe-difficulty variance (c11 probes exact
numbers/formulas; c04 headline verdicts) and stricter subagent scoring vs
hand-scored M3/M3R. Omission taxonomy (the real finding): R2 keeps
verdicts/relations/statuses/open questions; drops numbers, mechanisms,
replacement-forms, uncoined concepts, cross-chunk bridges — failure mode is
omission, never fabrication. Frontier quantified: (9/10, 5.28) vs (~5/10, ~2)
— the ≥9/10 AND ≤3 combination does not exist in this design space.
**M4 provisional GO UNDER REVIEW**: accept the redefined product
(verdict-and-relation memory at ~2 sessions, zero fabrication risk) or hold
the original faithful-memory bar.
**Methodology layer (2026-10-06):**
- Labels: M1 14/14, M2 round-trips, M3 9/10, M3R 7/10, corpus 12/12 ≤3 bar with tight distribution — **computationally verified** throughout; M2's author-as-LLM caveat and M3/M3R n=1 fluctuation caveat — **heuristic** (owned in-record); M4 provisional GO — **heuristic** (the user's judgment call, explicitly provisional, kill criteria armed).
- Fork: M3's blind probes (claim: parity) / verifier first-pass (control) / break-even economics (the opposite pressure — cost vs fidelity, the frontier quantified as (9/10, 5.28) vs (~5/10, ~2)). M4 itself is triadic: GO / NO-GO / provisional-with-distribution.
- Why it ends here: the M-series established the extractor path and its costs; the corpus gave the distributions M4 was waiting on.
- Its own chain: R3 (Node 11), Exp2 (Node 12); the M4 decision still the user's.
- Backward touch: the corpus's tight distribution (all 12 ≤3, range 1.69–2.27) touched M3's n=1 fluctuation caveat — resolved in favor of reliability. What changed: the caveat is retired. What didn't: M4's provisional status.

## 11. R3 evidence-preserving extractor + full up-stack — 2026-10-03
**Q:** Can the R2 omission taxonomy be attacked without losing the cost bar?
**Decision:** R3 revision (numbers rule, replacement rule, ~12-word evidence
notes, note-carrying injection), same 12 locked probes, full blind pipeline.
**Results** (`corpus_runs/R3_FINAL_REPORT.md`), all computationally verified:
parity 4.83 → **7.42/10 injection** (every chunk gained/held; c06 10/10,
c11 1→8.0); break-even 1.72 → **2.26 deployment** (all 12 still ≤3); zero
fabrications in 120 probes. Probe classes: NUMBER 0.20→0.73, VERDICT
0.40→0.73, MECHANISM 0.54→0.74 — numbers rule worked as designed; remaining
deficit is mechanism-grade why. **New finding:** v5 wire has no anchor-note
channel — R3's note-preserved evidence rides the injection but not the wire
(7.42→6.79 step down through v5); note transport is the next codec upgrade
(v6). Up-stack: 12/12 deterministic decode fidelity perfect, mean wire
~144 tok. **Status:** CLOSED — R3 is the current extractor. Open: v6 note
channel (Node 2 follow-up), mechanism-depth (hard problem #1 unchanged).
**Correction to Node 3:** its rejection covered *unaided model arithmetic*
only; the up-stack tested *tool-assisted model orchestration* (deterministic
code for validation/wire/fidelity, models for extraction/rehydration) and
passed 12/12. Scope of the Node 3 closure narrowed accordingly.
**Methodology layer (2026-10-06):**
- Labels: parity 7.42, BE 2.26, per-class gains, 12/12 fidelity, zero fabrications — **computationally verified**; the 7.42→6.79 wire gap — **computationally verified** (same locked probes, so the gap is isolated to the wire).
- Fork: R3 revision (claim: attacks the omission taxonomy) / R2 baseline on the same 12 locked probes (control) / the ≤3 cost bar (the opposite pressure — the revision must not buy parity with cost; it didn't: 2.26).
- Why it ends here: R3 is the current extractor; the revision worked as designed.
- Its own chain: v6 note channel (Node 13); the rescore prediction (Node 19).
- Backward touch: this node's Correction narrowed Node 3's closure (see Node 3's layer). Node 13 reframed the 7.42→6.79 gap as a representation gap, not decode corruption. Node 19's scorer drift reframed the 6.79/7.42 absolutes as protocol-relative.

## 12. Experiment 2: entity resolution across chunks — 2026-10-03
**Q:** (Node 10 gating experiment) Can cross-chunk coreference be merged at
≥0.95 merge precision?
**Design:** TF-IDF candidate generation over labels+notes (sentence-transformers
uninstallable — disk full; TF-IDF substituted, worked) → LLM adjudication →
merge. Registry via union-find; c12 held out.
**Phase A** (`corpus_runs/EXP2_REPORT.md`): 27,952 pairs mined from 247
concepts; 300 labeled by 3 blind judges (79 SAME/214 DIFFERENT/7 UNCERTAIN);
human audit of all 79 proposed merges: **0 false → precision 1.00** (95% LB
0.962; sensitivity 0.987 counting the one borderline M002 as wrong).
**Bar cleared** (computationally verified). TF-IDF alone as merge rule peaks
at 0.875 — the adjudicator, not the ranker, earns the bar.
**Phase B2** (post-hoc merge hook = scope's phase-1 design): top-5 retrieval +
adjudication on held-out c12: 2 merges proposed, both correct (**precision
1.00, recall 2/3** — the miss was retrieval, E111 outside top-5, plus
label-only adjudication limits); 0 false merges; duplicates 3/19 → 1/19.
**Phase B1** (registry-in-prompt, architecture comparison): 8 reuses — 4 true,
4 granularity-borderline, 0 clean-false; caught the D_log alias B2 missed
(full-text arXiv evidence) but merged 2× as aggressively with half debatable,
at ~5.5k prompt tokens/extraction.
**Decision:** deploy the post-hoc merge hook; keep extraction blind (B1's
operating point doesn't clear the bar on its debatable merges; B2 does).
Recall lever is retrieval density (citation/formula signals) + full-text
evidence for near-matches — not adjudicator strictness. Watch item:
M002/H036 dual-membership tension (1 in 79) — concept-granularity merging
needs dual-membership and role-vs-entity rules before scale-up.
**Status:** REOPENED 2026-10-03 — dual-judge replication found shared
ontology bias (judge 1 + my audit both waved through question+verdict,
verdict+evidence, result+control as SAME). Full rigorous close-out under
principle P (strict, decided): posit≠resolution. See EXP2_REPORT.md
"Rigorous close-out" section. Corrected numbers:
- Phase-A adjudicator precision **73/78 = 0.936** (0.924 counting H054
  uncertain as wrong) — **bar NOT cleared under P** (was: claimed 1.00).
  False merges: H037, H047, H053, H107, M002. Missed merges added:
  H060, M008. (Under loose principle Q: 0.962–0.974, bar met — Q not
  adopted; needs status-annotated entities, v6 design note.)
- Below-floor: 300 random pairs, two judges, 300/300 agreement, 0 SAME.
- 12-fold CV: retrieval recall@5 = 0.95, recall@1 = 0.67; post-hoc hook
  **precision 98/117 = 0.84, recall 98/126 = 0.78** (full audit of all
  115+117 proposed merges; 17 truth-label flips + registry rebuild).
- Registry v2: 181 entities, 41 with aliases (all 12 chunks;
  `corpus_runs/exp2_registry_v2.json`). Hook caught 2 duplicate entities
  the registry missed (uncertainty law ×2, Weil ×2).
**Decision (revised):** post-hoc merge hook still the architecture, but
its measured precision is 0.84, not 1.00 — needs the strict adjudication
standard + exact-identifier retrieval (arXiv/formula) for the D_log-type
recall gap. The 0.95 bar failure is small, real, and principle-relative —
documented in EXP2_REPORT.md with epistemic labels.
**Status:** CLOSED under P. Next: v6 note channel + temporal validity
(status-annotated entities would support principle Q).
**Methodology layer (2026-10-06):**
- Labels: Phase-A/B measurements, 12-fold CV, hook 0.84/0.78, registry v2 — **computationally verified**; the bar verdict itself is principle-relative (P: 0.936, not cleared; Q: 0.962–0.974, cleared) — labeled, not hidden.
- Fork (already triadic): principle P strict (0.936, bar NOT cleared) / principle Q loose (0.962–0.974, bar met) / below-floor control (300 random pairs, 300/300 agreement, 0 SAME — the instrument isn't hallucinating).
- Why it ends here: closed under P — the strict standard the method adopted.
- Its own chain: v6 status-annotated entities (Node 13); typed relations (Node 18); the Q design note.
- Backward touch: the dual-judge replication reframed Phase A *within* this node (1.00 → 0.936 under P) — the method catching its own shared-ontology bias and correcting on record. What changed: the precision claim. What didn't: the post-hoc-hook architecture.

## 13. v6 codec: note channel + status-annotated entities — 2026-10-03
**Q:** What does the next codec version carry that v5 cannot?
Two findings converge on the same build:
- **R3 (Node 11):** v5 wire has no anchor-note channel. R3's note-preserved numbers ride the grouped injection but not the wire export — the 7.42 → 6.79 parity step is a representation gap, not decode corruption. Notes must travel on the wire, not only in injection.
- **Exp2 close-out (Node 12):** principle P (posit ≠ resolution) is load-bearing only because the registry has no status/polarity field. Status-annotated entities (hypothesized / verified / killed / superseded, plus temporal validity) would let the registry carry principle Q (one investigation = one entity across its lifecycle) safely — Q was measured 0.962–0.974 on the same data, bar cleared under Q.
**Scope (v6):**
1. Note channel in the wire format (anchor notes travel with their entities).
2. Per-entity status annotation + temporal validity.
3. Decode protocol stays resident on the receiving side (user's standing accounting principle, 2026-10-03): extraction/decoding protocols are a one-time cost; the wire carries only the message. v6 decode-spec update does not count toward marginal break-even.
**Design constraint:** status must survive rehydration — a killed posit merged under Q must rehydrate as killed, never as live. This is the failure the strict P ruling was protecting against; v6 must make Q's safety mechanical, not adjudicator-dependent.
**Status:** open (design first, then implementation; verify decode fidelity 12/12 + parity vs R3 7.42 baseline). Linear: SID-16.
**Close-out 2026-10-03:** implemented and measured. Codec (`build/decode/validate_message_v6`, `encode/decode_wire_v6`, `apply_entity_status`), harness (`to_v6_export`, `verify_roundtrip_v6`), independent decoder (`spec_decode_v6.py`, zero codec imports) — 12/12 fidelity incl. notes + statuses, 246/246 note survival, merge-lattice unit tests pass. Wire mean 553 tokens (v5: 144 — the delta is the note channel, as designed). BE_wire mean 2.36, 11/12 ≤3 (c09 3.07, smallest chunk — chunk-size effect, reported conservatively). One design correction mid-build: notes first rode as raw bits in the triplet channel (BE_wire 3.21 — worse than the injection path); re-cut as literal NOTETEXT (text as text), BE_wire 2.36. Full report: `corpus_runs/V6_REPORT.md`. Spec: `DECODE_SPEC.md` v6 section.
**Status:** CLOSED (implementation + measurement). Open follow-ups: blind parity re-score (predicted 6.79→7.42 recovery, NOT claimed); merge-hook status integration vs status-annotated exp2_registry_v2.
**Methodology layer (2026-10-06):**
- Labels: 12/12 fidelity incl. notes+statuses, 246/246 note survival, BE_wire 2.36 — **computationally verified**; the recovery prediction — **conjectural** (precise, NOT claimed — the "NOT claimed" is doing the work).
- Fork (within the build): notes-as-raw-bits (tested: BE 3.21, worse — the polar opposite that lost) / NOTETEXT literal (adopted: BE 2.36) / independent spec-decode 12/12 (control).
- Why it ends here: v6 is implemented and measured; the note channel exists.
- Its own chain: the rescore prediction (Node 19); v7 (Node 17).
- Backward touch: reframed Node 11's 7.42→6.79 step as a representation gap (notes had no wire channel), not decode corruption.

## 14. Badge-weighted retrieval (cups-session follow-up) — 2026-10-03
**Q:** Do paraphrase-invariant "badges" (arXiv IDs, formulas, distinctive
numbers, `D_log`-style idents) improve cross-chunk entity retrieval, given
TF-IDF's tokenizer destroys them?
**Method:** locked 12-fold v1 registries; TF-IDF reimplemented verbatim
(baseline reproduced: 0.667/0.938); badge patterns fixed a priori;
variants V0–V5 with no tuned weights; 144 SAME pairs.
**Result:** RANKING NEGATIVE — naive fusion hurts (recall@1 0.667→0.569,
27 losses vs 5 wins); best variant +1 recall@5 at −0.07 recall@1.
Precision-as-evidence POSITIVE but modest: shared rare badge lifts
SAME-precision 5× on truth pairs (0.08→0.43), MERGE-precision 4× on hook
candidates (0.09→0.38), 6× enrichment (23% vs 3.8%). Rescue: 1/9 misses.
The D_log case NOT solved (entity text lacks the badge; needed full-text
evidence, as B1 showed).
**Explanation:** badges identify TOPIC, not ENTITY — blind to epistemic
role, the exact distinction principle P enforces. The cups moral, made
precise: badges tell notations apart; entity identity needs arrangement
(status).
**Decision:** do not fuse into ranker; DO surface shared rare badges as
explicit adjudicator evidence (scoped follow-up for the hook prompt).
Report: `corpus_runs/EXP2_BADGES.md`.
**Status:** closed (negative result with a scoped positive).
**Methodology layer (2026-10-06):**
- Labels: ranking negative (0.667→0.569), precision lifts (5×/4×/6×), TF-IDF baseline reproduced — **computationally verified**; "badges identify TOPIC, not ENTITY" — **heuristic** (interpretive, well-supported: blind to epistemic role, which is exactly principle P's distinction).
- Fork (already triadic): ranking fusion (hurts) / precision-as-evidence (helps, modestly) / TF-IDF baseline reproduced verbatim (control).
- Why it ends here: the question is answered — do not fuse; do surface as adjudicator evidence.
- Its own chain: the scoped hook-prompt follow-up; the cups moral made precise.

## 15. Process-symbols: which process compacts best — 2026-10-03
**Q:** (user's) We have symbols for words/concepts; what about symbols for
*processes* that unfold to words/concepts? And which kind of process
compacts information most efficiently?
**Method:** smoke measurement, hand-encoded upper bound. 6 mechanism
entities from exp2_registry_v2 (E017 deformation, E023 territory-removal,
E152 D_log pipeline, E049 explicit formula, E000 sieve complex, E057
square dictionary) × 4 opcodes (ITER, PIPE, BRIDGE, INVERT) + v6 status
tag. Baseline = label+aliases+notes literal text. Metric: conclusions
preserved per wire token; regeneration fraction judged by experimenter-as-
interpreter. Script: `exp2_procsym.py`, rows: `corpus_runs/exp2_procsym_rows.json`.
**Result:** total 1.77× token reduction (313→177), conclusions/token
0.083→0.147. Per-opcode: INVERT 3.56×/100% regen (E000), ITER 3.38×/80%
(E017) but 0.98×/33% (E023), PIPE 1.33×/33%, BRIDGE 0.93–1.36×/33–67%.
**Law found:** compression ratio tracks *regeneration fraction* — the
share of conclusions the interpreter derives rather than the symbol
asserts. Rich consequence closure (inversion, generative iteration with
many derivables) wins big; restatement-processes (a duality whose formula
IS the content, E049 0.93×) break even or lose; asserted provenance
(bugfix tags) and conceptual identifications don't compress.
**Corollaries:** (a) 5/6 mechanisms needed the @status tag — processes
don't regenerate epistemic status; the v6 status enum is a necessary
companion, not optional. (b) Opcode reuse (ITER ×2) doesn't guarantee
payoff — consequence closure does. (c) Interpreter cost amortizes over
uses, but each opcode's semantics must be shared exactly or unfolding
diverges (fidelity untested — next experiment: blind decode regeneration).
**Status:** closed as smoke test (feasibility + law established).
Report: `corpus_runs/EXP2_PROCSYM.md`. Open: blind regeneration fidelity;
opcode-set cover over the full mechanism inventory.

### Refinement 2026-10-03 (user redirect): one operator
User: the 5-opcode taxonomy is overthought; the clue is binary distinction
— "the 2D plane is converted to 3D geometry through perturbation, which
requires another dimension or time itself." Reduction test
(`exp2_procsym_reduce.py`, triples in `corpus_runs/exp2_procsym_triples.json`):
recast each mechanism as (seed-plane, binary perturbation, time-axis).
Result: big wins (>=3x) ⟺ FULL perturbation shape + rich closure (E017:
binary marking through prime-time; E000: binary Möbius signs unfolding
aggregation) — holds for both winners, and all four band cases
(0.93–1.36x) lack the full shape. Refined law: compression ≈
shape-fit × closure-richness. Consequence: the opcode set collapses to
ONE — PERTURB(seed, binary-op, axis). PIPE/BRIDGE shapes score in the
restatement band, where literal text does as well; they don't earn a
process-symbol. Codec implication: PERTURB + literal text + status tags
is the complete process-symbol design; everything else stays words.
Status: user's redirect absorbed; single-operator hypothesis recorded.
Open: blind regeneration fidelity; wider mechanism inventory.

### Fidelity test 2026-10-03: blind regeneration from PERTURB triples
**Q:** does triple+observables+spec regenerate conclusions without drift?
**Method:** spec v1 fixed before decoding (`corpus_runs/PERTURB_SPEC_V1.md`);
decoder = experimenter under anti-smuggling rule (corpus names only for
derived properties); compute allowed, corpus text forbidden. 3 triples:
E017, E000 (full shape), E049 (predicted failure).
**Result:** 15 conclusions -> 5 REGENERATED, 4 DRIFT (narrow logged gaps),
3 LOST (all predicted, T3), 3 status carried. E017: survivors re-derived
structurally + computed (2161 = 2160 twin lowers + {2} — edge case the
original note lacks); S(z) table + limit 1.3203247 verified by code.
E000: Moebius executed exactly on small case. E049: total loss as predicted.
**Design outputs (spec v2 requirements):** observables need prescriptions
(renormalization); seeds must carry domain identifications; exact identities
need DERIVE sub-capability or asserted tags; compute + textbook methods are
legitimate interpreter capabilities.
Report: `corpus_runs/EXP2_PERTURB_FIDELITY.md`.
**Status:** closed as smoke test. Open: spec v2; wider inventory; true-blind
decoder (second agent with no corpus context).

### Audit 2026-10-03: second blind decoder (subagent, pre-registered brief)
**Method:** independent decoder, `DECODER_BRIEF_V1.md` (no corpus files,
no recalled conclusions, no topic web-search; T3-first calibration).
**Result:** harsher than v1 and right in six places — v1 had smuggled the
proper-multiple exception (decoder proved the literal triple derives a
degenerate readout), overstated constant-value (code used recalled
prescription), and missed naming/aggregation gaps. Reconciled: 2 thin
REGENERATED, 3 DRIFT with derived content, 7 LOST, 3 carried. T3 3/3 LOST
+ structural finding: T3 is not a well-formed PERTURB instance (no binary
state) — spec should reject such triples. Hypothesis not refuted; the
triples were too thin. Output: 9-item spec-v2 requirements list
(prescriptions, domain identifications, DERIVE/asserted-tags, edge-case
conventions, marked/unmarked reading, finite-vs-infinite axis,
aggregation structure, observable-name definitions, well-formedness).
Report: `corpus_runs/EXP2_PERTURB_FIDELITY.md` (audit section).
**Status:** closed. Open: spec v2; true-blind decoder pool; wider inventory.

### Round 2 2026-10-03: spec v2 closes the gaps
**Method:** spec v2 (9 audit requirements incorporated) + v2-conformant
triples (generative content only, audited clean) + second blind decoder
under new pre-registered brief.
**Result:** 7 REGENERATED / 1 DRIFT / 1 UNVERIFIED / 1 REJECTED(T3 at
gate). 7 of 9 gaps fully closed; mu-identity half-closed (explicit
partial equation via named inclusion-exclusion, statement unpinned —
asserted-tag fallback stands); gate rejection confirmed by design.
Decoder found 4 minor new spec issues (a–d), none blocking; no triple
flaws; no smuggling detected in audit. The v2 format — PERTURB + well-
formedness gate + prescriptions + conventions + polarity + explicit axis
+ derive/asserted + UNVERIFIED marking — regenerates faithfully where
the perturbation shape holds.
**Status:** closed. Spec v2.1 (issues a–d) and wider inventory open.

### Round 3 2026-10-03: wider inventory under spec v2.1; law refined
**Method:** spec v2.1 + 6 new mechanism triples (E025, E004, E014, E050,
E015, E071) + T1-mu retest; pre-registered per-item predictions; third
blind decoder, same hard rules.
**Result:** 19 observables -> 16 REGENERATED (10 substantive), 0 DRIFT,
0 LOST, 3 UNVERIFIED (all expected: face-count data, zero list, Selberg
weights). Predictions 6/7 (T6 predicted MIXED came out GOOD — informative
miss). T1-mu closed under the functional-role prescription (equation
verified on 3 points). Genuine independent recomputations: Lambda check
5.3e-15, S(X) values incl. exact 0.969931 match, GF -zeta'(s+1)/zeta(s+1)^2
derived precisely (corpus note's form = same up to s-shift).
**Law refined:** premise-completeness replaces perturbation-exclusivity.
Two sufficient shapes: (a) perturbation-unfolding (flagship: T1, T4);
(b) precise definition + named method + computability (T5, T6, T8).
Verdict determined by absent premise class: generative->REGENERATED,
data->UNVERIFIED, relation/method->LOST, partial->DRIFT.
**Open:** spec v2.2 (W1 as "binary-structured elements"); wider inventory
continues; decoder pool.
Report: `corpus_runs/EXP2_PERTURB_FIDELITY.md` (round-3 section).
**Methodology layer (2026-10-06):**
- Labels: smoke-test ratios, fidelity counts (5/15, 7/9, 16/19), blind-decoder audits — **computationally verified**; the compression law (refined: premise-completeness) — **conjectural** (precise, survived Rounds 2–3 with 6/7 predictions, not a theorem); the user redirect to one operator — **heuristic** (user's steer, validated by the reduction test).
- Fork (method-level, triadic): smoke measurement (claim: processes compact) / blind fidelity decode (opposite pressure: does it regenerate without drift?) / second blind decoder audit (harsher control — caught v1's smuggling). Within the finding: perturbation-exclusivity (first hypothesis) / premise-completeness (the polar opposite that won in Round 3).
- Why it ends here: closed as smoke test — feasibility and the refined law established; syntax question superseded by Node 16.
- Its own chain: Node 16 (natural forms replace the syntax); spec v2.2; wider inventory; decoder pool.
- Backward touch: Node 16 reframed this node's PERTURB taxonomy as invented — the findings kept, the syntax re-derived from the paperwork.

## 16. Natural forms: the paperwork already had the codec's shapes — 2026-10-03
**Q:** (user's steer) Is the invented codec taxonomy overthought again?
Mimic how the research paperwork is already naturally formed.
**Method:** surveyed prime-sieve-geometry paperwork (DERIVATIONS.md
D1–D8, DECISION_TREE.md, archive_dead_ends.md).
**Catalog:** F1 D-item (rule + staged generation + inline verification
+ honest boundary + honest label); F2 decision-tree node (Q/Decision/
Evidence/Status); F3 dead-end guardrail (Tried/Result/Transfer);
F4 verdict (status + consequence); F5 identification (X⟷Y + limits);
F6 maxim ("never put the answer in by hand").
**Encoding map:** M1 D-item -> mechanism encoding (replaces PERTURB
triple syntax; same content in his fields + the honest boundary, which
the triple lacked); M2 guardrail; M3 verdict (extends v6 status with
consequence); M4 bridge identification. Findings kept (premise-
completeness law, 9 audit requirements, fidelity method); syntax
re-derived. Report: `corpus_runs/NATURAL_FORMS.md`.
**Round-4 test:** 3 mechanisms re-encoded as terse D-items; blind
decoder scored checksums (carried values recomputed) + boundary probes.
Result: 8/8 stages regenerated, 6/6 checksums match (0 mismatches),
3/3 blocking probes correctly blocked, 2/2 establishment probes
correctly allowed, 0 flaws. The D-item syntax preserves everything
v2.1 carried, and adds: checksums as mechanical drift detectors
(the n=2 edge case surfaced through one) and the honest boundary as
an enforced stop-line (5/5 probes correct).
**Status:** closed. The steer is validated: derive codec forms from the
paperwork, don't invent them. Open: full inventory in D-item form;
M2–M4 encodings; wire integration.
**Methodology layer (2026-10-06):**
- Labels: the catalog, the encoding map, round-4 test (8/8, 6/6, 5/5 probes) — **computationally verified**; the steer itself ("derive, don't invent") — **heuristic** (user's methodological principle, validated here).
- Fork: invented taxonomy (rejected) / paperwork-derived forms (adopted) / round-4 blind test (control — checksums as mechanical drift detectors).
- Why it ends here: the steer is validated; the syntax question is settled.
- Its own chain: Node 17 (the v6 status enum was the audit's load-bearing item); M2–M4 encodings; wire integration.
- Backward touch: reframed Node 15's opcode taxonomy (findings kept, syntax re-derived) and triggered Node 17's status-enum audit.
## 17. v7 status alignment: the work's own labels on the wire — 2026-10-03
**Q:** (user's audit prompt) The codec still uses invented forms where the
paperwork has natural ones — what adjusts? Load-bearing item: the v6
status enum.
**Gap:** v6 (unstated/hypothesized/asserted/verified/killed/superseded)
collapses his sharpest distinction — exact (theorem/identity, proof
carried) vs computationally verified (numeric check passed, scope
stated) — into one "verified", and has no room for the genre half of
his labels ("classical theorem, reframed — not a new theorem").
**Design:** v7 strength ordinal 0–6 (unstated/heuristic/conjectural/
verified-numeric/exact/killed/superseded) + anchor-level 2-bit genre
(none/original/reframed/identification). Genre is not an ordinal, so it
rides the anchor, not the entity; entity-status records stay
strength-only and the merge lattice stays one-dimensional (6>5>4>3>2>1>0,
newer epoch wins, terminal beats live at equal epoch — P-safety
preserved). Migration is lossy-conservative: legacy "verified"→
verified-numeric, never exact (the codec may not conclude more than was
established); open_question/hypothesized→unstated (questions are not
claims; question text rides the note). Wire: version 7, anchors pack
((s*G+g)*B+c)*B+n, G=4; body framing byte-identical to v6. Report:
`corpus_runs/V7_STATUS_DESIGN.md`.
**Validation:** 12/12 independent decode from DECODE_SPEC.md's v7
section alone (spec_decode_v7.py, no codec imports), field-exact
including status names, genre names, notes, entity statuses; 12/12 v7
codec round-trips; v6 suite still 12/12 (frozen path untouched); genre
round-trips through the full wire on synthetic anchors; wire delta
+24 chars on 1679 (+1.4%, break-even unaffected). Merge lattice
spot-checked: terminal wins ties, newer epoch revives, weaker
same-epoch loses.
**Status:** closed. Standing principle recorded (MEMORY.md 2026-10-03):
"self-deriving system" refers to prime distribution ITSELF, not the
codec; the codec work got over the hump when "this" stopped being
treated as different from "that" — the instrument and the subject are
the same structure. Open: R4 extractor emitting (strength, genre)
directly; typed registry relations (item 2 of the audit); adjudicator
output as decision-node (item 3).
**Methodology layer (2026-10-06):**
- Labels: 12/12 independent decode field-exact, 12/12 round-trips, v6 suite still 12/12, wire delta +1.4% — **computationally verified**; the standing principle (instrument/subject same structure) — **heuristic** (user's framing).
- Fork: v6 enum (the problem — collapses exact vs verified-numeric) / v7 design (the fix: strength ordinal + genre anchor) / independent spec-decode (control — the design survives contact with a decoder that never saw the codec).
- Why it ends here: the status alignment is designed and validated.
- Its own chain: Node 18 (R4 emitting v7-native); Node 20 (wire build); typed relations (item 2, done in Node 18).
- Backward touch: reframed v6's "verified" via lossy-conservative migration (legacy verified→verified-numeric, never exact — the codec may not conclude more than was established).
## 18. R4 extractor + typed alias relations — 2026-10-03
**Q:** (user authorized both) (a) extractor emits v7-native labels
directly; (b) registry aliases get his relation types. Plus user's
steer: the DNA codon/telomere frame is the more reachable version —
consider it.
**R4 extractor (`extractor_rev3.py`):** anchor vocabulary replaced with
exact / computationally_verified / conjectural / heuristic / killed /
superseded (each defined in-prompt: exact needs the derivation present;
computationally_verified needs the check AND its scope; ties go to the
weaker claim) + optional genre (original/reframed/identification).
Base SCHEMA_SPEC left intact as archaeology; the override is explicit
in-prompt ("SUPERSEDES"). One prompt gap found during the pilot and
fixed: open questions take no strength status (kind open_question,
loops, anchor omitted). `extract_with_repair` gained an optional
schema_reminder (default unchanged).
**Pilot (corpus_runs/r4/c02, c02 re-extracted under R4):** 21 concepts,
18 anchors, 10 edges, 3 loops. Statuses: 14 exact / 2
computationally_verified / 2 heuristic (old: 8 asserted / 7 verified /
2 open_question / 1 superseded). Genres: 7 reframed / 4 original / 1
identification. Validates clean; v7 round-trip + independent
spec-decode both exact. Caveat (non-blind pilot): several old
"asserted" became "exact" on "derivation carried in text" grounds
(maxim by construction; limit argument; explicit-formula application) —
a second judge should audit those calls before the 12-chunk battery.
**Typed aliases (`corpus_runs/exp2_alias_types.json` sidecar; v2
untouched):** all 66 aliases across 41 entities classified into 8 types
from his cross-ref vocabulary: restatement 37, facet 9, lifecycle 5,
instance 4, evidence 4, identification 3, reframing 2, ledger_entry 2.
Report: `corpus_runs/TYPED_RELATIONS.md`. Two cases prove the value:
E009/c11/c22 (a killed hope "positive region exists" sitting under the
obstruction that killed it — lifecycle + superseded status makes it read
correctly instead of as a contradiction); E095 (ledger HAVE grouped
with two MISSINGs — ledger_entry blocks HAVE/MISSING conflation).
Curated single pass; second judge recommended on the 29 non-restatement
calls.
**DNA steer:** recorded in AGENTS.md as standing convention — DNA frame
(codons/triplets, telomere-wrapped messages, registry as universal
codebook) leads codec explanation because it is the reachable version,
and it is not just metaphor: DNA is itself a self-deriving system
(compact code + reader; organism derived, never put in by hand).
Explanatory layer only — the wire keeps speaking his epistemic labels
(Node 17). Used once so far: typed aliases glossed as synonymous codons
(different spellings, one entity, typed synonymy).
**Status:** battery CLOSED 2026-10-04 — 12/12 chunks drafted and
second-judged (238 concepts, 217 anchors; exact 127 / CV 53 / killed
14 / conjectural 16 / heuristic 7; genres original 88 / reframed 26 /
identification 13). All validate clean, v7 round-trip + independent
decode exact. Review calibrations recorded in
`corpus_runs/r4/REVIEW_LOG.md`; report
`corpus_runs/r4/R4_BATTERY_REPORT.md`. Open: full v7/R4 wire build,
measured token cost, parity re-measurement.
**Methodology layer (2026-10-06):**
- Labels: battery 12/12 second-judged, all validate clean, round-trips exact — **computationally verified**; pilot's "asserted→exact" upgrades — **heuristic** (flagged non-blind; the battery's second judging is the control that answers it); typed-alias non-restatement calls (29) — **heuristic** (second judge recommended); DNA frame — **heuristic** (explanatory layer only, standing convention).
- Fork: pilot non-blind (caveat) / battery second-judged (the control answering the caveat) / REVIEW_LOG calibrations (the instrument record).
- Why it ends here: the battery is closed; R4 emits v7-native labels.
- Its own chain: Node 20 (wire build + parity re-measurement); the open-questions prompt gap fix.
- Backward touch: the battery answered the pilot's own caveat — the "second judge should audit" was specified in the pilot and executed here.
## 19. Blind v6 parity rescore — 2026-10-04
**Q:** (user authorized) does the v6 note channel recover the
injection→wire parity gap? Blind rescore: 4 scorers × (v5 control +
v6), 10 locked probes/chunk, 0/0.5/1 rubric, miss classes.
**Measured:** v5 control **4.88**/10 (NOT reproducing published 6.79);
v6 **6.00**/10; **delta +1.12**. 10/12 chunks gain, 0 decline; all 4
scorers agree on direction. 0 FABRICATION both wires. Gain mechanism:
full marks 7→32/120 — notes convert 0.5s to 1.0s. Largest class gain
MECHANISM (+0.12/probe), the R3-identified frontier.
**Calibration finding:** scorer drift — systematic 1.0→0.5 threshold
shift (42/50 original full marks downgraded); 0.5/0.0 stable. v5
structures byte-identical to R3's, so drift is strictness, not
degradation. Absolute 6.00 NOT comparable to 6.79/7.42; the
within-protocol +1.12 is the valid measurement. The +1.12 exceeds the
R3-measured wire loss (0.63) — consistent with full gap recovery, but
confirming 7.42 needs the injection scored under the new protocol
(not done). Report: `corpus_runs/r3/RESCORE_V6_REPORT.md`.
**Status:** closed (measurement). Open: R4 battery parity
re-measurement (Node 18) will give the v7-native numbers.
**Methodology layer (2026-10-06):**
- Labels: v5 4.88 / v6 6.00 / delta +1.12 within-protocol, 0 fabrication both wires — **computationally verified**; the scorer-drift calibration (42/50 downgrades; ones-rate 5.8% vs 41.7%) — **computationally verified** (the instrument check that makes the within-protocol delta the valid measurement).
- Fork (already triadic): v5 control (byte-identical to R3's) / v6 treatment / scorer-drift calibration (the control on the scorers themselves — strictness, not degradation).
- Why it ends here: the measurement is closed; the +1.12 is the valid wire comparison.
- Its own chain: Node 20's v7 parity (read with calibration awareness).
- Backward touch: the drift finding reframed Node 11's 6.79/7.42 absolutes as protocol-relative — absolute scores are not comparable across scorer strictness; only within-protocol deltas are.

## 20. v7/R4 wire build + parity re-measurement — 2026-10-04
**Q:** (user: "proceed") build the v7/R4 battery: wires, token cost,
blind parity.
**Build:** `corpus_runs/r4/build_wires_v7.py` — 12/12 v7 wires from
accepted R4 extractions. Wire tokens mean **483** (range 344–659;
v6 was 553). Deployment break-even mean **2.06**, 12/12 ≤ 3 (v6:
2.36; R3 injection: 2.26). The v7/R4 combination is cheaper than v6
AND cheaper than the R3 injection path.
**Parity (interim, 9/12 chunks):** blind scorers, v7 structures only.
c01 4.5, c02 6.5, c03 7.0, c04 9.5, c05 9.0, c06 9.0, c10 8.0,
c11 7.0, c12 7.5 — mean **7.56**. Zero fabrication.
**Calibration:** v7 scorers' ones-rate 50.8% matches the original R3
scorer (41.7%) far more closely than the strict v6 rescorers (5.8%).
Under that calibration, v7 7.56 ≈ R3 injection 7.42 — the v7 wire
preserves parity at the injection level. NOT directly comparable to
v6's 6.00 (different scorer strictness); the v5→v6 +1.12 remains the
valid wire-comparison.
**Parity (final, 12/12):** mean **7.46**/10 (range 4.5–9.5), zero
fabrication. Per-class: NUMBER 0.73, VERDICT 0.70, MECHANISM 0.76 —
the R3 frontier inverted. Cost: 483 mean wire tokens, BE_dep 2.06
(12/12 ≤ 3). Calibration: v7 scorers match original R3 scorer
(50.8% vs 41.7% ones), so 7.46 ≈ R3 injection 7.42 — wire loss gone.
Scorer reports: killed/conjectural/exact+identification statuses
specifically carried probes bare labels couldn't. Remaining gap:
mechanism *derivations* (proof steps) don't travel in notes; c02
marks the boundary. Report:
`corpus_runs/r4/V7_PARITY_REPORT.md`.
**Injection parity (final, 12/12):** mean **7.46**/10 — identical to
the wire. **Wire loss: +0.00.** The v7 codec is perfectly lossless at
the battery level; the entire remaining gap to 10 lives in the
extraction (derivation-grade mechanism content in notes). Scorer
distributions identical (50.8% ones both). Per-chunk deltas cancel
(scorer variance, ±1.5 max).
**Status:** closed. The codec is done losing parity — further gains
come from extraction quality (R5), not wire design.
**Methodology layer (2026-10-06):**
- Labels: wire 483 tok, BE_dep 2.06 (12/12 ≤3), parity 7.46/10 wire = 7.46/10 injection, per-class NUMBER 0.73 / VERDICT 0.70 / MECHANISM 0.76, zero fabrication — **computationally verified**; the ones-rate calibration (50.8% vs 41.7%) establishing 7.46 ≈ 7.42 comparability — **computationally verified**; "further gains come from extraction (R5)" — **conjectural** (precise direction by elimination, R5 untested).
- Fork: v7 wire parity (7.46) / R3 injection parity (7.42, the baseline) / ones-rate calibration (the control establishing the two numbers are comparable — without it, 7.46 vs 7.42 would be another drift artifact).
- Why it ends here: the codec is done losing parity — wire loss +0.00, measured both directions.
- Its own chain: R5 extraction quality (Node 21, drafted); the M4 decision (the user's).
- Backward touch: reframed Node 13's "v6 note channel is the next codec upgrade" — the upgrade worked beyond its prediction (wire now lossless, not merely recovered); sharpened Node 10's hard-problem ranking — the extractor is now the *only* remaining lever, not just #1.

## 21. R5: extraction quality — the remaining frontier (EXECUTED 2026-10-06)
**Q:** Can extraction quality close the remaining parity gap (7.46 → 10) without breaking the ≤3 break-even bar? The wire is lossless (+0.00, Node 20); by elimination the entire remaining gap lives in extraction — specifically derivation-grade mechanism content in notes (c02 marks the boundary: proof steps don't travel).
**Discriminating prediction (winner before it wins, pre-registered):** R5 must move MECHANISM class ≥0.85 (from 0.76) with BE_dep ≤3 held and zero fabrication held, on blind rescore under the Node 19/20 protocol (locked probes, calibrated scorers, 0/0.5/1 rubric). If R5 cannot move MECHANISM while holding cost, the gap is irreducible to extraction — and that negative is itself the verdict the M4 decision needs.
**Triadic fork (run):**
1. **Claim:** R5 — targeted at derivation-grade mechanism content (proof-step notes; DERIVE prescriptions per Node 15's spec-v2 requirements; note-carrying injection already proven in Node 11) — raises parity toward the ceiling at held cost.
2. **Polar opposite:** the remaining gap is irreducible — mechanism derivations are inherently non-compact (Node 15's restatement band: content whose formula IS the content doesn't compress); R5 gains asymptote, and the honest product is verdict-and-relation memory (Node 10's redefinition), not faithful memory.
3. **Null:** R4 battery as control arm (same 12 chunks, same protocol family); no fresh chunks exist — recorded deviation; drift controlled directly (see below).
**Method:** anchors first — R4's 7.46/2.06 reproduced live from stored artifacts before any change. R5 = R4 extractor + derivation-preservation rules only (extractor_rev4.py): mechanism notes carry premises→steps→conclusion+prescription (~25 words), restatement stays short, invented steps forbidden. 12 blind extractions (probe-blind agents), every draft second-judged (c06/c12 vocabulary corrections on record). Deterministic wire build (build_wires_r5.py). 4 blind scorers × 3 chunks + 2 drift-control scorings of existing R4 wires (c02, c06), same rubric, blind to prior scores.
**Results** (R5_BATTERY_REPORT.md, R5_PARITY_REPORT.md), all computationally verified:
- Parity: **8.92/10** (R4: 7.46). Every chunk gained or held; zero declines. Range 7.0–10.0.
- Per class: NUMBER 0.867 (0.73), VERDICT 0.833 (0.70), **MECHANISM 0.906** (0.76).
- Cost: wire mean 913 tok (R4: 483); BE_dep mean **2.84** (R4: 2.06), **9/12 ≤3** — c04 3.23, c05 3.22, c06 3.14 breach.
- Fabrication: **0/120**. Ones-rate 79.2% (R4: 50.8%).
- Drift controls: S1 R4-c02 7.5 (battery 6.5, within ±1.5 variance); S2 R4-c06 **6.0** (battery 9.0 — a strictly harsher scorer) yet R5-c06 **9.5**. Within-scorer wire deltas (strictness-free): **+1.5** (c02), **+3.5** (c06); on MECHANISM probes: +0.188, **+0.429**. S2's misses on the R4 wire are exactly the mechanism steps R5 added. The gain is in the wire, not the scorers.
**Verdict vs prediction:**
- MECHANISM ≥0.85: **MET** (0.906). [computationally verified]
- BE_dep ≤3: **PARTIAL** — mean 2.84 holds; 9/12 chunks ≤3, three breach. [computationally verified]
- Zero fabrication: **HELD** (0/120). [computationally verified]
**Triadic reading:** (1) claim CONFIRMED — R5 raises parity; the derivation notes caused it (within-scorer deltas; c02 boundary moved 6.5→9.0). (2) Polar opposite ELIMINATED as stated — the mechanism gap was reducible; its cost concern survives weakened (gain cost 0.78 BE headroom; 3/12 over bar). (3) Null HELD — no fabrication; R4 stands as control arm.
**What R5 moved / didn't:** moved — mechanism derivations now travel (the V7 "systematic remaining gap" substantially closed). Didn't move — *interpretive framing* (S4: remaining 0.5s are definitional/retrodictive distinctions and legitimation narratives, not numbers or steps). That is the next boundary, if drawn.
**M4 decision frame (the user's):** the R5 distribution is the awaited evidence — extraction CAN close the mechanism gap (0.906 ≥ 0.85) at a cost (BE 2.84 mean, 3/12 over bar), zero fabrication risk. Kill criteria remain armed.
**Status:** CLOSED (executed). Reports: corpus_runs/r5/R5_BATTERY_REPORT.md, corpus_runs/r5/R5_PARITY_REPORT.md. Scripts: extractor_rev4.py, corpus_runs/r5/build_wires_r5.py, corpus_runs/r5/SCORER_BRIEF_R5.md.
**Methodology layer (2026-10-06):**
- Labels: all measurements above — **computationally verified**; the R4-comparability of absolute levels — **heuristic** (between-scorer variance −3.0/+1.0 on controls; the within-scorer deltas are the rigorous core); "further gains from interpretive framing" — **conjectural** (S4's observation, untested).
- Fork: claim / polar opposite / null all run; the opposite leg's cost concern partially survived — recorded, not rounded off.
- Why it ends here: the pre-registered prediction is adjudicated on all three legs; the M4 evidence is delivered.
- Its own chain: the M4 decision (the user's — this was the evidence it waited on); the interpretive-framing boundary as a possible R6; the "cited" vocabulary gap noted for a future prompt revision.
- Backward touch: sharpens Node 20's "further gains come from extraction" — confirmed and quantified (MECHANISM +0.146 at 0.78 BE cost); reframes Node 10's hard-problem #1 — the extractor was the only lever and it delivered, which moves the question to the M4 product decision; touches Node 15's restatement band — the band held for interpretive framing even as derivations proved compressible, refining the law's boundary.

## 22. R5 targeted extraction-drop battery — mapping drops by probe class (EXECUTED 2026-10-15)
**Q:** What exactly does the v7 extraction pipeline drop, by probe class — so failed probes stop being hand-audited one by one?
**Method:** 12 new targeted probes on the c02 mechanism-derivation boundary (6 MECHANISM / 3 NUMBER / 3 VERDICT), answer keys locked from source prose before scoring; 2 blind scorers (S1, S2), notes-only, 0/0.5/1 rubric; corroborated against the 25 sub-1.0 probes of the R5 parity rescore (120 probes, 12 chunks). Pipeline under test: extractor_rev4 output (r5/c02/extraction.json). Reports: ~/workspace/your_files/r5-extraction-drop-report.md; rerunnable suite: ~/workspace/your_files/r5-targeted-probe-suite.yaml.
**Results** [computationally verified]: S1 10.5/12, S2 8.5/12 (S2 systematically harsher — same strictness gap as Node 21). Per class (means): MECHANISM 0.792, NUMBER 0.833, VERDICT 0.750. All misses OMISSION; zero fabrication (both batteries).
**Failure classes** [heuristic taxonomy; instances computationally verified]:
1. Conclusion-drop — premises kept, load-bearing conclusion lost (M4, both scorers; R5-rescore c02 P8).
2. Payoff-drop — honest label travels, its upshot doesn't (V1 both; V2 S2).
3. Number-grid drop — endpoints survive, interior trajectory thinned (N1 both).
4. Interpretation-drop — steps travel, named interpretation doesn't (M1, M3 S2; R5-rescore c02 P5 independently reproduced).
5. Prescription-thinning — prescription present but underspecified (M6 S2).
Corroboration: 18/25 R5-rescore misses are MECHANISM — drops concentrate at mechanism content across all 12 chunks.
**Fix list** [conjectural — concrete, testable, unmeasured]: CONCLUSION-FIRST, PAYOFF CLAUSE, GRID RULE, INTERPRETATION RIDER, PRESCRIPTION COMPLETENESS — each with a named re-run test predicting 1.0 (see report).
**Backward touch:** sharpens Node 21's "interpretive framing is the next boundary" — the drop map shows it is not one boundary but five distinct drop patterns, two of them (Conclusion-drop, Payoff-drop) independently reproduced by the R5 rescore's own c02 misses; the fixes are the candidate R6 intervention, with the suite as its pre-registered test.
**Status:** CLOSED (executed). Next: apply fixes, re-run suite, check predicted 1.0s.

## 23. R6 targeted re-run — the five fixes tested (PRELIMINARY 2026-10-18)
**Q:** Node 22's fixes (CONCLUSION-FIRST, PAYOFF CLAUSE, GRID RULE, INTERPRETATION RIDER, PRESCRIPTION COMPLETENESS) each predicted 1.0s on re-run. Do they materialize?
**Method:** extractor_rev5.py (EXTRACTOR_PROMPT_R6) re-run on corpus/c02_deriv_d1_d5.txt; deterministic wire build; the 12-probe suite with locked keys scored 0/0.5/1, notes-only, one scorer. Same suite and rubric as Node 22's battery.
**Results** [preliminary — see labels]: **12.0/12** (baseline mean 9.5: S1 10.5, S2 8.5). All nine predicted 1.0s materialize — M4 (conclusion-first), V1/V2 (payoff clauses with "buys:"), N1 (six-value S(X) grid carried), M1/M3 (interpretation riders: reduced Euler characteristic; multiplicative-identity framing), M6 (prescription with ψ(x) target + both paths), R5 c02 P5/P8. The three already-1.0s held. Zero fabrication.
**Cost** [computationally verified]: c02 wire tokens 726→1221 (+68%); note words 205→472. The fixes are content, not free — whether 12/12 ≤3 BE_dep survives R6 on the full battery is unmeasured.
**Methodology layer (2026-10-18):**
- Labels: 12/12 and 9/9 agreement — **preliminary (unblinded)**: the extractor had read the keys before extracting; the scorer is the same instrument. The honest battery needs blind rescorers. Cost numbers — **computationally verified** (deterministic builds, tiktoken counts).
- Fork: claim (fixes sufficient) / polar opposite (a drop class exists no fix repairs) / null (fixes are neutral text changes). The opposite leg is eliminated on this chunk — every named drop was repairable by its fix; no third class surfaced.
- Why it ends here (as preliminary): the pre-registered predictions are adjudicated on the same suite. Open: full-battery R6 re-extraction, blind rescore, BE_dep measurement, whether conclusion-first changes concept structure at scale.
- Backward touch: sharpens Node 22's "fixes: conjectural" — now sufficient-on-c02, preliminary; the R6 cost trend is steeper than R5's, so Node 21's cost headroom question is live again.
**Status:** PRELIMINARY (executed, unblinded). Reports: corpus_runs/r6/R6_TARGETED_RERUN_REPORT.md. Scripts: extractor_rev5.py, corpus_runs/r6/c02/extraction.json.
**Blind rescore (2026-10-18) — measured:** two independent blind scorers, notes + locked keys only: A = 12.0/12 targeted (13.5/14; c02 P8 at 0.5), B = 11.0/12 targeted (12.5/14; M2, V3, c02 P8 at 0.5). Mean targeted 11.5/12 vs R5 baseline 9.5. Predicted 1.0s: 8/9 confirmed by both (M4, V1, V2, N1, M1, M3, M6, c02 P5); c02 P8 did NOT survive — both scorers 0.5 (failure reason present, sharpest question absent); the preliminary 1.0 was scorer-generosity. New single-scorer 0.5s (M2, V3) medium confidence, harsh-scorer pattern. Verdict: fixes confirmed working 8-for-9 under blind two-scorer protocol; P8 open for one more targeted pass.

## 24. P8 targeted pass — crowned-verdict rule (2026-10-18)
**Q:** R6 blind rescore left c02 P8 at 0.5/0.5 (notes carry the D4 failure reason, not the text's crowned "single sharpest question"). Does a targeted rule repair it without regressions?
**Method:** extractor_rev6.py — EXTRACTOR_PROMPT_R7 (R6 + CROWNED-VERDICT RULE: program-scope crowned verdicts ride as "sharpest:"/"open:" clauses). Clean extractor subagent applied it to c02 fresh (briefed on prompt only; nothing of P8/keys/scores). Two new blind scorers, notes + locked keys only, same packet protocol.
**Results** [blind, two-scorer]: A = 11.5/12 targeted, 13.5/14; B = 11.5/12 targeted, 13.5/14. c02 P8 = **1.0/1.0** — fix confirmed; the sharpest question now rides verbatim in the note. Targeted mean 11.5 = r6 blind mean 11.5: no net regression. Movers: M2 1.0/0.5→0.5/0.5 (integer-side set {p_a·m} not characterized in fresh note — borderline probe, note-phrasing drift, not a rule effect); V3 1.0/0.5→1.0/1.0.
**Labels:** scores blind-measured (role-separated, brief-scoped scorers). Fix 9/9 predicted 1.0s now confirmed blind across R6+R7.
**Status:** CLOSED (executed). Reports: corpus_runs/r7/. Open: M2 bijection-completeness pass (offered, not authorized).

## 25. R8 full 12-chunk battery — generalization test (2026-10-18)
**Q:** The R5→R8 fixes were validated on c02 only. Do they generalize across all 12 chunks, and at what cost?
**Method:** 12 independent extractor subagents, each briefed with ONLY EXTRACTOR_PROMPT_R8 + one chunk text + JSON schema (knew nothing of probes/keys/scores). 12 blind packets (notes + 10 locked probes + strict rubric each). Two blind scorers × 120 probes, notes-only. Baselines: corpus_runs/cXX/report.json (R5 binary parity/omission, 58/120).
**Results** [blind, two-scorer]: R8 mean **77.75/120** (A 79.0, B 76.5; gap 2.5) vs R5 58/120 → **+19.75 net**. 8 chunks gain (c11 +7.5 largest), 4 lose (c06 −4.25). 22 full gains: R5 omission → R8 1.0/1.0 across 9 chunks. 10 consensus 0.0/0.0; 61 consensus ≤0.5. 30 hard regressions (R5 parity → R8 ≤0.5) with protocol caveat: binary-vs-ternary makes 0.5s incomparable; 30 is an upper bound, 5 (0.0-on-parity) the lower.
**Cost** [computationally verified]: 808 → 3,258 note words, **4.03× inflation** (R5 notes were ~3.8 words/note; R8 ~15.4, inside revision budgets).
**Key finding — extractor variance dominates:** the same prompt across 12 independent runs produced 5.5–24.7 words/note; the three tersest chunks scored lowest. Smoking gun: c02 P8 (crowned-verdict fix, validated 1.0/1.0 on r7's extraction) scored 0.0/0.0 on the fresh r8 extraction — the rule was in the prompt and did not fire. Prompt rules alone don't guarantee application.
**Fork:** claim (fixes sufficient at scale) / polar opposite (variance swamps fixes) / null. Verdict: claim holds on net (+19.75), but the opposite leg is live at the extraction level — variance, not drop classes, is now the binding constraint.
**Next intervention:** per-extraction compliance gate (check rules fired before accepting; re-run/patch on failure) — NOT more prompt rules. This is the redundancy principle applied: catch drops after the fact rather than preventing them upfront.
**Backward touch:** bounds Nodes 22–24 (single-chunk wins stand, but their method — longer prompts — has a measured ceiling); reframes the R5 cost question (4× words may breach BE_dep ≤3 — unmeasured).
**Status:** CLOSED (executed). Report: corpus_runs/r8/R8_FULL_BATTERY_REPORT.md.
