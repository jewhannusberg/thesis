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

DIR = '../ForecastedData' # Move back a directory
PLOTTING = False

def list_files(dir):
    '''
    returns a list containing the files within the subfolders of DIR
    '''
    all_files = []
    names = []
    for root, _, files in os.walk(dir):
        for name in files:
            if '.CSV' in name:
                names.append(name) # probably change to dictionary for when reading in more data
                all_files.append(os.path.join(root, name))                                
            else:
                # TODO: Need to add a check here for any wrong file types
                continue

    return all_files, names


# Return a list of all the files within the folder and subfolders
all_files, names = list_files(DIR)

# ctr = 0
for file in all_files:
    print file
    data = pd.read_csv(file)
    data.columns = data.iloc[0] # make second row the column row
    # data.reindex(data.index.drop(1)) # drop the second row (original column row)
    data = data.loc[data['REGIONID'] == 'NSW1']

    demand = data.filter(['INTERVAL_DATETIME','OPERATIONAL_DEMAND_POE10',
                          'OPERATIONAL_DEMAND_POE50', 'OPERATIONAL_DEMAND_POE90'], axis=1)


    break
    # if ctr == 2:
    #     break
    # ctr += 1

if PLOTTING == True:
    plt.plot(demand['OPERATIONAL_DEMAND_POE10'].values, 'r', label='POE10', linewidth=0.75)
    plt.plot(demand['OPERATIONAL_DEMAND_POE50'].values, 'b', label='POE50', linewidth=0.75)
    plt.plot(demand['OPERATIONAL_DEMAND_POE90'].values, 'g', label='POE90', linewidth=0.75)
    plt.legend(loc='upper left', shadow=True)
    plt.title('Demand distributions for %s' % names[0])
    plt.show()
