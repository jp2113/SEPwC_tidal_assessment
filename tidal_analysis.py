#!/usr/bin/env python3

# import the modules you need here
import argparse
import numpy as np
import pandas as pd
import glob


# Opens a specified file, formats columns as needed, and removes uneeded data
def read_tidal_data(filename):
    global data
# Removes unneeded data
    data = pd.read_csv(filename , sep=r"\s+", skiprows=[0,1,2,3,4,5,6,7,8,10])
# Renames column to 'Sea Level'
    data = data.rename(columns={data.columns[3] : 'Sea Level'})
# Amalgamating the Date and Time column into one
    data["Datetime"] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
# Replaces any value containing M,N,T with NaN, in the 'Sea Level' column
    data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    
    return data


def extract_single_year_remove_mean(year, data):
    data['Date'] = pd.DatetimeIndex(data['Date']).year
    year_data = data['Date']
    global year_data_start
    global year_data_end
    year_data_start = str(year) + '0101'
    year_data_end = str(year) + '1231'
    # remove mean to oscillate around zero
    mmm = np.mean(year_data['Sea Level'])
    year_data['Sea Level'] -= mmm
    
    return data

def extract_section_remove_mean(start, end, data):
    year_data = data.loc[year_data_start:year_data_end, ['Tide']]
    mmm = np.mean(year_data['Sea Level'])
    year_data['Sea Level'] -= mmm
    
    return data

def join_data(data1, data2):
    formatted_data1 = read_tidal_data(data1)
    formatted_data2 = read_tidal_data(data2)
    tidal_data_set = pd.merge(formatted_data1, formatted_data2)
    print(tidal_data_set)
    
    return 

def sea_level_rise(data):
                                                     
    return 

def tidal_analysis(data, constituents, start_datetime):
    
    return 

def get_longest_contiguous_data(data):
    
    return 

tidal_file = 'data/1947ABE.txt'
tidal_file2 = 'data/1946ABE.txt'

join_data(tidal_file, tidal_file2)


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











