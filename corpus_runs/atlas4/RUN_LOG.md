# Atlas-4 RUN LOG

Phase notes from drafters and pipeline steps, chronological.

---

## 2026-10-07 — R4 drafter (neuro_hubelwiesel62, NEUROSCIENCE sky)

- **Assigned:** Hubel & Wiesel, 1962, "Receptive fields, binocular
  interaction and functional architecture in the cat's visual cortex",
  J. Physiology.
- **Primary URL tried:**
  `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1359523/` → 404
  (upstream_request_rejected, HTTP 404) via browser.open.
- **Backup URL tried:**
  `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1359523/pdf/jphysiol01247-0121.pdf`
  → 404 (upstream_request_rejected, HTTP 404) via browser.open.
- **Outcome:** FETCH FAILURE. Neither route returned the paper; no
  title verification was possible, and no other source was consulted
  (blind-per-sky; no substitution per task protocol and charter
  BK2011 rule: drop and record, never substitute secondary summaries).
- **Extraction:** NOT WRITTEN — no source text was obtained, so no
  empty/dummy JSON was produced (an empty draft would be
  indistinguishable from a null-result chunk at merge time).
- **Words in/out:** 0 / 0. Concepts/anchors/edges/loops/strands: n/a.
- **Action needed by coordinator:** supply a verified primary-text
  route (corrected URL, fetched chunk, or coordinator-confirmed
  substitute within the same tradition, recorded) before this sky can
  be drafted.

## 2026-10-07 — R4 blind drafter, BRIDGE (LeCun et al. 1989, "Backpropagation Applied to Handwritten Zip Code Recognition", Neural Computation 1(4):541-551)

- Provenance: primary URL https://raw.githubusercontent.com/Frost-Lee/disparity-recovery/master/neco.1989.1.4.541.pdf — fetched full text via browser.open (2 passes, 629 lines); title verified before extraction. Backup not needed.
- Words in: ~5,600 (est., full paper pp. 541–551, under the 12k threshold → whole paper extracted). Words out: ~1,766 (est.).
- Coverage: full extraction — abstract, intro, zip-code data base (2.1–2.2), network design (3.1–3.3), experimental environment (4), results incl. controls/comparison/DSP (5–5.2), conclusion, references.
- Extraction: bridge_lecun89.json — 22 concepts / 22 anchors / 20 edges / 1 loop / 5 strands. JSON parses; all ids resolve; every concept anchored.
- Blindness: worked only from this paper's own vocabulary; no other paper/tradition read or referenced. Cross-tradition terms (Hubel & Wiesel 1962 biological vision detectors; Rumelhart et al. 1986 backprop/weight-sharing) recorded only as the paper itself cites them — the S1/S2 positive-control links rest on those citations.
- Fidelity concerns: (1) PDF text-extraction garbling on the MSE figures ("2.5 x on the training set and 1 .8 x lop2 on the test set") — exponents unreadable, NOT treated as verified; error counts (0.14%/10, 5.0%/102) are clean. (2) Figure 2 text extraction garbled; figure captions otherwise recoverable. (3) The authors omit the H1→H2 map-subset selection scheme ("will not be described here") — a deliberate paper-level gap, not an extraction failure. (4) Reference list is the paper's own; no completeness check performed (drafter blindness).
- Notable contents for the S1/S2 controls: c13 (learned kernels resemble Hubel & Wiesel 1962 biological detectors — spatial derivative estimators, off-center/on-surround); c4 (weight sharing attributed to Rumelhart et al. 1986 T-C problem); c14 ("constrained backpropagation" framing: convolutional layers with learned kernels, shift-invariance, reduced entropy/VC-dim/free params); c22 killed (unconstrained fully-connected nets ruled out by the c12 control: 1.6% train / 8.1% test vs 0.14%/5.0%).

## R4 draft — symbolic_mccarthy59 (blind drafter, symbolic sky)

