#!/usr/bin/env python3
"""Reduction test: does the seed + binary-perturbation + time-axis shape
predict which mechanisms compress?

User's refined spec (2026-10-03): the 2D plane converts to 3D geometry
through perturbation, which needs another dimension or time itself.
Single operator: PERTURB(seed-plane, binary-op, axis).

For each of the six mechanisms: write the triple, judge fit
(2=full, 1=partial, 0=no fit), and compare against the measured
token ratios from exp2_procsym.py. Refined law under test:
compression ~= shape-fit x consequence-closure richness.
Big wins need the full shape; restatements sit in the ~1x band.
"""
import json

rows = {r["eid"]: r for r in
        json.load(open("corpus_runs/exp2_procsym_rows.json"))}

TRIPLES = {
 "E017": dict(
   seed="integer line / residue classes, each marked or unmarked (binary)",
   pert="R_p marking: R_2={0}, R_p={0,-2} odd p (binary mark/unmark)",
   axis="prime sequence p=2,3,5,... z->oo (time-like iteration order)",
   unfolded="survivors=twin lowers, mu-identity, face multiplicities, "
            "delta(z), 2C2=1.32032",
   fit=2, closure="rich",
   note="mechanism IS binary perturbation of a line through prime-time"),
 "E023": dict(
   seed="phi(x,a) count table",
   pert="two-term split: remove p_a territory or not (binary per step)",
   axis="a descending (iteration index as time)",
   unfolded="face-sum D1 (one derivable); ~=soft-limit asserted, not unfolded",
   fit=1, closure="thin",
   note="perturbation shape present but closure thin; baseline already short"),
 "E152": dict(
   seed="prime Euler products",
   pert="(none) staged build, not an iterated binary perturbation",
   axis="(none) stages, not a time axis",
   unfolded="eq checks (run pipeline); bugfix provenance asserted",
   fit=0, closure="thin",
   note="pipeline shape, not perturbation; 1.33x is restatement, not regeneration"),
 "E049": dict(
   seed="zero locations rho (the formula itself holds most information)",
   pert="(weak) truncation T->oo as approximation axis",
   axis="T increasing (time-like) for error decay",
   unfolded="trunc-approx, err-decay; but formula = seed, perturbation adds little",
   fit=1, closure="thin",
   note="seed IS the content; unfolding cannot compress what the seed stores"),
 "E000": dict(
   seed="face data: binary subsets (in/out), aggregated counts",
   pert="Moebius inversion: alternating +-1 signs (literally binary)",
   axis="subset lattice large->small (unfolding aggregation to fine structure)",
   unfolded="prime counts, exact bijection, corrected sieve = primes",
   fit=2, closure="rich",
   note="binary signs perturbing aggregated data back into structure"),
 "E057": dict(
   seed="Q (resp. H)",
   pert="(none) squaring is a one-shot transform, not iterated perturbation",
   axis="(none)",
   unfolded="positivity both sides (recognized, not unfolded)",
   fit=0, closure="thin",
   note="transform shape; 1.36x is concise restatement"),
}

print(f"{'eid':6} {'fit':>4} {'closure':>8} {'ratio':>6}  triple-summary")
for eid, t in TRIPLES.items():
    r = rows[eid]
    print(f"{eid:6} {t['fit']:>4} {t['closure']:>8} {r['ratio']:6.2f}  "
          f"{t['seed'][:52]}")
    print(f"         pert: {t['pert'][:70]}")
    print(f"         note: {t['note'][:70]}")

# law check: big wins (>=3x) should have fit==2 and rich closure;
# rest (0.9-1.4x band) should lack the full shape
big = [e for e, t in TRIPLES.items() if rows[e]["ratio"] >= 3.0]
band = [e for e, t in TRIPLES.items() if rows[e]["ratio"] < 3.0]
ok_big = all(TRIPLES[e]["fit"] == 2 and TRIPLES[e]["closure"] == "rich" for e in big)
ok_band = all(not (TRIPLES[e]["fit"] == 2 and TRIPLES[e]["closure"] == "rich") for e in band)
print(f"\nlaw check: big-win=>full-shape+rich: {ok_big} ({big}); "
      f"band=>lacks full shape: {ok_band} ({band})")
json.dump(TRIPLES, open("corpus_runs/exp2_procsym_triples.json", "w"), indent=1)
print("wrote corpus_runs/exp2_procsym_triples.json")
