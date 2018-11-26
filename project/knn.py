import csv
import random
import math
import operator
import MySQLdb
from generate import Feature


mydb = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="root",
    db="learningdb"
)


def loadDataset(filename, split, trainingSet=[], testSet=[]):
    mydb.query("""select * from dataset """)
    r = mydb.store_result()
    dataset = r.fetch_row(maxrows=0, how=1)
    for x in dataset:
        f = Feature()
        f.problem = x['problem']
        f.student_id = x['student_id']
        f.knowledgeLevel = x['knowledge_level']
        f.learningObject = x['learning_object']
        f.learningStyle = x['learning_style']
        f.path = x['path']
        f.testPerformance = x['test_performance']
        if random.random() < split:
            trainingSet.append(f)
        else:
            testSet.append(f)


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getScore(x, testInstance):
    mydb.query("""select * from feature_sim """)
    r = mydb.store_result()
    sims = r.fetch_row(maxrows=0, how=1)
    pScore = calculate(x.problem, testInstance.problem, sims, 'problem')
    learningStyleScore = calculate(
        x.learningStyle, testInstance.learningStyle, sims, 'learning_style')
    kScore = calculate(x.knowledgeLevel, testInstance.knowledgeLevel,
                       sims, 'knowledge_level')
    # oScore = calculate(x.learningObject, testInstance.learningObject,
    #                    sims, 'learning_object')
    pathScore = calculate(x.path, testInstance.path, sims, 'path')
    testScore = 10-abs(int(x.testPerformance) -
                       int(testInstance.testPerformance))
    total = pScore+learningStyleScore+kScore+pathScore+testScore
    return 200-total


def calculate(xValue, testValue, similarity, featureVal):
    for sim in similarity:
        if sim['feature'].lower() == featureVal.lower():
            if (sim['value1'].lower() == xValue.lower() and sim['value2'].lower() == testValue.lower()) or (sim['value1'].lower() == testValue.lower() and sim['value2'].lower() == xValue.lower()):
                return sim['score']


def getNeighbors(trainingSet, testInstance, k):
    distances = {}

    for x in trainingSet:
        dist = getScore(x, testInstance)
        distances[dist] = x

    neighbors = []
    for x in sorted(distances):
        if(k == 0):
            break
        neighbors.append(distances[x])
        k = k-1
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x].learningObject
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(),
                         key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0


def main():
    # prepare data
    trainingSet = []
    testSet = []
    split = 0.67
    loadDataset('iris.data', split, trainingSet, testSet)
    print('Train set: ' + repr(len(trainingSet)))
    print('Test set: ' + repr(len(testSet)))
    # generate predictions
    predictions=[]
    k = 3
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x].learningObject))
    # accuracy = getAccuracy(testSet, predictions)
    # print('Accuracy: ' + repr(accuracy) + '%')


main()
