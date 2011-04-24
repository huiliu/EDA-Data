#!/export/home/liuhui/opt/python3/bin/python3

import sys
import offset
import matrix
import common


def generateJS( js, fname ):
    """
        generateJS      produce JavaScript file which use to generate
                        Chart.
            js          The offset coordination that have transpose to
                        js formation.
    """
    end = '\n\t\t});\t\n});'
    ftemplate = open('/export/home/liuhui/script/data_template.js', 'r').readlines()
    
    Js = js + end

    f = open( fname, 'w' )
        f.writelines(ftemplate)
        f.write( Js )
    f.close()

    print("generate JavaScript sucessfully!")


def ChartData( data ):
    name = "Orbital"
    section = 'series: ['
    i = 0 
    for d in data:
        section = section + "{\nname: '" + name + str(i) + \
    "',\ndata: [" + data[i] + "]\n}, "
        i += 1
    section = section[:-2] + ']'

    return section

def ReadData( fName = '/tmp/chartdata' ):
    """
        ReadData        read offset data from file
    """
    blocks = common.ReadDataFromFile( fName )

    return blocks
    
def FormatOutput( data ):
    """
        FormatOutput        make the output information is perfect.
            data            a list
    """
    nColumn = len(data[0])
    nRow = len(data)

    i = 0
    oData = []
    while i < nRow:
        tmp = ', '.join( str(x)  for x in data[i] )
        oData.append(tmp)
        i += 1
    
    return oData
        
def HandleData(bData):
    """
        HandleData      transpose the input data to a matrix
            bData       a List
    """

    nColumn = len(bData)
    i = 0
    data = []

    while i < nColumn:
        one =  bData[i].split('   ')
        one[-1] = one[-1][:-1]
#Shit! forgot add a comma, Waste plenty of time to debug.
        data.append( one[1:] )
        i += 1

    #check the data, 
    if len(data[0]) != len(data[1]):
        print("The Data May be not completely! Please Check it.")

    return data


if __name__ == "__main__":
    n = len(sys.argv)
    if n == 1:
        print("Input error!")
        print( "chart [-w | datafile] distfile " ) 
        sys.exit(1)

    distfile = 'OffsetChart'

    blocks =  ReadData(sys.argv[1])
    wData = HandleData(blocks)
    transData = matrix.transpose(wData)
    oData = FormatOutput(transData)
    chart = ChartData(oData)
    generateJS( chart, distfile + '.js' )

    #produce a file that contain offset data used to check
    f = open( distfile + '.dat', 'w' )
        f.writelines(repr(transData))
    f.close()
