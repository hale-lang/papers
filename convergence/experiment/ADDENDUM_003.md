# Addendum 003 — Pre-Registration Overshoot Disclosure

This addendum is filed *after* data collection and the
auto-generated `EVALUATION_REPORT.md`, to document a
methodological honesty issue discovered while interpreting
the run's results.

**Status:** the data, the operational definitions, and the
auto-generated evaluation are all unchanged. What this
addendum corrects is the *narrative claim* of what the
framework actually predicted versus what the pre-registration
committed to.

*[Migration note: this addendum was authored under the source
paper's notation (α for interface formality, "Section 2.2"
for the multi-channel form (1′)). After the split, the
interface-formality symbol is **φ** throughout both staged
papers, and the per-direction multi-channel form (1′) lives
in the framework paper §2.3. References below to "α_d / α_E /
α_D" should be read as "φ_d / φ_E / φ_D"; references to
"Section 2.2" point to framework §2.3. The substantive
content of this addendum — that (1′) admits φ_E = φ_D as a
special case and that the registered [2, 4] band was a
literature-anchored tightening — is unchanged.]*

## What was overshot

`PRE_REGISTRATION.md` (committed at hash `708f13f`) bound
Prediction 4.5.1 to:

> w_E / w_D ∈ [2, 4] under typical task structure (precise
> band [2, 4]; falsification at < 1.5 or > 5.5).

The framework's *actual* claim — the per-direction
multi-channel form (1′) of Section 2.2 — is:

  k_max = B / Σ_d [(1−α_d)c_d + α_d σ_d]

which says α_d may differ across directions; *it does not
predict any specific magnitude of asymmetry*. Setting
α_E = α_D collapses (1′) to bidirectional symmetry; nothing
in the framework rules this out.

The numerical band [2, 4] was anchored to **prior empirical
findings in the language-pivoting literature** (Wendler et al.
2024 reporting ratio ≈ 4.0 in Llama-2-70B; Dumas et al. 2024
reporting ≈ 2.7 in Llama-2-7B), not derived from (1′). At
pre-registration time we treated the literature anchor as
"framework + literature-supported" and committed it as a
single prediction. This conflated two distinct claims:

- (a) **Framework claim:** asymmetry between α_E and α_D is
  *possible*. (1′) admits any (α_E, α_D); a finding of
  α_E = α_D is one of the values it admits.
- (b) **Literature-anchored magnitude claim:** prior probing
  of language-pivoting effects in transformer LLMs has
  produced ratios in [2, 4]; we expected our operationalization
  to land similarly.

The pre-registration locked claim (b) as if it were a
prediction of (a). It is not.

## What the data shows

Across all four probed models (Llama-3.2-3B, Mistral-7B-v0.3,
Qwen2.5-7B, Llama-3.1-8B), the language-identity probe shows
the following pattern:

- **Layer 0 (raw token embeddings, before any transformer
  block):** accuracy 0.37–0.48 — well above 1/6 ≈ 0.167
  random baseline, but *not* saturated. This is consistent
  with disjoint token vocabularies across scripts (Hans, Cyrl,
  Arab, Deva use entirely different token IDs from Latin)
  partially identifying language even before any block runs.
- **Layer 1 (after the first transformer block):** accuracy
  0.96–0.998 — *fully saturated*. A single transformer block
  is sufficient to push language identity to near-perfect
  linear separability.
- **Layer 2 through final layer:** accuracy 0.99–1.00,
  preserved monotonically. No layer compresses the signal
  back below saturation.

Under the pre-registered operationalization (w_E = contiguous
early layers ≥ τ_lang = 0.70; w_D = contiguous late layers ≥
τ_lang), this gives w_E ≈ w_D ≈ n_layers in 4/4 models, ratio
≈ 1.03–1.04 — because layer 1 onwards meets the τ = 0.70
threshold trivially.

By the registered criteria, Prediction 4.5.1 is **falsified**
(0/4 models confirm). We honor the registered criteria; this
addendum does not change the verdict.

What it does change is the *interpretation*:

- **(1′) is not falsified.** The data is consistent with
  α_E = α_D for language identity in these models — a special
  case (1′) explicitly admits.
