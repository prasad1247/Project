import MySQLdb
import random
from project.generate import Feature

mydb = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="root",
    db="learningdb"
)

problemList = {"for": 1, "if": 2, "if else": 3,
               "while": 4, "do while": 5, "switch": 6}
learningStyles = {"Visual": 1, "Auditory": 2, "Kinesthetic": 3}
knowledgeLevels = {"Beginner": 1, "Intermediate": 2, "Expert": 3}
learningObjects1 = {"Video": 1, "Chart": 2,
                    "Audios": 3, "Simulation": 4, "Highlighted Text": 5}

learningObjects1 = {"https://nptel.ac.in/cources/106104128/15": 1, "https://www.geeksforgeeks.org/c-language-2-gq/loops-control-structure-gq/": 2,
                    "https://www.cluster2.hostgator.co.in/files/writeable/uploads/hostgator99706/file/letusc-yashwantkanetkar.pdf": 3, "http://cse02-iiith.vlabs.ac.in/exp3/simulation/index.html": 4,
                     "https://www.tutorialspoint.com/cprogramming/c_for_loop.htm": 5}

testPerformance = [3, 4, 5, 6, 7]
path1 = {"Video->Chart": 1, "Audios->Video": 2,
        "Simulation->Highlighted Text": 3}
path = {"https://nptel.ac.in/cources/106104128/15->https://www.geeksforgeeks.org/c-language-2-gq/loops-control-structure-gq/": 1, "https://www.cluster2.hostgator.co.in/files/writeable/uploads/hostgator99706/file/letusc-yashwantkanetkar.pdf->https://nptel.ac.in/cources/106104128/15": 2,
        "http://cse02-iiith.vlabs.ac.in/exp3/simulation/index.html->https://www.tutorialspoint.com/cprogramming/c_for_loop.htm": 3}

def parseData(attr):
    trainingSet = []
    mydb.query("""select * from dataset where problem='switch'""")
    r = mydb.store_result()
    dataset = r.fetch_row(maxrows=0, how=1)
    for x in dataset:
        f = []
        f.append(problemList[x['problem']])
        # f.append(x['student_id'])
        f.append(knowledgeLevels[x['knowledge_level']])
        f.append(learningStyles[x['learning_style']])
        f.append(int(x['test_performance']))
        if(attr == "path"):
            f.append(learningObjects1[x['learning_object']])
            f.append(path[x['path']])
        if(attr == "learningObject"):
            f.append(path[x['path']])
            f.append(learningObjects1[x['learning_object']])

        trainingSet.append(f)
    return trainingSet

def parseData1(attr,cnt):
    trainingSet = []
    for i in range(0,cnt):
        mydb.query("""select * from dataset where problem='switch'""")
        r = mydb.store_result()
        dataset = r.fetch_row(maxrows=0, how=1)
        for x in dataset:
            f = []
            f.append(problemList[x['problem']])
            # f.append(x['student_id'])
            f.append(knowledgeLevels[x['knowledge_level']])
            f.append(learningStyles[x['learning_style']])
            f.append(int(x['test_performance']))
            if(attr == "path"):
                f.append(learningObjects1[x['learning_object']])
                f.append(path[x['path']])
            if(attr == "learningObject"):
                f.append(path[x['path']])
                f.append(learningObjects1[x['learning_object']])

            trainingSet.append(f)
    return trainingSet


def loadDataset(split, attr=None, offset=None, cnt=None):
    trainingSet = []
    testSet = []
    query = ""
    if attr != None:
        query = "select * from dataset where problem='"+attr+"'"
    elif cnt != None:
        query = "select * from dataset order by id limit " + \
            str(offset)+","+str(cnt)
    else:
        query = "select * from dataset"

    mydb.query(query)
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
        if(split != None):
            if random.random() < split:
                trainingSet.append(f)
            else:
                testSet.append(f)
        else:
            trainingSet.append(f)
    return trainingSet, testSet
