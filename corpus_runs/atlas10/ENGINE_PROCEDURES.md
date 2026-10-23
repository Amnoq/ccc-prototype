# Atlas-10 Engine Procedures (PRE-REGISTERED)

**Date:** 2026-10-07
**Status:** written BEFORE any engine analysis was run. No procedure
may be added, removed, or re-parameterized after analysis output is
seen. If a procedure cannot run, record the concept as absent — do
not substitute.
**Engine:** Stockfish 17.1 (UCI), binary at
`corpus_runs/atlas10/bin/stockfish`, driven via python-chess.

## Fixed analysis set

**Games** (clean PGNs in `engine_corpus/`, extracted from the Blue
Book PGN supplement, annotations stripped):
- G1: Lasker–Tarrasch (Blue Book game 70)
- G2: Zukertort–Steinitz (Blue Book game 84)
- G3: Morphy–Anderssen (Blue Book game 18)
- G4: Anderssen–Morphy (Blue Book game 24)

**Theoretical positions** (FENs in `engine_corpus/positions.fen`):
- F1: `8/8/8/8/3N4/8/8/k1K4B w - - 0 1`
  (K+B+N vs K — Capablanca ch. 15 subject)
- F2: `8/8/8/8/8/1Q6/8/k1K5 w - - 0 1`
  (K+Q vs K — Capablanca ch. 1 subject)
- F3: `8/8/8/8/8/1R6/8/k1K5 w - - 0 1`
  (K+R vs K — Capablanca ch. 1 subject)

## Blindness

The engine drafter NEVER reads the theory or annotation texts, the
charter's literature discussion, or any chess vocabulary beyond what
these procedures name. Labels are structural and neutral:
"eval-swing event", "played-move rank divergence",
"forced-deterioration structure", "conversion failure". NEVER
"blunder", "brilliant", "novelty", "zugzwang", "fortress",
"winning", "lost" as labels (outcome classes below are engine
readouts, reported as numbers).

## Procedures

**E1 — Game evaluation profiles (G1–G4).**
For every position (initial + after each half-move): MultiPV=3,
depth=20. Record per position: best eval in cp white-relative
(mate scored as ±100000), PV1 move (UCI), played move's rank among
the 3 PVs (1/2/3/>3 by UCI match), played move's eval loss in cp
from the mover's perspective = best_eval_mover − played_eval_mover
(if rank >3: loss ≥ best − 3rd-best, recorded as lower bound).
Extract per game: max single-move swing (|eval_after − eval_before|,
white-relative, cp); the list of "eval-swing events" (swing > 100cp)
with move numbers; result vs sign-of-final-eval agreement (1/0).

**E2 — Played-move divergence (G1–G4, from E1 data).**
Per game: count of positions with played-move rank >3
("rank divergences"); mean eval loss of played moves (cp);
the 3 largest-loss moves with FENs. kind: result.

**E3 — Theoretical positions (F1–F3).**
Single PV, depth=24. Record: outcome class — `mate-in-N` (N for the
strong side) or `cp <value>` white-relative. kind: result.

**E4 — Endgame conversion (G1–G4, from E1 data).**
Endgame segment = first position with total non-king units ≤ 10
through game end. Record eval at segment start and the game result.
"Conversion failure": eval > +200cp white-relative at any segment
position but result ≠ 1-0, or eval < −200cp but result ≠ 0-1.
Record count per game. kind: result.

**E5 — Forced-deterioration structures (G1–G4, from E1 data).**
A position qualifies iff (a) the mover's best-move eval is worse
for the mover than the previous position's eval was for that same
side by > 150cp, AND (b) the previous position's eval was within
±100cp (level before, forced loss after). Record count per game +
FENs. kind: result.

## Positive controls (pre-registered)

- **C1 (theory↔engine):** Capablanca ch. 15 ("How to mate with a
  knight and bishop") states K+B+N vs K is a forced mate within
  the fifty-move limit. E3 on F1 must report mate-in-N with N ≤ 50
  for White. RESOLVED iff so; else method failure, reported.
- **C2 (annotations↔engine):** Blue Book game 70 (Lasker–Tarrasch),
  note at 25...f6: "This move, or resigning" — the annotator's
  claim that White is winning. Engine at depth=20 on the position
  after 25...f6 must report eval ≥ +300cp white-relative or mate.
  RESOLVED iff so; else method failure, reported.

## Output schema

One JSON per engine drafter at
`corpus_runs/atlas10/extractions/engine_<id>.json`:
`concepts` ({"id","kind","label"}; kind ∈ {claim, definition, method,
result, conjecture, question}; labels in the NEUTRAL vocabulary
above), `anchors` ({"concept_id","genre","note","status"}; status ∈
{exact, computationally_verified, conjectural, heuristic, killed};
every engine number in the note; computed facts =
computationally_verified), `edges` (within-engine relations only),
`loops` (open questions, e.g. un-runnable procedures), `strands`.
Valid JSON; validate with python3 json.load. Final report: counts,
positions actually processed, any procedure that could not run.
