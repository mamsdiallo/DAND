# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 14:06:59 2017

@author: DIALLO_MAM
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1": set([type(float()), type(int()), type(str())]),
 "field2": set([type(str())]),
  ....
}
The type() function returns a type object describing the argument given to the 
function. You can also use examples of objects to create type objects, e.g.
type(1.1) for a float: see the test function below for examples.

Note that the first three rows (after the header row) in the cities.csv file
are not actual data points. The contents of these rows should note be included
when processing data types. Be sure to include functionality in your code to
skip over or detect these rows.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}

    # YOUR CODE HERE
    # initialise fildtypes
    for field in FIELDS:
        fieldtypes[field] = set()
    
    # Test
    ##pprint.pprint(fieldtypes)
    #print "None type",type(None)
    #print "1.1 type",type(1.1)
    #print "[] type",type([])
    # Test
    count = 0
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        # Test
        print header
        # for each row
        
        for row in reader:
            # for each field
            for field in FIELDS:
                val = row[field]
                if count == 0:
                    #get name
                    t = val.split('/')
                    #print "variable name:",t[-1]
                    continue
                elif(count == 1):
                    # get type expected
                    t = val.split('#')[-1]
                    #print "expected type:",t
                    if (t=='string'):
                        fieldtypes[field].add(type("string"))
                    elif(t=='double'):
                        fieldtypes[field].add(type(1.1))                        #
                    elif(t=='float'):
                        fieldtypes[field].add(type(1.1))
                    elif(t=='nonNegativeInteger'):
                        fieldtypes[field].add(type(10))
                    elif(t=='Thing'):
                        fieldtypes[field].add(type("Thing"))
                    else:
                        print "type not found"
                    continue
                elif(count == 2):
                    continue
                else:
                    val = row[field]
                    #expectedType = fieldtypes[field][0]
                    tp = type(val)
                    #if (field == "areaLand"):
                    #print "field:",field,"type:",tp,"val:",val
                    #fieldtypes[field].append(tp)
                    try:
                        if val is None:
                            #print "1.None field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type(None))
                        elif val.startswith('{'):
                            #print "LIST field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type([]))                                
                        elif (val=='NULL'):
                            ##print "2. NULL field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type(None))
                        elif (val.isdigit()):
                            #print "3.integer field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type(1))
                        elif (val.find(".") > 0):
                            #print "Decimal field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type(1.1))
                        elif(val.find("e+") > 0):
                            #print "float field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type(1.1))
                        elif (val is str):
                            #print "STR field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type("string"))
                        elif (not val):
                            #print "Empty string field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type(None))
                        else:
                            #print "Not found NONE field:",field,"type:",tp,"val:",val
                            fieldtypes[field].add(type("string"))
                    except ValueError:
                        #print "Error NONE field:",field,"type:",tp,"val:",val
                        fieldtypes[field].add(type(None))
                    #print "----"
                        
            #if count > 300:
            #    break
            #print "------------------------------"
            count +=1

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
