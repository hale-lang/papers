# Addendum 001 — Operational Changes

Per the pre-registration discipline ("we do not modify
`PRE_REGISTRATION.md` after data collection begins; if we
discover a flaw in operational definitions or methodology, we
add an `addendum_<n>.md` file"), this file documents two
operational changes made *before* the language-identity probe
data was extracted, but *after* `PRE_REGISTRATION.md` was
committed.

**Status:** these changes do not modify the predictions
themselves (4.5.1, 4.5.2, 4.5.3, 4.5.4) or their
falsification thresholds. They adjust the operational data
source.

## Change 1: dataset source

**Pre-registration said:**
> Source dataset: FLORES-200 dev split (Costa-jussà et al.
> 2022; HuggingFace `Muennighoff/flores200`, revision pinned
> in `configs/experiment.yaml`).

**Operational change:** switched to
`openlanguagedata/flores_plus` (the official ongoing
maintenance fork by the OpenLanguageData group).

**Reason:** `Muennighoff/flores200` and `facebook/flores`
both distribute the dataset as Python script-loaders that
require `trust_remote_code=True` to execute arbitrary code on
the local machine. We declined this for safety and
reproducibility reasons. `openlanguagedata/flores_plus` is
distributed as parquet files (no script execution) and
contains the same FLORES dev set sentences with the addition
of community-contributed language additions (which we do not
use; we filter to the same 6 pre-registered languages).

**Impact on predictions:** none. The sentences for the 6
languages we use are the same FLORES sentences derived from
the original Costa-jussà et al. (2022) release.

## Change 2: examples per language

**Pre-registration said:**
> Examples: 1012 dev sentences × 6 languages = 6072 sentences
> total. 4858 train / 1214 test after 80/20 split.

**Operational change:** the FLORES+ dev split contains 997
sentences per language (rather than 1012). Total: 5982
sentences × 80/20 split = 4786 train / 1196 test.

**Reason:** FLORES+ inherited a slightly trimmed dev split
(removing some sentences that were flagged for quality issues
in the original release).

**Impact on predictions:** none. 997 sentences is well above
the threshold at which probe accuracy estimates stabilize for
6-class language identification (typically a few hundred
examples suffice). The threshold τ_lang = 0.70 is unchanged.

## Discipline trail

These changes were made between commit `708f13f`
(pre-registration commit) and the start of activation
extraction. The changes were committed to the repo:

- Dataset switch (`facebook/flores` → `openlanguagedata/flores_plus`)
  in commit dealing with FLORES+ filter mapping in
  `configs/experiment.yaml` and `src/01_download_data.py`.
- Examples-per-language adjustment was a *consequence* of the
  dataset switch, not a separate decision; FLORES+ ships with
  997 per language and we used what was available.

The threshold and falsification criteria remain as
pre-registered. The auto-generated `EVALUATION_REPORT.md`
will record the pre-registration commit hash (`708f13f`) and
the activation-extraction commit hash to make the trail
auditable.
