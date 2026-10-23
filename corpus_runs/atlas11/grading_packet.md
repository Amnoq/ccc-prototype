# Atlas-11 grading packet

Machine grading per the 2026-10-08 delegation (router withdrew from the prediction loop; the machine grades and archives; the router's word remains final and overrides on request). Router override available on request.

## Sampled triples (concept / paper-note / status)

### T1 [analytics] (method, exact)
**Concept:** adeles for dynamicists (invertible Hecke shift)
**Paper note:** Intuitive picture: force the multi-valued Hecke operator T_p invertible via the sequence space X-tilde_p; the shift S is the right action of a diagonal matrix in SL2(Q_p). Doing this at all primes yields X-tilde.
**Status:** exact (facet a2_michelvenkatesh_p3/c3, original)

### T2 [analytics] (result, exact)
**Concept:** degenerate term bound lemma (5.2.9)
**Paper note:** Lemma (5.2.9): degenerate term << Q^{eps} |z|^{-4} ||Ad(u)||^{-gamma} (5.18), gamma>1/2. H_{s,t} expanded as sum of H^{+-}_{s,t} with local factors (5.19); J-terms analogous with intertwining operators.
**Status:** exact (facet a2_michelvenkatesh_p14/c9, original)

### T3 [analytics] (method, exact)
**Concept:** J-term local bounds (5.24), (5.25)
**Paper note:** J^{--}_v bounds: ||J^{--}_v|| << ||Ad(u_v)||^{-gamma} (5.24), gamma = 1-theta > 1/2, for v in S via Lemma 3.2.8; <= 1 for v in T via Lemma 3.2.7. Derivative bounds (5.25) via Cauchy estimates off the unitary axis using Proposition 3.2.4 and the section 4.1.8 bounds for M-bar_v.
**Status:** exact (facet a2_michelvenkatesh_p15/c1, original)

### T4 [analytics] (result, conjectural)
**Concept:** Lower bounds Mk(T) ≫_k T (log T)^{k²} (Ramachandra; Heath-Brown; Ramachandra under RH)
**Paper note:** Cited: Ramachandra [13] (2k integer), Heath-Brown [6] (rational k), Ramachandra [12] under RH (all real k); also [1], [20].
**Status:** conjectural (facet a1_soundararajan_p1/c4, original)

### T5 [analytics] (method, exact)
**Concept:** Proposition: under RH, log|ζ(1/2+it)| bounded by a prime Dirichlet polynomial; zeros near 1/2+it are benign (λ0=0.4912…)
**Paper note:** Proved in §2 via Hadamard factorization and Stirling; λ0≈0.4912 is the unique positive root of e^{-λ0}=λ0+λ0²/2; choice σ0=1/2+λ/log x makes the F(s0) term negative so it is dropped.
**Status:** exact (facet a1_soundararajan_p1/c10, original)

### T6 [geometry] (question, heuristic)
**Concept:** 7.1: integral coefficients? effective bounds on M(g,i) and N? tightness of O(g^2 i^2)?
**Paper note:** Section 7.1 asks: does Theorem 1.2 hold with integral coefficients? What is an effective bound on M(g,i) (where dim H_i(M_{g,n}) becomes polynomial-times-exponential)? Is the O(g^2 i^2) generation bound tight? What is an effective bound on the N of Theorem 1.4?
**Status:** heuristic (facet g2_tosteson_p3/c6, original)

### T7 [geometry] (method, exact)
**Concept:** generalized Birkhoff decomposition for time evolution
**Paper note:** Method from [14,16]: time evolution S(t) from generalized Birkhoff decomposition exp diag(D1,D2).Y(t) = S(t).S(0)^{-1} as in (7.5).
**Status:** exact (facet g1_mulase_p6/c4, original)

### T8 [geometry] (method, exact)
**Concept:** Lemma 5.2 case (3): cross ratio relation reduces adjacent trivalent vertices to case (2)
**Paper note:** Lemma 5.2 case (3): for adjacent trivalent vertices v1,v2 each with an external edge, the cross ratio relation gives [M_H]=[M_H'] where H' has a vertex adjacent to two external edges, reducing to case (2).
**Status:** exact (facet g2_tosteson_p3/c5, original)

### T9 [geometry] (claim, conjectural)
**Concept:** Proposition 4.3: P_{Conf_n(C-p)}(q,t) <=_pure (2gqt+q^2t^2)^n (Getzler, cited)
**Paper note:** Proposition 4.3: P_{Conf_n(C-p)}(q,t) <=_pure (2g q t + q^2 t^2)^n, from Getzler's spectral sequence for compactly supported cohomology of configuration space [10]; pure classes on the E_1 page are (H^._c(C-p)^{tensor n}) in the stated bidegrees. Cited, not proved here.
**Status:** conjectural (facet g2_tosteson_p2/c10, original)

### T10 [geometry] (definition, exact)
**Concept:** Serre duality involution on Higgs moduli
**Paper note:** Involution (2.4): (E,phi) -> (E* x KC, -phi*) in HC(n,-d+2n(g-1)); induces Serre duality on moduli.
**Status:** exact (facet g1_mulase_p2/c9, original)

### T11 [bridge] (result, exact)
**Concept:** abelian class field theory isomorphism
**Paper note:** Abelian class field theory (1.5): Gal(F^ab/F) ~= group of connected components of F^x\A_F^x. Stated as classical theorem; rigidifying property deferred to Frobenius subsection.
**Status:** exact (facet b1_frenkel_p2/c7, reframed)

### T12 [bridge] (result, exact)
**Concept:** coinvariants as D-modules on Bun_G via localization
**Paper note:** For G((t)), G^out, G[[t]]: Delta(V) on Bun_G is the CFT sheaf of coinvariants, fiber V/g^P_out . V; line bundle L (non-abelian theta) from universal central extension; D'_k exists for arbitrary complex k [15,98,99].
**Status:** exact (facet b1_frenkel_p15/c4, original)

### T13 [bridge] (result, exact)
**Concept:** Drinfeld-Lafforgue theorem for function fields
**Paper note:** Function-field Langlands is a theorem: Drinfeld proved GL_2 case [39,40], Lafforgue GL_n [41]; completions all non-archimedean so theory more uniform.
**Status:** exact (facet b1_frenkel_p4/c10, reframed)

### T14 [bridge] (result, exact)
**Concept:** Hecke eigensheaf as system of differential equations
**Paper note:** Delta_{chi~} = D'_{-h^vee}/Ker chi~ . D'_{-h^vee} represents D_i f = chi~(D_i) f (9.17); holonomic (dim Bun_G = N); singular support = global nilpotent cone p^{-1}(0); very stable bundles (Drinfeld [114]); monodromies around singular locus.
**Status:** exact (facet b1_frenkel_p21/c3, original)

### T15 [bridge] (definition, exact)
**Concept:** local systems as sheaves, pi_1 representations, flat connections
**Paper note:** Local system on complex curve: locally constant sheaf <-> homomorphism pi_1(X,x_0) -> GL_n(C) <-> vector bundle with flat connection (Leibniz (3.1), flatness (3.2)); on curves one operator nabla = d/dz + A(z), automatically flat.
**Status:** exact (facet b1_frenkel_p6/c6, original)

## All adjudications

### A1 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-via-c-chi-r`
**B:** [analytics] `ana:corollary-power-bound-for-cuspidal-count-by-cond`
**Relation:** shared-concept
**Reason:** Both nodes concern cuspidal automorphic representations of GL_n with central character: Frenkel defines C_{chi,rho}(GL_2(Q)\GL_2(A)) (smooth, K-finite, cuspidal, multiplicity one); Michel-Venkatesh prove a power bound on the count of such representations with conductor <= X. Definition vs counting theorem - distinct concepts, same referent.

### A2 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-for-functio`
**B:** [analytics] `ana:corollary-power-bound-for-cuspidal-count-by-cond`
**Relation:** shared-concept
**Reason:** Frenkel's function-field definition C_chi(GL_n(F)\GL_n(A)) (locally constant, central character of finite order, cuspidality, multiplicity one) and Michel-Venkatesh's power bound on cuspidal representations of GL_n(F) with fixed central character concern the same object class (function-field vs number-field instances of cuspidal automorphic representations).

### A3 — split_link (S1, resolved)
**A:** [bridge] `bri:categories-aut-e-and-eisenstein-series`
**B:** [analytics] `ana:fourier-coefficients-of-eisenstein-series`
**Relation:** geometric-analog
**Reason:** Frenkel's node is the geometric Eisenstein series (reducible local system E -> complexes on Bun_G, [61]); Michel-Venkatesh's node treats classical Eisenstein series Fourier coefficients (constant term, Whittaker factorization, Lambda(pi,Ad,1) norm relation). The geometric Eisenstein series is the categorification of the classical one - genuine kinship, distinct objects.

### A4 — split_link (S1, resolved)
**A:** [bridge] `bri:restricted-tensor-product-decomposition-of-pi`
**B:** [analytics] `ana:smooth-vectors-v-infty`
**Relation:** shared-concept
**Reason:** Both concern the local-global tensor structure of automorphic representations: Frenkel gives pi = tensor'_p pi_p tensor pi_infty with spherical vectors at unramified places; Michel-Venkatesh define V^infty whose global version is the tensor product of the local smooth subspaces. Decomposition theorem vs smooth-subspace definition.

### A5 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-via-c-chi-r`
**B:** [analytics] `ana:standard-automorphic-representations-and-planche`
**Relation:** shared-concept
**Reason:** Frenkel defines cuspidal automorphic representations via C_{chi,rho}; Michel-Venkatesh define 'standard' automorphic representations (abstractly unitarizable, exactly those needed for the unitary/Plancherel decomposition). Distinct representation classes within the same automorphic family.

### A6 — split_link (S1, resolved)
**A:** [bridge] `bri:categories-aut-e-and-eisenstein-series`
**B:** [analytics] `ana:singular-eisenstein-series-eis`
**Relation:** geometric-analog
**Reason:** Geometric Eisenstein series for reducible E (Frenkel, complexes not perverse) vs the classical singular Eisenstein series Eis* (Michel-Venkatesh, residue construction at chi_+=chi_-=1). Geometric analog vs classical object.

### A7 — split_link (S1, resolved)
**A:** [bridge] `bri:categories-aut-e-and-eisenstein-series`
**B:** [analytics] `ana:identity-4-36-for-f-q-at-full-level`
**Relation:** geometric-analog
**Reason:** Frenkel's geometric Eisenstein series (reducible E -> Aut_E categories) vs Michel-Venkatesh's identity (4.36), a spectral expansion over Maass forms and classical Eisenstein series. Shared Eisenstein-series content, geometric vs classical.

### A8 — split_link (S1, resolved)
**A:** [bridge] `bri:galois-representation-from-etale-cohomology-of-e`
**B:** [analytics] `ana:lower-bound-l-e-d-1-2-k-k-x-log-x-k-k-1-2-for-qu`
**Relation:** shared-concept
**Reason:** Both concern an elliptic curve E over Q: Frenkel defines its l-adic Galois representation sigma_{E,l} from H^1_et; Soundararajan bounds moments of its quadratic-twist L-values L(E tensor chi_d,1/2)^k. Galois-side vs L-function-side of the same arithmetic object (linked by modularity).

### A9 — split_link (S1, resolved)
**A:** [bridge] `bri:galois-representation-from-etale-cohomology-of-e`
**B:** [analytics] `ana:upper-bound-x-log-x-k-k-1-2-for-the-elliptic-cur`
**Relation:** shared-concept
**Reason:** Same as #19 with the upper bound: sigma_{E,l} (the Galois representation of E) vs the upper bound << X(log X)^{k(k-1)/2+eps} for the elliptic-curve twist family. Same object E, Galois vs analytic-moment aspects.

### A10 — split_link (S1, resolved)
**A:** [bridge] `bri:hecke-eigenvalues-as-fourier-coefficients-a-p`
**B:** [analytics] `ana:fourier-coefficient-a-phi-lambda-omega-along-a-c`
**Relation:** shared-concept
**Reason:** Frenkel: h_{1,p} = a_p, Hecke eigenvalues as classical Fourier coefficients of the modular cusp form; Michel-Venkatesh: a(phi_lambda,omega), Fourier coefficients of a Hecke-Laplace eigenfunction along a closed geodesic (related to central L-values via Waldspurger). Both are Fourier coefficients of automorphic forms, but of different kinds (Hecke eigenvalues vs geodesic periods).

### A11 — split_link (S1, resolved)
**A:** [bridge] `bri:hecke-eigenvalues-as-fourier-coefficients-a-p`
**B:** [analytics] `ana:fourier-coefficients-of-eisenstein-series`
**Relation:** shared-concept
**Reason:** Hecke eigenvalues as Fourier coefficients a_p (Frenkel, classical) vs Fourier coefficients of classical Eisenstein series (Michel-Venkatesh: constant term, Whittaker factorization). Both concern Fourier/Whittaker coefficients of automorphic forms; cuspidal Hecke eigenvalues vs Eisenstein coefficients.

### A12 — split_link (S1, resolved)
**A:** [bridge] `bri:irreducibility-essential-eisenstein-series-and-o`
**B:** [analytics] `ana:fourier-coefficients-of-eisenstein-series`
**Relation:** geometric-analog
**Reason:** Frenkel's claim about geometric Eisenstein series for non-irreducible E (open category problem) vs Michel-Venkatesh's classical Eisenstein-series Fourier coefficients. Geometric analog vs classical object.

### A13 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-via-c-chi-r`
**B:** [analytics] `ana:adelic-quotient-x-g-f-g-a`
**Relation:** shared-concept
**Reason:** Frenkel defines cuspidal automorphic representations as smooth functions on the adelic quotient GL_2(Q)\GL_2(A); Michel-Venkatesh define X = G(F)\G(A) as the base space of the whole paper. Same adelic quotient: the space automorphic forms live on.

### A14 — split_link (S1, resolved)
**A:** [bridge] `bri:function-field-correspondence-cleaner-than-numbe`
**B:** [analytics] `ana:principal-series-i-omega-omega-0`
**Relation:** shared-concept
**Reason:** Frenkel discusses GL_2(A) principal-series/Maass automorphic representations (noting they have no Galois counterpart over number fields); Michel-Venkatesh define the local principal series I(omega,omega_0) unitarily induced from B. Same representation class, discussed vs defined.

### A15 — split_link (S1, resolved)
**A:** [bridge] `bri:function-field-correspondence-cleaner-than-numbe`
**B:** [analytics] `ana:intertwiner-3-10-from-induced-to-whittaker-model`
**Relation:** shared-concept
**Reason:** Frenkel's function-field-vs-number-field note substantively discusses principal-series/Maass automorphic representations; Michel-Venkatesh's explicit intertwiner (3.10) maps the induced (principal series) model to the Whittaker model for unitary principal series. Shared referent: principal series representations.

### A16 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-via-c-chi-r`
**B:** [analytics] `ana:theorem-1-1-subconvexity-for-gl1-and-gl2`
**Relation:** theorem-instantiation
**Reason:** Michel-Venkatesh's Theorem 1.1 (subconvexity L(pi,1/2) << C(pi)^{1/4-delta} for pi on GL1/GL2 with unitary central character) is a theorem about central L-values of exactly the cuspidal automorphic representations Frenkel defines via C_{chi,rho} with central character (1.8). Definition vs theorem about the defined objects.

### A17 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-for-functio`
**B:** [analytics] `ana:theorem-1-1-subconvexity-for-gl1-and-gl2`
**Relation:** theorem-instantiation
**Reason:** Same as #34 with Frenkel's function-field definition C_chi(GL_n(F)\GL_n(A)) (central character of finite order): Theorem 1.1's subconvexity for automorphic representations with unitary central character applies to this object class.

### A18 — split_link
**A:** [bridge] `bri:witten-s-s-duality-to-langlands-duality-scenario`
**B:** [analytics] `ana:adelic-lift-acquires-invariance-hecke-operators-`
**Relation:** shared-concept
**Reason:** Frenkel's S-duality scenario ('t Hooft operators become Hecke operators; eigenbrane becomes Hecke eigensheaf) and Michel-Venkatesh's adelic lift ('Hecke operators are shadows of the adelic actions') are both substantively about Hecke operators. Genuine shared referent, but the bridge endpoint is the QFT/geometric scenario, not the classical-Langlands content - control null.

### A19 — split_link (S1, resolved)
**A:** [bridge] `bri:hecke-eigenvalues-as-fourier-coefficients-a-p`
**B:** [analytics] `ana:adelic-lift-acquires-invariance-hecke-operators-`
**Relation:** shared-concept
**Reason:** Frenkel: classical Hecke operators H_{1,p} on the upper half-plane with eigenvalues a_p; Michel-Venkatesh: Hecke operators as 'shadows' of adelic actions in the ergodic lift. Same Hecke operators, eigenvalue datum vs ergodic-theoretic role.

### A20 — split_link (S1, resolved)
**A:** [bridge] `bri:hecke-correspondences-recover-classical-hecke-op`
**B:** [analytics] `ana:adelic-lift-acquires-invariance-hecke-operators-`
**Relation:** shared-concept
**Reason:** Frenkel: the geometric Hecke correspondence recovers the classical Hecke operators (T_{i,x}(f) = H_{i,x} * f); Michel-Venkatesh: Hecke operators as 'shadows' of the adelic actions. Shared referent: classical Hecke operators.

### A21 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-of-gl-2-a-q`
**B:** [analytics] `ana:plancherel-formula-langlands-theorem-for-l-2-x`
**Relation:** shared-concept
**Reason:** Frenkel defines cuspidal automorphic representations in the discrete spectrum of L^2(GL_2(Q)\GL_2(A_Q)); Michel-Venkatesh recall Langlands' theorem (Eisenstein intertwiner gives an isometry int^oplus I(chi)dchi -> L^2(X)). Both concern the spectral decomposition of automorphic representations on the adelic quotient.

### A22 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-of-gl-2-a-q`
**B:** [analytics] `ana:standard-automorphic-representations-and-planche`
**Relation:** shared-concept
**Reason:** Frenkel's cuspidal automorphic representations of GL_2(A_Q) vs Michel-Venkatesh's 'standard' automorphic representations (the unitarizable ones carrying the Plancherel measure dmu_P). Distinct classes, same automorphic family.

### A23 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-of-gl-2-a-q`
**B:** [analytics] `ana:kim-shahidi-no-complementary-series-with-paramet`
**Relation:** shared-concept
**Reason:** Frenkel defines cuspidal automorphic representations of GL_2(A_Q); Michel-Venkatesh's Kim-Shahidi convention constrains the local constituents of unitary automorphic representations of GL2(A) (no complementary series beyond theta). Property of the local constituents of the defined objects.

### A24 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-via-c-chi-r`
**B:** [analytics] `ana:plancherel-formula-langlands-theorem-for-l-2-x`
**Relation:** shared-concept
**Reason:** Frenkel's C_{chi,rho} cuspidal automorphic representations vs Langlands' Plancherel theorem for L^2(X) (Michel-Venkatesh): the defined objects are the discrete-spectrum constituents of the decomposition the theorem describes.

### A25 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-via-c-chi-r`
**B:** [analytics] `ana:kim-shahidi-no-complementary-series-with-paramet`
**Relation:** shared-concept
**Reason:** Same as #49 with Frenkel's C_{chi,rho} definition: Kim-Shahidi constrains local constituents of unitary automorphic representations of GL2(A).

### A26 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-for-functio`
**B:** [analytics] `ana:plancherel-formula-langlands-theorem-for-l-2-x`
**Relation:** shared-concept
**Reason:** Frenkel's function-field cuspidal automorphic representations C_chi(GL_n(F)\GL_n(A)) vs Langlands' Plancherel theorem for L^2(X): same automorphic-representation content, function-field vs number-field setting.

### A27 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-for-functio`
**B:** [analytics] `ana:standard-automorphic-representations-and-planche`
**Relation:** shared-concept
**Reason:** Frenkel's function-field C_chi definition vs Michel-Venkatesh's 'standard' automorphic representations with Plancherel measure dmu_P: distinct classes of automorphic representations.

### A28 — split_link (S1, resolved)
**A:** [bridge] `bri:cuspidal-automorphic-representations-for-functio`
**B:** [analytics] `ana:kim-shahidi-no-complementary-series-with-paramet`
**Relation:** shared-concept
**Reason:** Same as #49 with Frenkel's function-field definition: Kim-Shahidi constrains local constituents of unitary automorphic representations of GL2(A).

### A29 — split_link (S1, resolved)
**A:** [bridge] `bri:progression-from-functions-to-d-modules-on-bun-n`
**B:** [analytics] `ana:plancherel-formula-langlands-theorem-for-l-2-x`
**Relation:** shared-concept
**Reason:** Frenkel's programmatic claim that automorphic representations become D-modules on Bun_n (functions -> l-adic sheaves -> perverse sheaves -> D-modules) vs Langlands' Plancherel theorem for L^2(X): the geometric upgrade vs the analytic spectral theorem, both about automorphic representations.

### A30 — split_link (S1, resolved)
**A:** [bridge] `bri:progression-from-functions-to-d-modules-on-bun-n`
**B:** [analytics] `ana:standard-automorphic-representations-and-planche`
**Relation:** shared-concept
**Reason:** Frenkel's 'automorphic representations become D-modules on Bun_n' vs Michel-Venkatesh's 'standard' automorphic representations with Plancherel measure: geometric vs analytic faces of automorphic representations.

### A31 — split_link (S1, resolved)
**A:** [bridge] `bri:progression-from-functions-to-d-modules-on-bun-n`
**B:** [analytics] `ana:kim-shahidi-no-complementary-series-with-paramet`
**Relation:** shared-concept
**Reason:** Frenkel's geometrization of automorphic representations vs Kim-Shahidi's constraint on local constituents of unitary automorphic representations: shared referent is automorphic representations, distinct aspects.

### A32 — split_link (S1, resolved)
**A:** [bridge] `bri:categories-aut-e-and-eisenstein-series`
**B:** [analytics] `ana:eisenstein-series-eis-f-and-deformation-pi-s`
**Relation:** geometric-analog
**Reason:** Frenkel's geometric Eisenstein series (reducible E -> Aut_E) vs Michel-Venkatesh's classical Eis(f) = sum_{B(F)\GL2(F)} f(gamma g) with deformation pi(s): geometric analog vs classical definition.

### A33 — split_link (S1, resolved)
**A:** [bridge] `bri:categories-aut-e-and-eisenstein-series`
**B:** [analytics] `ana:triple-product-period-realization-of-rankin-selb`
**Relation:** geometric-analog
**Reason:** Frenkel's geometric Eisenstein series vs Michel-Venkatesh's triple-product period realization of the Rankin-Selberg central value with E an Eisenstein series of type '1 chi': geometric vs classical Eisenstein series, the classical one entering the central-value formula.

### A34 — split_link (S1, resolved)
**A:** [bridge] `bri:irreducibility-essential-eisenstein-series-and-o`
**B:** [analytics] `ana:eisenstein-series-eis-f-and-deformation-pi-s`
**Relation:** geometric-analog
**Reason:** Frenkel's geometric Eisenstein series for non-irreducible E (open category problem) vs Michel-Venkatesh's classical Eis(f) definition: geometric analog vs classical object.

### A35 — split_link (S1, resolved)
**A:** [bridge] `bri:irreducibility-essential-eisenstein-series-and-o`
**B:** [analytics] `ana:singular-eisenstein-series-eis`
**Relation:** geometric-analog
**Reason:** Frenkel's geometric Eisenstein series (non-irreducible E) vs Michel-Venkatesh's singular classical Eis* (residue at chi_+=chi_-=1): geometric analog vs classical object.

### A36 — split_link (S1, resolved)
**A:** [bridge] `bri:irreducibility-essential-eisenstein-series-and-o`
**B:** [analytics] `ana:identity-4-36-for-f-q-at-full-level`
**Relation:** geometric-analog
**Reason:** Frenkel's geometric Eisenstein series vs Michel-Venkatesh's identity (4.36) expanded over Maass forms and classical Eisenstein series: geometric vs classical Eisenstein content.

### A37 — split_link (S1, resolved)
**A:** [bridge] `bri:irreducibility-essential-eisenstein-series-and-o`
**B:** [analytics] `ana:triple-product-period-realization-of-rankin-selb`
**Relation:** geometric-analog
**Reason:** Frenkel's geometric Eisenstein series (non-irreducible E) vs the triple-product period with classical Eisenstein series E of type '1 chi' realizing the Rankin-Selberg central value.

### A38 — split_link (S1, resolved)
**A:** [bridge] `bri:spherical-hecke-algebra-and-hecke-eigenvalues-as`
**B:** [analytics] `ana:explicit-regularizing-measure-4-3-7`
**Relation:** shared-concept
**Reason:** Frenkel packages unramified Hecke eigenvalues as conjugacy classes via Satake (H_x ~= C[z_i^{+-1}]^{S_n}, strong multiplicity one); Michel-Venkatesh's regularizing measure is built from the Hecke operators T_v and their eigenvalues lambda_v(chi) at unramified v. Same unramified Hecke eigenvalue data: parameterized via Satake vs used for analytic regularization.

### A39 — split_link (S1, resolved)
**A:** [bridge] `bri:discrete-series-to-modular-cusp-forms`
**B:** [analytics] `ana:identity-4-36-for-f-q-at-full-level`
**Relation:** shared-concept
**Reason:** Frenkel attaches a modular cusp form f_pi of weight k, level N to a discrete series pi_infty; Michel-Venkatesh's identity (4.36) is a spectral expansion over Maass forms and Eisenstein series. Both concern automorphic forms on GL_2 (holomorphic cusp forms vs Maass forms in the spectral basis).

### A40 — split_link (S1, resolved)
**A:** [bridge] `bri:hecke-eigensheaves-as-spectral-basis`
**B:** [analytics] `ana:test-function-versions-of-spectral-identities`
**Relation:** shared-concept
**Reason:** Frenkel's claim that Hecke eigensheaves are a 'good basis' of the derived category (classical analogue: Hecke eigenfunctions form a basis of cuspidal functions) vs Michel-Venkatesh's open question on test-function versions of spectral identities: geometric spectral-basis picture vs analytic spectral identities, both about the spectral decomposition of automorphic functions.

### A41 — split_link (S1, resolved)
**A:** [bridge] `bri:ramified-representations-and-affine-hecke-algebr`
**B:** [analytics] `ana:adeles-for-dynamicists-invertible-hecke-shift`
**Relation:** shared-concept
**Reason:** Frenkel's ramified classical picture: affine Hecke algebra H(G(F_y),I_y) acting on automorphic functions on G(F)\G(A)/I_y x prod G(O_x); Michel-Venkatesh's 'adeles for dynamicists': the Hecke operator T_p made invertible via the sequence space X-tilde_p. Same Hecke operators, representation-theoretic vs dynamical packaging.

### A42 — split_link (S1, resolved)
**A:** [bridge] `bri:hecke-eigensheaves-as-spectral-basis`
**B:** [analytics] `ana:associativity-formula-kuznetsov-generalization`
**Relation:** shared-concept
**Reason:** Frenkel's Hecke eigensheaves as 'good basis' of the derived category (classical analogue: Hecke eigenfunctions form a basis of cuspidal functions) vs Michel-Venkatesh's associativity formula, a spectral identity generalizing Kuznetsov's: geometric spectral basis vs proven analytic spectral identity.

### A43 — split_link (S1, resolved)
**A:** [bridge] `bri:langlands-correspondence-for-n-dimensional-galoi`
**B:** [analytics] `ana:plancherel-formula-langlands-theorem-for-l-2-x`
**Relation:** shared-concept
**Reason:** Frenkel states Langlands' conjecture (n-dimensional Gal(Fbar/F) representations <-> automorphic representations of GL_n(A_F)); Michel-Venkatesh recall Langlands' theorem (Eisenstein intertwiner gives an isometry int^oplus I(chi)dchi -> L^2(X)). The conjectural correspondence vs the proven spectral theorem - two faces of Langlands' program on automorphic representations.

### A44 — split_link
**A:** [bridge] `bri:adeles-and-ideles-as-restricted-product`
**B:** [analytics] `ana:adeles-for-dynamicists-invertible-hecke-shift`
**Relation:** shared-concept
**Reason:** Frenkel defines the adeles A_F as the restricted product of completions; Michel-Venkatesh's 'adeles for dynamicists' uses the adelic inverse limit X-tilde (all primes) to make the Hecke shift invertible. Shared infrastructure: the adeles. Control null - background infrastructure, not the seeded automorphic/L-function content.

### A45 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-map-and-integrable-system`
**B:** [geometry] `geo:algebraically-completely-integrable-hamiltonian-`
**Relation:** definition-application
**Reason:** The geometry node is the abstract definition of an algebraically completely integrable Hamiltonian system; the bridge node instantiates it, asserting the Hitchin map p: T*Bun_G -> H_G with commuting Hamiltonians is such a system. Same concept, but definition vs. instance claim -- hence split, not merge.

### A46 — split_link (S2, resolved)
**A:** [bridge] `bri:ward-identities-force-global-extension-of-opers`
**B:** [geometry] `geo:holomorphic-extension-of-eta-and-omega-to-hc-n-d`
**Relation:** extension-across-codim-2-locus
**Reason:** Both nodes prove holomorphic extension of locally defined data across a codimension->=2 singular locus: Ward identities plus the residue theorem force the one-point functions and the projective connection (opers) to extend from D_x to X (bridge), while eta and omega=-d(eta) extend to all of HC(n,d) because the unstable/singular complement has codim >= 2 (geometry). Shared proof technique, distinct objects.

### A47 — split_link (S2, resolved)
**A:** [bridge] `bri:critical-level-vs-wzw-coinvariant-behavior`
**B:** [geometry] `geo:singular-spectral-curves-and-heisenberg-kp-flows`
**Relation:** singular-locus-workaround
**Reason:** Both are heuristic remarks on working past singular loci in moduli: the bridge notes coinvariant dimensions drop along Bun_G's singular locus, so one works with the D-module rather than functions; the geometry allows singular spectral curves away from the singular locus and invokes Heisenberg KP flows plus the moduli stack to work over all of V*_GL. Shared motif, distinct moduli problems.

### A48 — merged_link (S2, resolved)
**A:** [bridge] `bri:hitchin-map-and-integrable-system`
**B:** [geometry] `geo:theorem-2-1-hitchin-fibration-is-algebraically-c`
**Reason:** Both nodes state the same theorem: the Hitchin map/fibration is an algebraically completely integrable system with Lagrangian/abelian-variety (Jacobian) fibers -- the bridge as the Hitchin map p: T*Bun_G -> H_G with Fun T*Bun_G ~= Fun H_G, the geometry as Hitchin's Theorem 2.1 (attributed to Hitchin [9]). Identical referent, established-fact role on both sides.

### A49 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-fibration-and-fiberwise-transform`
**B:** [geometry] `geo:theorem-2-2-hamiltonian-flows-are-linear-jacobia`
**Relation:** shares-concept
**Reason:** Both concern the Hitchin fibration's generic abelian-variety fibers and their linear structure: the bridge (heuristic) hopes for a fiberwise Fourier-Mukai equivalence on those fibers, while the geometry's Theorem 2.2 asserts the Hitchin Hamiltonian flows are linear Jacobian flows on generic fibers. Same fibration, distinct claims.

### A50 — split_link (S2, resolved)
**A:** [bridge] `bri:complex-curve-construction-of-aut-e-via-abeliani`
**B:** [geometry] `geo:injectivity-of-pi-jac-c-jac-cs`
**Relation:** abelianization-via-jacobian
**Reason:** Both use the Jacobian as the abelianization site: the bridge constructs the GL_1 Hecke eigensheaf Aut_E from a rank-one local system via Jac(X) (E_Jac = Aut^0_E, descent along Abel-Jacobi fibers), while the geometry proves pi*: Jac(C) -> Jac(Cs) injective via the projection formula with the Jac(C)-action factoring through it. Shared abelianization machinery, distinct constructions.

### A51 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-map-and-integrable-system`
**B:** [geometry] `geo:hitchin-identification-of-character-variety-with`
**Relation:** integrable-system-identification
**Reason:** The bridge node's Hitchin map on T*Bun_G and the geometry node's Hitchin identification of the character variety with G-Higgs moduli share one referent -- the Hitchin integrable-system structure -- the geometry node equipping the character variety with the structure the bridge describes on the bundle side. Distinct statements, shared system.

### A52 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-map-and-integrable-system`
**B:** [geometry] `geo:theorem-5-6-hitchin-system-is-pullback-of-n-comp`
**Relation:** kp-pullback-identification
**Reason:** Both nodes are about the Hitchin integrable system: the bridge asserts the Hitchin map gives an algebraically completely integrable system, while the geometry's Theorem 5.6 identifies that same system as the pullback of the n-component KP equations. Same object, distinct characterizations.

### A53 — split_link (S2, resolved)
**A:** [bridge] `bri:quantization-of-the-hitchin-system`
**B:** [geometry] `geo:theorem-7-1-sp-hitchin-equations-as-twisted-self`
**Relation:** shares-concept
**Reason:** Both concern the Hitchin system on opposite sides of quantization: the bridge is the Beilinson-Drinfeld quantization (Fun Op_{^Lg}(X) ~= D'_{-h^vee}, proof reducing to the Hitchin isomorphism on associated graded), while the geometry gives the classical Sp-Hitchin equations as a twisted-self-adjoint KP reduction. Shared system, distinct (quantum vs. classical) formulations.

### A54 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-fibration-and-fiberwise-transform`
**B:** [geometry] `geo:c-scaling-gives-trivial-spectral-deformations-qu`
**Relation:** shares-concept
**Reason:** Both are about the Hitchin fibration itself: the bridge (heuristic) discusses its abelian-variety fibers and the hoped fiberwise Fourier-Mukai transform, while the geometry proves it is C*-equivariant (phi -> lambda.phi preserves spectral curves) so the C* action must be quotiented out. Same fibration, distinct properties.

### A55 — split_link (S2, resolved)
**A:** [bridge] `bri:loc-1-as-twisted-cotangent-bundle-of-the-jacobia`
**B:** [geometry] `geo:proposition-2-4-sp2m-hitchin-as-serre-duality-fi`
**Relation:** serre-duality-on-moduli
**Reason:** Both invoke Serre duality on the relevant moduli: the bridge identifies Loc_1 (moduli of flat line bundles) with the twisted cotangent bundle T*Jac via Serre duality, while the geometry's Proposition 2.4 identifies the Sp2m-Higgs moduli as the fixed-point set of the Serre-duality involution (E,phi) -> (E* x K_C, -phi*). Shared involution, distinct moduli.

### A56 — split_link (S2, resolved)
**A:** [bridge] `bri:loc-1-as-twisted-cotangent-bundle-of-the-jacobia`
**B:** [geometry] `geo:serre-duality-involution-on-higgs-moduli`
**Relation:** serre-duality-on-moduli
**Reason:** The bridge realizes Loc_1 as T*Jac via Serre duality; the geometry defines the Serre-duality involution (2.4) on Higgs moduli HC(n,-d+2n(g-1)). Both are the Serre-duality involution on bundle-type moduli -- one for flat line bundles, one for Higgs bundles.

### A57 — split_link (S2, resolved)
**A:** [bridge] `bri:riemann-hilbert-correspondence`
**B:** [geometry] `geo:hitchin-identification-of-character-variety-with`
**Relation:** moduli-of-local-systems
**Reason:** The geometry node's character variety is the moduli space of the local systems in the bridge node: the bridge states the Riemann-Hilbert equivalence of local systems with flat holomorphic bundles, while the geometry cites Hitchin's identification of the character variety with G-Higgs moduli. Two different identifications sharing the local-systems referent.

### A58 — split_link (S2, resolved)
**A:** [bridge] `bri:d-modules-as-d-branes`
**B:** [geometry] `geo:character-variety-functor-sends-langlands-dualit`
**Relation:** langlands-mirror-symmetry-motif
**Reason:** Both nodes (heuristic/conjectural, motivation-level) connect Langlands duality to mirror symmetry: the bridge asks whether D-modules (the geometric-Langlands objects) interpret as D-branes in Kontsevich homological mirror symmetry, while the geometry cites Hausel-Thaddeus that the character-variety functor sends Langlands duality to SYZ mirror symmetry. Shared motif, distinct mirror pictures.

### A59 — split_link (S2, resolved)
**A:** [bridge] `bri:moduli-stack-bun-n-of-rank-n-bundles`
**B:** [geometry] `geo:singular-spectral-curves-and-heisenberg-kp-flows`
**Relation:** moduli-stack-machinery
**Reason:** Both nodes invoke Artin moduli stacks to work over singular/unstable loci: the bridge argues Bun_n must be a stack (no variety parametrizes all rank-n bundles), while the geometry's Remark 5.7 calls it desirable to work over all of V*_GL with the moduli stack when allowing singular spectral curves. Shared stack machinery, distinct stacks.

### A60 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-fibration-and-fiberwise-transform`
**B:** [geometry] `geo:algebraically-completely-integrable-hamiltonian-`
**Relation:** definition-application
**Reason:** The bridge node's Hitchin fibration T*Bun^circ_G -> H_G with abelian-variety generic fibers is an instance of the geometry node's definition of an algebraically completely integrable Hamiltonian system (general fiber an N-dimensional abelian variety). Definition vs. instance -- split.

### A61 — split_link (S2, resolved)
**A:** [bridge] `bri:complex-curve-construction-of-aut-e-via-abeliani`
**B:** [geometry] `geo:spectral-correspondence-hitchin-fiber-jacobian-o`
**Relation:** abelianization
**Reason:** Both are the abelianization move: the bridge constructs the GL_1 Hecke eigensheaf Aut_E from a rank-one local system via Jac(X), while the geometry's spectral correspondence sends a Higgs bundle (E,phi) to the line bundle LE on the spectral curve Cs with Hitchin fiber Pic(Cs) ~= Jac(Cs). Same principle (non-abelian data as line bundles on an abelian variety), distinct constructions.

### A62 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-fibration-and-fiberwise-transform`
**B:** [geometry] `geo:hitchin-fibration-via-characteristic-coefficient`
**Relation:** shares-concept
**Reason:** Both nodes are the Hitchin fibration/map: the bridge (heuristic) as the arena for the hoped fiberwise Fourier-Mukai equivalence in geometric Langlands, the geometry (exact) via its definition H(E,phi) = det(x-phi). Identical object, but heuristic program vs. exact definition -- hence split, not merge.

### A63 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-fibration-and-fiberwise-transform`
**B:** [geometry] `geo:theorem-2-1-hitchin-fibration-is-algebraically-c`
**Relation:** theorem-instantiation
**Reason:** The bridge node's Hitchin fibration with abelian-variety generic fibers is the object of the geometry node's Theorem 2.1, which asserts it is a generically Lagrangian Jacobian fibration and algebraically completely integrable; the bridge's fiberwise Fourier-Mukai hope presupposes the abelian-fiber structure the theorem establishes.

### A64 — split_link (S2, resolved)
**A:** [bridge] `bri:quantization-of-the-hitchin-system`
**B:** [geometry] `geo:sp-hitchin-system-as-serre-duality-fixed-point-s`
**Relation:** shares-concept
**Reason:** Both concern the Hitchin system: the bridge's Beilinson-Drinfeld quantization (Fun Op_{^Lg}(X) ~= D'_{-h^vee}) and the geometry's Sp-Hitchin system as the Serre-duality fixed-point set of the GL-Hitchin system with KP (not BKP/CKP) reduction. Same system family, distinct (quantum vs. classical Sp) aspects.

### A65 — split_link (S2, resolved)
**A:** [bridge] `bri:quantization-of-the-hitchin-system`
**B:** [geometry] `geo:theorem-5-6-hitchin-system-is-pullback-of-n-comp`
**Relation:** shares-concept
**Reason:** The bridge node's quantized Hitchin system and the geometry node's Theorem 5.6 (the Hitchin integrable system as pullback of n-component KP) share the Hitchin system as referent -- quantum formulation vs. classical KP realization.

### A66 — split_link (S2, resolved)
**A:** [bridge] `bri:langlands-duality-and-qft-string-dualities-as-no`
**B:** [geometry] `geo:character-variety-functor-sends-langlands-dualit`
**Relation:** shares-concept
**Reason:** Both are framings of Langlands duality in terms of another duality: the bridge (heuristic survey) as 'some sort of non-abelian Fourier transform', the geometry (cited, conjectural) as sent to SYZ mirror symmetry by the character-variety functor. Shared subject (Langlands duality), distinct target dualities.

### A67 — split_link (S2, resolved)
**A:** [bridge] `bri:witten-s-s-duality-to-langlands-duality-scenario`
**B:** [geometry] `geo:character-variety-functor-sends-langlands-dualit`
**Relation:** shares-concept
**Reason:** Both concern Langlands duality in physical/geometric terms: the bridge gives Witten's scenario (S-duality -> Langlands duality, 't Hooft operators becoming Hecke operators, eigenbrane becoming Hecke eigensheaf), the geometry cites the character-variety functor sending Langlands duality to SYZ mirror symmetry. Shared Langlands-duality referent with Hecke content on the bridge side.

