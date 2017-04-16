'''
Creates a dataframe that displays how forecasts change over time
e.g. let's say there are x forecast for 0630 (starting from 0000-> 0600)
Make a data structure which displays that shows:
for time x, demand forecasts were: ...

Sounds a bit like an ordered dictionary of arrays?
'''

import os
import numpy as np
import pandas as pd
import collections
from data_cleanup import list_files
from data_cleanup import clean_fnames
from data_cleanup import rename_forecast_columns
from plotting import plot_error
from plotting import plot_exceedance
from hh_accuracy import forecasted_demand_dataframes
from hh_accuracy import actual_demand_dataframes

FORECASTED_DIR = '../ForecastedData/20February2017' # Move back a directory to required date
ACTUAL_DIR = '../ActualData/20February2017'
STATE = 'NSW1'

# Return a list of all the files within the folder and subfolders
forecast_files, forecast_names = list_files(FORECASTED_DIR)

# Get a forecasted demand dataframe
forecasts = forecasted_demand_dataframes(forecast_files, forecast_names, STATE, FORECASTED_DIR)

# get actual demand data
actual_files, actual_names = list_files(ACTUAL_DIR)

# Get an actual demand dataframe
actual_demand = actual_demand_dataframes(actual_files, actual_names, state=STATE)

# Compute deviation from actual demand
# for f_file in range(len(forecast_files)):
#     print "FILE NAME:" + clean_fnames(forecast_files[f_file], FORECASTED_DIR)
#     print forecasts[clean_fnames(forecast_files[f_file], FORECASTED_DIR)]

# for key, value in forecasts.iteritems():
    # print key
    # print value.INTERVAL_DATETIME
    # value.merge(value, left_on='INTERVAL_DATETIME', right_on='INTERVAL_DATETIME', how='left')

# Attempt to merge two dataframes based on column INTERVAL_DATETIME
# SUCCESS!
# check = pd.DataFrame()
# check = forecasts['PUBLIC_FORECAST_OPERATIONAL_DEMAND_HH_201702202000_20170220193204'].merge(
#     forecasts['PUBLIC_FORECAST_OPERATIONAL_DEMAND_HH_201702202030_20170220200204'],
#     left_on='INTERVAL_DATETIME', right_on='INTERVAL_DATETIME', how='left')
# check = check.transpose()
# check.to_csv('check_merge.csv')

# Rename columns
forecasts = rename_forecast_columns(forecasts)
for key,value in forecasts.iteritems():
    print value.columns
    exit()

# Extend to all the forecasts in a day
full_df = forecasts[forecasts.keys()[0]]
forecasts.pop(forecasts.keys()[0], None)
for key in forecasts.iterkeys():
    # print key
    # print forecasts.keys()[forecasts.keys().index(key) + 1]
    # print "------------------------------------------------------------------------"
    # GOAT line
    # print "key: " + forecasts.keys()[len(forecasts)-1]
    # exit()
    if key != forecasts.keys()[len(forecasts)-1]:
        print key
        full_df = full_df.merge(forecasts.values()[forecasts.keys().index(key)+1], left_on='INTERVAL_DATETIME', right_on='INTERVAL_DATETIME', how='left')
full_df = full_df.merge(forecasts[forecasts.keys()[len(forecasts)-1]], left_on='INTERVAL_DATETIME', right_on='INTERVAL_DATETIME', how='left')
full_df = full_df.transpose()
full_df.to_csv('test1.csv')

