"""THE FAMILY THEOREM and its proof by diagonal conjugacy.
Template: u = 1+xy, w = u^2 z + y^2(a + b xy),
F1 = u*w, F2 = y + k*x*w, F3 = c0*x + c1*x^2 y + c2*x^3 z.
Solving the 12 vanishing conditions for constant det gives the unique
non-degenerate family a=12/k, b=9/k, c0=-6c2/k, c1=9c2/k, det J = 6 c2/k.
Then D_out o F_3 o D_in = F_k with explicit diagonal linear maps, transporting
the 3-point collision to every member.
"""
import sympy as sp
x, y, z = sp.symbols('x y z')
a, b, k, c0, c1, c2 = sp.symbols('a b k c0 c1 c2')
u = 1 + x*y
w = u**2*z + y**2*(a + b*x*y)
F1 = sp.expand(u*w); F2 = sp.expand(y + k*x*w); F3 = c0*x + c1*x**2*y + c2*x**3*z
d = sp.expand(sp.Matrix([F1, F2, F3]).jacobian([x, y, z]).det(method='berkowitz'))
eqs = {sp.simplify(c) for mono, c in sp.Poly(d, x, y, z).terms() if mono != (0, 0, 0)}
print('vanishing conditions:', len(eqs))
for s in sp.solve([sp.Eq(e, 0) for e in eqs], [a, b, k, c0, c1, c2], dict=True):
    print('family:', s, '-> det =', sp.factor(sp.simplify(d.subs(s))))

# conjugacy transport of the collision (v = free scaling parameter):
kk, v = sp.symbols('kk v', nonzero=True)
wk = u**2*z + y**2*(sp.Rational(12)/kk + sp.Rational(9)/kk*x*y)
G = [sp.expand(u*wk), sp.expand(y + kk*x*wk), sp.expand(-6*x/kk + 9*x**2*y/kk + x**3*z)]
Q0 = (0, 0, sp.Rational(-27, 4)/(kk**3*v**2))
Q1 = (kk*v/3, sp.Rational(-9, 2)/(kk*v), sp.Rational(351, 2)/(kk**3*v**2))
Q2 = (-kk*v/3, sp.Rational(9, 2)/(kk*v), sp.Rational(351, 2)/(kk**3*v**2))
im = [tuple(sp.simplify(g.subs(dict(zip((x, y, z), Q)))) for g in G) for Q in (Q0, Q1, Q2)]
print('collision transported to arbitrary (k, v):',
      all(sp.simplify(im[0][i] - im[j][i]) == 0 for j in (1, 2) for i in range(3)))
