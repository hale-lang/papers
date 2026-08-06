# residue-ledger

*The Tangent Space Cannot See the Discriminant: infinitesimal rigidity
of Weil classes, with exact certificates in dimensions four and six* —
draft v0.6, August 2026. **Not yet submitted anywhere; treat as
a working draft.**

A local rigidity theorem for rational Weil classes on polarized
abelian 2n-folds of Weil type, certified by exact-arithmetic
computations (no floating point, no transcendence numerics) in
dimensions four and six, plus a K3 period-loop instrument. Headline
results:

- **Theorem 1 (infinitesimal rigidity, uniform in n).** The kernel of
  the infinitesimal Hodge obstruction of every nonzero rational Weil
  class is exactly the n²-dimensional K-linear Weil period domain, with
  rank n(n+1); consequently the local Hodge locus is smooth, reduced,
  and equal to the Weil locus at every point, including maximally split
  CM points. Depends only on the real signature (n,n), not the
  discriminant.
- **Theorem 2 (certificates; discriminant blindness).** Exact
  certificates in dimensions four (10/4/6) and six (21/9/12) — the
  sixfold pair run on a split (solved, disc [−1]) and a nonsplit
  (open, disc [−3]) hermitian form, returning identical infinitesimal
  datasets.
- **Theorem 3 (real conjugacy).** The explicit real isometry
  diag(1,1,1,1,1,3^(−1/2)) conjugates the entire local period geometry
  of the two discriminant classes — domain, Weil cell, Weil plane, and
  obstruction construction, fixing the base point — so the arithmetic
  discriminant is invisible to the *entire local period germ*, at every
  order; no rational conjugacy exists, by descent. Higher-order
  computations are thereby forced calibration channels. Verified
  exactly over Q(√3) in `code/conjugacy_theorem.py`.
- **Theorem 4 (the cusps can see the discriminant).** The two
  arithmetic quotients are separated by their rational boundary: Witt
  indices 3 (h₁ exactly hyperbolic) vs 2 (anisotropic kernel
  diag(1,−3)), so Q-ranks 3 vs 2, and the split quotient's Baily–Borel
  boundary has totally degenerate cusps while the nonsplit one has
  coranks ≤ 2 only. Locally the forms differ at exactly the primes
  {2, 3}. Certificates in `code/arithmetic_quotient.py`.
- **Theorem 5 (one cusp per depth; connected quotients).** Both genera
  have class number one (strong approximation + a diagonal determinant
  lemma + Hilbert 90 + Cl(Q(i)) = 1), and both groups act with exactly
  one orbit on primitive isotropic sublattices of every available rank:
  cusp counts (1,1,1) vs (1,1). Components and multiplicities carry no
  discriminant information — the entire distinction is the existence of
  the corank-3 cusp: one bit. Certificates in
  `code/cusp_class_numbers.py`.
- **Proposition C (K3 dichotomy loop).** A rational twistor loop in the
  K3 period domain whose very general fibers are nonprojective of
  Picard rank 19 while every one of its dense Noether–Lefschetz walls
  is projective of rank 20 — the instrument behind the paper's
  interpretive reading ("integer invariants are zero-mode shadows of
  continuous residual data").

The paper is deliberately explicit about what is classical and what is
new (§6): most of the mathematics is known; the contributions are the
certification pipeline, the reducedness statements, the
discriminant-blindness computation, and the observable layer.

## Contents

- `paper.md`, `references.bib`, `build.sh` — the paper (pandoc →
  `paper.pdf`, gitignored; build as for the sibling papers).
- `code/` — the exact computations (Python 3, `sympy`; `numpy` only for
  one numerical check of an asymptotic):
  - `two_meters.py` — fourfold setup: the two commuting complex
    structures, the Weil plane as an eigenpair of the arithmetic meter,
    balanced-vs-detuned signature, split-point ledger.
  - `two_meters_generic.py`, `two_meters_vgeneral.py`,
    `two_meters_polarized.py`, `two_meters_polarized_full.py` — the
    family computations, ending in the very-general polarized ledger
    Hdg⁴ = ⟨θ²⟩ ⊕ W (the intermediate scripts record two instructive
    failures kept deliberately: rational conjugation is an isogeny;
    the audit needs a fixed polarization).
  - `resonance_excess.py` — the first-order excess invariant e(γ),
    calibration table, and the exact attainment leg of Theorem A.
  - `sixfold_rig.py` — Theorem 2: both discriminant classes, sparse
    924-dimensional machinery, the form-side convention lemma,
    split/nonsplit certification.
  - `conjugacy_theorem.py` — Theorem 3: the exact Q(√3) verification of
    the real conjugacy (isometry, tangent transport, Weil-plane scaling,
    mu-equivariance).
  - `arithmetic_quotient.py` — Theorem 4: hyperbolic/anisotropic Gram
    decompositions, Witt indices, local separation at {2, 3}.
  - `cusp_class_numbers.py` — Theorem 5: the diagonal determinant lemma,
    the idele computation, the p = 3 positioning certificate, and the
    F_9 Hermitian-variety point count (2440, exact match).
  - `k3_residue_angle.py` — Proposition C (emits
    `k3_residue_data.json`); `build_k3_page.py` regenerates the
    interactive supplement from it.

  Every script is self-checking (asserts on all load-bearing
  identities); run with `python3 <script>` from inside `code/`.
- `supplements/` — self-contained HTML companions: `ledger-essay.html`
  (*Zero-Mode Shadows*, the interpretive essay, including its own
  post-instrument corrections) and `k3-residue-angle.html` (the
  interactive instrument).

Naming: **The Residue Ledger** is the project/instrument-suite identity;
the technical paper is *The Tangent Space Cannot See the Discriminant*;
the companion essay is *Zero-Mode Shadows*.

## Status and honesty notes

Draft v0.6. Attributions were checked against sources in August 2026.
The split/nonsplit discriminant distinction is settled invariantly in
the paper (explicit K-isotropic subspace for the split form; a descent
argument for the nonsplit class). The novelty claims in §6 are stated
with an explicit invitation to correction. An expert read of Theorem
1's novelty (in particular the reduced-germ conclusion for a single
rational Weil class) is the main gate before any submission.
