#!/usr/bin/env python3
"""Tiny pedagogical figure: k_max as a function of φ.

Shows how k_max = B / [(1−φ)c + φσ] transitions from the
open-interface limit B/c (small) to the formal-interface
limit B/σ (large) as φ moves from 0 to 1.

Output:
  results/plots/kmax_phi_curve.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
import numpy as np

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
PLOTS = EXPERIMENT_ROOT / "results" / "plots"


def kmax(B: float, c: float, sigma: float, phi: np.ndarray) -> np.ndarray:
    return B / ((1 - phi) * c + phi * sigma)


def main() -> None:
    matplotlib.rcParams.update({"font.size": 10})

    phi = np.linspace(0, 1, 200)

    # Pedagogical example values: B = 1000, c = 100, sigma = 10
    # gives k(φ=0) = 10, k(φ=1) = 100
    B, c, sigma = 1000.0, 100.0, 10.0

    k = kmax(B, c, sigma, phi)
    k_open = B / c
    k_formal = B / sigma

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(phi, k, color="#444", linewidth=2)

    # Mark endpoints
    ax.axhline(k_open, color="#d62728", linestyle="--", linewidth=1, alpha=0.6)
    ax.axhline(k_formal, color="#1f77b4", linestyle="--", linewidth=1, alpha=0.6)

    ax.text(0.02, k_open * 1.18, f"φ=0 (open):  k_max = B/c = {k_open:.0f}",
            color="#d62728", fontsize=9)
    ax.text(0.55, k_formal * 0.85, f"φ=1 (formal):  k_max = B/σ = {k_formal:.0f}",
            color="#1f77b4", fontsize=9)

    # Mark bimodality optima per Section 8.2 (the only stable φ values)
    ax.scatter([0, 1], [k_open, k_formal], s=80, color="#444", zorder=5,
               label="bimodality optima (φ=0 or φ=1; intermediate dominated when ι>0)")

    # Shade intermediate region as "dominated" per Section 8.2
    ax.axvspan(0.05, 0.95, color="#888", alpha=0.06)
    ax.text(0.5, k_formal * 0.5,
            "intermediate φ dominated\nby endpoints when ι > 0\n(Section 8.2)",
            ha="center", color="#666", fontsize=8.5, style="italic")

    ax.set_xlabel("interface formality φ")
    ax.set_ylabel("k_max")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(5, k_formal * 1.4)
    ax.set_yscale("log")
    ax.set_title(f"k_max = B / [(1−φ)c + φσ]    (B={int(B)}, c={int(c)}, σ={int(sigma)})")
    ax.legend(loc="lower right", fontsize=8.5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    PLOTS.mkdir(parents=True, exist_ok=True)
    out = PLOTS / "kmax_phi_curve.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"saved {out}")


if __name__ == "__main__":
    main()
