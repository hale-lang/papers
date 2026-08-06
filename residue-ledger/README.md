# residue-ledger

*Exact Transversality Certificates for Weil Classes through Dimension
Six* — draft v0.2, August 2026. **Not yet submitted anywhere; treat as
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
  datasets. The arithmetic invariant separating solved from open
  sixfold Weil families is invisible to any method whose input is the
  local first-order variation of Hodge structure.
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
  - `sixfold_rig.py` — Theorem B: both discriminant classes, sparse
    924-dimensional machinery, the form-side convention lemma.
  - `k3_residue_angle.py` — Proposition C (emits
    `k3_residue_data.json`); `build_k3_page.py` regenerates the
    interactive supplement from it.

  Every script is self-checking (asserts on all load-bearing
  identities); run with `python3 <script>` from inside `code/`.
- `supplements/` — self-contained HTML companions: `ledger-essay.html`
  (the interpretive essay, including its own post-instrument
  correction) and `k3-residue-angle.html` (the interactive instrument).

## Status and honesty notes

Draft v0.2. Attributions were checked against sources in August 2026.
The split/nonsplit discriminant distinction is settled invariantly in
the paper (explicit K-isotropic subspace for the split form; a descent
argument for the nonsplit class). The novelty claims in §6 are stated
with an explicit invitation to correction. An expert read of Theorem
1's novelty (in particular the reduced-germ conclusion for a single
rational Weil class) is the main gate before any submission.
