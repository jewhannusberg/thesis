# TODO: figure out a way to test __how the forecasts improve over time__

import os
import numpy as np
import pandas as pd
from data_cleanup import list_files
from data_cleanup import clean_fnames
from plotting import plot_error

# Test on a single day first
FORECASTED_DIR = '../ForecastedData/09February2017' # Move back a directory to required date
ACTUAL_DIR = '../ActualData/09February2017'
STATE = 'NSW1'

def forecasted_demand_dataframes(forecast_files, forecast_names, state):
    demand_poe = pd.DataFrame() # initialise total dataframe
    forecasts = {}
    # print forecast_names
    for fname in forecast_files:
        # print file
        data = pd.read_csv(fname)

        data.columns = data.iloc[0] # make second row the column row

        data = data.loc[data['REGIONID'] == state] # keep only specified states' data

        # keep the following columns, discard the remainder
        demand = data.filter(['INTERVAL_DATETIME','OPERATIONAL_DEMAND_POE10',
                            'OPERATIONAL_DEMAND_POE50', 'OPERATIONAL_DEMAND_POE90'], axis=1)
        # take only the latest estimate of each interval from the files
        # e.g. for 0030 take 0000 forecast of POE10, POE50, and POE90
        # demand_poe = demand_poe.append(demand.iloc[0], ignore_index=True)
        # daily_demand = daily_demand.append(demand, ignore_index=True)
        forecasts[clean_fnames(fname)] = demand

    return forecasts

def actual_demand_dataframes(actual_files, actual_names, state):
    actual_demand = pd.DataFrame() # initialise total dataframe
    for file in actual_files:
        print file
        data = pd.read_csv(file)

        # slightly hacky solution to remove duplicate OPERATIONAL_DEMAND columns
        drop_cols = [0,1,2,3]
        data.drop(data.columns[drop_cols],axis=1,inplace=True)

        data.columns = data.iloc[0] # make second row the column row

        data = data.loc[(data['REGIONID'] == state)] # keep only NSW data

        # keep the following columns, discard the remainder
        actual_demand = data[['INTERVAL_DATETIME','OPERATIONAL_DEMAND']]
    return actual_demand

def exceeds_actual_counter(error, actual_demand):
    return None

def error_calculation(forecasted_demand, actual_demand):
    # For actual discrepencies between POEx and actual_demand
    error = pd.DataFrame()
    error = forecasted_demand.merge(actual_demand)

    # For frequency of innacuracy
    count_POE10_over = 0
    count_POE50_over = 0
    count_POE90_over = 0

    # POE10 error
    error.OPERATIONAL_DEMAND_POE10 = error.OPERATIONAL_DEMAND.values.astype(float) - error.OPERATIONAL_DEMAND_POE10.values.astype(float)
    count_POE10_over += error.OPERATIONAL_DEMAND_POE10
    # Convert to numpy array for easier data operations
    count_POE10_over = count_POE10_over.as_matrix()
    exit()

    # if actual exceeds POE iterate counter
    # POE50 error
    error.OPERATIONAL_DEMAND_POE50 = error.OPERATIONAL_DEMAND.values.astype(float) - error.OPERATIONAL_DEMAND_POE50.values.astype(float)
    # POE90 error
    error.OPERATIONAL_DEMAND_POE90 = error.OPERATIONAL_DEMAND.values.astype(float) - error.OPERATIONAL_DEMAND_POE90.values.astype(float)

    return error

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
    print f_file
    error = error_calculation(forecasts[clean_fnames(forecast_files[f_file])], actual_demand)
    print error
    break

plot_error(error)