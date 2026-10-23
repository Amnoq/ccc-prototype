# Atlas-3 Pilot Report — the two-skies test (algebra vs geometry)

Date: 2026-10-07. Coordinator: Atlas-3 subagent. Charter: ATLAS3_CHARTER.md.
Question: ledger item 3 (user's theorization, outcome class `pass`) —
mapped as two skies, algebra and geometry show a very narrow link
between their constellations, like Atlas-2's pilot↔foreign result.

## Verdict (measurements; the narrow/wide verdict is the user's at grading)

**Direct algebra↔geometry: 0 adjudicated links.** Mechanical candidate
generation found 1 A↔G candidate (spurious token match on generic
words, correctly rejected by review). Semantic review of all 145
cross-sky node labels found no shared mathematical objects. The
vocabularies are disjoint: modules/rings/representations vs
curvature/flows/minimal surfaces.

**The bridge touches only at the discipline level.** The single
adjudicated cross-sky link in the whole run is bridge↔algebra:
Frenkel's "automorphic representations" ↔ Harris's "ITI(KG)/ITS(KG)"
— split_link, relation `shares-discipline`. Both are representation
theory; the objects differ (adelic groups vs finite groups in
characteristic p), so linked, not merged. No merges anywhere in the
run (0 false merges — the bar holds).

**Controls:** S1 (bridge↔algebra) WEAK PASS — the genuine
field-level relationship exists and was adjudicated, but ONLY the
semantic reviewed pass found it; the mechanical token-overlap pass
missed it entirely (it surfaced only a "Galois"/"Galois conjugates"
false friend, correctly rejected). S2 (bridge↔geometry) VOID —
misseeded, not method failure: geometric Langlands touches
complex-algebraic geometry (holomorphic bundles, D-modules on Bun_G);
the geometry sky as built is differential geometry (Ricci flow,
minimal surfaces). No shared objects exist at node level, so the
method correctly found nothing. R&D spec: seed positive controls
against the right subfield — "geometry" is not one sky.

**In Atlas-2 units:** Atlas-2 found 13 adjudications / 310 candidates
(2 genuine merges). Atlas-3 pilot: 1 adjudicated link / 3 mechanical
candidates, 0 merges, 0 contradictions, 1 control void. The direct
link is narrower than Atlas-2's — the measurement is consistent with
the user's "very narrow" prediction, and the bridge concentrates the
only link at the discipline level. Per the charter, the instrument
does not claim narrowness (S2 void); the counts go to the user, whose
narrow/wide verdict resolves ledger item 3.

## Honest limits

1. **Pilot scale, prefix samples.** 5 papers, 9 chunks, 176 concepts —
   vs Atlas-2's 7 papers / 84 files / 521 concepts. Chunks are
   prefixes (Harris whole paper; others first ~1/5–2/3). A full-paper
   run could surface links the prefixes miss — especially S2, where
   Frenkel's later sections (geometric Langlands in depth) lie beyond
   the chunk boundary.
2. **S2 misseeded.** The geometry sky should have included complex-
   algebraic geometry for a fair S2. This was a coordinator design
   error, recorded as void — not as evidence either way.
3. **Mechanical recall fails across vocabularies.** Token-overlap
   candidate generation (Atlas-2's method) found 3 candidates, all
   spurious, and missed the one genuine field-level link. Cross-domain
   work needs semantic candidate generation; the token method was
   tuned on a shared-vocabulary corpus (analytic number theory).
4. **Word counts are drafter estimates**, not machine counts (one
   drafter used curl on its own URL to count; disclosed in its report).
   Token figures are 1.3×word ESTIMATES.
5. **No fabrication re-check** beyond the drafters' self-validation
   and the coordinator's label review. The user's grading packet is
   the real check (delivered: grading_packet.md).
6. **Within-sky merging was thin** (3 merges, all obvious aliases).
   Drafters' per-chunk vocabularies barely overlapped — same pattern
   as Atlas-2 (522 occurrences → 521 nodes).

## Cost table (per phase; tokens = 1.3×words, ESTIMATE)

| Phase | Words in | Words out | Est. tokens |
|---|---|---|---|
| Corpus verification (14 page fetches) | ~40,000 | ~0 | ~52,000 |
| Coordinator transcription (superseded) | 0 | ~11,800 | ~15,300 |
| Extraction — 9 blind drafters | 82,931 | 12,552 | ~124,100 |
| Merge + adjudication + illustration | ~30,000 | ~5,000 | ~45,500 |
| **Pilot total** | **~152,900** | **~29,400** | **~237,000** |

Unit cost: extraction dominates — ~9,200 words in / ~1,400 words out
per chunk; ~13,800 tokens per chunk all-in. Per 1k source words:
~1,500 tokens (in+out at 1.3×).

Extrapolation (full-corpus Atlas-3, ~8 papers full text ≈ 150k words):
extraction ≈ 150k × 1.5 = ~225k tokens; total run ≈ 400–450k tokens.
No dollar figure — the subscription's token price is not in the
record; the $/token rate must come from the subscription terms before
a dollar extrapolation is honest.

## Pipeline record

- Corpus: 5/5 papers retrieved clean via ar5iv (provenance per chunk
  in manifest.json). BK2011 not triggered. A2/G2 coordinator-selected,
  ID-verified by search.
- Extraction: 9/9 blind R4 drafters, 100% schema-valid on arrival,
  all ids resolve. Design change recorded: drafters fetched their own
  primary text (fidelity + stronger blindness).
- Merge: merge_atlas3.py — within-sky P1 (4 explicit aliases,
  reviewed), cross-sky mechanical candidates (3, all rejected on
  review).
- Adjudication: write_links3.py → cross_sky_links.json — 1
  split_link, 3 rejected, 0 merged, 1 control void, 0 contradictions,
  0 false merges.
- Illustration: build_html3.py — atlas3_algebra.html,
  atlas3_geometry.html, atlas3_bridge.html, atlas3_cross.html
  (money view; the single gold link is the S1 discipline bridge).
- Atlas-2's and the pilot's directories were read-only throughout
  (template read, never written).

## Branching (charter)

Narrow measured + S1 weak-pass → full-corpus Atlas-3 is justified
**provided** S2 is re-seeded against complex-algebraic geometry and
mechanical candidate generation is replaced/augmented with semantic
review (the token method demonstrably misses cross-vocabulary links).
The grading packet is delivered regardless — his verdict is the
final leg and resolves ledger item 3.

## Backward touch — 2026-10-08 (Atlas-11)

Atlas-11 ran the correction this report's Branching section specified: S2 re-seeded against complex-algebraic geometry (Mulase Hitchin systems + Tosteson Deligne-Mumford, instead of Atlas-3's misseeded differential geometry), with the analytics↔geometry pair as the actual test. The corrected S2 **resolves** (1 merged_link on the Hitchin fibration theorem + 32 split_links; 0 false merges) — so Atlas-3's void S2 was a seeding error, not a method failure, and the instrument claims narrowness or wall findings only when its controls are correctly seeded. Atlas-11's own verdict: 0 direct analytics↔geometry links (wall), both controls resolved. Atlas-3's history is unchanged — its S2 remains void, its item 3 remains unscored.
