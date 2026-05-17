# Concept-Based Bundle Widths — Exploratory Follow-up

**STATUS: NON-PRE-REGISTERED EXPLORATORY ANALYSIS.**

This analysis is a hypothesis-generating follow-up to the
pre-registered evaluation in `EVALUATION_REPORT.md`. It
operationalizes w_E and w_D using the concept probe instead
of the language probe, motivated by the observation that
the language probe is saturated and the concept probe
exhibits the predicted middle-peak shape (4.5.3 confirmed,
4/4 models).

Pre-registration (commit `708f13f`) committed to
language-probe operationalization with τ_lang = 0.70. This
script is *not* part of that pre-registration. Quantitative
claims surfaced here are hypothesis-generating; confirming
any of them requires fresh pre-registration on a different
experimental run.

**Bundle definition:** concept-probe accuracy stays within
Δ = 0.1 of the empirical peak. w_E counts layers from
peak backward toward layer 0 (encoding bundle); w_D counts
layers from peak forward toward the final layer (decoding
bundle).

## Measured concept-based widths

| Model | n_layers | peak_layer | peak_acc | w_E (concept) | w_D (concept) | ratio |
|---|---|---|---|---|---|---|
| llama-3.2-3b | 29 | 12 | 0.802 | 6 | 9 | 0.67 |
| mistral-7b-v0.3 | 33 | 14 | 0.807 | 7 | 9 | 0.78 |
| qwen2.5-7b | 29 | 17 | 0.804 | 9 | 7 | 1.29 |
| llama-3.1-8b | 33 | 13 | 0.822 | 6 | 11 | 0.55 |

## Interpretation

The concept-based bundle widths capture the structural
region around the format-agnostic semantic middle — the
layers where concept information is held at near-peak
accuracy. w_E is the lead-in (concept structure forming);
w_D is the lead-out (concept structure being projected
back to format-specific representations).

This operationalization is consistent with the framework's
per-direction prediction in spirit but not in pre-registered
operational form: the bundle is now anchored to the *narrow*
interior signal (concept) rather than the *saturated*
perimeter signal (language identity). The cross-architecture
distribution of concept w_E / w_D ratios surfaces here as a
hypothesis worth pre-registering on a separate run.

## What this analysis does and does not establish

*Establishes:*
- The concept signal exhibits a structurally non-trivial
  shape across all four models, with measurable bundle
  widths around the peak.
- The concept-bundle widths are concrete numbers that
  could be the target of a future pre-registered prediction.

*Does not establish:*
- The framework's per-direction asymmetry prediction (1′)
  is **not confirmed** by this analysis. Confirmation
  requires a pre-registered prediction on a separate run.
- Non-pre-registered analyses are subject to garden-of-
  forking-paths concerns; we report this analysis once,
  honestly labeled, without iterating on the bundle
  definition until the numbers look favorable.

## Methodology pointers

- Pre-registered predictions: see `PRE_REGISTRATION.md`
  (committed at git hash `708f13f`).
- Pre-registered evaluation: `EVALUATION_REPORT.md`.
- Addenda: ADDENDUM_001 (pre-data dataset switch),
  ADDENDUM_002 (pre-data probe convergence fix),
  ADDENDUM_003 (post-data interpretive disclosure).
- Probe accuracy curves: `results/probes/<model>/`.

