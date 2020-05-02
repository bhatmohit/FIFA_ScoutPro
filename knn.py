import csv
import random
import math
import operator
from prettytable import PrettyTable
table = PrettyTable(['Name','Predicted','Actual'])
 
def loadDataset(filename, split, trainingSet=[] , testSet=[]): # load dataset and generate training and testing sets
	with open(filename, 'r') as csvfile:
            next(csvfile)
            lines = csv.reader(csvfile)
            dataset = list(lines)
            for x in range(len(dataset)-1):
                for y in range(16):
                    dataset[x][y] = float(dataset[x][y])
                if random.random() < split:
                   trainingSet.append(dataset[x])
                else:
                   testSet.append(dataset[x])
 
 
def euclidDistance(instance1, instance2, length): #calculate distance 
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)
 
def getNeighbors(trainingSet, testInstance, k): #get k closest neighbours of the testinstance
	distances = []
	length = len(testInstance)-2
	for x in range(len(trainingSet)):
		dist = euclidDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors
 
def classify(neighbors): #classify the player based on number of votes 
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]
 
def getAccuracy(testSet, predictions): #calculate the accuracy
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0
	
# prepare data
trainingSet=[]
testSet=[]
split = 0.80
loadDataset('fifa.data', split, trainingSet, testSet)
print('Train set: ' + repr(len(trainingSet)))
print('Test set: ' + repr(len(testSet)))

# make predictions
predictions=[]
k = 3
for x in range(len(testSet)):
	neighbors = getNeighbors(trainingSet, testSet[x], k)
	result = classify(neighbors)
	predictions.append(result)
	table.add_row([testSet[x][-2],result,testSet[x][-1]]) 
accuracy = getAccuracy(testSet, predictions)
print(table)
print('Accuracy: ' + repr(accuracy) + '%')
