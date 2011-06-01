#!/home/huiliu/opt/bin

from pprint import pprint


def transpose( matrix ):
    nColumn = len(matrix[0])
    nRow = len(matrix)
#    print('nRow=%d nColumn=%d'%(nRow,nColumn))
#pprint(matrix)
    trans = []
    i = 0
    while i < nColumn:
        j = 0
        tmp = []
        while j < nRow:
#print('i=%d j=%d'%(i,j))
            tmp.append( matrix[j][i] )
            j += 1
        trans.append(tmp)
        i += 1
#    print( 'nRow = %d, nColumn = %d'%(len(trans), len(trans[0])))
    return trans

