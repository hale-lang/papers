---
title: "The Prime Torus Cannot See the Critical Line"
subtitle: "Arithmetic blindness and marked-boundary leakage for the Riemann zeta function"
author: Riley Rook
date: "Draft v0.3 — August 2026"
---

**Abstract.** We assemble an exact architecture for the Riemann
Hypothesis as a *restriction problem*, organized around two provable
blindness statements and one exact leakage ledger. (1) The Möbius lift
$F_\sigma(z) = \prod_p (1 - p^{-\sigma}z_p)$ of the free multiplicative
structure of $\mathbb{Z}$ to the infinite prime torus lies in
$H^2(\mathbb{T}^\infty)$ exactly for $\sigma > 1/2$, with energy
$\zeta(2\sigma)/\zeta(4\sigma)$: the critical exponent is present,
unconditionally, before any zero of $\zeta$ is mentioned. (2)
Completely multiplicative unimodular twists act on this field as
unitary coordinate rotations, so every unmarked Haar statistic is
twist-invariant — while Helson zeta functions realize essentially
arbitrary zero and pole sets in $21/40 < \mathrm{Re}\, s < 1$
unconditionally. No argument consuming only unmarked prime-torus
geometry can decide a critical-line statement. (3) Symmetrically, the
functional-equation channel — the uncompleted Riemann FE multiplier,
the trivial-zero divisor, order and exponential type, and the two-term
Riemann–von Mangoldt asymptotic with its $O(\log T)$ remainder class —
provably contains both RH-true and RH-false spectra: a
*class-relative* indeterminacy theorem whose witnesses are Nakamura's
functions (which carry ζ's exact gamma-ratio multiplier) and their
product with an explicit FE-symmetric quartic carrying a planted
off-line quadruple, with a second, distributional realization inside
Burnol's property-S class. The witnesses share this data with each
other, not with ζ itself — whose pole, residue, Dirichlet
coefficients, and exact counting constants remain available to a
proof — so the conclusion is: no argument *uniform over that class*
can decide critical-line placement. (4) A third channel completes the triptych with a
*located boundary*: the short-interval channel of
Matomäki–Radziwiłł factors through the pretentious projection — its
output is a functional of one twist frequency and one pretentious
distance, uniform over all 1-bounded multiplicative functions, a
class containing Helson twists with essentially arbitrary strip
zeros — yet the mean-value channel provably decides behavior at the
edge $\sigma = 1$: the channel sees the edge and cannot see the
line, and the crossing point is exactly the almost-all-to-all
intervals upgrade where phase/additive-energy data enters.
(5) What RH is, then, is a statement about the *coupling*:
by a classical criterion of Littlewood, RH is equivalent to convergence
of the height-cut, phase-aligned readings
$\sum_{n \le x} \mu(n)n^{-\sigma}$ for every $\sigma > 1/2$ — the first
object consuming both the prime-coordinate structure and the
Archimedean ordering — and the finite Möbius inverse defect
$1 - \zeta V_{N,w}$ has an exact leakage ledger: hard windows push the
defect past the boundary; polynomial windows redistribute it into the
generalized von Mangoldt tower, with the linear taper (the
Bettin–Conrey–Farmer window) producing $\Lambda(m)/\log N$ and the
quadratic taper producing Selberg's $\Lambda_2$ — the first explicit
two-prime convolution channel appearing at degree two. Every finite identity is
machine-certified in exact arithmetic (no floating point in any
proof-critical channel). The claims are deliberately modest: nearly
every ingredient is classical and cited as such; what is ours is the
paired-channel architecture (the torus channel forgets the zeros; the
FE channel forgets the arithmetic; RH lives in the marked coupling),
the class-relative indeterminacy formalization, the window-tower
packaging, and the certificate suite.

# Results

Throughout, $\mathbb{T}^\infty$ is the infinite-dimensional torus with
one coordinate $z_p$ per prime, with Haar measure; the Bohr
correspondence identifies Dirichlet series with square-summable
coefficients with $H^2(\mathbb{T}^\infty)$ via
$n^{-s} \leftrightarrow z^{\alpha(n)}$, where $\alpha(n)$ is the
exponent vector of $n$. Certificates for every finite identity below
are in `code/` (files and channel tags cited inline); the suite
distinguishes PROVED-BY-CODE / PROVED-IN-TEXT / CITED / EXPLORATORY.

**Theorem 1 (free-field criticality).** The Möbius lift
$$F_\sigma(z) = \sum_{n \ge 1} \mu(n)\, n^{-\sigma} z^{\alpha(n)}
= \prod_p \big(1 - p^{-\sigma} z_p\big)$$
(the product understood coefficientwise, as the $H^2$-limit of its
finite-prime sections — not as a pointwise-convergent infinite product
on the boundary torus) lies in $H^2(\mathbb{T}^\infty)$ exactly for
$\sigma > 1/2$, with
$$\lVert F_\sigma \rVert_2^2 \;=\; \sum_{n \ge 1}
\frac{\mu(n)^2}{n^{2\sigma}} \;=\; \frac{\zeta(2\sigma)}{\zeta(4\sigma)}.$$
The critical exponent $1/2$ is the finite-energy boundary of the free
multiplicative field, unconditionally and prior to any statement about
zeros.

*Proof.* Torus characters are orthogonal, so the energy is the
coefficient sum; the squarefree Dirichlet series equals the Euler
product $\prod_p (1 + p^{-2\sigma})$, which per prime equals
$(1 - p^{-4\sigma})/(1 - p^{-2\sigma})$ — certified symbolically
(`prime_cascade.py` [C4], [C8]) — whence the zeta ratio; convergence
is $\sum_p p^{-2\sigma} < \infty$, i.e. $\sigma > 1/2$. The
Bohr/$H^2$ framework is classical [@bohr1913; @hedenmalmlinseip1997].
$\blacksquare$

**Theorem 2 (prime-torus blindness).** Let $\chi$ be completely
multiplicative with $|\chi(p)| = 1$ and
$F_{\chi,\sigma}(z) = \prod_p (1 - \chi(p) p^{-\sigma} z_p)$. The
coordinate rotation $(U_\chi z)_p = \chi(p) z_p$ is Haar-unitary and
$F_{\chi,\sigma} = F_\sigma \circ U_\chi$; hence every unmarked
rotation-invariant statistic — all Haar-distributional data, including
each $L^q$ norm and moment where defined, and the energy threshold of
Theorem 1 — is identical across all such twists. But the associated Helson zeta functions
$\zeta_\chi(s) = \prod_p (1 - \chi(p)p^{-s})^{-1}$ realize essentially
arbitrary zero and pole configurations after continuation — in
$21/40 < \mathrm{Re}\, s < 1$ unconditionally, and in the whole strip
$1/2 < \mathrm{Re}\, s < 1$ under RH [@helson1969; @seip2020;
@bochkovromanov2021]; a 2024 preprint of Andersson [@andersson2024]
proposes prescription throughout $\mathrm{Re}\, s < 1$
unconditionally — if confirmed, the cleanest witness pair. We keep
Bochkov–Romanov as the load-bearing citation and state the
unconditional conclusion in their proven region. Consequently: **no argument that consumes only
unmarked prime-torus geometry can decide a critical-line statement.**

*Proof.* The rotation identity and the twist-invariance of the
coefficient energy are certified symbolically (`prime_cascade.py`
[C6], [C9]); rotation-invariance of Haar statistics is immediate from
unitarity of $U_\chi$ on $L^2$ of Haar measure. The zero-realization
results are cited. The no-go: a decision procedure invariant under
$U_\chi$ assigns the same verdict to twists whose zero sets differ in
the stated regions. $\blacksquare$

**Theorem 3 (marked-boundary equivalence — RH as a restriction
statement).** Let $P_x$ be the projection retaining exactly the
characters of integers $n \le x$ — a cutoff that consumes the
Archimedean size map $\alpha \mapsto \sum_p \alpha_p \log p = \log n$,
not intrinsic to the torus — and let $\mathbf{1} = (1, 1, \ldots)$ be
the aligned phase. Then RH is equivalent to: for every real
$\sigma > 1/2$, the marked-boundary readings
$$\mathcal{R}_\sigma(x) \;=\; (P_x F_\sigma)(\mathbf{1})
\;=\; \sum_{n \le x} \frac{\mu(n)}{n^{\sigma}}$$
converge as $x \to \infty$ (necessarily to $1/\zeta(\sigma)$).

*Proof.* The equivalence of RH with convergence of
$\sum \mu(n) n^{-\sigma}$ for every $\sigma > 1/2$ is classical
[@littlewood1912] (forward: the RH-equivalent bound
$M(x) = O_\varepsilon(x^{1/2+\varepsilon})$ plus partial summation;
converse: convergence for all real $\sigma > 1/2$ bounds the abscissa
of convergence by $1/2$, giving a holomorphic continuation of
$1/\zeta$ to the half-plane, and the functional equation reflects).
What is ours is the decomposition — free field, then Archimedean
height cutoff, then aligned phase — which identifies RH's entire
content as the behavior of one restriction operation on a field whose
free geometry is already critical at $1/2$ (Theorem 1) and provably
blind (Theorem 2). Substrate certificates: the signed cascade
$R_{k+1} = R_k - \tau_{\log p_{k+1}} R_k$ has closed form
$\sum_{d \mid P_k} \mu(d) H(u - \log d)$, resolved front exactly the
Mertens function below the next unborn prime, and Laplace transform
$\tfrac1s \prod_{p \le p_k}(1 - p^{-s})$ (`prime_cascade.py`
[C1]–[C3]); the Boolean form
$M(x) = \sum (-1)^{|S|}$ over subsets with
$\sum_{p \in S} \log p \le \log x$ ([C7]) states the remaining problem
as a parity/restriction estimate for the logarithmic-prime knapsack
down-set; and the aligned readings separate twists that the unmarked
torus cannot ([C6]/[C9] against `marked_lab.py` [X4]): the marking
sees, the torus does not. $\blacksquare$

*Remark (the two incompatible truncations).* For
$1/2 < \sigma < 1$ the prime-box truncation
$\prod_{p \le y}(1 - p^{-\sigma}) \to 0$, while under RH the height
truncation $\mathcal{R}_\sigma(x) \to 1/\zeta(\sigma) \ne 0$: two
limits of the same formal multiplicative field, and the analytic
continuation lives in their difference. Treating the divergent Euler
product in the strip as if the two summation geometries were
interchangeable assumes away the hard part — which is why
partial-Euler-product methods in the strip must be renormalized or
paired with zero-side information (the hybrid Euler–Hadamard
tradition [@gonekhugheskeating2007]).

**Proposition 4 (boundary redistribution and the window tower).** For
a window $w$ let
$V_{N,w}(s) = \sum_{n \le N} \mu(n)\, w(\log n / \log N)\, n^{-s}$ and
define the inverse defect $L_{N,w}(s) = 1 - \zeta(s) V_{N,w}(s)$, with
coefficients $\delta_{m,1} - c_{N,w}(m)$,
$c_{N,w}(m) = \sum_{d \mid m,\, d \le N} \mu(d) w(\log d/\log N)$ —
the exact ledger of what the finite Möbius inverse fails to cancel.
Then:
(i) hard cutoff $w = 1$: $c(m) = \delta_{m,1}$ for every $m \le N$ —
no interior leakage; the whole defect is pushed beyond the boundary;
(ii) linear taper $w(u) = 1 - u$ (the Bettin–Conrey–Farmer window,
conditionally shown to attain the conjectured optimal Nyman–Beurling
asymptotic under RH plus a zero-derivative moment hypothesis
[@bettinconreyfarmer]): for $2 \le m \le N$,
$\log N \cdot c(m) = -\sum_{d \mid m} \mu(d) \log d = \Lambda(m)$ —
the boundary defect becomes the prime harmonic
$-\Lambda(m)/\log N$ in the interior;
(iii) quadratic taper $w(u) = (1-u)^2$: the new interior channel is
$\sum_{d \mid m} \mu(d) \log^2 d = \Lambda_2(m) - 2\Lambda(m)\log m$,
where $\Lambda_2 = \mu * \log^2$ is Selberg's function, satisfying
$\Lambda_2 = \Lambda \log + \Lambda * \Lambda$.
In general the window's polynomial degree walks the generalized von
Mangoldt tower $\Lambda_j = \mu * \log^j$.

*Proof.* All identities are certified division-free in the free
$\mathbb{Z}$-module over $\{\log p\}$ and its symmetric square
(`inverse_defect.py` [W1]–[W5], including Selberg's identity itself as
[W4]). Connection to the Nyman–Beurling meter: the Báez-Duarte-type
energy of $L_{N,w}$ on the critical line is exactly the
approximation functional whose vanishing (over optimal coefficients,
$N \to \infty$) is equivalent to RH [@baezduarte2003;
@bettinconreyfarmer]; the ledger above is the exact coefficient-side
geometry of that meter's leakage. $\blacksquare$

*Remark (interpretation, deliberately modest).* At degree two the new
term contains the first explicit two-prime convolution channel
$\Lambda * \Lambda$ — the point where the leakage geometry first
meets the algebraic shape underlying sieve parity phenomena
[@friedlanderiwaniec]. This is a contact point, not a barrier
statement: Selberg's $\Lambda_2$ does not break the parity barrier,
and neither does this proposition. The window tower is a packaging of
binomial/Möbius-convolution identities, claimed as organization, not
as new sieve theory.

**Theorem 5 (finite-spectrum indeterminacy of the FE channel).** Let
$I_0$ assign to an entire function the data: the uncompleted Riemann
functional-equation multiplier — $F(1-s) = \Gamma_{\cos}(s) F(s)$ with
$\Gamma_{\cos}(s) = 2\Gamma(s)(2\pi)^{-s}\cos(\pi s/2)$, exactly
$\zeta$'s gamma ratio; the trivial-zero divisor; the order and
exponential type; and the two-term Riemann–von Mangoldt asymptotic
$N(T) = (T/2\pi)\log T + cT + O(\log T)$ together with its remainder
class. There exist entire $F_+, F_-$ with identical $I_0$-data such
that all nontrivial zeros of $F_+$ lie on the critical line
(unconditionally, refereed), while $F_-$ carries an explicitly planted
finite off-line symmetric quartet $\{3/4 \pm 2i,\ 1/4 \pm 2i\}$ with
the rest of its spectrum on the line. Consequently critical-line
placement is not determined on this class by $I_0$, and **any uniform
argument factoring only through $I_0$ must fail on it**.

*Scope rider (essential).* This is a class-relative statement, not a
$\zeta$-fiber theorem: the witnesses share $I_0$ with each other, not
with $\zeta$. $R_1$ is entire where $\zeta$ has its pole at $s = 1$;
it is not an ordinary Dirichlet series; and its linear counting
coefficient $(\log(4/2\pi) - 1)/2\pi$ differs from $\zeta$'s
$(\log(1/2\pi) - 1)/2\pi$ by $\log 4 / 2\pi$ — both formulas are
printed in [@nakamura2023]. A proof of RH therefore remains free to
consume $\zeta$'s pole, residue, Dirichlet coefficients, or exact
counting constants; what the theorem forecloses is any argument
uniform over the $I_0$-class.

*Proof.* Take $F_+ = R_1$, Nakamura's function [@nakamura2023,
Thm. 1.1]: it satisfies the $\Gamma_{\cos}$ equation — "the gamma
factor completely coincides with that of the functional equation for
$\zeta(s)$" (his words) — has zeros only at the negative even integers
and on $\mathrm{Re}\, s = 1/2$, and obeys the full counting law
$N(T) = (T/2\pi)\log T + cT + O(\log T)$. Take $F_- = Q \cdot R_1$
with $Q(s) = ((s - \tfrac12)^2 - w)((s - \tfrac12)^2 - \bar w)$,
$w = (\rho_0 - \tfrac12)^2$, $\rho_0 = \tfrac34 + 2i$: $Q$ has real
coefficients, satisfies $Q(1-s) = Q(s)$ identically, has exactly the
off-line quadruple as roots (all inside the open strip, none on the
line), and does not vanish at the negative even integers — all
certified (`fe_indeterminacy.py` [T3], [T5]). Then
$F_-(1-s) = Q(1-s)R_1(1-s) = \Gamma_{\cos}(s) F_-(s)$: same
multiplier, same trivial divisor, same order and type — and under the
positive-ordinate convention $0 < \mathrm{Im}\,\rho < T$ the planted
quartet contributes exactly two new zeros for $T > 2$ (its other two
members lie below the real axis; the two-sided count gains four), so
the two-term asymptotic and its remainder class are unchanged. The
zero set of $F_-$ is the planted quartet together with the on-line
zeros of $R_1$. $\blacksquare$

