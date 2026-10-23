#!/usr/bin/env python3
"""Atlas-10 engine analysis runner. Implements ENGINE_PROCEDURES.md
E1-E5 + controls C1/C2 EXACTLY as pre-registered. Deterministic given
the fixed binary and depths. Writes engine_raw.json."""
import os, json
import chess
import chess.engine
import chess.pgn

BASE = os.path.expanduser("~/workspace/ccc-prototype/corpus_runs/atlas10")
EC = os.path.join(BASE, "engine_corpus")
STOCKFISH = os.path.join(BASE, "bin", "stockfish")
OUT = os.path.join(BASE, "engine_raw.json")

MATE_CP = 100000
GAME_DEPTH = 20
POS_DEPTH = 24

def wrel(score):
    """White-relative cp; mate -> +/-MATE_CP."""
    return score.white().score(mate_score=MATE_CP)

def analyse_position(engine, board, depth, multipv):
    info = engine.analyse(board, chess.engine.Limit(depth=depth),
                          multipv=multipv)
    if isinstance(info, list):
        # multipv=N (even N=1) returns a list; fewer than N PVs come
        # back when the position has fewer legal moves. Normalize.
        assert 1 <= len(info) <= multipv, f"got {len(info)} PVs"
        return info[0] if multipv == 1 else info
    return info

def main():
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH)
    engine.configure({"Hash": 256})
    raw = {"games": {}, "positions": {}, "controls": {}}

    games = ["g1_lasker_tarrasch", "g2_zukertort_steinitz",
             "g3_morphy_anderssen", "g4_anderssen_morphy"]
    for slug in games:
        game = chess.pgn.read_game(open(os.path.join(EC, slug + ".pgn")))
        board = game.board()
        moves = list(game.mainline_moves())
        positions = []
        # E1: evaluate initial + after each half-move
        boards = [board.copy()]
        for mv in moves:
            board.push(mv)
            boards.append(board.copy())
        prev_wrel = None
        for ply, b in enumerate(boards):
            if b.is_game_over():
                rec = {"ply": ply, "fen": b.fen(), "terminal": True,
                       "result_claim": b.result()}
                positions.append(rec)
                prev_wrel = None
                continue
            info = analyse_position(engine, b, GAME_DEPTH, 3)
            pvs = [(wrel(p["score"]), p["pv"][0].uci() if p.get("pv") else None)
                   for p in info]
            best_w, best_uci = pvs[0]
            # played move = the move leading OUT of this position
            played_uci = moves[ply].uci() if ply < len(moves) else None
            rank, loss = None, None
            if played_uci:
                rank = next((i + 1 for i, (_, u) in enumerate(pvs)
                             if u == played_uci), 4)
                s = 1 if b.turn == chess.WHITE else -1
                best_mover = s * best_w
                if rank <= 3:
                    played_w = pvs[rank - 1][0]
                    loss = best_mover - s * played_w
                else:
                    # lower bound: at least as bad as worst returned PV
                    worst_w = pvs[-1][0]
                    loss = best_mover - s * worst_w
                    loss = {"lower_bound_cp": loss,
                            "pvs_returned": len(pvs)}
            swing = None
            if prev_wrel is not None and abs(prev_wrel) < MATE_CP \
               and abs(best_w) < MATE_CP:
                swing = best_w - prev_wrel
            rec = {"ply": ply, "fen": b.fen(), "best_cp_wrel": best_w,
                   "pv1_uci": best_uci, "played_uci": played_uci,
                   "played_rank": rank, "played_loss_cp_mover": loss,
                   "swing_cp_wrel": swing}
            positions.append(rec)
            prev_wrel = best_w if abs(best_w) < MATE_CP else None
        raw["games"][slug] = {
            "result": game.headers.get("Result"),
            "half_moves": len(moves),
            "positions": positions}

    # E3: theoretical positions
    for line in open(os.path.join(EC, "positions.fen")):
        pid, fen = line.split(" ", 1)[0], line[len(line.split(" ", 1)[0]) + 1:].strip()
        b = chess.Board(fen)
        info = analyse_position(engine, b, POS_DEPTH, 1)
        sc = wrel(info["score"])
        mate_n = info["score"].white().mate()
        raw["positions"][pid] = {"fen": fen,
                                 "outcome": ("mate-in-%d" % mate_n) if mate_n else ("cp %+d" % sc),
                                 "mate_n": mate_n, "cp_wrel": sc}

    # C2 control position
    c2fen = open(os.path.join(EC, "c2_control.fen")).read().strip()
    b = chess.Board(c2fen)
    info = analyse_position(engine, b, GAME_DEPTH, 1)
    sc = wrel(info["score"])
    raw["controls"]["C2"] = {"fen": c2fen, "cp_wrel": sc,
                             "mate_n": info["score"].white().mate()}

    engine.quit()
    json.dump(raw, open(OUT, "w"))
    print("wrote", OUT, "bytes:", os.path.getsize(OUT))

if __name__ == "__main__":
    main()
