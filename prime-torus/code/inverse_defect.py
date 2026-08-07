r"""
inverse_defect.py — the finite Mobius inverse defect
L_{N,w} = 1 - zeta V_{N,w} (paper, Proposition 4): the exact leakage
ledger, certified in the free Z-module over {log p} — no real numbers
anywhere.

THE OBJECT. V_{N,w}(s) = sum_{n<=N} mu(n) w(log n/log N) n^{-s};
zeta(s)V_{N,w}(s) = sum_m c_{N,w}(m) m^{-s} with
c_{N,w}(m) = sum_{d|m, d<=N} mu(d) w(log d/log N). The defect
L_{N,w} = 1 - zeta V has coefficients delta_{m,1} - c_{N,w}(m): the
exact ledger of what the finite inverse failed to cancel.

EXACTNESS DEVICE: log d lives in the free Z-module over {log p}
(exponent vectors); (log d)^2 lives in Sym^2 of it (symmetric integer
matrices). All window identities below are certified as VECTOR/MATRIX
identities, division-free (multiply through by log N).

Channels (all exact):
  [W1] HARD CUTOFF w = 1: for every m <= N, c(m) = sum_{d|m} mu(d)
       = delta_{m,1} — no interior leakage; the whole defect is pushed
       beyond the Archimedean boundary. (Certified m <= 300, N = 300.)
  [W2] LINEAR TAPER w(u) = 1 - u (the Bettin-Conrey-Farmer window;
       Bettin-Conrey-Farmer): for 2 <= m <= N,
           log N * c(m) = -sum_{d|m} mu(d) log d = Lambda(m)
       as vectors over {log p} — the boundary defect is redistributed
       into the CANONICAL PRIME HARMONIC Lambda(m)/log N. (Certified
       m <= 300 in the log-prime module.)
  [W3] QUADRATIC TAPER w(u) = (1-u)^2 — THE WINDOW TOWER (the linear
       taper is not unique: the window's polynomial DEGREE selects
       the von Mangoldt tower): for
       2 <= m <= N,
           (log N)^2 c(m) = sum_{d|m} mu(d)(log N - log d)^2
                          = 2 log N * Lambda(m) - [2 Lambda(m) log m
                            - Lambda_2(m)]
       where Lambda_2 = mu * log^2 is SELBERG'S function, satisfying
       Lambda_2(m) = Lambda(m) log m + (Lambda*Lambda)(m). Certified
       as Sym^2 matrix identities, m <= 200. The quadratic window's
       new interior channel is exactly Lambda_2 — the parity-BREAKING
       object of Selberg's sieve: the taper ladder walks the
       generalized von Mangoldt functions Lambda_j = mu * log^j, and
       the parity barrier meets the leakage geometry at degree 2.
  [W4] the Selberg identity Lambda_2 = Lambda log + Lambda*Lambda
       itself, certified in Sym^2 (m <= 200) — the algebraic engine
       of [W3].
  [W5] defect bookkeeping: with the linear taper at N = 30, the
       interior L-coefficients are exactly -Lambda(m)/log N for
       2 <= m <= 30 and the m = 1 coefficient is 0 (certified as the
       vector statement log N * [coefficient] = -Lambda-vector).

Grading: [W1] classical (Mobius); [W2] classical in substance (the
BCF window; the identity -sum mu(d) log d = Lambda is textbook);
[W3]/[W4] elementary consequences of Selberg's identity — the
observation that the window-degree ladder IS the Lambda_j tower, with
degree 2 = the parity-breaking channel, is (to our current knowledge)
this paper's addition; stated with an explicit invitation to
correction in the literature section.
"""

from sympy import factorint

MAXP = 300
PRIMES = [p for p in range(2, MAXP + 1)
          if all(p % q for q in range(2, int(p ** 0.5) + 1))]
PIDX = {p: i for i, p in enumerate(PRIMES)}

def mobius(n):
    f = factorint(n)
    if any(e > 1 for e in f.values()):
        return 0
    return (-1) ** len(f)

def logvec(n):
    """log n as an integer vector over {log p}."""
    v = [0] * len(PRIMES)
    for p, e in factorint(n).items():
        v[PIDX[p]] += e
    return tuple(v)

def vadd(a, b, sb=1):
    return tuple(x + sb * y for x, y in zip(a, b))

def vscale(a, t):
    return tuple(t * x for x in a)

ZV = tuple([0] * len(PRIMES))

def sym2(u, v):
    """Symmetric product of two log-vectors as an upper-triangular map."""
    m = {}
    for i, ui in enumerate(u):
        if ui:
            for j, vj in enumerate(v):
                if vj:
                    key = (min(i, j), max(i, j))
                    m[key] = m.get(key, 0) + ui * vj
    return m

def madd(a, b, sb=1):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + sb * v
        if out[k] == 0:
            del out[k]
    return out

def Lambda_vec(m):
    f = factorint(m)
    if len(f) == 1:
        p = next(iter(f))
        v = [0] * len(PRIMES)
        v[PIDX[p]] = 1                     # Lambda(p^a) = log p
        return tuple(v)
    return ZV

