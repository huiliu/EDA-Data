#!/bin/env python3
#-*- encoding: utf-8 -*-

"""
此文件用来帮助消除虚频。

输入文件为GAMESS计算HESSIAN的输出文件。
1. 首先会判断是否存在虚频
2. 如果存在虚频，进行经验调整，并输出初始优化坐标。
3. 新坐标＝原坐标＋虚频在各方向振动值/factor
    factor为经验因子，默认为2
4. 注意原坐标来看计算HESSIAN的输入文件INP，请确认输入文件
    没有被修改


TODO:
    1. 检查HASSIAN计算文件是否有虚频
    2. 根据经验判断振动频率是否正常
"""

import os
import sys
from optparse import OptionParser


def parsecmd():
    """
    """
    usage = "Usage: %prog [options] filename"
    p = OptionParser(usage)
    p.add_option('-n', action='store', dest='factor', help=
                '经验校正因子。[默认值:%default]', default=2)

    options, argv = p.parse_args()
    if not argv or len(argv) > 1:
        print(p.usage)
        sys.exit(1)
    return (options, argv[0])

def NewOptCoordination(fname, factor):
    """生成新的优化初始坐标
    """
    # the file is the hess output file. hess.out
    HessOutputFile = fname
    # May be have error when file name contained out
    HessInputFile = HessOutputFile.replace('out', 'inp')
    cmd = "tail -20000 " + HessOutputFile + "|sed -n '/1           2           3           4           5/,/6           7           8           9          10/{/#/d;p;}' |sed '1,6d' |sed -n -e :a -e '1,12!{P;N;D;};N;ba' | sed 's/.*            //g'|awk '{print $2}'"
    HessOri = os.popen(cmd).readlines()
    AdjustCoord = [ float(x) for x in HessOri]

    cmd = "sed -rn '/C1/,/$(end)|(END)/{/#/d;p;}' " + HessInputFile + "|sed -e '1d' -e '$d'"
    InitialCoordination = os.popen(cmd).readlines()
    InitCoor = []
    CoorTag = []
    for tmpInitCor in InitialCoordination:
        tmp = tmpInitCor.split()
        CoorTag.append('\t'.join(tmp[:2]))
        for tmp in tmp[2:]:
            InitCoor.append(float(tmp))

    print("=" * 70)
    print("The adjustable factor = {0}".format(factor))
    print("=" * 70)

    numAtom = int(len(AdjustCoord)/3)
    for i in range(numAtom):
        point = [format(a + b/factor, "13.9") for a, b in zip(InitCoor[i*3:(i+1)*3], AdjustCoord[i*3:(i+1)*3])]
        print(CoorTag[i] + '\t'.join(point))

if __name__ == "__main__":

    options, argv = parsecmd()
    factor = options.factor

    NewOptCoordination(argv, factor)
