# native bayes
# authot: duanmh
# 2015-08-13 22:46

from numpy import *

# train dataset  and  labels
def loadDataSet():
	postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                          ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                          ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                          ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                          ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                          ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
 	classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
 	return postingList,classVec

# get unique vocabulary  list in dataset
def creatVocabList(dataSet):
 	vocabList = set([])
 	for document in dataSet:
 		vocabList = vocabList | set(document)
 	return list(vocabList)

# transform document to vector
def setOfWord2Vec(vocabList, inputSet):
 	returnVect = [0] * len(vocabList)
 	for word in inputSet:
 		if word in vocabList:
 			returnVect[vocabList.index(word)] = 1
 		else:
 			print ("the word: %s is not in my vocabulary" %word)
 	return returnVect

def loadTrainingSet():
	dataSet, labels = loadDataSet();
	vocabList = creatVocabList(dataSet)
	trainMatrix = []
	for document in dataSet:
		trainMatrix.append(setOfWord2Vec(vocabList, document))
	return trainMatrix, labels

def trainNB0(trainMatrix, trainCatary):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = sum(trainCatary)/ float(numTrainDocs)
	p0Num = ones(numWords)
	p1Num = ones(numWords)
	p0Denom = 2.0; p1Denom = 2.0
	
	for i in range(numTrainDocs):
		if trainCatary[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p1Vect = log(p1Num / p1Denom)
	p0Vect = log(p0Num /p0Denom)
	return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Clissify, p0Vec, p1Vec, pClass1):
	p1 = sum(vec2Clissify * p1Vec) + log(pClass1)
	p0 = sum(vec2Clissify * p0Vec) + log(1-pClass1)

	if p1 > p0:
		return p0,p1,1
	else:
		return p0,p1,0

def testingNB():
	listPosts, listClasses = loadDataSet()
	myVocabList = creatVocabList(listPosts)
	trainMat = []
	for postsinDoc  in listPosts:
		trainMat.append(setOfWord2Vec(myVocabList, postsinDoc))
	p0v , p1v, pAb = trainNB0(array(trainMat), array(listClasses))
	testEntry = ['love', 'my', 'dalmation']
	thisDoc = array(setOfWord2Vec(myVocabList,testEntry))
	print(testEntry, 'classified as:' , classifyNB(thisDoc,p0v,p1v,pAb))
	testEntry = ['stupid', 'garbage']
	thisDoc = array(setOfWord2Vec(myVocabList,testEntry))
	print(testEntry, 'classified as:' , classifyNB(thisDoc,p0v,p1v,pAb))

# transform document to vector bag of word model 
def bagOfWord2Vec(vocabList, inputSet):
 	returnVect = [0] * len(vocabList)
 	for word in inputSet:
 		if word in vocabList:
 			returnVect[vocabList.index(word)]+=1
 		else:
 			print ("the word: %s is not in my vocabulary" %word)
 	return returnVect

# regrex parse and splite text 
def textParse(bigString):
 	import re
 	listOfTokens = re.split(r'\W*', bigString)
 	return [token.lower() for token in listOfTokens if(len(token)) >2]


def spamTest():
	docList = []; classList = []; fullText = [];
	for i in xrange(1,10):
		wordList = textParse(open('./email/spam/%d.txt' % i).read())		
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(open('./email/ham/%d.txt'  % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = creatVocabList(docList)
	trainingSet = range(50); testSet = []
	for i in range(10):
		randIndex= int(random.uniform(0, len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat = []; trianClass = []
	for docIndex in trainingSet:
		trainMat.append(bagOfWord2Vec(vocabList, docList))
		trianClass.append(classList[docIndex])
	p0, p1, pab = trainNB0(array(trainMat), array(trainClass))
	errorCount =0
	
	for docIndex in testSet:
		wordVec = bagOfWord2Vec(vocabList, docList)
		if classifyNB(wordVec,p0,p1,pab) != classList[docIndex]:
			errorCount+=1
	print('the error rate is: ', float(errorCount)/len(testSet))





	

