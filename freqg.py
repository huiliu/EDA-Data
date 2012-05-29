#!/bin/env python3
#-*- encoding: utf-8 -*-

"""
此程序用于通过频率验证中的第一个虚频坐标与平衡坐标来调整优化坐标以得到分子最终
的平衡构型。

使用的状态机原理对文件进行分步匹配。
各状态的匹配内容请见code中的详细注释。

TODO:
    与GAMESS的同功能代码整合为一个文件。

Liu Hui
2012-05-29
"""
import sys
import re
from optparse import OptionParser

def main(argv):
    """主函数。

    argv        为需要检查的文件(Gaussian几何优化结果文件，如果包含频率计算
                将检查是否存在虚频，如果存在将自动校正。
    """
    options, filename = parsecmd()
    # 检查是否存在虚频
    chkImag(filename)
    lines = open(filename, 'r').readlines()
    locateData(lines, options)

def chkImag(fname):
    """此函数用来检查Gaussian优化构型并计算频率结果文件中是否存在虚频。

    通过shell命令grep -c来实现的，所以无法移植至Windows平台。
    """
    # USE TO Check imaginary frequencies
    cmd_chkImag = 'grep -c "imaginary frequencies" %s'
    if sys.popen(cmd_chkImag) != 0:
        # the frequencies has a negative value.
        print("There has imaginary frequencies")
    else:
        print("计算所得平衡构型没有频率虚。\
            但是，请用GaussView查看确认构型是否合理.")
        sys.exit(0)

def locateData(data, options=None):
    """此函数利用状态机原理对Gaussian构型优化文件进行解析，以找出平衡坐标
    第一个虚频对应坐标，用以计算校正坐标进行再次优化。

    data        为按行读取的Gaussian输出文件内容。为一个列表
    options     从命令获取的一个选项信息，如校正因子的大小
    """
    def swich_state(currentState):
        """此函数用于切换正则表达式的匹配状态。

        currentState        为当前匹配状态。

        返回下一个匹配状态，指示循环将进行下一个匹配操作。
        """
        currentState += 1
        # 此 if语句用于控制重复匹配过程，即当状态６完成后，重新进行初始状态
        if (currentState > 6):
            currentState = 0
        return currentState

    def getCoord(line, start, end=None):
        """此函数用于从匹配行中提取所需的坐标值，与Gaussian输出文件格式有关。

        line            为所根据正则表达式时匹配的数据行.为一行文本.
        start           为所需坐标的起始位。
        end             为所需坐标的末位。

        返回一个包含所需坐标的列表。
        """
        items = line.split()
        return items[start:end]

    def CorrectCoord(eqCoord, imagCoord, factor=2):
        """此函数通过频率计算得到的第一个虚频坐标来校正计算所得的平衡坐标,
        同时打印校正后的坐标值.
        eqCoord         为平衡坐标。数据结构为一个嵌套列表，
                        每个点的x,y,z三组值组成一个列表，然后所有点的列表组合
                        为eqCoord. 如: [[x1,y1,z1],[x2,y2,z2,],......]
                        从Gaussian计算结果文件中取得.

        imagCoord       为计算第一个虚频振动坐标，亦从Gaussian计算结果文件提取.
                        数据结构形式与eqCoord一致.
        """
        for a, b in zip(eqCoord, imagCoord):
            for c, d  in zip(a, b):
                tmp = float(c) + float(d)/factor
                print("%.4f" % tmp, end='\t')
            print()

    currentState = 0
    Eq_Coord = []
    Imag_Coord = []

    # 状态机原理。当匹配到某一行后将进行下一个匹配状态，匹配新的数据
    # 每一个状态匹配的数据新注意已被注释的print语句
    for line in data:
        if currentState == 0:
            # 初始查找，直到确认计算找到的稳定构型
            # print 'finding Stationary...'
            if re.match(r'.*Stationary point found.*', line):
                currentState = swich_state(currentState)
        elif currentState == 1:
            # 确认计算已找到的稳定构型，继续查找坐标
            # print 'finding orientation...'
            if re.match(r'.*Standard orientation.*', line):
                currentState = swich_state(currentState)
        elif currentState == 2:
            # 已查找到稳态坐标块，剔除表头
            # print 'about to finding data...'
            if re.match(r' +[0-9]{1,2} +[0-9]{1,2} +[0-9] +-*[0-9]+\.[0-9]+ +-*[0-9]+\.[0-9]+ +-*[0-9]+\.[0-9]+', line):
                currentState = swich_state(currentState)
                Eq_Coord.append(getCoord(line, 3))
                # print(line)       # 中间匹配时输出
        elif currentState == 3:
            # 记录输出平衡坐标块
            # print "printing stationary point coordination..."
            if re.match(r' +[0-9]{1,2} +[0-9]{1,2} +[0-9] +-*[0-9]+\.[0-9]+ +-*[0-9]+\.[0-9]+ +-*[0-9]+\.[0-9]+', line):
                Eq_Coord.append(getCoord(line, 3))
                # print(line)       # 中间匹配时输出
            else:
                currentState = swich_state(currentState)
        elif currentState == 4:
            # print "searching imaginary frequencies data block"
            if re.match(r'.*imaginary frequencies.*negative Signs.*', line):
                currentState = swich_state(currentState)
        elif currentState == 5:
            # print "found imaginary frequencies data block"
            if re.match(r'.*[0-9]+ +[0-9]+ +-*[0-9]+\.[0-9]+ +-*[0-9]+\.[0-9]+ +-*[0-9]+\.[0-9]+', line):
                currentState = swich_state(currentState)
                # print(line)       # 中间匹配时输出
                Imag_Coord.append(getCoord(line, 2, 5))
        elif currentState == 6:
            # print "# print imaginary frequencies data block"
            if re.match(r'.*[0-9]+ +[0-9]+ +-*[0-9]+\.[0-9]+ +-*[0-9]+\.[0-9]+ +-*[0-9]+\.[0-9]+', line):
                Imag_Coord.append(getCoord(line, 2, 5))
                # print(line)       # 中间匹配时输出
            else:
                currentState = swich_state(currentState)
        else:
            break

    CorrectCoord(Eq_Coord, Imag_Coord, options.factor)

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

if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)
