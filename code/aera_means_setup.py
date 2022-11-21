# Calculate global means of surface air temperature and CO2 vmr from archived netCDF files
# of the historical run
# Give name of the run as argument
import sys, iris, netCDF4, numpy as np, os, glob, cf_units, cftime, warnings

RUNID = sys.argv[1]

d = netCDF4.Dataset('aera_input.nc', 'w')
d.createDimension('time', None)
d.createDimension('nv', 2)
d.createVariable('time', np.float32, ('time',))
d.createVariable('time_bnds', np.float32, ('time','nv'))
d.createVariable('tas', np.float32, ('time',))
d.createVariable('co2', np.float32, ('time',))

time = d.variables['time']
time.units = 'days since 1850-01-01 00:00'
time.calendar = 'proleptic_gregorian'
time.bounds = 'time_bnds'
time.standard_name = 'time'

tas = d.variables['tas']
tas.units = 'K'
# This doesn't work?
# tas:cell_methods = "time: mean"
setattr(tas, 'cell_methods', 'area: time: mean')
tas.standard_name = 'air_temperature'

co2 = d.variables['co2']
co2.units = 'kg/kg'
setattr(co2, 'cell_methods', 'area: time: mean')
co2.standard_name = "mass_fraction_of_carbon_dioxide_tracer_in_air"

d.close()

areacella = iris.load_cube('/g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/piControl/r1i1p1f1/fx/areacella/gn/latest/areacella_fx_ACCESS-ESM1-5_piControl_r1i1p1f1_gn.nc')

d = netCDF4.Dataset('aera_input.nc', 'r+')
time_var = d.variables['time']
time_bnds = d.variables['time_bnds']
tas_var = d.variables['tas']
co2_var = d.variables['co2']
time_units = cf_units.Unit("days since 1850-01-01 00:00", calendar='proleptic_gregorian')

# For iris to merge need a callback that skips the history attribute
def fixatts(cube, field, filename):
    # Remove the attributes that prevent merging
    del cube.attributes['history']

nlev = 38
for year in range(1850,2015):

    files = glob.glob(os.path.join('/g/data/p73/archive/CMIP6/ACCESS-ESM1-5', RUNID, 'history', 'atm', 'netCDF',
                                   f'{RUNID}.pa-{year}*.nc'))
    files.sort()
    # Need to use load and concatenate rather than load_cube because merge doesn't work
    # with existing time dimensions
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Ignoring netCDF variable")
        warnings.filterwarnings("ignore", message="Missing CF-netCDF boundary variable")
        warnings.filterwarnings("ignore", message="Missing CF-netCDF formula term variable")
        tas = iris.load(files, 'fld_s03i236', callback=fixatts).concatenate_cube()
        co2 = iris.load(files, 'fld_s00i252', callback=fixatts).concatenate_cube()
        p_rho = iris.load(files, 'fld_s00i407', callback=fixatts).concatenate_cube()
        ps = iris.load(files, 'fld_s00i409', callback=fixatts).concatenate_cube()

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
    co2_int = co2_w.collapsed(['atmosphere_hybrid_height_coordinate'], iris.analysis.SUM)  / ps.data
    co2_ann = co2_int.collapsed(['time'], iris.analysis.MEAN)
    co2_g = co2_ann.collapsed(['latitude', 'longitude'], iris.analysis.MEAN, weights=areacella.data)

    nt = len(time_var)
    date0 = cftime.DatetimeProlepticGregorian(year, 1, 1, 0, 0, 0)
    date1 = cftime.DatetimeProlepticGregorian(year+1, 1, 1, 0, 0, 0)
    time_bnds[nt,0] = time_units.date2num(date0)
    time_bnds[nt,1] = time_units.date2num(date1)
    time_var[nt] = time_bnds[nt].mean()
    tas_var[nt] = tas_g.data
    co2_var[nt] = co2_g.data
    d.sync()

d.close()
