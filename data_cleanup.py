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

def clean_fnames(fname):
    message = re.search(FORECASTED_DIR + "/(.+)\.CSV", fname)
    if message:
        return message.group(1)
    else:
        return "Invalid name: " + str(fname)