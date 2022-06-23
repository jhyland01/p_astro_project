"""Use this script to obtain a set of hyperparameters from the set of samples provided with GWTC-3. This has been extended to allow for multiple sets (nsets) of hyperparameters to be selected."""


from bilby.core.result import read_in_result
import numpy as np
import gwpopulation as gwpop

def select_hyper(nsets=20):
    # read in all the hyperposterior samples
    PP_path = '../../GWTC-3-population-data/analyses/PowerLawPeak/o1o2o3_mass_c_iid_mag_iid_tilt_powerlaw_redshift_result.json'
    PP_result = read_in_result(PP_path)
    PP_hyperposterior_samples = PP_result.posterior.copy()

    # define a random seed
    np.random.seed(220222)

    # select a pseudo-random set of hyperposteriors
    hyper = PP_hyperposterior_samples.iloc[np.random.randint(0, len(PP_hyperposterior_samples))].to_dict()
    hyper = gwpop.conversions.convert_to_beta_parameters(hyper, remove=False)[0]
    # add in z_max
    hyper['z_max'] = 2.3
    PP_params = [hyper]

    for i in range(1,nsets):
        # define a random seed
        np.random.seed(220222+i)

        # select a pseudo-random set of hyperposteriors
        new_hyper = PP_hyperposterior_samples.iloc[np.random.randint(0, len(PP_hyperposterior_samples))].to_dict()

        # use the conversion tool pointed out by Colm Talbot
        new_hyper = gwpop.conversions.convert_to_beta_parameters(new_hyper, remove=False)[0]

        new_hyper['z_max'] = 2.3

        PP_params.append(new_hyper)

    return PP_params
