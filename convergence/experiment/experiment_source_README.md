# Experiment: Encoding/Decoding Bundle-Width Asymmetry

This experiment evaluates the paper's per-direction asymmetry
prediction (Section 4.5) against open-weights transformer LLMs
under a uniform probe criterion: linear probes on per-layer
hidden states for (a) language-identity and (b) abstract-concept
features, measuring the layers where each kind of probe
succeeds.

The framework predicts:

- **Encoding bundle width** w_E = layers from the start where
  language-identity probes succeed strongly.
- **Decoding bundle width** w_D = layers from the end where
  language-identity probes succeed strongly again.
- **Predicted ratio** w_E / w_D ≈ 2–4 for autoregressive
  decoder-only transformers handling typical complex-input /
  constrained-output tasks (the per-direction asymmetric
  prediction from Section 4.5 of the paper, derived from
  per-direction cost asymmetry between input parsing and
  output generation).

Pre-registered predictions are stated in
[`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) before any data is
collected. Do not modify after results are collected. Operational
adjustments made between pre-registration and data collection
are documented in numbered addenda
([`ADDENDUM_001.md`](ADDENDUM_001.md), etc.).

---

## Reproducibility

This experiment is designed to be reproducible from scratch on
a Pop!_OS 24.04 (Ubuntu Noble) system with an AMD GPU
supporting ROCm 6.4+. All package versions are pinned;
HuggingFace model and dataset revisions are pinned where
possible.

### Hardware requirements

- **Linux.** Tested on Pop!_OS 24.04 (Ubuntu Noble base).
- **AMD GPU** with ROCm 6.4+ support. Verified working on
  RDNA 4 / gfx1201 (Radeon RX 9070 XT, 16 GB VRAM); should
  also work on RDNA 2/3 (RX 6000/7000-series, Radeon Pro,
  Instinct).
- **VRAM** ≥ 14 GB recommended for the 7-8B-class models in
  bf16. Smaller cards can run the 3B-class model only.
- **System RAM** ≥ 24 GB recommended (Mistral-7B and
  Llama-3.1-8B in bf16 use ~8 GB during model load).
- **Disk** ≥ 60 GB free for model downloads, datasets, and
  per-layer activations.

### One-shot setup

```bash
cd experiments/encoding_decoding_asymmetry

# Install ROCm 6.4 (skip if already installed)
./setup.sh --install-rocm    # interactive; requires sudo; system-modifying

# Pop!_OS / Ubuntu may need this one-time prerequisite for the venv:
sudo apt install python3.12-venv

# After ROCm install, reboot, then:
./setup.sh --install-python  # creates ./venv/, installs pinned PyTorch ROCm 6.4

# Verify environment (no system changes)
./setup.sh --verify
```

If after `--install-rocm` you don't see `/opt/rocm/`, AMD's
installer may have only created the versioned directory
`/opt/rocm-6.4.0/`. Create the symlink manually:

```bash
sudo ln -s /opt/rocm-6.4.0 /opt/rocm
```

Then either source `~/.profile` to pick up the PATH addition,
or open a new terminal.

### Authentication

Before the first run, authenticate with HuggingFace:

```bash
source venv/bin/activate
huggingface-cli login   # paste a read-token; needs gated-repo permission
```

The Llama models (Llama-3.2-3B and Llama-3.1-8B) are gated.
You must accept the Meta license at
`huggingface.co/meta-llama/Llama-3.2-3B` and
`huggingface.co/meta-llama/Llama-3.1-8B` while logged in.
Approval typically takes a few minutes after acceptance.

### One-shot run

```bash
cd experiments/encoding_decoding_asymmetry
source venv/bin/activate

# Quick smoke test first — load smallest model, run one
# forward pass, confirm RDNA 4 kernels work end-to-end (~3 min):
./run.sh --smoke

# Full pipeline (~90-120 min on RX 9070 XT):
./run.sh
```

The pipeline is **resumable**: if interrupted, re-running
skips completed (model, probe) pairs. Activation extraction
is the long stage (~15-20 min per model × 4 models = ~60-80
min); probe training, plotting, and report generation
together take ~10 minutes.

The pipeline produces:
- `results/activations/` — per-layer hidden states per model
- `results/probes/` — trained linear probes per layer per task
- `results/widths.csv` — measured w_E and w_D per model
- `results/plots/` — publication-quality figures
- `results/EVALUATION_REPORT.md` — auto-generated report
  comparing measured widths to pre-registered predictions

---

## Pipeline

The pipeline is a sequence of numbered scripts in `src/`. Each
script is idempotent (skips if outputs exist). To re-run a
specific stage, delete the corresponding output directory.

### `src/00_verify_env.py`
Sanity-check that PyTorch sees the GPU, that all packages are
importable, that GPU memory is sufficient.

### `src/01_download_data.py`
Download FLORES-200 (parallel sentences across languages, used
for both language-identity and concept-identity probes) and
XNLI (cross-lingual NLI; secondary semantic-content probe
target). Save to `data/` with version pins.

### `src/02_extract_activations.py`
For each model in `configs/models.yaml`:
1. Load model with `output_hidden_states=True`.
2. For each probe sentence, run forward pass.
3. Save per-layer hidden states (last-token position) to
   `results/activations/<model_name>/`.

Memory-managed by streaming sentences one at a time and
quantizing models that don't fit in fp16.

### `src/03_train_probes.py`
For each model and each probe task:
1. Load activations.
2. Train sklearn `LogisticRegression` linear probe on each
   layer's activations against the target label.
3. Cross-validate; report per-layer accuracy.
4. Save probe accuracy curves to
   `results/probes/<model_name>/<task>.csv`.

### `src/04_compute_widths.py`
For each model:
1. Load language-identity probe accuracy curve.
2. Apply pre-registered threshold (e.g., accuracy > 0.7) to
   identify high-language-probe regions.
3. Identify the contiguous region from layer 0 (encoding bundle)
   and from layer N (decoding bundle).
4. Record w_E and w_D per model.
5. Compute w_E / w_D ratio.
6. Save to `results/widths.csv`.

### `src/05_plot.py`
Generate plots:
- Per-layer probe accuracy curves for each model (language vs
  concept probes overlaid).
- Cross-model w_E vs w_D scatter.
- w_E / w_D ratio histogram against pre-registered range [2, 4].

### `src/06_evaluate_predictions.py`
Auto-generate `results/EVALUATION_REPORT.md` summarizing:
- Each pre-registered sub-prediction (4.5.1, 4.5.2, 4.5.3,
  4.5.4) and whether the measured data confirms or falsifies it.
- Honest narrative: lands cleanly / lands with caveats /
  partial / falsified.

---

## Models probed

Selected for AMD-GPU + 16 GB VRAM compatibility, architectural
diversity, and matched scale. See `configs/models.yaml` for
exact revisions.

| Model | Layers | Hidden dim | Tokenizer | Why probe |
|---|---|---|---|---|
| Llama-3.2-3B | 28 | 3072 | Llama-3 (128K vocab) | Smallest model; tests small-model regime |
| Mistral-7B-v0.3 | 32 | 4096 | Mistral SentencePiece (32K vocab) | Different tokenizer family; similar depth |
| Qwen2.5-7B | 28 | 3584 | Qwen (152K multilingual vocab) | Strong multilingual; different family |
| Llama-3.1-8B | 32 | 4096 | Llama-3 (128K vocab) | Reference; comparable to Wendler 2024 / Dumas 2024 |

This 4-model set tests within-family scaling (Llama-3.2-3B vs
Llama-3.1-8B) and cross-family invariance (Llama vs Mistral
vs Qwen). All fit in 16 GB VRAM in bf16.

Mistral-7B-v0.3 ships a SentencePiece-based tokenizer; this
requires `sentencepiece` and `protobuf` at runtime, both
pinned in `requirements.txt`.

---

## Probe datasets

### Language-identity probe (target for w_E, w_D)

**Dataset:** FLORES+ dev split (`openlanguagedata/flores_plus`,
the parquet-based maintenance fork of Costa-jussà et al. 2022's
FLORES-200; see [`ADDENDUM_001.md`](ADDENDUM_001.md) for the
dataset-source change rationale).

**Subset for probing:** 6 languages with diverse families:
- English (Latin script)
- Spanish (Latin script)
- Mandarin Chinese (Han script)
- Russian (Cyrillic script)
- Modern Standard Arabic (Arabic script)
- Hindi (Devanagari script)

**Examples:** 997 dev sentences × 6 languages = 5982
sentences total. 80/20 train/test split with seed 42.

**Probe task:** Given the per-layer hidden state at the last
token of a sentence, predict which of the 6 languages the
sentence is in.

**Expected behavior:** Language identity should be highly
decodable in early layers (encoding bundle), drop in middle
layers (where representations become language-agnostic per
Wendler 2024 / Dumas 2024), and become decodable again in late
layers (decoding bundle, where the model commits to output
language).

### Concept-identity probe (control, for middle-layer peak)

**Dataset:** XNLI dev split (Conneau et al. 2018); each
example has premise + hypothesis + label
(entailment/neutral/contradiction).

**Subset for probing:** Same 6 languages; ~2K examples per
language.

**Probe task:** Given the per-layer hidden state, predict the
NLI label (3 classes: entailment, neutral, contradiction).

**Expected behavior:** Semantic content (NLI label) should be
maximally decodable in middle layers (the format-agnostic
reasoning manifold per Wendler 2024 et al.), with lower
decodability in early and late layers.

---

## Pre-registration

See [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) for the
specific quantitative predictions stated before data
collection.

Pre-registration is committed to git before
`02_extract_activations.py` is run; the commit hash of the
pre-registration is recorded in
`results/EVALUATION_REPORT.md` automatically.

---

## Honest scope

**What this experiment can show:**
- Quantitative w_E / w_D measurements per model under a
  uniform probe criterion.
- Cross-architecture comparison.
- Direct evaluation of Section 4.5 sub-predictions
  4.5.1–4.5.4.

**What this experiment cannot show:**
- Whether the asymmetry is *causal* (manipulating cost
  asymmetry to verify it shifts the ratio).
- Whether asymmetry persists for non-decoder-only
  architectures (would require encoder-decoder MT model
  experiments; cf. Section 4.5.3).
- Whether the κ·k² mutual-information argument from Section
  4.4 holds (would require multi-agent benchmark, not single-
  model probing).

The experiment converts Section 4.5 from "literature-
supported pre-registered claim" to "measured forward
prediction with own-collected data." It does not address every
prediction in the paper; it addresses the most evaluable
within-scope claim with the resources available.
