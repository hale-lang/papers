# A Capacity-Allocation Framework for Coordinated Systems

**Author:** Riley Rook (rileyrook@gmail.com)
**Status:** v0 draft (2026-05-16)

---

## Abstract

We develop a capacity-allocation framework for bounded structural
arity in coordinated systems. The framework starts from a single
bound

> **k_max = B / [(1−φ)c + φσ]**                                  (1)

for a coordination locus with capacity B, full per-attachment cost
c, summary per-attachment cost σ, and interface formality φ ∈ [0, 1],
and develops four extensions: (i) a *three-mechanism taxonomy*
distinguishing scaling regimes by where φ sits — mechanism-1
(physics-fixed at substrate terminal depth), mechanism-2
(formal-interface composition, φ near 1), mechanism-3
(open-interface coordination, φ near 0); (ii) a *projection-class
taxonomy* (P_3-rich / P_3-chunked / P_3-recognition) sub-dividing
mechanism-3 by per-coordinatee state dimensionality and giving
substrate-invariant ceilings at 4–10, 10–30, and 100–500
respectively; (iii) a *per-direction multi-channel generalization*
in which equation (1) sums over unidirectional channels rather than
treating an interface as a single bidirectional object, licensing
asymmetric per-direction formalization without a half-formalization
penalty; (iv) a *cross-depth propagation form* in which the
per-attachment cost at depth d decomposes via the depth-(d-1)
coordinatee's exposed interface bits, with three continuity
constraints reducing per-sub-chain parameter count to ~3 effective
parameters. The framework's *architectural lever* — raising φ to
replace c with σ — is bimodal in practice under a stylized
step-function formalization-cost model, predicting empirical
clustering at φ ≈ 0 or φ ≈ 1 with rare intermediates. A 19-row
cross-mechanism table demonstrates the framework's reach across
chemistry, biology, neural systems, cognition, software,
distributed systems, multi-agent AI, organizational management,
macro policy, and modern ML architectures. The framework's
empirical core — a substrate-invariant ceiling at k̄ ≈ 7 ± 2 across
working-memory-class coordinators with rich-state coordinatees,
with own-collected cross-architecture probing evidence — is
developed in a companion convergence paper.

---

## 1. Introduction

A capacity-allocation bound

> **k_max = B / [(1−φ)c + φσ]**                                  (1)

recovers a striking range of empirical regularities in coordinated
systems: Miller's 7 ± 2 chunks of working memory, Cowan's 4 ± 1
distinct items, the 5–9 span-of-control bound on direct reports,
Dunbar's intimate-ring 5 (and his larger nested rings 15, 50,
150, 500 under chunked per-relationship state), the canonical
cortical microcircuit's 3–4 cell-type populations, mixture-of-
experts active-expert counts (1–8), surgical OR team sizes (5–10),
Paxos and Raft scaling theorems' linear N, and multi-agent LLM
orchestration saturation at 4–8 agents in role-based frameworks
vs. linear scaling in graph-based frameworks. The convergence is
documented in a companion paper.

The bound is parsimonious enough that a reader can be forgiven
for skepticism about the breadth of its claims. This paper makes
the framework's structure explicit: under what *mechanisms* does
the bound hold; under what *projection-class* does it admit a
substrate-invariant dimensionless ceiling; how does the bound
*decompose per-direction* when interfaces really consist of two
unidirectional channels with potentially different per-direction
parameters; how does the bound at one *depth* couple to the bound
at the next depth down through the locus tower of nested
coordinatees; and what *architectural lever* the bound identifies
in design.

### 1.1 Why this paper exists alongside the convergence paper

The convergence paper makes a narrow empirical claim: a
substrate-invariant ceiling at k̄ ∈ [4, 10] for open-interface
coordinators with rich-state coordinatees, supported by eight
substrates with otherwise unrelated B-units and by an
own-collected cross-architecture probing experiment. The
convergence paper is workshop-shaped: a single equation, a
single conjecture, an own-collected pre-registered experiment, a
falsification result reported honestly.

The framework material in this paper has its own audience. The
three-mechanism taxonomy distinguishes contexts where the bound
is *small* (mechanism-3) from those that *scale with system
capacity* (mechanism-2) from those that are *physics-fixed*
(mechanism-1, which we will show is the terminal-depth special
case of mechanism-3); without the taxonomy, the framework's
breadth is a footnote rather than a structural claim. The
projection-class formulation predicts which sub-substrates land
in which sub-class, generalizing the rich-state cluster across
the chunked and recognition regimes. The per-direction generalization
matters in domains where interface asymmetry is load-bearing
(software with side effects; central banks with formal
announcement but informal market response). The cross-depth
propagation form gives the bound a generative reading: the same
equation acts at every depth in a locus tower, with neighboring
depths coupled through the depth-(d-1) coordinatee's exposed
interface bits, and continuity constraints reduce per-sub-chain
parameter count enough that the framework can predict missing
configurations from neighboring anchors.

These extensions are framework-shaped rather than experiment-
shaped. They are best read by readers interested in the
unified structure rather than in the empirical bite. This paper
is for those readers.

### 1.2 Organization

Section 2 introduces the coordination context, derives the
bound (1), and develops the per-direction multi-channel form
(1′) — a generalization in which the bound sums over
unidirectional channels rather than treating an interface as a
single bidirectional object. Section 3 distinguishes the three
mechanisms. Section 4 derives the φ-bimodality theorem under a
stylized step-function formalization cost. Section 5 develops
the projection-class taxonomy with sub-classification by
per-coordinatee state dimensionality and the structural argument
for the rich-state ceiling. Section 6 develops the cross-depth
propagation form. Section 7 develops the architectural lever.
Section 8 presents a 19-row cross-mechanism table. Section 9
discusses limitations and future work.

---

## 2. The capacity-allocation bound

### 2.1 The coordination context

Let a *coordination context* be a tuple (L, B, c, σ, φ).

**L** is a *coordination locus*: a structurally-local point at
which attachments are made. Examples include an atom (with
attached bonds), a Lagrangian operator (with attached fields), a
manager (with attached direct reports), an LLM orchestrator
(with attached sub-agents), and a node in a consensus protocol
(with attached peers). The locus is the *one* in a 1→N relation.

We use *coordination locus* — and the shorthand *the locus*
within sections — to denote this structurally-local point. The
genetics, geometry, and psychology senses of "locus" are
unrelated; the modifier "coordination" disambiguates.

**B** is the *capacity* available at the locus. Capacity is a
resource that the locus must allocate across its attachments. The
unit and meaning of B vary by context: number of valence
electrons (atoms), mass-dimension budget for a renormalizable
operator (QFT), working-memory chunks (cognitive coordinator),
context-window tokens (LLM orchestrator), reserves and analytical
throughput (central bank), buffer space and protocol state slots
(distributed-system node).

**c** is the *full per-attachment cost*. To attach a coordinatee
or interaction partner with no formal interface, the locus must
hold full state about that partner: complete behavior, history,
possible reactions, or relevant features.

**σ** is the *summary per-attachment cost*. When a formal
interface exists, the partner's state can be reduced to a
contractual summary: a function signature, a typed protocol
header, a bounded message format, an exchange-rate-target
specification. We assume σ ≤ c.

**φ ∈ [0, 1]** is the *interface formality*. The fraction φ of
each attachment's coordination cost is met by summary state σ;
the remainder (1−φ) is met by full state c.

Intermediate φ is permitted by the model but, as Section 4
shows, empirically uncommon — interfaces tend to be designed
near one limit or the other.

