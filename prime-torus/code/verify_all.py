r"""
verify_all.py — top-level verifier for the prime-torus certificate
suite. Runs every script (assert-laden; nonzero exit fails the suite)
and prints the per-result grading legend:

  PROVED-BY-CODE : an exact finite computation asserted here.
  PROVED-IN-TEXT : a short proof in the paper (code may spot-check).
  CITED          : rests on a standard literature result.
  EXPLORATORY    : observation-only channels, loudly flagged, never
                   proof-critical.

Usage: python3 verify_all.py     (from code/; a few seconds total)
"""

import subprocess
import sys
import time

SCRIPTS = [
    ("prime_cascade.py",   "Thms 1-3 substrate: cascade, Mertens front, energy,"
                           " Helson rotation, Boolean cube"),
    ("inverse_defect.py",  "Prop 4: leakage ledger; windows -> von Mangoldt"
                           " tower (Selberg Lambda_2 at degree 2)"),
    ("fe_indeterminacy.py","Thm 5: multiplier lemma, locality, planting"
                           " quartic, composition"),
    ("dh_pencil.py",       "historical panel: the Davenport-Heilbronn family"
                           " exactly (xi = half-argument of the root number)"),
    ("marked_lab.py",      "directions: structure-search lab (exploratory;"
                           " floats flagged)"),
]

LEGEND = """
RESULT GRADING
  Theorem 1 (free-field criticality)
    finite energy identities .............. PROVED-BY-CODE ([C4], [C8])
    Bohr/H^2 correspondence; zeta ratio ... CITED
  Theorem 2 (prime-torus blindness)
    rotation identity; twist invariance ... PROVED-BY-CODE ([C6], [C9])
    Helson zeta zero realization .......... CITED (Helson; Seip;
                                            Bochkov-Romanov)
  Theorem 3 (marked-boundary equivalence)
    the convergence criterion ............. CITED (Littlewood 1912)
    the restriction decomposition ......... PROVED-IN-TEXT
    cascade/Mertens/knapsack substrate .... PROVED-BY-CODE ([C1]-[C3],
                                            [C5], [C7])
  Proposition 4 (boundary redistribution; the window tower)
    hard window: interior cancellation .... PROVED-BY-CODE ([W1])
    linear taper -> Lambda/log N .......... PROVED-BY-CODE ([W2]; window
                                            due to Bettin-Conrey-Farmer)
    quadratic taper -> Selberg Lambda_2 ... PROVED-BY-CODE ([W3], [W4])
    defect ledger bookkeeping ............. PROVED-BY-CODE ([W5])
  Theorem 5 (FE-channel indeterminacy)
    witness F+ (all zeros on line) ........ CITED (Nakamura QJM 2023)
    planting quartic; composition ......... PROVED-BY-CODE ([T3], [T4])
    Route B operator machinery ............ PROVED-BY-CODE ([T1], [T2]) +
                                            CITED (Burnol AIF 2007)
    off-line witnesses in the FE class .... CITED (Davenport-Heilbronn;
                                            Nakamura Abh. 2025)
    the no-go conclusion .................. PROVED-IN-TEXT
  Historical panel (Davenport-Heilbronn family)
    cyclotomic structure; xi tuning ....... PROVED-BY-CODE ([P0]-[P3])
  Structure-search lab .................... EXPLORATORY (flagged)
"""

def main():
    t0 = time.time()
    failures = []
    for script, blurb in SCRIPTS:
        s = time.time()
        r = subprocess.run([sys.executable, script],
                           capture_output=True, text=True)
        status = "PASS" if r.returncode == 0 else "FAIL"
        print(f"[{status}] {script:22s} {time.time()-s:6.1f}s  {blurb}")
        if r.returncode != 0:
            failures.append((script, r.stdout[-1500:] + r.stderr[-1500:]))
    print(LEGEND)
    if failures:
        for name, tail in failures:
            print(f"--- {name} ---\n{tail}\n")
        print(f"SUITE: {len(failures)} FAILURE(S) in {time.time()-t0:.0f}s")
        sys.exit(1)
    print(f"SUITE: ALL {len(SCRIPTS)} SCRIPTS PASS in {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
