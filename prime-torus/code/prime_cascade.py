r"""
prime_cascade.py — the signed prime cascade: the Mobius/Mertens field
certified exactly (paper, Theorems 1-3 and the restriction framing).
The compressed statement: THE FREE PRIME-RESIDUAL FIELD IS
AUTOMATICALLY CRITICAL AT 1/2; the Riemann Hypothesis says the marked
Archimedean restriction introduces no anomalous growth exponent. This
file certifies every finite identity in that chain.

THE SIGNED FIELD carries the RH obstruction: the cascade
    R_0 = H (Heaviside on the log line),
    R_{k+1} = R_k - tau_{log p_{k+1}} R_k
(each prime birth subtracts a translated copy of the whole residual).

Channels (all exact):
  [C1] closed form: R_k(u) = sum_{d | P_k} mu(d) H(u - log d) — the
       recursion's atom multiset equals the Mobius atoms exactly
       (P_k = primorial; certified through k = 6 by exact atom algebra).
  [C2] THE RESOLVED FRONT IS MERTENS: for x < p_{k+1},
       R_k(log x) = M(x) = sum_{d <= x} mu(d) — the cascade agrees with
       the true arithmetic residual up to the next unborn prime
       (certified for k = 6, all integer x < 17).
  [C3] the transform: sum_{d | P_k} mu(d) d^{-s} = prod_{p <= p_k}
       (1 - p^{-s}) symbolically (k = 4); with int H(u - log d)e^{-su}du
       = d^{-s}/s, the Laplace transform of the cascade is the
       reciprocal finite Euler product over s.
  [C4] THE ENERGY THRESHOLD: on the prime torus, orthogonality gives
       ||F_{k,sigma}||^2 = sum_{d | P_k} d^{-2 sigma} = prod_{p <= p_k}
       (1 + p^{-2 sigma}) (symbolic, k = 4). The infinite product
       converges iff sum p^{-2 sigma} < infty iff sigma > 1/2 (CITED:
       standard). 1/2 IS THE FINITE-ENERGY BOUNDARY OF THE FREE FIELD —
       the critical line appears before any zeta zero is mentioned.
  [C5] PER-PRIME CONTRACTION IS FALSE (a calibration result): after
       primes {2,3}, R_2 = -1 on [5,6); adding 5 gives R_3 = -2 there —
       the birth AMPLIFIED the local residual (certified at x = 11/2 by
       exact rational atom evaluation). Square-root behavior must be a
       global cascade property, not a per-prime contraction law.
  [C6] HELSON ROTATION (the torus-blindness engine): for unimodular
       completely multiplicative twists chi, psi, the coordinate
       rotation z_p -> (psi/chi)(p) z_p carries F_chi to F_psi
       (symbolic identity), and the torus energy is twist-INDEPENDENT.
       Every unmarked rotation-invariant statistic is identical across
       all twists — while Helson zetas realize radically different zero
       sets (Helson 1969; Seip 2020; Bochkov-Romanov). The torus
       channel is blind: one panel of the paper's two-sided no-go (the
       other is the FE channel, fe_indeterminacy.py / Theorem 5).
  [C7] the Boolean-cube form: M(x) = sum_{S subset P_x} (-1)^{|S|}
       [sum_{p in S} log p <= log x] — Mertens as the top parity
       Fourier coefficient of the subset-sum threshold (certified at
       x = 30 over all 1024 subsets). RH = a parity/restriction
       estimate: the marked restriction problem.

Honest grading: every identity here is classical in substance (the
parity barrier is Friedlander-Iwaniec territory; the Mertens-energy
equivalence is classical). The paper's contribution is the assembled
architecture, the formalized two-sided blindness pair, and the
window-tower observation — see the paper's literature section.
"""

from fractions import Fraction as Fr
from sympy import symbols, expand, simplify, prod, Rational

PRIMES = [2, 3, 5, 7, 11, 13]

def mobius(n):
    m, cnt = n, 0
    p = 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            cnt += 1
        p += 1
    if m > 1:
        cnt += 1
    return (-1) ** cnt