**Date:** 2026-10-07. **Paper:** John McCarthy, "Programs with Common Sense", 1959 (Teddington proceedings, pp. 75–91).
**Provenance:** primary URL returned only the jmvidal bibliographic page; the PDF fetch used the backup URL https://uploads.teachablecdn.com/attachments/u2vP37e6QQqYKaqOpGeM_McCarthy,+John+-+PROGRAMS+WITH+COMMON+SENSE.pdf — title "PROGRAMS WITH COMMON SENSE", author John McCarthy, Stanford, 1959 verified before extraction.
**Words in:** 5,505 (whole paper incl. references + discussion — under 12k, so full extraction, coverage 100%).
**Words out:** 1,616 (extraction JSON content). Token estimate: in ≈ 7,157 / out ≈ 2,101 (1.3× rule).
**Result:** 18 concepts (4 definition, 9 claim, 3 method, 1 conjecture, 1 question), 18 anchors, 17 edges, 2 loops, 6 strands. Schema validated against the pilot shape (concept ids unique; all anchors/edges/loops/strand ids resolve).
**Blindness:** never read or referenced any other paper or tradition; labels use the paper's own vocabulary (Advice Taker, common sense, immediate deduction routine, standing orders list, property lists, canachult, prog, do/want/at, stimulus-response).
**Fidelity concerns:**
- The whole paper is a *proposal* (unimplemented in 1959): most construction/heuristic concepts anchored `heuristic`; only the common-sense definition, the 8-step airport deduction *as presented*, and the stated intended conclusion earned `exact`. Do not let `exact` anchors be read as verified-implementation claims.
- The discussion section is included: Bar-Hillel's transitivity objection (c14) and relevance question (c15), Selfridge's amendability criterion (c16), McCarthy's replies (c17, c18) — genres `identification` for objections raised by others.
- The PDF text dropped some punctuation/formatting (e.g., "want(at(I, airport))" rendering, footnote markers); notation in labels follows the paper's intent. Minor OCR-ish artifacts in premise numbers were cross-checked against the deduction list.
- Nothing in this paper was `killed` or `computationally_verified` in its own terms.

## R4 draft — statistical_cortesvapnik95 (blind drafter, STATISTICAL sky)

**Date:** 2026-10-07. **Paper:** Corinna Cortes & Vladimir Vapnik, "Support-Vector Networks", Machine Learning 20:273-297 (1995).
**Provenance:** primary URL https://cafri-labs.github.io/lab-manual/papers/svm.pdf — full text fetched via browser.open (4 passes, 1961 extracted lines); title "Support-Vector Networks", authors Cortes/Vapnik, ML 20:273-297 verified before extraction. Backup (Springer) not needed.
**Words in:** ~9,000 (est., full paper incl. appendix + references — under ~12k, so whole paper extracted, coverage 100%).
**Words out:** 1,893 (extraction JSON content). Token estimate: in ≈ 11,700 / out ≈ 2,461 (1.3× rule).
**Result:** 22 concepts (4 definition, 11 claim, 4 method, 3 result), 22 anchors, 25 edges, 2 loops, 6 strands. Schema validated against the pilot shape (concept ids unique; all anchors/edges/loops/strand ids resolve).
**Blindness:** never read or referenced any other paper or tradition; labels use the paper's own vocabulary (support-vector network, optimal hyperplane, support vectors, soft margin, convolution of the dot-product, Mercer's condition, structural risk minimization, VC-dimension, Occam-Razor). Cited prior art (Fisher 1936, Rosenblatt 1962, Rumelhart–Hinton–Williams 1986 back-propagation, Aizerman et al. 1964 potential functions, LeNet1/LeNet4) recorded only as this paper cites them, with conjectural-from-this-paper statuses per the calibration rule.
**Fidelity concerns:**
- Heavy OCR garbling of mathematics (Greek letters → "~"/"Œ", superscripts/subscripts lost, equations interleaved); anchor notes carry concept content rather than formula detail. Equation/section numbers in notes (5, 15–18, 24, 30, 37–39, App. A.1/A.2) are as recovered from the text.
- "soft" rendered "soff", "learning" rendered "leaming" throughout — transcription noise in the source extraction, faithfully not in my labels.
- Note numbering in extraction jumps 5→7 (a note 6 appears absent in the extracted text — likely OCR loss, not paper structure).
- Tables 1–3 partially garbled but key numbers recoverable and recorded (Table 2 rows: error%/SV/feature-dim per degree; Table 3 per-classifier support counts 1379–2765; Fig. 9 benchmark ordering linear < LeNet1 < LeNet4 < SVN ≈ k=3-NN).
- Statuses applied strictly per calibration: cited theorems (Mercer, Hilbert–Schmidt, VC bound, support-vector bound) are `conjectural`-from-this-paper with citations; the universality and C-control readings are `heuristic`; all derivations in §§2–4/App. A are `exact`; the USPS/NIST experiments are `computationally_verified`.
- Loops are the paper's own open items: special-K convolution functions reflecting a priori knowledge (end of §6.2.2), and general monotone-convex F(u) beyond k=2 unused in experiments (App. A.2).

