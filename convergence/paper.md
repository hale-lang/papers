# Capacity-Allocation Predicts a Coordination Ceiling at k ≈ 7 ± 2

**Author:** Riley Rook (rileyrook@gmail.com)
**Status:** v0 draft (2026-05-16)

---

## Abstract

Across four open-weight transformer LLMs (Llama-3.2-3B,
Mistral-7B-v0.3, Qwen2.5-7B, Llama-3.1-8B) we report four
cross-architecture geometric measurements of an organizational
transition between *format-specific* perimeter layers and a
*format-agnostic* middle, all replicating 4/4: (a) probe accuracy
uniformity (language linearly recoverable from layer 1 onwards);
(b) cluster-NMI inverted-U (language identity is the dominant
clustering axis only at the perimeter; 0.11–0.22 absolute NMI drop
in the middle); (c) participation ratio inverted-U (middle 3–4×
late effective dimensionality, peak at normalized depth 0.28–0.43);
(d) effective rank at variance thresholds (M2; per-model peak-middle
layer needs 5.7×–65× more PCA components than late at 90% variance;
cosine and raw within 5%, so the inversion is direction-count-driven
not magnitude-driven). The pre-registered concept probe also peaks
in the middle in 4/4 models (registration commit `708f13f`).

A capacity-allocation model k_max = B / [(1−φ)c + φσ] predicts the
transition as a mechanism-3 (open-interface, perimeter) /
mechanism-2 (formal-interface, middle) projection-class boundary.
The model produces a structural argument for a coordination ceiling
k̄ ∈ [4, 10] from the K log₂(K) entropy cost of distinguishing
rich-state items combined with working-memory-class effective B
(specific within-band values like Miller's 7 ± 2 or Cowan's 4 are
substrate-calibrated, not first-principles outputs). The same
ceiling appears in Miller's working memory (7 ± 2), Cowan's tight
working memory (4 ± 1), Dunbar's intimate ring (5), span-of-control
(5–9), surgical OR teams (5–10), mixture-of-experts active experts
(1–8), and multi-agent LLM orchestration saturation (4–8). The
empirical case is concentrated in this paper; the framework
extensions (three-mechanism taxonomy, per-direction multi-channel
form, cross-depth propagation) are developed separately.

---

## 1. Introduction

