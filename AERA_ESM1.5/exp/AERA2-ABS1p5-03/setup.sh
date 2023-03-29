# Setup the AERA2 experiment for 2026 start
# Run in the experiment directory

RUNID=$(basename $PWD)
mkdir -p aera_data
cp /g/data/p66/mrd599/AERA/CO2_fluxes_AERA_ABS1p5-03.anc aera_data/CO2_fluxes_${RUNID}.anc
ln -s aera_data/CO2_fluxes_${RUNID}.anc CO2_flux.anc
cp /g/data/p66/mrd599/AERA/aera_input_AERA-ABS1p5-03_1850-2025.nc aera_data/aera_input_${RUNID}.nc
python /g/data/p66/mrd599/AERA/aera_co2_update.py ${RUNID} 2025
