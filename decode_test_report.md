# Model-Side Decode Test — Report (2026-09-28)

The decisive experiment: can a live model decode CCC wire context and
reason over it as well as over prose, at net token savings?

## Design

Two deployment architectures tested separately:
- **(A) Model-as-parser**: raw wire in the prompt; the model decodes it by
  following written instructions. Tests mechanical decode.
- **(B) Harness-parses**: deterministic code (`codec.py`) parses the wire;
  the model only reasons over the compact structured form (indices +
  registry legend). Tests reasoning parity — the realistic deployment.

Test material: a 32-concept research context (prime-distribution
investigation), 4 strands, 16 edges, 3 anchors, 2 loops. Wire: 25 ints,
226 digits. Prose: an information-equivalent paragraph (written to match
the structured facts). 10 probes: factual, relational, multi-hop,
negative, open-loop.

Caveat: the experimenter built the codec (contaminated subject). Test A
measures spec completeness + mechanical burden, not naive-model
reliability. Test B (does the representation support reasoning) is clean:
answers were not memorized.

## Test A — mechanical decode: PASS on correctness, FAIL on practicality

- Wrote `DECODE_SPEC.md`: complete decoder instructions for a naive model
  (telomere scan, fingerprint, checksum, triples→bits, gamma decode,
  prime-product factoring, edge unpacking, index→name).
- Implemented `spec_decode.py` from the spec alone (zero calls to codec's
  decode functions). Output matched the reference `decode_struct` exactly.
  The spec is complete; the format is decodable-in-principle.
- Mechanical burden for this TOY message: 73 triples → 657 bits →
  25 hand gamma-decodes + factoring 6 prime products (largest 2.2×10^16,
  55 bits — factoring a 16-digit number by hand) + 16 edge unpacks +
  a 73-term mod-1000 checksum. The spec itself is 1478 tokens.
- Verdict: model-as-parser is barely feasible at toy scale and implausible
  at real scale. A model doing this mentally would be extremely slow and
  slip-prone; the failure mode is silent arithmetic error, not detectable
  confusion. **Architecture (A) is dead. The viable deployment is (B):
  the harness MUST do the mechanical parsing.**

## Test B — reasoning parity: 10/10 both, with representational gaps

All 10 probes answered correctly from the structured form AND from prose.
But the probes were structural (membership, relation existence) — exactly
what the codec encodes. Two gaps found where prose carries information
the codec drops:
1. **Strand labels**: prose names thread (1) "Gap analysis"; the wire
   carries only an unlabeled set ("strand 1"). Strand names are not encoded.
2. **Edge types**: prose says jacobsthal_function *bounds*
   maximal_prime_gap; the wire carries only "related". Edges are untyped.
   (Also: anchor *rationale* — "verified", "validated to 0.1%" — does not
   travel; the registry has content strings but they are not in the wire.)
- Verdict: reasoning parity holds for what the codec claims to carry, but
  the codec's ceiling is strictly lower than prose. It captures the
  skeleton (what connects to what); prose captures the meat (how, why, in
  what way). "Why/how" probes would favor prose by construction.

## Token economics (cl100k_base, measured)

| form | tokens |
|---|---|
| prose (compressed summary) | 360 |
| wire (naked) | 76 |
| wire + telomere | 82 |
| legend (index→name, 32 concepts) | 262 |
| wire + legend (cold start) | 338 |
| compact indices form (harness-injected) | 206 |
| struct.json names form (harness-injected) | 504 |
| DECODE_SPEC.md (one-time, arch A) | 1478 |

- The wire is 4.7× smaller than prose (76 vs 360) — the serialization win
  is real.
- The legend dominates at small scale: cold-start wire+legend ≈ prose
  (338 vs 360) — a tie.
- Steady state (registry cached, the realistic case): compact indices
  form 206 vs prose 360 = **1.75×**. NOT the 11× from earlier ledgers —
  that was wire vs raw transcript; vs an already-compressed prose summary
  the margin is much thinner at this scale.
- The names-form expansion (504) is worse than prose: the harness must
  inject indices, not names.
- Scaling note (untested): prose cost grows with verbosity (grammar, glue
  words); indices grow with concepts. The 1.75× should widen with size,
  but this is an argument, not a measurement.

## Bottom line

The project survives, narrowed:
1. Viable architecture is (B): harness-side deterministic codec +
   compact structured injection. Model-as-parser is out.
2. Reasoning parity holds for structural content; the codec needs labeled
   strands, typed edges, and status payloads to close the expressiveness
   gap with prose. All three are encodable — concrete buildable work.
3. Steady-state savings over good prose are modest at toy scale (~1.75×)
   and should widen with scale (untested).
4. Still untested: a NAIVE model (a) following the structured format
   reliably, (b) at real registry scale, (c) with the gaps closed.

Next build if pursued: codec v5 (+ strand labels, typed edges, status
payloads), then re-run Test B with why/how probes.

---

# v5 addendum — 2026-09-28 (later)

