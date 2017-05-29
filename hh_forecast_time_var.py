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
actual = actuals[actuals.keys()[0]]
# actuals.pop(actuals.keys()[0], None)

# Rename to become overall operational demand
# Very dangerous line - needs to be changed if the first data file changes
# Currently first file is 09/02/2017
# actual = actual.rename(columns = {'OPERATIONAL_DEMAND_20170209':'ACTUAL_DEMAND'})

for key in actuals.iterkeys():
    if key != actuals.keys()[len(actuals)-1]:
        # actual.ACTUAL_DEMAND += actuals[key]['OPERATIONAL_DEMAND_'+key] # Very hacky - relies on keys being consistent
        full_df = full_df.merge(actuals[key], left_on='INTERVAL_DATETIME', right_on='INTERVAL_DATETIME', how='left')
# full_df = full_df.merge(actual, left_on='INTERVAL_DATETIME', right_on='INTERVAL_DATETIME', how='left')
# print full_df.columns
# exit()

# for key in actuals.iterkeys():
    # if key in full_df.columns




'''Uncomment to save the dataframe to a csv transposed
Comment for any plotting requirements
Need to apply this for all data'''
# full_df = full_df.transpose()
# full_df.to_csv('../HH_FinalData/'+ DATE + '.csv')

# error = error_calculation_dictionaries(forecasts, actuals)

# plot_forecast_vs_poe(full_df, time='201702200000', dates=actuals.keys()[0:len(actuals)-1])


