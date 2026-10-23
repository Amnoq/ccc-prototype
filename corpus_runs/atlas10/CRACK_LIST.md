# Atlas-10 Crack List

**Date:** 2026-10-08
**Method:** every engine↔literature touch the literature skies do not
state is a crack candidate (epistemic label: candidate), verified
against the engine via rerunnable scripts with captured output.

## K10-1 — Annotator–engine directional agreement ✅ VERIFIED

**Claim:** Across the 10 positionally-joined annotator judgments in
the analyzed Blue Book games (Lasker–Tarrasch, Zukertort–Steinitz),
the engine's move rankings never contradict the annotator's
direction: every praised/confirmed move ranks in the engine's top 3
at depth 20; no criticized move is the engine's top choice.
(9 evaluative joins; 1 note is historical rather than evaluative —
engine rank 2, no contradiction.)

**The join:**
| game | move | annotator | engine rank | loss |
|---|---|---|---|---|
| Lasker–Tarrasch | 6.Nf3 | "the best line" | 1 | 0 |
| Lasker–Tarrasch | 6...c5 | "out of place" | 4 | ≥10cp |
| Lasker–Tarrasch | 9.Qxc3 | "excellent move" | 1 | 0 |
| Lasker–Tarrasch | 12.Qd2 | "forces paralyzed" | 1 | 0 |
| Lasker–Tarrasch | 12...Qb6 | "Qc7 seems better" | 4 | ≥6cp |
| Lasker–Tarrasch | 23...Qxb2 | "not judicious" | 3 | 216cp |
| Lasker–Tarrasch | 25...f6 | "or resigning" | 4 | ≥203cp |
| Zukertort–Steinitz | 5...d5 | "ingenious attack" | 2 | 11cp |
| Zukertort–Steinitz | 20.Kc2 | "remain a piece ahead" | 3 | 24cp |

**What is novel:** the literature states the judgments; it does not
state their engine-agreement profile. The engine "knows" something
the literature doesn't: period annotations (c. 1910) are
directionally sound against Stockfish 17.1 at depth 20 — including
the subtle case 23...Qxb2, which the engine ranks 3rd yet prices at
216cp worse than best (rank ≠ quality; the annotator's "not
judicious" is about the loss, which the engine confirms).

**Label:** computationally verified — with the honest caveat that
the directional comparison is EXPLORATORY (post-hoc), not
pre-registered. The ranks and losses are pre-registered E1/E2
outputs; the praise/criticize classification rule was fixed before
the verification script ran, and the script re-runs deterministically.
**Verification:** `verification/verify_k10_1_agreement.py` (+ captured
output). Exit 0.

## K10-2 — Engine divergence profiles of the four games ✅ VERIFIED

**Claim:** played-move rank-divergence profiles (pre-registered E2),
unstated by either literature sky:
- G1 Lasker–Tarrasch: 13 divergences / 55 moves, mean loss 20.09cp
- G2 Zukertort–Steinitz: 3 / 39, mean loss 16.62cp
- G3 Morphy–Anderssen: 23 / 144, mean loss 2055.28cp (mate-scale
  endgame losses dominate)
- G4 Anderssen–Morphy: 15 / 88, mean loss 19.05cp

**What is novel:** neither the theory nor the annotations quantify
how often master play diverges from engine top-3 choice. The
profiles are engine-held structural facts about the corpus games.

**Label:** computationally verified.
**Verification:** `verification/verify_k10_2_divergence.py` (+ captured
output) recomputes all four profiles exactly from engine_raw.json.
Exit 0.

## Non-cracks (recorded, not claimed)

- **E5 null:** zero forced-deterioration structures in 326 analyzed
  positions. An honest null — the zugzwang-proxy found nothing in
  these four games. Not a crack (absence, not a touch).
- **E4 absences:** the pre-registered endgame segment (≤10 non-king
  units) never begins in G1/G2/G4 (minima 16/21/13); only G3 has a
  segment, with zero conversion failures. Recorded as a procedure
  limitation, not a finding about chess.
- **C2 strengthening** (mate-in-8 vs "winning") is folded into
  adjudication A10-02's role difference, not a separate crack.

## Tally

- Candidates: 2 · verified: 2 ✅ · refuted: 0 · undecidable: 0
