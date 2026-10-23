#!/usr/bin/env python3
"""Atlas-10 corpus prep (v2): extract clean PGNs for G1-G4, positions.fen,
and the C2 control FEN. Deterministic; run once."""
import re, os, json
import chess
import chess.pgn

BASE = os.path.expanduser("~/workspace/ccc-prototype/corpus_runs/atlas10")
CORP = os.path.join(BASE, "corpus", "pg16377.txt")
OUT = os.path.join(BASE, "engine_corpus")
os.makedirs(OUT, exist_ok=True)

txt = open(CORP).read()
starts = [m.start() for m in re.finditer(r"\[Event ", txt)]
starts.append(len(txt))

def strip_parens(s):
    out, depth = [], 0
    for ch in s:
        if ch == "(": depth += 1
        elif ch == ")": depth = max(0, depth - 1)
        elif depth == 0: out.append(ch)
    return "".join(out)

GAMES = {70: "g1_lasker_tarrasch", 84: "g2_zukertort_steinitz",
         18: "g3_morphy_anderssen", 24: "g4_anderssen_morphy"}

meta = {}
for gi, slug in GAMES.items():
    seg = txt[starts[gi]:starts[gi + 1]]
    lines = seg.split("\n")
    hlines, i = [], 0
    while i < len(lines) and lines[i].startswith("["):
        hlines.append(lines[i]); i += 1
    movetext = "\n".join(lines[i:])
    movetext = strip_parens(re.sub(r"\{[^}]*\}", " ", movetext))
    m = re.search(r"\b(1-0|0-1|1/2-1/2)\b", movetext)
    assert m, f"no result token in game {gi}"
    movetext = " ".join(movetext[:m.end()].split())
    pgn_text = "\n".join(hlines) + "\n\n" + movetext + "\n"
    path = os.path.join(OUT, slug + ".pgn")
    open(path, "w").write(pgn_text)
    game = chess.pgn.read_game(open(path))
    board = game.board()
    moves = list(game.mainline_moves())
    errs = game.errors
    for mv in moves:
        board.push(mv)
    ply = game.headers.get("PlyCount")
    assert not errs, f"errors in {slug}: {errs}"
    assert ply is None or int(ply) == len(moves), f"ply mismatch {slug}"
    meta[slug] = {"blue_book_index": gi, "half_moves": len(moves),
                  "result": game.headers.get("Result"),
                  "white": game.headers.get("White"),
                  "black": game.headers.get("Black")}
    print(slug, "OK", len(moves), "half-moves", game.headers.get("Result"))

# C2 control: game 70 position after 25...f6 = 50th half-move (index 49)
game = chess.pgn.read_game(open(os.path.join(OUT, "g1_lasker_tarrasch.pgn")))
board = game.board()
moves = list(game.mainline_moves())
assert len(moves) == 55, f"expected 55 half-moves, got {len(moves)}"
for mv in moves[:50]:
    board.push(mv)
c2_fen = board.fen()
print("C2 FEN (after 25...f6):", c2_fen)
assert board.peek().uci() == "f7f6", f"50th half-move is not f6: {board.peek()}"
open(os.path.join(OUT, "c2_control.fen"), "w").write(c2_fen + "\n")

positions = {
    "F1": "8/8/8/8/3N4/8/8/k1K4B w - - 0 1",
    "F2": "8/8/8/8/8/1Q6/8/k1K5 w - - 0 1",
    "F3": "8/8/8/8/8/1R6/8/k1K5 w - - 0 1",
}
# sanity: all are legal positions
for k, v in positions.items():
    b = chess.Board(v)
    assert b.is_valid(), f"{k} invalid"
open(os.path.join(OUT, "positions.fen"), "w").write(
    "".join(f"{k} {v}\n" for k, v in positions.items()))
open(os.path.join(OUT, "meta.json"), "w").write(json.dumps(meta, indent=1))
print("wrote engine_corpus/")
