"""A place for storing the functions required for the P_astro analysis"""

import numpy as np
import pandas as pd


def convert(pdf):
    """
    Ensure formatting of the input pdf for use in the cdf functions.

    Parameters
    ----------
    pdf: pandas dataframe
        The probability distribution of interest.
    
    Returns
    -------
    pdf: ndarray
        The pdf converted to numpy.
    """
    if isinstance(pdf, (pd.Series, pd.DataFrame)):
        pdf = pdf.to_numpy()
    return pdf

def cdf(pdf):
    """
    Compute the normalised CDF of the probability distribution x.

    Parameters
    ----------    
    pdf: ndarray
        The probability distribution of interest.
    
    Returns
    -------
    cdf: ndarray
        The normalised cumulative distribution of the input probability distribution.
    """
    pdf = convert(pdf)
    cdf = np.cumsum(pdf) # sum all the probabilities
    cdf = (cdf - cdf[0]) # subtract the first value so we start from zero
    cdf /= cdf[-1] # divide by the last value to normalise to 1
    return cdf


def cdf_samp(pdf, param):
    """
    Create and normalise the cdf and return a sample from it.
    
    Parameters
    ----------
    pdf: ndarray
        The probability distribution of interest.

    param: ndarray
        The range of values the parameter being sampled can take.

    Returns
    -------
    sample: float or complex (corresponding to fp) or ndarray
        Random sample from the cdf.
    """
    CDF = cdf(pdf)
    return np.interp(np.random.random(), CDF, param)

class spin():
    """A class for holding the spin calculation functions."""
    def __init__(self, a1, a2, tilt_1, tilt_2, q):
        self.a1 = a1
        self.a2 = a2
        self.tilt_1 = tilt_1
        self.tilt_2 = tilt_2
        self.q = q

    # create functions converting spins
    def chi_eff(self, a1, a2, tilt_1, tilt_2, q):
        r"""
        Compute the effective spin parameter, which is that aligned with the orbital angular momentum.

        .. math::
            \chi_{eff} = \frac{a_{1}\cos{\theta_{1}} + q a_{2} \cos{\theta_{2}}}{1+q}

        Parameters
        ----------
        a1, a2: float
            Spin magnitudes.

        tilt_1, tilt_2: float
            The tilt angles for bodies 1 and 2.

        q: float
            Mass ratio (:math: `\frac{m_2}{m_1}`).

        Returns
        -------
        chi_eff: float
            Effective spin parameter.
        """
        cos_theta1, cos_theta2 = np.cosine(tilt_1), np.cosine(tilt_2)
        return (a1*cos_theta1 + q*a2*cos_theta2)/(1+q)

    def chi_p(self, a1, a2, tilt_1, tilt_2, q):
        r"""
        Compute the effective spin precession parameter, which is that projected into the plane of the orbit.

        .. math::
            \chi_{p} = max(a_{1}\sin{\theta_{1}}, \frac{4q + 3}{4+3q}qa_{2}\sin{\theta_2})

        Parameters
        ----------
        a1, a2: float
            Spin magnitudes.

        tilt_1, tilt_2: float
            The tilt angles for bodies 1 and 2.

        q: float
            Mass ratio (:math: `\frac{m_2}{m_1}`).

        Returns
        -------
        chi_p: float
            Effective spin precession parameter.
        """
        sin_theta1, sin_theta2 = np.sine(tilt_1), np.sine(tilt_2)
        return np.maximum(a1*sin_theta1, (4*q+3)*q*a2*sin_theta2/(4+3*q))


# write the FAR conversion as a function
def SNR_to_FAR(snr, FAR8=5500, alpha=0.18):
    """
    Calculate the FAR using the parameterisations from the Lynch at al paper https://arxiv.org/abs/1803.02880.
    
    Parameters
    ----------
    snr: float
        Signal to noise ratio.
    FAR8: float
        The approximate false alarm rate for an SNR=8.
    alpha: float
        The steepness of the exponential function (:math: `\alpha`)

    Returns
    -------
    FAR: float
        The approximate false alarm rate for the input SNR.    
    """
    return FAR8*np.exp(-(snr-8)/alpha)