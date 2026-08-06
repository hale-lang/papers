r"""
two_meters.py — exact-arithmetic instantiation of the "residue ledger" reading
at the minimal open frontier of the Hodge conjecture (Weil classes on abelian
fourfolds with multiplication by Q(i)).

Everything is exact (sympy Rational / Gaussian rationals). No floats except in
the Tier-1 near-miss check, which is a numerical verification of an asymptotic.

Objects
-------
V = Q^8, with two commuting complex structures:
  J_K : the ARITHMETIC i (multiplication by i in K = Q(i), V = K^4)
  J_t : the GEOMETRIC i (the Hodge/complex structure of the torus R^8/Z^8)

Residue meter: the derivation extension D(J) of J to Lambda^k V.
  On the (p,q) part of Lambda^k(V (x) C), D(J) acts as (p-q)*i.
  Weil operator C = exp((pi/2) D). "Residue-free" (type (p,p)) <=> D x = 0.

Weil space: W = ker(D(J_K)^2 + 16) in Lambda^4 V_Q  (the +-4i eigenpair of the
  arithmetic meter) = the classical Lambda^4_K V, a 2-dimensional Q-space.

Checks
------
[T1] near-miss asymptotics: complex roots of g(x)+eps sit at a +- i*sqrt(2 eps/g''(a)).
[A] dim_Q W = 2.
[B] BALANCED geometric structure (CM signature (2,2)): D(J_A) W = 0
    -> the arithmetic entries are residue-free for the geometric meter (Hodge).
[C] DETUNED structure (signature (3,1)): D(J_B)^2 = -4 on W
    -> the same rational entries read phase +-2i: NOT Hodge. Resonance lost.
[D] Divisor-algebra escape at a verified point of the Weil family:
    NS = rational (1,1) classes = ker D_2(J_C) on Lambda^2 V_Q;
    Div^2 = span{ n /\ n' } in Lambda^4; check W  (intersect)  Div^2 = 0.
    By semicontinuity (a flat rational class (1,1) at very general t is (1,1)
    everywhere, CDK), NS_verygeneral is contained in NS at ANY point, so
    escape at one point certifies escape for the very general member.
[E] (optional) existence of a compatible polarization at the test point.
"""

from itertools import combinations
from sympy import Rational, Matrix, eye, zeros, I as sI, nsimplify, im, re
import sys

# ----------------------------------------------------------------------------
# Tier 1: near-miss asymptotics
# ----------------------------------------------------------------------------
def tier1_near_miss():
    import numpy as np
    # g(x) = (x-1)^2 (x+2) = x^3 - 3x + 2 ; double root a=1, g''(1) = 6
    a, kappa = 1.0, 6.0
    print("[T1] near-miss roots of g(x)+eps vs prediction a +- i*sqrt(2 eps/kappa):")
    for eps in (1e-2, 1e-4, 1e-6):
        roots = np.roots([1.0, 0.0, -3.0, 2.0 + eps])
        pair = sorted([r for r in roots if abs(r.imag) > 1e-12], key=lambda z: z.imag)
        pred = (2.0 * eps / kappa) ** 0.5
        z = pair[1]
        print(f"     eps={eps:8.0e}  root={z.real:+.6f}{z.imag:+.6f}i   "
              f"pred Im={pred:.6f}   rel.err(Im)={abs(z.imag-pred)/pred:.2e}")

# ----------------------------------------------------------------------------
# Exterior algebra machinery (exact)
# ----------------------------------------------------------------------------
N = 8
B2 = list(combinations(range(N), 2))
B4 = list(combinations(range(N), 4))
IX2 = {t: k for k, t in enumerate(B2)}
IX4 = {t: k for k, t in enumerate(B4)}

def normalize(tup):
    """Sort a tuple of distinct indices; return (sign, sorted tuple)."""
    t = list(tup)
    sign = 1
    for i in range(len(t)):
        for j in range(len(t) - 1 - i):
            if t[j] > t[j + 1]:
                t[j], t[j + 1] = t[j + 1], t[j]
                sign = -sign
    return sign, tuple(t)

