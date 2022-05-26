#!/bin/bash

# Run this script to download data from the GWTC-3 populations paper.
# The complete data release for the GWTC-3 populations paper can be found at:
# https://zenodo.org/record/5655785
# https://dcc.ligo.org/LIGO-P2100239/public

# Download data from the public entry above
wget -P ../ https://zenodo.org/record/5655785/files/GWTC-3-population-data.tar.gz

# Unzip
tar -xvzf ../GWTC-3-population-data.tar.gz

# Remove zipped files
rm ../GWTC-3-population-data.tar.gz
