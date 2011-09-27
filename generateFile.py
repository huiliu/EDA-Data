#!/export/home/liuhui/opt/bin/python3
# -*- coding: UTF-8 -*-

import sys
import common

#This var use to store the file head part
FileHead=""

def GenerateFile( filename ):
    """
        GenerateFile        read coordination data and other necessary
                            data, finally, generate Series input file.
            filename        the name of template file. the structure 
                            of this file:
                            e.g.
    """
    try:
        f = open( filename, 'r' ).readlines()
    except IOError:
        print( "Failed open the file '" + sys.argv[1] + "'." ) 
        print( "Please check it exsit!" )
        sys.exit(1)
    
    data = common.SplitToBlock( f )
    FileHead = data[1]
    length = len( data )
    fName = GenerateFileName( data[0], length - 2 )
    fType = fName[-1]

    i = 2
    while i < length:
        WriteToFile( fName[i-2], FileHead,  data[i], fType )
        i += 1

    sys.exit(0)

def fWrite( f, head, name, data, end ):
    """

    """
    try:
        f.writelines( head )
        f.writelines(data) 
        f.write(end)
        f.close()
    except IOError:
        print("Failed to write data.")
        sys.exit(1)

def WriteToFile( fName, fHead, data, f_type ):
    """

    """
    # Write EDA input file.
    try:
        outputFile = open( fName, 'w' )
    except IOError:
        print("Failed to Create file.")
        sys.exit(1)

    #Need to Modify, we just judge create GAMESS or GAUSSIAN input file
    if f_type == "gms":
        fWrite(outputFile, fHead, fName, data, " $end")
    elif f_type == "gau":
        fWrite(outputFile, fHead, fName, data, "\n\n")
    else:
        print("I am not God! I cann't generate this type of file.\n \
    I just can generate GAMESS or GAUSSIAN input file.")
        sys.exit(1)

def CheckTitle( data, num):
    d = data.split(" ")
    if len(d) < num:
        print("You input file has error! Please Check it.")
        sys.exit(1)
    return d

def GenerateFileName( fileInfo, k ):
    """
        GenerateFileName        generate the file name
            fileInof            contain some information that use to
                                generate file name
                                "Prefix startNum EndNum StepNum 
                                filetype(gms/gau) suffix"
            k                   the number of coordination group
    """
    Name = []

    tmp = fileInfo[0]
    Info = CheckTitle( tmp, 6 )

    suffix = ""
    start = int(Info[1])
    end = int(Info[2])
    step = int(Info[3])

    if Info[4] == 'gms':
        suffix = '.inp'
    elif Info[4] == 'gau' :
        suffix = '.com'

    if k != int(( end - start ) / step + 1 ):
        print("The input File have error. Please check it.")
        sys.exit(1)

    for x in range(start, end + 1, step):
        Name.append( Info[0] + str(x) + "-" + Info[5][:3] + suffix)

    Name.append( Info[4] )
    return Name

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(" generateFile <InputFileName>")
    else:
        GenerateFile( sys.argv[1] )
