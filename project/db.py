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
 
def addAnswers(student_id,quest_id,answer_id):
    print(str(answer_id)+' '+str(student_id)+' '+str(quest_id))    
    cur = mysql.connection.cursor()
    cur.execute('insert into quest_responses(student_id,quest_id,answer_id)values(%s,%s,%s)',(student_id,quest_id,answer_id,))
    mysql.connection.commit()