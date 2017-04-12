# TODO: figure out a way to test __how the forecasts improve over time__
import os
import pandas as pd
from data_cleanup import list_files
from data_cleanup import clean_fnames

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
        demand_poe = demand_poe.append(demand.iloc[0], ignore_index=True)
        # daily_demand = daily_demand.append(demand, ignore_index=True)
        clean_ = clean_fnames(fname)
        print clean_
        exit()
        forecasts[clean_fnames(fname)] = demand_poe
    print forecasts
    return demand_poe

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


# Return a list of all the files within the folder and subfolders
forecast_files, forecast_names = list_files(FORECASTED_DIR)
# Get a forecasted demand dataframe
demand_poe = forecasted_demand_dataframes(forecast_files, forecast_names, state=STATE)
# print demand_poe
exit()
# get actual demand data
actual_files, actual_names = list_files(ACTUAL_DIR)
# Get an actual demand dataframe
actual_demand = actual_demand_dataframes(actual_files, actual_names, state=STATE)