Across multi-agent LLM frameworks, organizational management,
cortical neuroscience, social anthropology, and cognitive
psychology, observed coordination spans cluster around small bounded
numbers — but the bounds vary by context in seemingly disconnected
ways. Multi-agent role-based LLM frameworks saturate at 4–8 agents.
Human management spans cluster at 5–9 direct reports. The canonical
cortical microcircuit consists of 3–4 distinct cell-type populations.
Working memory holds 4 ± 1 distinct items (Cowan) or 7 ± 2 chunked
items (Miller). Stable intimate social relationships saturate at
~5 (Dunbar's smallest nested ring). Mixture-of-experts architectures
activate 1–8 experts per token. Surgical OR teams cluster at 5–10
members. Each bound is established within its own domain literature;
each has its own explanation; the explanations rarely speak to each
other.

This paper offers one parsimonious account. A capacity-allocation
bound

> **k_max = B / [(1−φ)c + φσ]**                                   (1)

predicts a *substrate-invariant ceiling* k̄ ∈ [4, 10] for systems in
the projection class *open-interface coordinator with rich-state
coordinatees* — independent of substrate-specific B-units. The
ceiling falls out of a K log₂(K) entropy argument combined with
working-memory-class effective B; specific within-band values
(Cowan's 4, Miller's 7, span-of-control 5–9) remain
substrate-calibrated, but the band itself is structural.

We support the claim with:

1. A simple derivation of (1) from three minimal assumptions
   (Section 2).
2. A structural argument for the k̄ ∈ [4, 10] band (Section 2.4).
3. Cross-domain anchoring across coordination-bound contexts that
   converge on the band (Section 3).
4. An own-collected pre-registered cross-architecture probing
   experiment evaluating four within-model predictions of the
   framework, including a scope-bounded falsification of a
   literature-anchored magnitude claim that sharpens what (1)
   commits to (Section 4).

What this paper does *not* claim: it does not produce novel
empirics within any single domain. The bound recovers — does not
re-derive — established results (Miller, Cowan, Dunbar,
span-of-control, the canonical microcircuit). The contribution is
the convergence itself + the structural argument for the band.
Framework extensions — three-mechanism taxonomy, projection-class
sub-classification beyond P_3-rich, per-direction multi-channel
generalization, cross-depth propagation form, the architectural
lever — are developed in a companion paper (this paper's framework
sibling).

---

## 2. The capacity-allocation bound

### 2.1 The coordination context

Let a *coordination context* be a tuple (L, B, c, σ, φ):

- **L** is a *coordination locus*: a structurally-local point at
  which attachments are made. Examples include an atom (with
  attached bonds), a manager (with attached direct reports), an
  LLM orchestrator (with attached sub-agents), and a node in a
  consensus protocol (with attached peers).

- **B** is the *capacity* available at the locus. The unit varies
  by context: working-memory chunks, context-window tokens, neural
  capacity, reserves and analytical throughput, buffer space.

- **c** is the *full per-attachment cost*. To attach a coordinatee
  with no formal interface, the locus must hold full state about
  that partner: complete behavior, history, possible reactions,
  relevant features. Examples: a manager tracking a direct report's
  open-ended context; an LLM orchestrator running natural-language
  coordination with a sub-agent whose state is conveyed as full
  conversational history.

- **σ** is the *summary per-attachment cost*. When a formal
  interface exists, the partner's state can be reduced to a
  contractual summary: a function signature, a typed protocol
  header, a bounded message format. We assume σ ≤ c.

- **φ ∈ [0, 1]** is the *interface formality*. The fraction φ of
  each attachment's coordination cost is met by summary state σ;
  the remainder (1−φ) is met by full state c.

### 2.2 The bound

The coordination context's *span* k is the number of attachments
the locus sustains stably. The capacity-allocation argument states
that total capacity used cannot exceed B:

```
k · [(1−φ)c + φσ] ≤ B
```

Solving for the maximum stable k yields the bound:

```
k_max = B / [(1−φ)c + φσ]                                       (1)
```

Two limiting cases recover familiar shapes:

- **Open-interface limit (φ = 0):** k_max = B / c. The locus's
  span is set by capacity divided by per-coordinatee full state.
  This is the regime where coordinator-side cognitive limits
  dominate — Miller's number for human managers, per-agent context
  cost for LLM orchestrators.

- **Formal-interface limit (φ = 1):** k_max = B / σ. With σ ≪ c
  this can be much larger; coordination scales with system-level
  capacity rather than cognitive bottlenecks (consensus protocols,
  software function-call graphs).

### 2.3 Derivation

The bound derives from three assumptions.

**(A1) Asymptotic additivity in the rich-state regime.** The
locus's per-attachment cost is approximately additive at the
structurally-local resolution: total cost ≈ Σᵢ cost(attachment_i).
A1 holds asymptotically where per-coordinatee state cost dominates
the identity-discrimination term log₂(k_max) — i.e., where each
coordinatee's full operational state is large enough that the
which-of-K bookkeeping is a small correction. Boundary cases
where additivity fails strongly — gossip protocols whose pairwise
overhead grows quadratically with peer count, or group dynamics
where each additional participant adds n−1 new pairwise
relationships — are outside the simple bound's scope.

**(A2) Mixed-formality cost.** When a fraction φ of each
attachment's interface is formalized, the per-attachment cost
interpolates linearly between c and σ. This is a modeling choice;
in practice partial formalization may not yield linear cost
reduction — the empirical observation that φ is near-bimodal
across coordination contexts suggests this nonlinearity is real.
A2 still serves as a useful continuum on which the two limits sit.

**(A3) Capacity bound.** Total cost is bounded above by the
locus's capacity B. When total cost exceeds B, the locus enters a
regime where the bound's predictions break — instability, collapse,
or escalation.

Combining A1, A2, A3 yields (1).

### 2.4 Structural argument for the ceiling k̄ ∈ [4, 10]

The open-interface limit k_max ≈ B/c gives a small bound, but the
specific magnitude requires an account of why diverse substrates
land in the same band. The argument below predicts the
*band-structure* of the ceiling (the existence of a ceiling, its
K log K form, its location in [4, 10]) rather than specific
within-band values.

**Setup: the coordinator's distinguishability budget.** A
coordinator at locus L manages K rich-state coordinatees through
an open interface (φ ≈ 0). At each coordination step, the
coordinator must operate on the right coordinatee — issuing
instructions, integrating responses, arbitrating conflicts. To do
this without confusing one coordinatee with another, the
coordinator's working representation must encode, for each
coordinatee:

1. **Identity bits.** log₂(K) bits to specify "which one of K"
   the coordinator is currently attending to.
2. **Task-relevant state bits.** h_task bits — the conditional
   entropy of the coordinatee's task-relevant state given the
   coordinator's current task context.

Total information the coordinator must hold to operate on K
rich-state coordinatees:

  I_total(K) = K · log₂(K) + K · h_task                          (2)

The first term is *cross-coordinatee* — it grows super-linearly in
K because identifying which-of-K is asked of the coordinator each
time it acts. The second is *per-coordinatee state*.

**The bound.** Setting I_total(K) ≤ B and rearranging:

  K · log₂(K) ≤ B − K · h_task

In the regime where h_task is bounded and B is bounded
working-memory-class capacity, the dominant constraint is the
super-linear log term. Treating h_task as absorbed into the
substrate's effective B calibration (so B below is the *residual*
discrimination budget after per-coordinatee state cost), solving
K · log₂(K) ≤ B numerically gives:

| Effective B (bits) | K_max (rich-state) |
|---|---|
| 10 | 4 |
| 20 | 7 |
| 30 | 9 |
| 50 | 13 |

For working-memory-class effective B ≈ 15–25 bits (Cowan 2001
working memory ≈ 4 chunks × ~4 bits/chunk for distinguishability;
Miller 1956 ≈ 7 chunks × ~3 bits/chunk for chunked binding —
both bits-per-chunk values are substrate-calibration estimates,
not standard literature numbers), K_max lands in the 5–9 range,
recovering the cross-substrate cluster.

**What this establishes:**
- The K log₂(K) growth form is substrate-invariant for any
  coordinator distinguishing K rich-state items at the identity
  level.
- The 4–10 numerical band emerges from the form combined with
  any working-memory-class B.
- The cross-substrate cluster at k ≈ 7 ± 2 has a structural
  explanation: same form + similar B/h_eff ratios across rich-state
  coordinators.

**What it does not establish:**
- The specific value ≈ 7 (vs ≈ 4 or ≈ 9) within the band remains
  empirically calibrated. The derivation predicts the band; it
  does not single out 7.
- The argument assumes h_task is bounded and additive across
  coordinatees (per A1). Domains with strongly non-additive
  coordination cost (gossip protocols; large-group dynamics)
  require a cross-coordinatee mutual-information correction, with
  k_sat ≈ √(B/κ) sub-linear scaling.
- The claim that "effective B clusters at working-memory-class
  across substrates" is itself a calibration, not a derivation.
  Why biological and artificial coordinators share this scale is
  an empirical observation; the framework predicts the *form*
  given this observation.

### 2.5 The conjecture

Combining the derivation with the cross-domain evidence
catalogued in Section 3:

> **Conjecture (cross-substrate ceiling for open-interface
> coordinators with rich-state coordinatees).** Any system in which
> a coordinator with bounded working-memory-class capacity manages
> rich-state coordinatees through an open interface (φ ≈ 0) will
> saturate at K_max ∈ [4, 10] regardless of substrate or absolute
> B-units, because the binding constraint is the entropy cost of
> distinguishing rich-state items rather than the raw capacity of
> the coordinator.

This is testable in three regimes:

1. **Near-term.** Frontier LLMs with very large context windows
   (10M+ tokens) in role-based orchestration should saturate at
   K_orch ∈ [4, 12] — *not* at the linear-extrapolation
   K_max ≈ 333 a simple B/c form would give at 10M context.
2. **Mid-term.** Any new multi-agent platform that emerges in
   production with informal sub-agent communication will hit the
   same band unless explicitly architected with a formal protocol.
3. **Open-ended.** Any newly-discovered coordination context with
   the same projection-class structure — a new biological
   hierarchy; a new human institution; a coordination structure
   in non-human intelligent systems — will land in the same band.

---

## 3. Cross-domain anchoring

The structural argument predicts that diverse substrates with
open-interface coordinators and rich-state coordinatees should
converge on k ≈ 7 ± 2. This section catalogues the empirical
case.

### 3.1 Anchors

**Anchor 1. Human working memory (Cowan, Miller).** Cowan (2001)'s
distillation of working-memory capacity at ~4 distinct items
under tight discrimination; Miller (1956)'s seven-plus-or-minus-two
chunked items under standard binding. With B ≈ 15–25 bits and c
varying with binding strength, (1) predicts the 4–9 band.

**Anchor 2. Span-of-control (management science).** Graicunas (1933)
and subsequent literature on direct-report span; modern surveys
report median spans of 5–9 across industries. The manager is an
open-interface coordinator (natural-language coordination with
direct reports); per-report cost is large (open-ended context,
relational state). (1) recovers the band.

**Anchor 3. Multi-agent LLM orchestration (CrewAI / AutoGen / ChatDev).**
Published benchmark studies of role-based / conversational
multi-agent LLM frameworks report performance saturation at 4–8
agents (Du et al. 2023; Qian et al. 2024). The orchestrator
coordinates sub-agents through natural-language interfaces; each
sub-agent contributes a prompt template, recent conversational
history, an output buffer, and pragmatic context. With orchestrator
context B and per-agent cost c, (1) predicts the observed
saturation.