def divisors(m):
    ds = [1]
    for p, e in factorint(m).items():
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return ds

def main():
    N = 300

    # ---- [W1] hard cutoff ----------------------------------------------------
    for m in range(1, N + 1):
        c = sum(mobius(d) for d in divisors(m))
        assert c == (1 if m == 1 else 0), m
    print("[W1] hard cutoff w = 1: c(m) = delta_{m,1} for every m <= N — the")
    print("     finite Mobius inverse cancels the interior perfectly; ALL")
    print("     defect is pushed past the Archimedean boundary. (m <= 300.)")

    # ---- [W2] linear taper ---------------------------------------------------
    for m in range(2, N + 1):
        acc = ZV
        for d in divisors(m):
            mu_d = mobius(d)
            if mu_d:
                acc = vadd(acc, logvec(d), -mu_d)   # -sum mu(d) log d
        assert acc == Lambda_vec(m), m
    print("[W2] linear taper w = 1 - u: log N * c(m) = -sum mu(d) log d =")
    print("     Lambda(m) as exact vectors over {log p} (m <= 300) — the")
    print("     boundary defect becomes the canonical prime harmonic")
    print("     -Lambda(m)/log N in the interior (the Bettin-Conrey-Farmer")
    print("     window).")

    # ---- [W4] Selberg's identity (the engine, certified first) ---------------
    M2 = 200
    for m in range(2, M2 + 1):
        lhs = {}
        for d in divisors(m):
            mu_d = mobius(d)
            if mu_d:
                md = m // d
                lhs = madd(lhs, sym2(logvec(md), logvec(md)), mu_d)
        lam_log = sym2(Lambda_vec(m), logvec(m))
        conv = {}
        for d in divisors(m):
            conv = madd(conv, sym2(Lambda_vec(d), Lambda_vec(m // d)))
        assert lhs == madd(lam_log, conv), m
    print("[W4] Selberg: Lambda_2(m) = sum mu(d) log^2(m/d) = Lambda(m)log m")
    print("     + (Lambda*Lambda)(m), certified as Sym^2 integer-matrix")
    print("     identities (m <= 200) — the parity-breaking engine.")

    # ---- [W3] quadratic taper ------------------------------------------------
    # (log N)^2 c(m) = sum mu(d)(log N - log d)^2
    #               = -2 log N Lambda(m)*(-1)... expand exactly:
    # = [sum mu(d)] log^2 N - 2 log N sum mu(d) log d + sum mu(d) log^2 d
    # = 0 + 2 log N Lambda(m) + [Lambda_2(m) - 2 Lambda(m) log m]   (m >= 2)
    for m in range(2, M2 + 1):
        lhs = {}
        for d in divisors(m):
            mu_d = mobius(d)
            if mu_d:
                lhs = madd(lhs, sym2(logvec(d), logvec(d)), mu_d)
        lam2 = {}
        for d in divisors(m):
            mu_d = mobius(d)
            if mu_d:
                md = m // d
                lam2 = madd(lam2, sym2(logvec(md), logvec(md)), mu_d)
        rhs = madd(lam2, sym2(Lambda_vec(m), logvec(m)), -2)
        assert lhs == rhs, m
    print("[W3] quadratic taper w = (1-u)^2: the new interior channel is")
    print("     sum mu(d) log^2 d = Lambda_2(m) - 2 Lambda(m) log m (Sym^2,")
    print("     m <= 200) — the window DEGREE walks the von Mangoldt tower")
    print("     Lambda_j = mu * log^j: hard -> edge only, linear -> Lambda,")
    print("     quadratic -> SELBERG'S Lambda_2, where sieve parity first")
    print("     breaks. The taper ladder is the parity ladder.")

    # ---- [W5] defect bookkeeping at N = 30 ------------------------------------
    N5 = 30
    for m in range(1, N5 + 1):
        acc = ZV
        for d in divisors(m):
            if d <= N5:
                mu_d = mobius(d)
                if mu_d:
                    acc = vadd(acc, logvec(d), -mu_d)
        target = Lambda_vec(m) if m >= 2 else ZV
        assert acc == target, m
    print("[W5] defect ledger at N = 30 (linear taper): interior")
    print("     L-coefficients are EXACTLY -Lambda(m)/log N for 2 <= m <= 30,")
    print("     0 at m = 1 (division-free vector certification) — the finite")
    print("     inverse's failure is precisely the prime-power comb, rescaled.")

    print("\nINVERSE DEFECT CERTIFIED: the leakage geometry of the")
    print("  Nyman-Beurling meter is now exact — hard windows hide the defect")
    print("  past the boundary, polynomial windows redistribute it into the")
    print("  von Mangoldt tower, and degree 2 is where the parity barrier")
    print("  enters. Next (the genuinely new target): the E_free + E_mark")
    print("  decomposition of the defect energy, with the four-channel")
    print("  calibration (zeta / FF / Helson / DH) and the leakage Gram")
    print("  matrix G_N — hunting a structural factorization, not numerics.")

if __name__ == "__main__":
    main()
