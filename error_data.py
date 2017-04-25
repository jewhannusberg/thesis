'''
Operate on the error files to construct error tables, values, etc
Works on ONE directory at a time
'''
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
from data_cleanup import convert_date
from data_cleanup import remove_csv
from data_cleanup import get_time_poe
from plotting import plot_single_day_time_error
from plotting import plot_single_day_all_time_error

POE10_DIR = '../poe10_error/'
POE50_DIR = '../poe50_error/'
POE90_DIR = '../poe90_error/'

# separate the relevant information from data here
data = OrderedDict()
filenames = []
for filename in os.listdir(POE10_DIR):
    if filename.endswith(".CSV") or filename.endswith(".csv"): 
        data[filename] = pd.read_csv(POE10_DIR+filename)
        data[filename] = data[filename].transpose()
        data[filename].columns = data[filename].iloc[0] # make second row the column row
        filenames.append(filename) # just in case filenames are needed again
    else:
        continue

for fname, df in data.iteritems():
    '''Plot single day forecast at a single time'''
    date = convert_date(remove_csv(fname))

    # limit the data to the specified date
    df = df.filter(regex=date)

    # limit the data to a specific point in time, e.g. OPERATIONAL_DEMAND_POE10_201703010000 (row 1)
    # comment the following line to get ALL forecasts for the specified date
    data_series = df.iloc[1,:] # Note that this creates a series
    time, poe = get_time_poe(data_series.name)
    # plot_single_day_time_error(data_series, date, time, poe)

    '''Plot single day forecast at all times'''
    plot_single_day_all_time_error(df)

    exit()

    '''Plot a full error forecast'''