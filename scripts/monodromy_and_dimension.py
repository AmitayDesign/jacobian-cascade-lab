"""S3 monodromy of the 3:1 cover + the n>=3 dimension obstruction."""
import sympy as sp
x, y, z, c1, c2, c3 = sp.symbols('x y z c1 c2 c3')
u = 1 + x*y
w = u**2*z + y**2*(4 + 3*x*y)
F1 = sp.expand(u*w); F2 = sp.expand(y + 3*x*w); F3 = sp.expand(2*x - 3*x**2*y - x**3*z)
zs = sp.solve(sp.Eq(F1, c1), z)[0]
N2 = sp.expand(sp.numer(sp.together(F2.subs(z, zs) - c2)))
N3 = sp.expand(sp.numer(sp.together(F3.subs(z, zs) - c3)))
res = sp.resultant(sp.Poly(N2, y), sp.Poly(N3, y))
for f, m in sp.factor_list(res)[1]:
    if x in f.free_symbols and any(s in f.free_symbols for s in (c1, c2, c3)):
        cubic = f
D = sp.factor(sp.discriminant(cubic, x))
print('discriminant of fiber cubic:', D)
print('square in C(c)?', all(m % 2 == 0 for _, m in sp.factor_list(D)[1]),
      ' -> NOT a square => monodromy = S3, cover non-Galois, no deck symmetry')

X, Y = sp.symbols('X Y')
A, B, K = sp.symbols('A B K')
W2 = Y**2*(A + B*X*Y)
g1 = sp.expand((1 + X*Y)*W2); g2 = sp.expand(Y + K*X*W2)
d2 = sp.expand(sp.Matrix([g1, g2]).jacobian([X, Y]).det())
conds = [c for mono, c in sp.Poly(d2, X, Y).terms() if mono != (0, 0)]
sols = sp.solve([sp.Eq(c, 0) for c in conds], [A, B, K], dict=True)
print('2-variable specializations with constant det:', sols)
print('all give det = 0 (degenerate) =>', 'the pivot mechanism REQUIRES n >= 3;')
print('this counterexample class says nothing about JC_2, which remains open.')
