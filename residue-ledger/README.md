# residue-ledger

*The Tangent Space Cannot See the Discriminant: local rigidity and
arithmetic boundary separation for Weil classes* — draft v0.15,
August 2026. **Not yet submitted anywhere; treat as
a working draft.**

A local rigidity theorem for rational Weil classes on polarized
abelian 2n-folds of Weil type, certified by exact-arithmetic
computations (no floating point, no transcendence numerics) in
dimensions four and six, plus a K3 period-loop instrument. Headline
results:

- **Theorem 1 (infinitesimal rigidity, n >= 2).** The kernel of the
  infinitesimal Hodge obstruction of every nonzero rational Weil class
  is exactly the n²-dimensional K-linear Weil period domain, with rank
  n(n+1); the local Hodge-locus zero scheme is smooth, reduced, and
  equal to the Weil locus at every point, including maximally split CM
  points. Depends only on the real signature (n,n). SHARP: at n = 1 a
  single rational class cuts out a strictly larger germ (only the full
  Weil plane recovers the cell) — verified as a boundary regression in
  `code/n1_sharpness.py`.
- **Theorem 2 (certificates; discriminant blindness).** Exact
  certificates in dimensions four (10/4/6) and six (21/9/12) — the
  sixfold pair run on a split (solved, disc [−1]) and a nonsplit
  (open, disc [−3]) hermitian form, returning identical infinitesimal
  datasets.
- **Theorem 3 (real conjugacy).** The explicit real isometry
  diag(1,1,1,1,1,3^(−1/2)) conjugates the entire local period geometry
  of the two discriminant classes — domain, Weil cell, Weil plane, and
  obstruction construction, fixing the base point — so, after
  forgetting the rational structure, the marked real-analytic local
  period data cannot distinguish the discriminant classes at any
  order; no rational conjugacy exists, by descent. Higher-order
  computations that see the discriminant must therefore consume the
  Q-structure. Verified exactly over Q(√3) in
  `code/conjugacy_theorem.py`.
- **Theorem 4 (the cusps can see the discriminant).** The two
  arithmetic quotients are separated by their rational boundary: Witt
  indices 3 (h₁ exactly hyperbolic) vs 2 (anisotropic kernel
  diag(1,−3)), so Q-ranks 3 vs 2, and the split quotient's Baily–Borel
  boundary has totally degenerate cusps while the nonsplit one has
  coranks ≤ 2 only. Locally the forms differ at exactly the primes
  {2, 3}. Certificates in `code/arithmetic_quotient.py`.
- **Theorems 5, 5b, 5c (class numbers; dyadic types; EXACT cusp
  spectra).** Both genera have class number one (strong approximation
  + a diagonal determinant lemma + Hilbert 90 + Cl(Q(i)) = 1). A
  dyadic type invariant — the norm-parity functional at the ramified
  prime, U(L)-invariant because unitary maps preserve norms —
  separates the boundary data, and a splitting-and-cancellation
  argument run at every rank proves the cusp spectra EXACTLY AND
  UNCONDITIONALLY at every corank: (2,2,1) vs (1,1). Corank 1
  (Theorem 5b): pairing ideal via the p = 3 positioning lemma; every
  primitive isotropic vector splits off [[0,1],[1,1]] with a rank-4
  complement whose parity IS the dyadic type; local uniqueness
  including the fixed Jordan shape at 3; class number one with the
  corrected determinant groups (the even complement's local
  determinant group at the ramified prime has index two — Kirschmer's
  exceptional case — and the global unit i cancels the defect).
  Coranks 2 and 3 (Theorem 5c): the same architecture at rank r —
  dual system, D-normal form via an exact parity transformation law
  (type A: diag(1,0,...,0), frozen at the coordinates of the all-ones
  vector; type B: diag(1,...,1), parities freed by odd complement
  vectors), complement genus fixed by type, class number one. At the
  deepest corank the complement VANISHES and the count is pure
  integral normal form — the deepest cusp turns out to be the easiest,
  and both formerly-conditional legs (within-type transitivity,
  parabolic local-global) dissolve rather than get computed.
  Certificates in `code/cusp_class_numbers.py`, `code/dyadic_types.py`,
  `code/theorem5_legs.py`, and `code/corank23_lemmas.py` (which also
  record the correction trail: one-cusp-per-depth asserted, retracted,
  then the richer spectra proved — the paper's own calibration lesson
  applied to itself, twice).
