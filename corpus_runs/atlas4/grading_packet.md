# Atlas-4 grading packet

The user's narrow/wide verdict on this run resolves ledger item 4.

## Sampled triples (concept / paper-quote / status)

### T1 [symbolic] (definition, heuristic)
**Concept:** declarative versus imperative instruction -- machines instructed mainly by imperative sequences, humans mainly by declarative situation descriptions with a few imperatives; the listed advantages of ea

**Paper quote/note:** Enumerated contrast: machines instructed by sequences of imperatives vs humans instructed by declaratives plus a few imperatives; advantages of each listed (imperatives laid out and fast; declaratives leverage prior knowledge, have logical consequences, are order-independent and state-independent).

### T2 [symbolic] (method, exact)
**Concept:** the 17-premise airport formalization -- at, walkable, drivable, can(go), did(go), canachult, prog, want, do; premises (1)-(17) and the deduction culminating in do(go(desk, car, walking))

**Paper quote/note:** Full worked formalization of the desk-to-airport problem: 17 premises with predicates at, walkable, drivable, can(go), did(go), canachult, prog, do; the paper exhibits the 8-step deduction ending in do(go(desk, car, walking)) as the derived action. Deductive derivation from premises exact as present

### T3 [symbolic] (claim, heuristic)
**Concept:** capable of being told as precondition of learning -- in order for a program to be capable of learning something it must first be capable of being told it

**Paper quote/note:** Stated doctrine: to be capable of learning something a program must first be capable of being told it; early versions concentrate entirely on being told improvements with no more internal knowledge than instructing a human requires.

