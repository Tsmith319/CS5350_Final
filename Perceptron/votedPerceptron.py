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

def votedPerceptron(data,labels,testData,testLabels, unavailable):
	w = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	epoch = 1
	T = 10
	r = 5
	m = 0
	vectors = []
	c = []
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
					new_w = []
					for x in copyOfExample:
						new_w.append(float(w[vector_Index]) + float(x))
						vector_Index += 1
					w = new_w

					if(len(vectors) != 0):
						m += 1

					if(m > (len(vectors) - 1)):
						vectors.append(new_w)
					else:
						vectors[m] = new_w

					if(m > (len(c) - 1)):
						c.append(1)
					else:
						c[m] = 1
					

				else:
					if(m > (len(c) - 1)):
						c.append(1)
					else:
						c[m] = c[m] + 1
			index += 1
		epoch += 1

		trainingPredictionError += predictData(data,labels,vectors,c,1,unavailable)
		testingPredictionError += predictData(testData,testLabels,vectors,c,0,unavailable)
		
	print("Training Errors")
	print(float(trainingPredictionError)/T)
	print("Testing Errors")
	print(float(testingPredictionError)/T)
	return vectors,c

def predictData(data,labels,vectors,c,isTrainingData,unavailable):
	predictedError = 0.0
	totalData = len(labels)
	index = 0
	for example in data:
		if isTrainingData == 1:
			if index not in unavailable:
				y_i = labels[index]
				
				wTx = 0.0
				c_index = 0
				for w in vectors:
					vector_Index = 0
					for x in example:
						wTx += c[c_index] * (float(x) * float(w[vector_Index]))
						vector_Index += 1
					c_index += 1
				if(y_i * wTx) < 0:
					predictedError += 1
		else:
			y_i = labels[index]
				
			wTx = 0.0
			c_index = 0
			for w in vectors:
				vector_Index = 0
				for x in example:
					wTx += c[c_index] * (float(x) * float(w[vector_Index]))
					vector_Index += 1
				c_index += 1
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
	numOfItems = int(len(trainingLabels) * 0.40)
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
	w_Vector = votedPerceptron(trainingData, trainingLabels, testingData, testingLabels,indecesNotAvailable)



if __name__=="__main__":
	main()