"""Module providing a tidal analysis on imported text files"""

#!/usr/bin/env python3

# import the modules you need here
import datetime
import argparse
import glob
from scipy.stats import linregress
import matplotlib.dates as base_date
import uptide
import pandas as pd
import numpy as np


def read_tidal_data(filename):
    """Opens specified file, formats the columns as needed, and removes any uneeded data"""
# Reads in a dataframe and removes uneeded rows
# (https://stackoverflow.com/questions/23810367/ignore-character-while-importing-with-pandas)
    data = pd.read_csv(filename, sep = r"\s+", skiprows = [0,1,2,3,4,5,6,7,8,10])
# Renames column to 'Sea Level'
# (https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas)
    data = data.rename(columns = {data.columns[3] : 'Sea Level'})
# Amalgamates the Date and Time column into one
# (https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)
    data["Datetime"] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
# Removes uneeded columns
# (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html)
    data = data.drop(columns = ['Date', 'Cycle', 'Residual'])
# Replaces any value containing M,N,T with NaN, in the 'Sea Level' column
# (https://jhill1.github.io/SEPwC.github.io/)
    data.replace(to_replace =".*M$", value={"Sea Level" : np.nan}, regex=True, inplace=True)
    data.replace(to_replace =".*N$", value={"Sea Level" : np.nan}, regex=True, inplace=True)
    data.replace(to_replace =".*T$", value={"Sea Level" : np.nan}, regex=True, inplace=True)
# Changes Sea Level data to float variable type
# (https://sentry.io/answers/change-a-column-type-in-a-dataframe-in-python-pandas/)
    data["Sea Level"]=data["Sea Level"].astype(float)
    return data


def extract_single_year_remove_mean(year, data):
    """Siphones data of a specific year from the df, and subtracts the mean from each row"""
# Sets start and end points of the year
    year_string_start = str(year) + "0101"
    year_string_end = str(year) + "1231"
# Siphones that year from the data frame
# (https://www.codecademy.com/resources/docs/pandas/dataframe/loc)
    year_data = data.loc[year_string_start:year_string_end, ['Sea Level']]
# Sets all data in the new data frame as numeric values
    year_data = year_data.apply(pd.to_numeric)
# Calculates mean and subtracts from all data points
    year_data = (year_data)-(year_data['Sea Level'].mean())
    return year_data


def extract_section_remove_mean(start, end, data):
    """Siphones data of a specific section from the df, and subtracts the mean from each row"""
# Sets start and end points of the section
    section_start = str(start)
    section_end = str(end)
# Siphones that section from the data frame
# (https://www.codecademy.com/resources/docs/pandas/dataframe/loc)
    section_data = data.loc[section_start:section_end, ['Sea Level']]
# Sets all data in the new data frame as numeric values
    section_data = section_data.apply(pd.to_numeric)
# Calculates mean and subtracts from all data points
    section_data = (section_data)-(section_data['Sea Level'].mean())
    return section_data


def join_data(data1, data2):
    """Joins data frames along the x axis in chronological order"""
# Joins the formatted files along the x axis
# (https://www.geeksforgeeks.org/how-to-combine-two-dataframe-in-python-pandas/)
    join_file = pd.concat([data1, data2])
# Sets the files in chronological order
# (https://pandas.pydata.org/docs/user_guide/merging.html)
    join_file = join_file.sort_values(by='Datetime', ascending=True)
    return join_file


def sea_level_rise(data):
    """Creates Sea Level on date2num for 1970"""
# Drops all null values in the subset
# (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html)
    data = data.dropna(subset=["Sea Level"])
# Records numer of days since the epoch
    x = base_date.date2num(data.index)
# Gathers the value only data from the subset
    y = data['Sea Level'].values
# Returns the p-value corresponding to the slope
# (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html)
    slope, _intercept, _r, p, _std_err = linregress(x,y)
    return slope, p


def tidal_analysis(data, constituents, start_datetime):
    """Completes Tidal analysis from constituents of amplitudes and time periods"""
# Drops all null values in the subset
# (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html)
    data = data.dropna(subset=["Sea Level"])
    tide = uptide.Tides(constituents)
# Gathers data as seconds from start_datetime
# (https://docs.python.org/3/library/datetime.html)
    tide.set_initial_time((start_datetime))
    seconds_since = (data.index.astype('int64').to_numpy()/1e9) - (start_datetime).timestamp()
# Tidal analysis to return amp, and pha for subset at specific number of seconds from epoch
    amp,pha = uptide.harmonic_analysis(tide, data['Sea Level'].to_numpy(), seconds_since)
    return amp, pha


def get_longest_contiguous_data(filename):
    """"Finds the index positions of the boundaries of the largest NaN stretch"""
# adding a pad with np.nan
    filename = np.append(np.nan, np.append(filename, np.nan))
# finds where the null values are
    w = np.where(np.isnan(filename))[0]
# finds length of nan value stretches, and finds the largest one
    a = np.diff(w).argmax()
# returns indeces of the boundary positions of the largest stretch
    return w[[a, a + 1]] + np.array([0, -2])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     epilog="Copyright 2024, Joshua Proctor"
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


# Uses the glob module to pull in all the txt files in a directory given by the user
    all_files = glob.glob(str(dirname) + "/*.txt")


# Creates empty list to append to further on
    formatted_files = []
# Iterates over the files, calling the read_tidal_data function to format the data,
# and appends to list
    for file in all_files:
        format_file = read_tidal_data(file)
        formatted_files.append(format_file)


# Creates full_file - holding the joined data from the first two files in the directory
    full_file = join_data(formatted_files[0], formatted_files[1])

# Creates a counter to iterate the correct amount of times
    COUNTER = 0

# Iterates over the rest of the files, joining each file to full_file
    while COUNTER < (len(formatted_files)):
        full_file = join_data(full_file, formatted_files[COUNTER])
        COUNTER = COUNTER + 1


# Outputs only the station name from the pathway given by user
    DIRECTORY = str(dirname)
    DIRECTORY = DIRECTORY[5:]
    print("---------------------")
    print ("Station Name: " + (DIRECTORY))


# Outputs the Sea Level Rise - p stat in metres based on directory
    print ("--------------------")
    print ("Sea Level Rise (m): ")
    print (sea_level_rise(full_file)[1])


# Outputs only the amplitude of the M2 tidal analaysis
    print ("--------------------")
    print ("M2 amplitude (m): ")
    M2 = str(tidal_analysis(full_file, ['M2'], (datetime.datetime(2000,1,1,0,0,0))))
    print (M2[8:13])


# Outputs only the amplitude of the S2 tidal analaysis
    print ("--------------------")
    print ("S2 Amplitude in (m): ")
    S2 = str(tidal_analysis(full_file, ['S2'], (datetime.datetime(2000,1,1,0,0,0))))
    print (S2[8:13])


# Drops the time column (already have info in index)
    full_file = full_file.drop(columns = ['Time'])


# Calls the contiguous data function to get boundary indeces of longest contiguous data
# Formats the returned data, to then output the longest contiguous dataset w/t NaNs
    print ("--------------------")
    print ("Longest contiguous data: ")
    print (" ")
    df = full_file['Sea Level']
    range_df = get_longest_contiguous_data(df)
    RANGE_DF_STR = str(range_df)
    RANGE_DF_STR = RANGE_DF_STR [1:-1]
    RANGE_DF_STR = RANGE_DF_STR.split()
    start_df = int(RANGE_DF_STR[0])
    end_df = int(RANGE_DF_STR[1])
    print (full_file[start_df:end_df])
    print("---------------------")
