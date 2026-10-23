"""extractor_rev5.py -- R6: drop-class fixes from the R5 targeted battery.

FORK (2026-10-17, decision tree node 22): the R5 targeted battery
(r5-extraction-drop-report.md, 2026-10-15) measured 12 locked probes
at the c02 mechanism-derivation boundary: 9.5/12 (S1 10.5, S2 8.5),
every miss an OMISSION. Five drop classes induced (heuristic),
five fixes proposed (conjectural, each with a predicted 1.0 on
re-run). This revision applies the five fixes as binding prompt
rules. Everything not mentioned below is byte-identical to R5
(extractor_rev4.EXTRACTOR_PROMPT_R5).
"""

from extractor_rev4 import EXTRACTOR_PROMPT_R5

R6_RULES = """\
DROP-CLASS FIXES (revision 6 -- binding; R5's derivation-preservation
rules still hold, including HONEST BOUNDARY: never invent a missing
conclusion, payoff, grid, interpretation, or target -- mark absent)
- CONCLUSION-FIRST (fixes Conclusion-drop): for mechanism notes, state
  the CONCLUSION first, then premises -> inference steps. A derivation
  note must be reconstructible from its last sentence alone. The note
  records the point, not just the walk.
- PAYOFF CLAUSE (fixes Payoff-drop): every verdict note carrying an
  honest label ("classical in new clothes", "identification, not a
  new theorem", ...) MUST include a "buys:" clause naming what the
  reframing or identification purchases. A label without its payoff
  is a dropped verdict.
- GRID RULE (fixes Number-grid drop): when the source gives a
  convergence trajectory, the note carries the GRID and the interior
  shape ("six values 0.9699...->1.0017 converging to 1"), never
  endpoints alone. Endpoints without the trajectory are a dropped
  number.
- INTERPRETATION RIDER (fixes Interpretation-drop): a mechanism step's
  NAMED interpretation in the text rides with the step in the note.
  The name is content, not decoration ("the multiplicative-identity
  framing", "reduced Euler characteristic"). A step without its
  interpretation is a dropped mechanism.
- PRESCRIPTION COMPLETENESS (fixes Prescription-thinning): a
  recomputation prescription names its COMPARISON TARGET ("compare
  against psi(x)"), and where the text gives two paths, the note
  carries BOTH. A prescription without its target is a dropped
  instruction.
- Worked shape (M4, fixed): "The geometry must live in the weights:
  as x->oo every finite prime set satisfies prod S <= x, so Delta_oo
  is the contractible infinite simplex -- no topology; the growing
  Betti numbers are a filtration phenomenon. Prescription: recompute
  the weight trajectory at larger x."
"""

EXTRACTOR_PROMPT_R6 = EXTRACTOR_PROMPT_R5 + "\n" + R6_RULES
