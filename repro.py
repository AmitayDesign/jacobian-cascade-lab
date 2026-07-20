"""
JACOBIAN CASCADE LAB - single-file reproduction of every claim.
Requires: python3 + sympy  (pip install sympy)
Run: python3 repro.py     Expected: 13 PASS lines, exit code 0.
"""
import sympy as sp

PASS = True
def check(label, ok):
    global PASS
    PASS = PASS and bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")

x, y, z = sp.symbols('x y z')

print("(1)+(2) Keller property, collision, pivot structure")
u = 1 + x*y
w = u**2*z + y**2*(4 + 3*x*y)
F1 = sp.expand((1 + x*y)**3*z + y**2*(1 + x*y)*(4 + 3*x*y))
F2 = sp.expand(y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y))
F3 = sp.expand(2*x - 3*x**2*y - x**3*z)
check("F1 = u*w", sp.expand(F1 - u*w) == 0)
check("F2 = y + 3x*w", sp.expand(F2 - (y + 3*x*w)) == 0)
J = sp.Matrix([F1, F2, F3]).jacobian([x, y, z])
d = sp.expand(J.det(method='berkowitz'))
check("det J = -2 (constant)", d == -2)
pts = [(0, 0, sp.Rational(-1, 4)), (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
       (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
imgs = [tuple(sp.simplify(f.subs(dict(zip((x, y, z), P)))) for f in (F1, F2, F3)) for P in pts]
check("3 distinct points, 1 image  => JC_3 FALSE", imgs[0] == imgs[1] == imgs[2] and len(set(pts)) == 3)

print("(3) Integer normalization, det J = +1 exactly")
H1 = -8*x**3*y**3*z - 24*x**2*y**4 - 12*x**2*y**2*z - 28*x*y**3 - 6*x*y*z - 8*y**2 - z
H2 = 12*x**3*y**2*z + 36*x**2*y**3 + 12*x**2*y*z + 24*x*y**2 + 3*x*z + y
H3 = -x**3*z - 3*x**2*y + x
dH = sp.expand(sp.Matrix([H1, H2, H3]).jacobian([x, y, z]).det(method='berkowitz'))
check("det J_H = 1", dH == 1)
ptsH = [(0, 0, sp.Rational(-1, 8)), (1, sp.Rational(-3, 4), sp.Rational(13, 4)),
        (-1, sp.Rational(3, 4), sp.Rational(13, 4))]
imgsH = [tuple(sp.simplify(h.subs(dict(zip((x, y, z), P)))) for h in (H1, H2, H3)) for P in ptsH]
check("H collides 3 points -> (1/8, 0, 0)", imgsH[0] == imgsH[1] == imgsH[2] == (sp.Rational(1, 8), 0, 0))

print("(4) Two-parameter family theorem")
k, c2, v = sp.symbols('k c2 v', nonzero=True)
wk = u**2*z + y**2*(sp.Rational(12)/k + sp.Rational(9)/k*x*y)
G1 = sp.expand(u*wk)
G2 = sp.expand(y + k*x*wk)
G3 = sp.expand(c2*(-6*x/k + 9*x**2*y/k + x**3*z))
dG = sp.simplify(sp.Matrix([G1, G2, G3]).jacobian([x, y, z]).det(method='berkowitz'))
check("det J(F_{k,c2}) = 6*c2/k, constant in x,y,z", sp.simplify(dG - 6*c2/k) == 0)
Q0 = (0, 0, sp.Rational(-27, 4)/(k**3*v**2))
Q1 = (k*v/3, sp.Rational(-9, 2)/(k*v), sp.Rational(351, 2)/(k**3*v**2))
Q2 = (-k*v/3, sp.Rational(9, 2)/(k*v), sp.Rational(351, 2)/(k**3*v**2))
imQ = [tuple(sp.simplify(g.subs(dict(zip((x, y, z), Q)))) for g in (G1, G2, G3)) for Q in (Q0, Q1, Q2)]
same = all(sp.simplify(imQ[0][i] - imQ[j][i]) == 0 for j in (1, 2) for i in range(3))
check("collision transports to arbitrary (k,v): F_k(Q0)=F_k(Q1)=F_k(Q2) symbolically", same)
check("published map is the member k=3, c2=-1",
      sp.simplify(dG.subs({k: 3, c2: -1}) + 2) == 0)

print("(5)+(6) Fiber degree 3 and S3 monodromy")
c1s, c2s, c3s = sp.symbols('C1 C2 C3')
zs = sp.solve(sp.Eq(F1, c1s), z)[0]
N2 = sp.expand(sp.numer(sp.together(F2.subs(z, zs) - c2s)))
N3 = sp.expand(sp.numer(sp.together(F3.subs(z, zs) - c3s)))
res = sp.resultant(sp.Poly(N2, y), sp.Poly(N3, y))
cubic = None
for f, m in sp.factor_list(res)[1]:
    if x in f.free_symbols and any(s in f.free_symbols for s in (c1s, c2s, c3s)):
        cubic = f
check("fiber polynomial has degree 3 in x", sp.Poly(cubic, x).degree() == 3)
D = sp.factor(sp.discriminant(cubic, x))
sq = sp.factor_list(D)
check("discriminant not identically 0 (map generically 3:1)", sp.simplify(D) != 0)
check("discriminant NOT a square in C(c) => monodromy S3, non-Galois cover",
      not all(m % 2 == 0 for _, m in sq[1]))

print("(7) The mechanism is intrinsically >= 3-dimensional")
X, Y = sp.symbols('X Y')
A, B, K = sp.symbols('A B K')
W2 = Y**2*(A + B*X*Y)
g1 = sp.expand((1 + X*Y)*W2)
g2 = sp.expand(Y + K*X*W2)
d2 = sp.expand(sp.Matrix([g1, g2]).jacobian([X, Y]).det())
conds = [c for mono, c in sp.Poly(d2, X, Y).terms() if mono != (0, 0)]
sols = sp.solve([sp.Eq(c, 0) for c in conds], [A, B, K], dict=True)
degenerate = all(sp.simplify(d2.subs(s)) == 0 for s in sols)
check("all constant-det specializations of the 2-var template are degenerate (det=0)", degenerate)

print()
print("ALL CHECKS PASSED" if PASS else "SOME CHECKS FAILED")
raise SystemExit(0 if PASS else 1)
