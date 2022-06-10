"""Tests for functions used within the project."""

import numpy as np
import numpy.testing as npt
import pytest
import pandas as pd


@pytest.mark.parametrize(
    "test, expected",
    [
        (np.ones(100), 1),
    ])
def test_cdf_norm(test, expected):
    """Test the cdf function is normalised."""
    from analysis.p_astro_utils import cdf
    npt.assert_array_equal(cdf(test)[-1], expected)

@pytest.mark.parametrize(
    "test, expected",
    [
        (pd.DataFrame({'values': [1,1,1,1]}), (0.25,1)),
    ])
def test_cdf_inputs(test, expected):
    """Test the cdf function is takes various inputs."""
    from analysis.p_astro_utils import cdf
    npt.assert_array_equal((cdf(test['values'])[0],cdf(test['values'])[-1]), expected)