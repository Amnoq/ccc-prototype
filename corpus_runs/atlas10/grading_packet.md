# Atlas-10 Grading Packet

**Date:** 2026-10-08 · **Run:** chess atlas (theory / annotations / engine)
**Bar:** 0 false merges, 0 contradictions.
**Corpus:** Capablanca *Chess Fundamentals* (Gutenberg #33870), Lasker *Chess Strategy* (#5614), Blue Book of Chess (#16377, 85 annotated games); Stockfish 17.1, 4 games + 3 FENs.

## Controls (both resolved)

- **C1 (theory↔engine):** Capablanca ch. 15 KBN forced mate within fifty moves → engine mate-in-2. RESOLVED.
- **C2 (annotations↔engine):** Blue Book game 70 note at 25...f6 ('This move, or resigning') → engine mate-in-8 White. RESOLVED and strengthened.

## Sampled triples (12: 4 per sky)

### theory
- [theory_lasker/c74] `exact` — the middle game starts from the pawn skeleton's TRANSFORMATION
- [theory_capablanca/c9] `exact` — Ex.5 drawn: Black keeps King directly in front of the Pawn (or White King)
- [theory_lasker/c34] `exact` — decline the King's Gambit; holding it needs expert complications
- [theory_lasker/c48] `exact` — the two opening principles restated

### annotations
- [annot_p1/c8] `exact` — G01 Morphy-Boucher, 26. Rd3: And Black has no possible means of escape; for, if he play Qe8, White simply cap
- [annot_p1/c107] `exact` — G27 Philadelphia-New York (1858), 30. Re1: The first move of a combination, which gave the victory to Philadelphia.
- [annot_p2/c89] `exact` — White obliged to lose the exchange, though he fought manfully
- [annot_p2/c105] `exact` — 4.Bf4 a favorite of Harrwitz though decried by the chief authorities

### engine
- [engine_games/c9] `computationally_verified` — G4 eval profile (E1)
- [engine_positions/c4] `computationally_verified` — F3 outcome class: mate-in-1, +99999 cp white-relative
- [engine_games/c6] `computationally_verified` — G1 eval profile (E1)
- [engine_games/c2] `exact` — result/final-eval agreement rule

## ALL adjudications (93)

### A10-01 — `split_link` (CONTROL C1)
- **pair:** engine-theory
- **a:** [engine_positions/c5] `computationally_verified` — C1 control verdict: RESOLVED
- **b:** [theory_capablanca/c41] `exact` — CONTROL C1: Knight+Bishop mate must be accomplished within the fifty moves granted by the rules
- **role difference:** theory: states the KBN forced-mate rule within the fifty-move limit as teachable knowledge (Capablanca ch. 15); engine: executes the claim on a fixed FEN, reporting mate-in-2 (<= 50 required)
- **reason:** C1 CONTROL, pre-registered: the book's forced-mate claim resolves against the engine. Both verified independently before adjudication.

### A10-02 — `split_link` (CONTROL C2)
- **pair:** engine-annotations
- **a:** [engine_positions/c6] `computationally_verified` — C2 control readout and verdict: mate-in-8, +99992 cp white-relative; RESOLVED
- **b:** [annot_p2/c72] `exact` — 25...f6: this move, or resigning; there is nothing else
- **role difference:** annotations: the annotator's verdict 'this move, or resigning' on 25...f6 in Lasker-Tarrasch (Blue Book game 70); engine: depth-20 analysis of the fixed post-25...f6 FEN reporting mate-in-8 for White
- **reason:** C2 CONTROL, pre-registered: the annotator's winning claim resolves against the engine — and the engine strengthens it (mate, not merely winning).

### A10-03 — `split_link`
- **pair:** engine-theory
- **a:** [engine_positions/c3] `computationally_verified` — F2 outcome class: mate-in-1, +99999 cp white-relative
- **b:** [theory_capablanca/c6] `exact` — Queen+King vs King easiest mate: under ten moves
- **role difference:** theory: Q+K mates in under ten moves (a bound for the student); engine: mate-in-1 from the fixed FEN (the position was already terminal-adjacent)
- **reason:** Same claim (Q+K forces mate), different roles: the book teaches the bound, the engine exhibits the instance. Not a merge: the book's 'under ten' is pedagogical, the engine's 'mate in 1' is positional.

### A10-04 — `split_link`
- **pair:** engine-theory
- **a:** [engine_positions/c4] `computationally_verified` — F3 outcome class: mate-in-1, +99999 cp white-relative
- **b:** [theory_capablanca/c3] `exact` — Rook+K vs K mate in under twenty moves
- **role difference:** theory: R+K mates in under twenty moves; engine: mate-in-1 from the fixed FEN
- **reason:** Same claim, different roles, as A10-03.

### A10-05 — `split_link`
- **pair:** annotations-theory
- **a:** [annot_p1/c32] `exact` — G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in the dark. If the doubled Pawn can be dissolved betimes,
- **b:** [theory_lasker/c83] `exact` — vs the B-Kt5 pin: B-K3; the doubled pawn is no harm
- **role difference:** annotations: the doubled pawn as a weakness to 'dissolve betimes' or compensate via the open file (game-specific, conditional); theory (Lasker): the doubled pawn 'in no way detrimental' — actively advantageous via the opened file (principled, unconditional)
- **reason:** Same object (doubled pawns), genuinely different stances: the annotator treats them as a defect to manage, Lasker as an asset. Mild tension surfaced, not resolved.

### A10-06 — `split_link`
- **pair:** annotations-theory
- **a:** [annot_p2/c11] `exact` — Advance the g pawn and sacrifice the N, as in the Muzio Gambit
- **b:** [theory_lasker/c8] `exact` — 'gambit'
- **role difference:** annotations: invokes the Muzio Gambit as a concrete attacking model ('sacrifice your N, as in the Muzio'); theory: the dictionary definition ('an opening in which a pawn sacrifice is offered')
- **reason:** Same concept, different roles: the annotator uses the gambit, the theorist defines it. Thin but genuine.

### A10-07 — `split_link`
- **pair:** annotations-theory
- **a:** [annot_p2/c65] `exact` — 6.Nf3 the best line against the McCutcheon defence (Sjoberg-Giersing 1906)
- **b:** [theory_lasker/c91] `conjectural` — open theoretical questions: Ruy Lopez Diag-26 continuation; McCutcheon 5.P-K5; Aljechin's line; Caro-Kann queen-trade
- **role difference:** annotations: confident verdict — 6.Nf3 'the best line' vs the McCutcheon (citing Sjoberg-Giersing 1906); theory (Lasker): the McCutcheon 5.P-K5 verdict listed among OPEN theoretical questions
- **reason:** Same opening, different epistemic stances: the annotator asserts, the theorist leaves open. A genuine narrow bridge between confident practice and honest theory.

### A10-R00 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c10] `exact` — G02 Morphy-Harrwitz, 15...g5: Very imprudent in such a position and against such an opponent. It must be admit
- **b:** [theory_capablanca/c44] `exact` — Fifty-move rule: demand mate within fifty moves; count restarts on exchange or Pawn advance
- **reason:** Spurious token overlap (however,must,opponent); no shared referent on coordinator review of all 90 candidates. Labels: G02 Morphy-Harrwitz, 15...g5: Very imprudent in such a posit // Fifty-move rule: demand mate within fifty moves; count resta

### A10-R01 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c32] `exact` — G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in the dark. If the doubled Pawn can be dissolved betimes,
- **b:** [theory_capablanca/c14] `exact` — Bishop and Knight same theoretical value, but Bishop more valuable in most cases; two Bishops > two Knights
- **reason:** Spurious token overlap (can,file,open); no shared referent on coordinator review of all 90 candidates. Labels: G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in t // piece valuation by mobility, void when mobility is hindered

### A10-R02 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c32] `exact` — G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in the dark. If the doubled Pawn can be dissolved betimes,
- **b:** [theory_lasker/c31] `exact` — luring away the centre pawn; Rook behind the advanced pawn
- **reason:** Spurious token overlap (file,may,open); no shared referent on coordinator review of all 90 candidates. Labels: G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in t // luring away the centre pawn; Rook behind the advanced pawn

### A10-R03 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c32] `exact` — G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in the dark. If the doubled Pawn can be dissolved betimes,
- **b:** [theory_lasker/c32] `exact` — do not surrender a centre pawn without compensation
- **reason:** Spurious token overlap (attack,can,open); no shared referent on coordinator review of all 90 candidates. Labels: G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in t // do not surrender a centre pawn without compensation

### A10-R05 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c32] `exact` — G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in the dark. If the doubled Pawn can be dissolved betimes,
- **b:** [theory_lasker/c90] `exact` — missing KKtP hurts mid-game, missing QKtP hurts the ending; compensation is the open file
- **reason:** Spurious token overlap (can,file,open); no shared referent on coordinator review of all 90 candidates. Labels: G08 Tchigorin-Pillsbury, 8...Ne7: Something like a leap in t // missing KKtP hurts mid-game, missing QKtP hurts the ending; 

### A10-R06 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c36] `exact` — G08 Tchigorin-Pillsbury, 19. f3: Manifestly weakening. The Russian champion feels himself on the defensive, and a
- **b:** [theory_lasker/c53] `exact` — Queen wins vs any piece; vs Rook transfer the move
- **reason:** Spurious token overlap (any,may,other); no shared referent on coordinator review of all 90 candidates. Labels: G08 Tchigorin-Pillsbury, 19. f3: Manifestly weakening. The R // Queen wins vs any piece; vs Rook transfer the move

### A10-R07 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c37] `exact` — G08 Tchigorin-Pillsbury, 24. Nd4: Nh4 would be much stronger, the importance of halting the advancing Rook Pawn du
- **b:** [theory_lasker/c27] `exact` — only P-K4/P-Q4 free two pieces; move only necessary pawns
- **reason:** Spurious token overlap (considered,need,two); no shared referent on coordinator review of all 90 candidates. Labels: G08 Tchigorin-Pillsbury, 24. Nd4: Nh4 would be much stronger // only P-K4/P-Q4 free two pieces; move only necessary pawns

### A10-R08 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c41] `exact` — G13 Staunton-Horwitz, 21. Qf3: White designedly gives up the Queen's Pawn, to get a counter attack with his com
- **b:** [theory_lasker/c79] `exact` — pawn attacks need overwhelming concentrated force
- **reason:** Spurious token overlap (attack,counter,forces); no shared referent on coordinator review of all 90 candidates. Labels: G13 Staunton-Horwitz, 21. Qf3: White designedly gives up the // pawn attacks need overwhelming concentrated force

### A10-R09 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c41] `exact` — G13 Staunton-Horwitz, 21. Qf3: White designedly gives up the Queen's Pawn, to get a counter attack with his com
- **b:** [theory_lasker/c81] `exact` — fix a pawn by blockade or superior control; fix a piece only by a pin; then pile on
- **reason:** Spurious token overlap (attack,forces,his); no shared referent on coordinator review of all 90 candidates. Labels: G13 Staunton-Horwitz, 21. Qf3: White designedly gives up the // fix a pawn by blockade or superior control; fix a piece only

### A10-R10 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c44] `exact` — G13 Staunton-Horwitz, 26. h3: A most important move. Black dare not now advance d4 on account of Qf7+, which w
- **b:** [theory_lasker/c81] `exact` — fix a pawn by blockade or superior control; fix a piece only by a pin; then pile on
- **reason:** Spurious token overlap (double,his,rooks); no shared referent on coordinator review of all 90 candidates. Labels: G13 Staunton-Horwitz, 26. h3: A most important move. Black d // fix a pawn by blockade or superior control; fix a piece only

### A10-R11 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c44] `exact` — G13 Staunton-Horwitz, 26. h3: A most important move. Black dare not now advance d4 on account of Qf7+, which w
- **b:** [theory_lasker/c85] `exact` — opposite-wing castling: first attacker usually wins; Q-side harder to defend
- **reason:** Spurious token overlap (account,his,win); no shared referent on coordinator review of all 90 candidates. Labels: G13 Staunton-Horwitz, 26. h3: A most important move. Black d // opposite-wing castling: first attacker usually wins; Q-side 

### A10-R12 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c58] `exact` — G15 Staunton-St. Amant, 12. h3: If White play f5 at this point, his opponent may move Ng4, threatening to play a
- **b:** [theory_capablanca/c44] `exact` — Fifty-move rule: demand mate within fifty moves; count restarts on exchange or Pawn advance
- **reason:** Spurious token overlap (mate,may,opponent); no shared referent on coordinator review of all 90 candidates. Labels: G15 Staunton-St. Amant, 12. h3: If White play f5 at this poi // Fifty-move rule: demand mate within fifty moves; count resta

### A10-R13 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c58] `exact` — G15 Staunton-St. Amant, 12. h3: If White play f5 at this point, his opponent may move Ng4, threatening to play a
- **b:** [theory_lasker/c31] `exact` — luring away the centre pawn; Rook behind the advanced pawn
- **reason:** Spurious token overlap (his,may,opponent); no shared referent on coordinator review of all 90 candidates. Labels: G15 Staunton-St. Amant, 12. h3: If White play f5 at this poi // luring away the centre pawn; Rook behind the advanced pawn

### A10-R14 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c76] `exact` — G26 Lasker-Steinitz, 6...Ng6: Black's difficulty is how to dispose of the Kt. Now g6 in this instance, althoug
- **b:** [theory_lasker/c86] `exact` — open files progressively paralyse the defender until position becomes material
- **reason:** Spurious token overlap (how,lasker,now); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 6...Ng6: Black's difficulty is how to d // open files progressively paralyse the defender until positio

### A10-R15 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c78] `exact` — G26 Lasker-Steinitz, 12...Bc6: There seems little use in this move. Either he can O-O now; if not, then it is p
- **b:** [theory_lasker/c41] `exact` — Sicilian: no B-B4 (P-K3 gains a move via P-Q4)
- **reason:** Spurious token overlap (can,defence,his); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 12...Bc6: There seems little use in thi // Sicilian: no B-B4 (P-K3 gains a move via P-Q4)

### A10-R16 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c83] `exact` — G26 Lasker-Steinitz, 23. g6: One of the moves which will make this game memorable. The object is, if hxg6 to 
- **b:** [theory_capablanca/c60] `exact` — Pawns strongest side-by-side on the same rank; centre pawns strongest at K4/Q4; their advance to the 5th rank often decides the game
- **reason:** Spurious token overlap (course,one,two); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 23. g6: One of the moves which will mak // Pawns strongest side-by-side on the same rank; centre pawns 

### A10-R17 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c83] `exact` — G26 Lasker-Steinitz, 23. g6: One of the moves which will make this game memorable. The object is, if hxg6 to 
- **b:** [theory_lasker/c4] `exact` — 'opposition'
- **reason:** Spurious token overlap (file,must,one); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 23. g6: One of the moves which will mak // 'opposition'

### A10-R18 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c83] `exact` — G26 Lasker-Steinitz, 23. g6: One of the moves which will make this game memorable. The object is, if hxg6 to 
- **b:** [theory_capablanca/c14] `exact` — Bishop and Knight same theoretical value, but Bishop more valuable in most cases; two Bishops > two Knights
- **reason:** Spurious token overlap (file,open,two); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 23. g6: One of the moves which will mak // piece valuation by mobility, void when mobility is hindered

### A10-R19 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c83] `exact` — G26 Lasker-Steinitz, 23. g6: One of the moves which will make this game memorable. The object is, if hxg6 to 
- **b:** [theory_lasker/c31] `exact` — luring away the centre pawn; Rook behind the advanced pawn
- **reason:** Spurious token overlap (behind,file,open); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 23. g6: One of the moves which will mak // luring away the centre pawn; Rook behind the advanced pawn

### A10-R20 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c83] `exact` — G26 Lasker-Steinitz, 23. g6: One of the moves which will make this game memorable. The object is, if hxg6 to 
- **b:** [theory_lasker/c68] `exact` — 2B > 2Kt; Rook beats minor piece even vs 1-2 extra pawns; tear up the pawn front first
- **reason:** Spurious token overlap (must,one,two); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 23. g6: One of the moves which will mak // 2B > 2Kt; Rook beats minor piece even vs 1-2 extra pawns; te

### A10-R21 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c83] `exact` — G26 Lasker-Steinitz, 23. g6: One of the moves which will make this game memorable. The object is, if hxg6 to 
- **b:** [theory_lasker/c86] `exact` — open files progressively paralyse the defender until position becomes material
- **reason:** Spurious token overlap (gain,lasker,open,two); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 23. g6: One of the moves which will mak // open files progressively paralyse the defender until positio

### A10-R22 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c85] `exact` — G26 Lasker-Steinitz, 33. Bf5: Bf5 is evidence with what perfect lucidity Lasker detects the weak spots, and ho
- **b:** [theory_lasker/c63] `exact` — pawns behind: the advanced King usually wins, unless a weak pawn counterbalances
- **reason:** Spurious token overlap (advantage,how,weak); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 33. Bf5: Bf5 is evidence with what perf // pawns behind: the advanced King usually wins, unless a weak 

### A10-R23 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c85] `exact` — G26 Lasker-Steinitz, 33. Bf5: Bf5 is evidence with what perfect lucidity Lasker detects the weak spots, and ho
- **b:** [theory_lasker/c81] `exact` — fix a pawn by blockade or superior control; fix a piece only by a pin; then pile on
- **reason:** Spurious token overlap (his,immediately,opponent); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 33. Bf5: Bf5 is evidence with what perf // fix a pawn by blockade or superior control; fix a piece only

### A10-R24 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c85] `exact` — G26 Lasker-Steinitz, 33. Bf5: Bf5 is evidence with what perfect lucidity Lasker detects the weak spots, and ho
- **b:** [theory_lasker/c86] `exact` — open files progressively paralyse the defender until position becomes material
- **reason:** Spurious token overlap (advantage,how,lasker); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 33. Bf5: Bf5 is evidence with what perf // open files progressively paralyse the defender until positio

### A10-R25 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c88] `exact` — G26 Lasker-Steinitz, 41...Qd7: Qd7 is a final blunder. Rd7 should have been played, or Re6. The game is now ove
- **b:** [theory_lasker/c16] `exact` — victory often by timely sacrifice, compensated in position
- **reason:** Spurious token overlap (advantage,some,victory); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 41...Qd7: Qd7 is a final blunder. Rd7 s // victory often by timely sacrifice, compensated in position

### A10-R26 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c88] `exact` — G26 Lasker-Steinitz, 41...Qd7: Qd7 is a final blunder. Rd7 should have been played, or Re6. The game is now ove
- **b:** [theory_lasker/c50] `exact` — exchange into typical elementary won positions
- **reason:** Spurious token overlap (advantage,player,some,victory); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 41...Qd7: Qd7 is a final blunder. Rd7 s // exchange into typical elementary won positions

### A10-R27 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c88] `exact` — G26 Lasker-Steinitz, 41...Qd7: Qd7 is a final blunder. Rd7 should have been played, or Re6. The game is now ove
- **b:** [theory_lasker/c86] `exact` — open files progressively paralyse the defender until position becomes material
- **reason:** Spurious token overlap (advantage,gain,lasker,now); no shared referent on coordinator review of all 90 candidates. Labels: G26 Lasker-Steinitz, 41...Qd7: Qd7 is a final blunder. Rd7 s // open files progressively paralyse the defender until positio

### A10-R28 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c131] `exact` — G36 de la Bourdonnais-McDonnell, 6...exf4: In this opening it is not advisable for the second player to take the gambit P. 
- **b:** [theory_capablanca/c76] `exact` — In the opening, time is of great importance; post pieces in the right places
- **reason:** Spurious token overlap (his,opening,player); no shared referent on coordinator review of all 90 candidates. Labels: G36 de la Bourdonnais-McDonnell, 6...exf4: In this opening i // In the opening, time is of great importance; post pieces in 

### A10-R29 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_capablanca/c50] `exact` — Never carry a direct attack a outrance without absolute certainty of success; failure means disaster
- **reason:** Spurious token overlap (attack,one,own); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // Never carry a direct attack a outrance without absolute cert

### A10-R30 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_capablanca/c51] `exact` — Force of the threatened attack: hold threats in hand; demonstrate on one side, shift quickly to the other
- **reason:** Spurious token overlap (attack,forces,one,other); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // Force of the threatened attack: hold threats in hand; demons

### A10-R31 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_capablanca/c52] `exact` — Relinquishing the initiative: weather the storm after gaining material, then act quickly with all forces
- **reason:** Spurious token overlap (attack,forces,gaining); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // Relinquishing the initiative: weather the storm after gainin

### A10-R32 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_capablanca/c54] `exact` — Sudden attack from a different side: transfer the attack side-to-side via greater mobility
- **reason:** Spurious token overlap (attack,one,other); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // Sudden attack from a different side: transfer the attack sid

### A10-R33 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_capablanca/c58] `exact` — A 'hole': defect in pawn formation letting the opponent establish un-dis-lodgeable forces
- **reason:** Spurious token overlap (dislodging,forces,his); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // A 'hole': defect in pawn formation letting the opponent esta

### A10-R34 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_capablanca/c76] `exact` — In the opening, time is of great importance; post pieces in the right places
- **reason:** Spurious token overlap (his,importance,time); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // In the opening, time is of great importance; post pieces in 

### A10-R35 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_lasker/c32] `exact` — do not surrender a centre pawn without compensation
- **reason:** Spurious token overlap (attack,one,other); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // do not surrender a centre pawn without compensation

### A10-R36 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_lasker/c56] `exact` — K+P vs K: draw needs queening-square command plus first-rank opposition at the sixth
- **reason:** Spurious token overlap (his,importance,one); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // K+P vs K: draw needs queening-square command plus first-rank

### A10-R37 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_lasker/c79] `exact` — pawn attacks need overwhelming concentrated force
- **reason:** Spurious token overlap (attack,forces,might); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // pawn attacks need overwhelming concentrated force

### A10-R38 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_lasker/c81] `exact` — fix a pawn by blockade or superior control; fix a piece only by a pin; then pile on
- **reason:** Spurious token overlap (attack,forces,his); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // fix a pawn by blockade or superior control; fix a piece only

### A10-R39 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_lasker/c84] `exact` — P-R3 anti-pin moves cost time and weaken squares
- **reason:** Spurious token overlap (attack,lost,time); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // P-R3 anti-pin moves cost time and weaken squares

### A10-R40 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_lasker/c85] `exact` — opposite-wing castling: first attacker usually wins; Q-side harder to defend
- **reason:** Spurious token overlap (attack,his,one); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // opposite-wing castling: first attacker usually wins; Q-side 

### A10-R41 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p1/c143] `exact` — G40 Stanley-Rousseau, 16. Qf3: This is very finely played, and is an example to young players of the importance
- **b:** [theory_lasker/c89] `exact` — same-wing castling: answer wing weaknesses by piece pressure, not pawn pushes
- **reason:** Spurious token overlap (attack,his,one); no shared referent on coordinator review of all 90 candidates. Labels: G40 Stanley-Rousseau, 16. Qf3: This is very finely played, a // same-wing castling: answer wing weaknesses by piece pressure

### A10-R42 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c1] `exact` — Black's ingenious knight sacrifice offer (22...Nxb4)
- **b:** [theory_lasker/c32] `exact` — do not surrender a centre pawn without compensation
- **reason:** Spurious token overlap (attack,give,some); no shared referent on coordinator review of all 90 candidates. Labels: Black's ingenious knight sacrifice offer (22...Nxb4) // do not surrender a centre pawn without compensation

### A10-R43 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c1] `exact` — Black's ingenious knight sacrifice offer (22...Nxb4)
- **b:** [theory_lasker/c84] `exact` — P-R3 anti-pin moves cost time and weaken squares
- **reason:** Spurious token overlap (attack,offer,time); no shared referent on coordinator review of all 90 candidates. Labels: Black's ingenious knight sacrifice offer (22...Nxb4) // P-R3 anti-pin moves cost time and weaken squares

### A10-R44 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c11] `exact` — Advance the g pawn and sacrifice the N, as in the Muzio Gambit
- **b:** [theory_capablanca/c44] `exact` — Fifty-move rule: demand mate within fifty moves; count restarts on exchange or Pawn advance
- **reason:** Spurious token overlap (advance,you,your); no shared referent on coordinator review of all 90 candidates. Labels: Advance the g pawn and sacrifice the N, as in the Muzio Gamb // Fifty-move rule: demand mate within fifty moves; count resta

### A10-R46 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c11] `exact` — Advance the g pawn and sacrifice the N, as in the Muzio Gambit
- **b:** [theory_lasker/c64] `exact` — the isolated pawn is weaker; its defence fetters mobility
- **reason:** Spurious token overlap (can,having,protected); no shared referent on coordinator review of all 90 candidates. Labels: Advance the g pawn and sacrifice the N, as in the Muzio Gamb // the isolated pawn is weaker; its defence fetters mobility

### A10-R47 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c24] `exact` — 3.Bc4 McDonnell's favorite opening, much analyzed by him
- **b:** [theory_lasker/c84] `exact` — P-R3 anti-pin moves cost time and weaken squares
- **reason:** Spurious token overlap (attack,opening,time); no shared referent on coordinator review of all 90 candidates. Labels: 3.Bc4 McDonnell's favorite opening, much analyzed by him // P-R3 anti-pin moves cost time and weaken squares

### A10-R48 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c41] `exact` — Absolutely injurious to allow three queenside pawns against two; pawns ought to be exchanged first
- **b:** [theory_capablanca/c24] `exact` — Control of the centre of great importance; no violent attack succeeds without it
- **reason:** Spurious token overlap (attack,centre,three,two); no shared referent on coordinator review of all 90 candidates. Labels: Absolutely injurious to allow three queenside pawns against  // Control of the centre of great importance; no violent attack

### A10-R49 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c41] `exact` — Absolutely injurious to allow three queenside pawns against two; pawns ought to be exchanged first
- **b:** [theory_capablanca/c60] `exact` — Pawns strongest side-by-side on the same rank; centre pawns strongest at K4/Q4; their advance to the 5th rank often decides the game
- **reason:** Spurious token overlap (centre,often,two); no shared referent on coordinator review of all 90 candidates. Labels: Absolutely injurious to allow three queenside pawns against  // Pawns strongest side-by-side on the same rank; centre pawns 

### A10-R50 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c41] `exact` — Absolutely injurious to allow three queenside pawns against two; pawns ought to be exchanged first
- **b:** [theory_lasker/c85] `exact` — opposite-wing castling: first attacker usually wins; Q-side harder to defend
- **reason:** Spurious token overlap (attack,first,shown); no shared referent on coordinator review of all 90 candidates. Labels: Absolutely injurious to allow three queenside pawns against  // opposite-wing castling: first attacker usually wins; Q-side 

### A10-R51 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c43] `exact` — Sufficient kingside force to ignore attack; b5 operations most in order
- **b:** [theory_capablanca/c51] `exact` — Force of the threatened attack: hold threats in hand; demonstrate on one side, shift quickly to the other
- **reason:** Spurious token overlap (attack,force,other); no shared referent on coordinator review of all 90 candidates. Labels: Sufficient kingside force to ignore attack; b5 operations mo // Force of the threatened attack: hold threats in hand; demons

### A10-R52 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c43] `exact` — Sufficient kingside force to ignore attack; b5 operations most in order
- **b:** [theory_capablanca/c54] `exact` — Sudden attack from a different side: transfer the attack side-to-side via greater mobility
- **reason:** Spurious token overlap (attack,other,sufficient); no shared referent on coordinator review of all 90 candidates. Labels: Sufficient kingside force to ignore attack; b5 operations mo // Sudden attack from a different side: transfer the attack sid

### A10-R53 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c43] `exact` — Sufficient kingside force to ignore attack; b5 operations most in order
- **b:** [theory_lasker/c66] `exact` — extra pawn won only by its sacrifice; the counterpart draws
- **reason:** Spurious token overlap (any,force,other); no shared referent on coordinator review of all 90 candidates. Labels: Sufficient kingside force to ignore attack; b5 operations mo // extra pawn won only by its sacrifice; the counterpart draws

### A10-R54 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c43] `exact` — Sufficient kingside force to ignore attack; b5 operations most in order
- **b:** [theory_lasker/c89] `exact` — same-wing castling: answer wing weaknesses by piece pressure, not pawn pushes
- **reason:** Spurious token overlap (attack,force,wing); no shared referent on coordinator review of all 90 candidates. Labels: Sufficient kingside force to ignore attack; b5 operations mo // same-wing castling: answer wing weaknesses by piece pressure

### A10-R55 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_capablanca/c38] `exact` — Combinations rest on co-ordination of the pieces against a weak point
- **reason:** Spurious token overlap (all,point,proper); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // Combinations rest on co-ordination of the pieces against a w

### A10-R56 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_capablanca/c44] `exact` — Fifty-move rule: demand mate within fifty moves; count restarts on exchange or Pawn advance
- **reason:** Spurious token overlap (advance,however,time); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // Fifty-move rule: demand mate within fifty moves; count resta

### A10-R57 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_capablanca/c49] `exact` — Direct attacks against the King must be carried en masse with full force; once begun they cannot be broken off
- **reason:** Spurious token overlap (all,attack,full); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // Direct attacks against the King must be carried en masse wit

### A10-R58 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_capablanca/c60] `exact` — Pawns strongest side-by-side on the same rank; centre pawns strongest at K4/Q4; their advance to the 5th rank often decides the game
- **reason:** Spurious token overlap (advance,next,two); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // Pawns strongest side-by-side on the same rank; centre pawns 

### A10-R59 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_capablanca/c73] `exact` — Danger of a safe position: no relaxing attention for even one move
- **reason:** Spurious token overlap (attention,danger,his); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // Danger of a safe position: no relaxing attention for even on

### A10-R60 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_capablanca/c76] `exact` — In the opening, time is of great importance; post pieces in the right places
- **reason:** Spurious token overlap (his,right,time); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // In the opening, time is of great importance; post pieces in 

### A10-R61 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c22] `exact` — defence maintains the balance; attack only with superior concentrated force
- **reason:** Spurious token overlap (attack,defence,only,point); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // defence maintains the balance; attack only with superior con

### A10-R62 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_capablanca/c14] `exact` — Bishop and Knight same theoretical value, but Bishop more valuable in most cases; two Bishops > two Knights
- **reason:** Spurious token overlap (all,however,two); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // piece valuation by mobility, void when mobility is hindered

### A10-R63 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c27] `exact` — only P-K4/P-Q4 free two pieces; move only necessary pawns
- **reason:** Spurious token overlap (necessary,only,two); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // only P-K4/P-Q4 free two pieces; move only necessary pawns

### A10-R64 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c60] `exact` — count each side's queening moves separately
- **reason:** Spurious token overlap (his,necessary,only); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // count each side's queening moves separately

### A10-R65 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c76] `exact` — attack only objects that cannot move away
- **reason:** Spurious token overlap (attack,only,point); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // attack only objects that cannot move away

### A10-R66 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c79] `exact` — pawn attacks need overwhelming concentrated force
- **reason:** Spurious token overlap (attack,only,point); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // pawn attacks need overwhelming concentrated force

### A10-R67 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c81] `exact` — fix a pawn by blockade or superior control; fix a piece only by a pin; then pile on
- **reason:** Spurious token overlap (attack,his,however,only); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // fix a pawn by blockade or superior control; fix a piece only

### A10-R68 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c85] `exact` — opposite-wing castling: first attacker usually wins; Q-side harder to defend
- **reason:** Spurious token overlap (attack,his,wing); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // opposite-wing castling: first attacker usually wins; Q-side 

### A10-R69 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c89] `exact` — same-wing castling: answer wing weaknesses by piece pressure, not pawn pushes
- **reason:** Spurious token overlap (advance,all,attack,followed,his,only,wing); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // same-wing castling: answer wing weaknesses by piece pressure

### A10-R70 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c94] `exact` — the K-side attack is the more effective (Forgacz-Tartakower)
- **reason:** Spurious token overlap (attack,combination,directed); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // the K-side attack is the more effective (Forgacz-Tartakower)

### A10-R71 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c44] `exact` — High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 sufficed; queen's wing the proper point
- **b:** [theory_lasker/c95] `exact` — the weak QP and the forced passed pawn decide (Blackburne-Schlechter)
- **reason:** Spurious token overlap (eventually,his,schlechter); no shared referent on coordinator review of all 90 candidates. Labels: High ingenuity wasted on an imaginary danger; g6/Rf7/Bf8 suf // the weak QP and the forced passed pawn decide (Blackburne-Sc

### A10-R72 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c46] `exact` — Rash attack and timid reply accounted for by time pressure on both sides
- **b:** [theory_lasker/c89] `exact` — same-wing castling: answer wing weaknesses by piece pressure, not pawn pushes
- **reason:** Spurious token overlap (attack,only,pressure); no shared referent on coordinator review of all 90 candidates. Labels: Rash attack and timid reply accounted for by time pressure o // same-wing castling: answer wing weaknesses by piece pressure

### A10-R73 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c54] `exact` — 10.O-O: a4 would have prevented the bishop being dislodged; only about an even game
- **b:** [theory_lasker/c65] `exact` — doubled pawns are weak only when isolated or passively held
- **reason:** Spurious token overlap (even,only,there); no shared referent on coordinator review of all 90 candidates. Labels: 10.O-O: a4 would have prevented the bishop being dislodged;  // doubled pawns are weak only when isolated or passively held

### A10-R74 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c54] `exact` — 10.O-O: a4 would have prevented the bishop being dislodged; only about an even game
- **b:** [theory_lasker/c68] `exact` — 2B > 2Kt; Rook beats minor piece even vs 1-2 extra pawns; tear up the pawn front first
- **reason:** Spurious token overlap (even,majority,there); no shared referent on coordinator review of all 90 candidates. Labels: 10.O-O: a4 would have prevented the bishop being dislodged;  // 2B > 2Kt; Rook beats minor piece even vs 1-2 extra pawns; te

### A10-R75 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c54] `exact` — 10.O-O: a4 would have prevented the bishop being dislodged; only about an even game
- **b:** [theory_lasker/c72] `exact` — Q vs Q drawish; Queen beats a King-backed passer except R/B pawn on seventh
- **reason:** Spurious token overlap (even,except,only); no shared referent on coordinator review of all 90 candidates. Labels: 10.O-O: a4 would have prevented the bishop being dislodged;  // Q vs Q drawish; Queen beats a King-backed passer except R/B 

### A10-R76 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c57] `exact` — 19.b4: doubtful whether the advance might not have been dispensed with; Marshall plays for attack, not content with a draw in an even position
- **b:** [theory_lasker/c68] `exact` — 2B > 2Kt; Rook beats minor piece even vs 1-2 extra pawns; tear up the pawn front first
- **reason:** Spurious token overlap (because,even,still); no shared referent on coordinator review of all 90 candidates. Labels: 19.b4: doubtful whether the advance might not have been disp // 2B > 2Kt; Rook beats minor piece even vs 1-2 extra pawns; te

### A10-R78 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c68] `exact` — After 10.Rd1 Black's alternatives fail; only 10...O-O gives a good enough game
- **b:** [theory_lasker/c27] `exact` — only P-K4/P-Q4 free two pieces; move only necessary pawns
- **reason:** Spurious token overlap (considered,good,only); no shared referent on coordinator review of all 90 candidates. Labels: After 10.Rd1 Black's alternatives fail; only 10...O-O gives  // only P-K4/P-Q4 free two pieces; move only necessary pawns

### A10-R79 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c68] `exact` — After 10.Rd1 Black's alternatives fail; only 10...O-O gives a good enough game
- **b:** [theory_lasker/c89] `exact` — same-wing castling: answer wing weaknesses by piece pressure, not pawn pushes
- **reason:** Spurious token overlap (all,only,there); no shared referent on coordinator review of all 90 candidates. Labels: After 10.Rd1 Black's alternatives fail; only 10...O-O gives  // same-wing castling: answer wing weaknesses by piece pressure

### A10-R80 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c79] `exact` — 11...Nd7 foresaw the attack on c4 and brought another piece into action
- **b:** [theory_lasker/c85] `exact` — opposite-wing castling: first attacker usually wins; Q-side harder to defend
- **reason:** Spurious token overlap (another,attack,way); no shared referent on coordinator review of all 90 candidates. Labels: 11...Nd7 foresaw the attack on c4 and brought another piece  // opposite-wing castling: first attacker usually wins; Q-side 

### A10-R81 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c80] `exact` — 13.a4 a very good one; White keeps up the attack on c4 with vigor
- **b:** [theory_capablanca/c43] `exact` — Queen vs Rook among the most difficult pawnless endings; only a very good player prevails within fifty moves
- **reason:** Spurious token overlap (good,one,very); no shared referent on coordinator review of all 90 candidates. Labels: 13.a4 a very good one; White keeps up the attack on c4 with  // Queen vs Rook among the most difficult pawnless endings; onl

### A10-R82 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c101] `exact` — From 51...d2 Black can draw against White's best play; latter part well played
- **b:** [theory_lasker/c70] `exact` — B vs B: same colour the extra pawn wins; opposite colour usually drawn
- **reason:** Spurious token overlap (can,draw,possible); no shared referent on coordinator review of all 90 candidates. Labels: From 51...d2 Black can draw against White's best play; latte // B vs B: same colour the extra pawn wins; opposite colour usu

### A10-R83 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c101] `exact` — From 51...d2 Black can draw against White's best play; latter part well played
- **b:** [theory_lasker/c72] `exact` — Q vs Q drawish; Queen beats a King-backed passer except R/B pawn on seventh
- **reason:** Spurious token overlap (can,draw,latter); no shared referent on coordinator review of all 90 candidates. Labels: From 51...d2 Black can draw against White's best play; latte // Q vs Q drawish; Queen beats a King-backed passer except R/B 

### A10-R84 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c106] `exact` — Had Black taken Nxd4, Nd7 would win at least the exchange
- **b:** [theory_capablanca/c8] `exact` — Pawn-promotion rule: King in front of Pawn with one intervening square; opponent's King in front = no win
- **reason:** Spurious token overlap (least,win,won); no shared referent on coordinator review of all 90 candidates. Labels: Had Black taken Nxd4, Nd7 would win at least the exchange // Pawn-promotion rule: King in front of Pawn with one interven

### A10-R85 — `rejected`
- **pair:** annotations-theory
- **a:** [annot_p2/c112] `exact` — 10.dxc5 Nf6 gets three pieces for the Queen but loses; Qe1 the only defence
- **b:** [theory_lasker/c39] `exact` — Caro-Kann: White gets a good game with 3.P-K5
- **reason:** Spurious token overlap (defence,gets,obtains); no shared referent on coordinator review of all 90 candidates. Labels: 10.dxc5 Nf6 gets three pieces for the Queen but loses; Qe1 t // Caro-Kann: White gets a good game with 3.P-K5

### A10-R86 — `rejected`
- **pair:** engine-theory
- **a:** [engine_games/c3] `exact` — E2 played-move rank-divergence extraction
- **b:** [theory_lasker/c17] `exact` — arithmetical rule for exchanges on one square
- **reason:** Spurious token overlap (count,loss,values); no shared referent on coordinator review of all 90 candidates. Labels: E2 played-move rank-divergence extraction // arithmetical rule for exchanges on one square

### A10-R87 — `rejected`
- **pair:** engine-theory
- **a:** [engine_games/c4] `exact` — E4 endgame segment and conversion-failure definition
- **b:** [theory_lasker/c17] `exact` — arithmetical rule for exchanges on one square
- **reason:** Spurious token overlap (count,relative,units); no shared referent on coordinator review of all 90 candidates. Labels: E4 endgame segment and conversion-failure definition // arithmetical rule for exchanges on one square

### A10-R88 — `rejected`
- **pair:** engine-theory
- **a:** [engine_games/c4] `exact` — E4 endgame segment and conversion-failure definition
- **b:** [theory_lasker/c60] `exact` — count each side's queening moves separately
- **reason:** Spurious token overlap (count,first,result); no shared referent on coordinator review of all 90 candidates. Labels: E4 endgame segment and conversion-failure definition // count each side's queening moves separately

## Merges applied (9 reviewed)

- 6 merged groups (blindfold-context notes ×4 pairs→1 group; two-knights theorem; B+Kt corner rule; general-plan doctrine; opposite-bishops draw; piece-value=mobility [FLAGGED WEAK]).
- 31 within-sky candidates rejected as spurious token overlap.

## Drops

- None. All three skies produced. (E4 segment never began in 3/4 games; E5 found zero — recorded as procedure limitations, not drops.)

## Cracks

- K10-1 ✅ verified (annotator–engine directional agreement 9/9; exploratory comparison, labeled as such)
- K10-2 ✅ verified (divergence profiles recomputed exactly)
- 0 refuted · 0 undecidable

## Method incidents (for the grade)

- annot_p1 drafter wrote status words into label fields; repaired mechanically from its own anchor notes (backup: extractions/annot_p1_raw.json).
- Two runner bugs caught by background runs (multipv=1 list shape; <3-legal-move PV count); fixed, logged.
- Node-id instability caught by the adjudication validator (slug collisions across re-runs); fixed with cid-keyed stable ids + alias resolution. The validator now fails loudly on any stale reference.
- One VM restart killed a background run; text extractions survived, engine leg re-ran cleanly.
