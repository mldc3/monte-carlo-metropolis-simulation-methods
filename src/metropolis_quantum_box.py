"""
Metropolis Monte Carlo simulation of a quantized ideal gas in a cubic box.

The system contains N non-interacting particles in a 3D cubic box. Each particle
is described by quantum numbers (nx, ny, nz), and the Metropolis rule samples
changes in those quantum numbers according to a Boltzmann acceptance factor.

This is an educational statistical-mechanics project designed to illustrate:
- detailed balance and Metropolis acceptance,
- equilibration and thermal fluctuations,
- dependence on kT, particle number N and box size L.
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def particle_energy(n_vector: np.ndarray, h: float = 1.0, m: float = 1.0, L: float = 1.0) -> float:
    """Energy of one particle in a 3D infinite cubic well in reduced units."""
    n_vector = np.asarray(n_vector)
    return h * h * np.pi * np.pi * np.sum(n_vector * n_vector) / (2.0 * m * L * L)


def run_metropolis(
    n_particles: int = 50,
    kT: float = 10.0,
    box_length: float = 1.0,
    steps: int = 80000,
    seed: int = 0,
) -> tuple[np.ndarray, float]:
    """Run a Metropolis chain and return total-energy history and acceptance rate."""
    rng = np.random.default_rng(seed)
    quantum_numbers = np.ones((n_particles, 3), dtype=int)
    energy = float(np.sum([particle_energy(quantum_numbers[i], L=box_length) for i in range(n_particles)]))
    energy_history = np.empty(steps + 1)
    energy_history[0] = energy
    accepted = 0

    for step in range(1, steps + 1):
        particle = rng.integers(0, n_particles)
        direction = rng.integers(0, 3)
        proposed_change = int(rng.choice(np.array([-1, 1])))
        new_quantum_number = quantum_numbers[particle, direction] + proposed_change

        if new_quantum_number >= 1:
            old_energy = particle_energy(quantum_numbers[particle], L=box_length)
            proposal = quantum_numbers[particle].copy()
            proposal[direction] = new_quantum_number
            new_energy = particle_energy(proposal, L=box_length)
            delta_E = new_energy - old_energy

            if delta_E <= 0.0 or rng.random() < np.exp(-delta_E / kT):
                quantum_numbers[particle, direction] = new_quantum_number
                energy += delta_E
                accepted += 1

        energy_history[step] = energy

    return energy_history, accepted / steps


def main(output_dir: str = ".") -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    steps = 80000

    energy_base, acceptance = run_metropolis(50, 10.0, 1.0, steps, seed=1)
    plt.figure(figsize=(7.2, 4.6))
    plt.plot(energy_base, linewidth=0.8)
    plt.xlabel("Monte Carlo step")
    plt.ylabel("Total energy")
    plt.title("Metropolis MC: equilibration of a quantum gas in a cubic box")
    plt.grid(True, alpha=0.35)
    plt.tight_layout()
    plt.savefig(out / "figure_metropolis_energy_base.png", dpi=180, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7.2, 4.6))
    for idx, kT in enumerate([1, 10, 30, 50]):
        energy, _ = run_metropolis(50, kT, 1.0, steps, seed=10 + idx)
        plt.plot(energy, linewidth=0.8, label=f"kT={kT}")
    plt.xlabel("Monte Carlo step")
    plt.ylabel("Total energy")
    plt.title("Temperature dependence of Metropolis energy sampling")
    plt.grid(True, alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "figure_metropolis_temperature_dependence.png", dpi=180, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7.2, 4.6))
    for idx, n_particles in enumerate([3, 10, 50, 100]):
        energy, _ = run_metropolis(n_particles, 10.0, 1.0, steps, seed=20 + idx)
        plt.plot(energy, linewidth=0.8, label=f"N={n_particles}")
    plt.xlabel("Monte Carlo step")
    plt.ylabel("Total energy")
    plt.title("Particle-number dependence in Metropolis sampling")
    plt.grid(True, alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "figure_metropolis_particle_number_dependence.png", dpi=180, bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(7.2, 4.6))
    for idx, box_length in enumerate([1, 3, 5, 10]):
        energy, _ = run_metropolis(50, 10.0, box_length, steps, seed=30 + idx)
        plt.plot(energy, linewidth=0.8, label=f"L={box_length}")
    plt.xlabel("Monte Carlo step")
    plt.ylabel("Total energy")
    plt.title("Box-size dependence of quantized energy levels")
    plt.grid(True, alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "figure_metropolis_box_length_dependence.png", dpi=180, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
