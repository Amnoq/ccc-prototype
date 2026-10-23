# Perplexity validation prompt — citation fidelity test

Paste the block below into Perplexity verbatim.

---

Verify each of the following factual claims against sources. Answer as a numbered list — one claim per item — and for each item give: (a) verdict: CONFIRMED, CORRECTED (with the corrected wording), or NOT FOUND; (b) the exact sentence from the source that supports your verdict, quoted; (c) the complete source URL written out as plain text (https://...) immediately after the claim, not as a bare footnote marker, so the link survives copy-paste.

Claims:
1. The English word "consciousness" is formed from "conscious" + "-ness."
2. Its Latin root is "conscius," from "com-" (with, together) + "scire" (to know), originally meaning "knowing, privy to" — a shared or mutual awareness.
3. The inward sense of "consciousness" ("knowing within oneself") first appears in English in the 1630s.
4. That inward sense developed through constructions such as "conscious to oneself."
5. In philosophy of mind, Ned Block distinguished "phenomenal consciousness" (what it is like to have an experience) from "access consciousness" (information available for reasoning and guiding action).

After the numbered list, add a clearly separated section labeled "Analysis" for any interpretive commentary. Keep interpretation out of the numbered list.

---

## What this tests

The previous run's substance was correct, but its citation markers came through empty — citation fidelity was ungradeable. This prompt fixes that by demanding, per atomic claim: a verdict, a quoted supporting sentence, and a full plain-text URL. Grading: (1) does each quoted sentence actually appear in its source; (2) does it actually support the claim; (3) are corrections accurate. A fabricated quote or a decorating citation is a hard fail.
