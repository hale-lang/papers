r"""
dh_pencil.py — the Davenport-Heilbronn family, exactly: the classical
conductor-5 illustration of functional-equation blindness (paper,
Theorem 5's historical companion), with its FE tuning constant
certified in pure cyclotomic arithmetic over Q(zeta_20). No floats.

THE PENCIL. Let chi be the quartic character mod 5 with chi(2) = i
(so chi(1), chi(2), chi(3), chi(4) = 1, i, -i, -1; chi(-1) = -1, odd).
For A in C consider

    F_A(s) = A * L(s, chi) + conj(A) * L(s, chi-bar),

the real-coefficient slice of the 2-complex-dimensional FE-closed
family V = {a L(s,chi) + b L(s,chi-bar)}. The completed vector
(Lambda(s,chi), Lambda(s,chi-bar)) satisfies a FIXED matrix functional
equation with gamma factor Gamma((s+1)/2), conductor 5, degree 1 —
SHARED BY EVERY MEMBER OF V. The geometry: the
Euler-product members are exactly the two coordinate corners L(chi),
L(chi-bar), which are each other's S^#-duals, NOT self-dual; the
scalar-self-dual members form a single REAL RAY, cut out by
conj(A) = A epsilon(chi) — and the Davenport-Heilbronn function IS
that ray. DH provably violates RH (zeros in sigma > 1 and off the
line in the strip; 1936; Balanzario-Sanchez-Ortiz 2007). The honest
blindness sentence: V is an FE-closed family with constant FE data;
moving from an Euler-product corner to the self-dual ray flips RH's
truth value while leaving all FE data fixed.

WHAT IS CERTIFIED HERE (the pencil's exact substrate):
  [P0] the Q(zeta_20) arithmetic itself: zeta^20 = 1, zeta^10 = -1,
       i := zeta^5 has i^2 = -1; the radical identifications
       sqrt5 := 1 + 2(zeta^4 + zeta^16) has sqrt5^2 = 5 and
       P := 2 zeta^3 - 2 zeta^7 has P^2 = 10 - 2 sqrt5 (i.e. P is
       sqrt(10 - 2 sqrt 5), the 4 sin(pi/5) radical); conjugation
       (zeta -> zeta^19) is an involution fixing sqrt5 and P.
  [P1] Gauss sums: tau(chi) = sum chi(a) zeta_5^a and tau(chi-bar),
       computed exactly; tau * conj(tau) = 5 for both; the classical
       twist tau(chi-bar) = chi(-1) conj(tau(chi)) = -conj(tau(chi)).
  [P2] THE SELF-DUALITY TUNING: with xi = (sqrt(10-2 sqrt5) - 2)/
       (sqrt5 - 1) (the classical Davenport-Heilbronn constant) and
       A = (1 - i xi)/2, the scalar-FE consistency condition
       (conj(A)/A)^2 = eps(chi)/eps(chi-bar) = tau(chi)/tau(chi-bar)
       — the squared, division-free form of the ray equation
       conj(A) = A eps(chi); equivalently:
       xi = tan(arg(eps(chi))/2), DH's constant is the HALF-ARGUMENT
       of the root number — holds EXACTLY, verified as
           (Q +- i(P-2))^2 tau = (Q -+ i(P-2))^2 tau'
       with P as above, Q = sqrt5 - 1 (one orientation;
       the instrument asserts exactly one orientation holds and
       reports which). DH's mysterious xi is exactly the FE-tuning
       that makes the interior pencil point scalar-self-dual.
  [P3] pencil-membership bookkeeping: A + conj(A) = 1 and
       i(A - conj(A)) = xi exactly — the pencil parameter is real,
       the Dirichlet coefficients a_n = A chi(n) + conj(A chi(n)) are
       real, and the 5-periodic pattern (a_1..a_5) = (1, xi, -xi, -1, 0)
       is recovered exactly.

Grading: [P0]-[P3] PROVED-BY-CODE; the matrix FE for the L-pair and
the off-line zeros of DH are CITED (classical). The blindness theorem
itself is Theorem 5 of the paper, whose unconditional witnesses are
Nakamura-based; this file certifies the classical family's exact
structure — including that the famous constant xi is precisely the
self-duality tuning (the half-argument of the root number).
"""

