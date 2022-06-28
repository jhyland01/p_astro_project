[![CI](https://github.com/jhyland01/p_astro_project/actions/workflows/main.yaml/badge.svg)](https://github.com/jhyland01/p_astro_project/actions/workflows/main.yaml) 
[![codecov](https://codecov.io/gh/jhyland01/p_astro_project/branch/main/graph/badge.svg?token=L4NSGM7TN6)](https://codecov.io/gh/jhyland01/p_astro_project)
[![Documentation Status](https://readthedocs.org/projects/p-astro-project/badge/?version=latest)](https://p-astro-project.readthedocs.io/en/latest/?badge=latest)

# P<sub>astro</sub> Project

Exploring the effect of using the probability of astrophysical origin as a thresholding statistic on the expected rate of detections and their purity.

## Installation instructions

This project only needs installed as a package if you wish to run tests, the .py files can be run without any installation.
To install, clone the project and navigate to the root of the project directory and run:
```console
pip3 install .
``` 

## Main Features

The scripts in this package are built to select a set of hyperposterior samples from the GWTC-3 data release and Gibbs sample posterior samples from this set of hyperposteriors.
The bilby package is then used to generate signal-to-noise ratios (SNRs) by injecting these event signals into a stationary noise background.
Using a simple parameterisation from a paper by Lynch et al. [3], these SNRs are converted into False-alarm-rates (FARs).
To calculate the probability of astrophysical origin (P<sub>astro</sub>) we need the true astrophysical event rate.
This is obtained by integrating over mass and spacetime volume from the power-law plus peak model fitted to GWTC-3 data available from [GWOSC](https://www.gw-openscience.org/).

## Basic Usage

Follow the [link](analysis/README.md) for instructions on running the analysis.

## Dependencies

See `requirements.txt` for a full list of environment packages.
This does not include the packages required for using the mpl_utils.py which originates from the GWTC-3 data release and required packages in the LVK igwn environments.

## Documentation

Documentation can be found at [p-astro-project.readthedocs.io](https://p-astro-project.readthedocs.io/en/latest/index.html).

## Future work

Predicted detection rates for future detectors (Advanced LIGO +/#, Einstein Telescope etc.)

## Contact information

Email: j.hyland.2@research.gla.ac.uk

## Citations

1. The LIGO Scientific Collaboration, the Virgo Collaboration, the KAGRA Collaboration, R. Abbott,
T. D. Abbott, F. Acernese, K. Ackley, C. Adams, N. Adhikari, R. X. Adhikari, and et al.,
“GWTC-3: Compact Binary Coalescences Observed by LIGO and Virgo During the Second Part
of the Third Observing Run,” arXiv e-prints, p. [arXiv:2111.03606](https://arxiv.org/abs/2111.03606), Nov. 2021.

2. The LIGO Scientific Collaboration, the Virgo Collaboration, the KAGRA Collaboration, R. Abbott,
T. D. Abbott, F. Acernese, K. Ackley, C. Adams, N. Adhikari, R. X. Adhikari, and et al., “The
population of merging compact binaries inferred using gravitational waves through GWTC-3,”
arXiv e-prints, p. [arXiv:2111.03634](https://arxiv.org/abs/2111.03634), Nov. 2021.

3. R. Lynch, M. Coughlin, S. Vitale, C. W. Stubbs, and E. Katsavounidis, “Observational implications
of lowering the ligo-virgo alert threshold,” The Astrophysical Journal, vol. 861, no. 2, 2018. [arXiv:1803.02880](https://arxiv.org/abs/1803.02880).