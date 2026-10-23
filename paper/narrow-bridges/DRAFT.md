# Narrow Bridges: Mapping the Walls Between Fields of Knowledge

**Draft** — 2026-10-07/08. Status: *draft for review* (conjectural
framing on the author's part; the results reported carry their own
labels below). Every claim in this paper carries exactly one
epistemic label: **exact theorem**, **computationally verified**,
**conjectural**, or **heuristic**. Labels are stated where the claim
is made.

---

## Abstract

We report nine runs of a knowledge-mapping instrument ("atlas")
that extracts the concepts of two or more bodies of knowledge
independently and blind, then adjudicates where they touch. Across
runs in analytic number theory, the Riemann Hypothesis literature,
the Birch–Swinnerton-Dyer literature, the history of AI, prime
distribution, and market data, the measured pattern is: knowledge
is dense within each field and nearly disconnected between
fields; contacts are almost always *splits* (same referent,
different epistemic role), never merges; and the load-bearing
contacts sit on narrow, named bridges. We call this the **wall
thesis**: the difficulty of hard problems is disjointness, not
disagreement. One run (market data) returned the polar-opposite
outcome — interweave, not walls — and is reported in full. Four
candidate novel structural results in prime distribution were
computationally verified against an executable sieve; zero were
refuted.

---

## 1. Introduction

Knowledge is dense inside each field and nearly disconnected between
fields. This paper reports nine runs of a mapping instrument that
tests that sentence as a measurement, not a metaphor.

The instrument — we call each run an *atlas* — maps two or more
bodies of knowledge independently, without letting either side see
the other, and then asks where they touch. It records every touch as
one of four verdicts: *merge* (same claim, same epistemic level —
they are one thing), *split_link* (same referent, different role or
epistemic level — they touch but are not one thing), *rejected*
(shared words or names, not a shared referent), or *missed*
(plausible link absent from the extractions, recorded as absence,
not as a negative).

Across the runs reported here, the same pattern repeats
(computationally verified, per-run): the skies are dense within and
barely touch between, and where they do touch, the contact is almost
always a split — same object, different role — never a merge. We
call this the **wall thesis**: the difficulty of hard problems is
disjointness, not disagreement. And where the wall admits a
passage, it is always narrow — one named bridge, sometimes one
classical formula — and the breakthroughs sit on it.

The instrument also reported against the thesis once. That run is
included, because an instrument that only finds what it looks for
is not an instrument.

## 2. Method

The pipeline is the same in every run (exact, per the run
charters and scripts in `corpus_runs/atlas*/`):

1. **Chunk.** Each source text is sliced into ~2.5k-word windows.
2. **Extract.** Independent drafter agents extract concepts,
   claims, and relations from each chunk, each in the source's own
   vocabulary, each carrying an epistemic label. Drafters are
   *blind*: no drafter on one side ever sees the other side's text
   or extractions.
3. **Merge.** Within-side merge canonicalizes identities, reviewed
   by the coordinator. Over-merging is treated as worse than
   under-merging; disputed cases are split, not forced.
4. **Adjudicate.** Cross-side candidate pairs are reviewed
   individually and adjudicated to merge, split_link, rejected, or
   missed, with the role-difference named on every split.
5. **Grade.** A grading packet is prepared — sampled
   concept/claim/status triples plus *all* adjudications —
   for independent review. User grading is still pending on
   several runs (conjectural status of the packets' final
   verdicts is recorded honestly; see §7).

Three methodological rules are non-negotiable:

- **Triadic forks.** At each decision, the claim is tested
  alongside its polar opposite and a null (control). The
  polar-opposite leg is load-bearing: without it you learn "it
  works"; with it you learn *what* works.
- **Positive controls.** Every run seeds pairs known to touch
  (e.g., a citation the literature documents). A run whose
  controls fail is a failed run, not a narrow map.
- **The dead-end ledger.** Dead ends are recorded permanently,
  never deleted, never re-dug. Adjudications are permanent the
  same way.

- **The dead-end ledger.** Dead ends are recorded permanently,
  never deleted, never re-dug. Adjudications are permanent the
  same way. A rejection with a reason is a result: it says *these
  two things share a name, not a referent*, and no future run
  needs to ask again.

The pipeline's discipline is borrowed from the subject it was
first built to study. A sieve never tests for primality — it
eliminates what is composite, and what remains is prime. The
decision procedure behind the atlas never argues for a truth — it
eliminates what is false, and what remains is the verdict. The
method and the subject are the same shape; that is not offered as
a metaphor but as the reason the method was trusted on this
subject first.

