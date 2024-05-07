"""Module providing a tidal analysis on imported text files"""

#!/usr/bin/env python3

# import the modules you need here
#import matplotlib.pyplot as plt
#import wget
#import os
#import uptide
#import pytz
#import math
#import glob
import argparse
import pandas as pd
import numpy as np




# Sets data being used temporarily
FILENAME1 = "data/1946ABE.txt"
FILENAME2 = "data/1947ABE.txt"


def read_tidal_data(filename):
    """Opens a specified file, formats columns as needed, and removes uneeded data"""
#Creates a gloobal variable
    #global data
# Reads in a dataframe and removes uneeded rows
    data = pd.read_csv(filename, sep = r"\s+", skiprows = [0,1,2,3,4,5,6,7,8,10])
# Renames column to 'Sea Level'
    data = data.rename(columns = {data.columns[3] : 'Sea Level'})
# Amalgamates the Date and Time column into one
    data["Datetime"] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
# Removes uneeded columns
    data = data.drop(columns = ['Date','Cycle', 'Residual'])
# Replaces any value containing M,N,T with NaN, in the 'Sea Level' column
    data.replace(to_replace =".*M$", value={"Sea Level" : np.nan}, regex=True, inplace=True)
    data.replace(to_replace =".*N$", value={"Sea Level" : np.nan}, regex=True, inplace=True)
    data.replace(to_replace =".*T$", value={"Sea Level" : np.nan}, regex=True, inplace=True)
    return data



def extract_single_year_remove_mean(year, data):
    """Siphones data of a specific year from the df, and subtracts the mean from each row"""
# Sets start and end points of the year
    year_string_start = str(year) + "0101"
    year_string_end = str(year) + "1231"
# Siphones that year from the df
#(https://www.codecademy.com/resources/docs/pandas/dataframe/loc)
    year_data = data.loc[year_string_start:year_string_end, ['Sea Level']]
# Sets all data in the new df as numeric values
    year_data = year_data.apply(pd.to_numeric, errors='raise')
# Calculates mean and subtracts from all data points
    year_data = (year_data)-(year_data['Sea Level'].mean())
    return year_data



def extract_section_remove_mean(start, end, data):
    """Siphones data of a specific section from the df, and subtracts the mean from each row"""
# Sets start and end points of the section
    section_start = str(start)
    section_end = str(end)
# Siphones that section from the df
#(https://www.codecademy.com/resources/docs/pandas/dataframe/loc)
    section_data = data.loc[section_start:section_end, ['Sea Level']]
# Sets all data in the new df as numeric values
    section_data = section_data.apply(pd.to_numeric, errors='raise')
# Calculates mean and subtracts from all data points
    section_data = (section_data)-(section_data['Sea Level'].mean())
    return section_data



def join_data(data1, data2):
    """Joins dfs along the x axis"""
# Joins the formatted files along the x axis
#(https://www.geeksforgeeks.org/how-to-combine-two-dataframe-in-python-pandas/)
    join_file = pd.concat([data1, data2])
    join_file = join_file.sort_values(by='Datetime', ascending=True)
    return join_file



def sea_level_rise(data):
    """a"""
    return



def tidal_analysis(data, constituents, start_datetime):
    """a"""
    return



def get_longest_contiguous_data(data):
    """a"""
    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     epilog="Copyright 2024, Jon Hill"
                     )
    parser.add_argument("directory",
                    help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                   action='store_true',
                    default=False,
                    help="Print progress")
    args = parser.parse_args()
    dirname = args.directory
    verbose = args.verbose

print(read_tidal_data("data/1947ABE.txt"))
