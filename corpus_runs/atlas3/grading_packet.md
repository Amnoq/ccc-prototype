# Atlas-3 grading packet

For the user: grade a sample the way the pilot was graded. Every triple below is concept / paper-quote / status. Then ALL adjudications (1 split_link, 3 rejected, 1 control void, 0 contradictions, 0 false merges). His narrow/wide verdict on the direct test resolves ledger item 3.

## Sampled triples (12)

### [geometry] the reduced volume ̃V(τ) and its monotonicity via the Bishop-Gromov relative volume comparison
- status: `heuristic` · kind: claim · file: perelman_p1.json / c13
- paper quote: 6.3: the Bishop-Gromov relative volume comparison on (̃M, ̃g) suggests the reduced volume ̃V(τ) = ∫ τ^{−n/2} exp(−L/√(2τ)) dx should increase as τ decreases; 6.3 states the rigorous proof is in §7 (which the chunk cuts b

### [algebra] Lemma 4.5: M is Gorenstein projective over A iff M_p is Gorenstein projective over A_p for each prime p (resp.
- status: `exact` · kind: result · file: liuren_p2.json / c5
- paper quote: Lemma 4.5; said to follow from the characterization of Gorenstein projective modules in 2.1, and to hold verbatim with 'projective' in place of 'Gorenstein projective'.

### [bridge] Hecke eigensheaf as holonomic twisted D-module on Bun_n determined by E
- status: `exact` · kind: definition · file: frenkel_p1.json / c1
- paper quote: Defined as a D-module on Bun_n satisfying a property determined by a holomorphic rank-n bundle with connection E on X; for general G it attaches to a holomorphic ^L G-bundle with connection a Hecke eigensheaf on Bun_G.

### [geometry] Psi is a desingularization of the RP^5-family Phi_5, with only finitely many desingularities left (Remark 4.1)
- status: `conjectural` · kind: claim · file: chuliwang_p2.json / c4
- paper quote: Remark 4.1 frames Psi as a desingularization of Phi_5 (Phi_5(a) = {a_0 + ... + a_5 x1 x2 = 0}); the desingularization claim rests on Theorem 4.2, whose proof is deferred.

### [algebra] ascent and descent of Gorenstein projective property
- status: `exact` · kind: definition · file: liuren_p1.json / c1
- paper quote: Introduced in the Introduction as the paper's motivating property: a finitely generated A-module is Gorenstein projective iff the underlying R-module is.

### [geometry] The canonical RP^5 family tilde{Phi}_5(a), Phi_5(a) = S^3 cap tilde{Phi}_5(a) (5.2)/(5.3): zero sets of a_0 + 
- status: `exact` · kind: definition · file: chuliwang_p2.json / c16
- paper quote: Phi_5 defined in (5.2)/(5.3); the paper notes it gives a 5-sweepout in the Almgren--Pitts setting but is not a Simon--Smith family.

### [algebra] ITI(KG) (resp. ITS(KG)): a set of representatives of the isomorphism types of indecomposable (resp. simple) mo
- status: `exact` · kind: definition · file: harris_p1.json / c3
- paper quote: Notation introduced in the paper, following [2, Section 2].

### [bridge] Galois representation sigma_{E,ell} from the first etale cohomology of an elliptic curve E over Q (dual of the
- status: `exact` · kind: definition · file: frenkel_p2.json / c11
- paper quote: Paper constructs sigma_{E,ell}: Gal(Qbar/Q) -> GL_2(Q_ell) from the first etale cohomology H^1_et(E_Qbar, Q_ell) ~= Q_ell^2 of an elliptic curve E over Q, concretely the dual of the Tate module; continuous in the Krull t

### [geometry] Theorem 1.1 (Enumerative min-max theorem): p cohomology classes satisfying (1) and (2) yield at least p+1 orie
- status: `exact` · kind: claim · file: chuliwang_p1.json / c4
- paper quote: Theorem 1.1 (L64–92). The full proof is carried out in §3: Lemma 3.1, Propositions 3.2–3.3, closing with 'we finish the proof of Proposition 3.3, and also Theorem 1.1' (L692). The produced surfaces have genus exactly g a

### [geometry] completion of a central component of the program of using topological methods to enumerate minimal surfaces wi
- status: `heuristic` · kind: claim · file: chuliwang_p1.json / c17
- paper quote: Abstract/§1 (L16–18): the paper 'completes a central component of our program of using topological methods to enumerating minimal surfaces with prescribed genus [8, 9, 7].'

### [geometry] \u00a77.3: alternative proof of a weakened no local collapsing theorem 4.1 by reduced-volume contradiction; st
- status: `exact` · kind: result · file: perelman_p2.json / c21
- paper quote: Argued in §7.3: the \mathcal{L}-exponential map integrates over T_pM; short vectors contribute \le 2\epsilon_k^{n/2} and long vectors \le exp(-\epsilon_k^{-1/2}/2) to \tilde V_k(\epsilon_k r_k^2)<3\epsilon_k^{n/2}, while

### [algebra] Frobenius extension of rings S subset A (A finitely generated projective as left S-module with _A A_S ~= Hom_S
- status: `conjectural` · kind: definition · file: liuren_p2.json / c7
- paper quote: Standard definition recalled from [27], with the two equivalent conditions (1)(2); interesting examples in [26]. Not established in this chunk.

## All adjudications

### S1: split_link (shares-discipline)
- A [bridge] automorphic representations (irreducible representations of GL_n(A_F) occurring in functions on GL_n(F)\GL_n(A_F), discr (`exact`)
- B [algebra] ITI(KG) (resp. ITS(KG)): a set of representatives of the isomorphism types of indecomposable (resp. simple) modules in m (`exact`)
- reason: S1 WEAK PASS. Genuine field-level relationship: the bridge's core subject (automorphic representations of GL_n(A_F)) and the algebra sky's core subject (modular representation theory of finite groups) are both representation theory. Different objects (adelic groups vs finite groups in characteristic p), so linked as shared discipline, NOT merged. Found ONLY by semantic review — the mechanical token-overlap pass missed it (R&D finding: mechanical recall fails across domain vocabularies).

### S1: rejected
- A [bridge] Galois representation sigma_{E,ell} from the first etale cohomology of an elliptic curve E over Q (dual of the Tate modu (`exact`)
- B [algebra] (5): for fixed K in Delta the members of E(W) over K are exactly the Galois conjugates (K, V^sigma) for sigma in Aut(K) (`exact`)
- reason: Mechanical candidate (shared tokens 'galois','sigma') correctly rejected by review: FALSE FRIEND. Bridge = continuous representation of Gal(Qbar/Q) on l-adic etale cohomology (arithmetic). Algebra = (K,V^sigma) for sigma in Aut(K/F), field automorphisms acting on module structures. Same word, different referents.

### S1: rejected
- A [bridge] Taniyama-Shimura conjecture proved by Wiles and others; implies Fermat's last theorem; bijection between isogeny classes (`exact`)
- B [algebra] Example 4.9: the surjection S[[x]]/(x^2) -> S with S not Iwanaga-Gorenstein has ascent and descent of Gorenstein project (`killed`)
- reason: Mechanical candidate (shared generic tokens 'between','implies','over','theorem') correctly rejected: unrelated referents (Taniyama-Shimura bijection vs a Gorenstein ring-theory example). Spurious token match.

### direct: rejected
- A [algebra] Example 4.9: the surjection S[[x]]/(x^2) -> S with S not Iwanaga-Gorenstein has ascent and descent of Gorenstein project (`killed`)
- B [geometry] \u00a77.3: alternative proof of a weakened no local collapsing theorem 4.1 by reduced-volume contradiction; strengthened (`exact`)
- reason: Mechanical candidate (shared generic tokens 'corollary','local','theorem') correctly rejected: unrelated referents (ring-theory example vs Ricci-flow proof technique). Spurious token match. Direct A<->G test: no genuine links found by mechanical OR semantic review.

### S2: control_void
- A [bridge] geometric Langlands content (Hecke eigensheaves, Bun_G, moduli of bundles)
- B [geometry] differential-geometry sky (Ricci flow, minimal surfaces)
- reason: S2 VOID (misseeded, not method failure). Geometric Langlands touches COMPLEX-ALGEBRAIC geometry (holomorphic bundles, D-modules on Bun_G); the geometry sky as built is DIFFERENTIAL geometry (Ricci flow, minimal surfaces). No shared objects exist at node level at this chunk depth — the method correctly found nothing because there is nothing at node level. R&D spec: positive controls must be seeded against the right subfield; 'geometry' is not one sky.

## Contradictions: none flagged. False merges: 0.