The instrument does not originate claims and does not make
decisions. It maps what is there and labels how well each piece
is known. The map is not the proof; it is the ground the proof
would walk.

## 3. Results I: the walls

The five runs in this section tested the same structural
prediction in different territories: two independently-developed
bodies of knowledge, mapped blind, will show dense internal
structure and narrow or zero contact between them. The prediction
was logged blind in the project's prediction ledger before the
runs (ledger items 3 and 4: the first blind, the second with the
router's probability stated pre-result at 0.775 against the
instrument's own 0.70 — the scoring is still open, the
probabilities on the record).

### 3.1. The literature against the program (Atlas-2)

The first foreign-contact run held 7 obtained analytic-number-theory
papers (1 dropped and recorded after 5 exhausted retrieval routes)
against the pilot atlas of an independent research program: 521
foreign concepts against 305 home nodes, both extracted blind
(computationally verified per the run's manifests).

The verdict: **13 adjudicated links — 2 genuine merges, 10
split_links, 1 correctly-unresolved; 0 false merges, 0
contradictions.** The mechanical first pass found nothing
(0/521 — expected, since vocabularies differ by design); the
reviewed pass adjudicated 13 from 310 candidates.

The two genuine merges are load-bearing evidence the instrument
merges when warranted: Deninger's exact Theorem 6.1 and the
transversal index equation merged with the program's nodes at the
same epistemic level — same theorem, same level, provenance on
both sides. Everything else that touched was split, and the splits
are all of one shape: the paper states the theorem; the program
holds a verdict *about* the theorem, a reimplementation *of* it,
or an analysis *of its data*. Theorem vs verdict-on-theorem. Merging
those would be the category error the labels exist to prevent.

One seeded intersection was *correctly unresolved*: Lamzouri's
exact theorem on the proportion of simple zeros had no
corresponding subject in the program's atlas, and the merge
refused to invent a resolution. A non-resolution, recorded as
such, is a pass — the instrument declines to connect what is not
connected.

The router's read of this run (his words): the two sides barely
touching *is* the wall resisting proof of the Riemann Hypothesis —
disjointness, not disagreement. That reading is his (conjectural
as a general claim); the counts are the instrument's
(computationally verified per the run's manifests).

### 3.2. The constellations around RH (Atlas-5)

Three analytic skies were drawn around the Riemann Hypothesis —
computation (109 concepts), proportion (91), density (75) — and
held against the program's relational sky (305 nodes, read-only),
275 concepts total across 6 papers, all paper IDs verified live
(computationally verified).

The analytic skies barely touch each other: **one genuine link**
(computation↔density, via explicit zero-density estimates); the
other two pairs share only the topic of RH, not a referent
(rejected with reasons). Both positive controls resolved.

The wall holds **with exactly one crack**: a single
analytic↔relational link — Weil's explicit formula / Weil
positivity, invoked by name on both sides (the Alpöge–Furman
preprint as the analytic engine of its 2/3 bound; the pilot as a
computed face-sum verification). Same named classical referent,
different constructions, different epistemic levels — hence
split_link, not merge. One link across 309 candidates. The receipt
reads: the relational floor the program exhibits is, with one
classical exception, invisible to the analytic literature standing
on it. RH remains a receipt, not the goal.

Deliberately *not* linked, though tempting: GUE universality —
a shared framework, not a shared referent, and linking it would
have been the inflation the wall test exists to prevent. The
rejection is recorded with its reason.

### 3.3. The skies around Birch–Swinnerton-Dyer (Atlas-7)

Three skies — analytic (explicit Gross–Zagier), algebraic
(Kolyvagin/patches Euler systems), computational (descent
machinery, rank records) — 374 concepts across 4 papers, all
obtained first-try (computationally verified).

The verdict: **the wall is real, and the crack is exactly the
conjecture's own bridge.** The analytic and algebraic skies touch
five times — the most contact of any run — but every touch runs
through the single load-bearing bridge BSD itself names:
Gross–Zagier + Kolyvagin converting Heegner-point nonvanishing
into rank = analytic order. All 9 cross-sky links are splits, 0
are merges (1 within-side merge; 4 rejected; 1 recorded miss).
The two sides share objects — the GZ formula, Heegner points,
Selmer groups, the canonical height — but never the same *role*
for them: the analytic side *produces* explicit formulas; the
algebraic side *consumes* cited ones. BSD itself is invoked in
four different roles and rejected as a link everywhere — it is
the subject, not a bridge. The computational floor barely touches
the theoretical skies: rank records and verification computations
live on a different floor from the GZ/Kolyvagin core. Both
controls resolved.

The map's reading of BSD's difficulty: not that its skies
disagree, but that its one genuine bridge is traversed in opposite
directions by the two sides — and the upgrades a proof route
would need are written on the split_links.

### 3.4. The archeology of AI (Atlas-4)

Four traditions of AI's own history — symbolic, connectionist,
statistical, neuroscience — plus the LeCun-1989 bridge paper: 106
concepts (computationally verified).

**Zero direct sky↔sky links.** The vocabularies are disjoint the
way Atlas-3's algebra↔geometry run was (0 direct links, 1
bridge↔algebra split, one control void on a mis-seeded geometry).
The only cross-tradition links are **4 split_links, all touching
the bridge**. Both positive controls resolved cleanly — unlike
Atlas-3's, no control was void, so the instrument's silence
between the skies is a measurement, not a malfunction.

The symbolic sky is the starkest finding and the starkest caveat:
zero candidates of any kind against all four other skies — the
deepest disjointness in the run, or an artifact of sampling one
proposal paper. Recorded as both.

### The pattern (computationally verified across runs)

| Run | Skies | Direct links | Merges | Splits |
|---|---|---|---|---|
| Atlas-2 | literature ↔ program | 13 adjudicated | 2 | 10 |
| Atlas-3 | algebra ↔ geometry | 0 | 0 | 0 (1 on bridge) |
| Atlas-4 | 4 AI traditions | 0 | 0 | 0 (4 on bridge) |
| Atlas-5 | 3 analytic + relational | 2 | 0 | 2 |
| Atlas-7 | analytic ↔ algebraic ↔ computational | 9 | 0 | 9 |

Dense within; nearly disconnected between; the contacts that
exist are splits with named role-differences, and the load-bearing
ones sit on named bridges. The polar-opposite leg of the thesis —
skies that merge freely, bridges everywhere — did not occur in
any of these runs.

## 4. Results II: the cracks

A wall with no passages is a curiosity. The instrument hunts the
passages: every place the skies touch on the same object is asked
whether one side holds something the other does not state. Each
unstated touch is a *crack candidate*, verified or refuted against
ground truth where ground truth exists.

### 4.1. The Weil bridge, drawn not walked (Atlas-6)

Atlas-5's single crack was re-examined under focused blind
re-extraction. The seed **reproduces**: AF's Hermitian form ↔ the
pilot's Guinand–Weil formula, split_link. Around it, 8 further
split_links chart the bridge's anatomy — 9 named role-differences
total, 0 merges, 0 contradictions, 4 candidates rejected with
reasons (117 nodes; Weil 1952 itself unobtainable behind access
walls, triangulated through citations).

The bridge is real and narrow: one shared classical referent,
nine role-differentiated touches. Every link is split because the
two sides invoke the same named objects for different purposes at
different epistemic levels — cited criterion vs proved
strengthening, proof-lemma vs computational program, cited lineage
vs independent derivation. **A proof route would have to walk the
split_links, upgrading each cited role to a proved one — and the
map names exactly which upgrades are needed.** The standing
division is explicit: the map, not the proof.

### 4.2. Four verified cracks in prime distribution (Atlas-8)

The instrument was turned on prime numbers directly: 6 landmark
papers (PNT, Cramér, Zhang, Maynard, Green–Tao, sieve lineage)
against the program's circle-sieve sky — 345 concepts (212 foreign,
133 home, including 39 span-first concepts treating gaps as
first-class), 11 split_links, 2 rejected, 0 merges; the positive
control resolved (computationally verified). The crack-hunt
question, asked of every adjudicated link: *does the literature
state what the sieve side holds here?* Every unstated touch is a
crack candidate — verified or refuted against the sieve
implementation where the implementation can decide, marked
undecidable where it cannot.

