"""
Monte Carlo numerical methods for physics coursework.

This script contains two examples:
1. Rejection Monte Carlo integration of a highly oscillatory function.
2. Monte Carlo estimation of the volume of a d-dimensional hypersphere.

The code is intentionally explicit and reproducible. It is designed as a small
scientific-computing portfolio project: each estimator has a reference value,
plots are saved to disk, and the figures highlight convergence, error scaling
and estimator limitations.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, IntegrationWarning
import warnings
from scipy.special import gamma


@dataclass
class RejectionResult:
    estimate: float
    x: np.ndarray
    y: np.ndarray
    accepted: np.ndarray


def target_function(x: np.ndarray | float) -> np.ndarray | float:
    """Highly oscillatory benchmark function used in the coursework."""
    x_arr = np.asarray(x)
    x_safe = np.clip(x_arr, 1e-12, 2.0 - 1e-12)
    return np.sin(1.0 / (x_safe * (2.0 - x_safe))) ** 2


def rejection_integral(
    f: Callable[[np.ndarray], np.ndarray],
    a: float,
    b: float,
    ymax: float,
    n_samples: int,
    rng: np.random.Generator,
) -> RejectionResult:
    """Estimate int_a^b f(x) dx by rejection Monte Carlo."""
    x = rng.uniform(a, b, n_samples)
    y = rng.uniform(0.0, ymax, n_samples)
    accepted = y <= f(x)
    estimate = (b - a) * ymax * accepted.mean()
    return RejectionResult(estimate, x, y, accepted)


def hypersphere_volume_mc(dim: int, radius: float, n_samples: int, rng: np.random.Generator) -> float:
    """Estimate the volume of a d-ball by sampling the containing hypercube."""
    points = rng.uniform(-radius, radius, size=(n_samples, dim))
    inside = np.sum(points * points, axis=1) <= radius * radius
    return (2.0 * radius) ** dim * inside.mean()


def hypersphere_volume_exact(dim: int, radius: float) -> float:
    """Analytical volume of a d-dimensional ball of radius R."""
    return (np.pi ** (dim / 2.0) / gamma(dim / 2.0 + 1.0)) * radius ** dim


def main(output_dir: str = ".", seed: int = 2026) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    a, b = 0.0, 2.0
    x_grid = np.linspace(0.001, 1.999, 2000)
    y_grid = target_function(x_grid)
    ymax = float(y_grid.max() * 1.01)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", IntegrationWarning)
        reference, _ = quad(lambda z: float(target_function(z)), a, b, limit=300)

    n_values = np.unique(np.logspace(2, 4, 90, dtype=int))
    estimates = []
    errors = []
    for n in n_values:
        result = rejection_integral(target_function, a, b, ymax, int(n), rng)
        estimates.append(result.estimate)
        errors.append(abs(result.estimate - reference))

    estimates = np.asarray(estimates)
    errors = np.asarray(errors)

    plt.figure(figsize=(7.2, 4.6))
    plt.plot(n_values, estimates, marker="o", markersize=2.4, linewidth=1.0, label="Monte Carlo estimate")
    plt.axhline(reference, linestyle="--", linewidth=1.2, label=f"quad reference = {reference:.5f}")
    plt.xscale("log")
    plt.xlabel("Number of samples N")
    plt.ylabel("Integral estimate")
    plt.title("Monte Carlo rejection integration: convergence with N")
    plt.grid(True, alpha=0.35, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "figure_mc_integral_convergence.png", dpi=180, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7.2, 4.6))
    plt.plot(n_values, errors, marker="o", markersize=2.4, linewidth=1.0, label="absolute error")
    ref = errors[10] * np.sqrt(n_values[10] / n_values)
    plt.plot(n_values, ref, linestyle="--", linewidth=1.2, label=r"reference $N^{-1/2}$")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Number of samples N")
    plt.ylabel("|I_MC - I_ref|")
    plt.title("Monte Carlo statistical error scaling")
    plt.grid(True, alpha=0.35, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "figure_mc_error_scaling.png", dpi=180, bbox_inches="tight")
    plt.close()

    # Hypersphere benchmark.
    dims = np.arange(1, 16)
    n_samples = 120000
    mc_volumes = np.array([hypersphere_volume_mc(int(d), 1.0, n_samples, rng) for d in dims])
    exact_volumes = np.array([hypersphere_volume_exact(int(d), 1.0) for d in dims])
    relative_errors = np.abs((mc_volumes - exact_volumes) / exact_volumes)

    plt.figure(figsize=(7.2, 4.6))
    plt.plot(dims, exact_volumes, marker="o", linewidth=1.2, label="exact")
    plt.plot(dims, mc_volumes, marker="s", linewidth=1.2, label="Monte Carlo")
    plt.xlabel("Dimension d")
    plt.ylabel("Volume of unit d-ball")
    plt.title("Volume of a unit hypersphere by dimension")
    plt.grid(True, alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "figure_hypersphere_volume_by_dimension.png", dpi=180, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7.2, 4.6))
    plt.plot(dims, relative_errors, marker="o", linewidth=1.2)
    plt.yscale("log")
    plt.xlabel("Dimension d")
    plt.ylabel("Relative error")
    plt.title("Relative error of the hypersphere Monte Carlo estimator")
    plt.grid(True, alpha=0.35, which="both")
    plt.tight_layout()
    plt.savefig(out / "figure_hypersphere_relative_error.png", dpi=180, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
