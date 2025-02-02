# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 21:05:31 2017

@author: Diallo
"""

# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook('{0}.xls'.format(datafile))
    sheet = workbook.sheet_by_index(0)
    data = None
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    data = {}

    stations = sheet.row_values(rowx=0,start_colx=1,end_colx=-1)
    maxvalue = []
    timevalue = []
    # "Number of rows in the sheet:", 
    ncols = sheet.ncols    
    for j in range(1,ncols-1):
        cur_col = sheet.col_values(j, start_rowx=1, end_rowx=None)
        max1 = max(cur_col)
        maxvalue.append(max1)
        n1 = cur_col.index(max1)
        maxtime = sheet.cell_value(n1+1,0)
        tm = xlrd.xldate_as_tuple(maxtime, 0)
        timevalue.append(tm)
    
    data['Station'] = stations
    data['Max Load'] = maxvalue
    data['time'] = timevalue
    
    return data

def save_file(data, filename):
    # YOUR CODE HERE\n
    keys = ['Station','Max Load','Year','Month','Day','Hour']
    with open('2013_Max_Loads.csv','wb') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys,delimiter='|')
        dict_writer.writeheader()
        Stations = data['Station']
        MaxLoad = data['Max Load']
        time = data['time']
        
        for i in range(len(Stations)):
            tm = time[i]
            dict_writer.writerow({'Station': Stations[i].strip(), \
                                  'Max Load': MaxLoad[i], \
                                  'Year':tm[0],'Month':tm[1],\
                                  'Day': tm[2],'Hour':tm[3]})
    
    import unicodecsv
    with open('2013_Max_Loads.csv', 'rb') as f:
        reader = unicodecsv.DictReader(f)
        loads = list(reader)
    
    print loads
    
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
