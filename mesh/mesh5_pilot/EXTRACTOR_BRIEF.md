# MESH-5 Pilot — Extractor Brief (E_blind)

**Version:** 2026-10-09 (Phase A shakedown; reused for Phase B).
**Your task:** extract verdict records from the assigned source file and
link them with typed relations. That is the entire task.

## Records

Each record:
- `record_id`: `R01` … `RNN` (sequential in your output).
- `claim`: ONE sentence stating a single claim from the source, in the
  work's own words and vocabulary. Never invent a private taxonomy;
  never paraphrase into your own terms. One claim per record — split
  compound sentences.
- `span`: the EXACT verbatim quote (copy character-for-character) from
  which the claim is drawn.
- `source`: the file path and section heading.

Do NOT assign epistemic labels (exact / verified / conjectural / …).
Do NOT summarize the document. Do NOT add commentary.

## Typed relations

Link records with these five relation types. Every record MUST carry
**≥3 typed links** (incoming and outgoing both count — aim for a mix
where the material supports it).

- `supports`: A's claim provides evidence, a reason, or a verified
  instance counting in favor of B's claim.
- `implements`: A describes a concrete computation, procedure, or worked
  instance that realizes B's general claim.
- `exemplifies`: A is a specific case or instance of B's general claim.
- `refines`: A agrees with B but sharpens, qualifies, or bounds it
  (agreement + added precision).
- `contradicts`: A asserts the NEGATION of a claim B asserts.
  This is the strict one — read the examples below carefully.

Each link: `{source_id, target_id, rel, reason}` where `reason` is one
line stating the specific textual basis (quote fragments welcome).

## contradicts — 5 worked examples (genuine)

1. A: "Information enters prices through fast public impounding."
   B: "Information enters prices through slow private diffusion."
   → B negates A's mechanism claim. CONTRADICTS.
2. A: "The C2 control is resolved."
   B: "C2 is resolved only weakly; the tape contains no news dates, so
   attribution cannot be tested."
   → B negates the unqualified "resolved." CONTRADICTS.
3. A: "K9-4 tail-date news attribution is decidable against the tape."
   B: "K9-4 is honestly undecidable — no news dates in the tape universe."
   → CONTRADICTS.
4. A: "The mechanical candidates did the adjudication work."
   B: "Semantic review did the real work; the merge script is a candidate
   generator, not an adjudicator."
   → CONTRADICTS.
5. A: "Verification labels state truths about markets."
   B: "Every 'holds' below means 'holds in the fixed window,' never
   'true of markets.'"
   → B negates the generalization. CONTRADICTS.

## contradicts — 5 near-miss NON-examples (do NOT label these contradicts)

1. A: "The fundamentals sky proves earnings jumps at tick resolution."
   B: "The tape sky measures the same phenomenon in the fixed window
   with no attribution of its own."
   → Same phenomenon, different epistemic roles. Neither negates the
   other. This is a role-difference, NOT a contradict.
2. A: "Tape↔narrative is the thinnest pair (1 link, 2 misses)."
   B: "Fundamentals↔narrative has 4 split links."
   → Different pairs, different facts. No negation. NOT contradicts.
3. A: "The drafter phase dominates cost (~30% of tokens)."
   B: "The next run should include event dates in the tape universe
   from the start."
   → Different topics entirely. NOT contradicts.
4. A: "C1 resolved and verified."
   B: "C2 resolved weakly with a recorded caveat."
   → Different controls, different outcomes. No negation between them.
   NOT contradicts.
5. A: "NVDA's entire 2-year drift came overnight (+0.848 vs −0.169
   intraday)."
   B: "Post-event adjustment is a shared phenomenon across skies."
   → Consistent; B's context accommodates A. NOT contradicts
   (if anything, A supports B's neighborhood).

## Link discipline

- ≥3 typed links per record (in + out). A record with fewer is
  malformed — fix it before finishing.
- Use `contradicts` wherever the definition is genuinely met.
  Never force it where it isn't — a missing contradicts is fine;
  a false one is a defect.
- Links must be defensible from the text: the `reason` field must
  cite the specific basis. If you cannot state the basis in one
  line, do not make the link.
- Prefer within-batch links (records from this same source file).

## Output

Write JSON to the assigned output path:
`{"records": [...], "links": [...]}`.
Then report: record count, total links, mean degree (links per
record, in+out), and the count/share of `contradicts` links.
