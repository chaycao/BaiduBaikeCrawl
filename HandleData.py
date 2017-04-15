# -*- coding: utf-8 -*-


# 初始化定义输入文件路径、输出文件路径
inputPath='/home/chaycao/PycharmProjects/BaibuBaikeCrawl/data/famousPeople_baidu.dat'
outputPath='/home/chaycao/PycharmProjects/BaibuBaikeCrawl/data/famousPeople_baidu_handle.dat'

def run_sougou():
    # 读取文件
    inputFile = open(inputPath, 'r')
    outputFile = open(outputPath, 'w')

    print("Start Handle Data")

    # 按行读取文件
    while 1:
        line = inputFile.readline()
        if not line:
            break;
        outputFile.write(line.split()[1] + "\n")

    print("End Handle Data")

def run_baidu():
    # 读取文件
    inputFile = open(inputPath, 'r')
    outputFile = open(outputPath, 'w')

    print("Start Handle Data")

    # 按行读取文件
    while 1:
        line = inputFile.readline()
        if not line:
            break;
        outputFile.write(line.split()[0] + "\n")

    print("End Handle Data")


if __name__=='__main__':
    run_baidu()

