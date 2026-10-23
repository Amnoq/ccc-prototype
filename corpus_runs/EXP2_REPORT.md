# Experiment 2: Entity Resolution Across Chunks — Report (2026-10-03)

## Question
Can a cross-chunk entity registry merge coreferent concepts without corrupting
the registry? Bar from HARNESS_MVP_SCOPE §7: **precision ≥ 0.95 on merge
decisions** (a wrong merge silently corrupts; a missed merge only coins a
duplicate).

## Phase A — adjudication precision

- Mined 27,952 cross-chunk pairs from the 247 concepts in the 12 R3
  extractions (TF-IDF over labels + anchor notes; sentence-transformers
  uninstallable — disk full during pip, TF-IDF used instead).
- 300 pairs labeled by 3 blind judges (150 high / 100 mid / 50 low similarity):
  **79 SAME / 214 DIFFERENT / 7 UNCERTAIN**.
- I audited all 79 judge-proposed merges against the pairs: **0 false merges**.
  Closest call: M002 (ledger MISS list ↔ Deninger missing object) — defensible
  but creates dual-membership tension with H036 (MISS list ↔ ledger HAVE);
  flagged, not counted as error. Sensitivity: 78/79 = 0.987 even if M002
  were ruled wrong.
- **Adjudicator precision: 79/79 = 1.00** (95% lower bound 0.962 by rule of
  three). **Bar cleared.**
- Control: TF-IDF similarity alone as the merge rule never reaches the bar
  (precision 0.875 at sim≥0.5, 0.48 at sim≥0.2). The LLM adjudicator — not the
  ranker — is what earns ≥0.95. The ranker's job is candidate generation only.
- Registry built from c01–c11 via union-find over the 76 non-c12 SAME pairs:
  **228 concepts → 162 entities** (66 effective merges; 40 entities have
  aliases). c12 held out.

## Phase B2 — post-hoc merge hook on held-out c12 (the scope's phase-1 design)

- Per c12 concept: TF-IDF top-5 retrieval over the 162-entity registry, then
  independent LLM adjudication (MERGE / KEEP-SEPARATE), merge on any MERGE.
- Ground truth: 120 top c12–registry pairs labeled by a fourth blind judge
  (2 SAME / 116 DIFFERENT / 2 UNCERTAIN), which I audited. One UNCERTAIN
  (C075, D_log ↔ CCM triples) was **resolved SAME by source-text evidence**:
  the text cites the identical arXiv:2511.22755. Final truth: **3 aliases**
  in c12's 19 concepts (Deninger→E122, Weil→E058, D_log→E111).
- Hook proposed **2 merges, both correct** (Deninger, Weil).
  **Precision 2/2 = 1.00. Recall 2/3 = 0.67.** Zero false merges.
- The miss is instructive: E111 was not in c12/c4's TF-IDF top-5 (the shared
  arXiv token lived only in the source prose, not the concept label/note),
  and label-only adjudication could not resolve it. **Retrieval recall, not
  adjudicator precision, is the hook's binding constraint.**
- Duplicate-coin rate on c12: 3/19 without registry → 1/19 with hook.

## Phase B1 — registry-in-prompt re-extraction (architecture comparison)

- Blind extractor given the full 162-entity registry (~5.5k tokens) + c12
  source, instructed to reuse IDs when confident.
- Result: 18 concepts, **8 registry IDs reused**, 10 fresh.
- Audit vs source text: **4 true merges** (Deninger→E122, Weil→E058,
  D_log→E111, reimplement-target→E113), **4 borderline** (E083: text equates
  Selberg control with "D10d function-field template" — text-faithful but
  entity-loose; E110 Connes formula↔space — granularity; E120 kill
  bundle↔bundle — survey-identity; E143 bounded-heuristic computation ↔
  conjectural 3D posit — epistemic-kind), **0 clean false merges**.
- B1 caught the D_log alias B2 missed (full-text arXiv evidence), but merged
  2× as aggressively (8 vs 2) with half its merges debatable.

## Findings

1. **The ≥0.95 precision bar is cleared by TF-IDF retrieval + LLM
   adjudication** (Phase A: 1.00, 95% LB 0.962; Phase B2: 1.00, 0 false
   merges). Entity resolution is safe to deploy as a post-hoc merge hook.
2. **Keep extraction blind; merge post-hoc.** Registry-in-prompt shifts the
   operating point toward aggressive merging (8 vs 2 merges, 4 debatable)
   and costs ~5.5k prompt tokens per extraction against break-even. The
   scope's phase-1 design (merge hook, not registry-in-prompt) is vindicated.
