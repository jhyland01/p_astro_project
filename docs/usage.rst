Usage
=====

.. _installation:

Installation
------------

This project only needs installed as a package if you wish to run tests, the .py files can be run without any installation.
To install, clone the project and navigate to the root of the project directory and run:

.. code-block:: console

   (.venv) $ pip3 install .

Download data
-------------
Download the GWTC-3 population data by running 

.. code-block:: console
    bash download_data.sh

Select hyperposteriors
----------------------
Select a set of hyperposteriors, these are the parameters which describe the population models. 
This is achieved with the ``select_hyperposterior.select_hyper()`` function and defining how many sets of hyperparameters you want to select. 

.. autofunction:: select_hyperposterior.select_hyper

Sample from hyperposteriors
---------------------------
Sample from these sets of hyperposteriors to obtain posterior samples (mass, spin, redshift).
There is a dependency $m_1 > m_2$ and we sample mass and mass ratio so the values the mass ratio can take are dependent on what $m_1$ has been sampled as, we therefore use Gibbs sampling to account for this interdependence.
For each set of hyperposteriors, 1000 posterior samples are obtained, this can be changed withing the ``gibbs_sample.py`` script if necessary.
As an example, run 

.. code-block:: console
    python3 gibbs_sample.py 30 
    
to Gibbs sample from 30 sets of hyperposteriors.
The output will be saved as ``params_for_SNR.csv`` in the ouputs folder.

Generate SNRs and FARs
----------------------
Next we need to generate some signal-to-noise ratios (SNRs) and some false alarm rates (FARs).
To do this we run the ``generate_SNRs_FARs.py`` script which uses ``bilby``.
This reads in the ``params_for_SNR.csv`` and uses the posterior samples to generate waveforms.
It currently uses the `IMRPhenomPv2` waveform approximant, this can be updated.
The FARs are approximated using a parameterisation presented in the Lynch et. al. paper.
This will output the ``params_inc_FAR.csv`` file.

Calculate P_astro
-----------------
Following this we calculate the true alarm rates (TARs) and $P_\text{astro}$, underway as the ``event_rate.ipynb`` file.

SQL database creation
---------------------
The `'create_database.py`'' script turns the `'params_inc_FAR.csv`'' for searching/manipulating as an SQLite3 database if you are so inclined.