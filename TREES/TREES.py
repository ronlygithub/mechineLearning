from math import log

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