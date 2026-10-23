# Bridge-deletion test — Atlas-6 (with Atlas-4 control)

**Date:** 2026-10-09
**Status:** read-only analysis — no atlas records modified.
**Source records:** `cross_bridge_links.json` (13 adjudications: 9 split_link, 4 rejected),
`graphs/atlas6_graph.json` (117 nodes), `ATLAS6_REPORT.md`.

## The test

Delete the explicit-formula node(s) from the adjudicated graph and count how many
of the nine split_links are destroyed (touch a deleted node) vs survive intact.
Reviewer's hypothesis: if all nine touch the deleted node(s), the finding is one
crack with nine facets, not nine independent bridges.

## Deletion set (Atlas-6)

Nodes that **are** Weil's explicit formula / the Guinand–Weil formula / the W(f,g)
Hermitian form — identified from node labels and adjudication reasons:

| # | Node ID | Label (truncated) | Why it counts |
|---|---|---|---|
| 1 | `af:a-w-f-g-m-f-conj-g-1-2-i-weil-s-hermitian-form-o` | (a) W(f,g) = Σ_ρ m_ρ f̂(γ_ρ)·conj(ĝ(γ̄_ρ)) — Weil's Hermitian form | S0 reason: "Same named classical referent: Weil's explicit formula / Hermitian form" |
| 2 | `af:b-weil-s-explicit-formula-as-one-of-the-paper-s-` | (b) Weil's explicit formula as one of the paper's arithmetic inputs (§1.1) | A6 reason: "Both take the explicit formula as input" |
| 3 | `rel:symmetric-guinand-weil-formula-with-square-test-` | Symmetric Guinand-Weil formula with square test h_a(r), normalization confirmed by own numerics | S0 pilot side of the same referent |
| 4 | `rel:the-explicit-formula-grounded-in-our-objects-psi` | The explicit formula grounded in our objects — ψ(x) from the D1 face-sum | A6 reason: "the pilot re-ground it in its own objects" |
| 5 | `rel:the-guinand-weil-explicit-formula-as-the-bridge-` | The Guinand-Weil explicit formula as the bridge: arithmetic side = prime-power sum minus archimedean terms | A12 reason: "Both name the Guinand–Weil formula" |

**Borderline, excluded from the strict set:** `bom:the-guinand-1942-weil-1952-lineage-local-role-d-`
("The Guinand 1942 → Weil 1952 lineage") — historiography *about* the formula, not the
formula as a mathematical object. Sensitivity check: it appears only in A12, which is
already destroyed via its other endpoint, so strict vs. broad deletion sets give the
identical result.

## Per-link results (Atlas-6)

| Link | Relation | Analytic endpoint | Relational endpoint | Result |
|---|---|---|---|---|
| S0 | shares-classical-object | W(f,g) Hermitian form (af) — **deleted** | symmetric Guinand-Weil formula (rel) — **deleted** | **DESTROYED** (both ends) |
| A1 | shares-cited-criterion | Weil's RH-positivity criterion, BOM restatement | Weil's criterion W(h)≥0, pilot honesty boundary | **SURVIVES** |
| A2 | shares-criterion | Li's criterion (BOM proof lemma) | Li's criterion via face-sum (10b) | **SURVIVES** |
| A3 | lineage-cited-vs-independently-derived | g=f∗f̃ autocorrelation lineage (GRO, via Weil [29]) | square dictionary h=\|H\|² ↔ P=\|Q\|² (pilot derivation) | **SURVIVES** |
| A5 | proved-source-vs-cited-use | Bomberi Thm 8: negative eigenvalues count off-line pairs | AF's citation of the negative-index observation | **SURVIVES** |
| A6 | shared-input-different-grounding | Weil's explicit formula as AF input — **deleted** | explicit formula re-grounded in ψ/face-sum — **deleted** | **DESTROYED** (both ends) |
| A8 | object-vs-criterion-about-it | Weil's RH-positivity criterion (BOM) | W(f,g) Hermitian form (af) — **deleted** | **DESTROYED** (AF end; within-analytic-side link) |
| A11 | shared-cited-equivalence | Weil positivity ⟺ RH framing (GRO) | positivity of W on C_c²(R) ⟺ RH (AF) | **SURVIVES** |
| A12 | lineage-account-vs-working-use | Guinand→Weil lineage (BOM) | Guinand-Weil formula as bridge (rel) — **deleted** | **DESTROYED** (relational-side end) |

