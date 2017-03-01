'''
Read, clean and save the data
'''

import os
import sys
import math
import numpy as np
import pandas as pd

DIR = '../ForecastedData' # Move back a directory

def list_files(dir):
    '''
    returns a list containing the files within the subfolders of DIR
    '''
    all_files = []
    for root, _, files in os.walk(dir):
        for name in files:
            if '.CSV' in name:
                all_files.append(os.path.join(root, name))                                
            else:
                # TODO: Need to add a check here for any wrong file types
                continue
                
    return all_files


# Return a list of all the files within the folder and subfolders
all_files = list_files(DIR)


for file in all_files:
    print file
    data = pd.read_csv(file)
    data.columns = data.iloc[0] # make second row the column row
    print data.columns
    # if data['PUBLIC'] == 'NSW1':
        # demand = data.filter(['2016/09/10','FORECAST_OPERATIONAL_DEMAND_HH','DEMAND'], axis=1)
    # forecasted_demand = data['FORECAST_OPERATIONAL_DEMAND_HH']
    # print forecasted_demand
    # actual_demand = data['DEMAND']
    # print actual_demand

    break

