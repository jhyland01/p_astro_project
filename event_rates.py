"""
make_plpeak_mass_spectrum.py

Part of the data release: https://zenodo.org/record/5650062

Authors: Bruce Edelman on behalf of the LIGO Scientific Collaboration, Virgo Collaboration and KAGRA Collaboration

This software is provided under license: Creative Commons Attribution 4.0
International (https://creativecommons.org/licenses/by/4.0/legalcode) and  is provided as-is.

This script creates Figure 10 in the companion paper

JH: python make_plpeak_mass_spectrum.py ../analyses/PowerLawPeak/o1o2o3_mass_c_iid_mag_iid_tilt_powerlaw_redshift_mass_data.h5 output_name.png

"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_utils
import argparse
import json
import h5py
import gwpopulation

fig_width = mpl_utils.widths["textwidth"]

# cli_parser = argparse.ArgumentParser()
# cli_parser.add_argument('input_fname')
# cli_parser.add_argument('output_fname')
# cli_args = cli_parser.parse_args()

input_fname = '../GWTC-3-population-data/analyses/PowerLawPeak/o1o2o3_mass_c_iid_mag_iid_tilt_powerlaw_redshift_mass_data.h5'

color_plpeak = "#1f78b4"
# O3a_PPD = "o3a_population_data_release/Multiple-Fig-Data/mass_ppd/default/o1o2o3_mass_c_iid_mag_two_comp_iid_tilt_powerlaw_redshift_mass_data.h5"
O3a_PPD = '../GWTC-3-population-data/analyses/PowerLawPeak/o1o2o3_mass_c_iid_mag_iid_tilt_powerlaw_redshift_mass_data.h5'
O3_only_PPD = input_fname
O3_only_result = O3_only_PPD.replace("_mass_data.h5", "_result.json")

with open(O3_only_result, "r") as jfile:
    plpeak_jf = json.load(jfile)

posterior_samples_plpeak = plpeak_jf["posterior"]["content"]
peak_plp = posterior_samples_plpeak["mpp"]
peak_plp_05 = np.quantile(peak_plp, 0.05)
peak_plp_95 = np.quantile(peak_plp, 0.95)

mass_1 = np.linspace(2, 100, 1000)
mass_ratio = np.linspace(0.1, 1, 500)

fig, axs = plt.subplots(
    nrows=1, ncols=2, figsize=(2 * fig_width, (9.0 / 16) * fig_width)
)

with h5py.File(O3_only_PPD, "r") as f:
    mass_ppd = f["ppd"]
    mass_lines = f["lines"]
    mass_1_ppd = np.trapz(mass_ppd, mass_ratio, axis=0)
    mass_r_ppd = np.trapz(mass_ppd, mass_1, axis=-1)
    mass_1_lower = np.percentile(mass_lines["mass_1"], 5, axis=0)
    mass_1_upper = np.percentile(mass_lines["mass_1"], 95, axis=0)
    mass_r_lower = np.percentile(mass_lines["mass_ratio"], 5, axis=0)
    mass_r_upper = np.percentile(mass_lines["mass_ratio"], 95, axis=0)

# write a function for the distribution, or import from gwpopulation
import gwpopulation as gwpop
mmin = min(mass_1)
mmax = max(mass_1)
mass_model = Model([gwpop.models.mass.SinglePeakSmoothedMassDistribution(mmin = mmin, 
                                                                         mmax = mmax)])

# fit the function parameters to the curve above, or just select some median


# input the function and the upper and lower bounds into scipy.quad to integrate