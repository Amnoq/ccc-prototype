# Atlas-2 grading packet

For the user: grade a sample the way the pilot was graded (10/13 strict). Every triple below is concept / paper-quote / status. Then all seeded resolutions, all splits, all flagged contradictions (none).

## Sampled triples (22)

### [sierra] closed periodic orbits with turning point B=(x_m(E), l_p) and energy-preserving momentum bounce at C
- status: `exact` · kind: result · file: sierra_s2.json / c2
- paper quote: Derived from Hamilton equations (4), explicit solution (5); trajectory A->B->C closes via momentum bounce l_p^2/p_0 -> p_0 at C, preserving energy; period T_E=cosh^-1(E/2h).

### [sierra] theta arising from an electric field at the boundary x=l (expected, not derived)
- status: `conjectural` · kind: conjecture · file: sierra_s5.json / c5
- paper quote: Stated only as an expectation ('We expect the parameter theta to arise from an electric field applied at the boundary x=l'); no derivation given.

### [sierra] normal-ordered quantum Hamiltonian H-hat = x^{1/2}(p-hat + l_p^2/p-hat)x^{1/2}
- status: `exact` · kind: method · file: sierra_s3.json / c1
- paper quote: Normal ordering chosen by the paper (8); 1/p-hat defined as the 1D Green function with matrix elements -i/hbar theta(y-x) (9); action on psi is the integro-differential operator (10).

### [ccm] Convergence of the suitably normalized regularized determinants det_reg(D_log^{(lambda,N)} - z) towards the Ri
- status: `conjectural` · kind: conjecture · file: ccm_s1.json / c10
- paper quote: Abstract and Section 1; the analytic justification is the program of Section 7 (prolate-wave approximation).

### [ccm] The Weil class W(R^*_+) of complex valued functions with first-kind discontinuities at most and the decay esti
- status: `exact` · kind: definition · file: ccm_s3.json / c1
- paper quote: Defined at the start of Section 3; functions admit a Mellin transform (3.1).

### [ccm] Proposition 5.9: the Fourier transform of the extended minimal eigenvector is the entire function xi-hat(z) = 
- status: `exact` · kind: result · file: ccm_s8.json / c2
- paper quote: Proposition 5.9: proved by the change of variables x = log(lambda u); the zeros of sin(sL/2) at 2 pi Z / L cancel the poles at 2 pi j / L when xi_j != 0.

### [lamzouri] comparison with Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh Theorem 3(ii)(iii): same C_1 average bound unde
- status: `conjectural` · kind: claim · file: lamzouri_s1.json / c7
- paper quote: Compares with [4] Theorem 3 under a narrow-box hypothesis b/log T: same C_1 average bound as b→0, while their conditional simple-or-critical bound (2+C_0)/3 = 0.89083… slightly exceeds the unconditional 0.88762…; the cited results are not proved here.

### [lamzouri] proof of (2.4): the elementary bounds a²+4 ≥ 4a on the first range, a²+1 ≥ 2a on the second, and the trivial t
- status: `exact` · kind: method · file: lamzouri_s3.json / c1
- paper quote: Completes (2.4): combines (2.22) a²+4 ≥ 4a on the first range, (2.23) a²+1 ≥ 2a on the second, and the trivial (2.24) with (2.16) and (2.21).

### [lamzouri] replacing the whole finite-dimensional matrix framework by a single Hilbert space inequality, then applying Mo
- status: `exact` · kind: method · file: lamzouri_s1.json / c9
- paper quote: Announced in the abstract and §1: the matrix machinery is replaced by a single Hilbert space inequality, after which Montgomery's pair correlation applies directly; carried out in §2.

### [mty2022] ν(t)=1/(55.241(log t)^{2/3}(log log t)^{1/3}); Z(β,t)=(1−β)B^{2/3}(log t)^{2/3}(log log t)^{1/3} (5.1); M=inf_
- status: `exact` · kind: definition · file: mty2022_s5.json / c2
- paper quote: Definitions (5.1)–(5.2); target constant M1=0.048976 with B^{2/3}/M1<55.241.

### [mty2022] final contradiction: M≥(0.17949−0.755/log T0)/(3.25351+Y(t))≥0.04897601>M1, where Y(t) is decreasing for t≥T0 
- status: `exact` · kind: result · file: mty2022_s5.json / c5
- paper quote: Final contradiction (5.15); Y(t) decreasing for t≥T0 checked by Mathematica, Y(T0)<0.4110503; the monotonicity argument repairs Ford's (8.9).