**ι: per-channel formalization implementation cost.** Beyond
runtime per-attachment cost, formalization carries a one-time
implementation overhead per formalized channel: writing schemas,
building protocol state machines, parsers and validators,
integration glue. We denote this overhead ι. Unlike c, σ, and φ,
ι is paid *once per channel* rather than per attachment — it
amortizes across all k attachments using that channel. ι is
load-bearing for the φ-bimodality argument of Section 4; it does
not appear in (1) or (1′) directly because those bounds describe
runtime capacity allocation given a chosen φ.

### 2.2 Per-direction structure

What we have just described as a single "interface" is, in most
real systems, *two unidirectional channels* sharing a single
attachment. Each direction has its own per-direction full cost,
summary cost, and formality: forward channel (c_f, σ_f, φ_f) and
reverse channel (c_r, σ_r, φ_r). Examples:

- A function call has caller → callee (arguments, formal) and
  callee → caller (return values, formal; side effects, often
  informal). The two channels can have markedly different
  formality.
- A manager ↔ report relationship has manager → report
  (instructions / context, often open) and report → manager
  (status / output, often more formalized through structured
  reporting).
- An autoregressive transformer has input → concept (encoding
  channel) and concept → output (decoding channel). These are
  two unidirectional channels with intrinsically different
  per-direction costs c_f and c_r.

The per-direction structure is real even when both directions
are formalized symmetrically (Paxos, typed graph edges, software
function calls without side effects). When the two directions
are *asymmetrically* formalized — common in real systems — the
per-direction treatment makes the asymmetry explicit rather than
collapsing it into an averaged φ.

### 2.3 The bound

The coordination context's *span* k is the number of attachments
the locus sustains stably. The capacity-allocation argument
states that total capacity used cannot exceed B:

```
k · [(1−φ)c + φσ] ≤ B
```

Solving for the maximum stable k yields the bound:

```
k_max = B / [(1−φ)c + φσ]                                       (1)
```

This is the model's central claim. We call it the
**capacity-allocation bound**.

**Multi-channel form.** With per-direction structure made
explicit, the bound becomes a sum over channels d ∈ {forward,
reverse} (or, more generally, over any set of unidirectional
channels constituting the attachment):

```
k_max = B / Σ_d [(1−φ_d)c_d + φ_d σ_d]                          (1′)
```

Equation (1) is the special case where channels are summed and
treated as a single bidirectional cost; equation (1′) is the
general form. Most analytical content follows from (1); the
multi-channel form (1′) is invoked where per-direction asymmetry
produces predictions distinct from the averaged form (Sections 3,
4, and 7 below).

Two limiting cases recover familiar shapes:

- **Open-interface limit (φ = 0):** k_max = B / c. The locus's
  span is set by capacity divided by per-coordinatee full state.
  This is the regime where coordinator-side cognitive limits
  dominate.

- **Formal-interface limit (φ = 1):** k_max = B / σ. With σ ≪ c,
  this can be much larger. This is the regime where coordination
  scales with system-level capacity rather than cognitive
  bottlenecks.

### 2.4 Derivation

The bound derives from three assumptions, all made explicit.

**(A1) Asymptotic additivity in the rich-state regime.** The
locus's per-attachment cost is approximately additive at the
structurally-local resolution: total cost ≈ Σᵢ cost(attachment_i).
A1 holds asymptotically in the rich-state regime where
per-coordinatee state cost h(d-1) dominates the
identity-discrimination term log₂(k_max). Boundary cases where
additivity fails strongly — gossip protocols whose pairwise
overhead grows quadratically; group dynamics where each
additional participant adds n−1 new pairwise relationships —
require explicit corrections (Section 9).

**(A2) Mixed-formality cost.** When a fraction φ of each
attachment's interface is formalized, the per-attachment cost
interpolates linearly between c and σ. This is a modeling choice.
In practice, partial interface formalization may not yield linear
cost reduction — half-formalized interfaces sometimes inherit the
worse of both worlds. The empirical observation that φ is
near-bimodal across coordination contexts suggests this
nonlinearity is real (Section 4).

**(A3) Capacity bound.** Total cost is bounded above by the
locus's capacity B. When total cost exceeds B, the locus enters a
regime where the framework's predictions break — instability,
collapse, regime-change, or resort to non-local mechanisms.

Combining A1, A2, A3:

```
k · [(1−φ)c + φσ] ≤ B
k ≤ B / [(1−φ)c + φσ]
```

The maximum stable span is given by equality, yielding (1).

---

## 3. Three structural mechanisms

The bound (1) holds in coordination contexts where a "locus with
capacity" exists. The contexts of interest in this paper fall
into three structurally distinct families that we call
*mechanisms*. The mechanism distinction concerns *what kind of
entity is the locus and how its capacity arises*.

### 3.1 The taxonomy

- **Mechanism 2** (φ near 1, formal-interface composition).
  The locus is a designed coordinator (software runtime,
  distributed-system node, graph-orchestration framework, central
  bank with formal reaction function) and attachments are
  coordinated through *formalized* interfaces — typed protocols,
  function signatures, typed graph edges, contractual policy
  frameworks. Per-attachment cost is dominated by the summary
  state σ, which is small. The bound k_max = B / σ is large;
  mechanism-2 systems scale with system-level capacity rather
  than per-coordinatee cost. Recovered: linear scaling of
  distributed-system consensus protocols (Paxos, Raft, gossip),
  the unbounded fan-out of software function-call graphs, and
  the polynomial scaling of graph-based LLM orchestration
  frameworks. The architectural commitment to formal interfaces
  is the mechanism-2-defining design choice.

- **Mechanism 3** (φ near 0, open-interface coordination). The
  locus is a coordinator (human manager, LLM orchestrator with
  natural-language inter-agent communication, discretionary
  monetary regime) and attachments are coordinated through
  *open* interfaces — natural language, relationship state, ad-hoc
  discretion. Per-attachment cost is dominated by full state c,
  which is large. The bound k_max = B / c is small; mechanism-3
  systems saturate at small spans regardless of overall system
  size. Recovered: Miller's number, the saturation of role-based
  and conversational LLM orchestration frameworks, optimal
  decision-making group size, and the multi-objective trilemma
  on monetary regimes.

- **Mechanism 1** (φ fixed by physical law). The locus sits at
  its substrate's terminal depth: per-attachment cost c is
  substrate-irreducible (electrons in a valence shell,
  mass-dimension budget in a Lagrangian, metabolic budget in a
  microcircuit) because there is no further depth from which
  interface state could be decomposed. Interface formality φ is
  ≈ 0 (open-interface limit, since "formalization" is itself a
  designed interface-bit-compression that requires a non-terminal
  depth to operate at). Mechanism-1 is *on* the φ spectrum at
  the mechanism-3 endpoint, evaluated where parameters bottom
  out to substrate physics. The bound describes the
  structurally-local arity of a configuration at equilibrium
  with its substrate.

**Mechanism 1 is the terminal-depth special case of mechanism 3.**
Mechanism-1 contexts are not a separate structural family; they
are mechanism-3 evaluated at a substrate's terminal depth, where
parameters bottom out to substrate physics. Section 6's cross-depth
propagation form develops this in the context of the locus tower:
every depth runs the same propagation form (eq. (5) of §6); mechanism-1
labels the terminal-depth case where the recursion has nowhere
further to descend, and substrate physics directly sets c.