### A68 — split_link (S2, resolved)
**A:** [bridge] `bri:kapustin-witten-relation-of-langlands-duality-to`
**B:** [geometry] `geo:character-variety-functor-sends-langlands-dualit`
**Relation:** shares-concept
**Reason:** The bridge cites Kapustin-Witten (Langlands duality closely related to S-duality of QFT); the geometry cites Hausel-Thaddeus (Langlands duality sent to SYZ mirror symmetry). Both are cited identifications of Langlands duality with another duality.

### A69 — split_link (S2, resolved)
**A:** [bridge] `bri:loc-1-as-twisted-cotangent-bundle-of-the-jacobia`
**B:** [geometry] `geo:sp-hitchin-system-as-serre-duality-fixed-point-s`
**Relation:** serre-duality-on-moduli
**Reason:** The bridge node's Loc_1 ~= T*Jac via Serre duality and the geometry node's Sp-Hitchin system as the fixed-point set of Serre duality on the GL-Hitchin system both engage Serre duality on Hitchin-type moduli -- rank-one vs. symplectic cases.

### A70 — split_link (S2, resolved)
**A:** [bridge] `bri:loc-1-as-twisted-cotangent-bundle-of-the-jacobia`
**B:** [geometry] `geo:sp-prym-fibration-and-its-dual-via-quotient-by-g`
**Relation:** abelian-fibration-via-serre-duality
**Reason:** Both describe abelian-variety fibrations tied to Serre duality in the Hitchin picture: the bridge node's Loc_1 fibers over Jac = Pic^0 (T*Jac via Serre duality), the geometry node's V_Sp generates the Prym fibration {Prym(Cs/C'_s)} along the Serre-duality fixed set. GL_1/Jacobian vs. Sp/Prym instances of the same abelian-fibration structure.

### A71 — split_link (S2, resolved)
**A:** [bridge] `bri:loc-1-as-twisted-cotangent-bundle-of-the-jacobia`
**B:** [geometry] `geo:theorem-6-8-serre-duality-as-adjoint-action`
**Relation:** serre-duality-correspondence
**Reason:** Both nodes are about Serre duality: the bridge geometrically (Loc_1 ~= T*Jac via Serre duality), the geometry as realized on the KP side (Theorem 6.8: Serre duality is the adjoint action W^perp <-> (S*)^{-1} on pseudo-differential operators). Shared involution, geometric vs. KP-operator realizations.

### A72 — split_link (S2, resolved)
**A:** [bridge] `bri:loc-1-as-twisted-cotangent-bundle-of-the-jacobia`
**B:** [geometry] `geo:lax-operator-and-serre-duality-on-lax-operators`
**Relation:** serre-duality-correspondence
**Reason:** The bridge node's Serre duality on Loc_1 (T*Jac) and the geometry node's Serre duality acting as the adjoint on Lax operators (W <-> L implies W^perp <-> L*) are the same involution on the geometric and Lax-operator sides.

### A73 — split_link (S2, resolved)
**A:** [bridge] `bri:hitchin-map-and-integrable-system`
**B:** [geometry] `geo:theorem-2-2-hamiltonian-flows-are-linear-jacobia`
**Relation:** theorem-instantiation
**Reason:** The bridge node's Hitchin map as an algebraically completely integrable system is the object whose Hamiltonian flows the geometry node's Theorem 2.2 describes as linear Jacobian flows on generic fibers. Same system; the geometry node supplies its flow structure.

### A74 — split_link (S2, resolved)
**A:** [bridge] `bri:complex-curve-construction-of-aut-e-via-abeliani`
**B:** [geometry] `geo:cayley-hamilton-construction-of-le`
**Relation:** abelianization-construction
**Reason:** Both construct rank-one (line-bundle) data on an auxiliary curve from higher-rank input: the bridge builds the Hecke eigensheaf Aut_E from a rank-one local system via Jac(X) (abelianization), the geometry builds the spectral line bundle LE on Cs from a Higgs bundle (E,phi) via the Cayley-Hamilton factorization. Distinct constructions of the same abelianization type.

### A75 — split_link (S2, resolved)
**A:** [bridge] `bri:loc-1-as-twisted-cotangent-bundle-of-the-jacobia`
**B:** [geometry] `geo:spectral-correspondence-hitchin-fiber-jacobian-o`
**Relation:** jacobian-hitchin-fiber
**Reason:** The bridge node's Loc_1 -> Jac = Pic^0 fibration is the GL_1 (abelian) case of the Hitchin picture whose generic fiber the geometry node's spectral correspondence identifies with the Jacobian of the spectral curve (for n=1, Cs = C). Shared Jacobian-as-abelian-fiber referent.

### A76 — split_link (S2, resolved)
**A:** [bridge] `bri:moduli-stack-bun-n-of-rank-n-bundles`
**B:** [geometry] `geo:hitchin-identification-of-character-variety-with`
**Relation:** bundle-moduli-arena
**Reason:** Both concern the moduli of G-bundles as the geometric-Langlands arena: the bridge argues Bun_n must be an Artin stack (automorphism groups vary), while the geometry identifies the character variety with the moduli of stable G-Higgs bundles (pairs (E,phi) over the bundle E). Shared bundle-moduli referent; distinct claims (stack foundations vs. non-abelian Hodge identification).

### A77 — split_link (S2, resolved)
**A:** [bridge] `bri:hecke-eigensheaf-as-system-of-differential-equat`
**B:** [geometry] `geo:hitchin-identification-of-character-variety-with`
**Relation:** shares-hitchin-moduli
**Reason:** The bridge node's Hecke eigensheaf has singular support the global nilpotent cone p^{-1}(0) -- the Hitchin map's zero fiber -- while the geometry node identifies the character variety with the G-Higgs moduli carrying the Hitchin integrable structure. Both refer to the Hitchin moduli space, one via the quantum D-module side, one via the classical identification.

### R1 — rejected
**Pair:** analytics ↔ geometry
**Reason:** 0 of 123 mechanical candidates resolved; all 123 reviewed individually and marked missed. Strongest near-misses declined on the evidence: 'projection formula' (MV (4.22) L2 spectral-projection norm identity vs Mulase sheaf projection formula pi_*(pi^*L tensor -) — same name, different theorems); 'spectral' (automorphic spectral decomposition vs Higgs-field spectrum; 'ramified' likewise homonymous); 'adjoint' (adjoint L-function vs formal adjoint of pseudo-differential operator). Other declined homonyms: compactly supported (test functions vs compactly supported cohomology), orbits, flows, smooth (vectors vs morphisms), self-adjointness, residues, coefficients, restriction. Generator-miss scan (periods/Hecke/Eisenstein/Whittaker, Lax/KP/Hitchin, moment/character/orthogonal/curve/integrable/singular/family) found no genuine pair outside the candidate list. The direct arm is a clean wall at this pilot scale.

### R2 — rejected
**Pair:** bridge ↔ analytics
**Reason:** 107 of 151 mechanical candidates marked missed after individual review. Declined homonyms recorded per record: Harish-Chandra functor vs spherical function; affine Hecke algebra vs Hecke period functional; Langlands vs Jacquet-Langlands; Hecke eigensheaf vs Hecke integral; Arthur's SL2 vs Arthur truncation; Hecke eigenvalues vs geodesic/Eisenstein Fourier coefficients (same phrase family, different notions). 44 split_links resolved separately — none of the misses concealed a control-bearing link.

### R3 — rejected
**Pair:** bridge ↔ geometry
**Reason:** 74 of 107 mechanical candidates marked missed after individual review. The 19-candidate 'differential operators' block is systematically homonymous (holomorphic/twisted differential operators of Frenkel's D-modules on Bun_G vs pseudo-differential operators of Mulase's Sato/KP formalism); other caught homonyms: direct sum, finite-dimensional, modular, Deligne, rational, cover, orbit, functor/sends. 1 merged_link + 32 split_links resolved separately. No control-bearing link among the misses.

## Contradictions

0. The merge flagged no `contradicts` relations; no adjudication surfaced one.

## Reviewer notes (from arm reviewers)

### direct: Direct-arm adjudication, Atlas-11. Reviewed all 123 candidates by reading both endpoint facet notes in full. Verdict: 123 missed, 0 merged, 0 split. The candidate generator (threshold >=8.0, recall-favoring) matched almost entirely on homonymous tokens: lambda (spectral parameter vs C*-scaling scalar, 10 candidates), spectral (automorphic spectral decomposition vs Higgs-field spectrum; cf. watch-list #81), projection formula (#1, checked against source text: MV's (4.22) is the L2 spectral-projection norm identity, Mulase's is the sheaf projection formula - different theorems), compactly suppor

### S1: S1 is the seeded positive control (classical Langlands content in the Frenkel bridge paper <-> the analytics sky). All 151 candidates were read against full node facets. 0 merged_link (bar held: same-object pairs like #2/#3 and #122 differ in epistemic role - definition vs counting theorem, conjecture vs spectral theorem - so were kept as split_link, not merged). 44 split_link: 42 bear on S1 (automorphic representations #2/#3/#12/#26/#47/#48/#50/#52/#53/#55/#56, principal series #30/#31, Kim-Shahidi #49/#51/#54/#57, Theorem 1.1 subconvexity #34/#35, Hecke operators/eigenvalues #40/#41/#99/#111

### S2: S2 is the seeded positive control (Frenkel geometric-Langlands bridge vs. Mulase Hitchin/KP + Tosteson DM geometry), and it resolves decisively: 1 merged + 32 split links, 74 missed, 33 S2-bearing resolved records. Carrying links: (1) the Hitchin-system cluster -- #3 merged (Hitchin map/fibration as algebraically completely integrable system, both skies), #0/#22 definition-applications, #9 (Hitchin identification of character variety with G-Higgs moduli), #10/#33 (Hitchin = pullback of n-component KP), #30/#31/#12/#5/#66 (Hitchin fibration, its abelian fibers, C*-equivariance, linear Jacobian 
