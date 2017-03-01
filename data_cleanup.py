'''
Read, clean and save the data
'''

import os
import sys
import math
import numpy as np
import pandas as pd

DIR = './ForecastedData'

def list_files(dir):
    '''
    returns a list containing the files within the subfolders of DIR
    '''
    all_files = []
    for root, _, files in os.walk(dir):
        for name in files:
            if name is '.DS_Store':
                continue
            else:
                # Need to add a check here for any wrong file types
                all_files.append(os.path.join(root, name))                
    return all_files


# Return a list of all the files within the folder and subfolders
all_files = list_files(DIR)

for file in all_files:
    print file
    data = pd.read_csv(file)
    print data.columns
    break

