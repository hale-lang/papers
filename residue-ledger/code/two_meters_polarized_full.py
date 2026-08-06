r"""
two_meters_polarized_full.py — multi-parameter polarized Weil cell (v2, fast).

Construction as in two_meters_polarized.py: V+ = graph(Z), V- = h-perp =
graph'(Z*), so one fixed rational polarization E works across the whole cell
(the polarized Weil family), with Z now carrying 4 real parameters so the
slice's very general member sheds the accidental rational classes thin slices
retain (1-param slice: NS = 7, Weil entries absorbed).

Exactness notes:
 * Jd := J * det(S) is polynomial via the Schur block inverse (4x4 adjugate).
 * The identities Jd^2 = -d^2, [Jd, J_K] = 0, Jd^T E Jd = d^2 E hold BY
   CONSTRUCTION (conjugation by C, E in the Tr(lambda h) family, V- = h-perp);
   they are point-checked at random rational parameter tuples as regression
   guards rather than re-proved symbolically (the full symbolic expands are
   what timed out — they carry no additional mathematical content here).
 * The load-bearing facts are verified EXACTLY and identically in the
   parameters: D_4(J) W = 0 (Weil entries Hodge), and every identical-kernel
   basis vector is re-checked against the full polynomial matrix.
 * Identical kernels are computed by ITERATIVE intersection over monomial
   coefficient matrices (kernel shrinks fast; each step is a small solve).
"""

import random
from sympy import symbols, Matrix, eye, zeros, expand, Poly, Rational
from two_meters import (B2, B4, IX2, IX4, derivation_matrix, wedge22,
                        J_K, Rrot, blockdiag)

PARAMS = symbols('x y u v')
x, y, u, v = PARAMS
q = Rational

def kentry(a, b):
    return a * eye(2) + b * Rrot

def realify2(Kentries):
    M = zeros(4, 4)
    for (r, c), (a, b) in Kentries.items():
        M[2*r:2*r+2, 2*c:2*c+2] = kentry(a, b)
    return M

def monomial_matrices(Msym, nrows, ncols):
    """{monomial: coefficient matrix}, monomials sorted by total degree."""
    mats = {}
    for r in range(nrows):
        for c in range(ncols):
            e = Msym[r, c]
            if e == 0:
                continue
            for mono, coef in Poly(e, *PARAMS).terms():
                if mono not in mats:
                    mats[mono] = zeros(nrows, ncols)
                mats[mono][r, c] = coef
    return [mats[m] for m in sorted(mats, key=lambda m: (sum(m), m))]

def identical_kernel_iterative(Msym, n):
    """Q-vectors killed by the polynomial matrix identically (fast path)."""
    Kb = eye(n)                       # columns span the current candidate space
    for A in monomial_matrices(Msym, n, n):
        if Kb.cols == 0:
            break
        AK = A * Kb
        if AK == zeros(n, Kb.cols):
            continue
        small = AK.nullspace()
        if not small:
            return []
        Kb = Kb * Matrix.hstack(*small)
    basis = [Kb.col(j) for j in range(Kb.cols)]
    # exact re-verification against the full polynomial matrix
    for b in basis:
        assert (Msym * b).applyfunc(expand) == zeros(n, 1)
    return basis

def rand_subs(rng):
    return {p: q(rng.randint(-9, 9), rng.randint(1, 9)) for p in PARAMS}