## What changed
Codec v5 closes the three expressiveness gaps: **labeled strands**
(`L_i` = label concept index, 0 = unlabeled), **typed directed edges**
(`c = (a*B+b)*B + t`, t = relation-type concept, direction preserved —
v4 sorted endpoints undirected), **anchor statuses** (`p = s*B + c`,
status concept + anchor concept). Types, labels, statuses are ordinary
registry concepts: no side tables. Clean break from v4, selected by the
telomere version field (5). Wire layer untouched.

Test registry grew 32 → 54 concepts (15 relation types: bounds,
exemplifies, measured_in, closed_as, converges_to, belongs_to, attacks,
sums_over, derived_from, implements, layer_of, overhead_of,
constrained_by, eases, co_probes; 3 statuses; 4 thread labels).

## Test A (v5): PASS
`spec_decode_v5.py` (independent, spec-only) reproduces the v5 reference
structure exactly. v5 spec section added to DECODE_SPEC.md with worked
example. Wire: 32 ints, 328 digits (vs v4's 226 — the payload costs
~45% more wire).

## Test B (v5): gaps closed, 10/10 why/how probes parity
Ten new why/how probes (label lookup, relation-type lookup, anchor
status/rationale, directed "what does X do to Y") — all answerable from
the v5 structured form; all 10 also answered from prose. 8 original
structural probes re-run: no regression.

## Corrected token economics (equal information, cl100k_base)
- v5 wire: 110 vs prose 360 → 3.3x (transmission, not model-consumable).
- Model-consumable steady-state injection (parsed indices, registry
  already in context): 284 vs 360 → **1.27x**.
- Cold start wire + full legend: 543 vs 360 → loses at toy scale.
- **Correction to the v4 ledger:** the reported 1.75x (206 vs 360) was
  information-asymmetric — v4's structure omitted labels, relation
  types, and statuses that the prose contained. v5's 1.27x is the first
  apples-to-apples figure. The expressiveness the prose always had costs
  compression ratio.
- Per-fact: ~25 facts; wire 4.4 tok/fact vs prose 14.4 tok/fact. The
  wire is genuinely dense; injection syntax overhead eats roughly half
  the advantage.

## Verdict update
v5 proves the expressiveness gaps are closable inside the integer/prime
architecture with modest wire cost (+45%). The honest steady-state gain
at toy scale, equal information, is **~1.3x**, not 1.75x and not 11x.
Whether it grows at real scale (registry amortization, denser graphs)
remains the untested claim that decides the project.

---

# Scale test — 2026-09-28 (later)

## Question
Does the steady-state ratio (CCC injection vs prose) grow, hold, or
collapse at real scale? Synthetic research graphs, B = 174..1030
concepts, edge densities 0.5..2.0 per concept, 3 seeds each. Prose is
template-generated but terse and subject-grouped (the way a careful
summarizer writes); information content equal both sides. Tokens =
cl100k_base.

## Results (steady-state grouped injection vs prose)

| B    | dens 0.5 | dens 1.0 | dens 2.0 |
|------|----------|----------|----------|
| 174  | 2.32x    | 2.21x    | 2.15x    |
| 326  | 2.35x    | 2.24x    | 2.17x    |
| 628  | 2.40x    | 2.28x    | 2.21x    |
| 1030 | 2.22x    | 2.06x    | 1.94x    |

Wire vs prose runs 2.9x -> 1.9x over the same range. Cold start
(legend + wire vs prose): 1.0-1.3x at low density, 0.8-0.9x at high
density — the legend dominates until amortized (~2-3 sessions to
break even; 10 sessions at B=628/dens=1.0 gives 2.0x cumulative).

## Findings
1. **No collapse.** The ratio is ~2.2x and roughly FLAT across a 6x
   scale-up (174 -> 1030 concepts). The toy 1.27x was pessimistic,
   dragged down by JSON injection overhead, not by the codec.
2. **No unbounded growth either.** The predicted log-vs-linear
   mechanism (indices grow as log B, names cost prose linearly) is
   real but counterbalanced: edge ints grow as B^3 (gamma ~6 log B
   bits) while synthetic names stay fixed-length. Real vocabularies
   need longer distinctive names at scale, which would tilt further
   toward CCC — so 2.2x may be conservative.
3. **Injection syntax matters as much as the codec.** Naive JSON
   indices gave 1.3-1.6x with a density penalty; subject-grouped
   minimal injection gives 1.9-2.4x and nearly erases the density
   penalty. Grouped injection converges to wire size — the wire is
   near the practical floor for a model-consumable form.
4. **Two real codec improvements fell out:** (a) weight-balanced
   multiline chunking (`encode_lines_balanced`) — count-based
   chunking clusters all heavy strand prime-products into line 0
   and overflows the 999-triple v3 header past B~300; (b) confirmed
   the multiline transport as the large-message path, with
   order-independent reassembly verified at every scale/density.

## Caveats
Synthetic graphs and template prose, not a real corpus or a real
summarizer. Reasoning sufficiency at scale still untested (needs the
naive-model + harness trial). The durable number from this test:
**~2.2x steady-state at equal information**, flat across scale.
