# Results analysis

This document gives a detailed interpretation of the generated figures. The emphasis is not only on what the code produces, but also on why the behaviour is physically and numerically expected.

## 1. Rejection Monte Carlo integration

### Figure: `figure_mc_integral_convergence.png`

The convergence plot shows the Monte Carlo estimate of the integral as the number of samples increases. For small `N`, the estimator fluctuates strongly because each accepted or rejected point has a large statistical weight. As `N` grows, the estimate stabilizes around the reference value obtained with `scipy.integrate.quad`.

The function used in this example is highly oscillatory near the endpoints of the interval, so the problem is a good test of a stochastic method. The method does not need to resolve every oscillation deterministically; instead, it estimates the average area statistically. This is a useful conceptual point: Monte Carlo methods can be robust even when the function is not visually smooth, provided the sampling domain is correct and sufficiently many samples are used.

The reference integral for the generated run is approximately `1.451496`. The exact value is not hard-coded: it is computed numerically and used only as a benchmark.

### Figure: `figure_mc_error_scaling.png`

The error plot is shown on log-log axes and includes a reference `N^{-1/2}` trend. This is the expected scaling for a Monte Carlo estimator based on independent random samples. The curve is not perfectly monotonic because Monte Carlo error is itself random: adding more samples reduces the expected error, but a particular realization can still fluctuate up or down.

The main conclusion is that the error decreases statistically, not deterministically. This distinction matters in scientific computing. A deterministic method such as Simpson integration often gives smooth convergence as the grid is refined. A Monte Carlo method instead gives convergence in probability, so the correct diagnostic is the statistical envelope or scaling trend rather than monotonic decrease at every point.

### Figure: `figure_mc_ymax_sensitivity.png`

This plot compares the estimator for three bounding maxima: an underestimated bound, a safe bound and an oversized bound.

- If the maximum is underestimated, part of the function lies outside the sampling rectangle. The estimator is then biased and converges to the wrong value. Increasing `N` cannot fix this, because the missing region is never sampled.
- If the maximum is safe and close to the true maximum, the estimator is both valid and reasonably efficient.
- If the maximum is much larger than necessary, the estimator remains unbiased but becomes less efficient. The acceptance probability decreases, so more points are rejected and the variance increases.

This figure is important because it separates statistical error from systematic error. Monte Carlo noise can be reduced by increasing `N`, but a wrong sampling domain produces a systematic bias.

### Figure: `figure_mc_accept_reject.png`

The accept/reject scatter plot shows the geometric interpretation of rejection Monte Carlo. Points below the curve contribute to the accepted count, while points above the curve are rejected. The accepted fraction estimates the ratio between the area under the curve and the area of the bounding rectangle.

The plot also illustrates why the method can be inefficient: every rejected point still costs computation. In high-dimensional or sharply concentrated distributions, naive rejection sampling can become very inefficient, which motivates importance sampling and Markov Chain Monte Carlo methods.

## 2. Hypersphere volume estimation

### Figure: `figure_hypersphere_volume_by_dimension.png`

The volume of a unit hypersphere does not increase forever with dimension. It rises for low dimensions, reaches a maximum and then decreases. This is counterintuitive at first but follows directly from the exact expression involving the Gamma function.

The Monte Carlo estimator follows the exact curve well in low and moderate dimensions. However, agreement becomes more difficult in high dimensions because the volume of the hypersphere occupies a smaller and smaller fraction of the containing hypercube. In practice, this means that most sampled points fall outside the hypersphere.

### Figure: `figure_hypersphere_relative_error.png`

The relative error increases in the high-dimensional regime. This is not because the formula changes or because the implementation is wrong. It is a consequence of sampling efficiency. The estimator depends on the fraction of accepted points. When the true probability becomes small, the binomial noise in the accepted count becomes large relative to the signal.

This is a useful example of the curse of dimensionality. Monte Carlo methods avoid the exponential grid cost of deterministic quadrature, but naive uniform sampling can still become inefficient when the important region occupies a tiny fraction of the sampling domain.

## 3. Metropolis Monte Carlo for particles in a cubic quantum box

### Figure: `figure_metropolis_energy_base.png`

The base simulation starts with all particles in the lowest-energy state. The Metropolis updates then allow the system to explore excited states. The total energy rapidly leaves the initial value and fluctuates around a statistical equilibrium.

The fluctuations are not numerical error. They are the expected thermal fluctuations of a finite system sampled in a canonical-like way. The chain does not converge to a fixed energy; it samples a distribution of energies compatible with the chosen effective temperature.

### Figure: `figure_metropolis_temperature_dependence.png`

The temperature-dependence plot shows that higher `kT` leads to higher average energies and larger fluctuations. This follows directly from the Metropolis acceptance probability

```math
P_{accept} = e^{-\Delta E/kT}
```

for energetically uphill moves. At low `kT`, upward moves are strongly suppressed, so the system remains close to low-energy states. At high `kT`, many upward moves are accepted, so the chain explores higher quantum numbers and the energy increases.

### Figure: `figure_metropolis_particle_number_dependence.png`

Increasing the number of particles increases the total energy because the plotted observable is extensive. More particles means more degrees of freedom and more possible single-particle updates. The absolute fluctuations also grow with system size, although relative fluctuations are expected to become smoother for larger systems.

This distinction between extensive and intensive quantities is important. Total energy scales with `N`, while energy per particle would be the better quantity for comparing systems of different sizes.

### Figure: `figure_metropolis_box_length_dependence.png`

The energy levels scale as `1/L^2`. Therefore, increasing the box length compresses the energy spectrum and lowers the typical energy scale. The figure shows lower total energies for larger boxes, consistent with the analytical expression for a particle in a cubic box.

Larger `L` also makes energy differences between neighbouring quantum states smaller, which changes the acceptance behaviour. The model therefore connects a simple quantum-mechanical formula with a statistical sampling algorithm.

## 4. What the project demonstrates

This repository demonstrates several skills that are transferable to scientific software and molecular simulation:

- implementing stochastic algorithms from physical definitions;
- validating numerical output against reference calculations;
- distinguishing systematic bias from statistical noise;
- analysing convergence and estimator efficiency;
- interpreting energy fluctuations physically;
- connecting code, equations and plots in a reproducible workflow.

These are the same habits needed in larger simulation projects: careful modelling assumptions, explicit diagnostics, reproducibility and clear explanation of numerical limitations.
