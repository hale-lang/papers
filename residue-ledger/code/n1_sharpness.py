r"""
n1_sharpness.py — the n = 1 boundary case (abelian surfaces): Theorem 1
FAILS for a single rational Weil class at n = 1, exactly as the referee
review of v0.7 states. This script is the boundary regression.

Setting: V = Q^4 = K^2, K = Q(i); J_K two rotation blocks; split point
J_A = R (+) (-R) (signature (1,1)); E = (-R) (+) R. Weil plane
W = ker(D_2(J_K)^2 + 4) in Lambda^2 Q^4 (the +-2i eigenpair, dim 2).

Expected (referee's reconstruction, verified here):
  dim_R T(polarized) = 6 (dim_C A_2 = 3);  K-cell = 2 (dim_C 1);
  SINGLE rational Weil entry: rank_R mu = 2 (rank_C 1 != n(n+1) = 2),
    kernel_R = 4 (complex kernel 2 — STRICTLY BIGGER than the cell);
  JOINT (both entries): rank_R = 4 (rank_C 2), kernel_R = 2 = the cell.

Explanation: the arithmetic-meter grades of the w_+ and w_- contributions
coincide at n = 1 ((2n-2)i = 0), so the conjugate channels can cancel for
a single rational class; only the full rational plane cuts out the Weil
germ. Theorem 1 therefore requires n >= 2, with this as the sharpness
statement.
"""

from itertools import combinations
from sympy import Matrix, eye, zeros

N = 4
B2 = list(combinations(range(N), 2))
IX2 = {t: k for k, t in enumerate(B2)}
R = Matrix([[0, -1], [1, 0]])

def blockdiag(blocks):
    M = zeros(N, N)
    for b, blk in enumerate(blocks):
        M[2*b:2*b+2, 2*b:2*b+2] = blk
    return M

J_K = blockdiag([R, R])
J_A = blockdiag([R, -R])
E = blockdiag([-R, R])

def normalize(tup):
    t = list(tup)
    s = 1
    for i in range(len(t)):
        for j in range(len(t) - 1 - i):
            if t[j] > t[j+1]:
                t[j], t[j+1] = t[j+1], t[j]
                s = -s
    return s, tuple(t)

def deriv(J):
    D = zeros(len(B2), len(B2))
    for col, T in enumerate(B2):
        for p, ip in enumerate(T):
            for l in range(N):
                c = J[l, ip]
                if c == 0:
                    continue
                if l == ip:
                    D[col, col] += c
                    continue
                if l in T:
                    continue
                newT = list(T)
                newT[p] = l
                s, st = normalize(newT)
                D[IX2[st], col] += s * c
    return D

def tangent(J, extra_K=False):
    cols = []
    for a in range(N):
        for b in range(N):
            U = zeros(N, N)
            U[a, b] = 1
            rows = [ (U*J + J*U)[i, j] for i in range(N) for j in range(N) ]
            rows += [ (U.T*E*J + J.T*E*U)[i, j] for i in range(N) for j in range(N) ]
            if extra_K:
                rows += [ (U*J_K - J_K*U)[i, j] for i in range(N) for j in range(N) ]
            cols.append(rows)
    A = Matrix(cols).T
    out = []
    for v in A.nullspace():
        out.append(Matrix(N, N, lambda i, j, v=v: v[N*i + j, 0]))
    return out

def main():
    DK = deriv(J_K)
    Wb = (DK*DK + 4*eye(len(B2))).nullspace()
    assert len(Wb) == 2
    DA = deriv(J_A)
    for w in Wb:
        assert DA * w == zeros(len(B2), 1)       # Hodge at balance (1,1)

    T = tangent(J_A)
    TK = tangent(J_A, extra_K=True)
    assert len(T) == 6 and len(TK) == 2
    print(f"[n=1] dim_R T = {len(T)} (A_2: 3 complex);  K-cell = {len(TK)} (1 complex)")

    Ds = [deriv(dJ) for dJ in T]
    M1 = Matrix.hstack(*[D * Wb[0] for D in Ds])
    M2 = Matrix.hstack(*[D * Wb[1] for D in Ds])
    Mj = Matrix.vstack(M1, M2)
    r1, r2, rj = M1.rank(), M2.rank(), Mj.rank()
    print(f"[n=1] rank_R mu: single entries {r1}, {r2}; joint {rj}")
    assert r1 == 2 and r2 == 2, "single-class rank_C = 1, NOT n(n+1) = 2"
    assert rj == 4, "joint rank_C = 2: the plane, not one class, cuts the germ"
    print("[n=1] CONFIRMED: a single rational Weil class has complex kernel 2 >")
    print("      1 = dim(Weil cell) — Theorem 1 fails at n = 1 and requires the")
    print("      full rational plane there; the n >= 2 hypothesis is necessary,")
    print("      and the conjugate-channel grading argument shows exactly why:")
    print("      the two arithmetic grades +-(2n-2)i coincide at n = 1.")

if __name__ == "__main__":
    main()