*Route B (distributional realization).* Inside Burnol's
Fourier-invariant even property-S class [@burnol2007, Déf. 4.26,
Thms. 4.30, 4.41], the same pair is realized with $F_+ = \hat A_a$
(all nontrivial zeros on the line — his Thm. 4.61, with the explicit
$A_a$ from [@burnol2002]) and $F_- = $ the Mellin transform of
$Q(E)A_a$, $E = -x\,d/dx$: the Euler operator preserves the class
(support-vanishing on the $D$-side trivially; on the Fourier side
because $\mathcal{F}(ED) = (1 + \xi\partial_\xi)\mathcal{F}(D)$ is
local — certified symbolically, [T2]) and acts on the Mellin transform
by an affine multiplier ([T1]), so polynomials in $E$ realize every
polynomial multiplier — machinery that is Burnol's own (his Lemme 4.38
and Prop. 4.39, stated in the zero-removal direction; we run it in
the planting direction). Caveat: $\zeta$ itself lies in his *extended*
class (poles; the Poisson comb does not vanish near $0$), so the
"proof of RH" consequence runs through Route A, which sits in
$\zeta$'s exact FE data; extending the counting theorem to the
extended class is an unpaid obligation if Route B is to carry that
weight alone.

*Remark (the shared remainder class is the discriminator).* Every
published witness pair fails the counting agreement earlier: Pólya's
1927 family
$e^{-z^2/2}(a + \cos z)$ — the ancestor of this statement, with his
own conclusion that from the shared properties "the reality of the
zeros cannot be inferred" [@polya1927] — has linearly many zeros,
failing the leading order; the Davenport–Heilbronn function
[@davenportheilbronn1936] sits at conductor 5; Epstein zeta functions
gave the first printed "a functional equation of the usual type is not
sufficient" [@pottertitchmarsh1935; cf. @bombierighosh2011, §2.1]; and
Nakamura's own on-line and off-line examples differ in the linear
term ($r_j \in \{2,3,6\}$ versus $\zeta$'s constant). The pair
$\{F, Q\!\cdot\!F\}$ shares both unbounded terms and the remainder
class — that agreement, and the instrument-relative formulation, are
what this theorem adds; the construction itself is elementary and is
not claimed. (v0.1 said "to all orders", which overstated: a
polynomial factor does not preserve the exact counting function, its
constant term, or its step structure — only the two-term asymptotic
and the $O(\log T)$ class.)

*Remark (layered markings; the Hamburger caveat, required).* Under
Hamburger's full hypotheses — an ordinary Dirichlet series with
analytic continuation, the pole, and finite-order/growth conditions —
the Riemann functional equation is rigid: the class collapses to
$C\zeta$ [@hamburger1921]. Two layers of arithmetic marking must be
separated: the ordinary Dirichlet-frequency expansion is already a
substantial marking (it is what Hamburger consumes; no Euler product
is required), and the Euler product is a further, strictly stronger
multiplicative marking. The witnesses above live outside the first
layer already (for Nakamura's $Q(s,a)$-type functions he states this
explicitly; for $R_j$ it follows from the $s$-prefactor and shifts;
$Q \cdot F$ is likewise not an ordinary Dirichlet series). The
no-go's precise content is therefore: **the FE multiplier plus coarse
spectral data cannot decide critical-line placement; the
Dirichlet-frequency marking is already rigidifying; and RH lives in
the coupling of the markings to the reflection.** Together with
Theorem 2 this is two-sided: the torus channel forgets the zeros; the
FE channel forgets the arithmetic; a proof must consume the coupling —
which is what the explicit formula and Weil positivity are.

**Theorem 6 (located boundary of the short-interval channel).** Let
$\mathcal{C}$ be the class of 1-bounded multiplicative functions
$f: \mathbb{N} \to \mathbb{C}$.

(a) *The discrepancy channel factors through the pretentious
projection, hence is blind to strip zero placement.* By the
Matomäki–Radziwiłł theorem [@matomakiradziwill2016] in the complex
form of Matomäki–Radziwiłł–Tao [@mrt2015, Thm. A.1 — cite the arXiv
version, which carries a recorded correction to the published proof
of its Prop. A.3]: for every $f \in \mathcal{C}$ and
$X \ge h \ge 10$,
$$\frac1X \int_X^{2X} \Big| \frac1h \sum_{x \le n \le x+h} f(n)
\Big|^2 dx \;\ll\; e^{-M(f;X)} \;+\;
\frac{(\log\log h)^2}{(\log h)^2} \;+\; \frac{1}{(\log X)^{1/50}},
\qquad M(f;X) = \inf_{|t| \le X}
\mathbb{D}\big(f, n^{it}; X\big)^2 .$$
The bound is a functional of the pretentious-distance datum alone,
uniformly over $\mathcal{C}$ with no further hypotheses: the
channel's information content is at most the pair (minimizing twist
$t_1(f, X)$, distance $M(f;X)$) — one real frequency and one
distance — and the zeros of the associated Dirichlet series appear
nowhere in that factorization. Since $\mathcal{C}$ contains the
Helson twists of Bochkov–Romanov (completely multiplicative,
unimodular, no further conditions) realizing essentially arbitrary
zero and pole multisets in $21/40 < \mathrm{Re}\, s < 1$
unconditionally [@bochkovromanov2021], no argument consuming only
this channel decides strip zero placement. Two caveats are part of
the statement: the bound is one-sided (vacuous in the pretentious
sector — the comparison form "short average $\approx$ twisted long
average" is *not* asserted here and is not in the published record),
and the twist is per-function, so the degeneracy assertion is for
families with matching distance data — exactly the regime the Helson
constructions inhabit.

(b) *The mean-value channel sees the edge.* Halász's theorem
[@halasz1968] reads mean values through pretentious distance; the
pretentious proof of $\zeta(1+it) \ne 0$
[@granvillesoundararajan2008; @ghs2019; @koukoulopoulos2019] and
Aymone's theorem [@aymone2022] — a completely multiplicative
$f: \mathbb{N} \to [-1,1]$ with $\sum_{n \le x} f(n) \ll
x^{1-\delta}$ for some $0 < \delta < 1/2$ *and* $F(1) = 0$ forces
$\zeta$ zero-free in $\mathrm{Re}\, s > 1 - \delta$ — show that
mean-value data of class members does constrain zeros at and near
$\sigma = 1$.

(c) Hence the channel's seeing-boundary is *located*: it includes
the edge and excludes the critical line, and the crossing point is
the almost-all $\to$ all-intervals upgrade — where the
phase/additive-energy data enters (higher uniformity; the
large-values program [@guthmaynard]) — precisely the data the
discrepancy channel discards. $\blacksquare$ (Assembly of cited
results; ours are the factorization observation, the located
framing, and the witnesses' pairing.)

*The finite shadow (certified).* Matomäki–Radziwiłł's own
introduction argument — in a short enough window every integer can
own a private prime, and a completely multiplicative $\pm 1$
function rigged on those primes produces a sign-change desert — is
realized exactly in `code/interval_rigging.py` ([R1]–[R4]): the
window $[226, 236)$, ten private primes, a certified constant-sign
window with four sign changes adjacent. The all-intervals
sub-channel below private-prime scale is adversarially riggable;
the almost-all channel survives because rigged windows are rare.

*Remark (the two-sided bracket).* Theorems 2, 5, and 6 now bracket
the "minimal seeing channel" question from both sides: Weil-positivity
data sees exactly (negative truncation eigenvalues count off-line
conjugate pairs [@bombieri2000]); the pretentious/short-interval
projection is blind; the mean-value channel sees only the edge. The
open question — the sharpest this paper leaves — is the minimal
extension of the blind channels that decides.

*Correction note (v0.1 → v0.2, kept deliberately).* Version 0.1
stated Theorem 5 as a $\zeta$-fiber result ("the exact $\zeta$ FE
data", "conductor", counting law "to all orders") and drew the
conclusion "any proof of RH must consume data outside $I_0$". A first
referee pass caught the overclaim: the witnesses share the data with
each other, not with $\zeta$ (pole, linear counting coefficient, and
Dirichlet structure all differ), and "all orders" overstated what a
polynomial factor preserves. The theorem is now class-relative with
the scope rider; the paired-channel architecture is unaffected. The
same pass softened the parity phrasing of Proposition 4 (the window
tower meets the two-prime convolution channel at degree two; it does
not break the parity barrier).

# The historical panel: the Davenport–Heilbronn family, exactly

The classical conductor-5 landmark is kept as a certified companion.
In the two-complex-dimensional FE-closed family
$V = \{aL(s,\chi) + bL(s,\bar\chi)\}$ ($\chi$ the quartic character
mod 5), all members share conductor, gamma factor
$\Gamma((s{+}1)/2)$, and the matrix functional equation; the
Euler-product members are the two corners (each other's duals, not
self-dual); the scalar-self-dual members form a single real ray
$\bar A = A\,\varepsilon(\chi)$ — and the Davenport–Heilbronn function
is that ray. Its famous constant
$\xi = (\sqrt{10 - 2\sqrt5} - 2)/(\sqrt5 - 1)$ is certified,
division-free in $\mathbb{Q}(\zeta_{20})$, to be exactly the
self-duality tuning — equivalently the half-argument of the root
number, $\xi = \tan(\tfrac12 \arg \varepsilon(\chi))$
(`dh_pencil.py` [P0]–[P3]). Moving from the Euler-product corners to the scalar-self-dual
interior ray produces a known RH violator while retaining the ambient
matrix functional-equation data — the corners' GRH remains
conjectural, which is why Theorem 5's unconditional witnesses use
Nakamura's functions instead. (Every member shares the matrix FE;
only the tuned ray satisfies the scalar self-dual equation.) Zero-distribution theory for this
family is due to Bombieri–Ghosh [@bombierighosh2011], with the
corrected density landscape in [@righetti2017].

# What is classical, and what is claimed

Nearly everything above is classical in substance: the Bohr/$H^2$
correspondence and the squarefree energy (Theorem 1's computation);
Helson's twists and the modern zero-realization theorems (Theorem 2's
inputs); Littlewood's criterion (Theorem 3's core); the linear-taper
window and its Nyman–Beurling optimality (Bettin–Conrey–Farmer);
Selberg's identity; Nakamura's witnesses; Burnol's operator machinery;
Hamburger's rigidity; the 1927/1935/1936 blindness lineage
(Pólya; Potter–Titchmarsh; Davenport–Heilbronn). The nearest published
no-go is Kaczorowski–Kulas [@kaczorowskikulas2007], a degree-one,
function-class-relative theorem (off-line zeros in every substrip for
degree-one extended-Selberg-class elements outside the Euler-product
stratum of the Kaczorowski–Perelli classification
[@kaczorowskiperelli1999]) whose abstract states the thesis — "a
positive answer would mean that arithmetic is necessary for proving
the Riemann Hypothesis" — without the instrument-relative form. The
Lax–Phillips appendix "How not to prove the Riemann hypothesis"
[@laxphillips1976; @laxphillips1980] is a method-specific autopsy, not
a class-level statement.

The inputs of Theorem 6 are entirely classical or recent-refereed
(Matomäki–Radziwiłł; MRT; Halász; Granville–Soundararajan;
Granville–Harper–Soundararajan; Aymone; Bochkov–Romanov); ours are
the factorization observation, the located-boundary framing, and the
pairing of witnesses.

To our knowledge new here: (1) the formalized **instrument-relative**
no-go of Theorem 5 — the named data class $I_0$ with the shared
two-term-asymptotic-and-remainder agreement (closer than any
published witness pair), the witness pair differing by an
FE-symmetric quartic, and the class-relative consequence about proof
channels; (2) the **window tower** of
Proposition 4 — the observation that the taper degree walks
$\Lambda_j = \mu * \log^j$, placing the parity barrier at degree two
of the leakage geometry; (3) the assembled **two-sided blindness
architecture** (Theorems 2 and 5 as symmetric panels, Theorem 3 as
the coupling statement) with its exact certificate suite. Each is
stated with an explicit invitation to correction; none is a claim of
progress on RH itself.

# Directions

- **The decomposition target.** Split the Nyman–Beurling energy of
  the defect $L_{N,w}$ as
  $E^2_{N,w} = E^{\mathrm{free}}_{N,w} + E^{\mathrm{mark}}_{N,w}$
  with the first term twist-blind and the second consuming the
  marking — then test, in a four-channel calibration ($\zeta$; a
  function-field zeta as known-good control; a Helson twist with
  prescribed off-line singularities; Davenport–Heilbronn), whether
  the marked term admits a positive factorization precisely in the
  arithmetic channel. The finite-field control is where the desired
  compression provably exists: a curve's Frobenius polynomial
  determines all future point and closed-point counts (a two-line
  Möbius inversion), with positivity forcing the critical circle.
- **The leakage Gram matrix.** For a window family $w_\theta$, the
  matrix $G_N(\theta, \theta')$ of defect cross-energies: hunt a
  structural factorization $G_N = B_N^* B_N + R_N$ with
  $R_N \succeq 0$, a monotone Schur-complement law in $N$, or a
  bounded-rank update under the birth of a new prime — proved
  structurally, not observed numerically.
- **The minimal seeing channel.** Now bracketed from both sides:
  $I_0$ (Theorem 5) and the pretentious/short-interval projection
  (Theorem 6) are blind; the mean-value channel sees only the edge;
  Weil-positivity data sees exactly (Bombieri's finite-truncation
  theorem: negative eigenvalues count off-line conjugate pairs
  exactly [@bombieri2000]). Locating the minimal deciding extension
  of the blind channels — conjecturally at the Weil form itself —
  would say positivity is not merely sufficient machinery but the
  first channel that can see at all.
- **The interface, precisely.** The additive–multiplicative
  interface is not blind: the large-values/additive-energy channel
  sees zero density [@guthmaynard]; what is blind is the
  phase-discarding projection. The follow-up is a quantitative
  ledger of exactly which phase data the seeing results consume.

*Reproducibility.* All proof-critical identities are exact (integer,
rational, cyclotomic, or symbolic; the one exploratory lab flags its
floating-point channels loudly) and accompany this draft in `code/`:
`prime_cascade.py`, `inverse_defect.py`, `fe_indeterminacy.py`,
`dh_pencil.py`, `marked_lab.py`; run `python3 verify_all.py` for the
suite with per-result grading. A companion paper in this collection
(*The Tangent Space Cannot See the Discriminant*) develops the same
blindness-and-coupling architecture at a Hodge-theoretic substrate;
nothing here depends on it.

# References
