from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
import time
import random
from werkzeug.exceptions import abort
from project import db
from project import knn,data
from project.generate import Feature
from project import comparison
bp = Blueprint('blog', __name__)


@bp.route('/')
@bp.route('/logout')
def index():
    """Login."""
    session.pop('user',None)
    return render_template('login.html')

def getUser(request,session):
    id=request.form.get("userId") or request.args.get("userId")
    username=request.form.get("username") or request.args.get("username")
    user ={"id":id,"username":username}
    if user.get("id")==None and 'user' in session:
        user=session['user']
    return user

@bp.route('/home')
def home():
    """Login."""
    user =getUser(request,session)
    if  user['id'] ==None:
        msg="User Not Found. Please Register"
        return render_template('login.html',msg=msg)
    else:
        userdataset=db.getIncompleteDataset(user.get("id"))    
        return render_template('index.html', user=user,userDataset=userdataset)


@bp.route('/dologin',methods=('GET', 'POST'))
def doLogin():
    """Process Login."""
    users=db.validateUser(request.form.get("username"),request.form.get("password"))
    if users ==[]:
        msg="User Not Found. Please Register"
        return render_template('login.html',msg=msg)
    else:
        user=users[0]
        session['user'] = user
        userdataset=db.getIncompleteDataset(user.get("id"))
        return render_template('index.html', user=user,userDataset=userdataset)

@bp.route('/register')
def register():
    """Register."""
    return render_template('register.html')

@bp.route('/doregister',methods=('GET', 'POST'))
def doRegister():
    """Process REgistration."""
    user=db.validateUser(request.form.get("username"),request.form.get("password"))
    if user ==[]:
        db.registerUser(request.form.get("username"),request.form.get("password"),request.form.get("name"))
        users=db.validateUser(request.form.get("username"),request.form.get("password"))
        return render_template('index.html', user=users[0])
    else:
        msg="User Found with username "+user[0].get("username")+". Redirected to Login"
        return render_template('login.html',msg=msg)

@bp.route('/questions')
def showQuestions():
    """Show all the Questions."""
    questions=db.getQuestions()
    user =getUser(request,session)
    return render_template('questions.html', question=questions,user=user)


@bp.route('/post', methods=('GET', 'POST'))
def post():
    """Show all the posts, most recent first."""
    answers=[]
    student_id=time.time()+random.randint(1,100000)
    a=b=c=0
    for i in range(1,28):
        if(request.form.get('option'+str(i))==str(1)):
            a=a+1
        if(request.form.get('option'+str(i))==str(2)):
            b=b+1
        if(request.form.get('option'+str(i))==str(3)):        
            c=c+1
        db.addAnswers(student_id,i,request.form.get('option'+str(i)))
    learningStyle=''
    if a > b and a > c:
        learningStyle="Visual"
    if b > a and b > c:
        learningStyle="Auditory"
    if c > b and c> a:
        learningStyle="Kinesthetic"
       
    print(learningStyle)
    user=getUser(request,session)
    return render_template('result.html',learningStyle=learningStyle,user=user)

@bp.route('/knn')
def blog():
    """Run Knn."""
    Xt,Yt=data.loadDataset(0.8,offset=0,cnt=200)
    result=knn.main(Xt,Yt,"learningObject")
    return render_template('knn.html',result=result)

@bp.route('/showResults', methods=('GET', 'POST'))
def showResults():
    """Generate the suggestion."""
    user=getUser(request,session)
    problem=request.form.get('problem')
    learningStyle=request.form.get('learningStyle')
    knowledgeLevel=request.form.get('knowlevel')
    x = Feature()
    x.problem=problem
    x.learningStyle=learningStyle
    x.knowledgeLevel=knowledgeLevel
    x.testPerformance=7
    displayResult={}
    result=knn.predict(x,"path")
    x.path=result
    result1=knn.predict(x,"learningObject")
    x.learningObject=result1
    displayResult['path']=result
    displayResult['learningObject']=result1
    db.addTouserDataset(user.get("id"),x)
    return render_template('final.html',result=displayResult)

@bp.route('/test')
def test():
    """Show all the posts, most recent first."""
    user =getUser(request,session)
    return render_template('result.html',learningStyle="Visual",user=user)

@bp.route('/compare')
def compare():
    """Show all the posts, most recent first."""
    
    time1,accuracy1=comparison.timerAnalysis(3)
    time2,accuracy2=comparison.timerAnalysis(4)
    time3,accuracy3=comparison.timerAnalysis(5)
    return render_template('compare.html',learningStyle="Visual",time1=time1,time2=time2,time3=time3,
    accuracy1=accuracy1,accuracy2=accuracy2,accuracy3=accuracy3)

@bp.route('/taketest')
def takeTest():
    """Show all the posts, most recent first."""
    user =getUser(request,session)
    problem=request.args.get("problem")
    questions=db.getTestQuestions(problem)
    return render_template('test.html',learningStyle="Visual",user=user,problem=problem,questions=questions)

@bp.route('/showResults1', methods=('GET', 'POST'))
def showTestResults():
    """Show all the posts, most recent first."""
    user =getUser(request,session)
    questions=db.getTestQuestions(request.form.get('problem'))
    marks=0
    response=''
    for i in range(1,10):
        ans=request.form.get('problem'+str(i))
        for quest in questions:
            if(i==quest['id']):
                if ans==str(quest['answer']):
                    marks +=2

    if(marks>5):
        response='Y'
        db.insertIntoDataset(user['id'])
    else:
        response='N'
        db.updateUserDataset(str(user['id']),str(marks)+'',"Video")

    return render_template('revise.html',learningStyle="Visual",user=user,response=response,marks=marks)
