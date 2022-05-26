"""Use this script to obtain a set of hyperparameters from the set of samples provided with GWTC-3."""


from bilby.core.result import read_in_result
import numpy as np
import gwpopulation as gwpop


# read in all the hyperposterior samples
PP_path = '../GWTC-3-population-data/analyses/PowerLawPeak/o1o2o3_mass_c_iid_mag_iid_tilt_powerlaw_redshift_result.json'
PP_result = read_in_result(PP_path)
PP_hyperposterior_samples = PP_result.posterior.copy()

# define a random seed
np.random.seed(220222)

# select a pseudo-random set of hyperposteriors
PP_params = PP_hyperposterior_samples.iloc[np.random.randint(0, len(PP_hyperposterior_samples))].to_dict()

# use the conversion tool pointed out by Colm Talbot
PP_params = gwpop.conversions.convert_to_beta_parameters(PP_params, remove=False)[0]

# add in z_max
PP_params['z_max'] = 2.3