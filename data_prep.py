'''
Clean up the ForecastedData folder where data is downloaded
Unzip csv files
'''

import os
import sys
import glob
import zipfile

DIR = '../ForecastedData/16February2017/' # this should go through every folder in the directory
DIRx = '../ForecastedData/'
# move listScraper.sh, data_prep.py, items.txt (for now), links.txt (for now) into /thesisb


def scrub_data(directory):
    for root, _, files in os.walk(directory):
        for name in files:
            # regex check: does the name end in .zip?
            if not name.endswith(".zip"):
                print "deleting files not ending in .zip"
                os.remove(root+name)

def unzip_data(directory):
    zip_files = glob.glob(DIR+'*.zip')
    for fname in zip_files:
        zip_handler = zipfile.ZipFile(fname, "r")
        zip_handler.extractall(DIR)
        zip_handler.close()
        if not fname.endswith(".CSV"):
            print "deleting files not ending in .CSV"
            os.remove(fname)

days = [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
temp_DIRx = ""
for i in days:
    temp_DIRx = DIRx + str(i) + "February2017/"
    print temp_DIRx 
    scrub_data(temp_DIRx)
    unzip_data(temp_DIRx)
