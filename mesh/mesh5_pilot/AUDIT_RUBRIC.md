# MESH-5 Pilot — Held-Out Link Audit Rubric

**Version:** 2026-10-09 (pre-registered before the audit runs).
**Your task:** re-verify every link on the assigned 40 records against
the relation definitions below. You are blind to which extractor
produced each record — judge only the link, never the source.

## Input

A JSON list of records with links: `{record_id, claim, span, links:
[{source_id, target_id, rel, reason}]}`. Extractor identity is stripped.

## Relation definitions (the check standard)

- `supports`: the source record's claim provides evidence, a reason, or
  a verified instance counting in favor of the target's claim.
- `implements`: the source describes a concrete computation, procedure,
  or worked instance realizing the target's general claim.
- `exemplifies`: the source is a specific case/instance of the target's
  general claim.
- `refines`: the source agrees with the target and sharpens, qualifies,
  or bounds it.
- `contradicts`: the source asserts the NEGATION of a claim the target
  asserts. Strict: difference of topic, difference of epistemic role
  for a shared object, or difference of scope is NOT contradicts.

## Verdict per link: PASS or FAIL

FAIL if any holds:
1. **Wrong type** — the cited basis does not meet the definition of the
   assigned rel (e.g., labeled `contradicts` but the records merely
   address different topics or roles; labeled `supports` but the basis
   is decorative).
2. **Fabricated basis** — the `reason` does not follow from the two
   records' claims/spans (the cited text doesn't say what the reason
   claims it says).
3. **Duplicate** — the same unordered record pair is linked more than
   once (redundant links inflate degree).

Otherwise PASS.

## Output

JSON: `{"results": [{"source_id","target_id","rel","verdict","note"}],
"n_links": N, "n_fail": F, "fail_rate": F/N}` to the assigned path.
Then report the fail rate. No other commentary.