### [mty2022] seven iterations give R0=5.5586904517, establishing Theorem 1.3 (R0=5.558691); iteration values in Table 3
- status: `computationally_verified` · kind: result · file: mty2022_s8.json / c6
- paper quote: §9: seven iterations (Table 3) give R0=5.5586904517; h^{(4)} variant gives 5.5608403, so the swap gains ≈2.15·10^{−3}.

### [mt2015] update Faber-Kadiri psi/theta bounds and Ramare's sum Lambda(n)/n bound with new R0
- status: `heuristic` · kind: question · file: mt2015_s7.json / c5
- paper quote: Suggested updates only; Faber-Kadiri [3] building on Schoenfeld [17]; Ramare [12, Thm 1.1] uses Kadiri's R0.

### [mt2015] Kondrat'ev's degree-8 polynomial k_8(phi) coefficients (Table 2)
- status: `conjectural` · kind: result · file: mt2015_s1.json / c7
- paper quote: Normalized a_0=1: a_1=1.733792817542616, a_2=1.110484293773627, a_3=0.4895739485699287, a_4=0.1180328991868943, a_7=0.009253861629263798, a_8=0.004429241403972788, A=3.465567070455195; cited [6].

### [mt2015] C_4(eta) with C_41(k), C_42(k) and integral estimates
- status: `exact` · kind: result · file: mt2015_s4.json / c7
- paper quote: U_0(t) piecewise bound (4.2); optimal c=0.462935...; range split with eps=1e-3 around b.

### [bty2026] Theorem 1: zeta(sigma+it) != 0 in sigma > 1 - 1/(4.896 log t) for t >= 3
- status: `exact` · kind: result · file: bty2026_s1.json / c1
- paper quote: Theorem 1 proved via Lemma 1 plus the explicit Littlewood region (3); the constant 4.896 improves the previous best 5.559 from [11].

### [bty2026] whether iterating Lemma 15 with an improved lower bound for eta (footnote 4) yields a further-improved constan
- status: `heuristic` · kind: question · file: bty2026_s7.json / c4
- paper quote: Footnote 4: the authors note a possible minor improvement from iterating with an improved eta lower bound, and explicitly decline to pursue it as negligible.

### [bty2026] contradiction hypothesis (7): a simple zero rho0 = beta0 + it with A <= (1-beta0) log t < A + epsilon lying ju
- status: `killed` · kind: claim · file: bty2026_s2.json / c5
- paper quote: Assumed for contradiction in Section 2; refuted by the iteration lemma (Lemma 15, Section 5).

### [deninger] the colimit construction and the dynamical system X_0
- status: `exact` · kind: method · file: deninger_s37.json / c5
- paper quote: X̌_0(C) = colim_N X̲_0(C) inverts the injective F_ν to a Q^{>0}-action; X_0 = (X̌_0(C) × R^{>0})/Q^{>0} with diagonal action; φ^t[P,u] = [P,e^t u]; the 1-codimensional 'foliation' F has leaves the images of X̌_0(C) × {u}, everywhere transversal to the flow; the limit over Frobeni

### [deninger] Theorem 9.2: density of the fibres, proved by constructing characters χ approximating P
- status: `exact` · kind: result · file: deninger_s15.json / c1
- paper quote: Theorem 9.2 asserts characters χ ∈ Hom_{E_f}(K^×, C^×) satisfying the approximation estimate (80) |χ(r) − P(r)| < ε for all r ∈ T; the proof ends with χ constructed to meet (80).

### [deninger] Theorem 1.9: Verschiebung preserves rationality for Fatou domains
- status: `exact` · kind: result · file: deninger_s3.json / c6
- paper quote: Thm 1.9: for Fatou A, V_N(W(A))∩W_rat(A)=V_N(W_rat(A)); rationality detected by finite continued-fraction expansion, commuting with V_N.

### [deninger] Theorem 9.8 (Kucharczyk–Scholze): G acts freely on r^{-1}(Hom_inj(μ(K), C^×))
- status: `exact` · kind: result · file: deninger_s16.json / c7
- paper quote: Theorem 9.8, due to Kucharczyk and Scholze: G acts freely on r^{-1}(Hom_inj(μ(K), C^×)) ⊂ pr^{-1}(η); from P = P^σ, the cyclotomic character gives κ(σ) = 1 and [KS18, Lemma 4.12] with char K_0 = 0.

