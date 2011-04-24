#!/export/home/liuhui/opt/python3/bin/python3

"""
    This File include some function that often used
"""


def ReadDataFromFile(fName):
    try:
        fData = open( fName, 'r').readlines()
    except IOError:
        print( "Failed to read \"" + fName + "\"! \n \
    Please Chech the file exsit." )
        return 1
    
    return fData
