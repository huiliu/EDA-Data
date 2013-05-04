#!/bin/env python3
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
# ---------------------------
# 输入文件模板
#
# 以空行来分割块，空行只有换行符,没有多余空格
# ---------------------------

# 下面为第一行，亦为第一块，包括六个必需字段：

 ---------------- 文件前缀，一般用于描述是什么体系
 |
 |   ------------ 原意为坐标start, end, step，可以自由定义。它们也定义了
 |   | | |        坐标块数，即生成的文件数。
 |   | | |
 |   | | |  ----- 说明生成的输入文件类型。gms为GAMESS输入文件，后缀为inp
 |   | | |  |     gau说明生成GAUSSIAN输入文件，后缀为com
 |   | | |  |
 |   | | |  |   - 自由定义的标签符，如说明体系特点等
 |   | | |  |   |
2h2o 1 9 1 gms homo

# 第二块为输入文件的头部，此处为GAMESS计算PCM-EDA的示例
 $CONTRL SCFTYP=RHF RUNTYP=eda ICHARG=0 ispher=1 mplevl=2 $end
 $LMOEDA MATOM(1)=3 3 MCHARG(1)=0 0 MMULT(1)=1 1 $END
 $BASIS GBASIS=acct $END
 $PCM SOLVNT=WATER $END
 $PCMCAV RADII=SUAHF $END
 $PCMCAV epshet(1)=4.0 epshet(2)=4.0 epshet(3)=4.0 $END
 $TESCAV NTSALL=240 mthall=4 $END
 $SCF DIIS=.f. SOSCF=.t. DIRSCF=.T. FDIFF=.F. NPUNCH=1 $END
 $SYSTEM TIMLIM=99999999 MWORDS=100 memddi=200 $END
 $DATA
Comments go here: optimized at mp2/accq
C1

# 第三块到最后均为坐标块
 O      8.0          -5.44191107    0.03724232    0.00028528
 H      1.0          -5.78596783   -0.44063637   -0.76078243
 H      1.0          -5.78611217   -0.44063955    0.76128953
 O      8.0           5.51700704   -0.04517310   -0.00041368
 H      1.0           4.55794769    0.09038914   -0.00027831
 H      1.0           5.88503889    0.84193762   -0.00010039

......

# ---------------------------------------------------------------------
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
        print("\x1B[31m Input File Error. Please check!\x1B[0m\n" + "-" * 40)
        print("只有\x1B[32m%s\x1B[0m个坐标块！请修改输入文件." % k)
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
