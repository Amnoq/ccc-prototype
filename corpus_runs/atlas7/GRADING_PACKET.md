# Atlas-7 grading packet

Sampled concept / paper-quote / status triples. To grade: pick any triple, open the cited chunk file,
and check the label against the paper text, the note against what the paper actually says,
and whether the status label is honest.

## an1
- **concept:** the Birch and Swinnerton-Dyer conjecture implies the Sylvester conjecture
  **paper note:** Conditional implication proved in §1: root number −1 plus BSD gives positive rank, hence a cube sum.
  **status:** exact | **genre:** original

- **concept:** base-change L-function factorization L(s,E_9,χ) = L(s,E_p)·L(s,E_{3p²}), sign −1
  **paper note:** From the Artin formalism; L(s,E_p) has a simple zero at s=1 and L(1,E_{3p²}) ≠ 0 by [DV17].
  **status:** exact | **genre:** original

- **concept:** Sylvester conjecture: any prime p ≡ 4,7,8 mod 9 is a cube sum
  **paper note:** Attributed to Sylvester [Syl79] and Selmer [Sel51]; stated as Conjecture 1.1 in the paper; no proof attempted here.
  **status:** conjectural | **genre:** reframed

- **concept:** Remark 7.1: the strategy should work in full generality
  **paper note:** Remark 7.1 states this as an expectation for future applications, without proof in this paper.
  **status:** heuristic | **genre:** original

- **concept:** Theorem 2.2: explicit modular actions P^{1+3ω_3}=[ω²]P; P^{ω_3} (p≡4/7 mod 9 cases); P^{wε} (p≡7 mod 9)
  **paper note:** Proved by checking conjugates like B(1+3ω_3)A², Cω_3A² lie in V via explicit 3-adic matrix computations.
  **status:** exact | **genre:** original

## al1
- **concept:** Corollary 8.2.2: for nu(N-) even, the Heegner point main conjecture holds — Sel(K_infty, A_f[p^infty])^vee approx Lambda + M + M and Char_La
  **paper note:** Corollary 8.2.2: the nu(N-) even case of Theorem 8.2.1 gives the Heegner point main conjecture with the pseudo-isomorphism and the characteristic-ideal equality.
  **status:** exact | **genre:** original

- **concept:** Corollary 8.3.6: nu_m = max{r_m+, r_m-} when nu(N-) is odd, nu_m = max{r_m+, r_m-} - 1 when even, with the stated parity and tau-eigenvalue 
  **paper note:** Corollary 8.3.6 proved from Theorem 3.3.8's parity, Proposition 8.3.2, Lemma 8.3.3, and Proposition 6.2.7; the final statement uses that kappa(1,1) is the Kummer image of the classical Heegner point t
  **status:** exact | **genre:** original

- **concept:** whether the full anticyclotomic main conjecture holds when p is inert in K or non-ordinary
  **paper note:** Section A.1.2 states that the anticyclotomic main conjecture is currently not known in full generality when p is non-ordinary or inert in K; the paper circumvents it by combining main conjectures for 
  **status:** conjectural | **genre:** original

- **concept:** proof strategy for Theorems A and D: extend Kolyvagin's construction to classes c(m,Q1) and lambda(m,Q2) with auxiliary primes; for fixed m 
  **paper note:** Proof overview of section 1.4: the enlarged system c(m,Q1), lambda(m,Q2); bipartite Euler system for fixed m, Kolyvagin system for fixed Q1; the Euler system relations (8)-(9).
  **status:** exact | **genre:** original