For mechanism 1, the bound (1) recovers per-locus arity
observations across physics, chemistry, and biology. Carbon's
four valence electrons divided by one electron pair per bond
yields k_max = 4. The 4D Standard Model Lagrangian's mass-dimension
budget of 4 divided by per-field mass dimension of ~1.0–1.5
yields k_max = 4 (for scalar field interactions) to 2–3 (for
fermion interactions). Cortical canonical microcircuits support
3–4 cell-type populations stably. The genetic code's triplet
codon is the smallest integer satisfying 4^k ≥ 21 amino-acid +
stop classes; the framework predicts k = 3 from first principles
with no fitting parameters.

### 3.2 Per-direction mechanism designation

With the multi-channel form (1′) in view, mechanism designation
can be *per direction*: an interface can be mechanism-2 in its
forward channel (formal protocol; φ_f near 1) and mechanism-3 in
its reverse channel (open feedback; φ_r near 0), or vice versa.
Most "interfaces" in real systems exhibit some directional
asymmetry: a function call formalizes argument-passing (forward)
tightly but side-effect propagation (reverse) loosely; a central
bank formalizes policy announcement (CB → market) precisely but
reads market response (market → CB) through informal indicators.
The per-direction treatment makes these asymmetries first-class
rather than hidden in an averaged φ.

We default to the bidirectional form (1) elsewhere and invoke
the per-direction designation (1′) where structurally significant.

---

## 4. The φ-bimodality theorem

The empirical observation that φ is near-bimodal across
coordination contexts is a finding to be explained, not stipulated.
This section derives it as a theorem under a stylized
step-function formalization-cost model. The result *per
unidirectional channel* — combined with the multi-channel form
(1′) — licenses asymmetric across-channel formalization (φ_f ≠ φ_r)
without the half-formalization penalty.

### 4.1 The cost model

The per-channel formalization implementation overhead ι is paid
in full as soon as one formalizes a channel at all, independent
of φ. The total cost a locus pays to operate a channel at
formality φ with k attachments is the per-attachment runtime cost
summed over attachments, plus ι if any formalization has been
adopted:

```
R(φ; k) = k · [(1−φ)c + φσ] + ι · 1[φ > 0]
       = k · c − k · φ · (c − σ) + ι · 1[φ > 0]                 (2)
```

The runtime savings from raising φ is *linear* in φ (slope
−k · (c − σ), since c ≥ σ). The implementation cost ι is *flat in
φ for any φ > 0* — paid in full as soon as one formalizes at all.

### 4.2 The theorem

Intermediate φ is strictly dominated whenever ι > 0:

- *If formalization is worth doing at all* — that is, if
  k · (c − σ) > ι — then φ = 1 strictly dominates any φ' ∈ (0, 1).
  Both options pay ι; φ = 1 captures the full runtime savings
  k · (c − σ), while φ' < 1 captures only k · φ' · (c − σ).
- *If formalization is not worth doing* — that is, if
  k · (c − σ) ≤ ι — then φ = 0 strictly dominates any φ' > 0.
  Both options forgo or pay ι; φ = 0 avoids it entirely while
  φ' > 0 pays ι in full but captures only partial runtime savings.

The only stable optima are φ = 0 and φ = 1. The decision threshold
sits at

```
k* = ι / (c − σ)                                                (3)
```

below this k, don't formalize; above it, fully formalize.
Intermediate φ is *never optimal* for any (c, σ, ι, k) with ι > 0.

### 4.3 Per-channel bimodality

Under the multi-channel form (1′), the argument applies *per
unidirectional channel* — each channel independently chooses
φ_d = 0 or φ_d = 1 by the threshold k_d ≷ ι_d / (c_d − σ_d).

This recovers an important distinction: *asymmetric formalization
across channels* (φ_f = 1, φ_r = 0, for instance) does not inherit
the worst-of-both penalty. Each channel is committed to its own
regime; the per-channel scaling holds; the binding constraint is
whichever channel has the higher per-direction cost. Well-designed
interfaces routinely formalize the high-cost direction while
leaving the low-cost direction informal, and they do not suffer
the half-formalization penalty.

By contrast, *half-formalization within a single channel* — a
unidirectional channel that formalizes 50% of its communication
and leaves 50% open-text — inherits the mechanism-3 capacity
bound on the open part *plus* the implementation cost of the
formal part. The result is strictly more implementation overhead
than a fully open channel *and* strictly less scaling capacity
than a fully formal channel.

### 4.4 What this licenses

The bimodality theorem is *per channel*, not *per nominal
interface*. What looks like an intermediate-φ interface — a
manager ↔ report relationship with φ ≈ 0.4, say — typically
decomposes into two committed-φ channels: a manager → report
channel at φ_f ≈ 0 (open-text instruction) and a report →
manager channel at φ_r ≈ 0.8 (structured status reporting
through tickets, dashboards, KPI updates). The interface as a
whole exhibits "intermediate φ" only if the per-direction
channels are averaged. Once decomposed, each channel sits at a
near-bimodal value.

---

## 5. Projection-class taxonomy

The three mechanisms of Section 3 are *observational categories*
of coordination context — empirical clusters in the cross-mechanism
table (Section 8) where φ is fixed by physics (mechanism-1), near
1 (mechanism-2), or near 0 (mechanism-3). This section formalizes
the mechanism distinction as a *projection-class taxonomy* — an
informal equivalence relation on coordination loci by
typed-neighborhood structure — that makes substrate-invariant
predictions: the scaling regime of k_max is determined by the
*projection class* of the locus's typed neighborhood, not by
substrate-specific units of B and c. The taxonomy is presented
informally; a rigorous categorical formalization (objects,
morphisms, projection functor) is deferred to future work.

### 5.1 Typed neighborhood and projection class

A coordination locus v sits within a graph G of nodes connected
by typed edges. The *typed neighborhood* of v is the multiset of
(edge-type, neighbor-class) pairs at v — every coordination
attachment v has, labeled by the category of relation (open-text
channel; typed-protocol channel; physical-bond channel) and by
the class of entity at the other end (rich-state coordinatee;
bounded-state peer; physical-substrate attachment). The
*projection class* of v is its typed-neighborhood structure
abstracted away from the specific substrates of v and its
neighbors.

Two nodes v and v' across radically different substrates can
share projection class. A human manager coordinating direct
reports and an LLM orchestrator coordinating sub-agents share the
projection class "open-interface coordinator with rich-state
coordinatees" if both have natural-language-channel edges to
coordinatees that maintain rich internal state. A Paxos proposer
and a software function call dispatcher share the projection class
"formal-interface coordinator with typed-protocol attachments"
if both have schema-validated typed-message edges to bounded-state
peers. A carbon atom and a 4D Standard Model vertex share the
projection class "physical-substrate locus with intrinsic-state
attachments."

### 5.2 Substrate-invariant scaling regime

Equation (1) and its multi-channel form (1′) give a dimensionless
k_max from ratios of substrate-specific quantities. Of the four
model parameters, three are determined by edge type and
neighbor-class — i.e., projection-class invariant: φ, σ, and the
*scaling form* of c (rich-state vs. typed-bounded-state). Only B
is substrate-intrinsic; absolute c values likewise scale with
substrate units.

This means that **projection-equivalent loci share scaling
regime even when their substrates differ**. The k_max *function
form* — linear in B for mechanism-2, sub-linear-with-ceiling for
mechanism-3, fixed-by-physics for mechanism-1 — depends on
projection class only, not on substrate units. Substrate
determines absolute B and c numbers; projection class determines
scaling regime.

