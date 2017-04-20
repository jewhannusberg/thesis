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
'''Module imports'''
import data_cleanup
from plotting import plot_error
from plotting import plot_exceedance
from plotting import plot_forecast_vs_poe
from hh_accuracy import actual_demand_dataframes
from hh_accuracy import forecasted_demand_dataframes
from hh_accuracy import error_calculation_dictionaries

DATE = '31March2017'
FORECASTED_DIR = '../ForecastedData/' + DATE # Move back a directory to required date
ACTUAL_DIR = '../ActualData/' #+ DATE
STATE = 'NSW1'

# Return a list of all the files within the folder and subfolders
forecast_files, forecast_names = data_cleanup.list_files(FORECASTED_DIR)

# Get a forecasted demand dataframe
forecasts = forecasted_demand_dataframes(forecast_files, forecast_names, STATE, FORECASTED_DIR)

# get actual demand data
actual_files, actual_names = data_cleanup.list_files(ACTUAL_DIR)

# Get an actual demand dataframe
actuals = actual_demand_dataframes(actual_files, actual_names, STATE, ACTUAL_DIR)

# Compute deviation from actual demand
# for f_file in range(len(forecast_files)):
#     print "FILE NAME:" + data_cleanup.clean_fnames(forecast_files[f_file], FORECASTED_DIR)
#     print forecasts[data_cleanup.clean_fnames(forecast_files[f_file], FORECASTED_DIR)]

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

# Rename columns -- needed for merge
forecasts = data_cleanup.rename_forecast_columns(forecasts)
actuals = data_cleanup.rename_actual_columns(actuals)

# Extend to all the forecasts in a day
full_df = forecasts[forecasts.keys()[0]]
forecasts.pop(forecasts.keys()[0], None)
for key in forecasts.iterkeys():
    if key != forecasts.keys()[len(forecasts)-1]: # Prevents index error at last key
        # print key
        full_df = full_df.merge(forecasts.values()[forecasts.keys().index(key)+1], left_on='INTERVAL_DATETIME', right_on='INTERVAL_DATETIME', how='left')
# This will only put 1 days worth of actual demand
for key in actuals.iterkeys():
    if key != actuals.keys()[len(actuals)-1]:
        full_df = full_df.merge(actuals[key], left_on='INTERVAL_DATETIME', right_on='INTERVAL_DATETIME', how='left')

'''Uncomment to save the dataframe to a csv transposed
Comment for any plotting requirements
Need to apply this for all data'''
full_df = full_df.transpose()
full_df.to_csv('../HH_FinalData/'+ DATE + '.csv')

# error = error_calculation_dictionaries(forecasts, actuals)

# plot_forecast_vs_poe(full_df, time='201702200000', dates=actuals.keys()[0:len(actuals)-1])


