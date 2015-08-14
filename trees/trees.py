from math import log
import operator
def calcShannonEnt (dataSet):
	numEntries = len(dataSet)
	labelCounts = {}
	for vec in dataSet:
		currenLabel = vec[-1]
		if  currenLabel not in labelCounts:
			labelCounts[currenLabel] = 0
		labelCounts[currenLabel] +=1
	shannonEnt = 0.0
	for key in labelCounts:
		prop = float(labelCounts[key] )/ numEntries
		shannonEnt -= prop * log(prop,2)
	return shannonEnt

def createdataSet():
	dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
	labels = ['no surfacing', 'flippers']
	return dataSet,labels

def splitDataSet(dataSet,axis,value):
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reduceFeatVec = featVec[:axis]
			reduceFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reduceFeatVec)
	return retDataSet

def  chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0])-1
	baseEntropy = calcShannonEnt(dataSet)
	bestInfoGain = 0.0
	bestFeature = -1
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataset = splitDataSet(dataSet, i, value)
			prob = len(subDataset)/float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataset)
		infoGain =  baseEntropy - newEntropy
		if (bestInfoGain < infoGain):
			bestInfoGain = infoGain
			bestFeature = i;
	return bestFeature

def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] +=1
	sortedClassCount = sorted(classCount.iteritems(), key = operator.itemgetter(1), reverse = True)
	return sortedClassCount[0][0]

def createTree(dataSet, labels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0] ) ==1:
		return majorityCnt(classList)
	bestFeature = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeature]
	print('bestFeature %d, bestLabels %s'  %(bestFeature,bestFeatLabel))
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeature])
	featValues = [example[bestFeature] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeature, value), subLabels)
	return myTree

def classify(inputTree, featLabels, testVec):
	firstStr = inputTree.keys()[0]
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)
	for key in secondDict.keys():
		if testVec[featIndex] == key:
			if type(secondDict[key]).__name__=='dict':
				classLabel = classify(secondDict[key], featLabels,testVec)
			else:
				classLabel = secondDict[key]
	return classLabel
				pass

		
		



def storeTree(inputTree, fileName):
	import pickle
	fw = open(fileName,'w')
	pickle.dump(inputTree, fw)
	fw.close()

def getTree(fileName):
	import pickle
	fr = open(fileName)
	return pickle.load(fr)










		



			
		