## All seeded resolutions (13)

### [split_link] classical-hamiltonian-h-cl-x-p-l-p-2-p-on-the-ha  <->  node11i
- foreign: classical Hamiltonian H_cl = x(p + l_p^2/p) on the half line x >= l_x (exact)
- pilot: Node 11i: Sierra spectrum matches Riemann-von Mangoldt to 0.07%
- relation: tests
- reason: Foreign = Sierra's primary classical object H_cl=x(p+l_p^2/p) (exact, proved 2011). Pilot node11i = program's verdicts on its own implementation (spectrum matches RvM 0.07%; tones absent; forced sequence). Merging would collapse the paper's exact claims with the program's 2026 computational verdicts.

### [split_link] normal-ordered-quantum-hamiltonian-h-hat-x-1-2-p  <->  node11i
- foreign: normal-ordered quantum Hamiltonian H-hat = x^{1/2}(p-hat + l_p^2/p-hat)x^{1/2} (exact)
- pilot: Node 11i: Sierra spectrum matches Riemann-von Mangoldt to 0.07%
- relation: tests
- reason: Foreign = Sierra's quantized H-hat with non-local BC (exact). Pilot node11i = verdicts on the program's K-Bessel secular-equation implementation. Same mathematics, different epistemic levels.

### [split_link] theta-pi-4-with-h-2pi-hbar-reproduces-the-averag  <->  node11i
- foreign: theta = pi/4 with h = 2pi hbar reproduces the average position of the Riemann zeros (exact)
- pilot: Node 11i: Sierra spectrum matches Riemann-von Mangoldt to 0.07%
- relation: tests
- reason: Foreign = Sierra's theta=pi/4 Riemann-matching choice (exact). Pilot node11i implemented this choice and measured tones absent. Object vs verdict.

