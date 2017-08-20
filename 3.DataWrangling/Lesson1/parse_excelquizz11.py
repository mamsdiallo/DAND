# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 23:54:21 2017

@author: Diallo
"""

#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format

"""

import xlrd
from zipfile import ZipFile
datafile = "2013_ercot_hourly_load_data"

def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook('{0}.xls'.format(datafile))
    sheet = workbook.sheet_by_index(0)

    ### example on how you can get the data
    #sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

    ### other useful methods:
    # print "\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:", 
    # print sheet.nrows
    # print "Type of data in cell (row 3, col 2):", 
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):", 
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    # print sheet.col_values(3, start_rowx=1, end_rowx=4)

    # print "\nDATES:"
    # print "Type of data in cell (row 1, col 0):", 
    # print sheet.cell_type(1, 0)
    # exceltime = sheet.cell_value(1, 0)
    # print "Time in Excel format:",
    # print exceltime
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    # print xlrd.xldate_as_tuple(exceltime, 0)
    
    
    data = {
            'maxtime': (0, 0, 0, 0, 0, 0),
            'maxvalue': 0,
            'mintime': (0, 0, 0, 0, 0, 0),
            'minvalue': 0,
            'avgcoast': 0
    }

#    import numpy as np

    sheet_data = [[sheet.cell_value(r, col) 
                for col in range(sheet.ncols)] 
                    for r in range(sheet.nrows)]

    # "Number of rows in the sheet:", 
    nrows = sheet.nrows
    print "------------------------"
    
    # "Get a slice of values in column 3, from rows 1-3:"
    coast = sheet.col_values(1, start_rowx=1, end_rowx=None)
    tm = sheet.col_values(0, start_rowx=1, end_rowx=None)    
    
    data['maxvalue'] = max(coast)
    data['minvalue'] = min(coast)
    data['avgcoast'] = sum(coast)/float(len(coast))
    n1 = coast.index(max(coast))
    maxtime = tm[n1]
    data['maxtime'] = xlrd.xldate_as_tuple(maxtime, 0)
    n2 = coast.index(min(coast))
    mintime = tm[n2]
    data['mintime'] = xlrd.xldate_as_tuple(mintime, 0)
    
    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)
    import pprint
    
    pprint.pprint(data)
    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()