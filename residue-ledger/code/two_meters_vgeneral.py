r"""
two_meters_vgeneral.py — the very-general-member ledger, done right.

Lesson from two_meters_generic.py: conjugating J_A by a matrix with RATIONAL
(-function) entries is a Q-isogeny — the rational Hodge structure does not
move, and the Q(s)-kernel of D_2 is the wrong object (it stayed 16-dim).
The rational ledger only changes under IRRATIONAL deformation.

Correct object: for the family J(p), p = (s,t,u,v), the very general member's
rational (1,1) space is

    NS_vg = { v in Lambda^2 Q^8 : D_2(J(p)) v = 0 identically in p }
          = intersection of kernels of the coefficient matrices of D_2,

exactly (both inclusions), because at a transcendental parameter point a
Q-vector is killed iff it is killed coefficient-wise. No specialization
caveats.

The deformation directions: the four K-linear nilpotents mapping the
(f3,f4)-block to the (f1,f2)-block (with and without an i-twist) are a basis
of the tangent space of the U(2,2) period domain (dim_C 4) at the split point;
since all products N_i N_j = 0, M = I + sN1 + tN2 + uN3 + vN4 inverts exactly
to I - (...), and J(p) = M J_A M^{-1} sweeps an open cell of the WEIL FAMILY.
So "very general member of this slice" = very general member of the family.

Computations:
  [F] NS_vg (dim expected < 16), with identical-vanishing verification.
  [G] W stays Hodge identically across the family.
  [H] Hdg4_vg = rational classes (2,2) identically = the full degree-4 ledger
      of the very general member.
  [I] THE AUDIT TABLE: is Hdg4_vg = <NS_vg . NS_vg> (+) W ?
      (divisor-backed part + the two Weil entries, and nothing else)
"""

from sympy import symbols, Matrix, eye, zeros, expand, Poly
from two_meters import (B2, B4, IX2, IX4, derivation_matrix, wedge22,
                        J_K, J_A, Rrot, blockdiag)

PARAMS = symbols('p1:9')   # eight real parameters: the FULL open cell of the
                           # U(2,2) period domain (4 block positions x 2 twists)

def kblock(i, j, twist):
    """8x8 with 2x2 block at K-position (i,j): I2 (twist=0) or R (twist=1)."""
    M = zeros(8, 8)
    M[2*i:2*i+2, 2*j:2*j+2] = (Rrot if twist else eye(2))
    return M

def coefficient_matrices(Msym, nrows, ncols):
    """Split a polynomial matrix into {monomial: rational matrix}."""
    coeffs = {}
    for r in range(nrows):
        for c in range(ncols):
            e = expand(Msym[r, c])
            if e == 0:
                continue
            p = Poly(e, *PARAMS)
            for mono, coef in p.terms():
                if mono not in coeffs:
                    coeffs[mono] = zeros(nrows, ncols)
                coeffs[mono][r, c] = coef
    return coeffs

def identical_kernel(Msym, nrows, ncols):
    """Q-vectors killed by a polynomial matrix identically in the parameters."""
    coeffs = coefficient_matrices(Msym, nrows, ncols)
    stacked = Matrix.vstack(*coeffs.values())
    return stacked.nullspace()

def main():
    dirs = [kblock(i, j, tw) for i in (0, 1) for j in (2, 3) for tw in (0, 1)]
    assert len(dirs) == len(PARAMS) == 8
    for A in dirs:
        for Bm in dirs:
            assert A * Bm == zeros(8, 8)          # products vanish -> exact inverse
    Nsum = zeros(8, 8)
    for pk, Nk in zip(PARAMS, dirs):
        Nsum += pk * Nk
    M = eye(8) + Nsum
    Minv = eye(8) - Nsum
    Jp = (M * J_A * Minv).applyfunc(expand)

    assert (Jp * Jp).applyfunc(expand) == -eye(8)
    assert (Jp * J_K - J_K * Jp).applyfunc(expand) == zeros(8, 8)
    print("[setup] full 8-parameter cell of the Weil family built: J(p)^2 = -1, [J(p), J_K] = 0, identically.")

    # Weil space (constant in p)
    DK4 = derivation_matrix(J_K, B4, IX4)
    Wb = (DK4 * DK4 + 16 * eye(70)).nullspace()
    assert len(Wb) == 2

    # [G] W Hodge across the whole family
    D4p = derivation_matrix(Jp, B4, IX4)
    for w in Wb:
        assert (D4p * w).applyfunc(expand) == zeros(70, 1)
    print("[G] D_4(J(p)) W = 0 identically: the two Weil entries are Hodge on the whole family.")

    # [F] very-general NS
    D2p = derivation_matrix(Jp, B2, IX2)
    NSvg = identical_kernel(D2p, 28, 28)
    print(f"[F] dim_Q NS(very general member) = {len(NSvg)}    (split point had 16 = h^(1,1))")
    for x in NSvg:
        assert (D2p * x).applyfunc(expand) == zeros(28, 1)

    # [H] full degree-4 rational Hodge ledger of the very general member
    Hdg4 = identical_kernel(D4p, 70, 70)
    print(f"[H] dim_Q Hdg^4(very general member) = {len(Hdg4)}   (split point had 36 = h^(2,2))")

    # [I] the audit table
    prods = []
    g = len(NSvg)
    for i in range(g):
        for j in range(i, g):
            p4 = wedge22(NSvg[i], NSvg[j])
            if any(x != 0 for x in p4):
                prods.append(p4)
    Div = Matrix.hstack(*prods) if prods else zeros(70, 1)
    rD = Div.rank()
    rDW = Matrix.hstack(Div, *Wb).rank()
    inter = rD + 2 - rDW
    rAll = Matrix.hstack(Div, *Wb, *Hdg4).rank()
    print(f"[I] dim <NS.NS> = {rD};  dim(W cap <NS.NS>) = {inter};  "
          f"dim(<NS.NS> + W) = {rDW};  dim(<NS.NS> + W + Hdg4) = {rAll}")

    if inter == 0:
        print("    -> ESCAPE PROVED for the very general member of the Weil family:")
        print("       the two Weil entries are residue-free, rational, and NOT in the")
        print("       divisor algebra. (Transcendence argument; no specialization step.)")
    if rAll == rDW == rD + 2 and len(Hdg4) == rDW:
        print("    -> LEDGER COMPLETE: Hdg^4(very general) = <NS.NS> (+) W  exactly —")
        print("       every residue-free rational entry is either divisor-backed or one")
        print("       of the two Weil entries. The entire open frontier at this variety")
        print("       is the 2-dimensional Weil space.")
    elif len(Hdg4) != rDW:
        print(f"    -> NOTE: Hdg4 has dim {len(Hdg4)} vs <NS.NS>+W dim {rDW} — "
              f"additional unaccounted entries exist; report them honestly.")

if __name__ == "__main__":
    main()
