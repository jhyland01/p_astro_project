"""A place for storing the functions required for the P_astro analysis"""

import numpy as np
import pandas as pd


def convert(pdf):
    """
    Ensure formatting of the input pdf for use in the cdf functions.
    Parameters
    ==========
    pdf: pandas dataframe
        The probability distribution of interest.
    Returns
    =======
    pdf: numpy
        The pdf converted to numpy.
    """
    if isinstance(pdf, (pd.Series, pd.DataFrame)):
        pdf = pdf.to_numpy()
    return pdf

def cdf(pdf):
    """Compute the normalised CDF of the probability distribution x.
    :param prob_dist: The probability distribution of interest.
    :returns: The normalised cumulative distribution of the input probability distribution.
    """
    pdf = convert(pdf)
    cdf = np.cumsum(pdf) # sum all the probabilities
    cdf = (cdf - cdf[0]) # subtract the first value so we start from zero
    cdf /= cdf[-1] # divide by the last value to normalise to 1
    return cdf


def cdf_samp(pdf, param):
    """create and normalise the cdf and return a sample from it."""
    CDF = cdf(pdf)
    return np.interp(np.random.random(), CDF, param)


# create functions converting spins
def chi_eff(a1, a2, cos_theta1, cos_theta2, q):
    return (a1*cos_theta1 + q*a2*cos_theta2)/(1+q)

def chi_p(a1, a2, sin_theta1, sin_theta2, q):
    return np.maximum(a1*sin_theta1, (4*q+3)*q*a2*sin_theta2/(4+3*q))


# write the FAR conversion as a function
def SNR_to_FAR(snr, FAR8=5500, alpha=0.18):
    """Calculate the FAR using the parameterisations from the Lynch paper"""
    return FAR8*np.exp(-(snr-8)/alpha)