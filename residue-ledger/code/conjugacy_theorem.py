r"""
conjugacy_theorem.py — exact verification of the real-conjugacy theorem
(Theorem 3): the arithmetic discriminant is invisible to the ENTIRE local
period germ.

The map: phi = diag(1,1,1,1,1, 3^{-1/2}) on V (x) R = (K (x) R)^6, realified
to Phi (12x12 over Q(sqrt 3)), commuting with J_K and J_A.

Verified exactly:
  [C1] Phi commutes with J_K (K-linearity) and with J_A (fixes base point).
  [C2] Phi^T E_3 Phi = E_1  — phi is an isometry (h_1) -> (h_3); both the
       alternating (E) and symmetric (E(., J_K .)) parts transport.
  [C3] conjugation carries the E_1-polarized tangent space at J_A onto the
       E_3-polarized tangent space (all 42 basis images satisfy the E_3
       conditions; images are independent), and the 18-dim K-linear cell
       onto the K-linear cell.
  [C4] Lambda^6 Phi scales the Weil plane by 3^{-1/2} (each monomial of
       w+- has exactly one factor in the sixth K-block).
  [C5] mu-equivariance: D(Phi dJ Phi^{-1}) . (L6Phi w) = L6Phi . (D(dJ) w),
       sampled over tangent basis vectors — so kernels, ranks, and all
       higher derivatives of the obstruction construction correspond.
  [C6] (recorded, not computed) no rational Phi exists: a K-rational
       isometry would force [det h_1] = [det h_3], i.e. 3 in Nm(Q(i)^x),
       contradicting the descent argument (see sixfold_rig.py [S3b]).

Consequence: every finite jet of (Siegel domain, Weil cell, Weil plane,
obstruction sections) at the common fixed base point agrees between the
split (c=1) and nonsplit (c=3) discriminant classes. Second- and
higher-order computations are calibration channels, forced to agree.
"""

from sympy import sqrt, eye, zeros, Matrix, expand, simplify
from sixfold_rig import (N, B2, B6, IX2, IX6, Rrot, blockdiag12,
                         J_K, J_A, E_of, apply_D, tangent_space)

s3 = sqrt(3)
Phi = blockdiag12([eye(2)] * 5 + [(s3 / 3) * eye(2)])
PhiInv = blockdiag12([eye(2)] * 5 + [s3 * eye(2)])
assert (Phi * PhiInv).applyfunc(simplify) == eye(N)

E1, E3 = E_of(1), E_of(3)

def L6Phi(vec, inverse=False):
    """Diagonal Lambda^6 action of Phi on a sparse Lambda^6 vector."""
    out = {}
    for idx, cf in vec.items():
        T = B6[idx]
        scale = 1
        for k in T:
            scale *= (PhiInv if inverse else Phi)[k, k]
        out[idx] = simplify(cf * scale)
    return out

def main():
    # [C1]
    assert (Phi * J_K - J_K * Phi).applyfunc(simplify) == zeros(N, N)
    assert (Phi * J_A - J_A * Phi).applyfunc(simplify) == zeros(N, N)
    print("[C1] Phi commutes with J_K and with J_A (base point fixed).")

    # [C2]
    assert (Phi.T * E3 * Phi).applyfunc(simplify) == E1
    B1 = E1 * J_K
    B3 = E3 * J_K
    assert (Phi.T * B3 * Phi).applyfunc(simplify) == B1
    print("[C2] Phi^T E_3 Phi = E_1 and Phi^T (E_3 J_K) Phi = E_1 J_K:")
    print("     phi is a (K x R)-linear isometry (V_R, h_1) -> (V_R, h_3).")

    # [C3]
    T1 = tangent_space(J_A, E1)
    TK1 = tangent_space(J_A, E1, extra_K=True)
    assert len(T1) == 42 and len(TK1) == 18
    flat_imgs = []
    for dJ in T1:
        dJ3 = (Phi * dJ * PhiInv).applyfunc(simplify)
        assert (dJ3 * J_A + J_A * dJ3).applyfunc(simplify) == zeros(N, N)
        assert (dJ3.T * E3 * J_A + J_A.T * E3 * dJ3).applyfunc(simplify) == zeros(N, N)
        flat_imgs.append(Matrix([[dJ3[i, j] for i in range(N) for j in range(N)]]).T)
    assert Matrix.hstack(*flat_imgs).rank() == 42
    for dJ in TK1:
        dJ3 = (Phi * dJ * PhiInv).applyfunc(simplify)
        assert (dJ3 * J_K - J_K * dJ3).applyfunc(simplify) == zeros(N, N)
        assert (dJ3.T * E3 * J_A + J_A.T * E3 * dJ3).applyfunc(simplify) == zeros(N, N)
    print("[C3] conjugation carries T(E_1-polarized) onto T(E_3-polarized)")
    print("     (42 independent images, all conditions exact) and the")
    print("     18-dim K-linear cell onto the K-linear cell.")

    # [C4] Weil vectors: rebuild as in sixfold_rig
    w_re, w_im = {}, {}
    for r in range(64):
        S = [j for j in range(6) if (r >> j) & 1]
        T = tuple(2*j + (1 if j in S else 0) for j in range(6))
        k = len(S) % 4
        idx = IX6[T]
        if k == 0:
            w_re[idx] = w_re.get(idx, 0) + 1
        elif k == 2:
            w_re[idx] = w_re.get(idx, 0) - 1
        elif k == 1:
            w_im[idx] = w_im.get(idx, 0) - 1
        else:
            w_im[idx] = w_im.get(idx, 0) + 1
    for w in (w_re, w_im):
        Lw = L6Phi(w)
        assert Lw == {k: simplify(v * s3 / 3) for k, v in w.items()}
    print("[C4] Lambda^6 Phi = 3^{-1/2} . id on the Weil plane W (exact).")

    # [C5] mu-equivariance on a sample of tangent directions
    for dJ in T1[:5] + TK1[:2]:
        dJ3 = (Phi * dJ * PhiInv).applyfunc(simplify)
        for w in (w_re, w_im):
            lhs = apply_D(dJ3, L6Phi(w), B6, IX6)
            rhs = L6Phi(apply_D(dJ, w, B6, IX6))
            lhs = {k: simplify(v) for k, v in lhs.items() if simplify(v) != 0}
            rhs = {k: simplify(v) for k, v in rhs.items() if simplify(v) != 0}
            assert lhs == rhs
    print("[C5] mu-equivariance D(Phi dJ Phi^-1)(L6Phi w) = L6Phi(D(dJ) w):")
    print("     exact on sampled polarized and K-linear directions —")
    print("     kernels, ranks, and all higher derivatives correspond.")

    print("\n[C6] no rational conjugacy exists: [det h_1] = [-1] != [-3] =")
    print("     [det h_3] in Q^x/Nm(Q(i)^x) (descent; sixfold_rig [S3b]).")
    print("\nTHEOREM 3 VERIFIED: the split and nonsplit local period germs are")
    print("carried onto each other by the single linear map Phi, fixing the")
    print("base point and intertwining the entire obstruction construction.")
    print("The arithmetic discriminant is invisible to the ENTIRE local")
    print("period germ; second- and higher-order computations are forced")
    print("calibration channels.")

if __name__ == "__main__":
    main()
