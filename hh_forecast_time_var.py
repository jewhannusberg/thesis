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
forecasts = forecasted_demand_dataframes(forecast_files, forecast_names, state=STATE)

# get actual demand data
actual_files, actual_names = list_files(ACTUAL_DIR)

# Get an actual demand dataframe
actual_demand = actual_demand_dataframes(actual_files, actual_names, state=STATE)


# Compute deviation from actual demand
for f_file in range(len(forecast_files)):
    print forecasts(f_files).columns
    exit()