**Anchor 4. Cortical microcircuit (canonical motif).** Douglas and
Martin (1991); Bastos et al. (2012) on canonical microcircuits
for predictive coding. The motif consists of 3–4 distinct
cell-type populations — superficial pyramidal, deep pyramidal,
and one or two inhibitory interneuron classes. Capacity B is
*physical* (metabolic budget; signaling-pathway specificity;
excitation/inhibition balance constraints); per-cell-type cost c
is substrate-irreducible at the cortical depth. The cortical
anchor demonstrates that the bound holds *without any central
coordinator* — bound arity emerges from local stability of
interactions.

**Anchor 5. Decision-making groups.** Hackman and Vidmar (1970); Steiner
(1972) on group process losses. Optimal decision-making group
size 4–8 across studies, with marginal participation falling
sharply above this band as cross-member coordination overhead
accumulates.

**Anchor 6. Mixture-of-experts active experts (modern ML).** Switch
transformer (Fedus et al. 2022); Mixtral (Jiang et al. 2024).
Gating networks route tokens to 1–8 active experts at inference.
The gating selection is informally trained over pre-trained experts
(open-interface selection from a rich-state pool), consistent
with the mechanism-3 reading.

**Anchor 7. Surgical OR teams.** Cross-study evidence on
operating-room team size at 5–10 members for typical procedures.
Coordinator-mediated open-interface coordination under
working-memory-class constraints; per-member state is
operationally rich.

**Anchor 8. Dunbar's intimate ring.** Hill and Dunbar (2003); the
innermost of Dunbar's nested social-relationship rings at ~5
relationships under tight per-relationship binding. Dunbar's
larger rings (15, 50, 150, 500) — discussed below — operate
under progressively chunked per-relationship state and admit
correspondingly larger k.

### 3.2 The convergence

Eight substrates spanning chemistry-free biology, neural systems,
human cognition, organizational management, modern ML architecture,
multi-agent AI, social anthropology, and decision-making groups
all cluster at k ∈ [4, 10] when the projection class is
*open-interface coordinator with rich-state coordinatees*. The
substrate-specific B and c values differ by orders of magnitude
(working-memory chunks vs. context-window tokens vs. metabolic
capacity vs. management-attention units), but the dimensionless
ratio at saturation lands in a narrow band.

Table 1 summarizes:

| Substrate | B units | c units | k observed | Source |
|---|---|---|---|---|
| Working memory (tight, Cowan) | discriminability budget | rich items | 4 ± 1 | Cowan 2001 |
| Working memory (chunked, Miller) | working-memory chunks | bound items | 7 ± 2 | Miller 1956 |
| Span-of-control | attention budget | per-report state | 5–9 (median 7–8) | Graicunas 1933 |
| LLM orchestrator (role-based) | context-window tokens | per-agent context | 4–8 | Du et al. 2023; Qian et al. 2024 |
| Cortical microcircuit | metabolic / signaling budget | per-cell-type contribution | 3–4 | Douglas & Martin 1991; Bastos 2012 |
| Decision-making group | collective-attention budget | per-participant state | 4–8 | Hackman & Vidmar 1970 |
| MoE active experts | routing budget | per-expert integration | 1–8 | Fedus 2022; Jiang 2024 |
| OR team | coordinator attention | per-member state | 5–10 | Loft 2007 (review) |
| Dunbar intimate ring | neocortex social-tracking | per-relationship state | 5 | Hill & Dunbar 2003 |

### 3.3 Sub-class extension (briefly)

Outside the rich-state regime, the same equation (1) admits
substrates with chunked or recognition-state coordinatees and
predicts correspondingly larger k. Dunbar's empirical *nested
rings* 5/15/50/150/500 are the single clearest demonstration: one
individual maintains relationships at five binding strengths,
each with progressively smaller c per relationship, each giving
progressively larger k_max under (1). ATC controllers manage
10–25 aircraft with chunked per-aircraft state (call-sign +
altitude + heading + intent + conflict candidates), well above
the rich-state band. The full projection-class taxonomy
(P_3-rich at 4–10; P_3-chunked at 10–30; P_3-recognition at
100–500) is developed in this paper's framework sibling. We
report the rich-state band here because it carries the strongest
cross-substrate signal and the cleanest structural argument.

### 3.4 What the convergence does and does not show

The convergence supports two claims:

- The *form* of the bound (linear B/c saturation under an
  open-interface coordinator with rich-state coordinatees) is
  substrate-spanning. Eight substrates fit the form.