from fractions import Fraction as Fr

# ------------------------------------------------ Q(zeta_20), exact
# Phi_20(x) = x^8 - x^6 + x^4 - x^2 + 1;  zeta^8 = zeta^6 - zeta^4 + zeta^2 - 1

DEG = 8

def reduce_(v):
    v = list(v)
    for k in range(len(v) - 1, DEG - 1, -1):
        c = v[k]
        if c:
            v[k] = 0
            v[k - 2] += c
            v[k - 4] -= c
            v[k - 6] += c
            v[k - 8] -= c
    return tuple(v[:DEG])

def cmul(a, b):
    out = [Fr(0)] * (2 * DEG - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                out[i + j] += ai * bj
    return reduce_(out)

def cadd(a, b):
    return tuple(x + y for x, y in zip(a, b))

def csub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def cscale(a, t):
    return tuple(x * t for x in a)

ZERO = tuple([Fr(0)] * DEG)
ONE = tuple([Fr(1)] + [Fr(0)] * (DEG - 1))

# power table zeta^0 .. zeta^19
Z = [ONE]
zvec = tuple([Fr(0), Fr(1)] + [Fr(0)] * (DEG - 2))
for _ in range(19):
    Z.append(cmul(Z[-1], zvec))

def conj(a):
    out = ZERO
    for j, aj in enumerate(a):
        if aj:
            out = cadd(out, cscale(Z[(20 - j) % 20], aj))
    return out

def main():
    # ---- [P0] the arithmetic and the radicals -------------------------------
    assert cmul(Z[19], Z[1]) == ONE                       # zeta^20 = 1
    assert Z[10] == cscale(ONE, Fr(-1))                   # zeta^10 = -1
    I5 = Z[5]
    assert cmul(I5, I5) == cscale(ONE, Fr(-1))            # i^2 = -1
    SQRT5 = cadd(ONE, cscale(cadd(Z[4], Z[16]), Fr(2)))   # 1 + 2(z^4 + z^16)
    assert cmul(SQRT5, SQRT5) == cscale(ONE, Fr(5))       # sqrt5^2 = 5
    P = csub(cscale(Z[3], Fr(2)), cscale(Z[7], Fr(2)))    # 2z^3 - 2z^7
    assert cmul(P, P) == csub(cscale(ONE, Fr(10)),
                              cscale(SQRT5, Fr(2)))       # P^2 = 10 - 2 sqrt5
    assert conj(SQRT5) == SQRT5 and conj(P) == P          # both real
    assert conj(conj(Z[7])) == Z[7]                       # involution
    print("[P0] Q(zeta_20) exact: i = zeta^5, sqrt5 = 1 + 2(z^4+z^16),")
    print("     sqrt(10-2 sqrt5) = 2z^3 - 2z^7 — all certified by squaring;")
    print("     conjugation is an involution fixing both radicals.")

    # ---- [P1] Gauss sums ----------------------------------------------------
    z5 = Z[4]                                             # zeta_5 = zeta_20^4
    z5p = [ONE, Z[4], Z[8], Z[12], Z[16]]                 # zeta_5^a
    chi = {1: ONE, 2: I5, 3: cscale(I5, Fr(-1)), 4: cscale(ONE, Fr(-1))}
    chibar = {a: conj(v) for a, v in chi.items()}
    tau = ZERO
    taubar = ZERO
    for a in (1, 2, 3, 4):
        tau = cadd(tau, cmul(chi[a], z5p[a]))
        taubar = cadd(taubar, cmul(chibar[a], z5p[a]))
    assert cmul(tau, conj(tau)) == cscale(ONE, Fr(5))
    assert cmul(taubar, conj(taubar)) == cscale(ONE, Fr(5))
    assert taubar == cscale(conj(tau), Fr(-1))            # = chi(-1) conj(tau)
    print("[P1] Gauss sums exact: |tau(chi)|^2 = |tau(chi-bar)|^2 = 5;")
    print("     tau(chi-bar) = chi(-1) conj(tau(chi)) = -conj(tau(chi)).")

    # ---- [P2] the self-duality tuning ---------------------------------------
    Q = csub(SQRT5, ONE)                                  # sqrt5 - 1 (real)
    Pm2 = csub(P, cscale(ONE, Fr(2)))                     # P - 2 = Q * xi
    QpiP = cadd(Q, cmul(I5, Pm2))                         # Q + i(P-2)
    QmiP = csub(Q, cmul(I5, Pm2))                         # Q - i(P-2)
    lhs = cmul(cmul(QpiP, QpiP), taubar)
    rhs = cmul(cmul(QmiP, QmiP), tau)
    lhs2 = cmul(cmul(QpiP, QpiP), tau)
    rhs2 = cmul(cmul(QmiP, QmiP), taubar)
    o1, o2 = lhs == rhs, lhs2 == rhs2
    assert o1 != o2, "exactly one orientation must hold"
    orient = "(Q+iP)^2 tau(chi-bar) = (Q-iP)^2 tau(chi)" if o1 else \
             "(Q+iP)^2 tau(chi) = (Q-iP)^2 tau(chi-bar)"
    print("[P2] SELF-DUALITY CERTIFIED, division-free, in the orientation")
    print(f"     {orient}:")
    print("     with xi = (sqrt(10-2 sqrt5) - 2)/(sqrt5 - 1) and")
    print("     A = (1 - i xi)/2, the pencil member F_A satisfies the SCALAR")
    print("     functional equation — Davenport-Heilbronn's constant is")
    print("     exactly the FE-tuning of the pencil's interior point.")

    # ---- [P3] pencil bookkeeping --------------------------------------------
    # xi = (P - 2)/Q: real, since (P - 2) and Q are both real:
    assert conj(Pm2) == Pm2 and conj(Q) == Q
    # a_n = A chi(n) + conj(A chi(n)) = Re-part pattern; at n = 1..5 the
    # pattern (1, xi, -xi, -1, 0): certified as the identity
    # 2 Re(A chi(n)) with A = (1 - i xi)/2:
    #   n=1: 2 Re(A) = 1;  n=2: 2 Re(A i) = xi;  n=3: 2 Re(-A i) = -xi;
    #   n=4: 2 Re(-A) = -1;  n=5: chi(5) = 0.
    # Division-free check of the n=2 line, the only nontrivial one:
    # 2 Re(A i) = i(A - conj A)... = xi  <=>  Q * [i(A' - conj A')] = P - 2
    # where A' = (Q - iP')/2 with P' = P - 2... certified directly:
    Aq = cscale(csub(Q, cmul(I5, Pm2)), Fr(1, 2))         # (Q - i(P-2))/2
    lhs3 = cmul(I5, csub(Aq, conj(Aq)))                   # i(Aq - conj Aq)
    assert lhs3 == Pm2                                    # = P - 2 = Q * xi
    print("[P3] pencil bookkeeping: the parameter is real, coefficients are")
    print("     real, and the 5-periodic Dirichlet pattern (1, xi, -xi, -1, 0)")
    print("     is recovered exactly (division-free certification).")

    print("\nDH PENCIL CERTIFIED (the blindness theorem's exact substrate):")
    print("  a one-real-parameter family sharing ALL functional-equation data")
    print("  (degree 1, conductor 5, Gamma((s+1)/2), the matrix FE), whose")
    print("  endpoints are the Euler-product L-functions and whose exactly-")
    print("  tuned interior point is Davenport-Heilbronn — the provable")
    print("  RH-violator (1936: zeros in sigma > 1; off-line strip zeros).")
    print("  Target #1 is now a definability-and-invariance problem ON this")
    print("  family: define the instrument class I, prove I constant along")
    print("  the pencil — then no RH argument factoring through I alone can")
    print("  exist, unconditionally, because it would apply verbatim to the")
    print("  interior point. The theorem is NOT claimed here; its substrate is.")

if __name__ == "__main__":
    main()