### 5.3 Sub-classes of P_3 by per-coordinatee state dimensionality

The "rich-state" qualifier in projection class P_3 is doing real
work. Some mechanism-3 contexts saturate at k > 10 — Dunbar's
community ring (~150) and ATC sectors (10–25) — well above the
4–10 band derived for rich-state coordinatees. The structural
reason is that these contexts have *chunked* per-coordinatee
state: ATC tracks call-sign + altitude + heading + intent +
conflict candidates per aircraft (a small fixed-format header),
and Dunbar's community ring requires only recognition + minimal
pragmatic context per relationship rather than full relational
state. Lower h_task per coordinatee shifts the K log₂(K) bound
upward, giving larger k_max under *the same equation*.

P_3 sub-divides by per-coordinatee state dimensionality:

- **P_3-rich** (full operational / relational state per
  coordinatee): k̄ ≈ 4–10. Manager span, Cowan tight working
  memory (~4 chunks at maximum binding), Miller working memory
  (7 ± 2 chunks at typical binding — both Cowan-4 and Miller-7
  fall within this band; the difference reflects c-variation
  within P_3-rich, not a sub-class difference), LLM orchestration,
  surgical OR teams, MoE active experts, Dunbar's intimate ring
  (5).
- **P_3-chunked** (compressed / header state per coordinatee):
  k̄ ≈ 10–30. ATC aircraft tracking (~10–25 aircraft per
  controller), military squad-of-squads (~12–15), Dunbar's
  sympathy / friendship ring (~15–50, depending on the specific
  ring boundary).
- **P_3-recognition** (label / proxy state per coordinatee, e.g.
  recognition without active context): k̄ ≈ 100–500. Dunbar's
  community ring (150) and acquaintance ring (500).

Dunbar's empirical *nested rings* 5 / 15 / 50 / 150 / 500 are
the single clearest demonstration of this sub-classification:
the same individual maintains relationships at five different
binding strengths, each with progressively smaller c per
relationship, each giving progressively larger k_max under (1).
The framework predicts this nesting structure as a consequence of
c varying continuously across binding strengths within a single
substrate.

### 5.4 The structural argument for the P_3-rich ceiling

Section 4 of the convergence paper develops the K log₂(K)
entropy argument for the P_3-rich ceiling k̄ ∈ [4, 10] in detail.
We summarize the result here so this paper stands alone.

**Setup.** A coordinator at locus L manages K rich-state
coordinatees through an open interface (φ ≈ 0). To operate on
the right coordinatee without confusion, the coordinator's
working representation must encode, for each coordinatee:

1. **Identity bits.** log₂(K) bits to specify "which one of K"
   the coordinator is currently attending to.
2. **Task-relevant state bits.** h_task bits — the conditional
   entropy of the coordinatee's task-relevant state given the
   coordinator's current task context.

Total information:

  I_total(K) = K · log₂(K) + K · h_task                          (4)

**The bound.** Setting I_total(K) ≤ B and rearranging:

  K · log₂(K) ≤ B − K · h_task

Treating h_task as absorbed into the substrate's effective B
calibration (so B is the residual discrimination budget after
per-coordinatee state cost), and solving K · log₂(K) ≤ B
numerically: B = 10 bits → K_max = 4; B = 20 → K_max = 7;
B = 30 → K_max = 9; B = 50 → K_max = 13. For working-memory-class
effective B ≈ 15–25 bits, K_max lands in the 5–9 range,
recovering the cross-substrate cluster at k ≈ 7 ± 2.

**What this establishes.** The K log₂(K) growth form is
substrate-invariant for any coordinator distinguishing K
rich-state items at the identity level; the 4–10 numerical band
emerges from the form combined with any working-memory-class B;
the substrate-invariance of k̄_mech-3 ≈ 7 ± 2 has a structural
explanation.

**What it does not establish.** The specific value ≈ 7 (vs ≈ 4 or
≈ 9) within the band remains empirically calibrated. The
argument assumes h_task is bounded and additive across
coordinatees; domains with strongly non-additive coordination
cost require the cross-coordinatee mutual-information correction.
The claim that "effective B clusters at working-memory-class
across substrates" is itself a calibration, not a derivation.

### 5.5 Operational scope

The projection-class formulation is operational in domains where
typed-neighborhood structure is explicitly identifiable: software
systems (function signatures and call structure); distributed
systems (protocol state machines and message types); multi-agent
LLM systems (prompt template and inter-agent message schema);
within-model layer organization (per-bundle interfaces). It is
more abstract in domains where the typed neighborhood is implicit
or composite (macro policy regimes; cortical microcircuits). For
non-operational domains, the framework retains its
substrate-specific calibration.

### 5.6 Observer-depth scope

Projection-class invariance is an *at-fixed-observer-depth* claim.
Two loci across different substrates share scaling regime when
read from the same depth-position relative to the substrate's
tower. When projection-equivalent loci are compared across
observer depths, the per-direction (c, σ) projections re-weight
per the depth-gap, and an explicit depth-gap correction is
required to compare scaling regimes. The substrate-invariance
claim of this section is sharp at fixed observer-depth;
cross-depth comparison is developed in Section 6.

---

## 6. Cross-depth coupling and the propagation form

Section 5 derived the P_3-rich ceiling from K log₂(K) +
K · h_task information bookkeeping at a single depth, with the
per-coordinatee state cost h_task treated as a substrate-conditioned
input. This treatment is sufficient for the bound itself but
understates the framework's structure: h is not a free parameter.
It is the *depth-(d-1) coordinatee's exposed state*, and the
bound at depth d couples explicitly to the bound at depth d-1
through this cost. Making the coupling explicit yields a
propagation form for the framework — a system of equations
linking (B, c, σ, φ) tuples across depths.

### 6.1 Coordinatees as nested loci

The coordinatees of a depth-d locus are themselves loci at
depth d-1. A manager (depth d) coordinates reports (depth d-1);
each report is its own coordination locus, with its own internal
capacity, span, and interface. An LLM orchestrator (depth d)
coordinates sub-agents (depth d-1); each sub-agent has its own
context window, role, and exposed interface to the orchestrator.
A team-of-teams coordinator (depth d) coordinates teams (depth
d-1); each team has its own collective working memory and its
own external-facing interface. Every coordination locus is
*itself a coordinatee* at the next depth up.

This nesting forces a cross-depth coupling. The depth-d locus's
per-attachment cost is determined by what the depth-(d-1)
coordinatee exposes upward. Two depth-(d-1)-side quantities
matter:

- *Internal capacity* B(d-1) — the depth-(d-1) locus's own
  working budget. Bounded by substrate.
- *Exposed interface* I(d-1) — the compressed representation the
  depth-(d-1) locus offers to its depth-d coordinator. Bounded
  above by log₂(B(d-1)) (can't expose more state than the locus
  holds) and below by I_min(d-1) (must be enough to identify the
  locus uniquely):

    I_min(d-1)  ≤  I(d-1)  ≤  log₂(B(d-1))

Under mechanism-3 (open interface, φ ≈ 0), the depth-d locus
must hold the depth-(d-1) coordinatee's operational state per
attachment. The relevant state-bits the depth-d locus must carry
is denoted h(d-1):

    h_min(d-1)  ≤  h(d-1)  ≤  log₂(B(d-1))

with equality at the upper bound when full state visibility is
required, less when the coordinatee pre-aggregates. Under
mechanism-2 (formal interface, φ ≈ 1), the depth-d locus only
sees the compressed interface I(d-1) per attachment.

### 6.2 The propagation form

