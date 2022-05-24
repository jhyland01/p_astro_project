"""A place for storing the functions required for the P_astro analysis"""

import numpy as np


def cdf(prob_dist):
    """Compute the normalised CDF of the probabilioty distribution x.
    :param prob_dist: The probability distribution of interest.
    :returns: The normalised cumulative distribution of the input probability distribution.
    """
    cdf = np.cumsum(prob_dist).to_numpy() # sum all the probabilities
    cdf = (cdf - cdf[0]) # subtract the first value so we start from zero
    cdf /= cdf[-1] # divide by the last value to normalise to 1
    return cdf