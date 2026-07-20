# Jacobian Cascade Lab

Machine-verified structure theory built on the Alpöge–Fable counterexample to the
**Jacobian Conjecture** (announced July 19–20, 2026). Everything here is exact
rational/symbolic arithmetic — no floating point, no trust required.

## Reproduce everything (one command)

```bash
pip install sympy
python3 repro.py     # prints 13 PASS lines, exits 0
```

## What is verified

| # | Claim | Status |
|---|-------|--------|
| 1 | Alpöge–Fable map F: det J = −2 (constant), 3 distinct points → 1 image ⇒ **JC₃ false** | re-derived from scratch |
| 2 | Hidden pivot structure: F₁ = u·w, F₂ = y + 3x·w with u = 1+xy, w = u²z + y²(4+3xy) | new observation |
| 3 | Integer normalization H: ℤ-coefficients, **det J = +1 exactly**, same 3-point collision ⇒ Keller's original 1939 arithmetic form false | new construction |
| 4 | **Family theorem**: F_{k,c} (a=12/k, b=9/k, c₀=−6c/k, c₁=9c/k) has det J = 6c/k for ALL k,c ≠ 0, and the collision transports to every member by explicit diagonal conjugacy. The published map is the single member (k=3, c=−1) | **new theorem** |
| 5 | Generic fiber degree: F is globally **3-to-1** onto its image (fiber cubic in x, discriminant ≢ 0) — the collision is generic, not sporadic; and [ℂ(x,y,z) : ℂ(F)] = 3 means no rational inverse of any kind exists | **new theorem** |
| 6 | Monodromy of the 3:1 cover is full **S₃** (discriminant not a square in ℂ(c₁,c₂,c₃)) ⇒ the cover is non-Galois; no global deck symmetry exists | **new theorem** |
| 7 | Dimension obstruction: the pivot mechanism admits only degenerate (det = 0) specializations in 2 variables ⇒ this entire class of counterexamples **cannot touch JC₂**, which remains open | **new theorem** |

Cascade corollaries (via peer-reviewed implications; the premise JC₃-false is
re-verified in exact arithmetic inside each script): Dixmier conjecture false for
n ≥ 3 (explicit Weyl-algebra endomorphism, checked directly, not by citation),
Mathieu conjecture false (Mathieu 1997), Zhao vanishing conjecture false (Zhao 2006).

## Consistency audit

`scripts/heuristic_crosscheck.py` verifies the counterexample against every
classical partial result that made experts believe JC (Wang deg ≤ 2; Magnus–Moh;
Ax–Grothendieck/Cynk–Rusek injective ⇒ automorphism; Białynicki-Birula–Rosenlicht):
no contradiction with any proven theorem — only with the conjecture itself.

## Wolfram|Alpha one-click verification

