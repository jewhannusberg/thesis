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

MONTHS = [('January', '1'), ('February', '2'), ('March', '3'), ('April', '4'),
        ('May', '5'), ('June', '6'), ('July', '7'), ('August', '8'), ('September', '9'),
        ('October', '10'), ('November', '11'), ('December', '12')]

def list_files(dir):
    '''
    returns a list containing the files within the subfolders of DIR
    '''
    all_files = []
    names = []
    for root, _, files in os.walk(dir):
        for name in files:
            if '.CSV' in name or '.csv' in name:
                # clean up names to only contain date
                names.append(name) # probably change to dictionary for when reading in more data
                all_files.append(os.path.join(root, name))                                
            else:
                # TODO: Need to add a check here for any wrong file types
                # print "Wrong file type detected:", name 
                continue

    return all_files, names

def remove_csv(name):
    message = re.search('(.+)\.csv', name)
    if message:
        return message.group(1)
    else:
        return "Invalid name: " + str(name)

def clean_actual_names(fname, dirx):
    message = re.search('/.+_(\d+)_.+\.CSV', fname)
    if message:
        return message.group(1)
    else:
        return "Invalid name: " + str(fname)

def clean_fnames(fname, dirx):
    message = re.search(dirx + "/(.+)\.CSV", fname)
    if message:
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
    # Rename POE columns in all dataframes
    for name, df in forecasts.iteritems():
        # key = date
        # value = actual df

        df = df.rename(columns = {'OPERATIONAL_DEMAND_POE10':'OPERATIONAL_DEMAND_POE10_'+_get_date(name), 
                                'OPERATIONAL_DEMAND_POE50':'OPERATIONAL_DEMAND_POE50_'+_get_date(name),
                                'OPERATIONAL_DEMAND_POE90':'OPERATIONAL_DEMAND_POE90_'+_get_date(name)})
        forecasts[name] = df
    return forecasts

def rename_actual_columns(actuals):
    # Rename OPERATIONAL_DEMAND columns in all dataframes
    for name, df in actuals.iteritems():
        df = df.rename(columns = {'OPERATIONAL_DEMAND':'OPERATIONAL_DEMAND_'+name})
        actuals[name] = df
    return actuals

def convert_date(date):
    '''
    Convert ddMONTHyyyy strings to dd/mm/yy format used in data
    '''
    desired = re.search('(\d)(\d)([a-zA-Z]+)20(\d\d)', date)
    if desired:
        prefix = desired.group(1)
        word_month = desired.group(3)
        for (month, num_month) in MONTHS:
            if month == word_month:
                # convert date into required
                desired = desired.group(2) + "/" + num_month + "/" + desired.group(4)
                return desired, prefix
    else:
        return "Invalid date: " + str(date)

def get_time_poe(name):
    '''
    Take as input something of the form: OPERATIONAL_DEMAND_POE10_201703010000
    Return time=0000 and poe=POE10
    '''
    desired = re.search('OPERATIONAL_DEMAND_(POE\d\d)_2017\d\d\d\d(\d+)', name)
    if desired:
        return desired.group(2), desired.group(1)