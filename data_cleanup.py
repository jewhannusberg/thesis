'''
Read, clean and save the data
'''

import os
import re
import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# better to read these in as user input and modify constants to fit
FORECASTED_DIR = '../ForecastedData/09February2017' # Move back a directory to required date
ACTUAL_DIR = '../ActualData/09February2017'
PLOTTING1 = False
PLOTTING2 = False

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

def clean_fnames(fname, dirx):
    message = re.search(dirx + "/(.+)\.CSV", fname)
    if message:
        # print message.group(1)
        return message.group(1)
    else:
        return "Invalid name: " + str(fname)

def _get_date(name):
    date = re.search(".+_(\d+)_.+", name)
    if date:
        return date.group(1)
    else:
        return "Invalid name: " + str(name) 

def rename_forecast_columns(forecasts):
    # Rename POE columns in all dataframes -- move this to data_cleanup.py when done and working
    for name, df in forecasts.iteritems():
        # key = date
        # value = actual df

        df = df.rename(columns = {'OPERATIONAL_DEMAND_POE10':'OPERATIONAL_DEMAND_POE10_'+_get_date(name), 
                                'OPERATIONAL_DEMAND_POE50':'OPERATIONAL_DEMAND_POE10_'+_get_date(name),
                                'OPERATIONAL_DEMAND_POE90':'OPERATIONAL_DEMAND_POE10_'+_get_date(name)})
        forecasts[name] = df
    return forecasts