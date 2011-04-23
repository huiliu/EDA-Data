#!/export/home/liuhui/opt/python3/bin/python3

"""
    This file use to compute the offset of LCD Diple.
    You must offer the data file which contain all LMO doroids 
    coordination and seperate every parts with blank line.

    Group 1     Monomer 1 with own basis
    Group 2     Monomer 2 with own basis
    Group 3     Monomer 1 with all basis
    Group 4     Monomer 2 with all basis
    Group 5     super molecular with all basis
    Group 6     Monomer 1 super molecular own basis
    Group 7     Monomer 2 super molecular own basis
    Group 8     MONOMER ELECTROSTATIC INTERACTION (OWN BASIS)
    Group 9     MONOMER ELECTROSTATIC INTERACTION (ALL BASIS)
    Group 10    MONOMER EXCHANGE-REPULSION INTERACTION (OWN BASIS)
    Group 11    MONOMER EXCHANGE-REPULSION INTERACTION (ALL BASIS)

"""

import re
import sys
import os
import math

def OutputTable(coord, r):
    """
    OutputOffset    only output Table that contain 
                    coordination and offset
    coord           the origin coordination
    r               the offset value
    """
    i = 0
    length = len(r)
    while i < length:
        coord[0][i] = [float(x) for x in coord[0][i][1:4]]
        coord[1][i] = [float(x) for x in coord[1][i][1:4]]
        #print(coordination[0][i][0])
        print( "%11.6f%11.6f%11.6f%11.6f%11.6f%11.6f%11.6f" \
            % (coord[0][i][0],coord[0][i][1], coord[0][i][1], \
               coord[1][i][0],coord[1][i][1], coord[1][i][2], \
               r[i]) )
        i += 1
    
def OutputOffset(offset):
    """
    OutputOffset    only output the offset
                    this function does not use
    """
    i = 0
    length = len(offset)
    while i < length:
        print( "%11.6f" % offset[i] )
        i += 1

def Distance(coord1, coord2):
    """
        Distance    compute the distance between point 1 which 
                    coordination is coord1 with point 2 which 
                    coordination is coord2. 
        coord1      the coordination of point 1
        coord2      the coordination of point 2
    """
    rr = []
    i = 1
    while i < 4:
        rr.append( float(coord1[i]) - float(coord2[i]))
        i += 1

    return math.sqrt( rr[0]*rr[0] + rr[1]*rr[1] + rr[2]*rr[2] )
        
def GetTwoBlock(blocks, i, j):
    """
        GenerateTable   get the block that you need
        block           all the origin coordination
        i               the first you need
        j               the second you need
    """

    if len(blocks[i]) != len(blocks[j]):
        print("two block with different size")
        sys.exit(1)

    length = len(blocks[i])

    k = 0
    coord1 = []
    coord2 = []

    while k < length: 
        coord1.append( blocks[i][k].strip().split() )
        coord2.append( blocks[j][k].strip().split() )
        k += 1
    #print(coord1)
    return (coord1, coord2)

def ComputeOffset(twoblock, i, j):
    """
        ComputeOffset   compute the distance between coordination 1 with coordination 2
        i               the first you need
        j               the second you need
    """
    coordData = GetTwoBlock( twoblock, i, j )
    r = []
    length = len(coordData[0])
    i = 0
    while i < length:
        r.append( Distance(coordData[0][i], coordData[1][i]) )
        i += 1
    return (coordData, r)

def PrintBlock(blocks):
    """
        
    """
    for block in blocks:
        for line in block:
            sys.stdout.write(line)
        sys.stdout.write('\n')

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

def GenrateOwn(coord):
    """
        Generateown     output the origin coordination and the offset
        Data            the all origin coordination which may be 
                        contain eleven group.
    """
    print( "-" * 77 )
    coord_r = ComputeOffset(coord, 0, 5)
    #coord_r = ComputeOffset(blocks, 0, 5)
    OutputTable(coord_r[0], coord_r[1])
    print()
    coord_r = ComputeOffset(coord, 1, 6)
    #coord_r = ComputeOffset(blocks, 1, 6)
    OutputTable(coord_r[0], coord_r[1])
    #GenerateTable(coord)

def GenerateReport(data):
    """
        GenerateReport   output the origin coordination and the offset
        Data            the all origin coordination which may be 
                        contain eleven group.
    """
    GenrateOwn(data)
    #GenrateAll(data)

if __name__ == "__main__":
    n = len(sys.argv)
    if n == 1 :
        print("Input error!\nPlease type in -h or --help")
        sys.exit(1)
    f_name = sys.argv[1]
    if (f_name == '-h' or f_name == '--help'):
        print(" \
        -h --help   get help information\n \
        filename    The coordination data that you want to compute\n \
                    offset you can use another command(lcd refine)\n \
                     to generate the file.\n \
        own         compute the offset of coordination come from \n \
                    the own basis . default own\n \
        all         compute all data. in processing.\n \
        ")
    else:
        try:
            lines = open( f_name , 'r' ).readlines()
        except IOError:
            print( "Open the file " + f_name + " error.\n \
                    Please check the file exsit. ")
            sys.exit(1)

        #global var
        blocks = SplitToBlock(lines)
        
        if n == 2:
            GenrateOwn( blocks )
            sys.exit(0)
        elif sys.argv[2] == "all":
            GenerateReport(blocks)
            sys.exit(0)
        else:
            print( "Input command error! Please type in -h/ check")
            sys.exit(1)
