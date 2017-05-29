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
from plotting import plot_poex_single_time_error
from plotting import plot_poex_single_time_full_error

POE10_DIR = '../poe10_error/'
POE50_DIR = '../poe50_error/'
POE90_DIR = '../poe90_error/'

# separate the relevant information from data here
def get_data(directory):
    data = OrderedDict()
    filenames = []
    for filename in os.listdir(directory): # change this line for POE level change
        if filename.endswith(".CSV") or filename.endswith(".csv"): 
            data[filename] = pd.read_csv(directory+filename) # change this line for POE level change
            data[filename] = data[filename].transpose()
            data[filename].columns = data[filename].iloc[0] # make second row the column row
            filenames.append(filename) # just in case filenames are needed again
        else:
            continue
    return filenames, data

POE10_filenames, POE10_data = get_data(POE10_DIR)
POE50_filenames, POE50_data = get_data(POE50_DIR)
POE90_filenames, POE90_data = get_data(POE90_DIR)

for fname, df in POE10_data.iteritems():
    date, prefix = convert_date(remove_csv(fname)) # get date, prefix

    # limit the data to the specified date
    poe10_single_day = df.filter(regex=date)
    poe50_single_day = POE50_data[fname].filter(regex=date)
    poe90_single_day = POE90_data[fname].filter(regex=date)

    # limit the data to a specific point in time, e.g. OPERATIONAL_DEMAND_POE10_201703010000 (row 1)
    data_series = poe10_single_day.iloc[1,:] # Note that this creates a series
    poe50_series = poe50_single_day.iloc[1,:]
    poe90_series = poe90_single_day.iloc[1,:]

    # non-limited data
    poe10_all = df.iloc[1,:]
    poe50_all = POE50_data[fname].iloc[1,:]
    poe90_all = POE90_data[fname].iloc[1,:]

    time, poe = get_time_poe(data_series.name) # get time, poe level

    '''To plot single time error for a single POE level'''
    plot_single_day_time_error(data_series, date, time, poe, prefix)

    '''To plot all POE levels at a single time'''
    plot_poex_single_time_error(data_series, poe50_series, poe90_series, time, prefix, date)
    plot_poex_single_time_full_error(poe10_all, poe50_all, poe90_all, time, prefix, date)

    '''Plot single day forecast at all times'''
    plot_single_day_all_time_error(poe10_single_day, date, poe, prefix)
    plot_single_day_all_time_error(poe50_single_day, date, "POE50", prefix)
    plot_single_day_all_time_error(poe90_single_day, date, "POE90", prefix)

    '''Plot the median and average error on the same plot'''
    '''Should consider doing this for single day forecasts as well'''
    df = df.transpose()
    df = df.convert_objects(convert_numeric=True)
    avg_vals = df.mean(axis=1, skipna=True, numeric_only=True)
    med_vals = df.median(axis=1, skipna=True, numeric_only=True)

    plot_med_avg_error(avg_vals, med_vals, poe, date, prefix)

    '''Construct a table of median and average data'''
    avg_vals.to_csv("../avg_error_%s/%s_avg_err.csv" % (poe.lower(), remove_csv(fname)))
    med_vals.to_csv("../med_error_%s/%s_med_err.csv" % (poe.lower(), remove_csv(fname)))
