"""extractor_rev1.py -- M3R: density revision of the extractor prompt.

FORK (2026-10-03, decision tree node 10): M3 measured break-even 5.28 sessions
(lab) / 4.51 (deployment) against a <=3 GO bar, with extraction JSON running
2.1x the source prose. Per the gray-zone provision (one revision, one re-run),
this revision targets output verbosity while holding parity. Everything not
mentioned below is byte-identical to extractor.EXTRACTOR_PROMPT.

Changes (density):
- concepts: "aim for 15-60" -> "aim for 12-22; merge aggressively: one concept
  per IDEA, not per mention. If two phrasings name the same idea, one concept."
- labels: compressed noun phrases, <=10 words, still specific enough to
  identify (not "the method"). Load-bearing specifics go IN THE LABEL:
  anchor notes do not survive the grouped injection (M3 P6 finding), so any
  detail a probe might need must live in the label or an edge, not a note.
- notes: <=8 words, evidence only, no restatement of the label.
- edges: only edges whose removal would lose an argument the text actually
  makes. When in doubt, cut.
- strands: unchanged. anchors/loops: unchanged.
"""

from extractor import SCHEMA_SPEC

DENSITY_RULES = """\
DENSITY (revision 1 -- binding)
- concepts: aim for 12-22. Merge aggressively: one concept per IDEA, not per
  mention. Two phrasings of the same idea become ONE concept.
- labels: compressed noun phrases of at most 10 words, specific enough to
  identify (not "the method" -- "Elias-gamma wire"). Load-bearing specifics
  go IN THE LABEL: anchor notes do not survive downstream injection, so any
  detail a question might need must live in a label or an edge, never only
  in a note.
- notes: at most 8 words, evidence only, never a restatement of the label.
- edges: keep an edge only if removing it would lose an argument the text
  actually makes. When in doubt, cut it. Fewer, truer edges.
"""

EXTRACTOR_PROMPT_R2 = (
    "You are a precise information-extraction system. "
    "Read the technical discussion below and extract its "
    "argumentative structure.\n\n" + SCHEMA_SPEC +
    "\n" + DENSITY_RULES +
    "\n## Source text\n"
)
