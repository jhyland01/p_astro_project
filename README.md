# P_astro Project

Exploring the effect of using the probability of astrophysical origin as a thresholding statistic on the expected rate of detections and their purity.

## Main Features

The scripts in this package are built to select a set of hyperposterior samples from the GWTC-3 data release and Gibbs sample posterior samples from this set of hyperposteriors.
The bilby package is then used to generate signal-to-noise ratios (SNRs) by injecting these event signals into a stationary noise background.
Using a simple parameterisation from a paper by Lynch et al. (citation needed), these SNRs are converted into False-alarm-rates (FARs).
To calculate the probability of astrophysical origin (P_astro) we need the true astrophysical event rate.
This is obtained by integrating over mass and spacetime volume from the power-law plus peak model fitted to GWTC-3 data (figure 10 of citation needed).

## Basic Usage

From the command line (or otherwise) run:
1. select_hyperposterior.py
2. gibbs_sample.py
3. generate_SNRs_FARs.py
4. event_rate.py (under construction as .ipynb)

## Dependencies

See requirements.txt for a full list of environment packages.
This does not include the packages required for using the mpl_utils.py which originates from the GWTC-3 data release and required packages in the LVK igwn environments.

## Future work

Predicted detection rates for future detectors (Advanced LIGO +/#, Einstein Telescope etc.)

## Contact information

Email: j.hyland.2@research.gla.ac.uk

## Citations

1. GWTC-3 catalog
2. GWTC-3 Population paper
3. Lynch et al.

to be updated