# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 17:49:16 2017

@author: DIALLO_MAM
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    """
    Split the input file into separate files, each containing a single patent.
    As a hint - each patent declaration starts with the same line that was
    causing the error found in the previous exercises.
    
    The new files should be saved with filename in the following format:
    "{}-{}".format(filename, n) where n is a counter, starting from 0.
    """
    n = 0
    f1 = 0
    import os
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("<?xml"):
                # close previous file
                if (n>0):
                    #print "close file:","{}-{}".format(filename, n-1)
                    f1.close()
                # create new file
                #print "create new file:","{}-{}".format(filename, n)
                fname = "{}-{}".format(filename, n)
                f1=open(fname, 'a')
                f1.write(line + os.linesep)
                n +=1
            else:
                f1.write(line + os.linesep)
        # close last file
        print "close file:","{}-{}".format(filename, n-1)
        f1.close()
                
            


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()