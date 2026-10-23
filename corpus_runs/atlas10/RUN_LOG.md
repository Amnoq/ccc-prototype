# Atlas-10 Run Log

## 2026-10-07 — Coordinator's first decisions

**Corpus (all IDs verified live, all public-domain USA, all on disk):**
- T1 theory: Capablanca, *Chess Fundamentals* (1921), Gutenberg #33870
- T2 theory: Edward Lasker, *Chess Strategy* (1915), Gutenberg #5614
- A1 annotations: Staunton et al., *The Blue Book of Chess*,
  Gutenberg #16377 — PGN supplement, 85 games with period notes
- Engine: Stockfish 17.1 (official ubuntu-x86-64-avx2 binary,
  downloaded from GitHub releases, verified `uci` handshake),
  via python-chess 1.11.2 (pip). Binary at
  `corpus_runs/atlas10/bin/stockfish`. BK2011 satisfied:
  actually-runnable, no proxy.

**Analysis set (fixed):** G1 Lasker–Tarrasch (BB game 70, 55 ply),
G2 Zukertort–Steinitz (BB game 84, 39 ply),
G3 Morphy–Anderssen (BB game 18, 144 ply),
G4 Anderssen–Morphy (BB game 24, 88 ply); F1 KBN-vs-K, F2 KQ-vs-K,
F3 KR-vs-K (FENs in engine_corpus/positions.fen).

**Pre-registration:** ENGINE_PROCEDURES.md (E1–E5, depths 20/24)
written BEFORE any analysis. Controls grounded in passages the
coordinator read:
- C1 (theory↔engine): Capablanca ch. 15 KBN forced mate ≤ 50 moves
  → E3 on F1 must report mate-in-N ≤ 50.
- C2 (annotations↔engine): BB game 70 note at 25...f6 ("This move,
  or resigning") → depth-20 eval ≥ +300cp white or mate.

**Corpus-prep incident (caught, fixed):** v1 prep script used a
fixed 12000-char window per game and bled segments together
(headers/moves from adjacent games, illegal-SAN warnings). v2
splits on [Event boundaries, asserts PlyCount match and zero
parse errors. Also caught: F1 FEN had White to move with Black
in check (Nb3 attacked a1) — knight moved to d4.

**Fan-out:** 6 blind drafters spawned 2026-10-07 ~23:30 CDT:
theory×2 (Capablanca 2 chunks, Lasker 3 chunks), annotations×2
(games 0–42, 43–84), engine×2 (games E1/E2/E4/E5; positions E3 +
controls). Engine analysis running in background (proc_786cdefd5145).

**Next:** collect extractions → reviewed merge → adjudication →
crack hunt → verification → deliverables.

## 2026-10-08 — Runner bug caught by background run
`run_engine_analysis.py` failed: python-chess `analyse()` with
multipv=1 returns a 1-element LIST, not a dict (E3/C2 sections did
`info["score"]`). Fixed `analyse_position` to normalize single-PV
to dict. Rerun in background (proc_c21024926a60). Engine drafters
were briefed to run the script themselves only if engine_raw.json
is absent — the fixed script is what they will get.

## 2026-10-08 — Restart drain incident
VM restarted mid-run ("restart drain"): the background engine
analysis (proc_c21024926a60) was killed before writing
engine_raw.json, and both engine drafters errored the same way.
Text extractions (4 files) survived on disk — no work lost there.
python-chess had been pip-installed to system python (ephemeral)
and vanished; reinstalled into a venv at
~/workspace/ccc-prototype/.venv (persists). ENGINE_DRAFTER_BRIEF.md
updated: drafters must use the venv python. Fixed runner verified
on F1 (mate-in-2 at depth 24 — C1 will resolve) and startpos
MultiPV. Background analysis relaunched (proc_4b442b45c00e); both
engine drafters re-spawned with corrected instructions.
Annot_p2 drafter's numbering note: the Blue Book's own {PGN N}
markers are 1-based-ish and differ from my 0-based [Event indices
by ~2; game IDENTITIES were asserted via headers+PlyCount in
prep_corpus.py (g1=Lasker-Tarrasch 55 ply, C2 FEN asserted
50th half-move = f6), so the numbering offset is cosmetic only.

## 2026-10-08 — Few-legal-moves bug (caught by background run)
Second runner bug: a position with fewer than 3 legal moves makes
Stockfish return 1 PV for MultiPV=3; the strict `len == multipv`
assert fired ~30 min into the run. Fix: accept 1..multipv PVs;
the played-loss lower bound now uses the worst RETURNED PV
(recorded as `pvs_returned`). This is engine behavior, not a
re-parameterization — the procedure's divergence definition
(played move outside the engine's returned top moves) is preserved.
Relaunched (proc_880ee370aac3).

## 2026-10-08 — engine_raw.json complete (proc_880ee370aac3)
326 positions analyzed, depth 20 MultiPV 3 (games) / 24 (FENs).
Controls, pre-registered verdicts:
- C1 RESOLVED: F1 KBN-vs-K → mate-in-2 (≤ 50 required). Capablanca
  ch. 15 confirmed by the engine.
- C2 RESOLVED: game 70 after 25...f6 → mate-in-8 White (cp 99992).
  The annotator's "This move, or resigning" confirmed — White is
  mating, not merely winning.
- F2 KQ-vs-K → mate-in-1; F3 KR-vs-K → mate-in-1.
Both engine drafters were re-spawned with the fixed script path;
engine_raw.json is complete for their extraction.

## 2026-10-08 — Stale-failure re-dispatch
The re-spawned engine-games drafter (7/8's sibling) ran the UNFIXED
runner before the fix landed (it was spawned while proc_4b442b45c00e
was still on the old code), correctly diagnosed the strict-MultiPV
assert, and stopped per its brief — a correct stop on stale code.
The fix it suggested is exactly what was implemented; the full
analysis has since completed (engine_raw.json, 326 positions).
Re-dispatched the engine-games extraction with explicit instruction
NOT to re-run the script. The drafter's diagnosis is preserved
above as an honest instrument record: the method caught its own
bug twice (multipv=1 list; few-legal-moves PV count).

## 2026-10-08 — annot_p1 label repair
The annot_p1 drafter wrote "exact" (the status word) into all 150
concept LABEL fields; the real content was in the anchor notes
("G## players, move: 'judgment'"). Repaired MECHANICALLY: label =
note's context + quoted judgment (drafter's own recorded words,
truncated); original backed up as
extractions/annot_p1_raw.json. No content invented. annot_p2 was
unaffected (115 distinct labels).

## 2026-10-08 — RUN COMPLETE
All 7 charter deliverables built: ATLAS10_REPORT.md, CRACK_LIST.md,
verification/ (2 scripts + captured outputs, both exit 0),
atlas10_money.png, atlas10_interactive.html (454 nodes, 143 edges,
7 gold), grading_packet.md (93 adjudications), manifest.json.
Final: 454 concepts, 9 merges (1 weak-flagged), 0 contradictions,
93 adjudications (7 split_link / 86 rejected), C1+C2 resolved,
2/2 cracks verified, 0 drops.
Integrity incidents and their fixes: annot_p1 label repair
(mechanical, backup kept); 2 runner bugs; node-id instability
(cid-keyed stable ids + alias resolution + loud validator);
1 VM restart (no data lost).