- **Proposition 6 (K3 dichotomy loop).** A twistor-type rational
  period conic in the K3 period domain whose very general fibers are nonprojective of
  Picard rank 19 while every one of its dense Noether–Lefschetz walls
  is projective of rank 20 — the instrument behind the paper's
  interpretive reading ("integer invariants are zero-mode shadows of
  continuous residual data").

The paper is deliberately explicit about what is classical and what is
new (§7): most of the mathematics is known; the contributions are the
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
  - `dyadic_types.py` — Theorem 5's dyadic correction: the norm-parity
    type invariant, exact type-A witnesses in L_1, the mod-4 exclusion
    on L_3, and the full corank-3 enumeration (15 subspaces, all
    containing the all-ones vector).
  - `theorem5_legs.py` — Theorem 5b: the corank-one splitting-and-
    cancellation certificates (unit-norm criterion, parity forcing and
    freedom, the sqrt(-7) witness, the even-binary Hensel table, the
    exact even complement of the type-A pair, the pairing-ideal and
    determinant-group substrates).
  - `corank23_lemmas.py` — Theorem 5c: the corank-2/3 certificates
    (explicit corank-3 canonical basis with Gram [[0,I],[I,diag(1,0,0)]],
    the parity transformation law, transvection generation of GL_r(F_2),
    exact standard splits of both corank-2 types with their even/odd
    complements).
  - `k3_residue_angle.py` — Proposition 6 (emits
    `k3_residue_data.json`); `build_k3_page.py` regenerates the
    interactive supplement from it.

  The scripts assert their headline claims (ranks, kernels, tuple
  equality across discriminants, known-zero channels, enumeration
  counts); statement-level and cited legs are labeled as such in the
  docstrings and in the verifier's grading legend — the suite
  distinguishes PROVED-BY-CODE / PROVED-IN-TEXT / CITED / CONDITIONAL.
  Run `python3 verify_all.py` from inside `code/` for the full suite;
  `requirements.txt` pins the environment. A GitHub Actions workflow
  (`.github/workflows/residue-ledger-verify.yml`) is configured to run
  the suite on every push touching this directory, but at the time of
  writing hosted runners have not picked up any run (an
  infrastructure-side issue), so there is NO independently green CI
  certificate yet: the verification of record is the local suite run
  reported in each version's commit message (last full pass: v0.12,
  15/15, 252s; code unchanged since). Floats appear only in one numerical
  asymptotic check and in the K3 page's plotting data — every
  proof-critical identity is exact.
- `supplements/` — self-contained HTML companions: `ledger-essay.html`
  (*Zero-Mode Shadows*, the interpretive essay, including its own
  post-instrument corrections) and `k3-residue-angle.html` (the
  interactive instrument).

Naming: **The Residue Ledger** is the project/instrument-suite identity;
the technical paper is *The Tangent Space Cannot See the Discriminant*;
the companion essay is *Zero-Mode Shadows*.

## Status and honesty notes

Draft v0.15 (novelty-search results folded into §7: Zink 1979 named
as the closest-titled prior work for Theorems 5-5c and flagged as the
single largest unresolved literature risk — the spectra's novelty claim
is explicitly provisional until a line-by-line Zink comparison is done;
Stover's Picard modular cusp work cited as the adjacent tradition and
citation-tree entry point. Prior v0.14: fifth-referee editorial pass: stale conditional grading
sentence in Theorem 5's proof replaced — Theorems 5b/5c close those
exact legs; the class-set/determinant-coset implication made logically
explicit in Lemma L6 (strong approximation makes each fiber a single
special genus, indefinite special genera are single classes, so X
trivial IMPLIES class number one) and wired into all three proofs;
corank23_lemmas.py added to the paper's reproducibility list;
Proposition-6 naming and §7 references synchronized in this README; the
CI claim replaced with the honest status — no independently green
Actions run yet, local suite is the verification of record. Prior
v0.13: structural: the boundary arithmetic moved to a dedicated
section — "The arithmetic of the boundary" — with the local-lattice
toolkit stated as formal lemmas L1-L6 (dyadic unit norms; odd/even
unimodular dyadic classification; determinant groups at the ramified
prime; the inert prime; global inputs), each tagged with its machine
certificate; Theorems 5/5b/5c keep their statements in Results with a
pointer; positional section references renumbered. Prior v0.12:
fourth-referee explication pass on Theorem 5c: move (iv)
stated as the full integral shear — u_i += z with c -= h(c,z) f_i —
so the complement is replaced by an isometric copy rather than left
dangling, with an exact two-lattice certificate; 3-adic-primitivity
wording in Lemma 5c.1; the parity-identity sweep extended to all index
pairs. Prior v0.11: Theorem 5c added: coranks 2 and 3 proved by the rank-r
splitting architecture — at corank 3 the complement vanishes and the
count is pure integral normal form — making the full cusp spectra
(2,2,1) vs (1,1) exact and unconditional at every corank; third-referee
explication items folded in: finite-field type-B normalization proof,
explicit unramified-norm uniqueness at 3, and the Q-form/real-form
distinction for the strong-approximation groups, including the
Q-anisotropic nonsplit corank-2 complement. Prior v0.10: second-referee
arithmetic repairs to Theorem 5b — the
pairing-ideal lemma replaces the false unimodularity appeal for the
nonsplit lattice; the H+H determinant-group error is corrected via
Kirschmer's exceptional even-hyperbolic case, with the global unit i
supplying the cancelling class — conclusion unchanged, mechanism
repaired. Earlier v0.8-v0.9 corrections: n >= 2 hypothesis with n = 1
sharpness; filtration index; atypicality identification withdrawn;
Proposition 6 clause corrections; Theorem 5 spectra stated as
conditional predictions beyond corank one; rational-Picard calibration
in the K3 script).
Attributions were checked against sources in August 2026.
The split/nonsplit discriminant distinction is settled invariantly in
the paper (explicit K-isotropic subspace for the split form; a descent
argument for the nonsplit class). The novelty claims in §7 are stated
with an explicit invitation to correction. An expert read of Theorem
1's novelty (in particular the reduced-germ conclusion for a single
rational Weil class) is the main gate before any submission.
