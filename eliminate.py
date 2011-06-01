#!/export/home/liuhui/opt/bin/python3

"""
    This script use to 
"""

import common
from pprint import pprint
import re

#read data from the file which contain '*', and split to list
data = common.SplitToBlock( common.ReadDataFromFile('fix43-eda.lcd') )

#get coordination
aa = []
reg = re.compile(' DU ')
for x in data :
    for y in x:
        if reg.match( y ):
#           prfloat( y )
            aa.append( x )
            break

def DataList( larray, i ):
    tmp = []
    for x in larray[i]:
        tmp.append( x.strip().split()[1:] )
    return tmp


supermolecule = DataList(aa,4)
monomer1 = DataList(aa,5)
monomer2 = DataList(aa,6)

#pprint(supermolecule)
#pprint( monomer1)
#pprint( monomer2)

for x in monomer1:
    for z in  supermolecule:
        if x[0] == z[0]:
            x[1] = z[1]
            x[0] = float(x[0])
            x[1] = float(x[1])
            x[2] = float(x[2])

for y in monomer2:
    for z in  supermolecule:
        if y[0] == z[0]:
            y[1] = z[1]

pprint(monomer1)
pprint(monomer2)
