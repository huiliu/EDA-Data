#!/bin/env python3

import re
import sys
from pprint import pprint

def GetIntegral( fName, orb_No):
    
    orb1 = []
    orb2 = []

    try:
        f = open( fName , 'r' )
    except IOError:
        print( 'Failed to open "' + fName + '".' )
        sys.exit(1)

    #if the line start withc '  orb_no      1    '
    orb1_reg_new  = re.compile('^\s*' + str(orb_No[0]) + ' {4,5}1 ')
    orb1_reg = re.compile('^\s*' + str(orb_No[0]) + ' {4,5}[1-9]{1,2}')
    orb2_reg_new  = re.compile('^\s*' + str(orb_No[1]) + ' {4,5}1 ')
    orb2_reg = re.compile('^\s*' + str(orb_No[1]) + ' {4,5}[1-9]{1,2}')
    reg_split = re.compile(' *')
    
    tmp1 = []
    tmp2 = []
    for line in f:
        if orb1_reg_new.match(line):
            if tmp1:
                orb1.append( tmp1 )
                tmp1 = []
            elif tmp2:
                orb2.append( tmp2 )
                tmp2 = []
            tmp1.append( reg_split.split( line )[1:] )
        elif orb1_reg.match(line):
            tmp1.append( reg_split.split( line )[1:] )
        elif orb2_reg_new.match(line):
            if tmp1:
                orb1.append( tmp1 )
                tmp1 = []
            elif tmp2:
                orb2.append( tmp2 )
                tmp2 = []
            tmp2.append( reg_split.split( line )[1:] )
        elif orb2_reg.match(line):
            tmp2.append( reg_split.split( line )[1:] )

    return ( orb1, orb2 )

def ComputeVariation( origin_data ):
    orb1 = origin_data[0]
    orb2 = origin_data[1]

    variation1 = []
    variation2 = []

    print( orb1[0] )
    print( orb1[4] )
    i = 0
    length = len( orb1 )
    while i < length:
        variation1.append( orb1[0][i] - orb1[4][i] )
        variation2.append( orb2[0][i] - orb2[4][i] )
    print( len(orb1) )
    pprint( variation1 )
    pprint( variation2 )
    #print( orb1[1] )
    #print( orb1[3] )

if __name__ == "__main__":
    #GetIntegral( 'fix1600-eda-mp2.out', [17, 25] )[0]
    ComputeVariation( GetIntegral( 'fix1600-eda-mp2.out', [17, 25] ) )

