# Atlas-6 run log

## 2026-10-07/08: bridge-mapping run (Weil), coordinator-driven
- Charter: ATLAS6_CHARTER.md. Question: map the Atlas-5 Weil crack at high
  resolution from both sides. The map, not the proof.
- Retrieval (worker bda73429): AF arXiv:2608.13637v2 verified (preprint label);
  BOM Bombieri 2000 via bdim.eu (refereed); GRO arXiv:2607.02828 (preprint,
  disclaimers verified). Weil 1952 DROPPED per BK2011 (CERN Anubis, Numdam
  absent, IA absent — 3 routes). Li 1997 + Bombieri-Lagarias 1999 DROPPED
  (paywalled); BOM substituted as tighter lineage fit. manifest.json written
  with section refs + line ranges. Note: chunks/ holds no text files — per
  standing license discipline (D2) drafters fetched their own ranges via
  browser.open; the manifest's refs ARE the chunk record.
- Extraction: 5 workers, blind per side. Relational: weil_rel_step12.json
  (10 concepts), weil_rel_step3_tree.json (21). Analytic: AF 45 (3 files,
  10/10 Weil sections covered), BOM 25 (3 files, equation fragmentation
  recorded), GRO 19 (3 files, disclaimers as concepts). All schema-validated.
  One spawn misfire (placeholder message) closed before any action.
- Merge (merge_atlas6.py): 120 concepts -> 117 nodes after 3 reviewed merges
  (facets preserved). 631 mechanical candidates -> reviewed adjudication.
- Adjudication (adjudicate_atlas6.py, by coordinator): 13 records —
  9 split_link (incl. SEED S0) + 4 rejected with reasons. SEED REPRODUCES:
  Atlas-5's AF-W-form <-> pilot-Guinale-Weil link re-derives under focused
  blind re-extraction. 0 false merges, 0 contradictions.
- Illustration: build_html6.py -> atlas6_bridge.html (JS-validated; galaxy
  layout, gold bridge edges, role-difference labels at midpoints, clickable
  loops, preprint badges); atlas6_bridge.png static render.
- Report: ATLAS6_REPORT.md (verdict: bridge maps cleanly). Grading packet:
  grading_packet.md (24 Weil triples + all 13 adjudications + 3 merges).
- Cost: ~26.5k tokens ESTIMATE (extraction); ~1.84k tok/1k words all-in.