Five crack candidates; **4 verified, 0 refuted, 1 undecidable**
(truncated source). Each verified against rerunnable scripts with
captured outputs:

- **K8-1 — PNT as total weight 1** (computationally verified):
  Σ(−1)^{|S|+1} log(∏S)/∏S → 1 *is* PNT — the face-sum
  formulation of the Prime Number Theorem. The theorem is
  classical; the formulation appears new (the pilot's
  framing-novelty claim, searched 2026-09-30).
- **K8-2 — admissibility derived, not stipulated**
  (computationally verified): the literature *stipulates*
  admissible tuples as input hypotheses; the deformed sieve
  *produces* the admissible constellations as output, the
  obstruction emerging uninserted — 342/342 twin lowers ≤20000
  match brute force; the sole triple (3,5,7) below 10⁵.
- **K8-3 — the twin constant as renormalized sieve weight**
  (computationally verified): the Hardy–Littlewood constant
  2C₂ = 1.32032… derived as the renormalized total weight of the
  deformed sieve (S(1000) = 1.320491). The constant is classical
  (1923); the generative derivation appears new. The twin-prime
  asymptotic itself stays explicitly unclaimed.
- **K8-4 — the circle sieve as independent construction**
  (exact): geometric shared-boundary sifting, built without the
  literature; unshared points coincide with the classical primes
  at N = 30…10000. A provenance claim, verified — not a new
  theorem about primes.
