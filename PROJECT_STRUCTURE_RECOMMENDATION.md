# Repository organization recommendation

The ZIP provided here is intentionally flat because it can be uploaded quickly. For a professional GitHub repository, I recommend reorganizing it as follows:

```text
monte-carlo-metropolis-simulation-methods/
  README.md
  requirements.txt
  LICENSE
  .gitignore
  src/
    monte_carlo_methods.py
    metropolis_quantum_box.py
    run_all.py
  docs/
    theory.md
    results_analysis.md
  figures/
    figure_mc_integral_convergence.png
    figure_mc_error_scaling.png
    figure_mc_ymax_sensitivity.png
    figure_mc_accept_reject.png
    figure_hypersphere_volume_by_dimension.png
    figure_hypersphere_relative_error.png
    figure_metropolis_energy_base.png
    figure_metropolis_temperature_dependence.png
    figure_metropolis_particle_number_dependence.png
    figure_metropolis_box_length_dependence.png
  raw/
    raw_course_monte_carlo_integration_original.py
    raw_course_hypersphere_original.py
    raw_course_metropolis_quantum_box_original.py
    raw_course_report_monte_carlo.pdf
    raw_course_report_metropolis.pdf
```

The application should primarily point to the clean `src/`, `docs/` and `figures/` material. The `raw/` files are only kept as provenance.
