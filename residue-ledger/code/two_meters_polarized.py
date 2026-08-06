r"""
two_meters_polarized.py — the honest POLARIZED Weil family, and the escape
certificate for its very general member.

Fix for the lesson of two_meters_vgeneral.py (whose 8-parameter cell swept
K-linear complex structures WITHOUT a shared polarization, landing in a larger
PEL family with NS_vg = 4, Hdg4_vg = 11):

Over K = Q(i), a K-linear complex structure on V = K^4 is a choice of
2-dimensional K-subspace V+ (J = mult-by-i there, mult-by-(-i) on a chosen
complement). For the K-hermitian form h = diag(1,1,-1,-1), the E-compatible
choice is V- = h-perp of V+, and in graph coordinates:

    V+ = graph(Z)  = {(w, Zw)},      V- = graph'(Z*) = {(Z* y, y)},

Z a 2x2 K-matrix (the Harish-Chandra cell of the U(2,2) period domain,
8 real parameters). The rational form E = blockdiag(-R,-R,R,R) lies in the
Tr(lambda h) family, hence is J(Z)-invariant for EVERY Z — one fixed rational
polarization for the whole cell: this IS the polarized Weil family.

We take a one-real-parameter slice Z(x) = Z0 + x Z1 in a generic direction.
For the escape claim a slice is enough, a fortiori: identical vanishing on the
family implies identical vanishing on the slice, so

    NS_vg(full polarized family)  is contained in  NS_vg(slice),

and escape from the bigger algebra implies escape from the smaller.

All matrices polynomial via adjugates: J(x)*det = C * J_mid * adj(C).

Checks:
  [P1] Jd^2 = -det^2, K-linearity, and E-COMPATIBILITY, identically in x.
  [P2] Weil entries Hodge identically on the slice (signature (2,2) built in).
  [P3] polarization positivity of E at the base point x=0 (leading minors).
  [P4] NS_vg(slice) via coefficient kernels; audit table; escape vs W.
"""

from sympy import symbols, Matrix, eye, zeros, expand, Poly, Rational, nsimplify
from two_meters import (B2, B4, IX2, IX4, derivation_matrix, wedge22,
                        J_K, Rrot, blockdiag)

x = symbols('x')

def kentry(a, b):
    """Real 2x2 block for the K-scalar a + b i."""
    return a * eye(2) + b * Rrot

def kmat_real(Kentries):
    """Realify a 4x4 K-matrix given as {(r,c): (a,b)} with a,b in Q[x]."""
    M = zeros(8, 8)
    for (r, c), (a, b) in Kentries.items():
        M[2*r:2*r+2, 2*c:2*c+2] = kentry(a, b)
    return M

def coeff_kernel_1var(Msym, nrows, ncols):
    """Q-vectors killed by a polynomial (in x) matrix identically."""
    mats = {}
    for r in range(nrows):
        for c in range(ncols):
            e = expand(Msym[r, c])
            if e == 0:
                continue
            for k, coef in enumerate(reversed(Poly(e, x).all_coeffs())):
                if coef == 0:
                    continue
                if k not in mats:
                    mats[k] = zeros(nrows, ncols)
                mats[k][r, c] = coef
    return Matrix.vstack(*mats.values()).nullspace()