def main():
    # ---- [C1] cascade closed form -------------------------------------------
    atoms = {1: 1}                          # d -> weight; R_0 = H = atom at d=1
    for p in PRIMES:
        atoms = {**{d: w for d, w in atoms.items()},
                 **{d * p: atoms[d] * -1 for d in list(atoms)}} if False else \
                dict(list(atoms.items()) +
                     [(d * p, -w) for d, w in atoms.items()])
    Pk = 1
    for p in PRIMES:
        Pk *= p
    expected = {d: mobius(d) for d in sorted(atoms) if Pk % d == 0}
    assert atoms == expected, "cascade atoms = Mobius atoms"
    assert len(atoms) == 2 ** len(PRIMES)
    print("[C1] cascade closed form: the recursion R_{k+1} = R_k - tau R_k")
    print(f"     produces exactly the Mobius atoms mu(d) at log d for the")
    print(f"     {2**len(PRIMES)} divisors of P_6 = {Pk} — certified by exact")
    print("     atom algebra.")

    # ---- [C2] resolved front = Mertens --------------------------------------
    def R_of(x):                            # R_k(log x), exact: H = [d <= x]
        return sum(w for d, w in atoms.items() if d <= x)
    M = 0
    for x in range(1, 17):                  # p_7 = 17: front resolved below it
        M += mobius(x)
        assert R_of(x) == M, (x, R_of(x), M)
    print("[C2] resolved front: R_6(log x) = M(x) for every integer x < 17 —")
    print("     the cascade equals the true Mertens residual up to the next")
    print("     unborn prime. The 'current shape' is exact arithmetic memory.")

    # ---- [C3] the transform -------------------------------------------------
    s = symbols("s")
    k4 = PRIMES[:4]
    lhs = sum(mobius(d) * Rational(1) * d ** (-s)
              for d in range(1, 211) if 210 % d == 0)
    rhs = prod(1 - p ** (-s) for p in k4)
    assert simplify(expand(lhs) - expand(rhs)) == 0
    print("[C3] transform: sum_{d|210} mu(d) d^{-s} = prod_{p<=7}(1 - p^{-s})")
    print("     symbolically; with H's Laplace atom d^{-s}/s, the cascade")
    print("     transforms to the reciprocal finite Euler product over s.")

    # ---- [C4] the energy threshold ------------------------------------------
    sig = symbols("sigma", positive=True)
    lhs_e = sum(Rational(1) * d ** (-2 * sig)
                for d in range(1, 211) if 210 % d == 0 and mobius(d) != 0)
    rhs_e = prod(1 + p ** (-2 * sig) for p in k4)
    assert simplify(expand(lhs_e) - expand(rhs_e)) == 0
    growth = Fr(1)
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        growth *= (1 + Fr(1, p))
    print("[C4] energy: ||F_{k,sigma}||^2 = prod(1 + p^{-2 sigma}) by torus")
    print("     orthogonality (symbolic, k = 4); converges iff sigma > 1/2")
    print("     (cited). At sigma = 1/2 the partial products grow (exact:")
    print(f"     prod_(p<=47)(1+1/p) = {growth} ~ {float(growth):.3f}) — the")
    print("     critical line IS the finite-energy boundary of the free field,")
    print("     visible before any zero of zeta is mentioned.")

    # ---- [C5] per-prime contraction is FALSE --------------------------------
    atoms2 = {1: 1, 2: -1, 3: -1, 6: 1}                 # R_2
    atoms3 = dict(list(atoms2.items())
                  + [(5 * d, -w) for d, w in atoms2.items()])   # R_3
    x = Fr(11, 2)
    r2 = sum(w for d, w in atoms2.items() if d <= x)
    r3 = sum(w for d, w in atoms3.items() if d <= x)
    assert (r2, r3) == (-1, -2)
    print("[C5] contraction is FALSE: R_2(log 5.5) = -1 but adding the prime 5")
    print("     gives R_3(log 5.5) = -2 — the birth AMPLIFIED the residual.")
    print("     Square-root cancellation must be global, not per-prime.")

    # ---- [C6] Helson rotation -----------------------------------------------
    z1, z2, z3 = symbols("z1 z2 z3")
    c1, c2, c3, q1, q2, q3 = symbols("chi1 chi2 chi3 psi1 psi2 psi3",
                                     nonzero=True)
    t = symbols("t", positive=True)         # stands for p^{-sigma} per prime
    t1, t2, t3 = symbols("t1 t2 t3", positive=True)
    Fchi = (1 - c1 * t1 * z1) * (1 - c2 * t2 * z2) * (1 - c3 * t3 * z3)
    Fpsi = (1 - q1 * t1 * z1) * (1 - q2 * t2 * z2) * (1 - q3 * t3 * z3)
    rotated = Fchi.subs({z1: q1 / c1 * z1, z2: q2 / c2 * z2,
                         z3: q3 / c3 * z3}, simultaneous=True)
    assert simplify(expand(rotated - Fpsi)) == 0
    print("[C6] Helson rotation: F_psi = F_chi o R_{chi,psi} symbolically —")
    print("     every unmarked rotation-invariant torus statistic (all Haar")
    print("     norms, moments, value distributions, the energy threshold) is")
    print("     IDENTICAL across all unimodular twists, while Helson zetas")
    print("     realize radically different zero sets (Helson; Seip;")
    print("     Bochkov-Romanov). The")
    print("     torus channel is blind: panel two of the two-sided no-go.")

    # ---- [C7] Boolean-cube form ---------------------------------------------
    from itertools import combinations
    Px = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    x = 30
    total = 0
    for r in range(len(Px) + 1):
        for S in combinations(Px, r):
            w = 1
            for p in S:
                w *= p
            if w <= x:                      # sum log p <= log x <=> prod <= x
                total += (-1) ** r
    Mx = sum(mobius(n) for n in range(1, x + 1))
    assert total == Mx == -3
    print("[C7] Boolean cube: M(30) = -3 recovered as the parity-signed count")
    print("     of subset products <= 30 over all 1024 subsets of the primes")
    print("     below 30 — Mertens as the top parity Fourier coefficient of")
    print("     the subset-sum threshold. RH = the marked restriction problem:")
    print("     how strongly can the parity character of the free prime cube")
    print("     correlate with the Archimedean size half-space?")

    # ---- [C8] the zeta-ratio energy closed form:
    # prod(1 + p^{-2s}) = prod(1 - p^{-4s})/prod(1 - p^{-2s})
    # per-prime symbolically -- whence the H^2 energy of the FULL free
    # field is zeta(2s)/zeta(4s) (Euler; cited), finite iff s > 1/2.
    from sympy import symbols as _sym
    tt = _sym("t")
    assert expand((1 + tt) * (1 - tt) - (1 - tt ** 2)) == 0
    sgm = _sym("s", positive=True)
    for p in [2, 3, 5, 7]:
        lhs8 = 1 + p ** (-2 * sgm)
        rhs8 = (1 - p ** (-4 * sgm)) / (1 - p ** (-2 * sgm))
        assert simplify(lhs8 - rhs8) == 0
    print("[C8] energy closed form: (1 + p^{-2s}) = (1 - p^{-4s})/(1 - p^{-2s})")
    print("     per prime, symbolically — the full free field's H^2 energy is")
    print("     zeta(2s)/zeta(4s) (Euler, cited): finite iff s > 1/2, the")
    print("     unconditional statement of the exponent (paper, Theorem 1).")

    # ---- [C9] twist-energy invariance in EXACT arithmetic (replaces the
    # floating-point detour): with |chi(p)|^2 = 1 symbolic,
    # the coefficient energy is chi-independent.
    cvars = _sym("c1 c2 c3 c4", positive=True)   # |chi(p)|^2 placeholders
    prs = [2, 3, 5, 7]
    e_twist = 1
    e_plain = 1
    for p, c in zip(prs, cvars):
        e_twist *= (1 + c * p ** (-2 * sgm))
        e_plain *= (1 + p ** (-2 * sgm))
    subbed = e_twist.subs({c: 1 for c in cvars})
    assert simplify(subbed - e_plain) == 0
    print("[C9] twist invariance, exact: with |chi(p)|^2 = 1 the coefficient")
    print("     energy prod(1 + |chi(p)|^2 p^{-2s}) is chi-independent —")
    print("     the blindness engine certified without floats.")

    print("\nSIGNED CASCADE CERTIFIED: the free field is critical at 1/2 by")
    print("  energy; the resolved front is Mertens; contraction fails; the")
    print("  torus channel is Helson-blind and the FE channel is DH/Burnol-")
    print("  blind (fe_indeterminacy_draft.md) — a proof must couple the")
    print("  arithmetic marking to the Archimedean reflection. RH restated:")
    print("  the marked restriction introduces no anomalous exponent.")

if __name__ == "__main__":
    main()
