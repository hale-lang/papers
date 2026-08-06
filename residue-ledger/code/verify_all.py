r"""
verify_all.py — top-level verifier for the residue-ledger certificate suite.

Runs every script (each is assert-laden; a nonzero exit fails the suite)
and prints the per-theorem grading legend. Gradings:

  PROVED-BY-CODE : the leg is an exact finite computation asserted here.
  PROVED-IN-TEXT : the leg is a short proof in the paper (the code may
                   spot-check it, but the argument is the proof).
  CITED          : the leg rests on a standard literature result.
  CONDITIONAL    : the leg is stated as a prediction pending named work.

Usage: python3 verify_all.py          (from code/; ~10-20 min total)
"""

import subprocess
import sys
import time

SCRIPTS = [
    ("two_meters.py",               "fourfold split point: meters, Weil plane, absorption"),
    ("two_meters_generic.py",       "isogeny lesson (rational conjugation moves nothing)"),
    ("two_meters_vgeneral.py",      "unpolarized-cell lesson (larger PEL family)"),
    ("two_meters_polarized.py",     "polarized 1-param slice (absorbed: slice too thin)"),
    ("two_meters_polarized_full.py","polarized 4-param cell: Hdg4 = <theta^2> + W, escape"),
    ("resonance_excess.py",         "Theorem 1/2 fourfold leg: rank 6, kernel = cell"),
    ("n1_sharpness.py",             "n = 1 boundary regression (Theorem 1 sharpness)"),
    ("sixfold_rig.py",              "Theorem 2: sixfold certificates, both discriminants"),
    ("conjugacy_theorem.py",        "Theorem 3: real conjugacy over Q(sqrt 3)"),
    ("arithmetic_quotient.py",      "Theorem 4: Witt indices, local separation at {2,3}"),
    ("cusp_class_numbers.py",       "Theorem 5 part 1: class numbers, odd-place analysis"),
    ("dyadic_types.py",             "Theorem 5 part 2: dyadic types, predicted spectra"),
    ("theorem5_legs.py",            "Theorem 5b: corank-1 unconditional (four-lemma repair)"),
    ("corank23_lemmas.py",          "Theorem 5c: coranks 2-3 unconditional (full spectra)"),
    ("k3_residue_angle.py",         "Proposition 6: K3 loop incl. rational-Picard calibration"),
]

LEGEND = """
THEOREM LEG GRADING
  Theorem 1 (rigidity, n >= 2)
    middle-block vanishing ................ PROVED-IN-TEXT (+ code spot checks)
    Sym^2 injectivity, general n .......... PROVED-IN-TEXT (wedge replacement)
    exact attainment, n = 2, 3 ............ PROVED-BY-CODE
    n = 1 sharpness ....................... PROVED-BY-CODE
    reducedness sandwich .................. PROVED-IN-TEXT
  Theorem 2 (certificates; blindness)
    all ranks/kernels/tuple equality ...... PROVED-BY-CODE
  Theorem 3 (real conjugacy)
    isometry + transport identities ....... PROVED-BY-CODE
    mu-equivariance ....................... PROVED-IN-TEXT (functoriality;
                                            code samples as regression)
    nonexistence over Q ................... PROVED-IN-TEXT (descent)
  Theorem 4 (Witt/local/boundary)
    Gram decompositions, Witt indices ..... PROVED-BY-CODE
    local separation at 2, 3 .............. PROVED-IN-TEXT (finite checks in code)
    local isometry elsewhere .............. CITED (Jacobowitz)
    Baily-Borel boundary dictionary ....... CITED (Baily-Borel)
  Theorem 5 (class numbers; dyadic types; spectra)
    strong approximation .................. CITED (Platonov-Rapinchuk)
    diagonal determinant lemma ............ PROVED-BY-CODE
    Hilbert-90 / idele computation ........ PROVED-IN-TEXT
    p = 3 positioning; F_9 substrate ...... PROVED-BY-CODE
    dyadic type invariant + witnesses ..... PROVED-BY-CODE
    corank-3 forcing (15 subspaces) ....... PROVED-BY-CODE
    corank-1 pairing ideal (Lemma 5b.1) ... PROVED-IN-TEXT ([B8] substrate)
    corank-1 splitting/parity (5b.2) ...... PROVED-IN-TEXT (+ certificates)
    corank-1 local uniqueness (5b.3) ...... PROVED-IN-TEXT (p=3 Jordan shape;
                                            p=2 parity+det [B3]-[B5])
    corank-1 class number one (5b.4) ...... PROVED-IN-TEXT + CITED (Kirschmer
                                            determinant groups; [B9] substrate)
    corank-1 exact counts (2 vs 1) ........ PROVED (Theorem 5b)
    corank-3 canonical form (C = 0) ....... PROVED-BY-CODE ([E1]; pure normal
                                            form, no genus theory)
    corank-2 normal forms + parity law .... PROVED-IN-TEXT ([E2]-[E5], [E7])
    corank-2 complement genus + h = 1 ..... PROVED-IN-TEXT + CITED (Jordan at 3;
                                            Kirschmer at 2; strong approx)
    parabolic local-global (all coranks) .. DISSOLVED (proofs directly global)
    => spectra (2,2,1) vs (1,1) ........... PROVED (Theorems 5b + 5c)
  Proposition 6 (K3 loop)
    finite clauses (walls, slopes, ........ PROVED-BY-CODE
      counts, heights, calibration)
    projectivity / marked-K3 realization .. PROVED-IN-TEXT + CITED (surjectivity
                                            of the period map; Torelli)
    noble-angle extremality ............... CONDITIONAL (conjecture)
"""

def main():
    t0 = time.time()
    failures = []
    for script, blurb in SCRIPTS:
        s = time.time()
        r = subprocess.run([sys.executable, script], capture_output=True, text=True)
        status = "PASS" if r.returncode == 0 else "FAIL"
        print(f"[{status}] {script:32s} {time.time()-s:7.1f}s  {blurb}")
        if r.returncode != 0:
            failures.append((script, r.stdout[-2000:] + r.stderr[-2000:]))
    print(LEGEND)
    if failures:
        for name, tail in failures:
            print(f"--- {name} output tail ---\n{tail}\n")
        print(f"SUITE: {len(failures)} FAILURE(S) in {time.time()-t0:.0f}s")
        sys.exit(1)
    print(f"SUITE: ALL {len(SCRIPTS)} SCRIPTS PASS in {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
