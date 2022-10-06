#!/bin/bash

# create a folder for outputs
mkdir ../outputs

# run this script to run all the analysis files

python3 gibbs_sample.py $1

python3 generate_SNRs_FARs.py