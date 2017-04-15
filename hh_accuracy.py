# TODO: figure out a way to test __how the forecasts improve over time__

import os
import numpy as np
import pandas as pd
import collections
from data_cleanup import list_files
from data_cleanup import clean_fnames
from plotting import plot_error
from plotting import plot_exceedance

# Test on a single day first
FORECASTED_DIR = '../ForecastedData/09February2017' # Move back a directory to required date
ACTUAL_DIR = '../ActualData/09February2017'
STATE = 'NSW1'

def forecasted_demand_dataframes(forecast_files, forecast_names, state):
    demand_poe = pd.DataFrame() # initialise total dataframe

    '''SUPER FUCKING IMPORTANT'''
    # TODO: Use an ordered dictionary to preserve the order the data was read in!!
    forecasts = collections.OrderedDict()

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

# TODO: Need to read in ALL actual demand files
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
    # Boolean arrays. If exceeds, contains true. Else contains false
    POE10_over = np.empty(0)
    POE50_over = np.empty(0)
    POE90_over = np.empty(0)

    # Frequency count of exceedance
    count_POE10_over = 0
    count_POE50_over = 0
    count_POE90_over = 0

    # Calculate how often actual is greater than predicted
    # This occurs when actual - POEx > 0
    # Convert to numpy array for easier data operations
    error.OPERATIONAL_DEMAND_POE10 = error.OPERATIONAL_DEMAND_POE10.as_matrix()
    error.OPERATIONAL_DEMAND_POE50 = error.OPERATIONAL_DEMAND_POE50.as_matrix()
    error.OPERATIONAL_DEMAND_POE90 = error.OPERATIONAL_DEMAND_POE90.as_matrix()
    print error.OPERATIONAL_DEMAND_POE10

    POE10_over = np.array([error.OPERATIONAL_DEMAND_POE10 > 0])
    POE50_over = np.array([error.OPERATIONAL_DEMAND_POE50 > 0])
    POE90_over = np.array([error.OPERATIONAL_DEMAND_POE90 > 0])

    count_POE10_over = np.sum(POE10_over)
    count_POE50_over = np.sum(POE50_over)
    count_POE90_over = np.sum(POE90_over)

    print count_POE10_over
    print count_POE50_over
    print count_POE90_over

    return POE10_over, POE50_over, POE90_over

def error_calculation(forecasted_demand, actual_demand):
    # For actual discrepencies between POEx and actual_demand

    error = pd.DataFrame()

    # TODO: NEED TO FIX THIS - ONLY CARES FOR THE FIRST 48 DATAPOINTS
    error = forecasted_demand.merge(actual_demand)

    # POE10 error
    error.OPERATIONAL_DEMAND_POE10 = error.OPERATIONAL_DEMAND.values.astype(float) - error.OPERATIONAL_DEMAND_POE10.values.astype(float)

    # POE50 error
    error.OPERATIONAL_DEMAND_POE50 = error.OPERATIONAL_DEMAND.values.astype(float) - error.OPERATIONAL_DEMAND_POE50.values.astype(float)
    # POE90 error
    error.OPERATIONAL_DEMAND_POE90 = error.OPERATIONAL_DEMAND.values.astype(float) - error.OPERATIONAL_DEMAND_POE90.values.astype(float)

    POE10_over, POE50_over, POE90_over = exceeds_actual_counter(error, actual_demand)
 
    # plot_exceedance(forecasted_demand, actual_demand, error.OPERATIONAL_DEMAND_POE10)

    return error
'''
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
    error = error_calculation(forecasts[clean_fnames(forecast_files[f_file])], actual_demand)

plot_error(error, actual_demand)
'''