### [split_link] theorem-1-1-the-rank-one-perturbation-d-log-lamb  <->  node11f
- foreign: Theorem 1.1: the rank-one perturbation D_log^{(lambda,N)} = D_log^{(lambda)} - |D_log^{(lambda)} xi><delta_N| is selfadjoint, its regularized determin (exact)
- pilot: 11f — CCM: live candidate; zeros 1–8 recovered from primes alone (independent reimplementation); fragile exact-arithmetic reporter (drop p=2/3 destroy
- relation: reimplements
- reason: Foreign = CCM's Theorem 1.1 (rank-one perturbation D_log^{(lambda,N)}; exact as stated). Pilot node11f = program's INDEPENDENT reimplementation from prime Euler products (first zero recovered to machine precision; controls; fragility). The pilot deliberately re-derived rather than cited — merging would erase that independence.

### [split_link] theorem-1-1-the-rank-one-perturbation-d-log-lamb  <->  ccm
- foreign: Theorem 1.1: the rank-one perturbation D_log^{(lambda,N)} = D_log^{(lambda)} - |D_log^{(lambda)} xi><delta_N| is selfadjoint, its regularized determin (exact)
- pilot: 11f — CCM: live candidate; zeros 1–8 recovered from primes alone (independent reimplementation); fragile exact-arithmetic reporter (drop p=2/3 destroy
- relation: assesses
- reason: Foreign = CCM's primary construction. Pilot 'ccm' = program's verdicts (live candidate; top computational target; 11e audit). Assessment, not duplication.

### [split_link] theorem-1-3-no-zeros-of-it-for-t-2-with-1-1-5-55  <->  node9c
- foreign: Theorem 1.3: no zeros of ζ(σ+it) for |t|≥2 with σ≥1−1/(5.558691 log|t|) (exact)
- pilot: 9c — CLOSED NEGATIVE by theorem: positivity is blind left of Re(s)=1 (geometry owns positivity, analysis owns continuation); 9c as RH proof closed
- relation: assesses
- reason: Foreign = MTY2022's Theorem 1.3 (R0=5.558691; exact). Pilot node9c = program's verdict that trig-polynomial optimization is saturated ('near its intrinsic limit') plus the 9c' density analysis. The theorem vs the verdict on the theorem's optimality.

### [split_link] table-5-c-k-and-normalized-a-k-coefficients-for-  <->  node9c
- foreign: Table 5: c_k and normalized a_k coefficients for F_16(phi) (computationally_verified)
- pilot: 9c — CLOSED NEGATIVE by theorem: positivity is blind left of Re(s)=1 (geometry owns positivity, analysis owns continuation); 9c as RH proof closed
- relation: analyzes
- reason: Foreign = F16 coefficient table (exact data, c_k and normalized a_k). Pilot node9c' = program's computational analysis OF that table (Fejer-Riesz factors fully dense 17/17; saturation is numerical not geometric). Data vs analysis of the data.

### [missed_correct] theorem-1-1-the-four-unconditional-bounds-with-c  <->  None
- foreign: Theorem 1.1: the four unconditional bounds with C_0 = 0.67250…, C_1 = (C_0+1)/2 = 0.83625…, C_2 = (1+2√2+2C_0)/(3+2√2) = 0.88762… (exact)
- pilot: —
- relation: None
- reason: Foreign = Lamzouri's Theorem 1.1 (67.25% simple-and-on-line; 88.76%; 83.62%; exact). The pilot atlas has NO corresponding subject (only a passing mention inside 'gue'). Correctly unresolved: there is nothing to resolve TO, and no false merge was manufactured. This is the merge refusing to invent a resolution — a pass, not a failure.

### [resolved] theorem-6-1-periodic-orbits-form-packets-e-x-0-o  <->  node11m_deninger::c2
- foreign: Theorem 6.1: periodic orbits form packets Γ^E_{x_0} of length log Nx_0 (exact)
- pilot: Theorem 6.1: periodic orbits correspond to closed points of X0; 
- relation: same-theorem
- reason: Foreign = Deninger paper (a) Theorem 6.1 (periodic points decompose as packets Gamma^E_{x_0}, orbit length log N x_0; exact). Pilot c2 = Theorem 6.1 (periodic orbits correspond to closed points of X0; exact). Same theorem, same epistemic level -- a genuine cross-corpus resolution.

### [resolved] the-dynamical-transversal-index-formula-9  <->  node11m_deninger::c4
- foreign: the dynamical transversal index formula (9) (exact)
- pilot: transversal index (Lefschetz) formula in the foliation setting: 
- relation: same-formula
- reason: Foreign = Deninger paper (b) eq. (9), the dynamical transversal index formula (exact). Pilot c4's own note cites 'eq. (9) of arXiv:2301.11643' (proved in the foliation setting; exact). Same equation of the same paper, same level -- an earned resolution with textual provenance on both sides.

### [split_link] theorem-4-2-closed-points-correspond-to-packets-  <->  node11m_deninger::c2
- foreign: Theorem 4.2: closed points correspond to packets of periodic orbits (conjectural)
- pilot: Theorem 6.1: periodic orbits correspond to closed points of X0; 
- relation: restates
- reason: Foreign = Deninger paper (b) Theorem 4.2 in expository form, marked conjectural by the extractor (proved in the companion work [Den22a]). Pilot c2 = the exact theorem. Same referent, different epistemic level as extracted -- linked, not merged.

### [split_link] periodic-orbits-correspond-to-closed-points-x-0-  <->  node11m_deninger::c2
- foreign: periodic orbits γ correspond to closed points x_0 with length l(γ) = log N(x_0) (conjectural)
- pilot: Theorem 6.1: periodic orbits correspond to closed points of X0; 
- relation: heuristic-framing
- reason: Foreign = the primes/knots/orbits analogy in Deninger paper (a)'s introduction (conjectural framing claim). Pilot c2 = the proved correspondence theorem. Framing vs theorem -- linked, not merged.

### [split_link] sheafified-rational-witt-vectors-w-rat-x-with-co  <->  deninger
- foreign: sheafified rational Witt vectors W_rat(X) with commuting Frobenius endomorphisms (exact)
- pilot: 12c/12d: Deninger-type foliated dynamics (L4) survives as formulated conjecture; 12d Heisenberg nilmanifold probe negative (arithmetic flavor ≠ zero s
- relation: builds-on
- reason: Foreign = Deninger paper (a)'s exact W_rat(X) construction with commuting Frobenius endomorphisms. Pilot 'deninger' = the program's own Deninger-type foliated dynamics (L4) verdicts -- 'survives as formulated conjecture'. Exact primary construction vs the program's conjectural reformulation -- linked, not merged.

## Flagged contradictions

None. (flagged list is empty in atlas2_graph.json)

## Blindness note
Drafters never saw the pilot atlas. Seeded pairs were adjudicated by the coordinator after mechanical candidate generation; no seeded pair was granted a merge it did not earn (see reason fields).
