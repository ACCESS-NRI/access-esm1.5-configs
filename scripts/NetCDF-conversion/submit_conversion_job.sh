#!/bin/bash

# Submit the UM fields file to netcdf conversion job.
# Provide it with the correct output directory from payu.

CONVERSION_PBS_STORAGE=${PBS_NCI_STORAGE}+gdata/hh5+gdata/access+gdata/tm70 

qsub -l storage=${CONVERSION_PBS_STORAGE}\
    -P ${PROJECT} \
    -v PAYU_CURRENT_OUTPUT_DIR=${PAYU_CURRENT_OUTPUT_DIR} \
    ./scripts/NetCDF-conversion/UM_conversion_job.sh
