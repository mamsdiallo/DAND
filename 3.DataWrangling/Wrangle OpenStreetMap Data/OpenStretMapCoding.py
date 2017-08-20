# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 17:26:14 2017

@author: Mamadou DIALLO
"""

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import datetime
import numpy as np
#import cerberus

#import schema

OSM_PATH = "Nanterre.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# Pattern 1: lower case
LOWER = re.compile(r'^([a-z]|_)*$')
# Pattern 2: Lower case with colon
LOWER_COLON = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
# Pattern 3: Special caracters
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# Pattern 4: Get last word 
street_type_re = re.compile(r'\S+\.?$', re.IGNORECASE)
# Patter 5: first word of a sentence
street_type2_re = re.compile(r'^\S+',re.IGNORECASE)
street_types = defaultdict(int)

# files for fixing dates if any problem
OUTPUT_GOOD = 'dates-valid.csv'
OUTPUT_BAD = 'FIXME-dates.csv'

# files for location (lat, lon) problems
OUTPUT_GOOD_POS = 'Location-valid.csv'
OUTPUT_BAD_POS = 'FIXME-Location.csv'

'''
FUNCTION NAME: parse_firtElements

OBJECTIVE: Parse first Elements of the file

INPUT: input file

OUTPUT: None
'''
def parse_firtElements(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    count = 0
    print "root:"
    print root.tag, root.attrib

    for child in root:
        print count, ":",child.tag, child.attrib
        if count == 10:
            break
        count +=1
    #



'''
FUNCTION NAME: count_tags

OBJECTIVE: 
iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.

INPUT: input file

OUTPUT: It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.
'''
def count_tags(filename):
        # The Dictionary of the tag list in input file.
        # Initialisation
        tagsList = {}
        # scan input file
        with open(filename, "r") as f:
            # for each line
            for line in f:
                try:
                    val = line.split()[0]
                    # we do not consider the header
                    if line.startswith("<?xml"):
                        continue
                    # we do not consider the closing tag
                    elif val.startswith('</'):
                        continue
                    # get the tag
                    elif val.startswith('<'):
                        # get the tag name
                        tg = val.split('<')[1]
                        # count tag name if it already exits
                        if tg in tagsList:
                            tagsList[tg] += 1
                        # create the tag name when met the first time
                        # count set to 1
                        else:
                            tagsList[tg] = 1

                except ValueError:
                    continue

        return tagsList


'''
FUNCTION Name: key_type 

PURPOSE: count of each of four tag categories in a dictionary: 
  "LOWER", for tags that contain only lowercase letters and are valid,
  "LOWER_COLON", for otherwise valid tags with a colon in their names,
  "PROBLEMCHARS", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories. 
   
INPUT: current element (element), and keys caught (keys)

OUTPUT: dictionary of keys (keys)
'''
def key_type(element, keys):
    # catch tags
    if element.tag == "tag":
        # get value
        str = element.get('v')
        # Are there tags with problematic characters?
        if re.search(PROBLEMCHARS, str) != None:
            keys['problemchars'] += 1
            # DEBUG print "str pb:",str
        # Are there valid tags with a colon in their names?
        elif re.search(LOWER_COLON, str) != None:
            keys['lower_colon'] += 1
            # DEBUG print "str colon:",str
        # Are there tags that contain only lowercase letters and are valid?
        elif re.search(LOWER, str) != None:
            keys['lower'] += 1
            # DEBUG print "str lower:",str
        # Are there other tags that do not fall into the other 3 categories    
        else:
            keys['other'] += 1
            # DEBUG print "str other:",str
            
    return keys

"""
FUNCTION Name: get_user

PURPOSE: explore the data a bit more. find out how many unique users
have contributed to the map in this particular area!

INPUT: element
    
OUTPUT: User
"""
def get_user(element):
    user = element.get('user')
    if user != None:
        return user
    else:
        return None

'''
FUNCTION Name: audit_street_type
    
PURPOSE: 
    
    
INPUT: 

OUTPUT: None
'''
def audit_street_type(street_types, street_name):
    m = street_type2_re.search(street_name)
    if m:
        street_type = m.group()

        street_types[street_type] += 1

'''
FUNCTION Name: print_sorted_dict
    
PURPOSE: print the key and value of a dictionary
    
INPUT: the dictionary

OUTPUT: full content of the dictionary (k,v) 
'''
def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

'''
FUNCTION Name: is_street_name
    
PURPOSE: define if wether of not a it is a street type
    
INPUT: element

OUTPUT: Yes: it's a street No: not a street
'''
def is_street_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:street")

'''
FUNCTION Name: auditStreetType
    
PURPOSE: define if wether of not a it is a street type
    
INPUT: input file

OUTPUT: full content of the dictionary (k,v) 
'''
def auditStreetType(filename):
    for event, elem in ET.iterparse(filename):
        if is_street_name(elem):
            audit_street_type(street_types, elem.attrib['v'])    
    print_sorted_dict(street_types)    



'''
FUNCTION Name: process0_map 

PURPOSE: process for each element the count of the 4 types 
   
INPUT: input file

OUTPUT: dictionary of keys (keys)
'''
def process0_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    users = set()
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        user = get_user(element)
        if user != None:
            users.add(user)

    return keys, users
    #return keys #, users





"""
FUNCTION Name: get_timestamp