def derivation_matrix(J, basis, ix):
    """D(J)(v1^...^vk) = sum_j v1^...^(J vj)^...^vk on Lambda^k."""
    n = len(basis)
    D = zeros(n, n)
    for col, T in enumerate(basis):
        for p, ip in enumerate(T):
            for l in range(N):
                c = J[l, ip]
                if c == 0:
                    continue
                if l == ip:
                    D[col_idx := col, col] = D[col, col] + c  # diagonal slot
                    continue
                if l in T:
                    continue
                newT = list(T)
                newT[p] = l
                s, st = normalize(newT)
                D[ix[st], col] += s * c
    return D

def wedge22(u, v):
    """Wedge two Lambda^2 vectors (coords over B2) into a Lambda^4 vector."""
    out = zeros(len(B4), 1)
    for iS, S in enumerate(B2):
        cu = u[iS]
        if cu == 0:
            continue
        for iT, T in enumerate(B2):
            cv = v[iT]
            if cv == 0:
                continue
            if set(S) & set(T):
                continue
            s, st = normalize(S + T)
            out[IX4[st], 0] += s * cu * cv
    return out

# ----------------------------------------------------------------------------
# The two i's
# ----------------------------------------------------------------------------
Rrot = Matrix([[0, -1], [1, 0]])

def blockdiag(blocks):
    M = zeros(8, 8)
    for b, blk in enumerate(blocks):
        M[2*b:2*b+2, 2*b:2*b+2] = blk
    return M

J_K = blockdiag([Rrot, Rrot, Rrot, Rrot])          # arithmetic i  (K = Q(i))
J_A = blockdiag([Rrot, Rrot, -Rrot, -Rrot])        # geometric i, signature (2,2)
J_B = blockdiag([Rrot, Rrot, Rrot, -Rrot])         # geometric i, signature (3,1)

def k_linear_real(Q):
    """Realify a 4x4 matrix over K=Q(i) (sympy entries a+b*I) to 8x8 over Q."""
    M = zeros(8, 8)
    for r in range(4):
        for c in range(4):
            q = Q[r, c]
            a, b = nsimplify(re(q)), nsimplify(im(q))
            M[2*r:2*r+2, 2*c:2*c+2] = a * eye(2) + b * Rrot
    return M

