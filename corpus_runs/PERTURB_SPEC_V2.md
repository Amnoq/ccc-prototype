# PERTURB interpreter spec v2

Fixed 2026-10-03. Supersedes v1. Incorporates the 9 audit requirements
from the second-decoder audit (see EXP2_PERTURB_FIDELITY.md, audit
section). A triple that fails the well-formedness gate is rejected
upfront — no decoding attempted.

## Symbol form

PERTURB(
  seed:        { domain: ...,        # WHAT the elements are (req 2)
                shape: ...,         # binary structure per element
                aggregation: ... }, # how counts aggregate, if relevant (req 7)
  binary-op:   { rule: ...,         # elementwise function on binary values
                polarity: ...,      # mark=remove | mark=keep (req 5)
                conventions: [...] },# edge-case conventions (req 4)
  axis:        { order: ...,        # ordered steps
                extent: ... },      # finite(z=..) | infinite (req 6)
  derive:       [...],              # named proof methods decoder may use (req 3)
  asserted:     [...],              # conclusions carried, not derived (req 3 alt)
  observe:      { name: prescription, ... },  # HOW to read, not just what (req 1)
  definitions:  { name: definition, ... },    # every observable name defined (req 8)
  @status
)

Triple discipline: generative/definitional content only. No numerical
conclusion values, no theorem statements in the triple. Parameters that
set scope (e.g. X) are allowed; results (counts, constants) must be
derived by the decoder.

## Well-formedness gate (run FIRST; req 9)

- W1: seed.shape defines binary values per element.
- W2: binary-op.rule is elementwise on binary values.
- W3: axis.order is a sequence; axis.extent is explicit.
- W4: polarity is declared.
- W5: every observe name has a prescription AND a definition,
  or is listed in asserted.
Fail W1–W4: REJECT the triple (do not decode). Report which check failed.

## Decoder procedure

1. GATE: run W1–W5. On failure, stop with REJECTED + failed checks.
2. STATE: build the discrete state from seed (domain + shape).
3. STEP: apply binary-op elementwise per conventions; advance axis;
   repeat to axis end. Polarity determines the survivor reading:
   survivors = elements holding the keep-polarity value at axis end.
4. READOUT per observable, following its prescription:
   - survivors: structural description of the keep-polarity set.
   - invariants: quantity + one-line reason, else mark underivable.
   - aggregates: symbolic sums/products; numbers via code.
   - limits: only if axis.extent covers the limit.
   - derive: a method named in derive: may be applied by its textbook
     machinery to produce exact identities. The derived identity must be
     stated explicitly as an equation; partial derivations are marked
     DRIFT with the gap (partial credit, not full).
   - named-method: as in v1.
5. COMPUTE: code allowed for finite computations.
6. DATA: an observable whose prescription requires a dataset the triple
   does not supply is marked UNVERIFIED, with the verification criterion
   stated. It is not derived, not lost — pending data.
7. STATUS / ASSERTED: carried verbatim, never derived.

## Scoring (per conclusion)

- REGENERATED: derived by steps 1–7 from the triple alone.
- DRIFT: produced but required outside knowledge — log the exact gap.
- LOST: not obtainable from the triple — log why.
- UNVERIFIED: derivable-in-principle pending data; criterion stated.
- REJECTED: triple failed the well-formedness gate (whole-triple verdict).