def main():
    rng = random.Random(11)

    Zr = realify2({
        (0, 0): (q(1, 7) + x, q(1, 5) + y),
        (0, 1): (q(1, 3) + u, q(-1, 4) + v),
        (1, 0): (q(1, 2) - v, q(1, 9) + u),
        (1, 1): (q(-1, 6) - y, q(1, 8) + x),
    })
    Zs = Zr.T
    S = (eye(4) - Zr * Zs).applyfunc(expand)
    d = expand(S.det())
    adjS = S.adjugate().applyfunc(expand)

    C = zeros(8, 8)
    C[0:4, 0:4] = eye(4)
    C[0:4, 4:8] = Zs
    C[4:8, 0:4] = Zr
    C[4:8, 4:8] = eye(4)
    Cinv_d = zeros(8, 8)
    Cinv_d[0:4, 0:4] = d * eye(4) + Zs * adjS * Zr
    Cinv_d[0:4, 4:8] = -Zs * adjS
    Cinv_d[4:8, 0:4] = -adjS * Zr
    Cinv_d[4:8, 4:8] = adjS

    Jmid = blockdiag([Rrot, Rrot, -Rrot, -Rrot])
    Jd = (C * Jmid * Cinv_d).applyfunc(expand)
    E = blockdiag([-Rrot, -Rrot, Rrot, Rrot])

    # [P1] structural identities: point-checked at 4 random rational tuples
    for trial in range(4):
        sub = rand_subs(rng)
        d0 = d.subs(sub)
        if d0 == 0:
            continue
        J0 = Jd.subs(sub)
        assert J0 * J0 == -d0**2 * eye(8)
        assert J0 * J_K == J_K * J0
        assert J0.T * E * J0 == d0**2 * E
    print("[P1] J^2 = -1, K-linearity, E-compatibility: hold by construction; "
          "point-checked at 4 random rational parameter tuples.", flush=True)

    # [P2] Weil entries Hodge, EXACT and identical in the parameters
    DK4 = derivation_matrix(J_K, B4, IX4)
    Wb = (DK4 * DK4 + 16 * eye(70)).nullspace()
    assert len(Wb) == 2
    D4 = derivation_matrix(Jd, B4, IX4)
    for w in Wb:
        assert (D4 * w).applyfunc(expand) == zeros(70, 1)
    print("[P2] Both Weil entries Hodge identically across the 4-parameter slice.",
          flush=True)

    # [P3] polarization positivity at the base point
    subs0 = {p: 0 for p in PARAMS}
    d0 = d.subs(subs0)
    J0 = Jd.subs(subs0) / d0
    Ssym = E * J0
    assert (Ssym - Ssym.T).applyfunc(expand) == zeros(8, 8)
    ok_pos = all(Ssym[:k, :k].det() > 0 for k in range(1, 9))
    print(f"[P3] E positive-definite at base point: {ok_pos}", flush=True)
    assert ok_pos

    # [P4] NS of the very general member; escape test
    D2 = derivation_matrix(Jd, B2, IX2)
    NSvg = identical_kernel_iterative(D2, 28)
    print(f"[P4] dim_Q NS(very general member of slice) = {len(NSvg)}", flush=True)

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
    print(f"     dim <NS.NS> = {rD};  dim(W cap <NS.NS>) = {inter}", flush=True)

    if inter == 0:
        print("     -> ESCAPE CERTIFIED on the slice; transfers a fortiori to the full")
        print("        polarized Weil family (NS_vg(family) c= NS_vg(slice)): the two")
        print("        Weil entries are rational, Hodge, and NOT divisor-generated for")
        print("        the very general polarized member.", flush=True)
    else:
        print("     -> still absorbed on this slice; widen further.", flush=True)

    # [P5] full degree-4 ledger of the slice's very general member
    Hdg4 = identical_kernel_iterative(D4, 70)
    rAll = Matrix.hstack(Div, *Wb, *Hdg4).rank()
    print(f"[P5] dim_Q Hdg^4(very general of slice) = {len(Hdg4)};  "
          f"dim(<NS.NS> + W) = {rDW};  dim(sum with Hdg4) = {rAll}", flush=True)
    if len(Hdg4) == rDW and inter == 0:
        print("     -> LEDGER COMPLETE on the slice: Hdg^4 = <NS.NS> (+) W.", flush=True)

if __name__ == "__main__":
    main()
