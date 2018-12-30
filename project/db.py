from flask_mysqldb import MySQL
import json


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    # MySQL configurations
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'learningdb'
    app.config['MYSQL_HOST'] = 'localhost'
    print("in init db")
    global mysql
    mysql = MySQL()
    mysql.init_app(app)
    
    
def getQuestions():
    cur = mysql.connection.cursor()
    cur.execute('select * from assessment_quest')
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
            json_data.append(dict(zip(row_headers,result)))
    return json_data

def validateUser(username,password):
    cur = mysql.connection.cursor()
    cur.execute('select * from user where username=%s and password=%s',(username,password))
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
            json_data.append(dict(zip(row_headers,result)))
    return json_data

def getUser(userId):
    cur = mysql.connection.cursor()
    cur.execute('select * from user where id=%s',(userId,))
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
            json_data.append(dict(zip(row_headers,result)))
    return json_data

def getTestQuestions(problem):
    cur = mysql.connection.cursor()
    cur.execute('select * from tests where problem=%s',(problem,))
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
            json_data.append(dict(zip(row_headers,result)))
    return json_data

def getIncompleteDataset(userId):
    cur = mysql.connection.cursor()
    cur.execute('select * from user_dataset where done =0 and user_id=%s',(userId,))
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
            json_data.append(dict(zip(row_headers,result)))
    return json_data

def addTouserDataset(userId,x):
    cur = mysql.connection.cursor()
    cur.execute('insert into user_dataset(user_id,problem,learning_style,knowledge_level,learning_object,'+
    'test_performance,path,done)values(%s,%s,%s,%s,%s,%s,%s,%s)',(userId,x.problem,x.learningStyle,x.knowledgeLevel,
    x.learningObject,x.testPerformance,x.path,0))
    mysql.connection.commit()


def insertIntoDataset(userId):
    cur = mysql.connection.cursor()
    cur.execute('insert into dataset(student_id,problem,learning_style,knowledge_level,learning_object,'+
    'test_performance,path) select user_id,problem,learning_style,knowledge_level,learning_object,'+
    'test_performance,path from user_dataset where user_id='+userId)
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    cur.execute('update user_dataset set done = 1 where user_id=%s',(userId,))
    mysql.connection.commit()


def updateUserDataset(userId,test_performance,path):
    userData=getIncompleteDataset(userId)
    id=userData[0]['id']
    cur = mysql.connection.cursor()
    cur.execute('update user_dataset set done = 1 where user_id=%s',(userId,))
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    cur.execute('insert into user_dataset(user_id,problem,learning_style,knowledge_level,learning_object,'+
    'test_performance,path,done) select user_id,problem,learning_style,knowledge_level,learning_object,'+
    '"'+test_performance+'","'+path+'",0 from user_dataset where id=%s and user_id=%s',(id,userId))
    mysql.connection.commit()
    


def registerUser(username,password,name):
    cur = mysql.connection.cursor()
    cur.execute('insert into user(username,password,name)values(%s,%s,%s)',(username,password,name))
    mysql.connection.commit()
 
def addAnswers(student_id,quest_id,answer_id):
    print(str(answer_id)+' '+str(student_id)+' '+str(quest_id))    
    cur = mysql.connection.cursor()
    cur.execute('insert into quest_responses(student_id,quest_id,answer_id)values(%s,%s,%s)',(student_id,quest_id,answer_id,))
    mysql.connection.commit()