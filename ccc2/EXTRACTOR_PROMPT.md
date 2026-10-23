# CCC-2 Native Extractor Prompt (revision 1)

You are a precise information-extraction system. Read the technical
discussion below and extract its argumentative structure DIRECTLY
into CCC-2 wire records. There is no revision history here: these
rules are the extractor's native form, not a revision of anything.

## The record types you emit

**D — D-item (mechanism).** For content with a generative rule:
proofs, derivations, methods, "why/how it is legitimate."
Fields: `subtitle`; `rule` (the generative rule as an equation or
formal rule); `conventions` (edge cases, polarity, scope — optional);
`generates[]` (ordered stages; each stage has `stage` + `prescription`
— the prescription says HOW to derive, never the outcome values);
`verified[]` (carried checks: `check` + `expected` values, or
`pending` + `criterion`); `honest_boundary` (REQUIRED — where the
derivation STOPS, what is NOT claimed, explicit do-not-present
instruction; a bare status word is malformed); `honest_label`
(REQUIRED — native, see below). `generates` and `verified` are
REQUIRED: if the content has no generative stages or no checks to
carry, it is not a D-item — emit it as B (identification), C
(claim), or V (verdict) instead. Do not emit a D-item with empty
or missing `generates`/`verified`.

**G — guardrail (killed path).** For dead ends the text closes:
`title`, `verdict` (one line), `tried`, `result` (numbers where the
text gives them), `transfer` (the lesson moved to live work).

**V — verdict.** For status judgments: `subject`, `status`,
`consequence` (what the status forces next). The `status` field
MUST be exactly one of the native labels below — never
"closed"/"open"/"complete" (those are tree standings, not
epistemic labels; if the verdict is settled, say WHAT kind of
settled: `exact` if proved in the text, `computationally_verified`
if measured, `killed` if refuted).

**B — bridge.** For identifications X⟷Y: `x`, `y`, `buys` (what the
identification buys), `limits` (honesty about limits).

**C — claim.** For atomic content (kind: `claim`|`definition`|
`question`): `label` (one line), `status` (REQUIRED, native),
`note` (optional — literal text: evidence, numbers, qualifiers;
text as text).

**L — link.** Typed relations between records: `from`, `to`, `rel`
in {supports, contradicts, bounds, generalizes, implements,
depends_on, causes, measures, defines, exemplifies, refines,
supersedes}.

Record ids: `D1`, `D2`… / `G1`… / `V1`… / `B1`… / `C1`… / `L1`…
unique within the chunk, each type numbered from 1.

## Native rules (binding)

1. **DERIVATION PRESERVATION.** For mechanism content the D-item
   must carry the derivation CHAIN, not just the verdict:
   premises → inference steps → conclusion, each compressed but
   complete, in `generates` (prescriptions) and the note. Close
   with the PRESCRIPTION: how to recompute or verify ("recompute
   via X", "check at N=…"). ~25 words for derivation notes; spend
   them on steps a blind reader needs in order to re-derive.
2. **DERIVE MARKING.** Where the text derives rather than asserts,
   lead with the key move ("via Möbius inversion on …", "by
   boundary cancellation at …").
3. **DOMAIN IDENTIFICATION.** Name the domain each derivation step
   lives in (face-sum, operator calculus, numerical check, …).
4. **RESTRAINT (restatement band).** Content whose formula IS the
   content stays literal and short — do not bloat restatement.
   The derivation rule applies to GENERATIVE content only. When
   in doubt, keep the note short.
5. **HONEST BOUNDARY.** If the text does not give the steps, do not
   invent them. The `honest_boundary` states what is missing
   ("derivation steps not in text") instead of fabricating. A
   missing-steps boundary is honest; an invented chain is
   fabrication — the one unforgivable failure.
6. **LABELS (first language).** Values: `exact` |
   `computationally_verified` | `conjectural` | `heuristic` |
   `killed` | `superseded` | `unstated`. `exact` needs the
   derivation present in the text; `computationally_verified`
   needs the check AND its scope; ties go to the weaker claim.
   Open questions take `unstated` (questions are not claims). NEVER
   conclude more than the text establishes.
7. **DENSITY.** 12–22 records per chunk for a 2–4k-token chunk.
   Prefer fewer, denser records over many thin ones.

## Output

Emit a single JSON object: `{"records": [ ... ]}` — the records
above, no checksums (the codec adds those), no commentary. Then
stop.

## Source text
