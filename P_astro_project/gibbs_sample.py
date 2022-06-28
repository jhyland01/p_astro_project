"""Script for Gibbs sampling from the mass spin and redshuft distributions to generate a population of sources."""

import gwpopulation as gwpop
import numpy as np
import pandas as pd
from p_astro_utils import cdf_samp, chi_eff, chi_p
from bilby.hyper.model import Model
from P_astro_project import select_hyperposterior
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('nsets', help='number of hyperposterior sets to sample from', type=int)
cli_args = parser.parse_args()

PP_params = select_hyperposterior.select_hyper(cli_args.nsets)

# initiate a list to hold the dataframes of each set of samples from each set of hyperparameters
df_list = []

for j in range(0,len(PP_params)):
  # first obtain PP_params by running the select_hyperposterior.py script

  base_mass = gwpop.models.mass.SinglePeakSmoothedMassDistribution(mmin = PP_params[j]['mmin'],
                                                      mmax = PP_params[j]['mmax'])
  base_spin_mag = gwpop.models.spin.iid_spin_magnitude_beta
  base_spin_ori = gwpop.models.spin.iid_spin_orientation_gaussian_isotropic
  # can treat the redshift model a little differently, it is a class and the functions within don't need split out
  z_model = Model([gwpop.models.redshift.PowerLawRedshift(z_max = PP_params[j]['z_max'])])

  base_mass.parameters = base_spin_mag.parameters  = base_spin_ori.parameters = z_model.parameters = PP_params[j]

  # we end up discarding the first sample so set nsamps to n+1 of what you want
  nsamps = 1001
  m1_sample = np.zeros(nsamps)
  q_sample = np.zeros(nsamps)
  a_1_sample = np.zeros(nsamps)
  a_2_sample = np.zeros(nsamps)
  cos_tilt_1_sample = np.zeros(nsamps)
  cos_tilt_2_sample = np.zeros(nsamps)
  redshift_sample = np.zeros(nsamps)

  # first get an initial point to loop from, call our initial point m1=30, q=1. Use this q=1 for p(m|q)
  m1_sample[0] = 30
  q_sample[0] = 1
  # I don't actually need to define these as they don't have dependencies
  a_1_sample[0] = 0.5
  a_2_sample[0] = 0.5
  cos_tilt_1_sample[0] = 0
  cos_tilt_2_sample[0] = 0
  redshift_sample[0] = 1

  # difference in time is 55s for 200 fill_samps or 65s for 5000 fill_samps
  # these fill_samps are there to fill the space for the cdf
  fill_samps = 5000
  m1s = np.linspace(PP_params[j]['mmin']+0.02,PP_params[j]['mmax'],fill_samps) # small amount added to the minimum mass to ensure we stay within the range
  a = np.linspace(0,1,fill_samps)
  cos_tilt = np.linspace(-1,1,fill_samps)
  redsh = np.linspace(0,2.3,fill_samps)


  for i in range(1,nsamps):
      # build a dataframe to fill the pdf space
      qs_1 = np.full(fill_samps, q_sample[i-1])
      space_df = pd.DataFrame(m1s, columns = ['mass_1'])
      space_df = space_df.assign(mass_ratio = qs_1,
                                a_1 = a,
                                a_2 = a,
                                cos_tilt_1 = cos_tilt,
                                cos_tilt_2 = cos_tilt,
                                redshift = redsh)
      # obtain the pdf
      p_m1s = base_mass.p_m1(space_df, alpha = PP_params[j]['alpha'], 
                mmin = PP_params[j]['mmin'], 
                mmax = PP_params[j]['mmax'], 
                lam = PP_params[j]['lam'], 
                mpp = PP_params[j]['mpp'], 
                sigpp = PP_params[j]['sigpp'])
      # sample randomly from the cdf
      m1_sample[i] = cdf_samp(p_m1s, m1s)
      
      # define a minimum q , based on our mass sample
      q_min = PP_params[j]['mmin']/m1_sample[i]
      qs = np.linspace(q_min,1,fill_samps)
      # use the sampled m1 and the prob(q)=p_q from the mass model in gwpopulation
      m1s_new = np.full(fill_samps, m1_sample[i])

      space_df_q = pd.DataFrame(m1s_new, columns = ['mass_1'])
      space_df_q = space_df_q.assign(mass_ratio = qs)

      p_qs = base_mass.p_q(space_df_q, PP_params[j]['beta'], PP_params[j]['mmin'], PP_params[j]['delta_m'])

      q_sample[i] = cdf_samp(p_qs, qs)

      #now for spin mag
      p_a1s = gwpop.utils.beta_dist(space_df["a_2"], PP_params[j]['alpha_chi'], PP_params[j]['beta_chi'], scale=np.max(a))
      a_1_sample[i] = cdf_samp(p_a1s, a)

      p_a2s = gwpop.utils.beta_dist(space_df["a_2"], PP_params[j]['alpha_chi'], PP_params[j]['beta_chi'], scale=np.max(a))
      a_2_sample[i] = cdf_samp(p_a2s, a)

      # and the spin ori, this is currently ignoring the effect of the xi term for mixing field and dynamical
      # so we choose a random number between 0 and 1 and compare this to the value of xi_spin
      # check which channel is determined by above or below xi_spin, if less then proceed by field channel
      channel = np.random.random()
      if channel < PP_params[j]['xi_spin']:

        p_cos1s = gwpop.utils.truncnorm(space_df["cos_tilt_1"], 1, PP_params[j]['sigma_spin'], 1, -1)
        cos_tilt_1_sample[i] = cdf_samp(p_cos1s, cos_tilt)

        p_cos2s = gwpop.utils.truncnorm(space_df["cos_tilt_2"], 1, PP_params[j]['sigma_spin'], 1, -1)
        cos_tilt_2_sample[i] = cdf_samp(p_cos2s, cos_tilt)
      # if greater, proceed by dynamic channel
      else:
        p_cos1s = np.full(fill_samps, 0.25)
        cos_tilt_1_sample[i] = cdf_samp(p_cos1s, cos_tilt)

        p_cos2s = np.full(fill_samps, 0.25)
        cos_tilt_2_sample[i] = cdf_samp(p_cos2s, cos_tilt)

      # finally, the redhift
      p_zs = z_model.prob(space_df)
      redshift_sample[i] = cdf_samp(p_zs, redsh)


  # keep only the samples obtained from the Gibbs method, excluding the starter
  samples_sgl = pd.DataFrame(m1_sample[1:], columns = ['mass_1'])
  samples_sgl = samples_sgl.assign(mass_ratio = q_sample[1:],
                                  a_1 = a_1_sample[1:],
                                a_2 = a_2_sample[1:],
                                cos_tilt_1 = cos_tilt_1_sample[1:],
                                cos_tilt_2 = cos_tilt_2_sample[1:],
                                redshift = redshift_sample[1:])

  # append each dataframe of samples to a list of such dataframes
  df_list.append(samples_sgl)

