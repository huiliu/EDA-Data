#!/export/home/liuhui/opt/python3/bin/python3

import sys
import offset
import matrix
import pprint


def generateJS( js, fname ):
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
    try:
        fData = open( fName, 'r').readlines()
    except IOError:
        print( "Failed to Read Data! Please Chech the file exsit." )
        sys.exit(1)

    blocks = offset.SplitToBlock( fData )

    if len(blocks) % 2 != 0:
    #because the supermolecular was divided into two parts, so the 
    #data would be pairs.
        print( "The data may be have some errors. Please check it." )
        sys.exit(1)
    return blocks
    
def FormatOutput( data ):
    """
        """
    nColumn = len(data[0])
    nRow = len(data)
#pprint.pprint(data) 
#print( "fr=%d, fc=%d"%(nRow, nColumn) )
    i = 0
    oData = []
    while i < nRow:
        tmp = ', '.join( str(x)  for x in data[i] )
        oData.append(tmp)
        i += 1
    
    return oData
        
def HandleData(bData):

    nColumn = len(bData)
    i = 0
    data = []
    while i < nColumn:
        mono1 = ','.join(x for x in bData[i]).replace('\n','')
        mono2 = ','.join(x for x in bData[i+1]).replace('\n','')
#Shit! forgot add a comma, Waste plenty of time to debug.
        one = (mono1 + ','+ mono2).split(',')
        data.append( one )
        i += 2

    return data


if __name__ == "__main__":
    n = len(sys.argv)
    if n == 1:
        print("Input error!")
        print( "chart [-w | datafile] distfile " ) 
        sys.exit(1)
#    para = sys.argv[1]
#    datafile = ''
    distfile = 'OffsetChart'
#    blocks = ''
#    if n == 2:
#        distfile = sys.argv[1] 
#        blocks =  ReadData()
#    elif para == "-w" and len(sys.argv) == 2:
#        distfile = sys.argv[2]
#        blocks =  ReadData()
#    elif len(sys.argv) == 3 and para == "-w":
#        datafile = sys.argv[1]
#        distfile = sys.argv[2]
#        blocks =  ReadData(datafile)
#    else:
#        print("Input error!")
#        print( "chart [-w | datafile] distfile " ) 
#        sys.exit(1)

    blocks =  ReadData(sys.argv[1])
    wData = HandleData(blocks)
    transData = matrix.transpose(wData)
    oData = FormatOutput(transData)
    chart = ChartData(oData)
    generateJS( chart, distfile + '.js' )
    f = open( distfile , 'w')
    f.writelines(repr(transData))
    f.close()
