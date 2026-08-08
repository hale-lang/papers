r"""
interval_rigging.py — the Matomäki-Radziwiłł adversarial rigging
argument as an exact finite certificate: the all-short-intervals
channel is riggable, witnessed constructively.

THE ARGUMENT (MR, Annals 183 (2016), introduction, in our notation):
in a short enough interval every integer can have a PRIVATE prime
factor — a prime p > y dividing exactly one element of a length-y
window. A completely multiplicative +-1 function can then be rigged on
those private primes to force constant sign throughout the window,
even though the function has abundant sign changes globally. Hence no
nontrivial sign-change theorem can hold in ALL short intervals below
the private-prime scale (Jacobsthal/Rankin lengths, in the asymptotic
version): the all-intervals channel is adversarially blind at that
scale. This file realizes the argument at finite scale, exactly —
the finite shadow of the paper's Theorem 6(a).

Channels:
  [R1] PRIVATE-PRIME WINDOW: search for the first window [x, x+y),
       y = 10, in which every integer has a prime factor p > y
       dividing it exactly once (hence private to it within the
       window: two multiples of p > y cannot fit in a length-y
       window). Certified by factorization.
  [R2] THE RIGGING: define chi completely multiplicative with
       chi(q) = -1 on every prime except the window's private primes,
       where chi(p) is CHOSEN to force chi(n) = +1 for the window
       element n it owns. Assert: chi(n) = +1 for every n in the
       window — a sign-change desert manufactured to order.
  [R3] GLOBAL CONTRAST: the same chi has sign changes immediately
       outside (any prime q outside the private set has chi(q) = -1),
       and behaves Liouville-like on integers free of private primes.
       Assert sign changes in the adjacent window.
  [R4] framing print: what this certifies — the all-intervals channel
       below private-prime scale is adversarially riggable for the
       1-bounded completely multiplicative class; the almost-all
       channel (MR's theorem) survives precisely because rigged
       the almost-all channel survives; paper, Theorem 6.
All exact: integer factorization and sign bookkeeping only.
"""

from sympy import factorint

def main():
    Y = 10

    # ---- [R1] find the private-prime window ---------------------------------
    window = None
    x = 2
    while x < 200000:
        ok = True
        privates = {}
        for n in range(x, x + Y):
            f = factorint(n)
            cands = [p for p, e in f.items() if p > Y and e == 1]
            if not cands:
                ok = False
                break
            privates[n] = max(cands)
        if ok:
            # privacy is automatic (p > Y => at most one multiple in the
            # window) but assert it anyway:
            vals = list(privates.values())
            if len(set(vals)) == len(vals):
                window = (x, privates)
                break
        x += 1
    assert window is not None
    x0, privates = window
    print(f"[R1] private-prime window found: [{x0}, {x0 + Y}) — every element")
    print(f"     owns a private prime > {Y} (dividing it exactly once):")
    for n in range(x0, x0 + Y):
        print(f"       {n:6d} = {factorint(n)}   private prime {privates[n]}")

    # ---- [R2] the rigging ----------------------------------------------------
    private_set = set(privates.values())
    def chi_of(n):
        s = 1
        for p, e in factorint(n).items():
            base = rig[p] if p in rig else -1
            s *= base ** e
        return s
    rig = {}
    for n, p in privates.items():
        # chi(n) = chi(cofactor) * chi(p); force chi(n) = +1:
        cof = n // p
        s = 1
        for q, e in factorint(cof).items():
            s *= (-1) ** e                     # background chi(q) = -1
        rig[p] = s                             # chi(p) := chi(cofactor)
    for n in range(x0, x0 + Y):
        assert chi_of(n) == 1, n
    print(f"[R2] rigged: chi(q) = -1 on all primes except the {len(rig)}")
    print(f"     private primes, where chi(p) is chosen per-owner:")
    print(f"       {dict(sorted(rig.items()))}")
    print(f"     RESULT: chi = +1 on the entire window [{x0}, {x0 + Y}) — a")
    print("     manufactured sign-change desert, certified exactly.")

    # ---- [R3] global contrast ------------------------------------------------
    signs_before = [chi_of(n) for n in range(x0 - Y, x0)]
    assert -1 in signs_before and 1 in [chi_of(n) for n in range(2, 50)]
    assert chi_of(2) == -1                     # background Liouville-like
    changes = sum(1 for a, b in zip(signs_before, signs_before[1:]) if a != b)
    assert changes >= 1
    print(f"[R3] contrast: the SAME chi on the adjacent window "
          f"[{x0 - Y}, {x0}) has")
    print(f"     signs {signs_before} — {changes} sign change(s); globally the")
    print("     function is Liouville-like off the private primes.")

    # ---- [R4] framing --------------------------------------------------------
    print("\n[R4] WHAT THIS CERTIFIES: the all-short-intervals channel below")
    print("     the private-prime scale is adversarially RIGGABLE within the")
    print("     1-bounded completely multiplicative class — the finite shadow")
    print("     of Matomäki-Radziwiłł's own introduction argument (Annals 183")
    print("     (2016); Jacobsthal/Rankin lengths asymptotically). The")
    print("     almost-all channel survives because rigged windows are rare;")
    print("     the located-boundary draft states what the surviving channel")
    print("     can and cannot decide.")

if __name__ == "__main__":
    main()
