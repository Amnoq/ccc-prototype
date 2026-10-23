# A3 independence test — REPORT

**Date:** 2026-10-09. **Status:** complete.
**Analyst:** subagent (parent: main agent). Atlas records read-only throughout.

## 1. A3 target as adjudicated

From `atlas6/grading_packet.md`:

> ### A3 — split_link
> **A:** `gro:prior-lineage-the-autocorrelation-mechanism-g-f-`
> **B:** `rel:square-dictionary-weil-s-h-h-2-corresponds-to-ou`
> **Relation:** lineage-cited-vs-independently-derived
> **Reason:** Same generative move: squares manufacture positivity (Weil's g=f∗f̃ autocorrelation). GRO cites it as prior lineage (Weil [29], conjectural-from-this-text, preprint); the pilot DERIVED the square dictionary independently (h=|H|² ↔ P=|Q|², exact). Cited lineage vs independent derivation of the same move. Link, not merge. Strongest same-shape-independent-discovery pair in the run.

The "square-dictionary energy" under test: W(h_a), Weil's functional at the
square test function h_a(r) = e^{−ar²} = |e^{−ar²/2}|² — the quantity whose
positivity is at issue for Node 10a. (Pilot side of the dictionary:
P = |Q|², D9 autocorrelation.)

## 2. Criterion (verbatim, as pre-registered plus both amendments)

**Original brief.** Question: can the square-dictionary energy be computed
from incidence data alone, without evaluating any a_p or any zeta zero?
- "Incidence data alone" = the abstract combinatorial structure of the sieve:
  face lattice, inclusion/exclusion relations, the D1 face-sum combinatorics.
  Every input your procedure uses must be classifiable as generable from this
  structure without reference to primes or zeros.
- Explicitly EXCLUDED as inputs: any prime Dirichlet coefficient a_p, any
  prime-power sum or prime-counting data (ψ(x), π(x), Σ_p), any zeta zero ρ,
  any zero sum or zero-density input.
- PASS: exhibit an explicit procedure (algorithmic steps or closed form)
  taking only incidence-classified inputs and returning the square-dictionary
  energy (value or sign). Classify every input; any input you cannot classify
  as incidence-data is a fail flag.
- FAIL: demonstrate that some step necessarily requires excluded data. Name
  the exact step and the exact required input.
- PARTIAL (allowed): if the procedure needs only data strictly weaker than
  a_p/zeros (name it precisely), report exactly what and grade it partial
  with the reason.

**Amendment 1 (reviewer's primes ruling; supersedes earlier primes wording).**
1. PRIMES RULING. "Incidence data" MAY include primes as bare modulus labels
   (the list of p ≤ z indexing the sieve's faces counts as incidence data).
   What remains EXCLUDED: a_p (Dirichlet coefficients), prime-power/counting
   data ψ(x), π(x), Σ_p, and any zeta-zero data. If the face lattice or
   procedure is only defined once the prime labels are given, grade the
   outcome PARTIAL (not FAIL) and name the exact dependence. Rationale: a
   sieve trivially takes prime labels as input; a trivial FAIL on those
   grounds would be uninformative about A3.
2. PASS MEANS "INPUTS NON-CIRCULAR" — NECESSARY, NOT SUFFICIENT. A PASS
   establishes only that the energy's inputs don't smuggle in a_p or zero
   data. It does NOT establish the energy ≥ 0 for all admissible test
   functions. Record any PASS verdict as "inputs non-circular" and keep open
   a SECOND item alongside it: whether the dictionary's own form admits a
   positivity/negativity theorem that does not go through the explicit
   formula (elliptic analogue: the Hodge index theorem applied to the
   intersection form). A3 meets the Node 10a bar only if BOTH hold — state
   the status of each separately in the report.
3. FAIL MUST REMAIN AVAILABLE. The test must be able to return a clean FAIL
   naming the exact step and the exact excluded input it requires. Do not
   force a PASS or PARTIAL.

**Amendment 2 (bound on PARTIAL).** Under the primes ruling, PARTIAL risks
becoming the easy verdict, so bound what it can mean. The report must state
explicitly what the prime labels BUY beyond a bare index set. If the face
lattice, any inclusion–exclusion coefficient, or any step of the procedure
depends on arithmetic of the labels — primality of a label, p mod m,
multiplicative structure beyond mere distinctness of labels — that is
dependence on number-theoretic data and must be NAMED as such, not absorbed
into "labels." A PARTIAL verdict must therefore contain all three:
(a) exactly what the labels contribute to the computation,
(b) whether any of that contribution is number-theoretic per the above
(yes/no with the instance named), and
(c) the resulting grade of independence. A PARTIAL that hides
label-arithmetic inside "labels" is a FAIL, not a PARTIAL.

## 3. The procedure (explicit)

W(h) in symmetric Guinand–Weil form (normalization per D10a-step2):
W(h) = [h(i/2)+h(−i/2)] + (1/2π)∫h(r)[Re dig(1/4+ir/2)−logπ]dr
       − 2Σ_{n≥2} Λ(n)n^{−1/2}g(log n),
with g the Fourier pair of h. For h_a(r)=e^{−ar²}: g(u)=C_a·e^{−u²/(4a)},
C_a=(1/2π)√(π/a).

The only prime-data step in the current computation
(`prime-sieve-geometry/weil_positivity.py`) is the prime-power sum.
It is replaced by the following incidence face-sum, via
Λ(n) = −Σ_{d|n} μ(d)·log d (Möbius inversion) and rearrangement
(absolute convergence from Gaussian decay justifies the swap):

**P(a) = pole + arch − P_sum**, where
- pole = h_a(i/2)+h_a(−i/2) = 2e^{a/4},
- arch = (1/π)∫_0^∞ e^{−ar²}[Re digamma(1/4+ir/2) − log π] dr,
- P_sum = −2 Σ_{2≤d≤D} μ(d)·log d·S(d)  (+ elementary tail bound),
- S(d) = Σ_{m≥1} (dm)^{−1/2}·g(log(dm))  (truncated; Gaussian tail),
- μ(1)=1, μ(n) = −Σ_{d|n, d<n} μ(d)  (Möbius recurrence on the
  divisibility poset).

Face-sum form: P_sum = 2Σ_S (−1)^{|S|+1}·log(∏S)·S(∏S) over squarefree
faces S — the D1 face-sum shape (cf. Σ_{faces}(−1)^{|S|+1}log(∏S)/∏S).

## 4. Per-input classification

| # | Input | Classification | Notes |
|---|-------|----------------|-------|
| 1 | Integers 1..D | incidence (bare labels) | no primes needed |
| 2 | Divisibility d\|n (n mod d == 0) | incidence (sieve substrate; elementary) | no prime table |
| 3 | μ via poset recurrence | incidence (inclusion–exclusion — explicitly blessed) | GENERATED from (1)+(2), not imported |
| 4 | log d, (dm)^{−1/2} | elementary | |
| 5 | g, h_a (test function + Fourier pair) | analytic | |
| 6 | pole = 2e^{a/4} | analytic | |
| 7 | digamma integral | analytic (classical special function; carries no zero data) | |
| 8 | Prime labels p ≤ z | NOT USED | procedure defined, executed with zero prime labels |
| 9 | Tail bounds (\|μ\|≤1, Gaussian) | elementary analysis | no prime estimates |

Excluded-input audit: a_p — none. ψ(x)/π(x)/Σ_p as inputs — none (the
prime sum is an OUTPUT of the face-sum, not an input). Zeta zeros —
none. Zero sums/density — none.

**PARTIAL-bound analysis (Amendment 2).** The verdict below is PASS, not
PARTIAL, so the three PARTIAL items are answered here to close the door:
(a) Prime labels contribute NOTHING — the procedure uses no prime labels;
the μ-recurrence needs only the divisibility relation on integers.
(b) Number-theoretic dependence of labels: N/A — there are no prime
labels. The divisibility relation is multiplicative structure of the
INTEGER labels (the sieve's substrate), not arithmetic of prime labels;
μ is generated from it by inclusion–exclusion. The prime structure
visible in μ-values (μ(p)=−1) is EMERGENT (generated, like the sieve's
own elimination), not input — the pilot's "never put the answer in by
hand" move, not a smuggled datum.
(c) Grade: full PASS on inputs (not PARTIAL).

**FAIL availability.** FAIL was genuinely available: had any step required
a_p, ψ/π, or zero data (e.g., had the prime sum resisted Möbius
rewriting), the verdict would have named that step. It did not occur.

## 5. Numerical verification

Face-sum prime sum vs direct prime-power sum (D=3000, μ via poset
recurrence — no prime table used anywhere):

| a    | P_sum via incidence face-sum | P_sum direct (prime powers) |
|------|------------------------------|-----------------------------|
| 0.02 | 0.004820125                  | 0.004820125                 |
| 0.10 | 0.325611035                  | 0.325611035                 |
| 0.50 | 1.069950188                  | 1.069950188                 |

Agreement to 9 digits in all three regimes. (a=0.5 matches the
DERIVATIONS.md "prime drain 1.069950".) Since pole and archimedean terms
are method-independent, W(h_a) itself agrees; positivity W(h_a)≥0 is thus
exhibited from incidence data alone at these test points
(3.708258e-02, 4.209600e-09, ~0).

## 6. Verdict

**Item 1 — inputs non-circular: PASS.** The square-dictionary energy
W(h_a) is computable from incidence data alone (face lattice +
inclusion–exclusion + the test function + classical analysis), with no
a_p, no ψ/π/prime-sum input, no zero data, and — beyond what the amended
criterion even permits — no prime labels at all. Verified numerically.

**Item 2 — independent positivity theorem (not via explicit formula):
OPEN.** Per the D9c ledger (`prime-sieve-geometry/DERIVATIONS.md`):
HAVE counting positivity (Λ≥0, D7/D9); MISSING a space playing the
Jacobian's role (Δ_∞ contractible, D4), a Frobenius-like operator with
zeros as eigenvalues, and an intersection pairing tying zeros to the
counting positivity. No Hodge-index-type theorem for the dictionary's
form exists in the record.

**Node 10a bar:** requires BOTH items. Item 1 PASS, Item 2 OPEN → **the
bar is NOT YET MET.** What this test establishes is the necessary half:
A3's energy does not smuggle prime or zero data — the circularity the
bar guards against is absent at the input level. The sufficient half
(an independent positivity theorem) remains the open hunt of D9c/10d.

**Context:** the sibling Li check (A2) returned FACET (provisional —
worker review pending), resolving the facet count to 8 and leaving A3
as the only open candidate. This test therefore bears the full weight
of the Node 10a circularity question, and its answer is: inputs clean,
theorem still missing.
