#!/usr/bin/env python3
"""Chunker for Atlas-11 fetcher. Reads paper text from stdin, writes
~2500-word chunks on paragraph boundaries to chunks/<paperid>_pN.txt.
Prints JSON summary to stdout."""
import sys, os, json, re

def main():
    paper_id = sys.argv[1]
    outdir = sys.argv[2]
    target = int(sys.argv[3]) if len(sys.argv) > 3 else 2500
    text = sys.stdin.read()
    # Normalize: strip the browser "L<number>:" line prefixes if present
    lines = []
    for ln in text.split('\n'):
        m = re.match(r'^L\d+:\s?(.*)$', ln)
        lines.append(m.group(1) if m else ln)
    text = '\n'.join(lines)
    # Split into paragraphs on blank lines
    paras = [p.strip() for p in re.split(r'\n\s*\n', text)]
    paras = [p for p in paras if p]
    chunks = []
    cur = []
    cur_words = 0
    for p in paras:
        w = len(p.split())
        # If adding this paragraph would push us well past target and we
        # already have a decent chunk, cut here. Never split a paragraph.
        if cur and cur_words + w > target * 1.25 and cur_words >= target * 0.5:
            chunks.append('\n\n'.join(cur))
            cur, cur_words = [], 0
        cur.append(p)
        cur_words += w
    if cur:
        chunks.append('\n\n'.join(cur))
    # Merge a tiny trailing chunk into the previous one
    if len(chunks) > 1:
        last_words = len(chunks[-1].split())
        if last_words < target * 0.3:
            chunks[-2] = chunks[-2] + '\n\n' + chunks[-1]
            chunks.pop()
    os.makedirs(outdir, exist_ok=True)
    filenames = []
    total_words = 0
    for i, c in enumerate(chunks, 1):
        fn = f"{paper_id}_p{i}.txt"
        with open(os.path.join(outdir, fn), 'w') as f:
            f.write(c + '\n')
        filenames.append(fn)
        total_words += len(c.split())
    print(json.dumps({
        "paper_id": paper_id,
        "words_in": total_words,
        "n_chunks": len(chunks),
        "chunks": filenames,
        "chunk_words": [len(c.split()) for c in chunks],
    }))

main()
