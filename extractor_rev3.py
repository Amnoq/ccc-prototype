"""extractor_rev3.py -- R4: v7-native anchor vocabulary.

FORK (2026-10-03, decision tree node 18): v7 aligned the wire's status
enum with the work's own epistemic labels (exact / computationally
verified / conjectural / heuristic + claim genre). The extractor is the
forward contract: it must EMIT those labels directly instead of the
legacy asserted/verified/open_question vocabulary that the v7 migration
map then has to guess at (lossy-conservative). This revision replaces
the anchor status vocabulary in the prompt and adds the optional genre
key. Everything not mentioned below is byte-identical to R3
(extractor_rev2.EXTRACTOR_PROMPT_R3).

The base SCHEMA_SPEC text is left intact as archaeology (M2/R3 record);
the V7_ANCHOR_RULES below explicitly SUPERSEDE its anchor "status" list,
stated in the prompt itself so no model can miss the override.
"""

from extractor import SCHEMA_SPEC
from extractor_rev1 import DENSITY_RULES
from extractor_rev2 import R3_RULES

V7_ANCHOR_RULES = """\
ANCHOR VOCABULARY (revision 4 -- binding; SUPERSEDES the anchor "status"
list in the base schema above)
- "status" is one of: exact, computationally_verified, conjectural,
  heuristic, killed, superseded.
  - exact: the text PROVES the claim or states it as a theorem/identity
    with the proof or derivation carried in the text. "The text says it
    is true" is NOT exact -- the derivation must be present.
  - computationally_verified: the text reports a numeric or
    computational check. State the check's SCOPE in the note ("at z=30,
    x=200000", "to 2·10^6", "10-digit agreement"). A check without a
    scope is not a verification.
  - conjectural: a precise claim with its boundary stated, but no proof
    in the text.
  - heuristic: an intuition or analogy with no derivation path stated.
  - killed: the text refutes or rejects the claim. superseded: the text
    replaces it with an heir (name the heir -- see the REPLACEMENT RULE).
  - Do not mark "exact" unless the derivation is present. Do not mark
    "computationally_verified" unless the text gives the check AND its
    scope. When in doubt between exact and computationally_verified,
    choose computationally_verified: never claim more than the text
    establishes.
- Open questions and observed gaps: do not force a strength status onto
  a question. Give the concept kind "open_question", list it in "loops",
  and OMIT its anchor. Anchors are for claims; loops are for questions.
- "genre" (optional; OMIT the key when none applies) is one of:
  original, reframed, identification.
  - original: the text advances a new claim here.
  - reframed: a classical result given a new framing here -- "not a new
    theorem". Use this when the text re-presents known mathematics in a
    new language (e.g. a classical identity read through the sieve).
  - identification: the text states an X<->Y bridge (e.g. "D2's recursion
    read through her lens"). The bridge is the claim; it is not a new
    theorem about either side.
"""

# The effective R4 schema: base spec with the anchor vocabulary
# superseded in-text. Pass this as schema_reminder to
# extract_with_repair so repairs see the R4 rules, not the base text.
SCHEMA_R4 = SCHEMA_SPEC + "\n" + V7_ANCHOR_RULES

EXTRACTOR_PROMPT_R4 = (
    "You are a precise information-extraction system. "
    "Read the technical discussion below and extract its "
    "argumentative structure.\n\n" + SCHEMA_R4 +
    "\n" + DENSITY_RULES +
    "\n" + R3_RULES +
    "\n## Source text\n"
)
