'''Construct an average scalar of each error. e.g. for 01/03/2017 average POE10 error = x,
average POE50 error = y, average POE90 error = z. Use this to construct a histogram.'''


# need to do:
# 1. all average POE errors on the same plot
# 2. when not on same figure, include horizontal line of overall average error
# 3. create csv file containing the single-value average of each day (should be easy after doing 2)
# 4. create a histogram of these daily average error values for each POE level


import os
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


# Need to read everything in this time
POE10_filenames, POE10_data = get_data(POE10_DIR)
POE50_filenames, POE50_data = get_data(POE50_DIR)
POE90_filenames, POE90_data = get_data(POE90_DIR)


# fnames are shared by all dictionaries
for fname, df in POE10_data.iteritems(): # dfs contain the average error values of the POE level specified above
    if fname == "19March2017.csv": # This date is broken.
        continue

    # get the date and prefix of date (0, 1, 2, etc)
    date, prefix = convert_date(remove_csv(fname))


    plotting.plot_all_errors_one_graph(fname, df, POE50_data[fname], POE90_data[fname], date, prefix)


    exit()


