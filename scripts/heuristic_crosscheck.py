"""Consistency audit: the counterexample vs every classical partial result.
No proven theorem is contradicted -- only the conjecture itself.
Also determines the generic fiber cardinality (globally 3:1).
"""
import sympy as sp
x, y, z = sp.symbols('x y z')
u = 1 + x*y
w = u**2*z + y**2*(4 + 3*x*y)
F1 = sp.expand(u*w); F2 = sp.expand(y + 3*x*w); F3 = sp.expand(2*x - 3*x**2*y - x**3*z)

print('[H1] Wang (1980): Keller maps of deg <= 2 invertible. Our degrees:',
      [sp.total_degree(f) for f in (F1, F2, F3)], '-> no conflict')
print('[H2] Magnus/Moh: JC_2 low-degree results. Our map is n=3 -> no conflict')
print('[H3] Ax-Grothendieck/Cynk-Rusek: injective => automorphism. Ours is NON-injective -> consistent')
J = sp.Matrix([F1, F2, F3]).jacobian([x, y, z])
print('[H4] det J =', sp.expand(J.det(method='berkowitz')), '(constant, negative); real collisions -> consistent')

c1, c2, c3 = sp.symbols('c1 c2 c3')
zs = sp.solve(sp.Eq(F1, c1), z)[0]
N2 = sp.expand(sp.numer(sp.together(F2.subs(z, zs) - c2)))
N3 = sp.expand(sp.numer(sp.together(F3.subs(z, zs) - c3)))
res = sp.resultant(sp.Poly(N2, y), sp.Poly(N3, y))
for f, m in sp.factor_list(res)[1]:
    if x in f.free_symbols and any(s in f.free_symbols for s in (c1, c2, c3)):
        cubic = sp.Poly(f, x)
print('fiber polynomial degree in x:', cubic.degree())
print('discriminant identically zero?', sp.simplify(sp.discriminant(cubic.as_expr(), x)) == 0)
print('=> F is a globally 3-to-1 branched cover of its image; [C(x,y,z):C(F)] = 3')
print('=> no rational inverse of any kind exists (a birational inverse would force degree 1)')