## 2026-10-07 — R4 blind drafter, NEUROSCIENCE sky (neuro_hubelwiesel59)

**Substitution record:** assigned substitute for the unobtainable Hubel & Wiesel 1962 ("Receptive fields, binocular interaction and functional architecture in the cat's visual cortex"; 4 genuine retrieval routes failed, logged above). Substitute: Hubel & Wiesel, 1959, "Receptive fields of single neurones in the cat's striate cortex", J. Physiology 148:574–591 — same authors, same research program (receptive fields of striate-cortex units; orientation/specificity groundwork of the 1962 paper).

**Provenance:** PMC route failed first — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1363130/ returned HTTP 404 via browser.open (same failure mode as the 1962 PMC fetch; old J. Physiology PMC records appear unservable through this path). Second genuine route: university/lab-hosted PDF found by search — https://papers.baulab.info/papers/HubelWiesel-1959.pdf — fetched full text via browser.open (4 passes, 968 lines); title/author/journal verified BEFORE extraction: "RECEPTIVE FIELDS OF SINGLE NEURONES IN THE CAT'S STRIATE CORTEX", D. H. Hubel and T. N. Wiesel, Wilmer Institute / Johns Hopkins, J. Physiol. (1959) 148, 574-591, received 22 April 1959. PMCID PMC1363130 / PMID 14403679 confirmed via PubMed search (search-only, used solely for the ID — blind per sky).

**Words in:** 7,518 (pdftotext of fetched PDF; under the 12k threshold → whole paper extracted). **Words out:** ~1,294 (extraction JSON content). Token estimate: in ≈ 9,773 / out ≈ 1,682 (1.3× rule).

**Coverage:** full extraction — intro (Kuffler/Hartline/Hubel-1959 lineage), methods (24 cats, thiopental + succinylcholine, ophthalmoscope + screen-projection mapping), results (45 units: field mapping, antagonism/summation, orientation, movement, binocular), discussion, 10-point summary, references. Figures described via captions/text only; oscilloscope-trace art unreadable in extraction (captions carry the findings, as the text narrates them).

**Result:** 23 concepts (2 definition, 7 claim, 2 method, 9 result, 2 conjecture, 1 question), 23 anchors, 19 edges, 3 loops, 5 strands. Schema validated against pilot shape (top-level keys identical; ids unique; all anchors/edges/loops/strand ids resolve).

**Blindness:** worked only from this paper's own vocabulary ('on'/'off' regions, excitatory/inhibitory, receptive field, slit, antagonism, summation, homologous parts, maintained activity, striate cortex, area centralis, tapetum). No other paper or tradition read or referenced. Note: this paper predates the 1962 functional-architecture paper, so "simple/complex cell" and columnar-architecture language does not appear — absence is period-accurate, not an omission.

