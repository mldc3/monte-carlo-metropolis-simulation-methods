# Monte Carlo and Metropolis Methods in Computational Physics

This repository contains a compact scientific-computing portfolio project based on final-year Physics coursework in numerical modelling. It focuses on Monte Carlo integration, high-dimensional volume estimation and Metropolis Monte Carlo sampling in statistical mechanics.

The project is intentionally educational but written as a reproducible Python repository: the code includes deterministic random seeds, reference values, error diagnostics and saved figures. It complements my molecular-dynamics repository on FCC copper, where I use Lennard-Jones interactions, periodic boundary conditions and velocity-Verlet integration.

## Why this project is relevant

Many scientific-software workflows rely on the same basic structure:

1. define a physical model;
2. implement a numerical method;
3. validate against an analytical or trusted numerical reference;
4. analyse convergence, stability and systematic error;
5. document assumptions and limitations clearly.

This repository demonstrates that workflow using Monte Carlo methods. It is relevant for molecular simulation and scientific software because rejection sampling, Metropolis acceptance, Boltzmann factors, stochastic exploration and convergence diagnostics appear throughout computational physics, computational chemistry and biomolecular modelling.

## Contents

- `src/monte_carlo_methods.py`: rejection Monte Carlo integration and hypersphere-volume estimation.
- `src/metropolis_quantum_box.py`: Metropolis Monte Carlo sampling of a quantized ideal gas in a cubic box.
- `src/run_all.py`: regenerates all figures into `figures/`.
- `docs/theory.md`: detailed theoretical background.
- `docs/results_analysis.md`: detailed interpretation of the figures and numerical behaviour.
- `requirements.txt`: minimal Python dependencies.
- `raw/raw_course_*.py` and `raw/raw_course_report_*.pdf`: original coursework material kept for provenance.

## Methods implemented

### 1. Rejection Monte Carlo integration

The first part estimates the integral of a highly oscillatory function on `[0, 2]` by sampling random points in a bounding rectangle. The estimator is validated against `scipy.integrate.quad`. The figures show convergence with the number of samples, statistical error scaling and sensitivity to the chosen bounding maximum.

### 2. High-dimensional hypersphere volume

The second part estimates the volume of a unit hypersphere in dimensions 1 to 15. Points are sampled uniformly in the containing hypercube, and the estimator is compared with the exact expression involving the Gamma function.

### 3. Metropolis Monte Carlo

The third part simulates particles in a 3D cubic quantum box. Each particle is represented by quantum numbers `(nx, ny, nz)`, and trial changes are accepted according to the Metropolis rule. The simulation explores dependence on effective temperature `kT`, number of particles `N` and box length `L`.

## Generated figures

- `figures/figure_mc_integral_convergence.png`
- `figures/figure_mc_error_scaling.png`
- `figures/figure_mc_ymax_sensitivity.png`
- `figures/figure_mc_accept_reject.png`
- `figures/figure_hypersphere_volume_by_dimension.png`
- `figures/figure_hypersphere_relative_error.png`
- `figures/figure_metropolis_energy_base.png`
- `figures/figure_metropolis_temperature_dependence.png`
- `figures/figure_metropolis_particle_number_dependence.png`
- `figures/figure_metropolis_box_length_dependence.png`

## Installation and figure regeneration

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/run_all.py
```

This command regenerates all figures into `figures/` from the repository root.

## Skills demonstrated

- Python scientific programming
- NumPy, SciPy and matplotlib
- Monte Carlo integration
- Metropolis Monte Carlo
- stochastic numerical validation
- convergence and error analysis
- statistical-mechanics modelling
- documentation of scientific assumptions
- reproducible figure generation

## Related repository

For molecular dynamics with a more direct atomistic-simulation focus, see:

- <https://github.com/mldc3/Copper-molecular-dynamics-verlet>

That repository includes FCC copper, Lennard-Jones interactions, periodic boundary conditions, minimum-image convention, velocity-Verlet integration, thermodynamic diagnostics and radial-distribution analysis.
