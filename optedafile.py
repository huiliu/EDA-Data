#!/export/home/liuhui/opt/python3/bin/python3

import sys
import common
import generateFile



def GenerateFile( fData ):
    """

        """
    data = common.SplitToBlock( fData )
    fInfo = data[0][0]
    fHead = data[1]

    print( fInfo )
    title = generateFile.CheckTitle( fInfo, 2 )
    name = title[0]
    if title[1][:3] == 'gms':
        suffix = 'inp'
        end = ' $end'
    elif title[1][:3] == 'gau': 
        suffix = 'com'
        end = '\n\n'
    else:
        print("I am not God! I cann't generate this type of file.\n \
    I just can generate GAMESS or GAUSSIAN input file.")
        sys.exit(1)

    for block in data[2:]:
        distName = block[0].replace('\n','')
        distName = distName.replace('opt', name)
        distName = distName.replace('cor', suffix)

        distF = open( distName , 'w' )
        distF.writelines( fHead )
        distF.writelines( block[1:] )
        distF.write(end)

        distF.close()
    print("Handled completely! Please Check it.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(" generateFile <InputFileName>")
        sys.exit(1)
    else:
        try:
            d = open( sys.argv[1], 'r' ).readlines() 
        except IOError:
            print("Failed to open \"" + sys.argv[1] + "\".")
            sys.exit(1)
        GenerateFile( d )
        sys.exit(0)
