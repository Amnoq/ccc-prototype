"""CCC cursor layer -- the magician's trick as a compression layer.

The shared state is the accumulated concept graph: nodes are registry
indices, edges are relations from all previous sessions. Both sides
hold identical copies and evolve them in lockstep. (The grid is printed
before the show -- then drawn on live.)

A message is a sequence of ops executed from a shared cursor:

  0 TARGET_WALK  n e1..en   walk n hops; each ei indexes the sorted
                            neighbor list of the current node.
                            The endpoint joins the strand set.
  1 REL_WALK     n e1..en   walk n hops; positioning only.
  2 NEW_EDGE     m ...      add edge cursor->b; record relation
                            (cursor, b). m=0: absolute b follows.
                            m=1: walk (n e1..en) to b through the
                            shared graph instead.
  3 NEW_NODE     x          node x (absolute) joins the strand set.
  4 ADD_NODE     x          cursor jumps to node x (absolute).

Every op has fixed arity, so the stream is self-delimiting -- no
external framing needed. The encoder works hard (greedy nearest-target
walk cover; cheapest of absolute-vs-walk per new edge); the decoder
just walks. Unreachable targets fall back to jumps (ops 3/4), so the
layer never gets stuck -- walking is an optimization, not a requirement.
"""
from __future__ import annotations
from collections import deque

OP_TARGET_WALK = 0
OP_REL_WALK = 1
OP_NEW_EDGE = 2
OP_NEW_NODE = 3
OP_ADD_NODE = 4


def gamma_len(x: int) -> int:
    """Bit length of the Elias-gamma code for x (matches codec._gamma_enc)."""
    assert x >= 0
    return 2 * (x + 1).bit_length() - 1


class CursorState:
    """One side's copy of the shared graph + cursor."""

    def __init__(self, n_nodes: int):
        self.n = n_nodes
        self.adj: dict[int, set[int]] = {i: set() for i in range(n_nodes)}
        self.cursor = 0

    def add_edge(self, a: int, b: int):
        assert 0 <= a < self.n and 0 <= b < self.n
        self.adj[a].add(b)
        self.adj[b].add(a)

    def neighbors(self, u: int) -> list[int]:
        return sorted(self.adj[u])

    def edge_index(self, u: int, v: int) -> int:
        return self.neighbors(u).index(v)

    def path(self, src: int, dst: int) -> list[int] | None:
        """BFS shortest path as node list, or None if unreachable."""
        if src == dst:
            return [src]
        prev: dict[int, int] = {src: -1}
        dq = deque([src])
        while dq:
            u = dq.popleft()
            for v in self.neighbors(u):
                if v not in prev:
                    prev[v] = u
                    if v == dst:
                        p = [dst]
                        while p[-1] != src:
                            p.append(prev[p[-1]])
                        return p[::-1]
                    dq.append(v)
        return None

    def snapshot(self):
        return (self.cursor,
                tuple(sorted((k, tuple(sorted(v)))
                             for k, v in self.adj.items())))


def _emit_walk(st: CursorState, ops: list[int], opcode: int,
               node_path: list[int]) -> None:
    hops = [st.edge_index(u, v)
            for u, v in zip(node_path, node_path[1:])]
    ops += [opcode, len(hops)] + hops
    st.cursor = node_path[-1]


def encode_ops(strands: set[int], relations: list[tuple[int, int]],
               st: CursorState) -> list[int]:
    """Strand set + NEW relations -> op ints. Mutates st (encoder's copy).

    Contract: every relation must be an edge not already in the shared
    graph (already-known edges are implied and need no transmission).
    """
    ops: list[int] = []
    unvisited = set(strands)
    while unvisited:
        # nearest unvisited target by BFS distance from the cursor
        best, best_path = None, None
        for t in unvisited:
            p = st.path(st.cursor, t)
            if p is not None and (best_path is None or
                                  len(p) < len(best_path)):
                best, best_path = t, p
        if best is None:
            # nothing reachable: jump to each remaining node
            for t in sorted(unvisited):
                ops += [OP_NEW_NODE, t]
                st.cursor = t
            break
        _emit_walk(st, ops, OP_TARGET_WALK, best_path)
        unvisited.discard(best)
    for (a, b) in relations:
        if b in st.adj[a]:
            raise ValueError(f"relation {(a, b)} already in shared graph: "
                             f"only NEW edges are transmitted")
        p = st.path(st.cursor, a)
        if p is None:
            ops += [OP_ADD_NODE, a]   # jump: unreachable, no walk possible
            st.cursor = a
        elif len(p) > 1:
            _emit_walk(st, ops, OP_REL_WALK, p)
        assert st.cursor == a
        # cheapest way to name b: absolute, or walk to it through the
        # shared graph (both sides see the same graph, so both agree)
        p2 = st.path(a, b)
        use_walk, hops2 = False, []
        if p2 is not None and len(p2) > 1:
            hops2 = [st.edge_index(u, v)
                     for u, v in zip(p2, p2[1:])]
            if (gamma_len(len(hops2)) +
                    sum(gamma_len(h) for h in hops2) < gamma_len(b)):
                use_walk = True
        if use_walk:
            ops += [OP_NEW_EDGE, 1, len(hops2)] + hops2
            st.cursor = b
        else:
            ops += [OP_NEW_EDGE, 0, b]
            st.cursor = b
        st.add_edge(a, b)
    return ops


def decode_ops(ints: list[int], st: CursorState):
    """Op ints -> (strand set, relation list). Mutates st (decoder's copy).

    Must be called with a state identical to the encoder's at encode
    time; every op mutates the state exactly as the encoder's did.
    """
    strands: set[int] = set()
    relations: list[tuple[int, int]] = []
    i, n = 0, len(ints)

    def need(k: int):
        if i + k > n:
            raise ValueError("truncated op stream")

    while i < n:
        op = ints[i]
        i += 1
        if op == OP_TARGET_WALK or op == OP_REL_WALK:
            need(1)
            nh = ints[i]
            i += 1
            need(nh)
            for _ in range(nh):
                e = ints[i]
                i += 1
                nbrs = st.neighbors(st.cursor)
                if not 0 <= e < len(nbrs):
                    raise ValueError(f"edge index {e} out of range "
                                     f"at node {st.cursor}")
                st.cursor = nbrs[e]
            if op == OP_TARGET_WALK:
                strands.add(st.cursor)
        elif op == OP_NEW_EDGE:
            need(1)
            m = ints[i]
            i += 1
            start = st.cursor
            if m == 0:
                need(1)
                b = ints[i]
                i += 1
                st.cursor = b
            elif m == 1:
                need(1)
                nh = ints[i]
                i += 1
                need(nh)
                for _ in range(nh):
                    e = ints[i]
                    i += 1
                    nbrs = st.neighbors(st.cursor)
                    if not 0 <= e < len(nbrs):
                        raise ValueError(f"edge index {e} out of range "
                                         f"at node {st.cursor}")
                    st.cursor = nbrs[e]
                b = st.cursor
            else:
                raise ValueError(f"bad NEW_EDGE mode {m}")
            st.add_edge(start, b)
            relations.append((start, b))
        elif op == OP_NEW_NODE:
            need(1)
            x = ints[i]
            i += 1
            if not 0 <= x < st.n:
                raise ValueError(f"node {x} outside registry")
            strands.add(x)
            st.cursor = x
        elif op == OP_ADD_NODE:
            need(1)
            x = ints[i]
            i += 1
            if not 0 <= x < st.n:
                raise ValueError(f"node {x} outside registry")
            st.cursor = x
        else:
            raise ValueError(f"bad opcode {op}")
    return strands, relations
