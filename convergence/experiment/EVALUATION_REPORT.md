# Evaluation Report — Encoding/Decoding Asymmetry

**Generated:** 2026-05-01 01:04:29 UTC
**Pre-registration commit:** `708f13fdc673edff3acf632fb14f46c66f7c0477`
**Overall outcome:** **FALSIFICATION** (5/13 sub-evaluations confirm)

---

## Measured widths

| model_name      |   n_layers |   w_E |   w_D |   ratio |   concept_peak_layer |   concept_peak_layer_normalized | three_phase_qualitative   |
|:----------------|-----------:|------:|------:|--------:|---------------------:|--------------------------------:|:--------------------------|
| llama-3.2-3b    |         29 |    29 |    28 |    1.04 |                   12 |                            0.43 | False                     |
| mistral-7b-v0.3 |         33 |    33 |    32 |    1.03 |                   14 |                            0.44 | False                     |
| qwen2.5-7b      |         29 |    29 |    28 |    1.04 |                   17 |                            0.61 | False                     |
| llama-3.1-8b    |         33 |    33 |    32 |    1.03 |                   13 |                            0.41 | False                     |

## Prediction 4.5.1 — Within-model asymmetric ratio

**Outcome:** 0/4 models confirm (w_E/w_D ∈ [1.5, 5.5], with [2, 4] as the precise predicted range).

| Model | w_E | w_D | ratio | verdict |
|---|---|---|---|---|
| llama-3.2-3b | 29 | 28 | 1.04 | falsified (ratio < 1.5) |
| mistral-7b-v0.3 | 33 | 32 | 1.03 | falsified (ratio < 1.5) |
| qwen2.5-7b | 29 | 28 | 1.04 | falsified (ratio < 1.5) |
| llama-3.1-8b | 33 | 32 | 1.03 | falsified (ratio < 1.5) |

## Prediction 4.5.2 — Cross-architecture invariance band

**Outcome:** CONFIRMED (spread=0.00)
  - min ratio: 1.03
  - max ratio: 1.04
  - spread: 0.00 (predicted ≤ 2.0; falsify > 3.0)

## Prediction 4.5.3 — Concept peak in middle layers

**Outcome:** 4/4 models confirm (concept-probe peak in [0.4, 0.7] normalized depth).

| Model | peak (norm.) | verdict |
|---|---|---|
| llama-3.2-3b | 0.43 | CONFIRMED (peak at 0.43 of depth) |
| mistral-7b-v0.3 | 0.44 | CONFIRMED (peak at 0.44 of depth) |
| qwen2.5-7b | 0.61 | CONFIRMED (peak at 0.61 of depth) |
| llama-3.1-8b | 0.41 | CONFIRMED (peak at 0.41 of depth) |

## Prediction 4.5.4 — Qualitative three-phase recurrence

**Outcome:** 0/4 models confirm (early max ≥ 0.70, middle min ≤ 0.50, late max ≥ 0.50).

| Model | early_max | middle_min | late_max | verdict |
|---|---|---|---|---|
| llama-3.2-3b | 1.00 | 1.00 | 1.00 | FALSIFIED |
| mistral-7b-v0.3 | 1.00 | 1.00 | 1.00 | FALSIFIED |
| qwen2.5-7b | 1.00 | 1.00 | 1.00 | FALSIFIED |
| llama-3.1-8b | 1.00 | 0.99 | 1.00 | FALSIFIED |

---

## Summary by tier

- **Slam-dunk:** all 4 sub-predictions × 4 models confirm.
- **Partial confirmation:** ≥ 75% confirm.
- **Mixed:** 50–75% confirm.
- **Falsification:** < 50% confirm.

**This run:** 5/13 = 38% — **FALSIFICATION**

## Methodology pointers

- Pre-registered predictions: see `PRE_REGISTRATION.md` (committed at git hash `708f13fdc673edff3acf632fb14f46c66f7c0477`).
- Probe accuracy curves: `results/probes/<model>/`.
- Plots: `results/plots/`.
- Raw widths: `results/widths.csv`.