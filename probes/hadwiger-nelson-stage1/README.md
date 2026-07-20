# Stage 1 — Independent verification of the 510-vertex 5-chromatic unit-distance graph

**Problem:** Hadwiger–Nelson (chromatic number of the plane). The lower bound CNP ≥ 5
rests on finite unit-distance graphs with chromatic number 5. This probe independently
re-verifies the 510-vertex Heule graph (arXiv:1907.00929 lineage) end-to-end, trusting
no one's word — not the coordinates, not the edge list, not the published chromatic number.

## What was proven (all checks passed, 2026-07-20)

### 1a. The graph is a *strict* unit-distance graph — exact arithmetic
- Source data: `vtx/510.vtx` + `edge/510.edge` from marijnheule/CNP-SAT (checksums below).
- Coordinates live in Q(√3, √5, √11). Parsed symbolically; **zero floating-point decisions**.
- Certified interval arithmetic (mpmath.iv, 120 bits) scanned all 129,795 vertex pairs;
  every pair whose d² interval contained 1 was then proven **exactly**
  (sympy `simplify(d²−1)==0` / minimal polynomial == x−1).
- Result: exactly **2,504 unit pairs = exactly the published edge list**.
  No spurious edges, no missing unit pairs. → `exact_verification.json`

### 1b. χ > 4 — SAT with machine-checkable proof
- Direct encoding (var(v,c)=4v+c+1; ALO + conflict clauses), 2,040 vars / 10,526 clauses.
- Glucose 4.2: **UNSAT** in 315 s, emitting a 1,837,100-line DRUP proof.
- Proof independently checked by **drat-trim** (compiled from source):
  `s VERIFIED` in 187 s. → `sat_verification.json`
- The DRUP proof (263 MB) exceeds GitHub file limits; it is pinned by SHA-256 below and
  regenerable deterministically by `sat_verify.py`.

### 1c. χ ≤ 5 — explicit certificate
- 5-coloring found (SAT) and validated edge-by-edge in Python: **valid**.
  → `510-k5-coloring.json` (color class per vertex, 0-indexed).

**Conclusion:** χ(G₅₁₀) = 5 exactly, and G₅₁₀ is a genuine strict unit-distance graph.
CNP ≥ 5 is re-established fully independently: exact geometry + verified UNSAT proof +
explicit coloring. Nothing here is new mathematics — it is a hostile-referee
re-derivation of the frontier fact this problem's lower bound sits on.

## Reproduce
```bash
sha256sum -c checksums.txt          # pin inputs
pip install sympy mpmath python-sat
python3 verify_exact.py             # exact strict-UDG verification (~1 min)
python3 sat_verify.py               # UNSAT + DRUP + drat-trim + 5-coloring (~10 min)
```
drat-trim: github.com/marijnheule/drat-trim (`gcc -O2 -o drat-trim drat-trim.c`).

## Checksums (SHA-256)
```
66defa1743e64073776ed4c6a2e9c496abbd4628bf7d973dcc07cf834ce35b37  510.vtx
c6178b5a6ee12f9469d33f2cdac51e6e76b3cc6b39d3bd2358b0f97a894aac0a  510.edge
e112735ceeffc8d8132017d75a65ca7c065a6106e48219b82b85d042d1e99eef  510-k4.cnf
a975e5842a2036725068fdc0787e92878dc08384b98577da226f7a3c649c24a5  510-k4.drup
2057ec1bcd36d948ee88baa9ef10b6cd343e59999ed83659b826d043edc9e787  510-k5-coloring.json
```

## Why 510 and not 509
The current record is Parts' 509-vertex graph (Geombinatorics 29, 2020). Its coordinate
file is not published in a machine-readable archive we could pin by checksum; the 510-vertex
Heule graph is the smallest with canonical public data (CNP-SAT repo). The 509 graph is a
minimization of the same family; verifying 510 verifies the load-bearing bound CNP ≥ 5.
