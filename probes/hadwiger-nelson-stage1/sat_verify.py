#!/usr/bin/env python3
"""
Stage 1b: SAT verification that the 510-vertex Heule graph is NOT 4-colorable,
with a machine-checkable DRUP proof, and IS 5-colorable (explicit coloring).

Encoding (direct): var(v,c) = k*v + c + 1 for v in 0..n-1, c in 0..k-1.
  - ALO: each vertex gets >=1 color.
  - Conflict: adjacent vertices differ in every color.
(AMO clauses are unnecessary for colorability.)
"""
import json, subprocess, time
from pysat.solvers import Glucose42
from pysat.formula import CNF

def load_edges(path):
    edges = []
    with open(path) as f:
        header = f.readline().split()
        n = int(header[2])
        for line in f:
            p = line.split()
            if p and p[0] == "e":
                edges.append((int(p[1]) - 1, int(p[2]) - 1))
    return n, edges

def color_cnf(n, edges, k):
    cnf = CNF()
    v = lambda vert, c: k * vert + c + 1
    for vert in range(n):
        cnf.append([v(vert, c) for c in range(k)])
    for a, b in edges:
        for c in range(k):
            cnf.append([-v(a, c), -v(b, c)])
    return cnf

def main():
    n, edges = load_edges("510.edge")
    print(f"graph: {n} vertices, {len(edges)} edges")
    report = {"vertices": n, "edges": len(edges)}

    cnf4 = color_cnf(n, edges, 4)
    cnf4.to_file("510-k4.cnf")
    t0 = time.time()
    with Glucose42(bootstrap_with=cnf4, with_proof=True) as s:
        sat4 = s.solve()
        proof = s.get_proof() if not sat4 else None
    report["k4_sat"] = sat4
    report["k4_solve_seconds"] = round(time.time() - t0, 1)
    if sat4:
        print("UNEXPECTED: 4-colorable!"); json.dump(report, open("sat_verification.json","w")); return
    with open("510-k4.drup", "w") as f:
        f.write("\n".join(proof) + "\n")
    report["k4_proof_lines"] = len(proof)

    t1 = time.time()
    r = subprocess.run(["./drat-trim", "510-k4.cnf", "510-k4.drup"],
                       capture_output=True, text=True, timeout=3600)
    report["drat_trim_output_tail"] = r.stdout.strip().splitlines()[-3:]
    report["drat_trim_verified"] = "s VERIFIED" in r.stdout
    report["drat_trim_seconds"] = round(time.time() - t1, 1)

    cnf5 = color_cnf(n, edges, 5)
    with Glucose42(bootstrap_with=cnf5) as s:
        sat5 = s.solve()
        model = s.get_model() if sat5 else None
    report["k5_sat"] = sat5
    if sat5:
        pos = {l for l in model if l > 0}
        coloring = []
        for vert in range(n):
            cs = [c for c in range(5) if (5 * vert + c + 1) in pos]
            coloring.append(cs[0])
        ok = all(coloring[a] != coloring[b] for a, b in edges)
        report["k5_coloring_valid"] = ok
        with open("510-k5-coloring.json", "w") as f:
            json.dump(coloring, f)

    print(json.dumps(report, indent=2))
    json.dump(report, open("sat_verification.json", "w"), indent=2)

if __name__ == "__main__":
    main()
