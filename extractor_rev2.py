"""extractor_rev2.py -- R3: evidence-preserving revision of the extractor prompt.

FORK (2026-10-03, decision tree node 12): the 12-chunk corpus battery (R2)
measured parity mean 4.83/10 with a clean omission taxonomy. The #1 omission
class was numerical evidence -- exact numbers, formulas, measured values --
dropped incidentally by density rules, not economically: numbers cost 1-3
tokens each and are the most-probed content class. R3 keeps R2's density
discipline (12-22 concepts, cut-when-in-doubt edges) and adds three targeted
rules. Everything not mentioned below is byte-identical to R2.

Changes (evidence preservation):
- NUMBERS RULE: exact numbers, formulas, measured values, counts, thresholds,
  named constants are NEVER cut for density. They ride in labels (preferred:
  labels survive injection) or anchor notes. If a number is load-bearing to
  a claim, it appears in that claim's label or its anchor note. A number
  costs ~2 tokens; cutting it saves nothing and loses the most-probed class.
- REPLACEMENT RULE: when the text kills/rejects claim X and advances
  replacement Y, coin Y as its own concept (even if described briefly) and
  add edge (Y, supersedes, X). Kills were kept; replacements were dropped.
- NOTES: up to ~12 words (was 8), evidence only, no label restatement.
  Notes now survive: the R3 injection carries anchor notes (M3 P6 fixed),
  so notes are live payload, not dead weight.
- labels: still <=10 words, but numbers count as words and are welcome:
  "twin constant 2C2=1.32032 from deformation" is a good label.
- concepts cap stays 12-22: the uncoined-concept class is accepted as the
  deliberate price of the cap, partially offset by the replacement rule.
"""

from extractor import SCHEMA_SPEC
from extractor_rev1 import DENSITY_RULES

R3_RULES = """\
EVIDENCE PRESERVATION (revision 3 -- binding; density rules from R2 still hold)
- NUMBERS RULE: exact numbers, formulas, measured values, counts,
  thresholds, named constants are NEVER cut for density. Put them in the
  label when the number identifies the claim ("twin constant 2C2=1.32032
  from deformation"), otherwise in the anchor note. A number costs ~2
  tokens; dropping it is pure loss.
- REPLACEMENT RULE: when the text kills claim X and advances replacement Y,
  coin Y as its own concept even if described briefly, and add the edge
  (Y, supersedes, X). Record the kill AND the heir.
- notes: up to ~12 words, evidence only (numbers, measurements, citations),
  never a restatement of the label. Notes now reach the reader, so spend
  the words on evidence a question might need.
"""

EXTRACTOR_PROMPT_R3 = (
    "You are a precise information-extraction system. "
    "Read the technical discussion below and extract its "
    "argumentative structure.\n\n" + SCHEMA_SPEC +
    "\n" + DENSITY_RULES +
    "\n" + R3_RULES +
    "\n## Source text\n"
)
