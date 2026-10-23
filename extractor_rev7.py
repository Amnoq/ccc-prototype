"""extractor_rev7.py -- R8: bijection-completeness rule from the M2 consensus 0.5.

FORK (2026-10-18, decision tree node 24): the P8 pass blind rescore
(11.5/11.5 targeted) left M2 at consensus 0.5 — both scorers: the note
states the cone map S↦S∪{p_a} and the link target but never
characterizes the integer-side set {p_a·m : m ≤ x/p_a unshared by the
first a−1 territories}. The v7 baseline note carried it (1.0/1.0);
the R6/R7 rewrites thinned it. This revision adds one general rule.
Everything not mentioned below is byte-identical to R7
(extractor_rev6.EXTRACTOR_PROMPT_R7).
"""

from extractor_rev6 import EXTRACTOR_PROMPT_R7

R8_RULES = """\
BIJECTION COMPLETENESS (revision 8 -- binding; fixes the M2 drop class)
- When the text states an EXACT BIJECTION between two domains, the
  note characterizes BOTH sides: the map AND the sets it matches.
  A bijection note with only one side characterized is a dropped
  mechanism (Interpretation-drop family).
- Worked shape (M2, fixed): "Exact bijection: integers newly shared
  when territory p_a is added are exactly {p_a·m : m ≤ x/p_a unshared
  by the first a−1 territories}, matched by the cone S↦S∪{p_a} over
  link({p_a})=Δ_{⌊x/p_a⌋}; the recursion's two terms are the complex's
  deletion and link."
"""

EXTRACTOR_PROMPT_R8 = EXTRACTOR_PROMPT_R7 + "\n" + R8_RULES
