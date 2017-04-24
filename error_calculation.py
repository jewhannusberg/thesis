'''
Use newly constructed files (from hh_forecast_time_var.py) to
finally calculate the error
'''

import os
import re
import pandas as pd
import data_cleanup
import plotting
from collections import OrderedDict
import matplotlib.pyplot as plt
DIR = '../clean_data/'
POE10_DIR = '../poe10_error/'
POE50_DIR = '../poe50_error/'
POE90_DIR = '../poe90_error/'

# read the csv files into dictionary of dataframes
# make the dictionary key = name in names

data = OrderedDict()
filenames = []
for filename in os.listdir(DIR):
    if filename.endswith(".CSV") or filename.endswith(".csv"): 
        data[filename] = pd.read_csv(DIR+filename)
        data[filename] = data[filename].transpose()
        data[filename].columns = data[filename].iloc[0] # make second row the column row
        filenames.append(filename) # just in case filenames are needed again
    else:
        continue

for fname, df in data.iteritems():

    error = df

    actual_demand = error['ACTUAL_DEMAND'][1:-1].astype(float)
    error_POE10 = error.filter(regex="^OPERATIONAL_DEMAND_POE10_\d+$")

    error_POE50 = error.filter(regex="^OPERATIONAL_DEMAND_POE50_\d+$")

    error_POE90 = error.filter(regex="^OPERATIONAL_DEMAND_POE90_\d+$")

    # plotting.save_all(error_POE10, fname)
    # plotting.save_all(error_POE50, fname)
    # plotting.save_all(error_POE90, fname)
    """
    '''To plot POE10 ALL vs actual'''
    plt.plot(error_POE10[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE10 forecasts for %s" % data_cleanup.remove_csv(fname))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    plt.savefig("figures/poe10/POE10_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)
    # save to report figures also
    plt.savefig("../Report/figures/poe10/POE10_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)

    '''To plot POE50 ALL vs actual'''
    plt.plot(error_POE50[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE50 forecasts for %s" % data_cleanup.remove_csv(fname))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    plt.savefig("figures/poe50/POE50_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)
    # save to report figures also
    plt.savefig("../Report/figures/poe50/POE50_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)

    '''To plot POE90 ALL vs actual'''
    plt.plot(error_POE90[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE90 forecasts for %s" % data_cleanup.remove_csv(fname))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    plt.savefig("figures/poe90/POE90_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)
    # save to report figures also
    plt.savefig("../Report/figures/poe90/POE90_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)
    """

    '''Subtraction'''
    error_POE10 = error_POE10[1:-1].sub(actual_demand, axis=0)
    error_POE10.to_csv(POE10_DIR + fname)

    error_POE50 = error_POE50[1:-1].sub(actual_demand, axis=0)
    error_POE50.to_csv(POE50_DIR + fname)

    error_POE50 = error_POE50[1:-1].sub(actual_demand, axis=0)
    error_POE50.to_csv(POE50_DIR + fname)



