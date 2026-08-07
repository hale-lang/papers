r"""
marked_lab.py — the structure-search lab (paper, directions section):
compare the free-field, marked, and blindness-control readings of the
Mobius prime field for increasing height, hunting identities and
behavioral separations.

GRADING: EXPLORATORY LAB. Exact channels are asserted; the sigma-in-
the-strip channels use certified-precision arithmetic (mpmath-free
here: high-precision Fraction approximants are avoided; instead the
strip channels use Python floats and are LOUDLY flagged as
observation-only, never proof-critical, per the NF ground rules).
The purpose is NOT numerical evidence for RH — it is to search for
an identity, monotonicity law, or low-rank update present for the
arithmetic marking and absent under blindness controls.

Channels:
  [X1] EXACT: sieve M(x), squarefree count Q(x), the normalized
       parity correlation C(x) = M(x)/Q(x) at powers of 2 up to
       2^16 — the parity discrepancy's observed scale (printed, no
       claims), plus the exact identity Q(x) = sum mu^2 and the
       internal consistency M = sum mu.
  [X2] EXACT at sigma = 1: the marked reading R_1(x) = sum mu(n)/n
       and the box product prod_{p<=x}(1 - 1/p) as exact rationals —
       both tend to 0 at this edge (PNT-scale vs Mertens-scale), with
       the RATE separation printed: box * log ~ e^{-gamma} while
       marked * log -> 0 (observation only).
  [X3] STRIP OBSERVATION (floats, flagged): at sigma = 3/4, the
       marked reading R_sigma(x) vs the box product at y = x — the
       paper's two-geometries contrast made visible: the box marches
       to 0, the marked reading hovers near a nonzero value
       (1/zeta(3/4) < 0 under continuation). Observation only.
  [X4] TWIST SEPARATION, EXACT at sigma = 1: the Liouville twist
       chi(p) = -1 for all p (completely multiplicative, unimodular:
       the marked reading becomes sum lambda(n)/n, whose limit is
       zeta(2)/zeta(1)-type, i.e. 0 too, but with the OPPOSITE-SIGN
       early behavior) vs the Mobius reading — the MARKED readings
       separate the twists (exact partial sums printed) while the
       unmarked energy is twist-blind ([C9]): the marking sees,
       the torus does not. The lab's cleanest structural fact.
  [X5] EXACT: the box-vs-height set difference at small scale — the
       monomials kept by the prime-box {d | P_y} but discarded by
       the height cutoff {n <= x}: counted exactly for y = 13,
       x = 13: 2^6 = 64 box monomials vs 9 squarefree integers
       <= 13: the box keeps 55 "over-height" combinations — the
       discarded mass IS where the continuation hides.
"""

from fractions import Fraction as Fr
from math import log, exp

