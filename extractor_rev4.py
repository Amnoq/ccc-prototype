"""extractor_rev4.py -- R5: derivation-preserving notes.

FORK (2026-10-06, decision tree node 21): the R4 battery measured the
wire lossless (+0.00) and isolated the remaining parity gap to
extraction -- specifically, mechanism *derivations* (proof steps) do
not travel in notes (V7_PARITY_REPORT "systematic remaining gap";
c02 marks the boundary). Scorers' recurring 0.5 pattern: "mechanism
detail absent from notes." R3's note rule ("~12 words, evidence only")
cannot carry a derivation chain. This revision adds derivation
preservation for mechanism-type content, keeping the v7 schema,
density rules, and R3/R4 rules otherwise intact.

The intervention is minimal and targeted: only the note-content rules
change. Everything not mentioned below is byte-identical to R4
(extractor_rev3.EXTRACTOR_PROMPT_R4).
"""

from extractor import SCHEMA_SPEC
from extractor_rev1 import DENSITY_RULES
from extractor_rev2 import R3_RULES
from extractor_rev3 import V7_ANCHOR_RULES

R5_RULES = """\
DERIVATION PRESERVATION (revision 5 -- binding; density rules and the
R3/R4 rules still hold, except the note-length cap below which this
section SUPERSEDES for mechanism notes)
- DERIVATION RULE: for mechanism-type anchors -- proofs, derivations,
  methods, "why/how it is legitimate" content -- the note must carry
  the derivation CHAIN, not just the verdict: premises -> inference
  steps -> conclusion, each step compressed but complete. Close with
  the PRESCRIPTION: how to recompute or verify ("recompute via X",
  "check at N=...", "the move is ..."). Derivation notes may run to
  ~25 words; spend them on steps a blind reader would need in order
  to re-derive the conclusion.
- DERIVE MARKING: where the text derives rather than asserts, lead
  the note with the derivation's key move ("via Mobius inversion
  on ...", "by boundary cancellation at ...", "by exact scaling,
  not the fixed step").
- DOMAIN IDENTIFICATION: name the domain each derivation step lives
  in (face-sum, operator calculus, numerical check, ...).
- RESTRAINT (restatement band): content whose formula IS the content
  stays literal -- do not bloat restatement. The derivation rule
  applies to GENERATIVE mechanism content (derivations with
  derivable consequences) only. When in doubt whether content is
  generative or restatement, keep the note short.
- HONEST BOUNDARY: if the text does not give the steps, do not
  invent them. The note states what is missing ("derivation steps
  not in text") instead of fabricating. A missing-steps note is
  honest; an invented chain is fabrication.
- Worked shape (from the corpus, c02): "deform R_p={0} to {0,-2};
  survivors ARE twin lowers (verified to 2e5); renormalized weight
  S(z)->2C2=1.32032; prescription: recompute S(z) at larger z."
  Verdict + mechanism + numbers + prescription in ~25 words.
"""

EXTRACTOR_PROMPT_R5 = (
    "You are a precise information-extraction system. "
    "Read the technical discussion below and extract its "
    "argumentative structure.\n\n" + SCHEMA_SPEC +
    "\n" + DENSITY_RULES +
    "\n" + R3_RULES +
    "\n" + V7_ANCHOR_RULES +
    "\n" + R5_RULES +
    "\n## Source text\n"
)