Substituting the cross-depth costs into equation (1) gives the
*propagation form* of the bound:

```
k_max(d) · [ (1−φ(d)) · (log₂(k_max(d)) + h(d-1))
           + φ(d) · I(d-1) ]
           = B(d)                                                (5)
```

Equation (5) is equation (1) with c and σ expanded to their
cross-depth-explicit forms. The framework's single-depth bound is
recovered as a special case where h(d-1) and I(d-1) are absorbed
into c and σ respectively.

The multi-channel form (1′) generalizes naturally: per-channel
costs become per-channel cross-depth couplings, with each
direction carrying its own h and I in the forward and reverse
channels.

### 6.3 Recovery of the P_3 sub-classes

Equation (5) recovers the P_3 sub-classification of Section 5.3
from the cross-depth coupling alone, with no additional postulates.
At φ(d) ≈ 0:

```
k_max(d) · [ log₂(k_max(d)) + h(d-1) ]  =  B(d)
```

Three regimes of h(d-1):

- **P_3-rich** — h(d-1) is large (full operational state per
  coordinatee). Dominates log₂(k_max(d)). The bound reduces to
  k_max(d) ≈ B(d) / h(d-1), with the substrate-invariant
  k̄ ≈ 4–10 emerging when the B / h ratio is class-conditioned in
  working-memory units (≈ 3–6).
- **P_3-chunked** — h(d-1) is intermediate (compressed header
  state). The same form k_max(d) ≈ B(d) / h(d-1) lands in the
  10–30 range when h(d-1) is ≈ 1–3 bits and B is
  working-memory-class.
- **P_3-recognition** — h(d-1) is minimal (label / proxy state,
  ≈ 1 bit). The h(d-1) term becomes small compared to
  log₂(k_max(d)). The bound reduces to
  k_max(d) · log₂(k_max(d)) ≈ B(d), with
  k_max(d) ≈ B(d) / log₂(B(d)), yielding 100–500 range for
  working-memory-class B.

The sub-class is determined by *what the depth-(d-1) locus
exposes upward* — full state, chunked summary, or recognition
label. This is a depth-(d-1)-side design choice that propagates
upward through equation (5).

The substrate-invariance claim of Section 5 sharpens
correspondingly: k̄ ≈ 4–10 holds across substrates not because B
is invariant in absolute units but because the *ratio* B / h(d-1)
is class-conditioned. A human manager's B (working-memory bits)
and an LLM orchestrator's B (200K–1M tokens) differ by orders of
magnitude in absolute terms, but their B / h(d-1) ratios are
both ≈ 3–6 within P_3-rich because h(d-1) scales with B within
the substrate. The substrate-invariance is a ratio claim, not an
absolute one.

### 6.4 Multi-step propagation through the locus tower

The adjacent-depth coupling iterates through the locus tower of
nested coordinatees. Equation (5) at depth d-1 determines
(B, k_max, h) at d-1, which feeds depth d's parameters via the
relations of §6.1; and so on across the chain. The system across
depths {d − X, …, d + Y} is *Markov-1* in baseline form: each
depth's parameters depend directly on the immediate predecessor's
(B, I) only.

Three structural continuity constraints reduce parameter freedom
across the chain:

- **Substrate continuity.** B varies smoothly across depths
  within a single substrate (a chain of human managers; a chain
  of LLM-orchestrator levels; a chain of cortical-area
  aggregations). Discontinuities mark substrate boundaries
  (neural → social, biological → cognitive).
- **Mechanism continuity.** φ is bimodal — it sits at 0 or 1
  with rare transitions. Within a sub-chain of constant
  mechanism, φ is fixed; chains decompose into mechanism-3
  sub-chains (φ ≈ 0) and mechanism-2 sub-chains (φ ≈ 1).
- **Projection-class continuity.** h(d-1) is class-conditioned
  within mechanism-3 sub-chains. Sub-class transitions require
  designed chunking infrastructure; within a sub-class of
  constant h, the class-typical value applies.

**Error-propagation is the structural complement of the
propagation form.** When a coordinator-locus at depth d fails
(k > k_max(d), instability), the failure traverses the locus
tower — to coordinatees at depth d-1, to containing loci at
depth d+1 (parent absorbs the failure or promotes the locus
outward), or across tower edges to adjacent depth-d loci
(mediated by depth-(d+1) connections through the tower's graph
structure).

The propagation chain terminates at mechanism-1 loci. As Section
3 noted, mechanism-1 is the terminal-depth case of mechanism-3,
not a separate class. Error traversal terminates wherever it
reaches a depth with substrate-irreducible c, which is
substrate-conditioned, not tower-position-conditioned.

**Substrate-boundary parameter re-anchoring.** Where a propagation
chain crosses from one substrate's tower into another (neural →
social organization; biological → cognitive), the form (5) is
preserved and the parameters re-anchor in the new substrate's
units. This is parameter re-anchoring under one continuous
equation, not exception-handling.

### 6.5 Effective parameters per sub-chain

Combining the three continuity constraints, a single mechanism-3
sub-chain of constant projection class reduces from 4 per-depth
parameters to ~3 effective parameters across all its depths:

- log B *intercept* — substrate scale at the chain's reference
  depth.
- log B *slope* — substrate-continuity rate (smooth variation of
  log B with d within the substrate).
- h class — P_3-rich, P_3-chunked, or P_3-recognition, giving the
  class-typical h value.

φ is fixed (mech-3 sub-chain); k_max(d) is derived from (5) at
each depth. A mechanism-2 sub-chain similarly reduces to ~3
effective parameters with σ replacing h. *The chain's empirical
content at every depth is a function of three structural
parameters once continuity is enforced — not 4(X + Y + 1).*

### 6.6 Anchoring

N anchors at depths {d_1, …, d_N} ⊂ chain provide 2N data points
(B(d_i) and k_max(d_i) at each), constraining the ~3 effective
parameters:

- N ≥ 2: parameters over-determined; excess anchors are
  consistency checks. If anchors disagree on the propagation
  form, this signals a substrate-boundary, mechanism transition,
  or projection-class transition that violates the assumed
  continuity.
- N = 1: parameters under-determined by 1 degree of freedom;
  class-typical assumptions close the system.
- N = 0: structural-prediction-only mode; the framework outputs
  a parameter family rather than a specific bound.

### 6.7 Candidate set at unanchored depth

Given anchors and continuity, the candidate parameter tuple at
depth d is the set of 4-tuples (B(d), φ(d), h(d-1), I(d-1))
consistent with (5), the three continuity constraints, and
matched anchor data points. This *candidate set* S(d) is
typically a small interval in (B, k_max) space when anchor
density is high and continuity is enforced. The interval's
width is the framework's prediction precision at depth d.

### 6.8 Bifurcation under φ-bimodality

When the chain spans both mechanism-2 and mechanism-3 sub-chains,
S(d) at an intermediate depth is bimodal:

```
S(d) = S_mech-3(d) ∪ S_mech-2(d)                                (6)
```

with each cluster a separate stability region. φ-bimodality
(Section 4) says intermediate φ is not stable; only the two
clusters are. Empirically, organizations exhibit this bimodal
pattern at the team-of-teams depth — small-team (mechanism-3,
k_max ≈ 5–9) vs. scaled-microservices (mechanism-2, k_max ≈
tens-to-hundreds) — and the framework recovers it from
cross-depth constraint structure without postulating it
separately.

### 6.9 Three classes of forward prediction