def main():
    tier1_near_miss()

    assert J_K * J_K == -eye(8) and J_A * J_A == -eye(8) and J_B * J_B == -eye(8)
    assert J_K * J_A == J_A * J_K and J_K * J_B == J_B * J_K

    print("\nBuilding residue meters D(J) on Lambda^4 (70-dim) ...")
    DK4 = derivation_matrix(J_K, B4, IX4)
    DA4 = derivation_matrix(J_A, B4, IX4)
    DB4 = derivation_matrix(J_B, B4, IX4)

    # [A] Weil space = +-4i eigenpair of the arithmetic meter, over Q
    Wbasis = (DK4 * DK4 + 16 * eye(70)).nullspace()
    print(f"[A] dim_Q ker(D(J_K)^2 + 16) on Lambda^4_Q  =  {len(Wbasis)}   (expect 2)")
    assert len(Wbasis) == 2

    # [B] balanced signature -> residue-free for the geometric meter
    okB = all((DA4 * w) == zeros(70, 1) for w in Wbasis)
    print(f"[B] balanced J_A (sig (2,2)):  D(J_A) W = 0  ->  {okB}   (Weil entries are Hodge)")
    assert okB

    # [C] detuned signature -> meter reads phase +-2i
    okC = all((DB4 * (DB4 * w)) == -4 * w for w in Wbasis)
    print(f"[C] detuned J_B (sig (3,1)):   D(J_B)^2 = -4 on W  ->  {okC}   (pure (3,1)+(1,3): NOT Hodge)")
    assert okC

    # [D] divisor-algebra escape at a point of the Weil family
    print("\n[D] hunting a verified point of the Weil family (K-linear conjugates of J_A):")
    trial_Qs = [
        Matrix([[1, sI, 0, 1], [0, 1, 1, 0], [sI, 0, 1, sI], [1, 0, 0, 1]]),
        Matrix([[1, 1, 0, sI], [sI, 1, 1, 0], [0, 1, 1, 1], [0, sI, 0, 1]]),
        Matrix([[2, sI, 1, 0], [0, 1, sI, 1], [1, 0, 1, 0], [sI, 1, 0, 1]]),
    ]
    certified = False
    for k, Q in enumerate(trial_Qs):
        if Q.det() == 0:
            continue
        Mr = k_linear_real(Q)
        J_C = Mr * J_A * Mr.inv()
        assert J_C * J_C == -eye(8) and J_C * J_K == J_K * J_C

        DC4 = derivation_matrix(J_C, B4, IX4)
        assert all((DC4 * w) == zeros(70, 1) for w in Wbasis), \
            "Weil entries must stay Hodge across the family (signature invariant)"

        DC2 = derivation_matrix(J_C, B2, IX2)
        NS = DC2.nullspace()          # rational (1,1) classes = NS (x) Q at this point
        prods = []
        for i in range(len(NS)):
            for j in range(i, len(NS)):
                p = wedge22(NS[i], NS[j])
                if any(x != 0 for x in p):
                    prods.append(p)
        Div = Matrix.hstack(*prods) if prods else zeros(70, 1)
        rD = Div.rank()
        rDW = Matrix.hstack(Div, *Wbasis).rank()
        inter = rD + 2 - rDW
        print(f"     point #{k}: dim NS_Q = {len(NS)}, dim <NS.NS> = {rD}, "
              f"dim(W  cap  <NS.NS>) = {inter}")
        if inter == 0:
            print(f"     -> ESCAPE CERTIFIED at point #{k}: W  cap  Div^2 = 0.")
            print("        Semicontinuity (CDK): NS(very general) c= NS(this point),")
            print("        so the Weil entries escape the divisor algebra for the")
            print("        very general member of the family.")
            certified = True
            break
    if not certified:
        print("     -> no escape at tried points (all too split); symbolic-parameter"
              " run owed.")

    # [E] optional: compatible polarization at J_A (existence check, numeric)
    try:
        import numpy as np
        # solve for antisymmetric E with J_A^T E J_A = E; then need E(x, J_A y) > 0
        rows = []
        for a in range(8):
            for b in range(8):
                row = [0]*28
                # E[a,b] expressed through basis of antisymmetric matrices
                def coef(i_, j_, a_, b_):
                    if (i_, j_) == (a_, b_):
                        return 1
                    if (i_, j_) == (b_, a_):
                        return -1
                    return 0
                # (J^T E J - E)[a,b] = sum_{i,j} J[i,a] E[i,j] J[j,b] - E[a,b]
                for idx, (i_, j_) in enumerate(B2):
                    v = 0
                    for ii in range(8):
                        for jj in range(8):
                            c = J_A[ii, a] * J_A[jj, b]
                            if c != 0:
                                v += c * coef(ii, jj, i_, j_)
                    v -= coef(a, b, i_, j_)
                    row[idx] = float(v)
                rows.append(row)
        A = np.array(rows)
        _, s, Vt = np.linalg.svd(A)
        null = Vt[s.size - (s < 1e-9).sum():] if (s < 1e-9).sum() else Vt[len(s):]
        found = False
        rng = np.random.default_rng(7)
        for _ in range(200):
            c = rng.standard_normal(null.shape[0]) @ null if null.size else None
            if c is None:
                break
            E = np.zeros((8, 8))
            for idx, (i_, j_) in enumerate(B2):
                E[i_, j_], E[j_, i_] = c[idx], -c[idx]
            S = E @ np.array(J_A, dtype=float)
            S = (S + S.T) / 2
            if np.linalg.eigvalsh(S).min() > 1e-8:
                found = True
                break
        print(f"\n[E] compatible polarization at J_A exists: {found} "
              f"(invariant antisym E with E(x,J_A y) pos.def.; numeric search)")
    except Exception as e:
        print(f"\n[E] polarization check skipped ({e})")

    print("\nAll asserts passed." if True else "")

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