- **concept:** Theorem 8.1.1 (Skinner-Urban): if Sel_{F_Lambda}(W_f) is Lambda-cotorsion then Char_Lambda Sel_{F_Lambda}(W_f)^vee is contained in (lambda-b
  **paper note:** Theorem 8.1.1: a corollary to the proof of the Skinner-Urban three-variable main conjecture [47], adapted here without the full residual-ramification hypothesis at N2; the core divisibility is cited f
  **status:** conjectural | **genre:** reframed

## c1
- **concept:** covariant columns are used in Section 5 for phi_{2,3} and phi_{3,4}; the classification explains where the formulae come from
  **paper note:** The paper explains that covariant columns are used in Section 5 to give formulae for phi_{2,3} and phi_{3,4}; the full classification is more than needed but explains where the formulae come from.
  **status:** exact | **genre:** original

- **concept:** every elliptic curve of prime conductor in the Stein-Watkins database has rank at least as large as predicted by the conjecture of Birch and
  **paper note:** Main application result: every elliptic curve of prime conductor in the Stein-Watkins database has rank at least as large as predicted by the conjecture of Birch and Swinnerton-Dyer.
  **status:** computationally_verified | **genre:** verified

- **concept:** 48 different 12-coverings computed from inverse pairs of order 12 in S^(12) ~= (Z/12)^2
  **paper note:** For the worked example, Magma returned 4 ternary cubics and 6 pairs of quadrics (inverse pairs for n=3,4); 48 different 12-coverings were computed from the inverse pairs of order 12 in S^(12) ~= (Z/12
  **status:** computationally_verified | **genre:** verified

- **concept:** height heuristic: a point of logarithmic height h on E(Q) should come from a point of height approximately h/(2n) on C_alpha(Q)
  **paper note:** Citing the theory of heights [13], the paper notes the imprecise heuristic that a point of logarithmic height h on E(Q) should come from a point of height about h/(2n) on a covering, motivating larger
  **status:** heuristic | **genre:** reframed

- **concept:** ad hoc minimisation for n > 5 via the gain m - (n-3)d
  **paper note:** The paper's ad hoc minimisation for n > 5: compute linear forms in the radical of I_p, transform, and keep the new quadrics when the gain m - (n-3)d is positive; there is no guarantee of a p-minimal m
  **status:** exact | **genre:** original

## c2
- **concept:** new K3 family E_u/Q(t) with Mordell-Weil group Z/2Z x Z^9 parametrized by the genus-zero Shimura curve of level 230
  **paper note:** New K3 family E_u/Q(t) of form y^2=x^3+2Ax^2+Bx with A, B_i from (3)-(4), parametrized by the genus-zero Shimura curve X/w_230 of level 230 (quaternion algebra ramified at {2,5}); for u!=+/-1,+/-2 wit
  **status:** exact | **genre:** original

- **concept:** Table 1: five records broken by 1, Z/5Z record of 8 stands
  **paper note:** Table 1 (Sec 8): Z/2Z 19->20, Z/3Z 14->15, Z/4Z 12->13, Z/5Z 8->8 (record stands), Z/6Z 8->9, Z/7Z 5->6; previous records as given by Dujella [5].
  **status:** computationally_verified | **genre:** original

- **concept:** Tamagawa bonus hack log(c(p-1)/p) with 1.2<=c<=1.68 works reasonably well but is a hack
  **paper note:** Empirical hack: adding log(c(p-1)/p) with 1.2<=c<=1.68 at each split-multiplicative prime (a fixed per-prime bonus) 'tended to work reasonably well', but is 'clearly a hack'.
  **status:** heuristic | **genre:** original

- **concept:** Kihara degree-4 rank-3 surface abandoned for Z/6Z after no rank-8 specializations above height ~2^13.5
  **paper note:** Abandoned the Kihara degree-4 rank-3 surface for Z/6Z: many low-height rank-8 specializations but none above height ~2^13.5, suggesting either rapid decay of high-rank specializations or loss of score
  **status:** killed | **genre:** killed

- **concept:** Birch and Swinnerton-Dyer conjecture linking large rank to rapidly vanishing partial products
  **paper note:** States: 'The conjecture of Birch and Swinnerton-Dyer suggests that when E_t has large rank such partial products should rapidly approach zero, and thus that S(t,B) should be large.'
  **status:** conjectural | **genre:** original

---
# ALL adjudications (15)

## A7-01 — SPLIT (algebraic-analytic) · seed S1
- A: corollary-c-p-converse-theorem-l-f-k-1-0-iff-rank-o-
- B: theorem-4-3-explicit-gross-zagier-l-1-e-p-l-1-e-3p2-
- relation: split_link
- role difference: analytic: proved an explicit GZ height formula for specific curve families (L-value <-> canonical height of a Heegner cycle); algebraic: cited the classical GZ formula [GZ86] as an identification step inside Kolyvagin-system machinery toward the p-converse theorem
- reason: AL1's p-converse theorem explicitly 'uses the cited Gross-Zagier formula' to identify L'(f/K,1)!=0 with nonvanishing of the Heegner class; AN1 proves a NEW explicit Gross-Zagier formula (Theorems 1.5/4.3) for the E_p/E_{3p^2} family. Same theorem-type, different instantiation and direction of travel: AN1 produces the formula (analytic output), AL1 consumes the classical formula as a black-box bridge input (algebraic input). Not the same referent, so not a merge.

## A7-02 — SPLIT (algebraic-analytic) · seed S1
- A: corollary-8-3-6-nu-m-max-r-m-r-m-when-nu-n-is-odd-nu
- B: non-triviality-of-heegner-points-implies-the-rank-pa
- relation: split_link
- role difference: algebraic: GZ used to convert Kolyvagin-class nonvanishing into analytic nonvanishing (converse direction); analytic: GZ+Kolyvagin used as the established forward route whose missing input (non-trivial Heegner point) is proved
- reason: AL1 Corollary 8.3.6 invokes 'kappa(1,1) is the Kummer image of the classical Heegner point together with the Gross-Zagier theorem' to close the rank-1 converse; AN1 cites [GZ86]+[Kol90] as the established route by which a non-trivial Heegner point yields the rank part of BSD for E_p, then supplies the non-trivial point via DV17. Both lean on the same cited GZ+Kolyvagin route, but one uses it as the capstone identification in a converse theorem, the other as the off-the-shelf engine whose input (the point) is what the paper proves.

## A7-03 — SPLIT (algebraic-analytic) · seed S1
- A: kolyvagin-classes-c-m-in-h-1-k-t-f-i-m-constructed-f
- B: dv17-prop-5-2-8-the-heegner-point-r-has-infinite-ord
- relation: split_link
- role difference: algebraic: Heegner points as construction material for a Kolyvagin system of cohomology classes (Selmer control); analytic: a single non-torsion Heegner point as the seed input to the GZ height computation
- reason: Same raw material (Heegner points on Shimura curves), different machinery: AL1 builds a whole Kolyvagin system {c(m)} of cohomology classes from Heegner points of varying conductor to bound Selmer groups; AN1 needs one non-torsion Heegner point R (from DV17) as the seed whose height the explicit GZ formula evaluates. One point vs a system of classes.

## A7-04 — SPLIT (algebraic-analytic)
- A: lemma-5-1-sel-m-a-f-formula-from-sel-sel-and-the-m-t
- B: proposition-2-6-4-greenberg-wiles-formula-sel-f-a-se
- relation: split_link
- role difference: analytic: explicit 3-Selmer dimension computation for specific curves to settle a BSD 3-part; algebraic: general Selmer-structure machinery (Greenberg-Wiles) controlling Selmer ranks en route to the converse theorem
- reason: Both are Selmer-group size formulas, but at different levels of generality and purpose: AN1 Lemma 5.1 is a concrete 3-isogeny Selmer-dimension formula used with Sat86 data to pin dim Sel_3(E_p)=1 / Sel_3(E_{3p^2})=0 (the 3-part of BSD); AL1's Greenberg-Wiles formula is the general local-global Selmer Euler-characteristic machinery that the whole patched Kolyvagin-system argument stands on.

## A7-05 — SPLIT (algebraic-analytic)
- A: cm-point-p-0-1-on-x-0-defined-over-the-ring-class-fi
- B: space-of-k-cm-points-c-n-n-cm-map-to-the-shimura-cur
- relation: split_link
- role difference: analytic: CM point as the Heegner cycle whose height is the GZ formula's output (L-value bridge); algebraic: CM points as the raw material of Kolyvagin classes in cohomology (Selmer bridge)
- reason: Both papers place CM/Heegner points on Shimura curves (Shimura reciprocity appears on both sides), but the points play different mathematical roles: AN1's CM point P_0 is the Heegner cycle whose canonical height the explicit GZ formula evaluates against L-values; AL1's CM points are the construction material for Kolyvagin cohomology classes. Same geometric object, disjoint mathematical roles.

## A7-06 — REJECTED (algebraic-analytic)
- A: the-birch-and-swinnerton-dyer-conjecture-implies
- B: birch-and-swinnerton-dyer-conjecture-r-a-q-ord-s-1-l
- reason: Shared name only. AN1 proves instances of BSD (the 3-part for E_p/E_{3p^2}) and notes BSD implies the Sylvester conjecture; AL1 states BSD as background and explicitly does not use it as an input. No shared referent work, no shared curve, no shared argument.

## A7-07 — SPLIT (analytic-computational)
- A: lemma-5-1-sel-m-a-f-formula-from-sel-sel-and-the-m-t
- B: selmer-exact-sequence-0-e-q-ne-q-s-n-e-q-sha-e-q-n-0
- relation: split_link
- role difference: computational: the general n-descent Selmer exact sequence as the organizing framework of point-finding (Selmer elements as coverings, Sha as the obstruction); analytic: a specific 3-isogeny Selmer-size formula used to compute the 3-part of BSD for E_p/E_{3p^2}
- reason: C1's exact sequence 0->E(Q)/nE(Q)->S^(n)(E/Q)->Sha(E/Q)[n]->0 is the general n-descent framework (reframed classical material) that organizes the whole point-finding enterprise; AN1's Lemma 5.1 is a specific 3-isogeny Selmer-dimension formula derived from it for the E_p family. General framework vs its specialization to a computed case.

## A7-08 — REJECTED (analytic-computational)
- A: theorem-1-3-full-bsd-l-part-for-e-p-for-every-prime-
- B: every-elliptic-curve-of-prime-conductor-in-the-stein
- reason: Both invoke BSD, but on disjoint curves with disjoint roles: AN1 proves the full BSD l-part / 3-part for the specific families E_p, E_{3p^2}; C1 computationally verifies that Stein-Watkins prime-conductor curves have rank at least the BSD-predicted rank. Shared conjecture name, no shared referent.

## A7-09 — SPLIT (analytic-computational)
- A: theorem-4-3-explicit-gross-zagier-l-1-e-p-l-1-e-3p2-
- B: nine-explicit-mordell-weil-generators-for-e-u-q-t-wi
- relation: split_link
- role difference: analytic: canonical height computed through GZ as the bridge from Heegner points to L-values; computational: canonical height pairing (regulator) used to certify independence of explicitly found generators
- reason: The canonical (Neron-Tate) height is genuinely the same mathematical object on both sides, used in opposite directions: AN1 computes h_Q(R_1) via the explicit GZ formula as the bridge from the Heegner point to L-values (height as L-value proxy); C2 computes the Gram matrix of canonical height pairings as the regulator certifying that found generators are independent (height as linear-independence certificate). Same object, mirrored roles.

## A7-10 — REJECTED (analytic-computational)
- A: birch-and-swinnerton-dyer-conjecture-linking-large-r
- B: rank-z-e-p-q-ord-s-1-l-s-e-p-1-and-rank-z-e-3p2-q-or
- reason: Shared BSD name only. C2 uses BSD heuristically ('suggests') to motivate the Mestre-Nagao-style score S(t,B) that guides rank-record search; AN1 proves rank_Z = ord_{s=1} for E_p/E_{3p^2} via GZ+Kolyvagin. Heuristic search guidance vs proved theorem.

## A7-11 — SPLIT (algebraic-computational)
- A: proposition-2-6-4-greenberg-wiles-formula-sel-f-a-se
- B: selmer-exact-sequence-0-e-q-ne-q-s-n-e-q-sha-e-q-n-0
- relation: split_link
- role difference: computational: Selmer groups computed explicitly via n-descent to find points and expose Sha; algebraic: Selmer groups controlled structurally via Kolyvagin systems to bound ranks (converse theorem)
- reason: Both sides center Selmer groups, but with opposite intent: C1 computes n-Selmer groups explicitly (via n-descent) to produce rational points and bound Sha; AL1 controls Selmer groups abstractly via patched Kolyvagin systems to bound ranks and prove the converse theorem. Determination vs control.

## A7-12 — SPLIT (within-computational) · seed S2
- A: fisher-2-power-isogeny-selmer-rank-bounds-via-magma-
- B: implementation-in-magma-of-6-descent-and-12-descent
- relation: split_link
- role difference: c2: consumes Fisher's 2-power isogeny Selmer-bound machinery as a subroutine in rank-record search; c1: develops 6/12-descent as new point-finding machinery for BSD-verification on the Stein-Watkins database
- reason: Documented lineage: C2 explicitly uses 'Fisher's 2-power isogeny Selmer machinery via Magma TwoPowerIsogenyDescentRankBound [13]' as a subroutine for rank bounds in record search; C1 is Fisher developing 6/12-descent to find missing generators in the Stein-Watkins database. Same author lineage, adjacent but distinct machinery (2-power isogeny bounds vs 6/12-descent point-finding); different papers, different purposes. S2 positive control resolves as split_link.

## A7-13 — REJECTED (algebraic-computational)
- A: birch-and-swinnerton-dyer-conjecture-r-a-q-ord-s-1-l
- B: every-elliptic-curve-of-prime-conductor-in-the-stein
- reason: Shared BSD name only. AL1 states BSD as background (explicitly not used as input); C1 tests BSD's rank prediction computationally on the Stein-Watkins database. No shared referent.

## A7-14 — MISSED (algebraic-computational)
- A: proposition-6-1-5-kappa-bar-lambda-bar-is-a-nontrivi
- B: implementation-in-magma-of-6-descent-and-12-descent
- reason: Kolyvagin's original program is philosophically a descent on Selmer groups, so a conceptual kinship with n-descent exists, but neither paper engages the other's machinery and no reviewed candidate pair shares a referent (Kolyvagin classes vs n-covering curves). Recorded as missed, not rejected: the link is plausible in the literature but not evidenced in these extractions.

## A7-15 — RESOLVED (within-computational)
- A: every-elliptic-curve-of-prime-conductor-in-the-stein
- B: every-curve-of-prime-conductor-in-the-stein-watkins-
- relation: merge
- reason: Pass-1 merge (reviewed): the same main application result — every prime-conductor curve in the Stein-Watkins database has rank at least the BSD-predicted rank — stated in the introduction (c1_p1, c15) and restated in the conclusion (c1_p7, c9). Same scope, same status (computationally_verified). Keep the p1 node; fold the p7 node.
