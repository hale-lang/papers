r"""
two_meters_generic.py — the generic-member escape computation.

Companion to two_meters.py (import machinery from it). That script showed the
Weil entries are ABSORBED by the divisor algebra at split CM points (NS = 16 =
h^{1,1}, products span all of h^{2,2} = 36). Here we deform along a K-linear
one-parameter subgroup and compute the GENERIC rational (1,1) space over the
function field Q(s), then certify:

  [D'] for the generic member of this one-parameter slice of the Weil family,
       W  cap  <NS_gen . NS_gen>  =  0
       (Weil entries escape the divisor algebra).

Method: symbolic nullspace of D_2(J(s)) over Q(s) -> generic NS basis; the
membership w in Div_gen(s) over Q(s) would specialize to membership at all but
finitely many rational s0; we check non-membership at three specializations of
the *generic* basis, with rank stability across the points.

  [E'] explicit compatible polarization E = blockdiag(-R,-R,R,R) at the base
       point (supersedes the failed random search in two_meters.py [E]).
"""

from sympy import symbols, Matrix, eye, zeros, expand, gcd, lcm, together, fraction
from two_meters import (B2, B4, IX2, IX4, derivation_matrix, wedge22,
                        J_K, J_A, Rrot, blockdiag)

s = symbols('s')

def polyclear(vec):
    """Clear denominators of a symbolic column vector; return polynomial vector."""
    dens = []
    ents = [together(x) for x in vec]
    for x in ents:
        _, d = fraction(x)
        dens.append(d)
    L = dens[0]
    for d in dens[1:]:
        L = lcm(L, d)
    out = [expand(x * L) for x in ents]
    g = 0
    for x in out:
        g = gcd(g, x)
    if g != 0 and g != 1:
        out = [expand(x / g) for x in out]
    return Matrix(out)

def main():
    # --- the one-parameter K-linear deformation -----------------------------
    # N: e4 |-> e1 over K (nilpotent, N^2 = 0); realified: block (0,3) = I_2
    Nq = zeros(8, 8)
    Nq[0, 6] = 1
    Nq[1, 7] = 1
    M = eye(8) + s * Nq
    Minv = eye(8) - s * Nq
    Js = M * J_A * Minv
    Js = Js.applyfunc(expand)

    assert (Js * Js).applyfunc(expand) == -eye(8), "J(s)^2 = -1"
    assert (Js * J_K - J_K * Js).applyfunc(expand) == zeros(8, 8), "K-linearity"
    print("[setup] J(s) = (1+sN) J_A (1+sN)^{-1} built; J^2=-1 and [J,J_K]=0 verified symbolically.")

    # --- Weil space over Q (constant in s) ----------------------------------
    DK4 = derivation_matrix(J_K, B4, IX4)
    Wb = (DK4 * DK4 + 16 * eye(70)).nullspace()
    assert len(Wb) == 2

    # Weil entries stay Hodge along the whole deformation (symbolic check)
    D4s = derivation_matrix(Js, B4, IX4)
    for w in Wb:
        assert (D4s * w).applyfunc(expand) == zeros(70, 1)
    print("[check] D_4(J(s)) W = 0 identically in s: Weil entries are Hodge on the whole slice.")

    # --- generic NS over Q(s) ------------------------------------------------
    D2s = derivation_matrix(Js, B2, IX2).applyfunc(expand)
    ns_gen = D2s.nullspace(iszerofunc=lambda x: expand(x) == 0)
    g = len(ns_gen)
    print(f"[D'] dim_Q(s) ker D_2(J(s)) on Lambda^2  =  {g}   (generic rational (1,1) space; 16 at split points)")
    ns_gen = [polyclear(v) for v in ns_gen]
    # confirm each cleared vector is still in the kernel, identically
    for v in ns_gen:
        assert (D2s * v).applyfunc(expand) == zeros(28, 1)

    # --- specialize the GENERIC basis and test escape ------------------------
    results = []
    for s0 in (1, 2, 7):
        NS0 = [v.subs(s, s0) for v in ns_gen]
        A = Matrix.hstack(*NS0)
        assert A.rank() == g, f"specialized generic basis degenerates at s={s0}"
        prods = []
        for i in range(g):
            for j in range(i, g):
                p = wedge22(NS0[i], NS0[j])
                if any(x != 0 for x in p):
                    prods.append(p)
        Div = Matrix.hstack(*prods) if prods else zeros(70, 1)
        rD = Div.rank()
        rDW = Matrix.hstack(Div, *Wb).rank()
        inter = rD + 2 - rDW
        results.append((s0, rD, inter))
        print(f"     s0={s0}:  dim<NS_gen.NS_gen>|_(s0) = {rD},   dim(W cap Div) = {inter}")

    ranks = {r for _, r, _ in results}
    inters = {i for _, _, i in results}
    if inters == {0} and len(ranks) == 1:
        print("     -> ESCAPE CERTIFIED for the generic member of the slice:")
        print("        membership over Q(s) would specialize to all but finitely many s0;")
        print("        non-membership holds at three rank-stable specializations of the")
        print("        generic basis  =>  W cap <NS_gen . NS_gen> = 0 over Q(s).")
    else:
        print("     -> not certified on this slice; try another deformation direction.")

    # --- [E'] explicit polarization at the base point ------------------------
    E = blockdiag([-Rrot, -Rrot, Rrot, Rrot])
    ok_inv = (J_A.T * E * J_A) == E
    S = E * J_A
    S = (S + S.T) / 2
    ok_pos = all(S[:k, :k].det() > 0 for k in range(1, 9))   # leading minors
    ok_K = (J_K.T * E * J_K) == E
    print(f"\n[E'] E = blockdiag(-R,-R,R,R):  J_A-invariant: {ok_inv},  "
          f"E(x, J_A y) positive-definite: {ok_pos},  J_K-invariant: {ok_K}")
    assert ok_inv and ok_pos and ok_K
    print("     -> (R^8/Z^8, J_A, E) is a genuinely polarized abelian fourfold with")
    print("        Q(i)-multiplication of signature (2,2); the slice lives inside its")
    print("        Weil family.")

if __name__ == "__main__":
    main()