- **The literature-anchored magnitude claim is falsified.**
  Wendler/Dumas-style 2-4× ratios in language-pivoting probes
  do *not* replicate when the operationalization is hidden-
  state language-probe accuracy with τ = 0.70. This is itself
  a substantive null finding; the prior literature's
  measurements use different probe families (logit-lens,
  activation patching, phase-entropy) that capture different
  signals than ours.
- **The substantive empirical finding is structural, not
  parametric.** A single transformer block (block 1) drives
  language identity from partial-recoverability (~0.42 from
  raw embeddings) to near-perfect linear separability (~0.99),
  and *every subsequent layer preserves it* across four LLMs
  spanning three vendors and two scale tiers. There is no
  narrowing of this signal at any depth past layer 1, so no
  asymmetry of bundle widths can appear *for this signal*
  regardless of α_E and α_D. The bottleneck the framework
  predicts is on *meaning* (concept), not on surface-form
  identity (language).

## What this addendum changes in the paper

Section 4.5 is rewritten to:

1. Distinguish (1′)'s possibility claim from the
   literature-anchored magnitude claim. Acknowledge the
   pre-registration tightened beyond what the framework
   predicts.
2. Report Prediction 4.5.1 as **registered prediction
   falsified; framework-claim not falsified** — α_E = α_D for
   language identity is empirically realized and is admissible
   under (1′).
3. Report Prediction 4.5.2 as **trivially confirmed** but
   degenerate (spread = 0.00 because all four ratios collapsed
   to ≈ 1; the test cannot distinguish convergent asymmetry
   from convergent symmetry when the underlying signal is
   saturated).
4. Report Prediction 4.5.3 as **confirmed in 4/4 models** —
   concept-probe peak in normalized depth ∈ [0.4, 0.7]. This
   is the substantive cross-architecture positive result.
5. Report Prediction 4.5.4 as **falsified in 4/4 models** —
   downstream of the saturation; the language-probe curve
   shows no middle dip because the signal never compresses.
6. Lead with the substantive empirical contribution:
   **language identity is preserved at near-perfect linear
   separability through every transformer layer across four
   LLMs**, with concept-level structure adding on top in
   middle layers (per 4.5.3). This is a real, novel
   measurement and is reported on its own merits.

## Pre-registration discipline note

This addendum is filed *post-data*, which is later than
ADDENDUM_001 and ADDENDUM_002 (both pre-data methodology
fixes). Filing post-data raises a fair scrutiny question:
*is this addendum motivated reasoning to soften an
inconvenient result?*

Two reasons we believe it is not:

1. **The interpretive distinction was always present in
   (1′).** Section 2.2 of the paper writes (1′) as admitting
   different α_d per direction; nowhere does (1′) require
   non-zero asymmetry. The pre-registration's [2, 4] band
   was a separate tightening, sourced from prior literature.
   Re-reading (1′) without the literature anchor recovers
   the possibility claim cleanly.
2. **The verdict is unchanged.** The auto-generated
   `EVALUATION_REPORT.md` continues to report Prediction
   4.5.1 as falsified per the registered criteria. We are
   not relocating the threshold or redefining the metric;
   we are clarifying that the registered prediction was
   tighter than the framework actually predicts and reporting
   that gap honestly.

The honest summary for any reader of the paper:

> Prediction 4.5.1 was registered at a magnitude tighter than
> the framework's actual claim, anchored to prior literature
> on a related but distinct probe family. The data falsifies
> the registered band; the data does not falsify (1′). We
> disclose this explicitly rather than retrofitting either the
> registration or the framework.

## Auditability

- Pre-registration commit: `708f13f` (predates all data).
- ADDENDUM_001 (FLORES-200 → FLORES+) and ADDENDUM_002
  (probe convergence fix): pre-data methodology fixes.
- ADDENDUM_003 (this file): post-data interpretive disclosure.
  No change to the operational definitions or the verdict.
- `EVALUATION_REPORT.md` records the pre-registration commit
  hash and the auto-computed pass/fail per registered
  threshold.

The trail is auditable. A reader can reconstruct exactly
what was registered, what was measured, what passed, and
what we are claiming the framework actually predicts.