When S(d) admits stable configurations not in the empirical
record, the framework produces a testable forward prediction. By
the gap's nature:

**(i) Engineering gaps.** Configurations the framework predicts
should be stable but humans haven't yet engineered. Example: a
hybrid LLM-orchestration-with-typed-protocol architecture is
predicted to exhibit P_3-chunked saturation (k_orch ∈ [10, 40])
when current architectures occupy only the P_3-rich band ([4, 8]);
cross-depth analysis from the single-agent depth and the
agent-cluster depth places the typed-protocol regime in S(d) for
the intermediate depth.

**(ii) Discovery gaps.** Configurations existing in nature but
not yet observed. Example: novel cell-type configurations
predicted by neighboring-depth anchors (cellular and tissue) but
not yet identified by single-cell omics. Mendeleev's
missing-element predictions are the historical template.

**(iii) Parameter gaps.** Regimes of (B, φ, h) not accessed by
current substrates. Example: what the framework predicts for
working-memory-class systems with B 100× larger than today's
frontier LLMs. Each parameter-gap prediction tests whether the
cross-depth continuity holds under extrapolation.

Each class is testable as the relevant substrate evolves or new
domain anchors accumulate.

---

## 7. The architectural lever

Equation (1) shows that increasing φ — formalizing the interface
between locus and coordinatee — raises k_max monotonically. This
is the model's *architectural lever*: any system facing
capacity-bound saturation has a direct design move available.

### 7.1 The lever

Replace open-interface coordination with formal-interface
coordination; replace ad-hoc state-tracking with typed contracts;
replace natural-language inter-agent communication with structured
outputs and graph orchestration. Each move raises φ and replaces
c-sized per-attachment state with σ-sized protocol-state header.

### 7.2 Where the lever is available

The lever is not always available:

- **Mechanism-1 contexts are fixed by physical law.** φ cannot
  be designed. Carbon's octet rule, mass-dimension counting,
  canonical microcircuit cell-type populations — these have no
  design knob for φ.
- **Mechanism-3 contexts where the open interface is
  load-bearing for the work product.** Relationship-management,
  judgment-laden discretion, exploratory open-ended reasoning.
  Formalizing the interface would lose the work itself.

The model identifies the bound; what to do about it depends on
whether the formality lever is reachable in the specific context.

### 7.3 Per-channel application

Under the multi-channel form (1′) and the φ-bimodality theorem
of Section 4, the architectural prescription is *per channel*,
not per nominal interface. Each unidirectional channel of an
interface should be either fully formalized (φ ≈ 1) or accept
the mechanism-3 bound and be designed within it.

Asymmetric formalization across channels is permitted and often
optimal. Formalizing the high-cost direction while leaving the
low-cost direction informal does not trigger the
half-formalization penalty; it concentrates formalization effort
where it raises k_max most.

### 7.4 Segmentation of hybrid architectures

Where flexibility and scale are both needed, the architectural
move is to *segment* rather than blend. A mechanism-2 graph
orchestrator at the top, with mechanism-3 leaves (small agent
clusters of 4–8 reasoning together in open-text). The top layer
scales with B (graph executor capacity); each leaf operates
within its own mechanism-3 bound; total system arity is the
product, not blended.

This pattern is visible across substrates:

- **Software.** Microservice architectures with formal typed APIs
  at service boundaries and mechanism-3 small-team coordination
  within each service.
- **Multi-agent AI.** Graph-orchestrated top layers (LangGraph-style)
  with role-based agent clusters at the leaves.
- **Macro policy.** Rules-based central banks with discretionary
  intervention reserved for crisis moments.
- **Organizations.** Formal team-of-teams hierarchy with
  small-team open coordination within each team.

### 7.5 The lever in production

Empirically, the lever's effects are observable:

- **Production multi-agent systems migrating from
  CrewAI / AutoGen (mechanism-3) to LangGraph (mechanism-2)** as
  deployment scale grows.
- **Software systems formalizing cross-team boundaries through
  typed APIs and microservices** while preserving small-team
  open coordination within services. Knowledge-graph platforms
  that represent software systems as typed-edge knowledge graphs
  operationalize this prescription at production scale.
- **Distributed-system consensus protocols** (Paxos / Raft /
  gossip) — formal protocols achieving linear scaling with N
  through small σ per peer.
- **Rules-based monetary regimes** with transparent reaction
  functions (Fed-style inflation-targeting; ECB-style forward
  guidance) achieving sustained policy commitments that
  discretionary regimes cannot.

The framework's prescription is not novel — distributed-system
designers, software architects, and central-bank reformers
already make these moves on different grounds. The framework
gives a unified rationale: each move is the same lever, raising
φ to replace c with σ.

---

## 8. Cross-mechanism table

This section reports nineteen coordination contexts (with codon
as a mechanism-1 sub-row of cortical microcircuit, listed as 5b)
fitted to the capacity-allocation form (1). The contexts span
chemistry, biology, neural systems, software, organizational
management, distributed systems, multi-agent AI, macroeconomic
policy, social anthropology, cognitive psychology, microeconomics,
political theory, safety-critical operations, and modern ML
architectures.

The aim is *coverage*: demonstrating that the same model form
holds across contexts whose underlying physics, biology, or
institutional structure could not be more different. The
discrimination across mechanisms — different φ, different c-vs-σ
ratios — is what makes the cross-domain unification non-trivial.

### 8.1 The table

| # | Context | Locus | B | c | σ | φ | k_max (predicted) | k (observed) | Mech |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Carbon-shell chemistry | atom | 4 valence e⁻ | 1 e⁻ / bond (carbon's contribution) | n/a | n/a | 4 | 4 | 1 |
| 2 | Lanthanide coordination | atom | ~14 (orbital + size) | 1 / ligand | n/a | n/a | ~14 | 12–14 | 1 |
| 3 | 4D Standard Model vertex | Lagrangian operator | 4 (mass dim.) | 1.0 / scalar; 1.5 / fermion | n/a | n/a | 4 (scalar) / 2–3 (fermion) | 4 / 3 | 1 |
| 4 | Enzyme active site | binding pocket | ~3–4 substrate slots | 1 / substrate | n/a | n/a | 2–4 | 2–3 (often 4) | 1 |
| 5 | Cortical microcircuit | canonical motif | 3–4 cell-type pop. budget | 1 / cell type | n/a | n/a | 3–4 | 3–4 | 1 |
| 5b | Genetic code (codon length) | codon | log₄(21) ≈ 2.196 | 1 nucleotide / codon position | n/a | n/a | 3 (smallest integer ≥ 2.196) | 3 (universal) | 1 |
| 6 | Software function call | call frame | call-stack budget | per-callee state | function signature | ~1 | scales with B | scales (no per-call k bound) | 2 |
| 7 | Graph-based orchestration | graph node | per-node buffer | per-edge state | typed-edge contract | ~1 | scales with B | scales linearly | 2 |
| 8 | Paxos consensus round | proposer | quorum-state buffer | per-acceptor state | protocol-state header | ~1 | scales with B | scales linearly with N | 2 |
| 9 | Manager (human) | manager | ~7 chunks (working mem) | ~1 / report | n/a | ~0 | ~7 | 5–9 (median 7–8) | 3 |
| 10 | LLM orchestrator (role-based) | orchestrator | 200K–1M tokens | 10–50K tokens / agent | (not formal) | ~0 | 4–100 (B-dependent) | 4–8 (saturation) | 3 |
| 11 | Decision-making group | participant | ~7 chunks | 1 / other participant | n/a | ~0 | ~7 | 4–8 (canonical 5–7) | 3 |
| 12 | Monetary policy regime | regime | reserves + tools + credibility | 1 / objective | n/a | ~0 (discretionary) / ~1 (rules-based) | 2 / 3+ | varies | 2/3 |
| 13 | Stable social relationships (Dunbar) | individual | neocortex social-tracking budget | 1 / relationship (chunked) | n/a | ~0 | ~150 (community ring) | 150 (Hill & Dunbar 2003); nested rings 5/15/50/150/500 | 3 |
| 14 | Working memory (Miller / Cowan) | cognitive locus | discriminability budget | high (tight) / low (chunked) per item | n/a | ~0 (both regimes) | 4 ± 1 / 7 ± 2 | 4 ± 1 (Cowan); 7 ± 2 (Miller) | 3 (P_3-rich) |
| 15 | Firm boundary (Coase) | firm-vs-market boundary | internal coord. capacity | mech-3 internal (high) | mech-2 market (low) + ι | varies | varies by industry | Coase 1937; Williamson 1975 | 2/3 boundary |
| 16 | Collective action (Olson) | group | mutual-monitoring budget | k² monitoring cost (small group) | per-member contribution-tracking (large group) | ~0 (small) / ~1 (formal) | ≤7 (small) / ≥50 (large) | Olson 1965; Ostrom 1990 | 3 → 2 |
| 17 | ATC sector | controller | attention / working-memory budget | 1 / aircraft (call-sign + state) | n/a | ~0 | 10–25 | 10–25 (FAA / Eurocontrol) | 3 (P_3-chunked) |
| 18 | MoE active experts | gating network | routing budget | per-active-expert integration | per-routed-token header | ~0 (gating informal) | 1–8 active | 1–8 (Switch; Mixtral; Gemini 1.5) | 3 |
| 19 | Software engineering team | team | collective working memory + integration | per-developer state | typed-API / microservice contract | ~0 within / ~1 across | 5–9 within | 5–9 (Brooks; Bezos two-pizza) | 3 (within) / 2 (across) |

