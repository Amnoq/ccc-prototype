# Extractor Brief — variant (c): limitation-as-contradicts

**Version:** 2026-10-09, contradicts-branch probe 1c.
**Base:** mesh/mesh5_pilot/EXTRACTOR_BRIEF_V2.md (limitation records as
first-class records; 5 rels; ≥3 typed links per record; no epistemic
labels; hypothesis never mentioned). Everything in v2 applies EXCEPT the
contradicts rule below, which REPLACES v2's contradicts definition
(including the scope-narrowing principle).

**Your task:** extract verdict records from the assigned source file and
link them with typed relations. That is the entire task.

## Records

Same as v2: `record_id` R01…RNN, ONE claim per record in the work's own
words, exact verbatim `span`, `source` file path + section heading.
Limitation records ("X fails / is weak / does not generalize / remains
open / was downgraded / is not yet met") are first-class records.

Do NOT assign epistemic labels. Do NOT summarize. Do NOT add commentary.

## Typed relations

`supports`, `implements`, `exemplifies`, `refines` — as in v2.

`contradicts` (THIS VARIANT'S RULE — replaces v2's): a record
contradicts another iff EITHER
  (i) it asserts the negation of a claim the other asserts (strict), OR
 (ii) it is a LIMITATION record (downgrade / failure / weakness /
      open item / "not yet met" / observed-not-proved) targeting the
      same item, claim, or verdict the other record affirms.
In other words: where v2 would label a downgrade or limitation as
`refines`, YOU label it `contradicts` — a downgrade of a PASS, a
limitation of a determination claim, an "observed not proved" against
a positivity claim, an OPEN against a MET, all count.

Each link: `{source_id, target_id, rel, reason}` — one line stating the
specific textual basis (quote fragments welcome). If you cannot state
the basis in one line, do not make the link.

## Link discipline

- ≥3 typed links per record (in + out). Malformed records get fixed
  before finishing.
- Use `contradicts` wherever clause (i) or (ii) is met. Never force it
  where neither is met — a missing contradicts is fine; a false one is
  a defect.
- Prefer within-batch links (records from this same source file).

## Output

Write JSON to the assigned output path:
`{"records": [...], "links": [...]}`.
Then report: record count, total links, mean degree (links per record,
in+out), and the count/share of `contradicts` links.
