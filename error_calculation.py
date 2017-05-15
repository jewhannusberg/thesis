'''
Use newly constructed files (from hh_forecast_time_var.py) to
finally calculate the error
'''

import os
import re
import pandas as pd
from data_cleanup import remove_csv
from data_cleanup import convert_date
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
    date, prefix = convert_date(remove_csv(fname))

    error = df

    actual_demand = error['ACTUAL_DEMAND'][1:-1].astype(float)
    error_POE10 = error.filter(regex="^OPERATIONAL_DEMAND_POE10_\d+$")

    error_POE50 = error.filter(regex="^OPERATIONAL_DEMAND_POE50_\d+$")

    error_POE90 = error.filter(regex="^OPERATIONAL_DEMAND_POE90_\d+$")

    plotting.save_all_plots(error_POE10, error_POE50, error_POE90, actual_demand, fname, prefix, date)

    '''Subtraction'''
    error_POE10 = error_POE10[1:-1].sub(actual_demand, axis=0) # FORECASTED MINUS ACTUAL
    error_POE10.to_csv(POE10_DIR + fname)

    error_POE50 = error_POE50[1:-1].sub(actual_demand, axis=0) # FORECASTED MINUS ACTUAL
    error_POE50.to_csv(POE50_DIR + fname)

    error_POE90 = error_POE90[1:-1].sub(actual_demand, axis=0) # FORECASTED MINUS ACTUAL
    error_POE90.to_csv(POE90_DIR + fname)
