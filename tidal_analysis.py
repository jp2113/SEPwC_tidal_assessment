#!/usr/bin/env python3

# import the modules you need here
import argparse
import numpy as np
import pandas as pd
#import glob

filename1 = "data/1946ABE.txt"
filename2 = "data/1947ABE.txt"


# Opens a specified file, formats columns as needed, and removes uneeded data
def read_tidal_data(filename):
    
  # Creates a gloobal variable 
    global data
  # Removes unneeded data - 
    data = pd.read_csv(filename , sep=r"\s+", skiprows=[0,1,2,3,4,5,6,7,8,10])
  # Amalgamates the Date and Time column into one
    data["Datetime"] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
  # Renames column to 'Sea Level'
    data = data.rename(columns={data.columns[3] : 'Sea Level'})
  # Removes uneeded columns (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html)
    data = data.drop(columns = ['Date','Time'])
  # Replaces any value containing M,N,T with NaN, in the 'Sea Level' column
    data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True, inplace=True)
    #print(data)
    
    return(data)

read_tidal_data(filename2)





# Reads and formats the two dfs, and joins them along the x axis
def join_data(data1, data2):
    
# Creates a global variable for viewing purposes
    global joined_file
# Formats the files ready for joining
    format_1 = read_tidal_data(data1)
    format_2 = read_tidal_data(data2)
    files = [format_1, format_2]
# Joins the formatted files along the x axis (https://www.geeksforgeeks.org/how-to-combine-two-dataframe-in-python-pandas/)
    joined_file = pd.concat(files)
    #print (joined_file)

    return joined_file

join_data(filename1, filename2)



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











