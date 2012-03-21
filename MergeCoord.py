#!/bin/env python3
# -*- coding: UTF-8 -*-

import glob
import sys
import common

def merge():

    fDist = open('all_coordination', 'w')

    for fName in glob.glob('./*.cor'):
        fData = common.ReadDataFromFile( fName )
        if len(fData) != 0:
            print( fName )
            fDist.write(fName[2:] + "\n")
            fDist.writelines(fData)
        else:
            print("\"" + fName + "\" is empty!")
        fDist.close

    fDist.close()

    print("I have done the work! Please Chech it.")
    sys.exit(0)


if __name__ == "__main__":
    merge()