3. **Recall lever is retrieval, not adjudication.** The one B2 miss came from
   top-5 TF-IDF retrieval, and the one label-UNCERTAIN was resolved by
   full-text evidence. Upgrades: denser retrieval signals (arXiv/citation
   tokens, formula fingerprints), and full-text evidence for adjudicating
   near-matches rather than label-only.
4. **Granularity modeling needed before scale-up:** the M002/H036 tension
   (ledger section vs Deninger missing-object — one span, two entities) and
   the E083 case (role-identity "both are working templates" vs
   entity-identity) show concept-granularity merging needs rules for
   dual-membership and role-vs-entity equations. Currently 1 tension in 79
   merges; watch the rate as the registry grows.

## Effect on the omission taxonomy
Cross-chunk bridge handling measured directly: duplicate coining on the
held-out chunk falls from 3/19 (16%) to 1/19 (hook) / 0/19 (registry-aware
extraction). The R2/R3 "cross-chunk bridge" omission class — same idea
re-coined per chunk instead of linked — is now mechanically closable.

## Human adjudication queue (8 distinct questions)
1. H096 — "no known positive region for the sieve" (c02) vs "ordinary
   positive region carrying w(S) exists" (c11, superseded): same existence
   question with contradictory verdicts, or different objects?
2. M043 — two 3-4-1 verifications via different routes (energy translation
   vs Lambda-sieve): one entity or two?
3. M050 — CCM zero-recovery headline vs even-subspace eigenvalue detail:
   same experiment, distinct claims — merge?
4. M052 / C023 — 8-point operator audit checklist vs R1–R6 Frobenius
   checklist: same evolving instrument?
5. M064 — two "D10a step-3"s describing different activities (square-H
   optimization vs prime-side detector): naming collision or one step?
6. L015 — "no known positive region" (c02 gap) vs "obstruction theorem"
   (c11): gap later resolved, or different objects (sieve region vs w(S))?
7. L021 — deformation definition vs "deformation derives twin constant":
   enriched definition or distinct derivation claim?
8. M002/H036 — ledger MISS list: ledger section, Deninger missing-object,
   or both (dual membership)?

## Limitations
- Corpus is one author's research notes; 12 chunks, 247 concepts.
- Ground truth for c12 covers sim ≥ 0.081 (top 120 of 3,078 pairs);
  aliases below that floor are unmeasured (likely few: steep drop + novel chunk).
- B2 recall measured on n=3 true aliases — the 0.67 is a point estimate
  with a wide interval, not a precise recall claim.
- Adjudicators are LLM judges with human audit; the audit is the anchor,
  and M002 shows where the anchor itself is soft.

## Artifacts
- `corpus_runs/exp2_candidate_pairs.json` — top 600 TF-IDF pairs (all chunks)
- `corpus_runs/exp2_batches/batch_{H,M,L,C}.json` + `labels_{H,M,L,C}.json`
- `corpus_runs/exp2_registry.json` — 162-entity registry (c01–c11)
- `corpus_runs/exp2_registry_prompt.txt` — registry rendered for prompts
- `corpus_runs/exp2_hook_candidates.json` + `exp2_hook_decisions.json` (B2)
- `corpus_runs/exp2_c12_registry_extraction.json` (B1)
- `exp2_pairs.py`, `exp2_merge_hook.py`

---

## Rigorous close-out (2026-10-03, second pass — "leave no stone unturned")

The initial report above is SUPERSEDED by this section. A dual-judge
replication found shared ontology bias between the first judge and my own
audit. Everything below was re-derived under principle P (strict), decided
2026-10-03: **a posit and its resolution are distinct entities**
(question≠verdict, hypothesis≠killing-theorem, proposal≠closure,
verification≠claim). Rationale: the registry has no status/polarity field,
so merging "P hypothesized" with "¬P proved" risks resurrecting dead
posits on rehydration; and the scope's own rule is "prefer missed merges
over false merges." The loose alternative (Q: an investigation is one
entity through its lifecycle) is defensible but needs status-annotated
entities — recorded as a v6 schema design note.

### R1 — dual-judge replication of the 300-pair battery
- Second blind judge relabeled all 300 H/M/L pairs. Agreement: H 90%,
  M 97%, L 98%. The high-similarity stratum is where ontology fights live.
- 15 H disagreements crossed the SAME boundary; I audited all 14 plus the
  M/L crossings. Finding: my original audit shared judge 1's loose
  ontology on 4 pairs — I had explicitly waved through question+verdict
  as "status update" (H037, H047), verdict+evidence as "adds technical
  detail" (H053), and result+undercutting-control as "control arm of one
  entity" (H107). The bias check worked exactly as designed.
