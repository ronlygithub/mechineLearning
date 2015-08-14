
# KNN Demo
# @author duanmh
# 2015-8-6
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
from os import listdir

def createDataSet():
	group = array([[1.0,1.1], [1.0,1.0],[0,0],[0,0.1]])
	labels = ['A','A','B','B']
	return group, labels


# inX: vector to be classified,
# dataSet: train dataset,
# labels: labels of train dataset,
# k: number of vote used

def classify0(inX, dataSet, labels, k):
	dataSetSize = dataSet.shape[0]
	diffMat  = tile(inX, (dataSetSize, 1)) - dataSet
	sqDiffMat = diffMat ** 2
	sqDistances = sqDiffMat.sum(axis=1)
	distances = sqDistances**0.5
	sortedDistIndicies = distances.argsort()
	classCount = { }
	for i in range(k):
		voteIlabel = labels[sortedDistIndicies[i]]
		classCount[voteIlabel] = classCount.get(voteIlabel,0) +1 
	sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)
	return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    fr = open(filename)
    index = 0
    for line in fr.readlines():
         line = line.strip()
         listFromLine = line.split('\t')
         returnMat[index,:] = listFromLine[0:3]
         classLabelVector.append(int(listFromLine[-1]))
         index += 1
    return returnMat,classLabelVector

def showLike(x, y):
     dataMat,dataLabels = file2matrix('datingTestSet2.txt')
     dataMat ,ranges, minValues= autoNorm(dataMat)
     fig = plt.figure()
     ax = fig.add_subplot(111)
     ax.scatter(dataMat[:,x],dataMat[:,y],15*array(dataLabels),15*array(dataLabels))
     plt.show()

def autoNorm(dataSet):
     minValues  = dataSet.min(0)
     maxValues = dataSet.max(0)
     ranges = maxValues - minValues
     normDataSet = zeros(shape(dataSet))
     m = dataSet.shape[0]
     normDataSet = dataSet - tile(minValues,(m, 1))
     normDataSet = normDataSet / tile(ranges,(m,1))
     return  normDataSet, ranges, minValues

def datingClassTest(ratio):
     dataMat,dataLabels = file2matrix('datingTestSet2.txt')
     hoRatio = ratio	
     normaMat, ranges, minValues = autoNorm(dataMat)
     m = normaMat.shape[0]
     numTestVesc = int(m*hoRatio)
     errorCount = 0.0
     for i in range(numTestVesc):
         classifierResult = classify0(normaMat[i,:], normaMat[numTestVesc:m,:],\
         	dataLabels[numTestVesc:m],3)
         print("the classifier came back with: %d, the real answer is %d"\
         	%(classifierResult, dataLabels[i]))
         if(classifierResult != dataLabels[i]):
         	errorCount+=1.0
     print("total number is %d ,  test number is %d, errorCount is %d, the total error rate is  %f"  %(m,numTestVesc,errorCount,errorCount/float(numTestVesc)))    	

def classifyPerson():
     resultList = ['not at all', 'in small doses', 'in large doses']
     percentTats = float(raw_input("percentage of time spent playing video games?"))
     ffMiles = float(raw_input("frequent flier mildes earned per year?"))
     iceCream = 	float(raw_input("liters of ice cream consumed per year?"))
     dataMat,dataLabels = file2matrix('datingTestSet2.txt')
     normaMat, ranges, minValues = autoNorm(dataMat)
     inArr = array([percentTats,ffMiles,iceCream])
     classifierResult = classify0((inArr - minValues)/ranges, normaMat,dataLabels,3)
     print("you may like this person :" ,resultList[classifierResult-1])

def img2vector(filename):
     returnVect = zeros((1,1024))
     fr = open(filename)
     for i in range(32):
         lineStr = fr.readline()
         for j in range(32):
             returnVect[0,32*i+j] = int(lineStr[j])
     return returnVect

def handwritingClassTest():
     hwLabels = []
     trianingFileList = listdir('./digits/trainingDigits')
     m = len(trianingFileList)
     trianingMat = zeros((m,1024))
     for i in range(m):
     	filenameStr = trianingFileList[i]
     	fileStr = filenameStr.split('.')[0]
     	classNumStr = int(fileStr.split('_')[0])
     	hwLabels.append(classNumStr)
     	trianingMat[i,:] = img2vector('./digits/trainingDigits/%s' %filenameStr)
     testFileList = listdir('./digits/testDigits')
     errorCount = 0.0
     mTest = len(testFileList)
     for j in range(mTest):
         fileNameStr = testFileList[j]
         fileName = fileNameStr.split('.')[0]
         classNumStr = int(fileName.split('_')[0])
         vectTest = img2vector('./digits/testDigits/%s' %fileNameStr)
         result = classify0(vectTest,trianingMat,hwLabels,5)
         if (result != classNumStr):
          	errorCount +=1.0
          	print('the result come back is %d,  the real real lable is %d '   %(result, classNumStr))
     accuracy = (1.0- errorCount/float(mTest))
     print('the number of total error is %d' %errorCount)
     print 'the accuracy rate is %f  ' %(accuracy)