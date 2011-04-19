#!/export/home/liuhui/opt/python3/bin/python3

import re
import sys
import os
import math


def GenerateTable(data):
    """
    """
    blocks = SplitToBlock(data)
    coord_r = ComputeOffset(blocks, 0, 5)
    OutputTable(coord_r[0], coord_r[1])

def OutputTable(coord, r):
    """
    OutputOffset    only output Table that contain 
                    coordination and offset
    """
    i = 0
    length = len(r)
    while i < length:
        coord[0][i] = [float(x) for x in coord[0][i][1:4]]
        coord[1][i] = [float(x) for x in coord[1][i][1:4]]
        #print(coordination[0][i][0])
        print( "%16.8f%16.8f%16.8f%16.8f%16.8f%16.8f%16.8f" \
            % (coord[0][i][0],coord[0][i][1], coord[0][i][1], \
               coord[1][i][0],coord[1][i][1], coord[1][i][2], \
               r[i]) )
        i += 1
    
def OutputOffset(offset):
    """
    OutputOffset    only output the offset
    """
    i = 0
    length = len(offset)
    while i < length:
        print( "%16.8f" % offset[i] )
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
    """
    #print( "============" + str(i) + "============" + str(j) + "=============")
    #print( blocks[0] )
    #print("===================")

    if len(blocks[i]) != len(blocks[j]):
        sys.stderr.write("two block with different size")
        sys.exit(1)

    length = len(blocks[i])
    k = 0
    coord1 = []
    coord2 = []

    while k < length: 
        coord1.append( blocks[i][k].strip().split() )
        coord2.append( blocks[j][k].strip().split() )
        k += 1
    return (coord1, coord2)

def ComputeOffset(twoblock, i, j):
    """
    """
    coordData = GetTwoBlock( twoblock, i, j )
    r = []
    length = len(coordData[0])
    i = 0
    while i < length:
        r.append( Distance(coordData[0][i], coordData[1][i]) )
        i += 1
    return (coordData, r)
    #OutputOffset( r )
    #return 1

def PrintBlock(blocks):
    for block in blocks:
        for line in block:
            sys.stdout.write(line)
        sys.stdout.write('\n')

def SplitToBlock(lines):
    """
        SplitToBlock    split the data file to block which is easy to 
                        process.
        lines           the data that is conpoud
    """
    reg = re.compile('^\s*$')
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


if __name__ == "__main__":
    if len(sys.argv) == 1 :
        print("Error! there foundn't *.tmp file.\n \
                Please Check the file exsit.")
    else:
        lines = open( sys.argv[1] , 'r' ).readlines()
        blocks = SplitToBlock(lines)
        GenerateTable(lines)