- **K8-5 — Selberg λ² face form** (undecidable): the source chunk
  is truncated mid-derivation; honestly undecidable, not a
  candidate until the derivation is recovered.

All four verified cracks are the same shape: the literature and
the sieve touch on the same objects, and at every touch the sieve
holds something the literature does not state — a framing, a
generative account, a derivation, an independent construction.
None is a new theorem about primes. Each is a candidate novel
result about the *structure*.

### 4.3. Interweave, not walls (Atlas-9) — the instrument reports against the thesis

The first quantitative-sky run mapped the market three ways —
tape (43 concepts, FRED + Nasdaq API, fixed 2-year window),
fundamentals (126), narrative (48) — with pre-registered
procedures and tape drafters blind to the text skies
(computationally verified).

**The verdict is the polar opposite of the thesis: interweave,
not walls.** Nine adjudicated cross-sky links, every one a
split_link, zero merges. The tape measured what the text skies
prove and document: the earnings-announcement price response
verified at 1.88× baseline moves across 23 verified earnings
dates; volume spikes, realized volatility, overnight adjustment,
post-event drift, cross-firm transmission, the information→prices
object — each touching across skies with named role-differences.
Three of four crack candidates verified against the tape
(earnings-window elevation; volume-spike next-day structure;
overnight gap-fill — including NVDA's entire two-year drift
arriving overnight, a window fact neither text sky states); the
fourth is honestly undecidable (no news dates in the tape).

The most load-bearing finding is a *tension*, not a link: both
text skies ask how information enters prices and give opposite
answers — fast public impounding vs slow private diffusion. The
instrument surfaces it without resolving it. The thinnest pair is
tape↔narrative, where the wall is incommensurable measurement,
not disagreement.

This run is why the thesis is stated as a measurement with a
counterexample on record, not as a law. An instrument that only
finds walls would be a wall-finder, not a map.

The run also stress-tested the instrument's first quantitative
sky: tape drafters followed procedures written before seeing any
data, blind to the text skies' vocabularies, and every crack was
verified against the fixed tape rather than asserted from the
literature. The adaptation graded B+/A− on the coordinator's
honest assessment — sound pipeline, with the load-bearing gap
identified (event dates must be in the tape universe from the
start of the next run). The method section of this paper
describes the text pipeline; the quantitative adaptation is
documented in the Atlas-9 report and is not claimed as settled
method here.

## 5. Discussion

**What would falsify the wall thesis.** Stated as a measurement,
the thesis is falsifiable per run: a run in which two
independently-developed skies merge freely — many genuine merges,
contradictions from overlapping claims, controls resolving as
merges rather than splits — would count against it, and Atlas-9
counts weakly in that direction already (interweave without
merges). The thesis predicts that such runs will be the
exception; nine runs are not enough to promote that prediction
past conjectural. The ledger exists to keep the score honestly:
predictions are logged before results, with probabilities, blind
where possible.

**What walls mean for hard problems.** In every run, the
difficulty sits where the skies don't touch — not in
contradiction (0 contradictions across all runs) but in
disjointness. The Riemann Hypothesis literature's three analytic
approaches share a topic, barely a referent. BSD's two sides
share objects but never roles. AI's founding schools share
neither. If this pattern generalizes (conjectural — nine runs
do not make a law), then the standard image of a hard problem as
a fortress to be stormed is wrong; it is a set of islands with
no ferry service, and the work is bridge-building, not
siege.

