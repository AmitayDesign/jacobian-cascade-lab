# Probe 1 — R(5,5): exhaustive SAT over ALL cyclic (circulant) 2-colorings of K_n, n=41..46.
# 43 is prime => every vertex-transitive graph on 43 vertices is circulant, so UNSAT at n=43
# proves: no vertex-transitive R(5,5)-witness on 43 vertices. UNSAT for 43..46 proves:
# if R(5,5) > 43, every witness coloring is NON-cyclic.
import itertools, json, time
from pysat.solvers import Glucose3

def run(n):
    half = n // 2
    dist = lambda a, b: min((a - b) % n, (b - a) % n)
    solver = Glucose3(); clauses = 0
    for quad in itertools.combinations(range(1, n), 4):
        pts = (0,) + quad
        ds = sorted({dist(a, b) for a, b in itertools.combinations(pts, 2)})
        solver.add_clause([-d for d in ds]); solver.add_clause(list(ds)); clauses += 2
    t0 = time.time(); sat = solver.solve()
    out = {"n": n, "clauses": clauses, "sat": sat, "sec": round(time.time() - t0, 2)}
    if sat:
        model = solver.get_model()
        out["red_distances"] = [d for d in range(1, half + 1) if model[d - 1] > 0]
    solver.delete(); return out

print(json.dumps([run(n) for n in [41, 42, 43, 44, 45, 46]], indent=1))
