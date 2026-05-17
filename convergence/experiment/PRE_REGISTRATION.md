# Pre-Registration: Encoding/Decoding Bundle-Width Asymmetry

This document commits to specific quantitative predictions
**before any data is collected**. It is committed to git prior
to running `src/01_download_data.py`. The git commit hash of
this file (at the time data collection begins) is recorded in
`results/EVALUATION_REPORT.md` automatically.

**Date authored:** 2026-04-30
**Author:** Riley Rook (rileyrook@gmail.com)
**Paper context:** Section 4 of the convergence paper
(`../paper.md`). Sub-prediction labels in this document
(4.5.1–4.5.4) are the stable identifiers carried through the
paper; they predate the section-numbering used in `paper.md`
and are referenced verbatim there.

## The framework's prediction (qualitative)

The capacity-allocation framework predicts that in
autoregressive decoder-only transformer LLMs handling typical
complex-input / constrained-output tasks (question-answering,
classification, summarization, generation):

- Encoding-side per-format cost c_f (input parsing under
  ambiguity) is intrinsically larger than decoding-side
  per-format cost c_r (conditional generation under accumulated
  context).
- The mechanism-3 capacity-allocation bound applied per channel
  yields encoding-bundle width w_E ≈ B / c_f and decoding-
  bundle width w_D ≈ B / c_r.
- Therefore w_E / w_D ≈ c_f / c_r, which the framework
  predicts to fall in the range **[2, 4]** under typical task
  structure.

## Operational definitions

### Bundle widths

For each probed model, we operationalize:

- **w_E (encoding-bundle width)** = the number of contiguous
  early layers (starting from layer 0) for which a linear
  probe trained to predict input language identity from the
  per-layer hidden state achieves accuracy ≥ τ_lang on
  held-out test data.
- **w_D (decoding-bundle width)** = the number of contiguous
  late layers (ending at the final layer) for which the same
  linear probe achieves accuracy ≥ τ_lang.

Where:

- **τ_lang** (language-identity threshold): set at 0.70 for the
  6-class language identification task. (Random baseline is
  0.167; a probe achieving ≥ 0.70 indicates the layer carries
  substantial language-specific information.)
- **Contiguity tolerance:** at most one layer below threshold
  is permitted within the contiguous region (allowing for
  per-layer probe noise without breaking the bundle).
- **Probe threshold τ_lang and contiguity tolerance are fixed
  here and not tuned after data collection.**

### Probe methodology

- **Architecture:** scikit-learn `LogisticRegression` with
  `solver='lbfgs'`, `max_iter=1000`, `C=1.0`,
  `multi_class='multinomial'`.
- **Input features:** per-layer hidden state at the *last token
  position* of each input sentence, dimensionality equal to
  model's `hidden_size`.
- **Train/test split:** 80/20 with random seed 42.
- **No hyperparameter tuning** of the probe itself (single
  configuration locked in at pre-registration time).

### Probe data

- **Source dataset:** FLORES-200 dev split (Costa-jussà et al.
  2022; HuggingFace `Muennighoff/flores200`, revision pinned
  in `configs/experiment.yaml`).
- **Languages:** English (eng_Latn), Spanish (spa_Latn),
  Mandarin Chinese (zho_Hans), Russian (rus_Cyrl), Arabic
  (arb_Arab), Hindi (hin_Deva). Six languages from six
  language families with diverse scripts.
- **Examples:** 1012 dev sentences × 6 languages = 6072
  sentences total. 4858 train / 1214 test after 80/20 split.
- **Tokenization:** each model's native tokenizer. Sequences
  truncated to 512 tokens (FLORES sentences are typically
  20–40 tokens; truncation should rarely apply).

### Models

- Llama-3.2-3B (28 layers; HuggingFace revision pinned)
- Mistral-7B-v0.3 (32 layers; HuggingFace revision pinned)
- Qwen2.5-7B (28 layers; HuggingFace revision pinned)
- Llama-3.1-8B (32 layers; HuggingFace revision pinned)

All models are decoder-only autoregressive transformers in the
"complex-input / constrained-output" task family the
prediction targets.

## Pre-registered predictions

### Prediction 4.5.1 (within-model asymmetric ratio)

**Claim:** In each of the four probed models, w_E / w_D falls
within the range [2, 4].

**Falsification criteria:** If for any of the four probed
models, w_E / w_D < 1.5 or w_E / w_D > 5.5, the prediction is
falsified for that model. If w_E / w_D < 1.0 (i.e., decoding
bundle is wider than encoding bundle), the per-direction cost-
asymmetry argument is strongly falsified.

**Edge cases:**
- If w_D = 0 (no contiguous late high-language-probe region),
  the prediction is treated as trivially confirmed (asymmetry
  is extreme); flag in the report.
- If w_E = 0 (no contiguous early high-language-probe region),
  the prediction is falsified — the predicted encoding bundle
  is absent.

### Prediction 4.5.2 (cross-architecture invariance band)

