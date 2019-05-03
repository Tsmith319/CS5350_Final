import random
# Creates a data set, list of labels, and a dictionary of the each attributes' values based upon the given file name. If unknownType = 1 then we treat any unknown attribute values as missing data otherwise
# they are treated as part of the data set. 
def openFile(filename):
	f = open(filename, 'r')

	dataSet = list()
	labels = list()

	index = 0
	currLine = 0
	for line in f:
		if currLine != 0:
			terms = line.strip().split(',')
			count = 0;
			currExample = []
			currLabel = None
			for term in terms:
				if count < 13:
					currExample.append(float(term))
				else:	
					currExample.append(float(1))
					if(int(term) == 0):
						currLabel = float(-1.0)
					else:
						currLabel = float(term)
				count = count + 1
			dataSet.append(currExample)
			labels.insert(index, currLabel)
			index = index + 1
		else:
			currLine += 1
			

	return (dataSet, labels)

def standardPerceptron(data,labels,testData,testLabels, unavailable):
	w = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	a = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	epoch = 1
	T = 10
	r = 5
	trainingPredictionError = 0
	testingPredictionError = 0
	while epoch != T:
		index = 0
		for example in data:
			if index not in unavailable:
				wTx = 0.0
				y_i = labels[index]

				vector_Index = 0
				for x in example:
					wTx += (float(w[vector_Index]) * float(x)) 
					vector_Index += 1

				copyOfExample = list(example)
				if (float(y_i) * float(wTx)) <= 0:
					r_yi = float(y_i * r)
					copyOfExample = [(float(x) * float(r_yi)) for x in copyOfExample]

					vector_Index = 0
					for x in copyOfExample:
						w[vector_Index] = float(w[vector_Index]) + float(x)
						vector_Index += 1

				vector_Index = 0
				for ai in a:
					a[vector_Index] = ai + w[vector_Index]
					vector_Index += 1

			index += 1
		epoch += 1

		trainingPredictionError += predictData(data,labels,a,1,unavailable)
		testingPredictionError += predictData(testData,testLabels,a,0,unavailable)
		
	print("Training Errors")
	print(float(trainingPredictionError)/T)
	print("Testing Errors")
	print(float(testingPredictionError)/T)
	print("Vector")
	print(a)
	return a

def predictData(data,labels,w,isTrainingData,unavailable):
	predictedError = 0.0
	totalData = len(labels)
	index = 0
	for example in data:
		if isTrainingData == 1:
			if index not in unavailable:
				y_i = labels[index]
				vector_Index = 0
				wTx = 0.0
				for x in example:
					wTx += (float(x) * float(w[vector_Index]))
					vector_Index += 1
				if(y_i * wTx) < 0:
					predictedError += 1
		else:
			y_i = labels[index]
			vector_Index = 0
			wTx = 0.0
			for x in example:
				wTx += (float(x) * float(w[vector_Index]))
				vector_Index += 1
			if(y_i * wTx) < 0:
				predictedError += 1
		index += 1

	return 1 - (float(predictedError)/float(totalData))

def shuffleData(data,labels):
	numOfItems = len(labels)
	shuffled_Data = list()
	shuffled_Labels = list()
	indecesAlreadyUsed = set()

	while ((len(shuffled_Data) != numOfItems) and (len(shuffled_Labels) != numOfItems)):
		currIndex = random.randint(0,numOfItems-1)
		if currIndex not in indecesAlreadyUsed:
			shuffled_Data.append(data[currIndex])
			shuffled_Labels.append(labels[currIndex])
			indecesAlreadyUsed.add(currIndex)

	return (shuffled_Data, shuffled_Labels)

def getTestData(trainingData, trainingLabels):
	numOfItems = int(len(trainingLabels) * 0.4)
	totalData = int(len(trainingLabels))
	testData = list()
	testLabels = list()
	indecesAlreadyUsed = set()

	while ((len(testData) != numOfItems) and (len(testLabels) != numOfItems)):
		currIndex = random.randint(0,totalData-1)
		if currIndex not in indecesAlreadyUsed:
			testData.append(trainingData[currIndex])
			testLabels.append(trainingLabels[currIndex])
			indecesAlreadyUsed.add(currIndex)

	return (testData, testLabels, trainingData, trainingLabels, indecesAlreadyUsed)

def main():
	trainingData, trainingLabels = openFile("heart.csv")
	trainingData, trainingLabels = shuffleData(trainingData,trainingLabels)
	testingData, testingLabels, trainingData, trainingLabels, indecesNotAvailable = getTestData(trainingData,trainingLabels)
	print("TEST DATA LENGTH: " + str(len(testingLabels)))
	print("Training Data Length: " + str(len(trainingLabels)))
	print(indecesNotAvailable)
	w_Vector = standardPerceptron(trainingData, trainingLabels, testingData, testingLabels, indecesNotAvailable)



if __name__=="__main__":
	main()