'''
Read, clean and save the data
'''

import os
import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

FORECASTED_DIR = '../ForecastedData' # Move back a directory
ACTUAL_DIR = '../ActualData'
PLOTTING = True

def list_files(dir):
    '''
    returns a list containing the files within the subfolders of DIR
    '''
    all_files = []
    names = []
    for root, _, files in os.walk(dir):
        for name in files:
            if '.CSV' in name:
                # clean up names to only contain date
                names.append(name) # probably change to dictionary for when reading in more data
                all_files.append(os.path.join(root, name))                                
            else:
                # TODO: Need to add a check here for any wrong file types
                print "Wrong file type detected:", name 
                continue

    return all_files, names


# Return a list of all the files within the folder and subfolders
forecast_files, forecast_names = list_files(FORECASTED_DIR)

demand_poe = pd.DataFrame() # initialise total dataframe
for file in forecast_files:
    print file
    data = pd.read_csv(file)

    data.columns = data.iloc[0] # make second row the column row

    data = data.loc[data['REGIONID'] == 'NSW1'] # keep only NSW data

    # keep the following columns, discard the remainder
    demand = data.filter(['INTERVAL_DATETIME','OPERATIONAL_DEMAND_POE10',
                          'OPERATIONAL_DEMAND_POE50', 'OPERATIONAL_DEMAND_POE90'], axis=1)

    # take only the latest estimate of each interval from the files
    # e.g. for 0030 take 0000 forecast of POE10, POE50, and POE90
    demand_poe = demand_poe.append(demand.iloc[0], ignore_index=True)
    # daily_demand = daily_demand.append(demand, ignore_index=True)


# TODO: dataframe of multiple days


# get actual demand data
actual_files, actual_names = list_files(ACTUAL_DIR)

actual_demand = pd.DataFrame() # initialise total dataframe
for file in actual_files:
    print file
    data = pd.read_csv(file)

    # slightly hacky solution to remove duplicate OPERATIONAL_DEMAND columns
    drop_cols = [0,1,2,3]
    data.drop(data.columns[drop_cols],axis=1,inplace=True)

    data.columns = data.iloc[0] # make second row the column row

    data = data.loc[(data['REGIONID'] == 'NSW1')] # keep only NSW data

    # keep the following columns, discard the remainder
    actual_demand = data[['INTERVAL_DATETIME','OPERATIONAL_DEMAND']]



if PLOTTING == True:
    # plot projected demand @ all POE
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE10'].values, 'r', label='POE10', linewidth=0.75)
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE50'].values, 'b', label='POE50', linewidth=0.75)
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE90'].values, 'g', label='POE90', linewidth=0.75)
    plt.plot(actual_demand['OPERATIONAL_DEMAND'].values, 'k:', label='Actual Demand', linewidth=1.5)

    plt.legend(loc='upper left', shadow=True)
    plt.title('Demand distributions for %s' % forecast_names[0])

    # overlay actual demand
    plt.show()