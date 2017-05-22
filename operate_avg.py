'''Construct an average scalar of each error. e.g. for 01/03/2017 average POE10 error = x,
average POE50 error = y, average POE90 error = z. Use this to construct a histogram.'''


# need to do:
# 1. all average POE errors on the same plot
# 2. count number of times error exceeds 0
# 3. create csv file containing the single-value average of each day (should be easy after doing 2)
# 4. create a histogram of these daily average error values for each POE level


import os
import numpy as np
import pandas as pd
from collections import OrderedDict
import plotting
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


# fnames are shared by all dictionaries
for fname, df in POE10_data.iteritems(): # dfs contain the average error values of the POE level specified above
    if fname == "19March2017.csv": # This date is broken.
        continue
    print fname
    # get the date and prefix of date (0, 1, 2, etc)
    date, prefix = convert_date(remove_csv(fname))

    # Plot all POE errors together
    # plotting.plot_all_errors_one_graph(fname, df, POE50_data[fname], POE90_data[fname], date, prefix)

    # Count the number of times POEx exceeds 0 error
    tot = df.values[1].size
    poe10_exceedance = exceeds_zero_error(df)
    poe50_exceedence = exceeds_zero_error(POE50_data[fname])
    poe90_exceedence = exceeds_zero_error(POE90_data[fname])
    x_ax = [poe10_exceedance, poe50_exceedence, poe90_exceedence]
    x_prob = [1 - poe10_exceedance/float(tot), 1 - poe50_exceedence/float(tot), 1 - poe90_exceedence/float(tot)]
    # Plot histogram
    plotting.plot_exceedance_num(x_ax, prefix, date)

    # Get average error value

    # Plot histogram of average error

    # exit()