### 8.2 Reading the table

**Mechanism 1 (rows 1–5b).** B and c are independently measurable
in domain-native units. Predicted k matches observed k within
~10% across all rows; the framework recovers known results
without fitting parameters. The genetic-code row (5b) is the
cleanest: k = 3 follows from log₄(21) ≈ 2.196 with no domain-
specific parameters. Carbon's k = 4 follows from the octet rule.
The canonical microcircuit's k = 3–4 follows from local
metabolic and signaling balance.

**Mechanism 2 (rows 6–8).** σ is measurable in bytes per
attachment; B is measurable in coordinator-side capacity. The
linear-scaling-with-B observation matches production scaling
patterns: software function-call graphs do not exhibit per-call
arity bounds; graph orchestrations scale to hundreds of nodes;
Paxos / Raft clusters operate at hundreds to low thousands of
peers per consensus group.

**Mechanism 3 (rows 9–11, 13, 14, 16 small-group, 17, 18, 19
within).** B is named-as-Miller for human contexts and is not
derived from first principles; for LLM orchestration B is the
orchestrator's context window, which is independently measurable.
c is estimated from per-coordinatee state. The K log₂(K)
derivation of Section 5.4 explains the substrate-invariant
clustering at k ≈ 4–9 across rich-state contexts.

**Mixed and architecture-conditional rows (12, 15, 16, 19).**
Row 12 (monetary policy regime) sits in the mixed region: a
regime can be operated discretionarily (low φ; observed
Mundell–Fleming 2-of-3 saturation) or rules-based (high φ;
algorithmic inflation-targeting + transparent reaction function).
Row 15 (Coase firm boundary): firms exist where internal mech-3
coordination cost is less than market mech-2 transaction cost
plus formalization overhead ι — the architectural-lever decision
threshold k = ι / (c − σ) of Section 4.2 applied to economic
coordination. Row 16 (Olson collective action): the threshold
k = ι / (c − σ) applied to cooperation specifically — below it,
small groups achieve cooperation through pairwise mutual
monitoring; above it, formal incentives dominate. Row 19
(software teams): within-team mechanism-3 at k ≈ 5–9; across-team
mechanism-2 through typed APIs.

### 8.3 What the cross-context fit shows

**(O1) Mechanism distinctions are real, not artifactual.** The
three mechanisms produce empirically distinct k_max ranges
(roughly 2–4 for mechanism-1, B/σ-scaling for mechanism-2, and
4–9 for mechanism-3 in the P_3-rich regime). If the model were
trivially restating per-domain known bounds without
mechanism-discriminating content, we would not see three
distinct k clusters reflecting φ differences.

**(O2) Cross-context φ is empirically bimodal.** Across the
rows, no row reports φ in the (0.2, 0.8) intermediate range.
Either interfaces are formalized (mechanism-2; rows 6–8) or they
are open (mechanism-3; rows 9–11), with mechanism-1 contexts
having φ fixed by physics. The bimodality theorem of Section 4
predicts this; the table empirically confirms it.

**(O3) The same mechanism distinction operates at multiple
resolutions.** LLM orchestration rows (10) and within-model
layer-organization observations (Wendler et al. 2024; Ng 2026)
report the *same* three-way mechanism distinction at *different*
scales. The framework predicts this convergence as a
consequence of mechanism-distinction-following-interface-formality-
variation.

### 8.4 Boundary cases: instability promotes to a containing locus

Two contexts initially appear to violate the framework's
applicability. On closer inspection, both are cases where the
local locus has *failed* to resolve coordination at its level and
the error propagates outward in dimensionality until a containing
locus absorbs it.

**Phase transitions / critical phenomena.** At criticality,
correlations diverge across all length scales; the local order
parameter loses its stability bound. Read structurally: this is
*exactly* a coordination failure — the system's local locus
cannot allocate capacity to maintain its order, and the
instability propagates to the containing thermodynamic ensemble,
which absorbs the bound through phase change. The framework
predicts: where local arity exceeds k_max, the locus dissolves
and the coordination problem promotes one level outward. Phase
transitions are the substrate-level expression of this promotion.

**Cosmological all-to-all gravitational coupling.** At aggregate
resolution, every mass interacts gravitationally with every
other mass, suggesting unbounded coordination. At the
*structurally-local* resolution, gravity is pairwise — A1 holds
at the per-pair level even in N-body cosmology. The framework
applies at the local pairwise level; the aggregate "coordination"
is the emergent property of pairwise interactions running, not a
locus that fails.

**General principle: error propagation through containing loci.**
Local coordination failure does not exit the framework; it shifts
the locus. When a system at level N exceeds its k_max — too many
bonds, too many sub-agents, too many policy commitments, too
many simultaneous actions — the local stability breaks and the
coordination load promotes to level N+1 (the containing system,
the supersystem, the next larger locus that has the capacity to
absorb it). Examples: a class accruing too many responsibilities
refactors to a containing module; a manager's span exceeding 5–9
promotes to multi-layer hierarchy; a regime exceeding the
impossible-trinity bound is supported by supranational systems
(IMF lending, swap lines); a cortical microcircuit exceeding
metabolic balance reorganizes across area boundaries.

---

## 9. Limitations and future work

### 9.1 What the framework does not claim

- **Not novel single-domain empirics.** Mundell–Fleming, Miller,
  Dunbar, Coase, Olson, the canonical microcircuit, Paxos
  correctness proofs — each remains established within its own
  domain literature. The framework re-expresses them in unified
  vocabulary.
