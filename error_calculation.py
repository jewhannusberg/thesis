import os
import pandas as pd
from data_cleanup import remove_csv
from data_cleanup import convert_date
import plotting
from collections import OrderedDict

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

    error = df # initialise error dataframe

    actual_demand = error['ACTUAL_DEMAND'][1:-1].astype(float) # actual demand series

    # filter out the POE levels into seperate dataframes
    error_POE10 = error.filter(regex="^OPERATIONAL_DEMAND_POE10_\d+$")
    error_POE50 = error.filter(regex="^OPERATIONAL_DEMAND_POE50_\d+$")
    error_POE90 = error.filter(regex="^OPERATIONAL_DEMAND_POE90_\d+$")

    # save plots of all the non-error data
    plotting.save_all_plots(error_POE10, error_POE50, error_POE90, actual_demand, fname, prefix, date)

    # subtract actual from the forecasted
    error_POE10 = error_POE10[1:-1].sub(actual_demand, axis=0)
    error_POE50 = error_POE50[1:-1].sub(actual_demand, axis=0)
    error_POE90 = error_POE90[1:-1].sub(actual_demand, axis=0)

    # save to csv files
    error_POE10.to_csv(POE10_DIR + fname)
    error_POE50.to_csv(POE50_DIR + fname)
    error_POE90.to_csv(POE90_DIR + fname)
