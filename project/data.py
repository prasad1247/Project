import MySQLdb

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
testPerformance = [3, 4, 5, 6, 7]
path = {"Video->Chart": 1, "Audios->Video": 2,
        "Simulation->Highlighted Text": 3}

def parseData(attr):
    trainingSet=[]
    mydb.query("""select * from dataset where problem='switch'""")
    r = mydb.store_result()
    dataset = r.fetch_row(maxrows=0, how=1)
    for x in dataset:
        f=[]
        f.append(problemList[x['problem']])
        # f.append(x['student_id'])
        f.append(knowledgeLevels[x['knowledge_level']])
        f.append(learningStyles[x['learning_style']])
        f.append(int(x['test_performance']))
        if(attr=="path"):
            f.append(learningObjects1[x['learning_object']])
            f.append(path[x['path']])
        if(attr=="learningObject"):
            f.append(path[x['path']])
            f.append(learningObjects1[x['learning_object']])

        trainingSet.append(f)
    return trainingSet
