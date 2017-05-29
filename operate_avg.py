import os
import plotting
import numpy as np
import pandas as pd
from collections import OrderedDict
from data_cleanup import convert_date
from data_cleanup import remove_csv

POE10_DIR = '../avg_error_poe10/'
POE50_DIR = '../avg_error_poe50/'
POE90_DIR = '../avg_error_poe90/'

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

def exceeds_zero_error(df):
    return df.values[1][np.where(df.values[1] > 0)].size

# Need to read everything in this time
POE10_filenames, POE10_data = get_data(POE10_DIR)
POE50_filenames, POE50_data = get_data(POE50_DIR)
POE90_filenames, POE90_data = get_data(POE90_DIR)

# set up multi-bar bar chart
poe10_exceedance = exceeds_zero_error(POE10_data["09February2017_avg_err.csv"])
poe50_exceedence = exceeds_zero_error(POE50_data["09February2017_avg_err.csv"])
poe90_exceedence = exceeds_zero_error(POE90_data["09February2017_avg_err.csv"])
poe10_exceedance_2 = exceeds_zero_error(POE10_data["10February2017_avg_err.csv"])
poe50_exceedence_2 = exceeds_zero_error(POE50_data["10February2017_avg_err.csv"])
poe90_exceedence_2 = exceeds_zero_error(POE90_data["10February2017_avg_err.csv"])
date1, prefix1 = convert_date(remove_csv("09February2017_avg_err.csv"))
date2, prefix2 = convert_date(remove_csv("10February2017_avg_err.csv"))

y = [poe10_exceedance, poe50_exceedence, poe90_exceedence]
z = [poe10_exceedance_2, poe50_exceedence_2, poe90_exceedence_2]
x = np.arange(3)

# generate multi-bar bar chart
plotting.generate_multi_bar(x, y, z)

# fnames are shared by all dictionaries
for fname, df in POE10_data.iteritems(): # dfs contain the average error values of the POE level specified above
    # get the date and prefix of date (0, 1, 2, etc)
    date, prefix = convert_date(remove_csv(fname))

    # Plot all POE errors together
    plotting.plot_all_errors_one_graph(fname, df, POE50_data[fname], POE90_data[fname], date, prefix)

    poe10_exceedance = exceeds_zero_error(df)
    poe50_exceedence = exceeds_zero_error(POE50_data[fname])
    poe90_exceedence = exceeds_zero_error(POE90_data[fname])
    x_ax = [poe10_exceedance, poe50_exceedence, poe90_exceedence]
    # Plot histogram
    plotting.plot_exceedance_num(x_ax, prefix, date)
