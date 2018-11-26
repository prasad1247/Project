import MySQLdb
from random import randint

class Feature:
    student_id=''
    problem=''
    learningStyle=''
    knowledgeLevel=''
    learningObject=''
    testPerformance=''
    path=''



mydb = MySQLdb.connect(
  host="localhost",
  user="root",
  passwd="root",
  db="learningdb"
)
problemList=("for","if","if else","while","do while","switch")
learningStyles=["Visual","Auditory","Kinesthetic"]
knowledgeLevels=["Beginner","Intermediate","Expert"]
learningObjects=["Video","Audios","Simulation","Highlighted Text","ChartsAnd"]
testPerformance=[3,4,5,6,7]
path=["Video->Simulation","Video->Audios","Audios->simulation","Highlighted Text->Simulation","Video->Chart","Chart->Simulation"]


def getStyles():
    mydb.query("""(select sum(quesA) ansA,sum(quesB) ansB,sum(quesC) ansC,student_id from 
            (select case when quest_id=1 then sum(1) else 0 end as quesA,
            case when quest_id=2 then sum(1) else 0 end as quesB,  
            case when quest_id=3 then sum(1) else 0 end as quesC, student_id  from 
            quest_responses  group by quest_id,student_id)a group by student_id)
            """)
    r=mydb.store_result()
    data=r.fetch_row(maxrows=0,how=1)
    learningStyle=''
    for d in data:

        if d['ansA'] > d['ansB'] and d['ansA'] > d['ansC']:
            learningStyle=learningStyles[0]
        if d['ansB'] > d['ansA'] and d['ansB'] > d['ansC']:
            learningStyle=learningStyles[1]
        if d['ansC'] > d['ansB'] and d['ansC']> d['ansA']:
            learningStyle=learningStyles[2]
        f=Feature()    
        f.student_id=d['student_id']
        f.learningStyle=learningStyle
        generateProblem(f)
        generateKnowledgeLevel(f)
        generateTestPerformance(f)
        generatePath(f)
        generateLearningObjects(f)
        c=mydb.cursor()
        c.execute("""insert into dataset(student_id,problem,learning_style,knowledge_level,learning_object,test_performance,path)
        values(%s, %s, %s, %s, %s, %s, %s)""",[f.student_id,f.problem,f.learningStyle,f.knowledgeLevel,f.learningObject,f.testPerformance,f.path])
        mydb.commit()
        
        

    
def generateProblem(f):
    for i in range(len(problemList)):
        cnt=randint(0, 5)
        f.problem=problemList[cnt]

def generateKnowledgeLevel(f):
    for i in range(len(knowledgeLevels)):
            cnt=randint(0, 2)
            f.knowledgeLevel=knowledgeLevels[cnt]

def generateTestPerformance(f):
    for i in range(len(testPerformance)):
            cnt=randint(0, 4)
            f.testPerformance=testPerformance[cnt]

def generatePath(f):
    for i in range(len(path)):
            cnt=randint(0, 5)
            f.path=path[cnt]


def generateLearningObjects(f):
    for i in range(len(learningObjects)):
            cnt=randint(0, 4)
            f.learningObject=learningObjects[cnt]


getStyles()
