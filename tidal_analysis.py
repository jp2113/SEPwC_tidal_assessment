#!/usr/bin/env python3

# import the modules you need here
import argparse
import numpy as np
import pandas as pd
import glob


filename = "data/1947ABE.txt"


# Opens a specified file, formats columns as needed, and removes uneeded data
def read_tidal_data(filename):
# Creates a gloobal variable 
    global data
# Removes unneeded data
    data = pd.read_csv(filename , sep=r"\s+", skiprows=[0,1,2,3,4,5,6,7,8,10])
# Amalgamating the Date and Time column into one
    data["Datetime"] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
# Renames column to 'Sea Level'
    data = data.rename(columns={data.columns[3] : 'Sea Level'})
# Removes uneeded columns
    data = data.drop(columns = ['Date','Time'])
# Replaces any value containing M,N,T with NaN, in the 'Sea Level' column
    data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    #print(data)
    
    return(data)

read_tidal_data(filename)



# Creates new df with specified year, and subtracts the mean from each data point
def extract_single_year_remove_mean(year, data):
# Creates a global variable for viewing purposes
    global year_data
# Sets start and end points of the year
    year_start = str(year) + "0101"
    year_end = str(year) + "1231"
# Siphones that year from the df
    year_data = data.loc[year_start:year_end, ['Sea Level']]
# Sets all data in the new df as numeric values
    year_data = year_data.apply(pd.to_numeric, errors='raise')
# Calculates mean and subtracts from all data points
    year_data = (year_data)-(year_data.mean())
    #print(year_data)
    
    return (year_data)

extract_single_year_remove_mean(1947, data)



def extract_section_remove_mean(start, end, data):
# Creates a global variable for viewing purposes
    global section_data
# Sets start and end points of the section
    section_start = str(start)
    section_end = str(end)
# Siphones that section from the df
    section_data = data.loc[section_start:section_end, ['Sea Level']]
# Sets all data in the new df as numeric values
    section_data = section_data.apply(pd.to_numeric, errors='raise')
# Calculates mean and subtracts from all data points
    section_data = (section_data)-(section_data.mean())
    print(section_data)
    
    return data

extract_section_remove_mean(19470501, 19471031, data)




def join_data(data1, data2):
    #formatted_data1 = read_tidal_data(data1)
    #formatted_data2 = read_tidal_data(data2)
    #tidal_data_set = pd.merge(formatted_data1, formatted_data2)
    #print(tidal_data_set)
    
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
    
print(read_tidal_data("data/1947ABE.txt"))