def main():
    q = Rational
    # Z(x) = Z0 + x Z1, entries (a, b) meaning a + b i
    Z = {(0, 0): (q(1, 7) + 0*x, q(1, 5) + 0*x),
         (0, 1): (q(1, 3) + 0*x, q(-1, 4) + 0*x),
         (1, 0): (q(1, 2) + 0*x, q(1, 9) + 0*x),
         (1, 1): (q(-1, 6) + 0*x, q(1, 8) + 0*x)}
    Z1 = {(0, 0): (1, 0), (0, 1): (1, 1), (1, 0): (1, -1), (1, 1): (2, 0)}
    for k in Z:
        a, b = Z[k]
        da, db = Z1[k]
        Z[k] = (a + x*da, b + x*db)

    # C = [[I, Z*], [Z, I]] in K-blocks (V+ columns first, then V-)
    Ke = {}
    for r in range(2):
        Ke[(r, r)] = (1, 0)
        Ke[(r + 2, r + 2)] = (1, 0)
    for (r, c), (a, b) in Z.items():
        Ke[(r + 2, c)] = (a, b)          # Z block (rows f3,f4; cols V+)
        Ke[(c, r + 2)] = (a, -b)         # Z* block (conjugate transpose)
    C = kmat_real(Ke)

    Jmid = blockdiag([Rrot, Rrot, -Rrot, -Rrot])
    det = C.det()
    adj = C.adjugate()
    Jd = (C * Jmid * adj).applyfunc(expand)      # Jd = J(x) * det(x), polynomial

    E = blockdiag([-Rrot, -Rrot, Rrot, Rrot])

    # [P1] structural identities, identically in x
    assert Poly(det, x).all_coeffs()[-1] != 0 or det.subs(x, 0) != 0
    assert (Jd * Jd).applyfunc(expand) == (-det**2 * eye(8)).applyfunc(expand)
    assert (Jd * J_K - J_K * Jd).applyfunc(expand) == zeros(8, 8)
    assert (Jd.T * E * Jd).applyfunc(expand) == (det**2 * E).applyfunc(expand)
    print("[P1] J(x)^2 = -1, [J, J_K] = 0, and E(Jx, Jy) = E(x, y) — all identically in x.")
    print("     One fixed rational polarization E across the slice: this is the polarized Weil family.")

    # [P2] Weil entries Hodge along the slice
    DK4 = derivation_matrix(J_K, B4, IX4)
    Wb = (DK4 * DK4 + 16 * eye(70)).nullspace()
    assert len(Wb) == 2
    D4 = derivation_matrix(Jd, B4, IX4)
    for w in Wb:
        assert (D4 * w).applyfunc(expand) == zeros(70, 1)
    print("[P2] D_4(J(x)) W = 0 identically: both Weil entries are Hodge on the whole slice.")

    # [P3] positivity of E at the base point (x = 0)
    d0 = det.subs(x, 0)
    J0 = Jd.subs(x, 0) / d0
    S = E * J0
    S = (S + S.T) / 2
    assert (E * J0 - (E * J0).T).applyfunc(nsimplify) == zeros(8, 8), "E*J0 symmetric"
    minors = [S[:k, :k].det() for k in range(1, 9)]
    ok_pos = all(m > 0 for m in minors)
    print(f"[P3] E(x, J(0) y) positive-definite at the base point: {ok_pos}")
    assert ok_pos

    # [P4] the audit
    D2 = derivation_matrix(Jd, B2, IX2)
    NSvg = coeff_kernel_1var(D2, 28, 28)
    print(f"[P4] dim_Q NS(very general member of slice) = {len(NSvg)}")
    for v in NSvg:
        assert (D2 * v).applyfunc(expand) == zeros(28, 1)

    Hdg4 = coeff_kernel_1var(D4, 70, 70)
    print(f"     dim_Q Hdg^4(very general member of slice) = {len(Hdg4)}")

    g = len(NSvg)
    prods = []
    for i in range(g):
        for j in range(i, g):
            p4 = wedge22(NSvg[i], NSvg[j])
            if any(e != 0 for e in p4):
                prods.append(p4)
    Div = Matrix.hstack(*prods) if prods else zeros(70, 1)
    rD = Div.rank()
    rDW = Matrix.hstack(Div, *Wb).rank()
    inter = rD + 2 - rDW
    rAll = Matrix.hstack(Div, *Wb, *Hdg4).rank()
    print(f"     dim <NS.NS> = {rD};  dim(W cap <NS.NS>) = {inter};  "
          f"dim(<NS.NS> + W) = {rDW};  dim Hdg4 = {len(Hdg4)};  dim(sum) = {rAll}")

    if inter == 0:
        print("\n     -> ESCAPE CERTIFIED, and it transfers a fortiori to the FULL")
        print("        polarized Weil family: NS_vg(family) c= NS_vg(slice), so the two")
        print("        Weil entries are rational, residue-free, Hodge on the family, and")
        print("        NOT in the divisor algebra of the very general polarized member.")
    if len(Hdg4) == rDW == rD + 2 == 3:
        print("     -> LEDGER COMPLETE on the slice: Hdg^4 = <NS.NS> (+) W, dims 1 + 2.")
        print("        Every residue-free rational degree-4 entry of the very general")
        print("        member is either the square of the polarization or a Weil entry.")

if __name__ == "__main__":
    main()
