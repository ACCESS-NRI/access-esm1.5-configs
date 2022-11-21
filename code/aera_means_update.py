import os, sys, iris, netCDF4, cf_units, cftime, glob, numpy as np

RUNID = sys.argv[1]
archivedir = sys.argv[2]
year = int(sys.argv[3])  # Just completed

# Update the time series of global mean surface air temperature
# Must have already been calculated from the historical run
areacella = iris.load_cube('/g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/piControl/r1i1p1f1/fx/areacella/gn/latest/areacella_fx_ACCESS-ESM1-5_piControl_r1i1p1f1_gn.nc')

d = netCDF4.Dataset(f'aera_data/aera_input_{RUNID}.nc', 'r+')
time_var = d.variables['time']
time_bnds = d.variables['time_bnds']
tas_var = d.variables['tas']
co2_var = d.variables['co2']
time_units = cf_units.Unit("days since 1850-01-01 00:00", calendar='proleptic_gregorian')

nt = len(time_var)
date0 = cftime.DatetimeProlepticGregorian(year, 1, 1, 0, 0, 0)
date1 = cftime.DatetimeProlepticGregorian(year+1, 1, 1, 0, 0, 0)
tb0 = time_units.date2num(date0)
tb1 = time_units.date2num(date1)
newt = (tb0+tb1)*0.5
# Check that the times are correctly in sequence before setting anything
if not 365 <= (newt - time_var[nt-1]) <= 366:
    print("Time mismatch from aera_means_update.py", time_var[nt-1], newt, file=sys.stderr)
    print("Unexpected difference of", newt - time_var[nt-1], file=sys.stderr)
    raise Exception("Time mismatch from aera_means_update.py")

nlev = 38
files = glob.glob(os.path.join(archivedir, 'history', 'atm',
                                f'{RUNID}.pa-{year}*'))
files.sort()
tas = iris.load_cube(files, iris.AttributeConstraint(STASH='m01s03i236'))
ps = iris.load_cube(files, iris.AttributeConstraint(STASH='m01s00i409'))
# The surface_altitude coordinate doesn't match because it was saved as a monthly mean
# Removing it in a callback doesn't work, perhaps because it hasn't been added at
# that state.
co2 = iris.cube.CubeList([iris.load_cube(f, iris.AttributeConstraint(STASH='m01s00i252')) for f in files])
p_rho = iris.cube.CubeList([iris.load_cube(f, iris.AttributeConstraint(STASH='m01s00i407')) for f in files])
for c in co2:
    c.remove_coord('surface_altitude')
for c in p_rho:
    c.remove_coord('surface_altitude')
co2 = co2.merge_cube()
p_rho = p_rho.merge_cube()

tas_ann = tas.collapsed(['time'], iris.analysis.MEAN)
tas_g = tas_ann.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=areacella.data)

# Vertically integrate CO2 using the difference between the rho level pressures.
dp = np.zeros((12, nlev, 145, 192))
dp[:,0] = ps.data - p_rho.data[:,1]
for k in range(1,nlev-1):
    dp[:,k] = p_rho.data[:,k] - p_rho.data[:,k+1]
dp[:,nlev-1] = p_rho.data[:,nlev-1]
dp[:] = dp[:]
co2_w = co2 * dp
co2_int = co2_w.collapsed(['model_level_number'], iris.analysis.SUM)  / ps.data
co2_ann = co2_int.collapsed(['time'], iris.analysis.MEAN)
co2_g = co2_ann.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=areacella.data)

time_bnds[nt,0] = tb0
time_bnds[nt,1] = tb1
time_var[nt] = newt
tas_var[nt] = tas_g.data
co2_var[nt] = co2_g.data

d.close()