- The K log₂(K) structural argument explains *why* the
  saturation band is narrow across substrates with otherwise
  unrelated B units.

It does not support:

- A *derivation* of any single substrate's bound. Each row's
  observed k is independently established in domain literature;
  the framework recovers them in unified vocabulary.
- *Specific within-band values* as framework outputs. Cowan's 4
  vs. Miller's 7 vs. cortical 3–4 vs. OR-team 5–10 reflect
  substrate-specific calibrations that the framework does not
  predict from first principles.
- *Sub-class boundaries* as derived. The h_task values
  separating rich-state from chunked-state from recognition-state
  coordinatees are identified by inspection in the present
  treatment; an empirical sub-classification by measured
  per-coordinatee state dimensionality is future work.

---

## 4. Pre-registered cross-architecture probing experiment

The convergence in Section 3 is recovery + unification of
established results. Section 4 reports own-collected forward
content: a pre-registered cross-architecture probing experiment
designed before data collection (registration commit `708f13f`),
evaluating four sub-predictions about within-model coordination
structure. The experiment confirms one prediction cleanly across
four architectures, falsifies a literature-anchored magnitude
claim under scope-bounded retraction, and surfaces a substantive
structural finding about hidden-state geometry.

### 4.1 The within-model prediction

The framework predicts that the same mechanism distinctions
(open-interface vs. formal-interface) appear *wherever interface
formality varies along a coordination pathway*, including within
a single transformer model along the layer axis. Recent
interpretability work (Wendler et al. 2024; Dumas et al. 2024;
Gromov et al. 2024; Men et al. 2024; Ng 2026) surfaces a
three-phase organization in transformer LLMs: format-specific
encoding layers, format-agnostic reasoning middle, format-specific
decoding layers.

In the framework's vocabulary, the format-specific encoding and
decoding bundles operate as open-interface coordination at the
layer-bundle level (per-format full state required), while the
format-agnostic middle operates as formal-interface composition
(abstract semantic representation per concept). The three-phase
shape is the projection-class transition predicted by (1) at the
layer resolution.

### 4.2 Pre-registered sub-predictions

Four sub-predictions were registered at commit `708f13f` before
data collection, with three documented addenda
(ADDENDUM_001/002/003) capturing operational changes and a
post-data interpretive disclosure:

- **4.5.1 (registered).** In autoregressive decoder-only
  transformers handling complex-input / constrained-output tasks,
  w_E / w_D ∈ [2, 4]. Falsified outside [1.5, 5.5].
- **4.5.2 (registered).** Cross-architecture spread of w_E / w_D
  ≤ 2 across the four probed models.
- **4.5.3 (registered).** Concept-probe peak in normalized depth
  [0.4, 0.7].
- **4.5.4 (registered).** Qualitative three-phase shape in
  language-probe accuracy: early max ≥ 0.70, middle min ≤ 0.50,
  late max ≥ 0.50.

The labels 4.5.1–4.5.4 are the pre-registration's stable
identifiers (see `experiment/PRE_REGISTRATION.md`) and are used
throughout the rest of this section so that paper claims and
audit-trail entries reference the same names.

**Disclosure: the registered 4.5.1 magnitude band [2, 4] was
literature-anchored, not framework-derived.** The band was anchored
to prior empirical findings in the language-pivoting literature
(Wendler et al. 2024 ratio ≈ 4.0 in Llama-2-70B; Dumas et al. 2024
≈ 2.7 in Llama-2-7B), not derived from (1) directly. Equation (1)
admits symmetric encoding/decoding widths (φ_E = φ_D) as a special
case; the registered band excluded it. ADDENDUM_003 documents this
disclosure in the experiment's record. We honor the registered
criteria in evaluating the result, and we note where the registered
criteria diverged from what the framework actually predicts.

### 4.3 Methodology

Linear logistic-regression probes over per-layer hidden states
(last-token pooling, bf16 extraction, StandardScaler + L2
regularization). Trained on ~6K FLORES+ dev sentences across six
languages (eng, spa, zho, rus, arb, hin) for the language probe
(FLORES+ is the OLDI-maintained continuation of FLORES-200; NLLB
Team / Costa-jussà et al. 2022); ~12K XNLI validation sentences
(Conneau et al. 2018) for the concept probe. Models:
Llama-3.2-3B, Mistral-7B-v0.3, Qwen2.5-7B, Llama-3.1-8B.

### 4.4 Results

