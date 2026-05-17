"""Run all simulations and regenerate all figures."""
from pathlib import Path

from monte_carlo_methods import main as run_monte_carlo
from metropolis_quantum_box import main as run_metropolis

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    figures_dir = repo_root / "figures"
    run_monte_carlo(str(figures_dir))
    run_metropolis(str(figures_dir))
    print(f"All figures regenerated in {figures_dir}.")
