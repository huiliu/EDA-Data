#!/export/home/liuhui/opt/python3/bin/python3

"""
    This File include some function that often used
"""

import re

def ReadDataFromFile(fName):
    """
        ReadDataFromFile        read data from file 'fName' and return
                                an list contain all lines in the file
                fName           the file name
    """
    try:
        fData = open( fName, 'r').readlines()
    except IOError:
        print( "Failed to read \"" + fName + "\"! \n \
    Please Chech the file exsit." )
        return 1
    
    return fData

def SplitToBlock(lines, regular='^\s*$'):
    """
        SplitToBlock    split the data file to block which is easy to 
                        process.
        lines           the data that is conpoud
    """
    reg = re.compile(regular)
    result = []
    block = []
    i = 0
    length = len(lines)

    while i < length:
        if reg.match(lines[i]) is None:
            block.append(lines[i])
            i += 1
        else:
            if block != []:
                result.append(block)
            while i < length and reg.match(lines[i]) :
                i += 1
            block = []

    return result
