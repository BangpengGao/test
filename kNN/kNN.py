#!/usr/bin/env Python
#coding:utf-8

from numpy import *
import operator

#k-NearestNeighbor
def classify0(idX, dataSet, labels, k):
    '''
    k-近邻算法
    idX:用于分类打输入向量
    dataSet:训练样本数据
    labels:标签向量
    k:最近邻居的数目
    '''

    dataSetSize = dataSet.shape[0]
    diffMat = tile(idX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis = 1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

#for txt to Numpy
def fileMatrix(fileName):
    '''
    将待处理数据的格式改变为分类器可以接受的格式
    fileName:待处理数据的路经
    '''

    fr = open(fileName)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector

#Normalize the feature
def autoNorm(dataSet):
    '''
    归一化特征值
    dataSet:待处理数据
    '''

    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet/tile(ranges, (m, 1))
    return normDataSet, ranges, minVals

#classifier for dataTestSet
def datingClassTest():
    '''
    分类器针对约会网站的测试代码
    '''

    hoRatio = 0.10
    datingDataMat, datingLabels = fileMatrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print "the classifier came back with: %d, the real answer is: %d"\
                % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))

#dating-web prediction function
def classifyPerson():
    '''
    约会网站测试函数
    '''

    resultList = ['not at all','in small doses','in large doses']
    percentTats = float(raw_input(\
            "percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = fileMatrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,\
            normMat, datingLabels, 3)
    print "You will probably like this person:",\
            resultList[classifierResult - 1]

