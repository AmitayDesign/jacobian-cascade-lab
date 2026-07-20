# Probe 3 — Andrews–Curtis: SOUND exhaustive BFS over pairs of cyclic-word classes
# (canonical up to rotation, inversion, swap — exact for AC moves since conjugation acts
# transitively on rotations). Multiplication move applied over ALL rotation representatives
# of both relators. Every state in the ball is PROVEN AC-trivializable with all intermediate
# relators <= L; non-membership proves any trivialization needs a relator > L.
import json, time, sys
from collections import deque

INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
def reduce_w(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]: out.pop()
        else: out.append(c)
    return "".join(out)
def cyc_reduce(w):
    while len(w) > 1 and w[0] == INV[w[-1]]: w = w[1:-1]
    return w
def inv_w(w): return "".join(INV[c] for c in reversed(w))
def variants(w):
    vs = set()
    for u in (w, inv_w(w)):
        for i in range(len(u)): vs.add(u[i:] + u[:i])
    return vs
def canon(w):
    w = cyc_reduce(reduce_w(w))
    return min(variants(w)) if w else w
def canon_pair(r1, r2):
    a, b = canon(r1), canon(r2)
    return (a, b) if a <= b else (b, a)

L = int(sys.argv[1]) if len(sys.argv) > 1 else 8
def neighbors(state):
    r1, r2 = state; res = set()
    for a, b in ((r1, r2), (r2, r1)):
        if not a or not b: continue
        for arep in variants(a):
            for brep in variants(b):
                m = canon(arep + brep)
                if m and len(m) <= L: res.add(canon_pair(m, b))
    return res

start = canon_pair("x", "y")
parent = {start: None}; q = deque([start]); t0 = time.time()
while q:
    s = q.popleft()
    for nb in neighbors(s):
        if nb not in parent: parent[nb] = s; q.append(nb)

def path_to(t):
    if t not in parent: return None
    p = []
    while t is not None: p.append(list(t)); t = parent[t]
    return p[::-1]

ms1_r2 = reduce_w("X" + "xyXYY")
targets = {"AK(2)": canon_pair("xxYYY", "xyxYXY"),
           "AK(3)": canon_pair("xxxYYYY", "xyxYXY"),
           "MS(1,xyXYY)": canon_pair("XyxYY", ms1_r2)}
print(json.dumps({"length_cap": L, "ball_size": len(parent),
    "seconds": round(time.time() - t0, 1),
    "membership": {k: (v in parent) for k, v in targets.items()},
    "AK2_chain": path_to(targets["AK(2)"])}, indent=1))