**The map vs. the proof.** Atlas-6 and Atlas-7 draw the same
division from opposite sides: the map names the upgrades; the
proof is the walking. The instrument refuses the proof's job
and the proof's credit alike. This is a feature: a map that
tried to prove would stop being a map. Concretely, the nine
split_links of the Weil bridge (Atlas-6) are a worklist — each
one says which cited role must become a proved role — and the
same holds for the nine BSD splits (Atlas-7). The instrument
cannot walk them; it can only draw them so precisely that the
walking is well-defined.

**Why the splits matter more than the merges.** A merge says two
sides already agree — it adds no information beyond
corroboration. A split says they invoke the same object for
different purposes at different epistemic levels, and it names
the difference. The split is where the work lives: every
Atlas-8 crack is a split whose role-difference turned out to
hide something one side never stated. The instrument's output is
not a consensus map; it is a *difference* map, and the
differences are the findings.

**The appreciating asset.** Every sky mapped enriches every
future crossing: each new run is checked against all previous
adjudications, and dead ends are never re-dug. The value of the
atlas grows with use — not as a metaphor (heuristic), but as a
counted property of the record: each run's candidates are
screened against every prior run's rejections and misses.

**The market run's lesson.** Value is relational all the way
down — a price is a relation between two things, and the
financial system is relations built on relations. The atlas maps
relations and never asks what a thing is worth in itself; that
is why the market was its most native test, and why the
interweave finding has the shape it does: value living in the
connections, exactly as the relational view predicts.

**What the instrument is not.** It does not originate (every
concept is extracted from a source, every candidate from a
pair); it does not decide (the human router holds all utility
judgments — the machine proposes, the router approves); it does
not forecast (a map of the territory is not a forecast of the
weather — Atlas-9's standing boundary is that it is a mapping
run, not investment advice).

## 6. Honest limits

1. **Pilot scale throughout.** The largest run holds 521 foreign
   concepts; the smallest, 106. Nothing here generalizes to a
   field, let alone to knowledge. The wall thesis is a measured
   pattern across nine runs, labeled conjectural as a general
   claim.
2. **Coordinator adjudication.** The reviewed pass was done by
   the run coordinator, not a separate blind adjudicator. The
   pre-registered positive controls are the method check — they
   resolved in every run — which is evidence the step worked,
   not proof it is unbiased.
3. **User grading pending.** Grading packets are prepared for
   all runs; independent review is still pending on several.
   Any verdict the packets revise is revised on the record.
4. **Retrieval gaps.** BK2011 drops are recorded per run (Berry–
   Keating 2011, Weil 1952, Stooq, Yahoo); each drop narrows
   what the run could have seen, and each is on the record
   rather than silently absorbed.
5. **The polar-opposite outcomes that didn't occur.** No run
   produced free merging, contradiction spikes, or control
   failures. A skeptic should note the instrument's designers
   also built its honesty checks — the checks are pre-registered
   precisely so this worry is answerable, not so it disappears.
6. **Cost is estimated, not metered.** Token figures throughout
   the run reports are labeled estimates; no dollar figures are
   claimed.
7. **Authorship and provenance.** The relational/home skies
   derive from one independent researcher's program; the
   instrument's builders are not neutral about the subject.
   Blind discipline and pre-registration are the answer offered;
   the reader judges whether it suffices.
8. **The Atlas-3 control failure.** One positive control in the
   nine runs was void — Atlas-3's S2, mis-seeded on the wrong
   geometry by a coordinator design error. The run is reported
   with the void marked, not repaired after the fact; the
   follow-up (re-seeded S2 plus the originally intended
   analytics↔geometry mapping) is queued, not claimed. A
   methods paper that hid its voided control would not deserve
   the reader's trust on the eight that resolved.

---

*Evidence: `corpus_runs/atlas*/` (charters, reports, grading
packets, money views), `prime-sieve-geometry/NOVEL_DERIVATIONS.md`,
`corpus_runs/atlas8/verification/` (rerunnable scripts + captured
outputs), `prediction_ledger/ledger.csv`, `prime-sieve-geometry/
METHODOLOGY.md`. [NEEDS SOURCE]: none — all figures above are
taken from the cited run reports; any figure the reader cannot
find there is an error in this draft, to be corrected on the
record.*
