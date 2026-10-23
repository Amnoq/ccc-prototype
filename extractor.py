"""extractor.py -- M2: LLM extractor prompt + repair-loop driver.

The driver is model-agnostic: it takes llm_fn(prompt_text) -> response_text.
M2 acceptance was run with the author as the LLM (see M2_REPORT.md); what is
under test is the prompt and the repair protocol, not any particular model.

The prompt is self-contained: schema, vocabularies, and rules all inline, so
any instruction-following LLM can serve as llm_fn without extra context.
"""

import json

import memory_harness as mh

SCHEMA_SPEC = """\
You extract the argumentative structure of a technical discussion into a
strict JSON object with exactly these keys:

{
  "concepts": [{"id": "c1", "label": "...", "kind": "..."}],
  "strands": [{"id": "s1", "label": "c1" | null,
               "concept_ids": ["c1", "c2"]}],
  "edges": [{"a": "c1", "b": "c2", "rel": "..."}],
  "anchors": [{"concept_id": "c1", "status": "...", "note": "..."}],
  "loops": [{"concept_id": "c9"}]
}

RULES
- concepts: the load-bearing nouns of the discussion: claims, methods,
  results, entities, metrics, and open questions. "id" is a short string
  you invent ("c1", "c2", ...). "label" is the text's own noun phrase for
  it, specific enough to identify (not "the method" -- "Elias-gamma wire").
  "kind" is one of: claim, method, result, entity, metric, open_question.
  Extract the argument, not every noun: aim for 15-60 concepts. Merge
  near-duplicate phrasings of the same idea into ONE concept.
- strands: topic clusters. "label" is the id of the concept naming the
  strand's topic, or null if it has none. "concept_ids" is non-empty, no
  duplicates. A concept may belong to several strands.
- edges: DIRECTED claims relating two concepts. "rel" must be exactly one
  of: supports, contradicts, bounds, generalizes, implements, depends_on,
  causes, measures, defines, exemplifies, refines, supersedes.
  "a supports b" means the text says a backs b. No duplicate (a, b, rel).
  Prefer fewer, truer edges over many speculative ones.
- anchors: the epistemic status the TEXT establishes for a concept.
  "status" is one of: asserted, verified, superseded, open_question.
  "note" is a short phrase of evidence (optional). At most one anchor per
  concept. Do not mark something "verified" unless the text gives a
  measurement, proof, or decisive test.
- loops: open questions or unresolved items. Each references a concept
  (usually kind "open_question") -- the text of the question lives on the
  concept's label.
- Every id you reference must be declared in "concepts". Every "rel",
  "status", and "kind" must come from the vocabularies above -- no
  improvising.

OUTPUT: a single JSON object and nothing else. No markdown fences, no
commentary. If you are unsure between two readings, pick the one the text
most directly states; do not hedge with extra edges.
"""

EXTRACTOR_PROMPT = ("You are a precise information-extraction system. "
                    "Read the technical discussion below and extract its "
                    "argumentative structure.\n\n" + SCHEMA_SPEC +
                    "\n## Source text\n")

REPAIR_PROMPT = """\
Your previous extraction was rejected by a deterministic verifier. Below is
your previous output and the list of failures. Fix ONLY what the failures
require; do not restructure anything else. Output a single corrected JSON
object and nothing else.

## Your previous output
{previous}

## Verifier failures
{failures}

## Schema reminder
{schema}
"""


def extract_json_from_response(text):
    """Pull the first balanced {...} object out of a response. Raises
    mh.ExtractionError if none parses."""
    start = text.find("{")
    if start < 0:
        raise mh.ExtractionError(["no JSON object found in response"])
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError as e:
                        raise mh.ExtractionError(
                            [f"JSON parse error: {e}"])
    raise mh.ExtractionError(["unbalanced JSON in response"])


def count_tokens(text):
    import tiktoken
    return len(tiktoken.get_encoding("cl100k_base").encode(text))


def extract_with_repair(chunk_text, llm_fn, max_repairs=2,
                        schema_reminder=None):
    """Run the extractor with verifier-gated repair.

    Returns {"doc", "repairs_used", "warnings", "token_counts",
             "attempt_kinds"}. Raises mh.ExtractionError if all attempts
    fail validation. `schema_reminder` overrides the schema text shown
    to the model during repair (revisions layer their own rules there);
    defaults to SCHEMA_SPEC.
    """
    attempts = []
    schema = schema_reminder or SCHEMA_SPEC

    def run(prompt, kind):
        response = llm_fn(prompt)
        attempts.append(kind)
        return response

    prompt = EXTRACTOR_PROMPT + chunk_text
    response = run(prompt, "extract")
    in_tokens = count_tokens(prompt)
    out_tokens = count_tokens(response)

    for repair_n in range(max_repairs + 1):
        try:
            doc = extract_json_from_response(response)
            warnings = mh.validate_extraction(doc)
        except mh.ExtractionError as e:
            failures = e.failures
        else:
            return {"doc": doc,
                    "repairs_used": repair_n,
                    "warnings": warnings,
                    "token_counts": {"input": in_tokens,
                                     "output": out_tokens},
                    "attempt_kinds": attempts}
        if repair_n == max_repairs:
            raise mh.ExtractionError(
                [f"still invalid after {max_repairs} repairs"] + failures)
        rprompt = REPAIR_PROMPT.format(previous=response,
                                       failures="\n".join("- " + f
                                                          for f in failures),
                                       schema=schema)
        response = run(rprompt, "repair")
        in_tokens += count_tokens(rprompt)
        out_tokens += count_tokens(response)
