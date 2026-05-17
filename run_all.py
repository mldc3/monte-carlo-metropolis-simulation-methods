"""Run all simulations and regenerate all figures."""
from monte_carlo_methods import main as run_monte_carlo
from metropolis_quantum_box import main as run_metropolis

if __name__ == "__main__":
    run_monte_carlo(".")
    run_metropolis(".")
    print("All figures regenerated.")
