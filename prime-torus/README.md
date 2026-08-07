# prime-torus

*The Prime Torus Cannot See the Critical Line: arithmetic blindness
and marked-boundary leakage for the Riemann zeta function* — draft
v0.1, August 2026. **Not yet submitted anywhere; treat as a working
draft. This paper makes no claim of progress on the Riemann
Hypothesis; its results are blindness (no-go) statements, an exact
leakage ledger, and an assembled architecture, with everything
classical cited as such.**

Headline results:

- **Theorem 1 (free-field criticality).** The Möbius lift of the free
  multiplicative structure of the integers to the infinite prime
  torus lies in H² exactly for σ > 1/2, with energy ζ(2σ)/ζ(4σ) —
  the critical exponent is present, unconditionally, before any zero
  of ζ is mentioned.
- **Theorem 2 (prime-torus blindness).** Unimodular completely
  multiplicative twists are unitary coordinate rotations, so every
  unmarked Haar statistic is twist-invariant — while Helson zeta
  functions realize essentially arbitrary zeros and poles in
  21/40 < Re s < 1 unconditionally (Seip; Bochkov–Romanov). No
  argument consuming only unmarked prime-torus geometry can decide a
  critical-line statement.
- **Theorem 3 (marked-boundary equivalence).** RH ⟺ convergence of
  the height-cut, phase-aligned readings Σ_{n≤x} μ(n)n^{−σ} for every
  σ > 1/2 (the criterion is Littlewood 1912; the decomposition — free
  field, then Archimedean height cutoff, then aligned phase — is the
  paper's restriction-theorem framing). Companion structural point:
  the prime-box and height-cutoff truncations of the same field
  separate in the strip; the analytic continuation lives in their
  difference.
- **Proposition 4 (boundary redistribution; the window tower).** The
  finite Möbius inverse defect 1 − ζV_{N,w} has an exact leakage
  ledger: hard windows push the defect past the boundary; the linear
  taper (Bettin–Conrey–Farmer's window) converts it to −Λ(m)/log N;
  the quadratic taper's channel is Selberg's Λ₂ — the taper degree
  walks the generalized von Mangoldt tower, and the sieve parity
  barrier enters the leakage geometry at degree two.
- **Theorem 5 (FE-channel indeterminacy).** The exact ζ
  functional-equation data — gamma factor, trivial zeros, and the
  counting law TO ALL ORDERS — provably contains both RH-true and
  RH-false spectra: witnesses via Nakamura's exact-gamma-factor
  functions (QJM 2023) times an explicit FE-symmetric quartic with a
  planted off-line quadruple, plus a distributional realization in
  Burnol's property-S class. No argument with FE-invariant premises
  can decide RH; by Hamburger's theorem, the Dirichlet-series/Euler-
  product axiom is exactly the arithmetic marking that collapses the
  ambiguity. (Ancestors, cited and distinguished: Pólya 1927;
  Potter–Titchmarsh 1935; Davenport–Heilbronn 1936;
  Kaczorowski–Kulas 2007.)

## Contents

- `paper.md`, `references.bib`, `build.sh` — the paper (pandoc →
  paper.pdf, gitignored).
- `code/` — the exact certificate suite (Python 3, sympy; no floating
  point in any proof-critical channel):
  - `prime_cascade.py` — the signed Möbius cascade: closed form,
    Mertens resolved front, reciprocal-Euler-product transform, the
    energy threshold, the failed-contraction witness, the Helson
    rotation identity (exact), the Boolean-cube Mertens form.
  - `inverse_defect.py` — Proposition 4's ledger, certified
    division-free in the free ℤ-module over {log p} and its Sym²
    (including Selberg's identity itself).
  - `fe_indeterminacy.py` — Theorem 5's computational ingredients:
    the Euler-operator multiplier lemma (both Mellin conventions),
    the Fourier locality identity, the planting quartic, the
    composition.
  - `dh_pencil.py` — the historical panel: the Davenport–Heilbronn
    family in exact ℚ(ζ₂₀) arithmetic; ξ certified as the
    self-duality tuning (= half-argument of the root number).
  - `marked_lab.py` — the structure-search lab (EXPLORATORY: exact
    channels asserted; float channels loudly flagged).
  - `verify_all.py` — the suite runner with per-result grading
    (PROVED-BY-CODE / PROVED-IN-TEXT / CITED / EXPLORATORY).

## Status and honesty notes

Draft v0.1. The two-sided no-go (Theorems 2 and 5) is stated with an
explicit invitation to correction; the nearest published results are
itemized in the paper's literature section (Kaczorowski–Kulas is the
closest theorem-shaped predecessor; Pólya 1927 the ancestor; the
all-orders counting-law agreement of Theorem 5's witness pair is the
discriminator no published pair reaches). Bib entries marked "TO BE
VERIFIED" await a factuality pass before circulation. Two residual
caveats are recorded in the paper: the Lax–Phillips appendix is cited
via the authors' 1980 survey (book page not independently read), and
Route B's extension of the counting theorem to Burnol's extended
class is an explicitly unpaid obligation (Route A carries the main
theorem). A companion paper in this collection, *The Tangent Space
Cannot See the Discriminant*, develops the same blindness-and-coupling
architecture at a Hodge-theoretic substrate.
