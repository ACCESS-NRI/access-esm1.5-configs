#!/bin/bash
#PBS -l ncpus=1
#PBS -l mem=16GB
#PBS -l jobfs=0GB
#PBS -q normal
#PBS -l walltime=00:30:00
#PBS -l wd
module use ~access/modules
module load pythonlib/um2netcdf4

/g/data/tm70/sw6175/development/um2nc-standalone/umpost/conversion_driver_esm1p5.py $PAYU_CURRENT_OUTPUT_DIR 