# concatenate this list of dataframes into one dataframe
samples = pd.concat(df_list)

# have a check to see if there are any NaNs in the sampled dataframe, True if there are
print('Check for NaNs:' + str(samples.isnull().values.any))

# save down the samples with some extra parameter calculations
samples = samples.assign(mass_2 = samples['mass_1']*samples['mass_ratio'])
samples = samples.assign(tilt_1 = np.arccos(samples['cos_tilt_1']))
samples = samples.assign(tilt_2 = np.arccos(samples['cos_tilt_2']))
samples = samples.assign(sin_tilt_1 = np.sin(samples['tilt_1']))
samples = samples.assign(sin_tilt_2 = np.sin(samples['tilt_2']))
samples = samples.assign(chi_eff = chi_eff(samples['a_1'], samples['a_2'],samples['tilt_1'],samples['tilt_2'],samples['mass_ratio']))
samples = samples.assign(chi_p = chi_p(samples['a_1'], samples['a_2'],samples['tilt_1'],samples['tilt_2'],samples['mass_ratio']))
samples = samples.assign(spin1z = samples['a_1']*samples['cos_tilt_1'])
samples = samples.assign(spin2z = samples['a_2']*samples['cos_tilt_2'])
samples = samples.assign(spin1x = samples['a_1']*samples['sin_tilt_1'])
samples = samples.assign(spin2x = samples['a_2']*samples['sin_tilt_2'])

# after concatenating the dataframes we have duplicate indices, so we need to reindex
samples.reindex()

samples.to_csv('../outputs/params_for_SNR.csv')