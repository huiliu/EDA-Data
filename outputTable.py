#!/export/home/liuhui/opt/python3/bin/python3

import re
import sys
import math



def Distance(coord1, coord2):
    
    coord1 = [float(i) for i in coord1[1:4]]
    coord2 = [float(i) for i in coord2[1:4]]

    x = coord1[0] - coord2[0]
    y = coord1[1] - coord2[1]
    z = coord1[2] - coord2[2]

    tmp = math.hypot(x,y)
    return math.hypot(tmp, z)
        

def GetTwoBlock(blocks, block1, block2):
    return (blocks[block1], blocks[block2])

def ComputeOffset(twoblock):
    print( "-----------compute------------")
    print( twoblock[0] )
    print( "-----------compute------------")
    print( twoblock[1] )
    if len(twoblock[0]) != len(twoblock[1]):
        sys.stderr.write("two block with different size")
        sys.exit(1)
    
    length = len(twoblock[0])
    print("========="+str(length)+"==========")
    i = 0
    print("--------------split---------------")
    print(twoblock[0][0].strip().split())

    result = []
    while i < length:
       #print(twoblock[0][i])
       #print(twoblock[1][i])
       result.append( Distance(twoblock[0][i].strip().split(),twoblock[1][i].strip().split()) )
       i += 1

    return result


def PrintBlock(blocks):
    for block in blocks:
        for line in block:
            sys.stdout.write(line)
        sys.stdout.write('\n')

def SplitToBlock(lines):
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


lines = open( 'haha', 'r' ).readlines()
blocks = SplitToBlock(lines)
PrintBlock(blocks)
twoblock = GetTwoBlock(blocks, 0, 5)
print("---------------------------")
print( twoblock )
print("---------------------------")
print(ComputeOffset(twoblock ))