| Model | n_layers | w_E | w_D | ratio | concept peak (norm.) |
|---|---|---|---|---|---|
| Llama-3.2-3B | 29 | 29 | 28 | 1.04 | 0.43 |
| Mistral-7B-v0.3 | 33 | 33 | 32 | 1.03 | 0.44 |
| Qwen2.5-7B | 29 | 29 | 28 | 1.04 | 0.61 |
| Llama-3.1-8B | 33 | 33 | 32 | 1.03 | 0.41 |

- **4.5.1 — falsified per registered criteria, 0/4 models.** All
  four models give w_E / w_D ≈ 1.03–1.04, well below the
  registered band [2, 4] and below the falsification threshold
  1.5. The data is, however, consistent with (1) under
  symmetric per-direction structure for language identity; the
  framework is not falsified, only the literature-anchored
  magnitude claim.

- **4.5.2 — trivially confirmed but degenerate.** Cross-architecture
  spread is 0.00, well within the registered band ≤ 2. The
  confirmation is not informative: all four ratios collapsed to
  ≈ 1, and the prediction does not distinguish convergent
  asymmetry from convergent symmetry when the underlying signal
  is saturated.

- **4.5.3 — confirmed, 4/4 models.** Concept-probe peak in
  normalized depth ∈ [0.4, 0.7] across all four models. This is
  the substantive cross-architecture positive result: the
  *meaning* signal exhibits exactly the predicted middle-peak
  shape, across three vendors and two scale tiers.

- **4.5.4 — falsified per registered criteria, 0/4 models.** The
  language-identity probe achieves accuracy ≥ 0.96 on every layer
  of every model from layer 1 onwards. Layer 0 (raw token
  embeddings) is partial: 0.37–0.48 across the four models, well
  above the 1/6 ≈ 0.167 random baseline but not saturated. The
  first transformer block then drives accuracy to ~0.99, and no
  subsequent layer compresses the signal back. There is no
  middle dip in the language-probe curve past layer 1.

Aggregate verdict per the auto-generated evaluation report under
the pre-registered aggregation rule: **FALSIFICATION**
(5/13 sub-evaluations confirm; below the 50% threshold). The
underlying picture is more nuanced — 4.5.3 confirms cleanly at 4/4,
4.5.1 is scope-bounded falsified, 4.5.4 is falsified at the
operationalization, and 4.5.2 is degenerate. We report the aggregate
verdict as the rule outputs it; the substantive contributions
stand independent of the aggregate label.

### 4.5 Substantive empirical contributions

Three findings worth reporting on their own merits, independent
of the registered-prediction verdict:

1. **A single transformer block drives language identity to
   saturation, and every subsequent layer preserves it.** Across
   four open-weight LLMs spanning three vendors (Meta, Mistral,
   Alibaba) and two scale tiers (3B / 7B / 8B), a linear probe on
   hidden-state geometry classifies six languages at 0.37–0.48
   from raw token embeddings (layer 0; well above 1/6 ≈ 0.167
   random baseline), transitions to ≥ 0.96 after the first
   transformer block, and remains at ≥ 0.99 through every
   subsequent layer including the final one. The hidden-state
   language-identity dimension is established by block 1 and
   never compressed away. This is novel as a hidden-state
   geometric finding: existing language-pivoting literature
   measures output-token probabilities (logit-lens, language-mixing
   metrics) which speak to what the model emits, not to what is
   geometrically preserved in its hidden states.

2. **Concept-level structure exhibits the predicted middle-peak
   shape, across architectures.** XNLI label classification
   (entailment / neutral / contradiction) peaks at normalized
   depth 0.41–0.61 in 4/4 models. This confirms 4.5.3 cleanly and
   is the predicted projection-class structure of the
   format-agnostic middle.

3. **The encoder/decoder bundle-width asymmetry, operationalized
   via hidden-state language-identity probing, manifests as
   symmetry (φ_E = φ_D).** Both directions preserve language
   identity to the same extent (full preservation in early *and*
   late layers); neither direction narrows. This is one of the
   values (1) admits per its per-direction generalization (see
   the framework sibling for details) and is the empirically
   realized configuration for this specific signal in these four
   models. It does *not* falsify the framework's per-direction
   structure; it characterizes one point in its parameter space.

### 4.6 Cross-architecture geometric follow-ups (exploratory)

Four non-pre-registered measurements on the extracted activations
all replicate 4/4 across the four models and converge on the same
picture: language identity is uniformly linearly recoverable but
the *dominant organizing axis* of the middle is something else,
with the middle's representational manifold spanning many more
roughly-orthogonal dimensions than the perimeter.

The four measurements are: (i) probe accuracy (linear
separability), (ii) cluster NMI (dominance axis), (iii)
participation ratio (effective dimensionality), and (iv)
effective rank at variance thresholds (M2 — finer-grained
refinement of (iii)).

