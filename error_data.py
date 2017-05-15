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
from plotting import plot_med_avg_error

POE10_DIR = '../poe10_error/'
POE50_DIR = '../poe50_error/'
POE90_DIR = '../poe90_error/'

# separate the relevant information from data here
data = OrderedDict()
filenames = []
for filename in os.listdir(POE50_DIR):
    if filename.endswith(".CSV") or filename.endswith(".csv"): 
        data[filename] = pd.read_csv(POE50_DIR+filename)
        data[filename] = data[filename].transpose()
        data[filename].columns = data[filename].iloc[0] # make second row the column row
        filenames.append(filename) # just in case filenames are needed again
    else:
        continue

for fname, df in data.iteritems():
    print fname
    if fname == "19March2017.csv": # NEED TO REDOWNLOAD DATA FOR THIS DATE
        continue
    '''Plot single day forecast at a single time'''
    date, prefix = convert_date(remove_csv(fname))
    # limit the data to the specified date
    # print date

    single_day_df = df.filter(regex=date)

    # limit the data to a specific point in time, e.g. OPERATIONAL_DEMAND_POE10_201703010000 (row 1)
    data_series = single_day_df.iloc[1,:] # Note that this creates a series
    time, poe = get_time_poe(data_series.name)
    print poe
    # plot_single_day_time_error(data_series, date, time, poe, prefix)

    '''Plot single day forecast at all times'''
    # Get the actual value and plot on top
    # plot_single_day_all_time_error(single_day_df, date, poe, prefix)

    '''Plot the median and average error on the same plot'''
    '''Should consider doing this for single day forecasts as well'''
    df = df.transpose()
    df = df.convert_objects(convert_numeric=True)
    avg_vals = df.mean(axis=1, skipna=True, numeric_only=True)
    med_vals = df.median(axis=1, skipna=True, numeric_only=True)
    
    # NEED TO PLOT ALL POE10, POE50, and POE90 avg/med errors on the same figure
    plot_med_avg_error(avg_vals, med_vals, poe, date, prefix)

    '''Construct a table of median and average data'''
    avg_vals.to_csv("../avg_error_%s/%s_avg_err.csv" % (poe.lower(), remove_csv(fname)))
    med_vals.to_csv("../med_error_%s/%s_med_err.csv" % (poe.lower(), remove_csv(fname)))

    '''Construct an average scalar of each error. e.g. for 01/03/2017 average POE10 error = x,
    average POE50 error = y, average POE90 error = z. Use this to construct a histogram.'''
    # print avg_vals
    # exit()
