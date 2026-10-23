"""CCC prototype demo: a scripted research session.

Narrative mirrors a real session (primorial-wheel verification): cues arrive
as the researcher reads/discovers, an interruption fragments the graph,
anchor-cued reconstruction recovers it, then the state is exported,
the graph is wiped (new session), rehydrated from the export, and probed.
"""
import json
from ccc import Graph

g = Graph()

# -- knowledge graph -------------------------------------------------------
NODES = {
    "wheel210": ("Wheel-210 keeps 48 of 210 residues "
                 "(density 8/35, reduction 77.14%).", ""),
    "symmetry": ("Reduced residues pair as r <-> 210-r: 24 reflection pairs, "
                 "no fixed points.", ""),
    "cython_bug": ("Cython floor_div_210 truncated negatives under "
                   "cdivision=True; fixed with the q/r version.", ""),
    "jacobsthal": ("j(210) = G(210) = 10; longest non-coprime run is 9, e.g. "
                   "2..10.", ""),
    "scaling": ("Larger primorials show diminishing returns; G/mean spacing "
                "grows 1.0 -> 5.81 by P8#.", ""),
    "continuum": ("Continuum reconstruction needs explicit coarse-graining; "
                  "moment asymptotics do not control extremal gaps.", ""),
    "ccc": ("CCC: compress relational structure (strands, anchors, rules), "
            "rehydrate by reconstruction, not retrieval.", ""),
    "rh_draft": ("Toroidal RH draft: empirical section 3 is wrong (prime gaps "
                 "realize all residues mod 9 and 27); the proof is not valid.",
                 ""),
    "gcc_trivia": ("Built with GCC 13.3.0 on Ubuntu 24.04.", ""),
}
for nid, (content, q) in NODES.items():
    g.add_node(nid, content, open_question=q)

EDGES = [("wheel210", "symmetry"), ("wheel210", "cython_bug"),
         ("wheel210", "jacobsthal"), ("wheel210", "scaling"),
         ("jacobsthal", "scaling"), ("symmetry", "continuum"),
         ("wheel210", "continuum"), ("ccc", "rh_draft")]
for u, v in EDGES:
    g.add_edge(u, v)

# one genuine open loop carried into the export
g.nodes["scaling"].open_question = "Add the scaling section to the paper?"

# -- scripted session ------------------------------------------------------
# (step, cues, damage, recovery, label)
SCRIPT = [
    ({"wheel210": 0.8}, 0, 0, "read: wheel definition"),
    ({"wheel210": 0.5, "symmetry": 0.7}, 0, 0, "read: reflection proof"),
    ({"symmetry": 0.4}, 0, 0, "verify pairs computationally"),
    ({"cython_bug": 1.0}, 0, 0, "DISCOVERY: negative-range bug"),
    ({"cython_bug": 0.9, "wheel210": 0.3}, 0, 0, "fix + recompile module"),
    ({"cython_bug": 0.7}, 0, 0, "3008/3008 differential pass"),
    ({"jacobsthal": 0.8}, 0, 0, "read: Jacobsthal subsection"),
    ({"jacobsthal": 0.6, "cython_bug": 0.4}, 0, 0, "cross-check gap proof"),
    ({"scaling": 0.9}, 0, 0, "compute primorial scaling table"),
    ({"scaling": 0.6, "jacobsthal": 0.4}, 0, 0, "G/mean divergence noted"),
    ({}, 0.9, 0, "INTERRUPTION: phone call, context switch"),
    ({}, 0.4, 0, "fragmentation lingers"),
    ({"cython_bug": 0.5}, 0, 0.8, "re-cue anchor, reconstruct"),
    ({"wheel210": 0.4, "scaling": 0.4}, 0, 0.5, "rebuild strand links"),
    ({"continuum": 0.8}, 0, 0, "read: continuum-limits section"),
    ({"ccc": 0.9}, 0, 0, "pivot: revisit CCC"),
    ({"rh_draft": 0.9}, 0, 0, "read toroidal draft"),
    ({"rh_draft": 0.7, "ccc": 0.3}, 0, 0, "verify gap-residue claims"),
    ({"gcc_trivia": 0.35}, 0, 0, "notice toolchain version (trivia)"),
]

print("=" * 70)
print("CCC PROTOTYPE — session timeline")
print("=" * 70)
for cues, damage, recovery, label in SCRIPT:
    for ev in g.step(cues, damage=damage, recovery=recovery, label=label):
        if ev["kind"] in ("insight", "conversion", "anchor",
                          "fragmentation", "reconstruction"):
            print(f"t={ev['t']:>2} [{ev['kind']:<14}] {ev['node']:<11} "
                  f"{ev['detail']}  (C={ev['C']}, F={ev['F']})  <{label}>")

print("\n" + "=" * 70)
print("final zones:", {nid: n.zone for nid, n in g.nodes.items()})
print(f"closure density C={g.closure_density():.3f}, "
      f"fragmentation F={g.F:.3f}")

# -- export ---------------------------------------------------------------
export = g.export_state()
transcript = json.dumps(g.events)
payload = json.dumps(export)
print("\n" + "=" * 70)
print("EXPORT (strand compression)")
print("=" * 70)
print(f"anchors:     {[a['id'] for a in export['anchors']]}")
print(f"strands:     {len(export['strands'])} "
      f"({sum(len(s['nodes']) for s in export['strands'])} nodes)")
print(f"constraints: {len(export['constraints'])}")
print(f"open loops:  {[l['node'] + ':' + l['question'][:40] for l in export['open_loops']]}")
print(f"compression: transcript {len(transcript)} bytes -> "
      f"export {len(payload)} bytes "
      f"({len(payload)/len(transcript):.1%})")

# -- wipe + rehydrate (new session) ----------------------------------------
g2 = Graph.rehydrate(export)
# settle: cue the anchors once, let activation spread along constraints
g2.step({a["id"]: 0.6 for a in export["anchors"]})
g2.step({})

PROBES = [
    "what was the cython bug",
    "wheel density reduction",
    "scaling larger primorials findings",
    "toroidal draft verdict",
]
DROP_PROBES = ["ubuntu 24.04 toolchain"]
print("\n" + "=" * 70)
print("PROBES — full graph vs rehydrated graph")
print("=" * 70)
ok = 0
for q in PROBES:
    full = g.probe(q)
    new = g2.probe(q)
    match = (full is not None) == (new is not None) and (
        full is None or full.split("(")[0] == new.split("(")[0])
    ok += match
    tag = "SAME " if match else "DIFF "
    print(f"[{tag}] q={q!r}\n"
          f"       full: {(full or '— not retained —')[:72]}\n"
          f"       new : {(new or '— not retained —')[:72]}")
print(f"\nretention fidelity: {ok}/{len(PROBES)} probes agree")
drops = 0
for q in DROP_PROBES:
    full = g.probe(q)
    new = g2.probe(q)
    dropped = full is not None and new is None
    drops += dropped
    tag = "SELECTIVE DROP (correct)" if dropped else "LEAKED (wrong)"
    print(f"[{tag}] q={q!r}\n"
          f"       full: {(full or '— not retained —')[:72]}\n"
          f"       new : {(new or '— not retained —')[:72]}")
print(f"selective forgetting: {drops}/{len(DROP_PROBES)} trivia items "
      f"correctly absent after rehydration")

with open("ccc_export.json", "w") as f:
    json.dump(export, f, indent=2)
print("\nexport written to ccc_export.json")