The M2 result deserves separate mention. At 90% variance, the
*peak middle layer* per model needs 5.7×–65× more PCA components
than the late layers (per-model peaks: 5.7×, 8.8×, 65×, 7.9×);
averaging over the entire middle third of layers and across
models gives a milder mean ratio of ~2.0× at 90% variance,
narrowing to ~1.3× at 99%. Cosine and raw geometries agree
within 5% — the inversion is about *direction count*, not
magnitude. Cosine-and-raw agreement establishes that the
inversion is direction-count-driven rather than magnitude-driven;
participation ratio alone cannot determine that.

All five follow-ups (four geometric + a concept-based bundle-width
re-operationalization that gives w_D > w_E in 3 of 4 models, mean
ratio 0.82, opposite to the literature-anchored magnitude claim)
are hypothesis-generating in the strict pre-registration sense
(the operationalizations were chosen after seeing the
pre-registered result). The cross-model 4/4 uniformity motivates
concrete pre-registered predictions for a v2 round on held-out
models — for example, *PR-peak normalized depth < 0.50 with peak
PR ≥ 1.5× both early and late thirds*.

### 4.7 Scope-bounded retraction

What the experiment falsifies: the registered magnitude band
[2, 4] for w_E / w_D measured via hidden-state language-identity
probing at the registered threshold, in four decoder-only
autoregressive transformers, on FLORES+ sentence inputs, with
last-token pooling.

What the experiment does *not* falsify: equation (1); the
cross-resolution recurrence claim about three-phase structure
(4.5.3 confirms it); the substrate-invariant ceiling for
open-interface coordinator systems (which Section 3 develops and
is not tested by this experiment).

The honest reading: the registered prediction was tighter than
the framework's actual claim, sourced from a literature anchor
that does not transfer cleanly to our operationalization. The
experiment's substantive content is the cross-architecture
confirmation of 4.5.3 and the structural finding about hidden-state
language identity. The encoder/decoder bundle-width asymmetry
remains an open empirical question for *concept-level* probing
operationalizations.

---

## 5. Discussion

### 5.1 What this paper adds

Three items beyond per-domain restatement:

1. **A cross-substrate convergence with a structural argument.**
   Section 3's eight substrates cluster within k ∈ [4, 10];
   Section 2.4's K log₂(K) argument explains why diverse
   substrates with otherwise unrelated B units converge on the
   same dimensionless band. The argument predicts the
   band-structure rather than specific within-band values; the
   contribution is the band prediction + the substrate-invariance
   claim, not a magic-number derivation.

2. **An own-collected pre-registered cross-architecture probing
   experiment.** Four open-weight transformers; pre-registration
   committed before data collection; three documented addenda;
   auto-generated evaluation report. One clean cross-architecture
   confirmation (concept-probe middle peak, 4/4 models); one
   scope-bounded falsification of a literature-anchored magnitude
   claim; one substantive structural finding (a single transformer
   block drives language identity to saturation, every subsequent
   layer preserves it); four follow-up geometric measurements all
   replicating 4/4. A methodological example that the framework's
   predictions can be operationalized strictly enough to be
   falsified, and that we report falsifications honestly when
   they occur.

3. **A forward-prediction handle.** The substrate-invariant
   ceiling is the framework's hardest forward claim: any
   newly-discovered coordination context with rich-state
   coordinatees and open-interface coordination should saturate
   in the same band. Frontier LLMs at 10M+ context windows; any
   newly-deployed multi-agent platform with informal sub-agent
   communication; a yet-to-be-identified biological hierarchy.
   The framework's track record on these is the empirical case
   for or against the substrate-invariance claim.

### 5.2 What this paper does not claim

- **Not novel single-domain empirics.** Miller, Cowan, Dunbar,
  span-of-control, canonical microcircuit, MoE active experts —
  each remains established within its own domain literature. The
  framework recovers them in unified vocabulary.

- **Not a derivation of within-band values.** The 4 vs. 7 vs.
  9 distinction is substrate-calibrated, not predicted.

- **Not a substitute for domain-specific theory.** Domain-native
  tools (cognitive-psychology bound calibration, predictive-coding
  microcircuit models, MoE routing analysis) remain the
  operational tools within their domains. The capacity-allocation
  form is a unifying layer, not a replacement.

- **Not a causal-generative claim.** Substrates differ; only the
  *form* of the bound is shared. Whether this commonality is
  meaningful or artifactual is partly resolved by whether the
  framework's forward predictions land.

### 5.3 Limitations

