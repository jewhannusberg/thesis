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

# Need to read everything in this time
POE10_filenames, POE10_data = get_data(POE10_DIR)
POE50_filenames, POE50_data = get_data(POE50_DIR)
POE90_filenames, POE90_data = get_data(POE90_DIR)

for fname, df in POE10_data.iteritems():
    date, prefix = convert_date(remove_csv(fname))
    # limit the data to the specified date
    poe10_single_day = df.filter(regex=date)
    # print poe10_single_day.shape
    poe50_single_day = POE50_data[fname].filter(regex=date)
    poe90_single_day = POE90_data[fname].filter(regex=date)
    time, poe = get_time_poe(poe10_single_day.iloc[1,:].name)


    plt.plot(poe10_single_day.transpose().values[:,1:-1])
    plt.show()
    plt.close()
    
    exit()
    plot_single_day_all_time_error(poe10_single_day, date, poe, prefix)
    exit()