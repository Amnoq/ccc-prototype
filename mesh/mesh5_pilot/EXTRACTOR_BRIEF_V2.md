# MESH-5 Pilot — Extractor Brief (E_blind), v2

**Version:** 2026-10-09 (revision 1 — supersedes v1).
**What changed from v1:** (a) extract "limitation records" as
first-class records (below); (b) the scope-narrowing contradicts
principle is now operational, with worked examples; (c) examples
re-grounded in the current source material. The strict contradicts
definition is unchanged.
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

**Limitation records (new in v2):** claims of the form "X fails / is
weak / does not generalize / remains open / was downgraded / is not
yet met" are FIRST-CLASS records — extract them like any other claim.
Do not skip a claim because it is negative. These are the natural
partners for negation relations.

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

**Scope-narrowing principle (operational, v2):** when record B bounds
A's claim to a narrower scope, and A's claim was stated (or would
naturally be read) with the broader scope, B CONTRADICTS A — the
narrowing negates the broad reading. If A's claim was already stated
with the narrow scope, B merely refines it.

Each link: `{source_id, target_id, rel, reason}` where `reason` is one
line stating the specific textual basis (quote fragments welcome).

## contradicts — 5 worked examples (genuine)

1. A: "Item 1 PASS establishes A3's energy is non-circular."
   B: "Item 1 is downgraded to 'inputs non-circular, low-information':
   three Gaussian evaluations do not prove W(h)≥0 for all admissible h."
   → B negates the sufficiency reading of A's PASS. CONTRADICTS.
2. A: "The Node 10a bar is met."
   B: "Node 10a requires BOTH items. Item 1 PASS, Item 2 OPEN → the bar
   is NOT YET MET."
   → B asserts the negation. CONTRADICTS.
3. A: "The pilot's μ-recurrence imports prime data."
   B: "μ(d)=(−1)^|S| is read off face dimension; generated, not imported."
   → CONTRADICTS.
4. A: "Divisibility-poset reconstruction of Λ is an informative A3
   finding."
   B: "Divisibility is the integers' entire multiplicative structure;
   recomputing Λ from it tests a guaranteed Möbius identity."
   → B negates the informativeness claim. CONTRADICTS.
5. A: "The finite face lattice determines W(h_a)."
   B: "The lattice determines W only up to the tail — and the tail
   swallows the signal precisely where positivity is nontrivial."
   → B negates the unqualified determination claim (scope-narrowing).
   CONTRADICTS.

## contradicts — 5 near-miss NON-examples (do NOT label these contradicts)

1. A: "Item 1 PASS on inputs (non-circular)."
   B: "Item 2 OPEN — no independent positivity/signature theorem."
   → Different items, different verdicts. B does not negate A's PASS.
   NOT contradicts.
2. A: "The D1 error tracks e^{−(log z)²/(4a)}."
   B: "The prefactor is 2√(a/π)·√z/log z."
   → B sharpens A's scaling law. Agreement + precision = REFINES,
   not contradicts.
3. A: "The μ-recurrence matched the direct prime-power sum to 9 digits."
   B: "The runner caught and fixed its own μ-implementation bug mid-run."
   → Different events (result vs process). No negation. NOT contradicts.
4. A: "W(h_a) ≈ 2e^{−aγ₁²} is tiny at large a."
   B: "At a=0.02 the lattice resolves W exactly already at z=30."
   → Different regimes, compatible facts. NOT contradicts.
5. A: "Positivity is observed at the Gaussians."
   B: "Positivity at the Gaussians is observed, not proved."
   → B qualifies the epistemic status of A's observation — this is
   REFINES (agreement + precision), not contradicts, unless A had
   claimed "positivity is PROVED at the Gaussians," in which case B
   would contradict. Read A's actual scope before deciding.

## Link discipline

- ≥3 typed links per record (in + out). A record with fewer is
  malformed — fix it before finishing.
- Use `contradicts` wherever the definition (including the
  scope-narrowing principle) is genuinely met. Never force it where
  it isn't — a missing contradicts is fine; a false one is a defect.
- Links must be defensible from the text: the `reason` field must
  cite the specific basis. If you cannot state the basis in one
  line, do not make the link.
- Prefer within-batch links (records from this same source file).

## Output

Write JSON to the assigned output path:
`{"records": [...], "links": [...]}`.
Then report: record count, total links, mean degree (links per
record, in+out), and the count/share of `contradicts` links.
