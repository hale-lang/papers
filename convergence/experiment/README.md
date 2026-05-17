# Encoding/Decoding Asymmetry Experiment

The pre-registered cross-architecture probing experiment supporting
Section 4 of the convergence paper.

## What this directory contains

- `PRE_REGISTRATION.md` — the registered predictions and evaluation
  rule, committed before data collection.
- `ADDENDUM_001.md` — pre-data operational change: dataset switch
  FLORES-200 → FLORES+, and the consequent reduction in
  examples-per-language.
- `ADDENDUM_002.md` — pre-data operational change: probe
  convergence fix (`StandardScaler` + `max_iter = 5000`).
- `ADDENDUM_003.md` — post-data interpretive disclosure: the
  registered 4.5.1 magnitude band [2, 4] was literature-anchored,
  not framework-derived. Equation (1′) admits symmetric per-direction
  costs as a special case; the registered band excluded it. The
  registered criteria are honored in evaluation; the framework's
  actual claim is wider than what was registered.
- `EVALUATION_REPORT.md` — auto-generated evaluation against the
  registered criteria. Aggregate verdict: FALSIFICATION (5/13
  sub-evaluations confirm) per the pre-registered aggregation
  rule. The underlying picture: 4.5.3 (concept-probe middle peak)
  confirms cleanly at 4/4 models; 4.5.1 is scope-bounded
  falsified; 4.5.4 is falsified at the operationalization (a
  single transformer block drives language identity to saturation
  and every subsequent layer preserves it — there is no middle
  dip); 4.5.2 is degenerate (spread = 0.00 because all four
  ratios collapsed to ≈ 1).

## What's staged here vs. what to re-download

This directory contains the full reproducible artifact except
for the heavy caches:

**Staged:**
- `PRE_REGISTRATION.md`, `ADDENDUM_001.md`, `_002.md`, `_003.md`,
  `EVALUATION_REPORT.md` — the auditable trail.
- `experiment_source_README.md` — the experiment's
  source-side README (preserved for context).
- `src/` — extraction, probing, and analysis scripts (15 numbered
  Python scripts, `01_*.py` through `14_effective_rank_m2.py`).
- `configs/` — probe configuration, model list, dataset splits.
- `data/processed/` — processed parquets and per-language
  splits.
- `results/` — per-model probe accuracy curves (`results/probes/`),
  plots (`results/plots/`: PR / NMI / probe-accuracy / effective-
  rank), all summary CSVs, and the follow-up reports
  (`CONCEPT_FOLLOWUP_REPORT.md`, `EFFECTIVE_RANK_M2_REPORT.md`,
  `OPTIMAL_K_REPORT.md`, etc.).
- `requirements.txt`, `requirements.lock.txt`, `run.sh`,
  `setup.sh` — reproduction harness.

**Not staged (regenerate locally):**
- `data/cache/` — downloaded raw FLORES+ and XNLI data (~110G).
  Re-download via `setup.sh install-python` + `run.sh --steps
  download`; the FLORES+ + XNLI URLs and licenses are in
  `configs/`.
- `results/activations/` — intermediate hidden-state extractions
  (~16G). Regenerate via `run.sh --steps extract` after
  re-downloading data.
- `venv/` — Python virtualenv. Recreate via `setup.sh
  install-python`.

## Pre-registration commit

`708f13fdc673edff3acf632fb14f46c66f7c0477`

The commit predates data collection. Modifications captured in
the three ADDENDA. The git history is the audit trail.

## Headline findings

| Sub-prediction | Outcome | Models confirming |
|---|---|---|
| 4.5.1 (registered ratio band [2, 4]) | FALSIFIED per registered criteria | 0/4 |
| 4.5.2 (cross-architecture spread ≤ 2) | DEGENERATE (spread = 0.00) | 4/4 trivially |
| 4.5.3 (concept-probe peak in [0.4, 0.7]) | CONFIRMED | 4/4 |
| 4.5.4 (qualitative three-phase shape in language probe) | FALSIFIED per registered criteria | 0/4 |

Substantive findings beyond the registered verdict:

1. A single transformer block drives hidden-state language
   identity from partial (0.37–0.48 raw embeddings) to
   near-perfect linear separability (≥ 0.96) across 4/4 models;
   every subsequent layer preserves it.
2. Concept-level (XNLI label) structure peaks in middle layers
   at normalized depth 0.41–0.61, 4/4 models.
3. Four orthogonal geometric measurements (probe accuracy
   uniformity, cluster NMI, participation ratio, effective rank
   at variance thresholds) all replicate 4/4 and converge on
   the same picture: language identity is uniformly recoverable
   from layer 1 onwards, but the middle's representational
   manifold spans many more roughly-orthogonal dimensions than
   the perimeter.

## Models

- Llama-3.2-3B
- Mistral-7B-v0.3
- Qwen2.5-7B
- Llama-3.1-8B

## Data

- FLORES+ dev sentences across six languages: eng, spa, zho, rus,
  arb, hin (~6K sentences total for the language probe).
- XNLI validation sentences for the concept probe (~12K).
