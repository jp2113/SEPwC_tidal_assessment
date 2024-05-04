#!/usr/bin/env python3

# import the modules you need here
#import argparse
import numpy as np
import pandas as pd
import glob

def read_tidal_data(filename):
    #Reads the data in, seperates the columns by spaces, skips rows 0-10, and adds in appropriate names for each row
    #References: https://geo-python-site.readthedocs.io/en/latest/notebooks/L5/exploring-data-using-pandas.html
    data = pd.read_csv(filename, sep=r'\s+', skiprows=[0,1,2,3,4,5,6,7,8,9,10],names =['Cycle', 'Date', 'Time', 'Sea Level', 'Residual'])
    data['datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    #Combines columns 'date' and 'time', to form datetimes variable
    data['datetime'] = pd.to_datetime(data['Date'] + " " +  data['Time'])
    #Adds in a seperate row for the new variable 'datetime'
    data = data.set_index('datetime')

    

    return data


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

#station =input("Which station would you like to use? Aberdeen, Whitby, or Dover: ")
#path = '/Users/joshuaproctor/Documents/SEPwC_tidal_assessment/data/' + (station)
#files = glob.glob(path + '/*.txt')
#for f in files:
#    print (read_tidal_data(f))
   
    


#if __name__ == '__main__':
   # parser = argparse.ArgumentParser(
       #              prog="UK Tidal analysis",
        #             description="Calculate tidal constiuents and RSL from tide gauge data",
         #            epilog="Copyright 2024, Jon Hill"
          #           )
    #parser.add_argument("directory",
     #               help="the directory containing txt files with data")
    #parser.add_argument('-v', '--verbose',
     #               action='store_true',
      #              default=False,
       #             help="Print progress")
    #args = parser.parse_args()
    #dirname = args.directory
    #verbose = args.verbose


