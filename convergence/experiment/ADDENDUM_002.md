# Addendum 002 — Probe Convergence Fix

This addendum documents a methodology fix applied to the
linear-probe training, prompted by `ConvergenceWarning` outputs
from sklearn LBFGS during the first probe-training pass.

**Status:** the fix corrects a methodology flaw (probes that
did not converge underestimate true probe accuracy); it does
not change the predictions, the falsification thresholds, or
the operational definitions of w_E and w_D.

## What was observed

During stage 03 (`03_train_probes.py`) of the first pipeline
run, sklearn emitted:

```
ConvergenceWarning: lbfgs failed to converge (status=1):
STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.
```

This warning indicates that the LBFGS optimizer hit the
`max_iter=1000` limit before reaching the optimum. When this
happens, sklearn returns the best parameters found at that
iteration — which means the reported test accuracy is *lower
than the converged probe accuracy* would be.

For our purposes: a layer's probe might appear below the
threshold τ_lang = 0.70 when, at convergence, it would be
above. This biases w_E and w_D measurements *downward* (we
under-count layers in each bundle).

## What was fixed

Two changes in `src/03_train_probes.py`:

1. **Standardize features** before fitting the probe. Fit a
   `sklearn.preprocessing.StandardScaler` on the training
   activations (zero mean, unit variance per feature), apply
   to both train and test. Standardization is a *linear
   transform* that does not change which classes are linearly
   separable; it dramatically improves LBFGS convergence speed
   and is standard practice in linear-probing interpretability
   work (e.g., Wendler et al. 2024; Belrose et al. 2023).

2. **Increase `max_iter` from 1000 to 5000.** Combined with
   standardization, this is sufficient for convergence on all
   layers we have inspected.

Also: the `multi_class='multinomial'` parameter was removed
from `configs/experiment.yaml`. It was deprecated in sklearn
1.5; the default behavior for >2-class targets is now
multinomial. Removing the parameter eliminates a
`FutureWarning` and matches sklearn's recommended usage.

## Pre-registration discipline note

Pre-registration committed to `max_iter=1000` and
`multi_class='multinomial'` exactly. This change is a
*methodology bug fix*, not a hyperparameter tune — the
pre-registered probe was not measuring what we said it would
measure (the converged linear separability of each layer's
representations). The fix is independent of the framework's
predictions; it would have been the right thing to do
regardless of which way the data trends.

The fix was applied *during* the first pipeline run before
the run completed. Probe CSVs from layers where the original
spec had already converged would be marginally affected (the
new probes have access to a slightly better-conditioned
optimization problem); probe CSVs from layers where LBFGS hit
the iteration limit are now revised upward toward their
converged values.

## Decision: re-run all probes

Because we cannot easily distinguish per-(model, layer)
which CSVs were affected by the convergence issue, the
decision is to **delete all existing probe CSVs and re-run
stage 03 from scratch**. Probe training is fast (~10 minutes
total across all four models); re-running is cheap. The
extracted activations themselves (stage 02) are unaffected
and are not regenerated.

Operationally:

```bash
rm -rf results/probes/
./run.sh --steps "03 04 05 06"
```

## What this change does *not* affect

- Pre-registered predictions 4.5.1, 4.5.2, 4.5.3, 4.5.4: unchanged.
- Falsification thresholds: unchanged.
- τ_lang = 0.70: unchanged.
- Operational definitions of w_E, w_D: unchanged.
- Datasets, models, languages, examples-per-language:
  unchanged.

The auto-generated `EVALUATION_REPORT.md` records the
pre-registration commit hash and the activation-extraction
commit hash; this addendum's commit hash will appear in the
script's commit history adjacent to the probe-training
commits.