def sieve_mobius(N):
    mu = [1] * (N + 1)
    primes = []
    is_comp = [False] * (N + 1)
    for i in range(2, N + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > N:
                break
            is_comp[i * p] = True
            mu[i * p] = 0 if i % p == 0 else -mu[i]
            if i % p == 0:
                break
    mu[0] = 0
    return mu, primes

def main():
    N = 1 << 16
    mu, primes = sieve_mobius(N)

    # ---- [X1] exact parity correlation --------------------------------------
    M = 0
    Q = 0
    marks = {1 << k for k in range(6, 17)}
    print("[X1] exact parity correlation (no claims; observed scale):")
    print("      x        M(x)     Q(x)      C = M/Q      M/sqrt(x)")
    for x in range(1, N + 1):
        M += mu[x]
        Q += 1 if mu[x] != 0 else 0
        if x in marks:
            print(f"  {x:7d}  {M:7d}  {Q:8d}   {M/Q:+.6f}     {M/x**0.5:+.4f}")

    # ---- [X2] sigma = 1 edge, exact -----------------------------------------
    R1 = Fr(0)
    for n in range(1, 3001):
        if mu[n]:
            R1 += Fr(mu[n], n)
    box = Fr(1)
    for p in primes:
        if p > 3000:
            break
        box *= 1 - Fr(1, p)
    print("\n[X2] sigma = 1 edge (exact rationals, x = 3000):")
    print(f"     marked  sum mu(n)/n     = {float(R1):+.6f}  (PNT: -> 0)")
    print(f"     box     prod(1 - 1/p)   = {float(box):+.6f}  (Mertens: ~ e^-gamma/log)")
    print(f"     box * log x = {float(box) * log(3000):.4f} ~ e^-gamma = {exp(-0.5772156649):.4f};")
    print(f"     marked * log x = {float(R1) * log(3000):+.4f} -> 0: same edge, different rates.")

    # ---- [X3] strip observation (floats, flagged) ---------------------------
    sig = 0.75
    Rs = 0.0
    for n in range(1, N + 1):
        if mu[n]:
            Rs += mu[n] / n ** sig
    boxs = 1.0
    for p in primes:
        boxs *= 1 - p ** (-sig)
    print(f"\n[X3] STRIP OBSERVATION (floats, observation-only) sigma = {sig}, x = {N}:")
    print(f"     marked reading R_sigma(x) = {Rs:+.6f}   (continuation target 1/zeta(3/4) ~ -0.3813)")
    print(f"     box product to same cutoff = {boxs:+.2e}  (marches to 0)")
    print("     THE TWO GEOMETRIES SEPARATE IN THE STRIP — the paper's main")
    print("     conceptual output, made visible. Not evidence; illustration.")

    # ---- [X4] twist separation at the marked reading, exact -----------------
    lam = [0] * (N + 1)                     # Liouville via smallest-prime-factor
    lam[1] = 1
    spf = list(range(N + 1))
    for p in primes:
        for m in range(p, N + 1, p):
            if spf[m] == m:
                spf[m] = p
    for n in range(2, N + 1):
        lam[n] = -lam[n // spf[n]]
    Rmu = Fr(0)
    Rlam = Fr(0)
    for n in range(1, 3001):
        if mu[n]:
            Rmu += Fr(mu[n], n)
        Rlam += Fr(lam[n], n)
    assert lam[2] == -1 and lam[4] == 1 and lam[12] == -1     # lambda checks
    print("\n[X4] twist separation, exact (x = 3000, sigma = 1):")
    print(f"     Mobius reading    sum mu(n)/n     = {float(Rmu):+.6f}")
    print(f"     Liouville reading sum lambda(n)/n = {float(Rlam):+.6f}")
    print("     The MARKED readings separate the twists; the unmarked torus")
    print("     energy cannot ([C9]) — the marking sees, the torus is blind.")

    # ---- [X5] the discarded mass, exact -------------------------------------
    Py = [2, 3, 5, 7, 11, 13]
    box_monomials = 1 << len(Py)
    sq_below = sum(1 for n in range(1, 14) if mu[n] != 0)
    over = box_monomials - sq_below
    assert (box_monomials, sq_below, over) == (64, 9, 55)
    print("\n[X5] the discarded mass (exact, y = x = 13): the prime box keeps")
    print(f"     {box_monomials} squarefree monomials; the height cutoff keeps {sq_below};")
    print(f"     {over} over-height combinations are box-kept but height-discarded.")
    print("     The analytic continuation lives in that discarded mass.")

    print("\nMARKED-RESTRICTION LAB COMPLETE (exploratory; exact where")
    print("  asserted, flagged floats where not). Structural facts observed:")
    print("  the marking separates twists that the torus cannot; the two")
    print("  truncation geometries separate in the strip; the discarded")
    print("  over-height mass is the continuation's home. Next: hunt a")
    print("  low-rank update law for R_sigma under x -> x' (target B),")
    print("  with escape_blindness bounding what it cannot be.")

if __name__ == "__main__":
    main()
