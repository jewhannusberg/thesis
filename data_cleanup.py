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
    # data.reindex(data.index.drop(1)) # drop the second row (original column row)
    print data.columns
    
    data = data.loc[data['REGIONID'] == 'NSW1']

    demand = data.filter(['INTERVAL_DATETIME','OPERATIONAL_DEMAND_POE10',
                          'OPERATIONAL_DEMAND_POE50', 'OPERATIONAL_DEMAND_POE90'], axis=1)
    break
print demand.columns

