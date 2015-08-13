# native bayes
# authot: duanmh
# 2015-08-13 22:46

from Numpy import *

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
 			returnVect.index(word) = 1
 		else:
 			print ("the word: %s is not in my vocabulary" %word)
 	return returnVect