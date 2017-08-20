# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:06:46 2017

@author: DIALLO_MAM
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the
"areaLand" field, you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it
has to return a float representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you
like, but changes to process_file will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint

CITIES = 'cities2.csv'

 

def fix_area(area):

    # YOUR CODE HERE
    import numpy as np 
    def count_letters(word):
        return len(word) - word.count(' ')
        
    if (area=='NULL'):
        return None
    elif area.startswith('{'):
        t = area.split('|')
        part1 = t[0][1:]
        part2 = t[1][:-1]
        n1 = count_letters(part1)
        n2 = count_letters(part2)
        part1 = np.float64(part1)
        part2 = np.float64(part2)
        if (n1>=n2):
            return part1
        else:
            return part2
    else:
        return np.float64(area)


def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    assert data[3]["areaLand"] == None        
    assert data[8]["areaLand"] == 55166700.0
    assert data[20]["areaLand"] == 14581600.0
    assert data[33]["areaLand"] == 20564500.0    


if __name__ == "__main__":
    test()