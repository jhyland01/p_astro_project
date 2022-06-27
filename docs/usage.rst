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
Download the GWTC-3 population data by running `bash download_data.sh`.

Select hyperposteriors
----------------------
Select a set of hyperposteriors, these are the parameters which describe the population models. 
This is achieved with the ``select_hyperposterior.select_hyper()`` function and defining how many sets of hyperparameters you want to select. 

.. autofunction:: select_hyperposterior.select_hyper
