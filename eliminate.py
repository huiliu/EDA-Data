#!/export/home/liuhui/opt/bin/python3

"""
    This script use to handle the lcd file which contain "*"
    The input file is lcd file
"""

import common
import sys
import re
from pprint import pprint

def getCoord( fName ):
    #read data from the file which contain '*', and split to list
    data = common.SplitToBlock( common.ReadDataFromFile(fName) )

    #get coordination
    refined_Coord = []
    # Use regular expression to match the coordiantion ofLCD
    reg = re.compile(' DU ')
    for x in data :
        for y in x:
            if reg.match( y ):
                refined_Coord.append( x )
                break
    return refined_Coord

def Cut( coordBlock ):
    """
        Cut             delete the string "DU"
    """
    tmp = []
    block = []

    for  larray in coordBlock:
        for x in larray:
            #tmp.append( x.strip().split()[1:] )
            tmp.append( x.strip().split() )
        block.append( tmp )
        tmp =[]
    return block

def Adjust( org, comp ):
    correct = org
    for x in correct:
        for z in  comp:
            if x[1] == z[1] or x[3] == z[3]:
                x[1] = z[1]
                x[2] = z[2]
                x[3] = z[3]
    #           x[0] = float(x[0])
    #           x[1] = float(x[1])
    #           x[2] = float(x[2])
    return correct

def refine( fName ):

    lcd_coord = Cut( getCoord( fName ) )

    supermolecule = lcd_coord[4]
    monomer1 = lcd_coord[5]
    monomer2 = lcd_coord[6]

    lcd_coord[5] = Adjust( monomer1, supermolecule )
    lcd_coord[6] = Adjust( monomer2, supermolecule )
#   pprint( lcd_coord )
    out(lcd_coord)

def out(coord):
    for x in coord:
        for y in x:
            for z in y:
                print( z.center(12), end='' )
            print()
        print()


if __name__ == '__main__':
#   print(sys.argv[1])
    refine( sys.argv[1] )