**Fidelity concerns:**
1. Status calibration: this is an experimental paper, not a theorem paper. "exact" anchors = findings demonstrated in the paper's experiments (figure + count evidence); "conjectural" = precise statements the paper makes without proof (e.g. c14's exclusion of afferent fibres, c21's Jung reconciliation, c23's sampling caveat); "heuristic" = explicitly tentative suggestions (c15 convergence, c18 two functions, c19 relief/fixation). No "killed" anchors — the paper refutes no prior claim outright (it reconciles with Jung).
2. c1 is genre "reframed" (Hartline 1938 concept applied to cortex) rather than "original".
3. Numerical fidelity: counts recorded from text (36 monocular = 15 ipsilateral + 21 contralateral; 9 binocular; fields 4°–10°; maintained activity 0.1–10 impulses/sec; inhibitory region ~1° in Fig. 4's 12° field; stimulus durations ~1 sec). Minor PDF OCR artifacts (degree signs, log notation) were cross-checked against the summary points.
4. Loops: c9 (directional selectivity only tentatively explained), c21 (diffuse-light responders may be more common than detected), c23 (complex-property units under study; no classification attempted). c23 doubles as the paper's stated null-avoidance: no classification into separate groups.
5. Potentially load-bearing for S1 (positive control): c6 (orientation specificity), c7 (form/size/position/orientation specificity), c14 (non-concentric elongated arrangement — the detector form), c8 (movement responses) — these are the biological-detector findings the bridge paper (LeCun 1989) cites from this research program.

## R4 drafter phase notes — connectionist_rhw86 (CONNECTIONIST sky, 2026-10-07)

1. Provenance: primary URL http://www.cs.toronto.edu/~hinton/absps/pdp8.pdf — downloaded successfully (2,058,649 bytes, 46 pages, PDF 1.3). Title verified on chapter title page: "Learning Internal Representations by Error Propagation", D. E. Rumelhart, G. E. Hinton, R. J. Williams — PDP book Chapter 8. The http variant worked, so no variant was needed. browser.open itself could not extract text (scanned PDF, no text layer), so pages were rendered to PNG and read directly — same primary text, no substitution.
2. Words in/out: paper ~46 scan pages ≈ 12–14k words total (estimated from page density); coverage = first ~8.6k words (scan pages 1–32, book pp. ~318–346), sections THE PROBLEM through Addition. Excluded by the ~8k rule: Negation Problem, Shape from Shading, Further Generalizations (incl. arbitrary networks), concluding remarks, references. Words out: 2,022 (extraction JSON).
3. Counts: 21 concepts (7 claim, 4 definition, 2 method, 7 result, 1 conjecture), 22 anchors (12 exact, 8 computationally_verified, 1 conjectural [c3: linear-hidden-units claim credited to Chapter 2], 1 heuristic [c19: graded-encoding conjecture]), 20 edges, 3 loops (c5: local-minima/time questions left open; c15: frequency of local minima unknown; c4: promised generalization to arbitrary networks beyond coverage), 3 strands (derivation / machinery / simulation discoveries).
4. Fidelity concerns: (a) all math and numbers transcribed by eye from scanned page images — equation numbers 1–16, tables 1–8, figures 1–11 verified against the images, but figure-internal weight labels (Figs. 3, 5, 8–11) are dense and should be spot-checked before the merge scores on them; (b) words-in is an estimate, not a count — no text layer existed; (c) the paper is experimental, not theorem-based, so "exact" anchors mark claims the paper derives or demonstrates by construction, "computationally_verified" marks the simulation findings; (d) no killed anchors — the paper refutes no prior claim outright (it positions against three alternatives). Blindness held: no other paper, tradition, or sky was consulted.

## 2026-10-07 — Coordinator: merge + adjudication + illustration complete

- Merge (merge_atlas4.py): 107 occurrences -> 105 nodes (1 subject, 104 standalone), 101 within-sky edges, 0 flagged contradictions.
- Candidates: 65 mechanical (token-overlap) + coordinator semantic review of all 105 node labels.
- Adjudication (cross_sky_links.json): 11 records — 4 split_link (S1 resolved, S2 resolved, 2 unseeded bridge<->statistical), 7 rejected with reasons. 0 merges, 0 contradictions, 0 false merges. Direct sky<->sky: 0.
- Illustration (build_html4.py): 5 sky views + atlas4_cross.html money view (4 gold edges), JS validated; atlas4_crossview.png static render.
- Deliverables: ATLAS4_REPORT.md, grading_packet.md/json, manifest.json. Pilot/atlas2/atlas3 dirs untouched (read-only).

## 2026-10-07: braided grading (user indisposed; Muse graded, user to review later)
User handed the grading to Muse ("braid this one"), will look back later.
Method: each triple checked against its extraction concept+anchor
(kind/status/note); each adjudication assessed on its stated reason
against the node labels. Strict.

Triples: 14/15 PASS. T1,T2,T3 (symbolic) pass; T4,T5 pass; T7,T8,T9
(statistical) pass; T10,T11,T12 (neuro) pass; T13,T14,T15 (bridge) pass.
T6 FAILS (minor): packet labels it (claim, exact); the extraction
anchor c5 is (claim, computationally_verified) — the concept bundles
the exact theoretical contribution with the simulation-demonstrated
empirical one; weakest-link status is computationally_verified. A
packet-labeling slip by the coordinator, not an extraction fabrication.

Adjudications: 11/11 PASS. A1 (S2 method-application) sound; the
beyond-chunk caveat is honestly recorded. A2 (S1 biological-precedent)
sound; the 1959/1962 vocabulary gap recorded. A3 (shares-concept, VC
dimension) passes with annotation: the paired bridge node is c14 while
the Baum&Haussler citation lives in c2 — node-choice imprecision that
does not change the verdict (the cross-paper VC link is genuine).
A4 (shared-dataset) sound and honestly split. A5-A11 rejections all
sound: citation-is-not-referent (A5), analogy-is-not-referent (A6),
spurious/generic token overlap (A7, A11), and the three symbolic
zero-candidate disjointness calls (A8-A10) — the starkest, correctly
not inflated.

Overall: 25/26. The single fail is cosmetic and does not touch any
adjudication or the verdict. Ledger item 4 NOT resolved here: the
narrow/wide verdict remains the user's at his review.
