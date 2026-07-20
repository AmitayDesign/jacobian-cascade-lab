#!/usr/bin/env python3
"""
Stage 1a: EXACT verification that the 510-vertex Heule graph is a strict
unit-distance graph, robust to nested radicals.

Method (fully rigorous, no bare floating point in any decision):
  1. Parse each coordinate into a sympy expression tree (rational + sqrt only).
  2. Evaluate every coordinate in mpmath.iv certified interval arithmetic (120 bits).
     For every vertex pair, compute an interval for d^2. If the interval excludes 1
     -> pair is PROVEN non-unit.
  3. Every pair whose interval contains 1 is then proven EXACTLY:
     simplify(d2 - 1) == 0 or minimal_polynomial(d2, x) == x - 1.
  4. Compare the proven unit-pair set with the published edge list:
     equality <=> strict unit-distance graph.
"""
import re, json, time
import sympy as sp
from mpmath import iv
from itertools import combinations

def parse_mma(s):
    py = re.sub(r"Sqrt\\[", "sqrt(", s)
    out, depth = [], []
    i = 0
    while i < len(py):
        c = py[i]
        if py.startswith("sqrt(", i):
            out.append("sqrt("); depth.append(True); i += 5; continue
        if c == "(":
            depth.append(False); out.append(c)
        elif c == "]":
            out.append(")")
            if depth: depth.pop()
        elif c == ")":
            out.append(c)
            if depth: depth.pop()
        else:
            out.append(c)
        i += 1
    return sp.sympify("".join(out), rational=True)

def to_iv(e):
    if e.is_Rational:
        return iv.mpf(int(e.p)) / iv.mpf(int(e.q))
    if e.is_Add:
        r = iv.mpf(0)
        for a in e.args: r += to_iv(a)
        return r
    if e.is_Mul:
        r = iv.mpf(1)
        for a in e.args: r *= to_iv(a)
        return r
    if e.is_Pow:
        base = to_iv(e.base)
        if e.exp == sp.Rational(1,2):  return iv.sqrt(base)
        if e.exp == sp.Rational(-1,2): return 1/iv.sqrt(base)
        if e.exp.is_Integer:           return base ** int(e.exp)
    raise ValueError(f"unhandled node {e}")

def main():
    t0 = time.time()
    verts_sym = []
    with open("510.vtx") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            inner = line[1:-1]
            d = 0
            for k, ch in enumerate(inner):
                if ch in "([{": d += 1
                elif ch in ")]}": d -= 1
                elif ch == "," and d == 0:
                    xs, ys = inner[:k], inner[k+1:]; break
            verts_sym.append((parse_mma(xs), parse_mma(ys)))
    n = len(verts_sym)
    print(f"parsed {n} vertices in {time.time()-t0:.1f}s", flush=True)

    iv.prec = 120
    vx = [to_iv(x) for x, y in verts_sym]
    vy = [to_iv(y) for x, y in verts_sym]

    one = iv.mpf(1)
    candidates = []
    for i, j in combinations(range(n), 2):
        dx = vx[i]-vx[j]; dy = vy[i]-vy[j]
        d2 = dx*dx + dy*dy
        if one in d2:
            candidates.append((i, j))
    print(f"pair scan: {len(candidates)} candidate unit pairs", flush=True)

    edges = set()
    with open("510.edge") as f:
        f.readline()
        for line in f:
            p = line.split()
            if p and p[0] == "e":
                a, b = int(p[1])-1, int(p[2])-1
                edges.add((min(a,b), max(a,b)))

    cand = set(candidates)
    missing_from_edges = cand - edges
    edges_not_candidate = edges - cand

    x = sp.Symbol("x")
    failures = []
    for k, (i, j) in enumerate(candidates):
        dxs = verts_sym[i][0] - verts_sym[j][0]
        dys = verts_sym[i][1] - verts_sym[j][1]
        d2 = sp.expand(dxs*dxs + dys*dys)
        ok = sp.simplify(d2 - 1) == 0
        if not ok:
            mp = sp.minimal_polynomial(d2, x)
            ok = (mp == x - 1)
        if not ok:
            failures.append((i, j, str(d2)))
        if (k+1) % 250 == 0:
            print(f"  exact-proved {k+1}/{len(candidates)}", flush=True)

    result = {
        "vertices": n,
        "edges_listed": len(edges),
        "interval_candidate_unit_pairs": len(candidates),
        "exact_proof_failures": failures[:10],
        "unit_pairs_missing_from_edge_list": sorted(missing_from_edges)[:10],
        "edges_that_are_not_unit": sorted(edges_not_candidate)[:10],
        "strict_udg_verified": (not failures) and (not missing_from_edges) and (not edges_not_candidate),
        "interval_bits": 120,
        "total_seconds": round(time.time()-t0, 1),
    }
    print(json.dumps(result, indent=2))
    json.dump(result, open("exact_verification.json", "w"), indent=2)

if __name__ == "__main__":
    main()
