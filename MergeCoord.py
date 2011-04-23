#!/export/home/liuhui/opt/python3/bin/python3

import glob
import sys

def merge():

    fDist = open('all_coordination.cor', 'w')
    for fName in glob.glob('./*.cor'):
        try:
            f = open(fName, 'r')
        except IOError:
            print("Failed to Open '" + fName + "'")
            sys.exit(1)
        fData = f.readlines()
        if len(fData) != 0:
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
