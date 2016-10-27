#!usr/bin/env Python
#coding:utf-8

import operator
from math import log

def calcShannonEnt(dataSet):
    '''
    计算给定数据集的香农熵
    dataSet:给定数据集
    '''

    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def createDataSet():
    '''
    手动建立的测试数据
    '''

    dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels

def splitDataSet(dataSet, axis, value):
    '''
    按照给定特征划分数据集
    dataSet:给定数据集
    axis:划分数据集的特征
    value:特征的返回值
    '''

    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    '''
    选择最好的数据集划分方式
    dataSet:给定数据集
    '''

    numFeatures = len(dataSet[0]) -1
    bestEntropy = calcShannonEnt(dataSet)
    bestInforGain = 0.0;bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i , value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        inforGain = bestEntropy - newEntropy
        if inforGain > bestInforGain:
            bestInforGain = inforGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    '''
    查找并返回出现次数最多的分类名称
    classList:分类标签向量
    '''

    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    '''
    创建树
    dataSet:数据集（如该数据需要归一化，该数据集为归一化后打数据集）
    labels:标签列表
    '''

    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del labels[bestFeat]
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value), subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):
    '''
    使用决策树的分类函数
    inputTree:训练好的决策树
    featLabels:测试数据的分类标签列表
    testVec:测试数据
    '''

    firstStr = imputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inputTree, filename):
    '''
    使用Pickle库存储决策树
    inputTree:训练好的决策树
    filename:保存路经
    '''

    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

