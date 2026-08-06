# Papers

Two papers on capacity-allocation bounds in coordinated systems, and
one standalone mathematics paper.

**Author.** Riley Rook <rileyrook@gmail.com>

## residue-ledger/

*The Tangent Space Cannot See the Discriminant* (the Residue Ledger
project). Standalone mathematics paper (draft v0.9, not yet submitted),
independent of the capacity-allocation pair. A local rigidity theorem
for rational Weil classes on polarized abelian 2n-folds of Weil type
(kernel of the infinitesimal Hodge obstruction = the n²-dimensional
Weil period domain; rank n(n+1); local Hodge locus smooth, reduced,
and equal to the Weil locus), certified by sparse exact SymPy
computations in dimensions four and six. In dimension six the
certificates run on both a split (solved) and a nonsplit (open)
discriminant class and return identical infinitesimal data, and an
explicit real conjugacy theorem upgrades this to every order, while
the arithmetic quotients ARE separated — by their rational boundary
(Witt indices 3 vs 2; totally degenerate cusps exist only on the
split side; local difference exactly at the primes 2 and 3; both
genera of class number one, with a dyadic type invariant separating
the boundary data and predicting cusp spectra (2,2,1) vs (1,1), with the corank-one
counts 2 vs 1 proved unconditionally): the tangent
cannot see the discriminant, the marked real-analytic germ cannot
see it, the rational boundary can. Includes a K3 period-loop
instrument and an interpretive companion essay. See
`residue-ledger/README.md`.

## convergence/

*Capacity-Allocation Predicts a Coordination Ceiling at k ≈ 7 ± 2.*
Workshop-shaped (~8 pp excluding
references). Concentrated empirical core: a single equation
k_max = B / [(1−φ)c + φσ], a structural argument for the
substrate-invariant ceiling k̄ ∈ [4, 10] from K log₂(K) entropy
combined with working-memory-class B, eight substrates clustering
in the band, and an own-collected pre-registered cross-architecture
probing experiment across four open-weight LLMs. The experiment
returns a mixed verdict (one cross-architecture confirmation of
the concept-probe middle peak in 4/4 models; a scope-bounded
falsification of a literature-anchored magnitude band that
sharpens what the framework actually commits to; one substantive
structural finding about hidden-state language preservation), and
is reported honestly rather than tidied into a clean confirmation.

The experiment artifact (pre-registration commit `708f13f`,
ADDENDA 001/002/003, source, configs, processed data, results,
plots) lives at `convergence/experiment/`. The heavy caches
(downloaded raw data, intermediate activations, virtualenv) are
not included; the README and `requirements*.txt` are sufficient
to reproduce.

## framework/

*A Capacity-Allocation Framework for Coordinated Systems.*
Long-form companion (arXiv preprint or journal venue). Develops
four extensions of the bound: three-mechanism taxonomy
(mechanism-1 / mechanism-2 / mechanism-3, with mechanism-1 as the
terminal-depth special case of mechanism-3); projection-class
taxonomy (P_3-rich / P_3-chunked / P_3-recognition); per-direction
multi-channel generalization with the φ-bimodality theorem;
cross-depth propagation form with three continuity constraints; the
architectural lever; a 19-row cross-mechanism table.

## Reading order

The convergence paper stands alone and is the recommended entry
point. The framework paper assumes the empirical convergence is
real and develops the structural framework that organizes it. Each
paper cross-references the other where appropriate but does not
require it.

## Building PDFs

Both papers are authored in Markdown. To build PDFs:

```
./build.sh                 # builds both papers
./convergence/build.sh     # builds the convergence paper only
./framework/build.sh       # builds the framework paper only
```

Requires `pandoc` and a LaTeX engine that handles Unicode well
(`xelatex` or `lualatex`). On macOS:

```
brew install pandoc
brew install --cask mactex          # or basictex + missing-package install
```

On Debian/Ubuntu:

```
sudo apt-get install pandoc texlive-xetex texlive-fonts-recommended \
                     texlive-latex-recommended texlive-latex-extra
```

PDF outputs land at `convergence/paper.pdf` and
`framework/paper.pdf` (gitignored; rebuild on demand).

## License

These papers are part of the surrounding repository and inherit
its license (Apache 2.0).

## Status

v0 drafts, 2026-05-16.
