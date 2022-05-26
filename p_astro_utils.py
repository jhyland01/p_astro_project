"""A place for storing the functions required for the P_astro analysis"""

import numpy as np
import pandas as pd


def cdf(pdf):
    """Compute the normalised CDF of the probabilioty distribution x.
    :param prob_dist: The probability distribution of interest.
    :returns: The normalised cumulative distribution of the input probability distribution.
    """
    if isinstance(pdf, pd.Series) == True:
        pdf = pdf.to_numpy()
    cdf = np.cumsum(pdf).to_numpy() # sum all the probabilities
    cdf = (cdf - cdf[0]) # subtract the first value so we start from zero
    cdf /= cdf[-1] # divide by the last value to normalise to 1
    return cdf


def cdf_samp(pdf, param):
    # create and normalise the cdf
    if isinstance(pdf, pd.Series) == True:
        pdf = pdf.to_numpy()
    cdf = np.cumsum(pdf)
    cdf = (cdf - cdf[0])
    cdf /= cdf[-1]
    # now we take a sample from the cdf
    samp = np.interp(np.random.random(), cdf, param)
    return samp


# create functions converting spins
def chi_eff(a1, a2, cos_theta1, cos_theta2, q):
    chi = (a1*cos_theta1 + q*a2*cos_theta2)/(1+q)
    return chi

def chi_p(a1, a2, sin_theta1, sin_theta2, q):
    chi = np.maximum(a1*sin_theta1, (4*q+3)*q*a2*sin_theta2/(4+3*q))
    return chi