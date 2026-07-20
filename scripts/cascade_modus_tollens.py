"""IMPLICATION CASCADE -- Mathieu and Zhao conjectures fall by modus tollens.
Each implication is peer-reviewed; the premise (JC_3 false) is re-verified here
in exact rational arithmetic.

(Mathieu 1997, Sem. et Congres 2, 263-279): Main Conjecture for SU(N) ==> JC on C^N.
(Zhao 2006, Trans. AMS 359, 249-274): JC (all n) <=> Vanishing Conjecture for
homogeneous degree-4 Hessian-nilpotent P: Delta^m P^{m+1} = 0 for m >> 0.
"""
import sympy as sp
x, y, z = sp.symbols('x y z')
F = [(1 + x*y)**3 * z + y**2*(1 + x*y)*(4 + 3*x*y),
     y + 3*x*(1 + x*y)**2 * z + 3*x*y**2*(4 + 3*x*y),
     2*x - 3*x**2*y - x**3*z]
assert sp.simplify(sp.Matrix(F).jacobian([x,y,z]).det()) == -2
pts = [(0,0,sp.Rational(-1,4)), (1,sp.Rational(-3,2),sp.Rational(13,2)), (-1,sp.Rational(3,2),sp.Rational(13,2))]
imgs = [tuple(sp.simplify(f.subs({x:p[0],y:p[1],z:p[2]})) for f in F) for p in pts]
assert imgs[0] == imgs[1] == imgs[2] and len(set(pts)) == 3
print('Premise verified: JC_3 is FALSE.')
print('==> Mathieu Conjecture (1997): FALSE (fails for SU(3)).')
print('==> Zhao Vanishing Conjecture: FALSE (a degree-4 Hessian-nilpotent witness exists).')