**Mechanical tally: 4 destroyed, 5 survive.**

## Atlas-4 control

Same procedure on `cross_sky_links.json`: 4 adjudicated split_links, deleted all
`bri:` (LeCun-89 bridge paper) nodes.

| Link | Relation | Endpoints | Touches bridge? |
|---|---|---|---|
| 1 | method-application | bri:constrained-backpropagation ↔ con:generalized-delta-rule | yes |
| 2 | biological-precedent | bri:synthesized-kernels ↔ neu:on/off cortical regions | yes |
| 3 | shares-concept | bri:constrained-backpropagation ↔ sta:VC-dimension bound | yes |
| 4 | shared-dataset | bri:data-base-9298 ↔ sta:USPS digit database | yes |

**Control result: 4/4 destroyed — all Atlas-4 links touch the bridge paper's nodes.**
The method behaves as the reviewer predicted on Atlas-4 (links there were defined as
bridge↔sky pairs, so this is the expected outcome, and it validates the test
machinery rather than discovering something new).

## Verdict

**The sharp hypothesis is not confirmed mechanically: 5 of 9 Atlas-6 split_links
survive deletion of the explicit-formula nodes.** It is not "one crack with nine
facets" in the strict graph sense.

Interpretive layer — what the five survivors are:

- **A2 (Li's criterion) — the cleanest independent candidate.** Distinct classical
  referent (Li 1997, via Bombieri–Lagarias); neither endpoint is a Weil-formula
  node. Caveat: Li's criterion is conventionally proved *through* the explicit
  formula, so its independence is adjudication-level, not mathematical.
- **A3 (square dictionary / g=f∗f̃ move) — the notable one for Node 10a.** The
  pilot *derived* the positivity-manufacturing mechanism independently (exact),
  which is precisely the kind of independent geometric sourcing the Node 10a
  circularity warning demands. The shared referent is still named as Weil's
  autocorrelation move, so it sits inside the Weil complex — but it is the only
  survivor with an independently-derived (not cited) pilot side.
- **A1, A11 (Weil's RH-positivity criterion / positivity⟺RH equivalence), A5
  (Bombieri Thm 8, negative index)** — facets of the same Weil-1952 complex at one
  remove: the criterion/equivalence *about* the formula's positivity, and the
  index theorem *about* its truncations. Same crack, different facets.

**Bottom line: one crack (the Weil complex) with ~8 facets + 1 independent
candidate (A2, Li's criterion), with A3 flagged as the independently-derived
mechanism most relevant to the Node 10a requirement that positivity come from
the geometry alone.** A1's pilot side remains the cited honesty boundary —
the circularity warning applies there unchanged.

## Limits of this test

- Node identity is adjudicator-labeled; "the explicit-formula node(s)" is an
  interpretive judgment, though the sensitivity check (lineage node in/out)
  leaves the tally unchanged.
- Deletion is graph-mechanical: a surviving link can still be conceptually
  downstream of the formula (A1/A11/A5 arguably are). The test separates
  "touches the formula object" from "about the formula's neighborhood," which
  is a real distinction but not the same as full independence.
- Atlas-4's 4/4 is partly by construction (cross-links were defined against the
  bridge paper); Atlas-6's link population is structurally different (includes
  analytic↔analytic links A5/A8/A11), so the control validates the method, not
  a parallel substantive claim.