- [det J = −2 (Keller property of F)](https://www.wolframalpha.com/input?i=det%20of%20Jacobian%20matrix%20of%20((1%2Bx%20y)%5E3%20z%20%2B%20y%5E2%20(1%2Bx%20y)(4%2B3%20x%20y)%2C%20y%20%2B%203%20x%20(1%2Bx%20y)%5E2%20z%20%2B%203%20x%20y%5E2%20(4%2B3%20x%20y)%2C%202x%20-%203%20x%5E2%20y%20-%20x%5E3%20z)%20with%20respect%20to%20(x%2C%20y%2C%20z))
- [F(0,0,−1/4) — collision image](https://www.wolframalpha.com/input?i=((1%2Bx%20y)%5E3%20z%20%2B%20y%5E2%20(1%2Bx%20y)(4%2B3%20x%20y)%2C%20y%20%2B%203%20x%20(1%2Bx%20y)%5E2%20z%20%2B%203%20x%20y%5E2%20(4%2B3%20x%20y)%2C%202x%20-%203%20x%5E2%20y%20-%20x%5E3%20z)%20at%20x%3D0%2C%20y%3D0%2C%20z%3D-1%2F4)
- [F(1,−3/2,13/2) — same image](https://www.wolframalpha.com/input?i=((1%2Bx%20y)%5E3%20z%20%2B%20y%5E2%20(1%2Bx%20y)(4%2B3%20x%20y)%2C%20y%20%2B%203%20x%20(1%2Bx%20y)%5E2%20z%20%2B%203%20x%20y%5E2%20(4%2B3%20x%20y)%2C%202x%20-%203%20x%5E2%20y%20-%20x%5E3%20z)%20at%20x%3D1%2C%20y%3D-3%2F2%2C%20z%3D13%2F2)
- [F(−1,3/2,13/2) — same image](https://www.wolframalpha.com/input?i=((1%2Bx%20y)%5E3%20z%20%2B%20y%5E2%20(1%2Bx%20y)(4%2B3%20x%20y)%2C%20y%20%2B%203%20x%20(1%2Bx%20y)%5E2%20z%20%2B%203%20x%20y%5E2%20(4%2B3%20x%20y)%2C%202x%20-%203%20x%5E2%20y%20-%20x%5E3%20z)%20at%20x%3D-1%2C%20y%3D3%2F2%2C%20z%3D13%2F2)
- [pivot identity F₁ = u·w (expands to 0)](https://www.wolframalpha.com/input?i=expand%20((1%2Bx%20y)%5E3%20z%20%2B%20y%5E2%20(1%2Bx%20y)(4%2B3%20x%20y))%20-%20(1%2Bx%20y)((1%2Bx%20y)%5E2%20z%20%2B%20y%5E2%20(4%2B3%20x%20y)))
- [family det J = 6c/k (constant for all k, c)](https://www.wolframalpha.com/input?i=det%20of%20Jacobian%20matrix%20of%20((1%2Bx%20y)((1%2Bx%20y)%5E2%20z%20%2B%20y%5E2%20(12%2B9%20x%20y)%2Fk)%2C%20y%20%2B%20k%20x%20((1%2Bx%20y)%5E2%20z%20%2B%20y%5E2%20(12%2B9%20x%20y)%2Fk)%2C%20c(-6x%2Fk%20%2B%209%20x%5E2%20y%2Fk%20%2B%20x%5E3%20z))%20with%20respect%20to%20(x%2Cy%2Cz))
- [integer map: det J = 1](https://www.wolframalpha.com/input?i=det%20of%20Jacobian%20matrix%20of%20(-8x%5E3%20y%5E3%20z%20-%2024%20x%5E2%20y%5E4%20-%2012%20x%5E2%20y%5E2%20z%20-%2028%20x%20y%5E3%20-%206%20x%20y%20z%20-%208%20y%5E2%20-%20z%2C%2012%20x%5E3%20y%5E2%20z%20%2B%2036%20x%5E2%20y%5E3%20%2B%2012%20x%5E2%20y%20z%20%2B%2024%20x%20y%5E2%20%2B%203%20x%20z%20%2B%20y%2C%20-x%5E3%20z%20-%203%20x%5E2%20y%20%2B%20x)%20with%20respect%20to%20(x%2C%20y%2C%20z))
- [integer map collision at (0,0,−1/8)](https://www.wolframalpha.com/input?i=(-8x%5E3%20y%5E3%20z%20-%2024%20x%5E2%20y%5E4%20-%2012%20x%5E2%20y%5E2%20z%20-%2028%20x%20y%5E3%20-%206%20x%20y%20z%20-%208%20y%5E2%20-%20z%2C%2012%20x%5E3%20y%5E2%20z%20%2B%2036%20x%5E2%20y%5E3%20%2B%2012%20x%5E2%20y%20z%20%2B%2024%20x%20y%5E2%20%2B%203%20x%20z%20%2B%20y%2C%20-x%5E3%20z%20-%203%20x%5E2%20y%20%2B%20x)%20at%20x%3D0%2C%20y%3D0%2C%20z%3D-1%2F8)
- [integer map collision at (1,−3/4,13/4)](https://www.wolframalpha.com/input?i=(-8x%5E3%20y%5E3%20z%20-%2024%20x%5E2%20y%5E4%20-%2012%20x%5E2%20y%5E2%20z%20-%2028%20x%20y%5E3%20-%206%20x%20y%20z%20-%208%20y%5E2%20-%20z%2C%2012%20x%5E3%20y%5E2%20z%20%2B%2036%20x%5E2%20y%5E3%20%2B%2012%20x%5E2%20y%20z%20%2B%2024%20x%20y%5E2%20%2B%203%20x%20z%20%2B%20y%2C%20-x%5E3%20z%20-%203%20x%5E2%20y%20%2B%20x)%20at%20x%3D1%2C%20y%3D-3%2F4%2C%20z%3D13%2F4)
- [integer map collision at (−1,3/4,13/4)](https://www.wolframalpha.com/input?i=(-8x%5E3%20y%5E3%20z%20-%2024%20x%5E2%20y%5E4%20-%2012%20x%5E2%20y%5E2%20z%20-%2028%20x%20y%5E3%20-%206%20x%20y%20z%20-%208%20y%5E2%20-%20z%2C%2012%20x%5E3%20y%5E2%20z%20%2B%2036%20x%5E2%20y%5E3%20%2B%2012%20x%5E2%20y%20z%20%2B%2024%20x%20y%5E2%20%2B%203%20x%20z%20%2B%20y%2C%20-x%5E3%20z%20-%203%20x%5E2%20y%20%2B%20x)%20at%20x%3D-1%2C%20y%3D3%2F4%2C%20z%3D13%2F4)
- [monodromy discriminant factorization](https://www.wolframalpha.com/input?i=factor%20-4(27%20a%20c%5E2%20-%209%20b%20c%20%2B%208)%5E2%20(27%20a%5E2%20c%5E2%20-%2018%20a%20b%20c%20%2B%2016%20a%20%2B%20b%5E3%20c%20-%20b%5E2))

## Files

- `repro.py` — single-file reproduction of claims 1–7 (13 assertions, exit code 0 = all pass)
- `scripts/` — individual investigation scripts (structure discovery, family theorem,
  conjugacy transport, monodromy, Dixmier endomorphism, cascade corollaries, cross-checks)

*Built with the Play harness, July 20, 2026. Independent re-derivation — no code or
values taken on trust from the announcement thread.*