PURPOSE: explore the data a bit more. find out how many unique users
have contributed to the map in this particular area!

INPUT: element
    
OUTPUT: User
"""
def get_timestamp(element):
    ts = element.get('timestamp')
    if ts != None:
        return ts
    else:
        return None


"""
FUNCTION Name: validateYear

PURPOSE: check if year is valid (i.e. in format %Y-%m-%dT%H:%M:%SZ)

INPUT: element
    
OUTPUT: User
"""
def validateYear(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        #raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return False


'''
FUNCTION Name: processDates_file 

PURPOSE:  
   
INPUT: input file, output good file, output bad file

OUTPUT: files
'''
def processDates_file(input_file, output_good, output_bad):

    badRow = []
    goodRow = []
    for _, element in ET.iterparse(input_file):
        ts = get_timestamp(element)
        #print "ts",ts
        row = {'Year':None}
        if ts:
            #only_date = ts.date()
            #print "valid?",validate(ts)
            if validateYear(ts) == False:
                # write rown to the output_bad file
                row['Year'] = ts
                badRow.append(row)        
            else:                
                y = ts.split('-')[0]            
                #print y
                if y.isdigit():
                    val = int(y)
                    if ((val >= 1980)&(val<=2017)):
                        # write row to the output_good file
                        row['Year'] = val
                        #pprint.pprint(row)
                        goodRow.append(row)
                    else:
                        # write row to the output_bad file
                        row['Year'] = val
                        badRow.append(row)
                        #pprint.pprint(row)
                else:
                    # write rown to the output_bad file
                    row['Year'] = y
                    badRow.append(row)        
                    #pprint.pprint(row)

    #print "good row"
    #pprint.pprint(goodRow)
    #print "bad row"
    #pprint.pprint(badRow)             
    # This is just an example on how you can use csv.DictWriter
    # Remember that you have to output 2 files
    fieldnames = ['Year']
    with open(output_good, "wb") as g:
        writer = csv.DictWriter(g, delimiter=",",fieldnames=fieldnames)
        for row in goodRow:
            writer.writerow(row)
            #pprint.pprint(row)

    with open(output_bad, "wb") as g:
        writer = csv.DictWriter(g, delimiter=",",fieldnames=fieldnames)
        for row in badRow:
            writer.writerow(row)
            #pprint.pprint(row)


"""
FUNCTION Name: get_lat

PURPOSE: explore the data a bit more. find out latitude

INPUT: element
    
OUTPUT: User
"""
def get_lat(element):
    lat = element.get('lat')
    if lat != None:
        return lat
    else:
        return None

"""
FUNCTION Name: get_lon

PURPOSE: explore the data a bit more. find out latitude

INPUT: element
    
OUTPUT: User
"""
def get_lon(element):
    lon = element.get('lon')
    if lon != None:
        return lon
    else:
        return None


'''
FUNCTION Name: get_bounds 

PURPOSE: count of each of four tag categories in a dictionary: 
  "LOWER", for tags that contain only lowercase letters and are valid,
  "LOWER_COLON", for otherwise valid tags with a colon in their names,
  "PROBLEMCHARS", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories. 
   
INPUT: current element (element), and keys caught (keys)

OUTPUT: dictionary of the bounding box (bbox)
'''
def get_bounds(input_file):
    # catch tags
    bbox = {'minlat':None,'minlon':None,'maxlat':None,'maxlon':None}
    for _, element in ET.iterparse(input_file):
        if element.tag == "bounds":
            # get value
            strminlat = element.get('minlat')
            strminlon = element.get('minlon')
            strmaxlat = element.get('maxlat')
            strmaxlon = element.get('maxlon')
            # Are there tags with problematic characters?
            bbox['minlat'] = np.float64(strminlat)
            bbox['minlon'] = np.float64(strminlon)
            bbox['maxlat'] = np.float64(strmaxlat)
            bbox['maxlon'] = np.float64(strmaxlon)
            break
            
    return bbox


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

"""
FUNCTION Name: validateLatLon

PURPOSE: check if position is valid (i.e. within the bounding box)

INPUT: bounding box, lat, lon
    