### T4 [connectionist] (method, computationally_verified)
**Concept:** the momentum term Delta w_ji(n+1) = eta(delta_pj o_pi) + alpha Delta w_ji(n) (16), alpha about 0.9 in most simulations; momentum filters out high-frequency variations of the error surface (long ravine

**Paper quote/note:** Introduced as equation 16; ravine/filtering rationale is the authors' argument; the alpha approx 0.9 practice and the alpha=0 comparison are reported from their simulations.

### T5 [connectionist] (result, computationally_verified)
**Concept:** XOR time-to-solution scaling (Yves Chauvin): P = 280 - 33log2 H presentations (eta = 0.25, 0.01/pattern criterion), from about 245 at 2 hidden units to about 120 at 32; time to solution reduced linear

**Paper quote/note:** Yves Chauvin's study reported in the text: P = 280 - 33log2 H (eta=0.25, 0.01/pattern criterion), 245 presentations at 2 hidden units down to 120 at 32; learning-rate effect ~450 at eta=0.1 to ~68 at eta=0.75 (8 hidden units).

### T6 [connectionist] (claim, exact)
**Concept:** the chapter's two contributions: the main theoretical contribution is an efficient way of computing the derivatives; the main empirical contribution is that the apparently fatal problem of local minim

**Paper quote/note:** Theoretical contribution: the efficient derivative computation derived in equations 7-16.

### T7 [statistical] (definition, exact)
**Concept:** support vectors: training vectors for which yi(w.xi+b) = 1 (Kuhn-Tucker equality cases); the only training data that determine the margin and enter the solution expansion w0 = sum alpha_i^0 yi xi

**Paper quote/note:** Defined via the Kuhn-Tucker equality alpha_i[yi(xi.w0+b0)-1] = 0 in Appendix A.1; only terms with alpha_i > 0 enter w0 = sum alpha_i^0 yi xi.

### T8 [statistical] (definition, exact)
**Concept:** support-vector network: a new learning machine for two-group classification problems; input vectors are non-linearly mapped to a very high-dimension feature space, in which a linear decision surface w

**Paper quote/note:** New machine defined in the Abstract and section 1; its algorithm is derived analytically in sections 2-4, extending the separable-only prior result of Boser, Guyon & Vapnik (1992) to non-separable training data.

### T9 [statistical] (claim, heuristic)
**Concept:** structural risk minimization (Occam-Razor principle): resolve the error/capacity trade-off by minimizing the sum of the two bound terms; the Occam-Razor case keeps the training error at zero and minim

**Paper quote/note:** Structural risk minimization is proposed as the resolution of the trade-off; the reading of optimal-margin minimization as an Occam-Razor execution is interpretive discussion in section 5.3.

### T10 [neuro] (conjecture, heuristic)
**Concept:** two suggested functions of the excitatory-inhibitory arrangements: (1) they determine the form, size and orientation of the most effective stimuli; (2) they may play a part in perception of movement

**Paper quote/note:** Discussion p. 589: 'two further possible functions' - explicitly tentative, no test offered.

### T11 [neuro] (result, exact)
**Concept:** synergism between opposite-type areas with moving stimuli: regions antagonistic when tested with stationary spots (Fig. 10A) can act synergistically when a spot moves from an 'off' area into an 'on' a

**Paper quote/note:** Fig. 10A (stationary: inhibitory centre of left eye + excitatory flank of right eye cancel) vs Fig. 10B (moving spot from 'off' to 'on' area gives greatly increased response).

### T12 [neuro] (definition, exact)
**Concept:** excitatory and inhibitory ('on' and 'off') regions within a cortical receptive field, defined by effects seen during the light stimulus (arbitrary terms; 'inhibition' used descriptively)

**Paper quote/note:** Defined at pp. 576-577: excitatory if illumination increases firing frequency; inhibitory if light suppresses maintained activity and/or is followed by an 'off' discharge. Terms called arbitrary and descriptive.

### T13 [bridge] (method, exact)
**Concept:** data base: 9298 segmented numerals digitized from handwritten zip codes on U.S. mail passing through the Buffalo, NY post office; 7291 for training, 2007 for testing generalization; both sets contain 

**Paper quote/note:** Data facts reported: 9298 segmented numerals from Buffalo, NY post office mail; 7291 training / 2007 test; ambiguous and misclassified examples in both sets.

### T14 [bridge] (claim, heuristic)
**Concept:** scaling properties were far better than one would expect just from extrapolating results of backpropagation on smaller, artificial problems; learning time was relatively short given the training set s

**Paper quote/note:** Authors' qualitative reading of their results versus extrapolation from small artificial problems; no formal scaling analysis given.

### T15 [bridge] (result, computationally_verified)
**Concept:** larger variant (footnote): a network with 100,000 connections and 2600 free parameters achieved 9% rejection for 1% error rate — about 30% better than the best of the hand-coded-kernel networks

**Paper quote/note:** Footnote result: 100,000-connection / 2600-free-parameter variant achieved 9% rejection for 1% error, ~30% better than hand-coded-kernel networks.

## All adjudications

### A1 — split_link (S2, resolved)
**A:** [bridge] `bri:constrained-backpropagation-the-first-two-layers`

**B:** [connectionist] `con:the-generalized-delta-rule-a-learning-procedure-`

**Relation:** method-application

**Reason:** Same method (backpropagation/generalized delta rule), different epistemic roles: RHW derives the learning procedure (exact); LeCun applies it as the training instrument for the constrained architecture (heuristic). Link, not merge (Atlas-2 D3). The bridge paper's weight-sharing attribution to RHW-1986 (T-C problem) has no target node in the connectionist extraction (section beyond the 8.6k-word chunk) — recorded, not adjudicated.

### A2 — split_link (S1, resolved)
**A:** [bridge] `bri:synthesized-kernels-some-can-be-interpreted-as-f`

**B:** [neuro] `neu:excitatory-and-inhibitory-on-and-off-regions-wit`

**Relation:** biological-precedent

**Reason:** The bridge paper explicitly claims its learned kernels resemble H&W biological detectors ('off-center/on-surround type feature detectors'); the neuro extraction (H&W 1959) contains the on/off-region findings at exact status. Corroborated by neu:orientation-specificity (spatial-derivative-estimator resemblance). Vocabulary gap recorded: the 1959 paper predates 'simple/complex cell' language the bridge's 1962 citation uses — the findings match, the terms don't. Link, not merge: artificial kernels vs cortical cells.

### A3 — split_link
**A:** [bridge] `bri:constrained-backpropagation-the-first-two-layers`

**B:** [statistical] `sta:vc-dimension-test-error-bound-pr-test-error-freq`

**Relation:** shares-concept

**Reason:** Same referent (Vapnik-Chervonenkis dimension), different roles: LeCun invokes reduced VC-dimensionality (via Baum & Haussler 1989) as a design consideration for free-parameter reduction; C&V derives the VC test-error bound as core theory. Unseeded — off the seeded bridges.

### A4 — split_link
**A:** [bridge] `bri:data-base-9298-segmented-numerals-digitized-from`

**B:** [statistical] `sta:us-postal-service-digit-database-polynomials-deg`

**Relation:** shared-dataset

**Reason:** Same underlying USPS handwritten-digit pool (both AT&T-era), different experimental splits: LeCun 7291 train/2007 test (of 9298); C&V 7300 train/2000 test. Same empirical object, different experiments — link, not merge. Unseeded.

### A5 — rejected
**Pair:** connectionist ↔ statistical

**Reason:** C&V's prior-art positioning cites the perceptron and RHW-1986, but citation is not a shared referent: no perceptron node exists in the RHW extraction, and C&V's node is historiography while RHW's XOR nodes are learnability results. No node-level pair to adjudicate.

### A6 — rejected
**Pair:** connectionist ↔ neuro

**Reason:** 5 mechanical candidates, all generic token overlap ('hidden units' vs cortical units, 'activation', 'more'). No shared mathematical or empirical object; layered-network/hierarchical-convergence resemblance is analogy, not a shared referent.

### A7 — rejected
**Pair:** statistical ↔ neuro

**Reason:** 1 mechanical candidate, spurious token overlap. No shared object.

### A8 — rejected
**Pair:** symbolic ↔ connectionist

**Reason:** 0 mechanical candidates; semantic review confirms disjoint vocabularies (advice taker / predicate calculus / deduction vs network learning). No shared referent.

### A9 — rejected
**Pair:** symbolic ↔ statistical

**Reason:** 0 mechanical candidates; semantic review confirms disjoint vocabularies. No shared referent.

### A10 — rejected
**Pair:** symbolic ↔ neuro

**Reason:** 0 mechanical candidates; semantic review confirms disjoint vocabularies. No shared referent.

### A11 — rejected
**Pair:** bridge ↔ connectionist

**Reason:** 37 remaining mechanical candidates beyond the S2 method link, all generic token overlap ('hidden', 'units', 'error', 'network'). No additional shared referent found in semantic review.

