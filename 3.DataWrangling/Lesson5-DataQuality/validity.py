# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 13:13:08 2017

@author: DIALLO_MAM
"""

"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in the range as described above,
  write that line to the output_good file
- if the value of the field is not a valid year as described above, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        #COMPLETE THIS FUNCTION
        badRow = []
        goodRow = []
        for row in reader:
            dt = row['productionStartYear']
            uri = row['URI']
            if (uri.startswith( 'http://dbpedia.org' ) == False):
                # skip row
                continue
            
            y = dt.split('-')[0]
            #print y
            if y.isdigit():
                val = int(y)
                if ((val >= 1886)&(val<=2014)):
                    # write row to the output_good file
                    row['productionStartYear'] = val
                    goodRow.append(row)
                else:
                    # write row to the output_bad file
                    badRow.append(row)
            else:
                # write rown to the output_bad file
                badRow.append(row)        
             
    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    with open(output_good, "wb") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in goodRow:
            writer.writerow(row)
            #pprint.pprint(row)

    with open(output_bad, "wb") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        for row in badRow:
            writer.writerow(row)
            pprint.pprint(row)

def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()