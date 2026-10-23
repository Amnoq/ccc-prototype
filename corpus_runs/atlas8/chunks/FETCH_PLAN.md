# Atlas-8 foreign-sky chunk materialization plan

The retriever verified all 6 papers and mapped exact slice anchors, but did
**not** write paper text into chunk files (copyright policy: no bulk
reproduction into files). This plan lets the parent materialize the 11
planned chunks deterministically in one step.

## Sources (all URLs verified live 2026-10-07)

| id | URL | kind |
|---|---|---|
| pnt | https://sites.math.rutgers.edu/~zeilberg/EM18/zagier.pdf | PDF (JSTOR scan) |
| cramer | https://chance.dartmouth.edu/chance_news/for_chance_news/Riemann/cramer.pdf | PDF (author-hosted) |
| zhang | https://math.rutgers.edu/~zeilberg/purdue22/YitangBoundedGaps.pdf | PDF (JSTOR scan) |
| maynard | https://ar5iv.org/html/1311.4600 | HTML (ar5iv) |
| greentao | https://ar5iv.org/html/math/0404188 | HTML (ar5iv) |
| sieve | https://people.math.harvard.edu/~elkies/M229.22/sieve.pdf | PDF (course notes) |

## Recipe

1. Download each URL with the parent's browser/file tools (plain file
   download, no text reproduction through the model).
2. PDFs: `pdftotext -layout <file>.pdf <file>.txt` (pdftotext is installed
   at /usr/bin/pdftotext).
3. ar5iv HTML: strip tags to text (e.g. `pandoc -f html -t plain`, or
   BeautifulSoup `.get_text()`), then slice.
4. Slice each text by the anchor pairs in `_provenance.json`
   (chunk entries, `slice.anchor_start` -> `slice.anchor_end`, first
   occurrence; anchors are unique section headers in every case).
   Strip the repetitive JSTOR "downloaded from / Terms & Conditions" banner
   lines from the pnt/zhang/cramer slices.
5. Write to `chunks/foreign_<id>_p<N>.txt` (UTF-8), ~2,500 words each
   (maynard_p3 will run ~3,200 — it is one complete section, kept whole
   for coherence). Verify word counts with `wc -w` and record actuals in
   `_provenance.json` (`est_words` -> `words`).

## Planned chunk map (from _provenance.json)

- foreign_pnt_p1.txt — Zagier, whole paper (steps I–VI + historical remarks)
- foreign_cramer_p1.txt — Granville, model definition + gap/prediction
  arc (anchors: "In 1937 Cram" ... "uniform version of the Hardy-Littlewood conjecture")
- foreign_zhang_p1.txt — Zhang §1 Introduction + §2 Notation/sketch
  (anchors: "1. Introduction" ... "3. Lemmas")
- foreign_zhang_p2.txt — Zhang §7 The dispersion method, complete section
  (anchors: "7. The dispersion method" ... "8. Evaluation of")
- foreign_maynard_p1.txt — Maynard abstract + §1 Introduction
- foreign_maynard_p2.txt — Maynard §2 improved GPY sieve + §3 notation +
  §4 outline of proof
- foreign_maynard_p3.txt — Maynard §5 Selberg sieve manipulations, complete
- foreign_greentao_p1.txt — Green–Tao abstract + §1 Introduction (Thms 1.1, 1.2)
- foreign_greentao_p2.txt — Green–Tao §2 outline of the proof, complete
- foreign_greentao_p3.txt — Green–Tao §3 pseudorandom measures (transference
  principle, Thm 3.5), complete
- foreign_sieve_p1.txt — Elkies notes, whole (Selberg inequality + proof +
  applications)

## ID corrections found during verification (already in provenance)

- Task's "arXiv:1305.2897" for Zhang is Helfgott's Goldbach paper; "arXiv:1305.0284"
  is a moduli-space paper. Zhang has **no** arXiv version; the published
  Annals version was fetched instead.
- Task's "arXiv:1404.0794" for Maynard is a hep-th paper; correct ID is
  **arXiv:1311.4600** (v3), published Annals 181 (2015), 383–413 (not 2016).
- Task's "arXiv:math/0404188" for Green–Tao verified correct (v6).

## S1 positive control

Maynard §1 Introduction cites Zhang's bounded-gaps breakthrough (ref [9])
and frames the paper as a refinement of the GPY method — see
_provenance.json `s1_control` for location + brief quote.
