#!/usr/bin/env python3

# import the modules you need here
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import wget
import os
import numpy as np
import uptide
import pytz
import math
import argparse
import glob



# Sets data being used temporarily
filename1 = "data/1946ABE.txt"
filename2 = "data/1947ABE.txt"
files =["data/1946ABE.txt", "data/1947ABE.txt"]


# Opens a specified file, formats columns as needed, and removes uneeded data
def read_tidal_data(filename):
  # Creates a gloobal variable 
    global data
  # Reads in a dataframe and removes uneeded rows (https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)
    data = pd.read_csv(filename , sep=r"\s+", skiprows=[0,1,2,3,4,5,6,7,8,10])
  # Amalgamates the Date and Time column into one (https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)
    data["Datetime"] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
  # Renames column to 'Sea Level'
    data = data.rename(columns={data.columns[3] : 'Sea Level'})
  # Removes uneeded columns (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html)
    data = data.drop(columns = ['Date','Time', 'Cycle', 'Residual'])
  # Replaces any value containing M,N,T with NaN, in the 'Sea Level' column
    data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    #print(data)
    return(data)

# Calls function
read_tidal_data(filename2)



# Siphones data of a specific year from the df, and subtracts the mean from each data point
def extract_single_year_remove_mean(year, data):
  # Creates a global variable for viewing purposes
    global year_data
  # Sets start and end points of the year
    year_start = str(year) + "0101"
    year_end = str(year) + "1231"
  # Siphones that year from the df (https://www.codecademy.com/resources/docs/pandas/dataframe/loc)
    year_data = data.loc[year_start:year_end, ['Sea Level']]
  # Sets all data in the new df as numeric values (https://saturncloud.io/blog/calculating-averages-of-multiple-columns-ignoring-nan-a-guide-for-data-scientists/#:~:text=By%20setting%20the%20skipna%3DTrue,columns%20while%20ignoring%20NaN%20values.)
    year_data = year_data.apply(pd.to_numeric, errors='raise')
  # Calculates mean and subtracts from all data points (https://stackoverflow.com/questions/35169368/subtract-every-column-in-dataframe-with-the-mean-of-that-column-with-python)
    year_data = (year_data)-(year_data['Sea Level'].mean())
    #print(year_data)
    return year_data

#Calls function
extract_single_year_remove_mean(1947, data)



# Siphones data of a specific time period from the df, and subtracts the mean from each data point
def extract_section_remove_mean(start, end, data):
  # Creates a global variable for viewing purposes
    global section_data
  # Sets start and end points of the section
    section_start = str(start)
    section_end = str(end)
  # Siphones that section from the df (https://www.codecademy.com/resources/docs/pandas/dataframe/loc)
    section_data = data.loc[section_start:section_end, ['Sea Level']]
  # Sets all data in the new df as numeric values (https://saturncloud.io/blog/calculating-averages-of-multiple-columns-ignoring-nan-a-guide-for-data-scientists/#:~:text=By%20setting%20the%20skipna%3DTrue,columns%20while%20ignoring%20NaN%20values.)
    section_data = section_data.apply(pd.to_numeric, errors='raise')
  # Calculates mean and subtracts from all data points (https://stackoverflow.com/questions/35169368/subtract-every-column-in-dataframe-with-the-mean-of-that-column-with-python)
    section_data = (section_data)-(section_data['Sea Level'].mean())
    #print(section_data)
    return section_data

#Calls function
extract_section_remove_mean(19470101, 19470815, data)



# Joins dfs along the x axis
def join_data(data1, data2):
# Creates a global variable for viewing purposes
    global joined_file
# Creates a list with the dfs
    file_dfs = [data1, data2]
# Joins the formatted files along the x axis (https://www.geeksforgeeks.org/how-to-combine-two-dataframe-in-python-pandas/)
    joined_file = pd.concat(file_dfs)
    joined_file.sort_values(by=['Datetime'], ascending=True)
    #print (joined_file)
    return joined_file



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











