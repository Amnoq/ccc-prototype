"""CCC minimum working prototype.

Implements the dynamical system specified in ccc_math_formalization_10:
nodes carry activation / interest / stability, edges carry weight / openness,
closure density and fragmentation load evolve per step, and discrete events
(insight, conversion, anchor emergence, fragmentation, reconstruction) are
detected from threshold crossings.

On top of the dynamics it implements the one idea the AI-integration note
calls the minimum working prototype: strand export (compress relational
structure, not transcript) and rehydration (rebuild working context from the
export in a fresh graph), with probe-based fidelity metrics.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# Parameters (from ccc_math_formalization_10_so6y.md)
# --------------------------------------------------------------------------
LAMBDA_A = 0.15   # activation decay
LAMBDA_S = 0.05   # stability decay
ALPHA = 0.30      # stability gain from activation
BETA = 0.45       # stability gain from interest
GAMMA = 0.60      # stability loss from fragmentation load
KAPPA = 0.35      # neighbor propagation gain
ETA = 0.25        # hebbian edge learning rate
THETA_I = 0.70    # insight: activation threshold
THETA_C = 0.55    # memory: stability threshold
THETA_A = 0.78    # anchor: stability threshold
THETA_R = 2.50    # relational exposure threshold
R_ANCHOR = 0.60   # interest level counting toward anchor streak
ANCHOR_STREAK = 4 # steps of high interest required for anchor promotion
W_STRAND = 0.40   # edge weight qualifying for strand membership
W_CONSTRAINT = 0.70  # edge weight qualifying as a relational constraint


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


@dataclass
class Node:
    id: str
    content: str
    a: float = 0.0   # activation
    r: float = 0.0   # interest (persistent bias)
    s: float = 0.0   # stability
    R: float = 0.0   # relational exposure (cumulative)
    zone: str = "latent"
    open_question: str = ""   # unresolved loop this node carries, if any
    _r_streak: int = 0
    _was_memory: bool = False

    def to_dict(self):
        return {"id": self.id, "content": self.content,
                "stability": round(self.s, 3), "zone": self.zone,
                "open_question": self.open_question}


@dataclass
class Edge:
    u: str
    v: str
    w: float = 0.30  # weight
    o: float = 0.80  # openness

    def closure(self) -> float:
        return self.w * (1.0 - self.o)


class Graph:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []
        self.adj: dict[str, list[Edge]] = {}
        self.F = 0.0            # fragmentation load
        self.t = 0              # discrete time
        self.events: list[dict] = []   # full transcript log
        self._insight_fired: set[str] = set()

    # -- construction -----------------------------------------------------
    def add_node(self, id: str, content: str, open_question: str = "") -> Node:
        n = Node(id=id, content=content, open_question=open_question)
        self.nodes[id] = n
        self.adj[id] = []
        return n

    def add_edge(self, u: str, v: str, w: float = 0.3, o: float = 0.8):
        e = Edge(u, v, w, o)
        self.edges.append(e)
        self.adj[u].append(e)
        self.adj[v].append(e)

    def other(self, e: Edge, nid: str) -> str:
        return e.v if e.u == nid else e.u

    # -- dynamics ---------------------------------------------------------
    def closure_density(self) -> float:
        if not self.edges:
            return 0.0
        return sum(e.closure() for e in self.edges) / len(self.edges)

    def step(self, cues: dict[str, float] | None = None,
             damage: float = 0.0, recovery: float = 0.0,
             label: str = "") -> list[dict]:
        """Advance one timestep. Returns events fired this step."""
        cues = cues or {}
        self.t += 1
        fired: list[dict] = []
        C = self.closure_density()

        def emit(kind, node_id="", detail=""):
            ev = {"t": self.t, "kind": kind, "node": node_id,
                  "detail": detail, "label": label,
                  "C": round(C, 3), "F": round(self.F, 3)}
            self.events.append(ev)
            fired.append(ev)

        # 1. fragmentation load dynamics: F(t+1) = F(t) + damage - recovery
        F_before = self.F
        self.F = clamp(self.F + damage - recovery)
        if damage >= 0.5:
            emit("fragmentation", detail=f"interruption: damage={damage}")
        if recovery > 0 and F_before >= 0.5 and self.F < F_before:
            emit("reconstruction",
                 detail=f"load {F_before:.2f}->{self.F:.2f}, C={C:.2f}")

        # 2. cue input: activation + interest growth
        for nid, strength in cues.items():
            n = self.nodes[nid]
            n.a = clamp(n.a + strength)
            n.r = clamp(n.r + 0.20 * strength)
            self.events.append({"t": self.t, "kind": "cue", "node": nid,
                                "detail": f"strength={strength}", "label": label})

        # 3. neighbor propagation through closed edges
        inflow: dict[str, float] = {nid: 0.0 for nid in self.nodes}
        for e in self.edges:
            flow = KAPPA * e.closure()
            inflow[e.v] += flow * self.nodes[e.u].a
            inflow[e.u] += flow * self.nodes[e.v].a
        for nid, f in inflow.items():
            self.nodes[nid].a = clamp(self.nodes[nid].a + f)
            if f > 0.15:  # participation also builds interest
                self.nodes[nid].r = clamp(self.nodes[nid].r + 0.03)

        # 4. hebbian learning on co-activated edges
        for e in self.edges:
            a_u = self.nodes[e.u].a
            a_v = self.nodes[e.v].a
            if a_u > 0.3 and a_v > 0.3:
                e.w = clamp(e.w + ETA * a_u * a_v)
                e.o = clamp(e.o - ETA * a_u * a_v)
        # damage reopens edges
        if damage > 0:
            for e in self.edges:
                e.o = clamp(e.o + 0.5 * damage)
                e.w = clamp(e.w - 0.2 * damage)

        # 5. decay + stability update
        for n in self.nodes.values():
            n.a = n.a * (1.0 - LAMBDA_A)
            n.s = clamp(n.s * (1.0 - LAMBDA_S)
                        + ALPHA * n.a + BETA * n.r - GAMMA * self.F)
            active_neighbors = sum(1 for e in self.adj[n.id]
                                   if self.nodes[self.other(e, n.id)].a > 0.3)
            n.R += n.a * (1 + active_neighbors)

        C = self.closure_density()

        # 6. threshold crossings -> events / zone transitions
        for n in self.nodes.values():
            # insight: high activation while not yet stable (fires once per node)
            if (n.a > THETA_I and n.s < THETA_C
                    and n.id not in self._insight_fired):
                self._insight_fired.add(n.id)
                emit("insight", n.id,
                     f"activation spike a={n.a:.2f} before stability s={n.s:.2f}")
            # conversion: insight -> memory
            if not n._was_memory and n.s >= THETA_C and n.R > THETA_R:
                n._was_memory = True
                n.zone = "memory"
                emit("conversion", n.id,
                     f"stabilized s={n.s:.2f}, exposure R={n.R:.1f}")
            elif n.s >= THETA_C and n.zone == "latent":
                n.zone = "active"
            # anchor: sustained high stability + persistent interest
            if n.r > R_ANCHOR:
                n._r_streak += 1
            else:
                n._r_streak = 0
            if n.zone != "anchor" and n.s >= THETA_A \
                    and n._r_streak >= ANCHOR_STREAK:
                n.zone = "anchor"
                emit("anchor", n.id,
                     f"promoted: s={n.s:.2f}, interest streak={n._r_streak}")
        return fired

    # -- strand export ----------------------------------------------------
    def export_state(self) -> dict:
        """Compress relational structure (not transcript) for transport."""
        anchors = [n.to_dict() for n in self.nodes.values()
                   if n.zone == "anchor"]
        # strands: connected components over strong edges among stable nodes
        stable = {nid for nid, n in self.nodes.items() if n.s >= THETA_C}
        seen: set[str] = set()
        strands = []
        for nid in stable:
            if nid in seen:
                continue
            stack, comp = [nid], set()
            while stack:
                cur = stack.pop()
                if cur in comp:
                    continue
                comp.add(cur)
                for e in self.adj[cur]:
                    nb = self.other(e, cur)
                    if nb in stable and e.w >= W_STRAND and nb not in comp:
                        stack.append(nb)
            seen |= comp
            members = sorted(comp)
            strands.append({
                "id": "strand:" + "+".join(members),
                "nodes": [{"id": m, **self.nodes[m].to_dict()} for m in members],
                "mean_stability": round(sum(self.nodes[m].s for m in members)
                                       / len(members), 3),
            })
        constraints = [
            {"a": e.u, "b": e.v, "weight": round(e.w, 3),
             "rule": f"{e.u} relates to {e.v}"}
            for e in self.edges if e.w >= W_CONSTRAINT
        ]
        open_loops = [
            {"node": n.id, "zone": n.zone, "question": n.open_question,
             "activation": round(n.a, 3)}
            for n in self.nodes.values()
            if n.open_question
        ]
        return {
            "format": "ccc/1",
            "t": self.t,
            "closure_density": round(self.closure_density(), 3),
            "anchors": anchors,
            "strands": strands,
            "constraints": constraints,
            "open_loops": open_loops,
            "reconstruction_rules": {
                "theta_memory": THETA_C, "theta_anchor": THETA_A,
                "theta_insight": THETA_I,
                "protocol": ("cue anchors first; spread activation along "
                             "constraints; re-close strands before new input"),
            },
        }

    # -- rehydration ------------------------------------------------------
    @staticmethod
    def rehydrate(data: dict) -> "Graph":
        """Rebuild working context from an export in a fresh graph."""
        g = Graph()
        keep: dict[str, float] = {}
        for a in data["anchors"]:
            keep[a["id"]] = (a["content"], a["stability"] * 0.95, "anchor")
        for s in data["strands"]:
            for m in s["nodes"]:
                if m["id"] not in keep:
                    keep[m["id"]] = (m["content"], m["stability"] * 0.90,
                                     "memory")
        for nid, (content, s, zone) in keep.items():
            n = g.add_node(nid, content)
            n.s = s
            n.r = 0.65 if zone == "anchor" else 0.45
            n.zone = zone
            n._was_memory = True
        for c in data["constraints"]:
            if c["a"] in g.nodes and c["b"] in g.nodes:
                g.add_edge(c["a"], c["b"], w=c["weight"] * 0.95, o=0.25)
        # reconnect strand members that lack a constraint edge
        for s in data["strands"]:
            ids = [m["id"] for m in s["nodes"] if m["id"] in g.nodes]
            for x, y in zip(ids, ids[1:]):
                if not any({e.u, e.v} == {x, y} for e in g.edges):
                    g.add_edge(x, y, w=0.55, o=0.35)
        for loop in data["open_loops"]:
            if loop["node"] not in g.nodes:
                n = g.add_node(loop["node"], "",
                               open_question=loop["question"])
                n.a = 0.5
        return g

    # -- probe ------------------------------------------------------------
    def probe(self, query: str) -> str | None:
        """Answer a keyword query from current graph state."""
        toks = {w.strip("?,.").lower() for w in query.split()}
        best, best_score = None, 0.0
        for n in self.nodes.values():
            if not n.content:
                continue
            overlap = len(toks & {w.strip("?,.").lower()
                                 for w in n.content.split()})
            score = overlap * (0.5 + n.a + n.s)
            if score > best_score:
                best, best_score = n, score
        return best.content if best is not None else None
