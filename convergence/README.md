# Convergence Paper

*Capacity-Allocation Predicts a Coordination Ceiling at k ≈ 7 ± 2*

**Status:** v0 draft, 2026-05-16
**Length:** ~8 pp excluding references
**Target:** NeurIPS / ICLR / ICML workshop venues

## Contents

- `paper.md` — the paper
- `figures/` — generated figures (to be populated from experiment
  results; see `experiment/results/plots/`)
- `experiment/` — the pre-registered cross-architecture probing
  experiment artifact (pre-registration commit, ADDENDA, source,
  results, evaluation report)
- `references.bib` — BibTeX references

## Single claim

A simple capacity-allocation bound `k_max = B / [(1−φ)c + φσ]`
predicts a coordination ceiling at k̄ ∈ [4, 10] for
working-memory-class open-interface coordinators with rich-state
coordinatees. The ceiling is independently observed in
coordination-bound contexts spanning human working memory,
multi-agent LLM orchestration, cortical microcircuits,
span-of-control management, mixture-of-experts active experts,
decision-making groups, surgical OR teams, and Dunbar's intimate
ring. An own-collected pre-registered cross-architecture probing
experiment returns a mixed verdict: the concept-probe middle peak
prediction is confirmed in 4/4 open-weight LLMs; a
literature-anchored magnitude band for encoder/decoder width
asymmetry is scope-bounded falsified (the framework's actual
claim admits the observed symmetric configuration as a special
case); and a substantive structural finding about hidden-state
language preservation surfaces alongside.

## Falsifiable handles

- Pre-registered cross-architecture probing (commit `708f13f`):
  4/4 confirmation on concept-probe middle peak; scope-bounded
  falsification of a literature-anchored magnitude band that
  sharpens what the framework actually commits to.
- Predicted saturation in next-generation LLM orchestration at
  k ∈ [4, 12] even at frontier context windows (10M+ tokens).
- Forward content: any newly-discovered coordination context with
  rich-state coordinatees and open-interface coordination should
  saturate in the same band.