OUTPUT: User
"""
def validateLatLon(bb,lat,lon):

    # bounding box: bb
    if isfloat(lat) == False or isfloat(lon) == False:
        return False
    elif (lat < bb['minlat']) and \
         (lat > bb['maxlat']) and \
         (lon < bb['minlon']) and \
         (lon > bb['maxlon']):
        return False
    else:
        return True

'''
FUNCTION Name: processPosition_file 

PURPOSE:  
   
INPUT: input file, output good file, output bad file

OUTPUT: files
'''
def processPosition_file(input_file, output_good, output_bad):
    
 
    badRow = []
    goodRow = []
    bounds = {}
    bounds = get_bounds(input_file)
    pprint.pprint(bounds)
    for _, element in ET.iterparse(input_file):
        lat = get_lat(element)
        lon = get_lon(element)
        #print "ts",ts
        row = {'Lat':None,'Lon':None}
        if lat and lon:
            if validateLatLon(bounds,lat,lon) == False:
                # write rown to the output_bad file
                row['Lat'] = lat
                row['Lon'] = lon
                badRow.append(row)        
            else:   
                valLat = float(lat)
                valLon = float(lon)
                row['Lat'] = valLat
                row['Lon'] = valLon
                #pprint.pprint(row)
                goodRow.append(row)

    fieldnames = ['Lat','Lon']
    with open(output_good, "wb") as g:
        writer = csv.DictWriter(g, delimiter=",",fieldnames=fieldnames)
        for row in goodRow:
            writer.writerow(row)
            #pprint.pprint(row)

    with open(output_bad, "wb") as g:
        writer = csv.DictWriter(g, delimiter=",",fieldnames=fieldnames)
        for row in badRow:
            writer.writerow(row)
            #pprint.pprint(row)
            
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    count = 0
    data = {}
    dt = {}
    if element.tag == 'node':
        node_attribs['id'] = element.attrib['id']
        node_attribs['lat'] = element.attrib['lat']
        node_attribs['lon'] = element.attrib['lon']
        node_attribs['user'] = element.attrib['user']
        node_attribs['uid'] = element.attrib['uid']
        node_attribs['version'] = element.attrib['version']
        node_attribs['changeset'] = element.attrib['changeset']
        node_attribs['timestamp'] = element.attrib['timestamp']
        #print "node_attribs:"
        #pprint.pprint(node_attribs)
        
        for sub in element:
            if sub.tag == 'tag':
                data = {
                    "id": None,
                    "key": None,
                    "value": None,
                    "type": None
                }                
                data["id"] = node_attribs['id']
                data["value"] = sub.attrib['v']
                str = sub.attrib['k']
                if re.search(PROBLEMCHARS, str) != None:
                    continue
                elif re.search(LOWER_COLON, str) != None:
                    data["type"] = str.split(":")[0]
                    data["key"] = ":".join(str.split(":")[1:])
                else:
                    data["type"] = "regular"
                    data["key"] = str

                tags.append(data)  

        #print "tags:"
        #pprint.pprint(tags)        

        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        way_attribs['id'] = element.attrib['id']
        way_attribs['user'] = element.attrib['user']
        way_attribs['uid'] = element.attrib['uid']
        way_attribs['version'] = element.attrib['version']
        way_attribs['changeset'] = element.attrib['changeset']
        way_attribs['timestamp'] = element.attrib['timestamp']
        #print "way_attribs:"
        #pprint.pprint(way_attribs)

        for sub in element:
            if sub.tag == 'nd':
                dt = {
                    "id": None,
                    "node_id": None,
                    "position": []
                }                
                dt["id"] = way_attribs['id']
                dt["node_id"] = sub.attrib['ref']
                dt["position"] = count
                count +=1
                way_nodes.append(dt) 
            
            if sub.tag == 'tag':
                data = {
                    "id": None,
                    "key": None,
                    "value": None,
                    "type": None
                }                
                data["id"] = way_attribs['id']
                data["value"] = sub.attrib['v']
                str = sub.attrib['k']
                if re.search(PROBLEMCHARS, str) != None:
                    continue
                elif re.search(LOWER_COLON, str) != None:
                    data["type"] = str.split(":")[0]
                    data["key"] = ":".join(str.split(":")[1:])
                else:
                    data["type"] = "regular"
                    data["key"] = str

                tags.append(data)  

        #print "tags:"
        #pprint.pprint(tags)

        #print "way_nodes:"
        #pprint.pprint(way_nodes)   

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
'''
def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))
'''        
        
class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

            
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    # TIP: use of wb instead of w for avoiding blank line.
    # ISSUE with utf-8 encoding -> ANSI
    with codecs.open(NODES_PATH, mode='wb') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, mode='wb') as nodes_tags_file, \
         codecs.open(WAYS_PATH, mode='wb') as ways_file, \
         codecs.open(WAY_NODES_PATH, mode='wb') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, mode='wb') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        #validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
#                if validate is True:
#                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

            
# ================================================== #
#               Main Function                        #
# ================================================== #
def test():
    
    # Parsing the map file
    # First elements
    #parse_firtElements(OSM_PATH)
    #tags = count_tags(OSM_PATH)
    #print "PARSING:"
    #pprint.pprint(tags)
    # Check the k value for each tag
    # check the number of users
    #keys, users  = process0_map(OSM_PATH)
    #print "CHECK K VALUES:"
    #pprint.pprint(keys)
    #print "CHECK USERS:"
    #pprint.pprint(users)
    #print "streets:"
    #auditStreetType(OSM_PATH)
    #print "dates"
    #processDates_file(OSM_PATH, OUTPUT_GOOD, OUTPUT_BAD)
    #print "positions"
    #processPosition_file(OSM_PATH, OUTPUT_GOOD_POS, OUTPUT_BAD_POS)
    print "processing"
    process_map(OSM_PATH, validate=True)
    
    
if __name__ == "__main__":
    test()