- Under principle P, the corrected Phase-A verdicts:
  - False merges (judge-1 SAME → DIFFERENT): H037, H047, H053, H107,
    M002 (ledger MISS list ≠ Deninger program; inventory ≠ program).
  - Uncertain: H054 (K-theoretic F_z'(1) home vs E_z home — same evolving
    home or two rivals; unresolvable from labels).
  - Missed merges added: H060 (zeros-regulate-face-sum, two routes),
    M008 (PNT-as-total-weight-1 + "no prior art" status).
  - Tie-breaks decided under P: H096→DIFFERENT (superseded posit ≠
    current gap), H140→UNCERTAIN, M043→DIFFERENT (two verifications =
    two experiment entities; the theorem is the shared entity),
    L015→DIFFERENT.
- **Corrected adjudicator precision: 73/78 = 0.936** (excluding H054),
  73/79 = 0.924 (counting it wrong). **The ≥0.95 bar is NOT cleared
  under the strict standard.** (Under principle Q it would be 76/78 =
  0.974 — the bar result is principle-relative; P is the decided
  standard.) Corrected pair list: `corpus_runs/exp2_corrected_pairs.json`
  (75 SAME pairs).

### R2 — below-retrieval-floor test
- 300 random cross-chunk pairs from below the TF-IDF top-600 floor,
  labeled by TWO independent judges: **300/300 agreement, 0 SAME**.
  The ranker's recall gap is bounded: no aliases hiding below the floor
  in the sample (95% upper bound ≈1%).

### R3 — twelve-fold held-out-chunk cross-validation
- Per fold: registry rebuilt from the other 11 chunks (union-find over
  corrected SAME pairs), top-150 held×registry pairs labeled as ground
  truth (1,800 pairs, 6 judges), top-5 candidates per concept adjudicated
  MERGE/KEEP-SEPARATE (1,275 candidates, 6 judges, strict standard).
- All 1,800 truth labels validated; I audited every hook MERGE (115),
  a random 15 of the agreed ones (caught 1 shared-bias case), and swept
  the risky pair-types (template-vs-verification, two-verifications,
  bundle-vs-component) for 4 more.
- Truth-label corrections under P: 17 flipped + 1 excluded as
  unresolvable (144 → 126 corrected aliases).
- **Retrieval: recall@5 = 0.95, recall@1 = 0.67** (9 misses audited; 8
  genuine, incl. the D_log/arXiv case reproducing — shared-identifier
  evidence lives outside TF-IDF's reach; 1 disputed).
- **Hook (post-hoc merge), 12-fold pooled: precision 98/117 = 0.84,
  recall 98/126 = 0.78.** Per-fold precision 0.17–1.00, recall
  0.33–1.00 — wide fold variation; c09's judge over-merged D_log/Connes
  pairs (0.17). The hook is conservative (9% merge rate) as instructed.
- Registry-completeness finding: the hook caught 2 duplicate entities
  the registry builders missed (uncertainty scaling law ×2, Weil
  criterion ×2) — the hook earns its keep finding missed merges too.
- Rebuilt artifacts: `corpus_runs/exp2_registry_v2.json` (181 entities,
  41 with aliases, all 12 chunks), `corpus_runs/exp2_folds/` v2
  registries + regenerated hook candidates (68 changed candidates
  re-audited by hand; 1,207 reused).

### Corrected architectural conclusion
- The adjudicator does NOT clear the 0.95 bar under the strict standard
  (0.924–0.936). The bar failure is small but real, and it is
  principle-relative — documented, not hidden.
- The post-hoc merge hook validates as the architecture (blind
  extraction + merge hook), but its measured precision is 0.84, not
  1.00: the hook needs the strict adjudication standard and ideally
  exact-identifier retrieval features (arXiv/formula matching) to close
  the D_log-type recall gap.
- Registry-in-prompt (B1) remains the more aggressive operating point,
  not the deployed design.

## Epistemic labels for the headline claims
- Hook precision 0.84 / recall 0.78 (12-fold CV): **computationally
  verified** (1,275 adjudications + full audit).
- Adjudicator precision 0.924–0.936: **computationally verified**
  (dual-judge + audit, principle-P-relative).
- "Bar cleared": **REFUTED under P** (was: claimed). Retained under Q
  only (0.962–0.974) — Q not adopted.
- Below-floor alias rate ≈ 0: **computationally verified** (600
  judgments, two raters).
- Retrieval recall@5 ≈ 0.95: **computationally verified** (12-fold).
