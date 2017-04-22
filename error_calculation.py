'''
Use newly constructed files (from hh_forecast_time_var.py) to
finally calculate the error
'''

import os
import re
import pandas as pd
import data_cleanup
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

    # To plot POE10 ALL vs actual
    plt.plot(error_POE10[1:-1].values)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE10 forecasts for %s" % data_cleanup.remove_csv(fname))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    plt.show()
    plt.close()
    exit()

    error_POE50 = error.filter(regex="^OPERATIONAL_DEMAND_POE50_\d+$")

    error_POE90 = error.filter(regex="^OPERATIONAL_DEMAND_POE90_\d+$")

    # error = error[error.columns[1:-1]][1:-1] - error['ACTUAL_DEMAND'][1:-1].astype(float)
    error_POE10 = error_POE10[1:-1].sub(actual_demand, axis=0)
    # print error_POE10

    # plt.plot(error_POE10.values)
    # plt.plot(actual_demand.values, color='k', linewidth=2)
    # plt.show()
    # plt.close()

    # error_POE10.to_csv(POE10_DIR + fname)
    exit()


