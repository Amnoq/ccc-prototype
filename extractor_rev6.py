"""extractor_rev6.py -- R7: crowned-verdict rule from the P8 blind-rescore miss.

FORK (2026-10-18, decision tree node 24): the R6 blind rescore
(12.0 + 11.0 / 12, mean 11.5 vs 9.5 baseline) confirmed 8/9 predicted
1.0s. The ninth — c02 P8 — did not survive: both blind scorers 0.5.
Mechanism: the c02 text explicitly crowns "the single sharpest
question of the program" (D4 resonance-and-gap passage), but the c13
note carried the failure reason and dropped the crowned question —
a Conclusion-drop the R6 rules did not catch, because the note's
conclusion slot was already filled by the passage's other (local)
conclusion. This revision adds one general rule. Everything not
mentioned below is byte-identical to R6
(extractor_rev5.EXTRACTOR_PROMPT_R6).
"""

from extractor_rev5 import EXTRACTOR_PROMPT_R6

R7_RULES = """\
CROWNED-VERDICT RULE (revision 7 -- binding; fixes the P8 drop class)
- When the source text explicitly crowns a claim or question at
  PROGRAM scope -- "the single sharpest question of the program",
  "the main result", "remains the open problem", "the gap stands" --
  the note carries it as a "sharpest:" / "open:" clause. A crowned
  verdict is the passage's point, not optional color; dropping it is
  Conclusion-drop even when the note already has a (local) conclusion.
- The clause states the crowned verdict in the text's own terms,
  compressed but complete. It does not invent what the text leaves
  open (HONEST BOUNDARY still holds: a crowned open question is
  carried AS a question).
- Worked shape (P8, fixed): "...not positive, so not canonical-form
  residues (alternation resonates with boundary-strata alternation).
  Sharpest: is there a positive region whose canonical form has
  these weights as its stratum residues? — the single sharpest
  question of the program."
"""

EXTRACTOR_PROMPT_R7 = EXTRACTOR_PROMPT_R6 + "\n" + R7_RULES
