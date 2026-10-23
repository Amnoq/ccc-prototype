# Atlas-8 Run Log

## 2026-10-07 — charter + setup
- Charter: ATLAS8_CHARTER.md (user's tap: "Charter Atlas-8 — the prime-distribution run").
- Coordinator: Atlas-8 coordinator subagent (this log's author).
- Foreign-sky retrieval: dispatched to retriever subagent (PNT/Zagier, Cramér/Granville, Zhang, Maynard, Green–Tao, sieve lineage; ~10–12 chunks; S1 control = Maynard→Zhang/GPY citation note; BK2011 for drops).
- Home-sky chunks staged from the pilot corpus (read-only): home_sieve1..4 (EXPERIMENT_REPORT + PAPER_OUTLINE; FRAMEWORK_WHOLE_VIEW p1; DERIVATIONS p1 D1–D8; DERIVATIONS p2 D9–D10c), 8,610 words total. Provenance: chunks/_home_provenance.json.
- Home-sky drafter brief: HOME_DRAFTER_BRIEF.md (blind to foreign sky).
- Sieve ground truth: ~/workspace/prime-sieve-geometry/sieve_complex.py — imports clean; linear_circle_sieve(N) is the executable number line. Verification scripts may IMPORT, never modify.

## 2026-10-07 — home-sky drafters launched
- 4 blind home-sky drafters spawned (home_sieve1..4), each with HOME_DRAFTER_BRIEF.md, blind to the foreign sky.
- Foreign-sky retrieval still running (retriever subagent).
- Next: foreign-sky drafters once chunks land; then merge_atlas8.py (adapted from merge_atlas7.py); adjudication; crack hunt; crack verification against sieve_complex.py; money view; report + grading packet.

## 2026-10-07 — home_sieve3 extraction complete
- home_sieve3.json: 15 concepts, 16 anchors, 18 edges, 4 loops, 4 strands. High quality; epistemic labels preserved (D1 exact at x=30/100/500; D4 S(X) to 2e6; D6 singular series 1.32032…; D7/D8 verification numbers in notes).
- Remaining: home_sieve1, home_sieve2, home_sieve4 drafters + foreign-sky retrieval.

## 2026-10-07 — home_sieve1 + home_sieve2 extractions complete
- home_sieve1.json: 24 concepts, 25 anchors, 22 edges, 3 loops, 7 strands. Notes: two-document concatenation (report + outline); homology table N=2000 row incomplete, recorded as-is.
- home_sieve2.json: 33 concepts, 33 anchors, 30 edges, 4 loops, 7 strands (10 verified / 9 killed / 8 exact / 5 heuristic / 1 conjectural). Notes: §VIII is a stub; D10 split into 5 concepts c14a–e.
- Home sky so far: 72 concepts across 3 chunks. Remaining: home_sieve4 drafter + foreign-sky retrieval.

## 2026-10-07 — home_sieve4 extraction complete; HOME SKY DONE
- home_sieve4.json: 22 concepts, 24 anchors, 18 edges, 2 loops, 4 strands (15 exact / 6 verified / 2 heuristic / 1 conjectural). QUALITY NOTE: the source chunk is truncated mid-D10c (Selberg λ² section cut off mid-sentence in the pilot's DERIVATIONS__p2.txt itself) — 10c claims extracted as incomplete; crack verification must not demand the missing optimizer/minimum/comparison.
- HOME SKY COMPLETE: 94 concepts across 4 chunks (sieve1: 24, sieve2: 33, sieve3: 15, sieve4: 22).
- Remaining: foreign-sky retrieval only.

## 2026-10-07 — SPAN DIRECTIVE folded in (user's standing instruction)
- Charter Protocol amended (item 7): spans between primes (gaps) are first-class concepts in extraction AND adjudication. His words: "like music — if we want to hear the song the zeta zeros are singing, we must pay attention to the spans in between; the song is in the intervals, not just the notes."
- SPAN_DRAFTER_BRIEF.md written; 4 supplementary span-pass drafters spawned on home_sieve1..4 (ids sp1..spN, blind to foreign sky). Merge will ingest both home_sieve<N>.json and home_sieve<N>_spans.json.
- Foreign-sky drafters (spawned after retrieval lands) will carry the span directive in their briefs: capture gap-structure claims wherever they appear (prime gaps, zero spacings, orbit-length intervals, rests between tones).
- Crack hunt will give spans priority: for each crack candidate, check what the literature states about the spans vs what the sieve shows.

## 2026-10-07 — home_sieve4 span pass complete
- home_sieve4_spans.json: 9 span concepts (sp1–sp9), 9 anchors, 6 edges, 3 loops, 3 strands: windowed zero detector span quantities (window widths, leakage 0.68→0.30→0.0007, window-edge positions), zero-height truncation vs error, residue-pattern autocorrelation spans, twin-residue {0,2} blind spot (a1=0 — a concrete gap-inventory datum).
- Remaining: span passes for sieve1–3 + foreign-sky retrieval.

## 2026-10-07 — home_sieve3 span pass complete
- home_sieve3_spans.json: 7 span concepts (sp1–sp7): zero-locus distances, deformed-sieve spanning-circle intervals [kp−2,(k+1)p−2], gap-2 constellation as native gap pattern (twin lowers to 200k), forbidden-residue inventory R_p with δ(7)=0.071429, zeros regulating face-sum error intervals, singular series → 2C₂, φ(x,a) span re-partitioning.
- Merge guidance from drafter: sp2 (spanning-circle intervals) and sp5 (zero-interval emphasis) genuinely supplementary; sp1/sp3/sp4/sp6/sp7 are span re-framings of main-pass c4/c7/c3.
- Remaining: span passes for sieve1, sieve2 + foreign-sky retrieval.

## 2026-10-07 — home_sieve2 span pass complete
- home_sieve2_spans.json: 12 span concepts (sp1–sp12): gap-pattern constellations (twin gap-2 survivor class, HL constant derived as renormalized weight, twin density UNPROVEN honest boundary, 9 k-tuple combos + {0,2,4} control, admissibility obstruction uninserted), binary distance form F_prior, tone interval structure (11l/11n/11o), spectral spacing statistics (13d GUE, 13e no-hearing).
- Crack-hunt gold flagged: sieve shows the twin-density weight mechanism; the analytic density proof is absent — an unstated-touch candidate.
- Remaining: span pass for sieve1 + foreign-sky retrieval.

## 2026-10-07 — home_sieve1 span pass complete; ALL SPAN PASSES DONE
- home_sieve1_spans.json: 11 span concepts (sp1–sp11): unshared-point spacings = prime gaps (verified N=30…2000), spam-forward marking rule, F(n) distance-to-boundary, b_0 large-gap tail (isolated vertex per prime in (N/2,N]), twin gap-2 combo as sieve output (survivors to 2e5), 2C₂ as renormalized weight (π₂ asymptotic NOT claimed), zeros as face-sum interval regulators, CCM triple from Euler products alone.
- VOCABULARY NOTE: this drafter used non-standard genre values (experiment_report/paper_outline) and inferred rels (derives-from, quantifies) — my brief referenced the main brief's vocabularies but the drafter was correctly blind to that file. Merge will remap: experiment_report→verified, paper_outline→original, derives-from→depends_on, quantifies→supports. Recorded here.
- SPAN PASSES COMPLETE: 39 span concepts (11+12+7+9). HOME SKY TOTAL: 133 concepts (94 main + 39 spans) across 8 extraction files.
- Remaining: foreign-sky retrieval only.

## 2026-10-07 — 11 foreign-sky drafters launched
- All blind to the home sky; each carries FOREIGN_DRAFTER_BRIEF.md (Atlas-2 schema + span directive + S1 control note for maynard_p1).
- Corpus final: 11 foreign chunks (17,683 words) + 4 home chunks + 4 home span-pass chunks (8,610 + span words). 0 drops.
- Next: merge_atlas8.py (adapt merge_atlas7.py; ingest home_sieve<N>.json + home_sieve<N>_spans.json + foreign_*.json; remap table for sieve1 span-pass vocabularies) → candidates (mechanical + semantic) → adjudication → crack hunt (span priority) → crack verification vs sieve_complex.py → money view PNG → ATLAS8_REPORT.md + CRACK_LIST.md + grading packet.

## 2026-10-07 — foreign extractions 2/11 in (cramer_p1, zhang_p2)
- foreign_cramer_p1.json: 16 concepts, 16 anchors, 16 edges, 1 loop, 3 strands. 8 span concepts (Em construction, P(Em)~m^-c, probability-1 gap theorem, Cramér's conjecture max gap ~ log²x, Shanks reformulation, record-gaps table, Poisson short-interval law). Notes: OCR garbling in 3 formulas (noted); chunk truncated mid-sentence at end (small-y confirmation incomplete → heuristic).
- foreign_zhang_p2.json: 13 concepts, 13 anchors, 13 edges, 0 loops, 3 strands (dispersion method, Type I/II setup, S1−2S2+S3 decomposition). 4 span concepts (N-intervals, R-ranges). Notes: heavy OCR garbling of displayed math; truncated mid-sentence (7.9 proof not in chunk).
- Remaining: 9 foreign drafters.

## 2026-10-07 — foreign extraction 3/11 in (greentao_p2)
- foreign_greentao_p2.json: 21 concepts, 21 anchors, 19 edges, 3 loops, 3 strands (§2 outline: Szemerédi, W-trick, transference strategy). 4 span concepts (Goldston–Yıldırım gap majorant, W-trick residue spacing, AP interval structure, AP-count). Notes: ar5iv formula-duplication artifacts; section complete.
- Remaining: 8 foreign drafters.

## 2026-10-07 — foreign extractions 5/11 in (zhang_p1, maynard_p3)
- foreign_zhang_p1.json: 21 concepts, 21 anchors, 18 edges, 1 loop, 4 strands (§1+§2: gap-2 conjecture, bounded gaps, GPY, admissible k-tuple as gap pattern, Theorem 1 → liminf < 7×10^7; all key numbers in notes). 6 span concepts. Notes: heavy JSTOR OCR garbling, garbled numbers reconstructed with OCR form noted.
- foreign_maynard_p3.json: 21 concepts, 21 anchors, 22 edges, 0 loops, 4 strands (§5: Lemmas 5.1–5.3 diagonalization, support restriction, level of distribution, BV error control). 3 span concepts (dyadic intervals, residue-class restriction, k shifts as gap pattern). Notes: mild ar5iv formula duplication; section complete.
- Remaining: 6 foreign drafters (pnt, maynard_p1, maynard_p2, greentao_p1, greentao_p3, sieve).

## 2026-10-07 — foreign extraction 6/11 in (pnt_p1)
- foreign_pnt_p1.json: 15 concepts, 15 anchors, 13 edges, 0 loops, 3 strands (Zagier/Newman: ζ/ψ/π definitions, Euler product, non-vanishing via 3+4cosθ+cos2θ, Newman's analytic theorem, ψ∼x ⇒ π∼x/log x). 2 span concepts (dyadic interval estimate ψ(x)−ψ(x/2), the (VI) interval contradiction). Notes: heavy JSTOR OCR symbol garbling; all prose recoverable.
- Remaining: 5 foreign drafters (maynard_p1, maynard_p2, greentao_p1, greentao_p3, sieve).

## 2026-10-07 — foreign extractions 8/11 in (maynard_p2, greentao_p1)
- foreign_maynard_p2.json: 20 concepts, 20 anchors, 20 edges, 0 loops, 4 strands (§2–§4: S(N,ρ) criterion, multidimensional weights, M_k bounds, Prop 4.2, Thms 1.1/1.3/1.4). 8 span concepts (admissible ℋ as gap pattern, liminf ≤ 600 unconditional, ≤12 under EH). S1-adjacent: c9 (Selberg twin suggestion + GY weights as prior art).
- foreign_greentao_p1.json: 19 concepts, 19 anchors, 16 edges, 1 loop, 4 strands (abstract+§1: Thms 1.1/1.2, HL AP conjecture, record APs with explicit coefficients). 10 span concepts (APs as interval/gap patterns). Loop: HL asymptotic explicitly unestablished.
- Remaining: 3 foreign drafters (maynard_p1, greentao_p3, sieve).

## 2026-10-07 — foreign extraction 9/11 in (sieve_p1)
- foreign_sieve_p1.json: 23 concepts, 23 anchors, 23 edges, 3 loops, 6 strands (Elkies Selberg sieve: inequality, proof, applications). 6 span concepts (sifting intervals, level of distribution y=z=A^{1/2}/log²A, remainder range, prime pairs at fixed gap, Brun's convergence). Key numbers in notes (incl. "if the coefficient 2 were any smaller this would banish the Siegel-Landau zero").
- Remaining: 2 foreign drafters (maynard_p1, greentao_p3).

## 2026-10-07 — foreign extraction 10/11 in (maynard_p1)
- foreign_maynard_p1.json: 24 concepts, 25 anchors, 32 edges, 1 loop, 5 strands (abstract+§1: GPY, Zhang, polymath, Thms 1.1–1.4). 13 span concepts (all bounded-gap numbers). S1 CONTROL CAPTURED: c5 (Zhang [9], ≤70M), c13 (Zhang's key breakthrough, weakened (1.3) for θ>1/2), c3/c4/c12/c14 (GPY [5]).
- METHOD NOTE: cited-without-proof claims marked conjectural per calibration even when established theorems — merge must treat as citing-chunk artifact, not epistemic downgrade.
- Remaining: 1 foreign drafter (greentao_p3).

## 2026-10-07 — RUN COMPLETE
- Merge: 345 nodes, 328 edges, 32 loops; 885 pass-1 pairs reviewed (0 merges — main↔span restatements deliberately unmerged); 2468 mechanical candidates triaged.
- Adjudication: 13 verdicts (11 split_link, 2 rejected), 5 misses; S1 control RESOLVES (A8-01).
- Crack hunt: 5 candidates (span-priority) → 4 verified vs sieve_complex.py/deformed_sieve.py, 0 refuted, 1 undecidable (K8-5, truncated D10c).
- Deliverables: report, CRACK_LIST.md, adjudications, grading packet (20 triples + all), money PNG + HTML, manifest, verification scripts + outputs, run log, 3 drafter briefs.
