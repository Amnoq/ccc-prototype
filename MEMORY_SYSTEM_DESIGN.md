# CCC as a Memory System — Design Notes

Reference point for the memory-system reframing (2026-09-28).
Status: exploration, not a build plan. See DECISION_TREE.md node 10.

## Positioning

CCC is not a memory *system*. It is a memory **codec and transport**.
The landscape (Letta/MemGPT tiered memory, Zep/Graphiti temporal KG,
Mem0 per-turn extraction) consists of *stores* with *retrieval* — none
with a portable exchange format. CCC slots in as:

- **Store**: a registry — concept/entity graph (Zep-shaped: entities,
  typed relations, statuses). This is the actual memory.
- **Transport / checkpoint**: the v5 wire — portable, checksummed,
  fingerprinted snapshots of registry state or deltas.
- **Working memory**: the cursor layer — shared accumulated graph
  evolving in encoder/decoder lockstep (1.3x over structural). The
  session-local live working set; the wire is the cross-session
  checkpoint.

CCC does not compete with Zep or Letta. It gives a graph memory
something none of them have: a **verifiable wire format** — snapshots
handed across subagent hops, tool boundaries, and sessions with
tamper-evidence intact.

## Session lifecycle (sketch)

1. Session N runs; the extractor converts transcript into a typed
   structural delta (strands/labels/typed edges/anchors+statuses/loops).
2. Delta merges into the registry (entity resolution at merge time).
3. Checkpoint: registry state (or delta) encoded to v5 wire, telomere-
   wrapped, checksummed. Stored verbatim.
4. Session N+1 opens: harness scans telomeres, validates checksums and
   fingerprint, decodes, injects grouped compact structure (or a
   retrieved subgraph) into the model's context.
5. Repeat. Cold-start legend sync amortizes over sessions (measured:
   break-even ~2-3 sessions at B=628).

## Hard problems, ranked

1. **Extractor (gating).** Text -> typed structure. Proposed design:
   LLM extractor constrained to a strict schema, then a deterministic
   verifier (indices resolve, types from fixed vocabulary, no duplicate
   edges, checksum discipline), then a semantic check (Test B style
   probes: structure vs source text). Metric: probe parity per
   extraction dollar, amortized. If extraction costs 5K tokens to save
   3K/session, the memory must live 2+ sessions to break even.
2. **Entity resolution.** "wheel_210" (session 3) vs "the mod-210 wheel"
   (session 9) must resolve to one concept or the registry forks and
   compression dies from duplicates. Embedding candidates +
   adjudication. Second gating experiment.
3. **Read path at scale.** 10K concepts can't be injected whole.
   Retrieval selects a relevant subgraph; CCC is the transport for
   whatever is materialized. The 2.2x applies to the retrieved slice.
   CCC meets RAG here rather than replacing it.
4. **Registry evolution.** Versioning (fingerprints already per-version),
   merges, splits, deprecation, garbage collection of dead concepts.
5. **Time and conflict.** v5 has no temporal validity (Zep's key
   insight: record *when* a fact became untrue). Statuses give a hook
   (st_verified -> st_superseded); real temporal edges are a v6
   consideration. Cross-session contradictions need a resolution
   policy, not just a codec.

## Integrity story (the differentiator)

Per-line checksums, header checksums binding headers to bodies,
registry fingerprints, order-independent reassembly, fountain erasure
recovery — composed, this is **tamper-evident memory across trust
boundaries**. Realistic corruptions handled: truncation in transit,
silent model edits of the wire (detected), duplicated lines from
retried sends (header checksum), reordered chunks from parallel
delivery (order-independent). Vector stores and Postgres-backed
memories offer none of this on interchange paths. For multi-agent
systems where memory crosses subagent hops, this is a selling point
independent of the 2.2x.

## Relation to the 2.2x

The compression ratio is a *property* of the memory system, not the
pitch. The pitch is density + integrity + determinism for
long-horizon agents whose structured memory needs exceed the context
window, where the alternative is lossy summarization or RAG
complexity. (Cost play is dead: prompt caching captures ~10x on the
same workload; see the decision brief.)

## Next build (if authorized)

`memory_harness.py`: SQLite-backed registry, LLM extractor with strict
schema + deterministic verifier, snapshot/restore through the v5 wire,
grouped injection on read, both gating experiments instrumented from
day one. External yardstick: LongMemEval / LoCoMo (comparable to
existing systems, not self-graded).