- **Not a substitute for domain-specific theory.** Domain-native
  tools remain the operational tools within their domains. The
  capacity-allocation form is a unifying layer, not a
  replacement.
- **Not a causal-generative claim.** Substrates differ; only the
  *form* of the bound is shared. Whether this commonality is
  meaningful or artifactual is partly resolved by forward content
  evaluation.
- **Not a derivation of within-band values.** Specific numerical
  values (Cowan's 4, Miller's 7, cortical 3–4) reflect
  substrate-specific calibrations; the framework predicts the
  band, not the within-band number.

### 9.2 Limitations

**(L1) B and c are independently measurable in only some
contexts.** For mechanism-1 contexts, B is set by physical
constants. For mechanism-2 contexts, σ is small and measurable.
For mechanism-3 contexts, B is sometimes named-as-Miller and is
not derived; c is estimated from per-coordinatee state but not
derived from first principles. This means mechanism-3 fits have
*structural* content (the model predicts a small constant k in
the open-interface regime) but not always *quantitative* content
beyond what domain-specific bounds already establish.

**(L2) Per-coordinatee state c is approximated as additive at
structurally-local resolution; cross-coordinatee mutual-information
terms appear at large k.** A1 (Section 2.4) treats per-attachment
cost as roughly additive. Domains with strongly non-additive
coordination cost (gossip protocols; large-group dynamics)
require explicit modeling of the cross-coordinatee
mutual-information term. The LLM-orchestration regime admits a
quadratic correction κ · k² from per-direction cross-agent
coordination cost, yielding the sub-linear saturation form
k_sat ≈ √(B/κ) that matches observed scaling across model
generations. Other contexts may have similar non-additive
corrections that (1) does not capture.

**(L3) The φ parameter is treated as continuous in the model but
is empirically bimodal.** Section 4's theorem derives this from
the step-function formalization cost. The intermediate-φ
predictions of (1) are extrapolated rather than empirically
calibrated.

**(L4) Mechanism-1 specific values come from domain physics, not
from the framework.** The framework does not derive carbon's
k = 4 from (1); it recognizes carbon's k = 4 as a mechanism-1
instance whose specific value is set by the substrate. This is
structurally consistent with the framework's "mechanism-1 is
terminal-depth mechanism-3" reading: parameters bottom out at
the substrate's terminal depth, and what the framework
contributes is the *recognition* that the same form governs
mechanism-1 contexts, not a derivation of their specific values.

**(L5) Projection-class assignment is currently identified by
inspection.** The rich-state vs. chunked-state vs.
recognition-state sub-classes of P_3 are identified by
inspection of typical h_task values across substrates rather
than by direct empirical measurement of per-coordinatee state
dimensionality. A more rigorous treatment would measure h_task
across substrates and test whether substrates with measurably
lower h_task cluster at correspondingly higher k_max.

### 9.3 Future work

**(F1) Rigorous categorical formalization of projection class.**
Section 5 introduces projection class as a *taxonomy* based on
typed-neighborhood structure and treats the scaling-regime
invariance informally. A future-work track would specify a
functorial mapping between substrate-categories that makes
"shared projection class across substrates" a rigorous categorical
equivalence rather than an empirical observation. The structural
argument of Section 5.4 establishes the *form* of the bound and
the universality argument for the band; a categorical
formalization would tighten the equivalence relation underlying
substrate invariance. Typed-edge knowledge-graph representations
of software systems instantiate the projection-functor structure
operationally; the categorical-formalization track would
generalize the underlying structure across substrates beyond
software.

**(F2) Empirical sub-classification of P_3 by per-coordinatee
state dimensionality.** Section 5.3 sub-divides P_3 into rich,
chunked, and recognition with class-typical ceilings 4–10,
10–30, and 100–500 respectively. The sub-classification is
currently identified by inspection. A follow-up empirical track
would *measure* per-coordinatee state dimensionality directly
across substrates — embedding dimensionality of typical
sub-agent state in production multi-agent systems;
representational dim of stored relationship state in cognitive
psychology paradigms; information content of an ATC controller's
per-aircraft mental model — and test whether substrates with
measurably lower h_task cluster at correspondingly higher k_max.

**(F3) Per-direction operationalization across the cross-mechanism
table.** The per-direction multi-channel form (1′) is invoked in
Sections 4 and 7 where it produces structurally distinct
predictions, but Section 8's table reports a single (c, σ, φ)
triple per row. A more systematic treatment would identify
forward and reverse channels for every coordination context in
the table and report per-direction triples (c_d, σ_d, φ_d),
with the binding-direction analysis made explicit per row. This
is expected to yield additional architectural prescriptions in
domains where interface asymmetries are load-bearing (software
with side effects; biological signaling with retrograde feedback;
market microstructure where order-flow and price-discovery have
asymmetric formality).

**(F4) Cross-depth empirical case studies.** The propagation form
(5) and the candidate-set construction (Section 6.7) admit
empirical case studies: predict missing-tier parameters from
neighboring-tier anchors and test against observation.
Candidates: multi-agent intermediate-depth specialization (LLM
agent clusters at depths between single-agent and team-of-teams);
cell-type gap-prediction (single-cell omics; predicting
unobserved-but-stable cell-type configurations); cortical-area
variant stability (predicting which canonical-microcircuit
variants are stable from neighboring-area anchors).

**(F5) Operationalization of B and c for macro regimes.**
Construction of a composite central-bank-capacity index combining
reserves, analytical throughput, market microstructure maturity,
and political / credibility capital. Substantial methodology work
that would permit quantitative evaluation of monetary-regime
predictions over historical episodes (1990–2025) by comparing
realized regime stability against framework-predicted bounds.

**(F6) Extension to other coordination domains.** Biological
signaling cascades (mechanism-1, possibly with φ-variation
across receptor-class formality); market microstructure
(mechanism-2 protocols at the engine layer; mechanism-3
participant coordination at the trader-network layer);
social-network coordination dynamics (mechanism-3 with B-extension
via algorithmic curation). Each is a candidate for testing the
framework's reach beyond the present anchors.

---

## 10. Conclusion

The capacity-allocation bound k_max = B / [(1−φ)c + φσ]
generalizes to a structured framework: a three-mechanism taxonomy
distinguishing scaling regimes by where φ sits; a projection-class
taxonomy sub-dividing mechanism-3 by per-coordinatee state
dimensionality and giving substrate-invariant ceilings; a
per-direction multi-channel generalization licensing asymmetric
formalization without a half-formalization penalty; a cross-depth
propagation form coupling the bound at one depth to the bound at
the next depth down through the locus tower; an architectural
lever that raises φ to replace c with σ; and a 19-row cross-
mechanism table demonstrating the framework's reach across
chemistry, biology, neural systems, cognition, software,
distributed systems, multi-agent AI, organizational management,
macro policy, and modern ML architectures.

The framework's empirical core — a substrate-invariant ceiling at
k̄ ≈ 7 ± 2 across working-memory-class coordinators with
rich-state coordinatees, with own-collected cross-architecture
probing evidence — is developed in a companion convergence paper.
This paper is for readers who want the unified structure.

The contribution is unification + structural argument for the
band + architectural lever + projection-class generalization +
cross-depth propagation form. It does not derive within-band
values, does not improve crisis-timing forecasts beyond
reserve-adequacy literature, does not produce novel neuroscience
or distributed-systems theory, and does not substitute for
domain-specific theory within any of its domains. Its value lies
in the unification and the structure of the framework.

---

## References

(See `references.bib`.)
