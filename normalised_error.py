'''
Calculate the normalised values of the error score at each half-hour interval
'''

import os
import re
import pandas as pd
from data_cleanup import remove_csv
from data_cleanup import convert_date
import plotting
from collections import OrderedDict
import matplotlib.pyplot as plt

POE10_DIR = '../poe10_error/'
POE50_DIR = '../poe50_error/'
POE90_DIR = '../poe90_error/'

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

for fname, df in POE10_data.iteritems():
    date, prefix = convert_date(remove_csv(fname))
    df = df.filter(regex="^OPERATIONAL_DEMAND_POE10_\d+$")

    plt.plot(norm_POE10.values)
    plt.show()
    plt.close()
    # norm_POE50
    # norm_POE90

    exit()