**Claim:** Across the four probed models, the w_E / w_D ratio
clusters in a band of width ≤ 2 (i.e., max(w_E/w_D) −
min(w_E/w_D) ≤ 2 across the four models).

**Falsification criteria:** If the spread of w_E / w_D across
the four models exceeds 3, the cross-architecture invariance
prediction is falsified. The framework would need a more
fine-grained model-class-specific reading.

### Prediction 4.5.3 (concept-probe peaks in middle)

**Claim:** A separate semantic-concept probe (XNLI 3-class
NLI label prediction) achieves its peak accuracy in middle
layers, *not* in early or late layers — consistent with the
format-agnostic semantic manifold reported by Wendler 2024 and
Dumas 2024.

**Operational form:** Let layer_concept_peak be the layer index
where the concept probe achieves its highest test accuracy. The
prediction is:

- For models with N total layers, layer_concept_peak / N falls
  in [0.4, 0.7] (i.e., between 40% and 70% of the way through
  the model).

**Falsification criteria:** If layer_concept_peak / N < 0.3
(concept peak in early layers) or > 0.8 (concept peak at the
very end) for any model, this prediction is falsified for that
model.

### Prediction 4.5.4 (qualitative three-phase recurrence)

**Claim:** The three-phase pattern (early high-language-probe
→ middle low-language-probe → late high-language-probe) is
qualitatively visible in each of the four probed models'
language-identity probe accuracy curves.

**Operational form:** For each model, the language-identity
probe accuracy curve must satisfy:

- Maximum accuracy in the first third of layers ≥ 0.70.
- Minimum accuracy in the middle third of layers ≤ 0.50.
- Maximum accuracy in the last third of layers ≥ 0.50.

**Falsification criteria:** If any model fails to exhibit this
qualitative shape (e.g., monotonically increasing accuracy
through all layers; monotonically decreasing; flat), the
qualitative three-phase recurrence is falsified for that
model.

## What we are *not* pre-registering

We do not pre-register specific numerical values for w_E or w_D
in absolute terms (only the ratio). The framework predicts the
*ratio* substrate-invariantly (per the projection-class
formulation, developed in the framework paper §5); absolute
widths depend on substrate-specific layer counts and per-layer
probe noise.

*[Migration note: this document was authored under the source
paper's section numbering, which placed projection-class
material in Section 2.5. After the split, the projection-class
formulation lives in the framework paper §5; the convergence
paper §2.5 is "The conjecture" (a downstream statement of the
substrate-invariant ceiling that builds on the projection-class
formulation). The substantive cross-reference is to the
projection-class material, now in framework §5.]*

We do not pre-register predictions about:
- Concept-probe absolute accuracy values.
- Differences between model families (Llama vs Mistral vs
  Qwen) in w_E or w_D individually.
- Performance on tasks not described in this experiment.

## What confirmation vs falsification looks like

The four predictions yield 16 individual evaluations (4
predictions × 4 models). Possible outcomes:

- **Slam dunk:** all 16 evaluations confirm; ratio cleanly in
  [2, 4]; tight cross-architecture clustering; concept peaks
  in middle. Paper Section 4.5 stands as written; experiment
  is reported as a substantive forward-prediction confirmation.

- **Partial confirmation:** ≥ 12 of 16 evaluations confirm.
  The framework's per-direction asymmetry lands directionally
  but with model-specific exceptions. Paper Section 4.5 is
  revised to acknowledge the exceptions; the overall claim is
  preserved.

- **Mixed results:** 8–11 of 16 evaluations confirm. The
  framework's qualitative claim (asymmetric organization
  exists) holds; the specific ratio prediction does not
  generalize cleanly. Paper Section 4.5 is substantially
  rewritten.

- **Falsification:** < 8 of 16 evaluations confirm. The
  per-direction asymmetric ratio prediction does not survive
  contact with the data. Paper Section 4.5 is rewritten as a
  literature-evaluation section without the own-collected
  forward prediction; honest framing of the framework's
  limits.

## Pre-registration discipline commitments

- This file is committed to git **before** any data is
  downloaded or any model is loaded for probing.
- The commit hash of this file at the start of data collection
  is recorded in `results/EVALUATION_REPORT.md`.
- We do not modify this file after data collection begins. If
  we discover a flaw in operational definitions or methodology,
  we add an `addendum_<n>.md` file and document in the report
  that the original predictions were modified, including the
  reason.
- The evaluation report is generated automatically by
  `src/06_evaluate_predictions.py`; we do not hand-edit it.
- All four predictions are reported regardless of outcome.
  No selection of "favorable" predictions or post-hoc
  redefinition.

## Methodological note

Pre-registration is itself an empirical commitment, not a
guarantee of correctness. The framework's predictions could be
right for the wrong reasons, wrong for surmountable reasons, or
wrong for fundamental reasons. The experiment cannot
distinguish these alone — it can only test whether the
predictions match the data under the chosen operational
definitions. Multiple operational definitions could be defended
ex ante; we have committed to one specific set above. Other
researchers running similar experiments under different
definitions are welcome to find different results; that
divergence is a feature, not a bug.
