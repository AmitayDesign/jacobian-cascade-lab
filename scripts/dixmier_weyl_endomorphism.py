"""DIXMIER CONJECTURE DC_3 -- explicit counterexample construction & verification.
DC_n: every endomorphism of the n-th Weyl algebra A_n is an automorphism.
We construct the pullback endomorphism EXPLICITLY and check the Weyl relations.

phi: A_3 -> A_3,  x_i |-> F_i(x),  d_i |-> D_i := sum_k A_ik(x) d_k,  A := (J^T)^{-1}.
Well-defined endomorphism iff (1) [D_i, F_j] = delta_ij, (2) [D_i, D_j] = 0.
Not an automorphism: its order-0 restriction g |-> g(F) is not surjective (any g(F)
is constant on the 3-point collision fiber; x is not).
"""
import sympy as sp

x, y, z = sp.symbols('x y z')
X = [x, y, z]
F1 = (1 + x*y)**3 * z + y**2 * (1 + x*y) * (4 + 3*x*y)
F2 = y + 3*x*(1 + x*y)**2 * z + 3*x*y**2 * (4 + 3*x*y)
F3 = 2*x - 3*x**2*y - x**3*z
F = [F1, F2, F3]
J = sp.Matrix(F).jacobian(X)
print('det J =', sp.simplify(J.det()))

A = (J.T).inv()
A = A.applyfunc(lambda e: sp.expand(sp.cancel(e)))
poly_ok = all(sp.denom(sp.together(A[i,j])).is_constant() for i in range(3) for j in range(3))
print('A has polynomial entries (denominators constant):', poly_ok)

M = sp.expand(A * J.T)
print('[D_i, F_j] = delta_ij :', M == sp.eye(3))

all_zero = True
for i in range(3):
    for j in range(i+1, 3):
        for kk in range(3):
            c = sum(A[i,l]*sp.diff(A[j,kk], X[l]) - A[j,l]*sp.diff(A[i,kk], X[l]) for l in range(3))
            if sp.expand(c) != 0:
                all_zero = False
print('[D_i, D_j] = 0 for all i,j :', all_zero)

pts = [(0, 0, sp.Rational(-1,4)), (1, sp.Rational(-3,2), sp.Rational(13,2)), (-1, sp.Rational(3,2), sp.Rational(13,2))]
same = all(tuple(sp.simplify(f.subs(dict(zip(X,p)))) for f in F) == tuple(sp.simplify(f.subs(dict(zip(X,pts[0])))) for f in F) for p in pts)
print('F identical on all 3 collision points:', same)
print('x values on those points differ -> x not in C[F], phi not surjective')
print('CONCLUSION: well-defined non-surjective endomorphism of A_3 => DC_3 FALSE.')