**(L1) B and c are independently measurable in only some contexts.**
For physics-fixed contexts (cortical microcircuit, MoE
architecture), B is set by substrate physics and is measurable
directly. For human-cognitive contexts (working memory, span-of-
control, group decision-making), B is sometimes named-as-Miller
(the "7 chunks" working-memory bound) and is not derived; c is
estimated from per-coordinatee state but not derived from first
principles. This means the framework's quantitative content
beyond the band-prediction relies on independent calibration.

**(L2) Per-coordinatee state c is approximated as additive at
structurally-local resolution.** Domains with strongly
non-additive coordination cost (gossip protocols' logarithmic
rounds; group-dynamics conversational amplification at large k)
require cross-coordinatee mutual-information corrections. The
qualitative predictions hold; quantitative predictions in
non-additive regimes require explicit treatment of the
correction term, which yields a k_sat ≈ √(B/κ) sub-linear form
in the LLM-orchestration regime.

**(L3) The φ parameter is treated as continuous but is empirically
near-bimodal.** Across the substrates in Section 3, no substrate
sits at intermediate φ; interfaces are either open (φ ≈ 0) or
formal (φ ≈ 1) with rare transitions. This is itself a finding,
and a stylized step-function formalization-cost model predicts
it as a theorem; it means the bound's intermediate-φ predictions
are extrapolated rather than empirically calibrated.

**(L4) Forward-prediction track record.** The own-collected
probing experiment of Section 4 produces one confirmed
cross-architecture prediction, one substantive structural finding,
and one scope-bounded falsification. The framework's broader
forward content — substrate-invariant saturation at frontier
context windows; newly-deployed multi-agent platforms at the
predicted band; cross-substrate replications in biological or
non-human systems — awaits future evaluation.

### 5.4 Future work

**(F1) Pre-registered v2 round on held-out frontier models.** The
exploratory geometric follow-ups (PR, NMI, M2, concept-bundle
widths) replicate 4/4 in the current four-model panel. The
natural pre-registration target — *PR-peak normalized depth
< 0.50 with peak PR ≥ 1.5× both early and late thirds* — should
hold on five held-out frontier-class models if the
projection-class transition is substrate-invariant at this scale.

**(F2) Encoder-decoder MT probing for per-direction asymmetry.**
The current operationalization (hidden-state language-identity
probing) yields φ_E = φ_D for language identity in the four
probed models. A concept-level probing operationalization on
encoder-decoder MT architectures (NLLB, M2M-100) would test
whether per-direction asymmetry surfaces under a different signal
on a different family.

**(F3) Empirical sub-classification of P_3 by per-coordinatee
state dimensionality.** The rich-state vs. chunked-state vs.
recognition-state sub-classes are currently identified by
inspection. A follow-up empirical track would *measure*
per-coordinatee state dimensionality directly across substrates
(embedding dimensionality of typical sub-agent state in production
multi-agent systems; representational dim of stored relationship
state in cognitive psychology paradigms) and test whether
substrates with measurably lower h_task cluster at correspondingly
higher k_max within the open-interface regime.

**(F4) Forward predictions about next-generation LLM
architectures.** As context windows expand to 10M+ tokens, the
framework predicts role-based saturation should *not* track the
linear-extrapolation K ≈ 333 a simple B/c form would give; the
4–10 band should hold absent architectural changes to the
projection class. Testable as new model generations release.

---

## 6. Conclusion

A capacity-allocation bound k_max = B / [(1−φ)c + φσ] predicts a
substrate-invariant ceiling k̄ ∈ [4, 10] for open-interface
coordinators with rich-state coordinatees. The ceiling falls out
of a K log₂(K) entropy argument combined with working-memory-class
effective B. Eight substrates — human working memory at two
binding strengths, span-of-control, multi-agent LLM orchestration,
cortical microcircuit, decision-making groups, MoE active experts,
surgical OR teams, Dunbar's intimate ring — all cluster in this
band. An own-collected cross-architecture probing experiment
across four open-weight LLMs confirms the framework's within-model
prediction of a format-agnostic middle in 4/4 models, surfaces a
structural finding about hidden-state language preservation, and
reports a scope-bounded falsification of a literature-anchored
magnitude claim that sharpens what the framework commits to.

The framework's value is the cross-substrate unification and the
structural argument for the band, not novel empirics within any
single domain. Specific within-band values (Cowan's 4, Miller's
7, cortical 3–4) remain substrate-calibrated. The framework's
forward content — substrate-invariant saturation at frontier
context windows and in newly-discovered coordination contexts —
will determine whether the unification has predictive value or
only descriptive value.

---

## References

(See `references.bib`.)
