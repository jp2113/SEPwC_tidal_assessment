#!/usr/bin/env python3

# import the modules you need here
import argparse
import numpy as np
import pandas as pd
import glob

# Opens a specified file, formats columns as needed, and removes uneeded data
def read_tidal_data(filename):
# Removes unneeded data
    tidal_data = pd.read_csv(filename , sep=r"\s+", skiprows=[0,1,2,3,4,5,6,7,8,10])
# Renames column to 'Sea Level'
    tidal_data = tidal_data.rename(columns={tidal_data.columns[3] : 'Sea Level'})
# Amalgamating the Date and Time column into one
    tidal_data["Datetime"] = pd.to_datetime(tidal_data['Date'] + ' ' + tidal_data['Time'])
    tidal_data = tidal_data.set_index("Datetime")
# Replaces any value containing M,N,T with NaN, in the 'Sea Level' column
    tidal_data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    tidal_data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    tidal_data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True, inplace=True)

    
    return tidal_data


def extract_single_year_remove_mean(year, data):
   
    return 

def extract_section_remove_mean(start, end, data):
    
    return 

def join_data(data1, data2):
    
    return 

def sea_level_rise(data):
                                                     
    return 

def tidal_analysis(data, constituents, start_datetime):
    
    return 

def get_longest_contiguous_data(data):
    
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


