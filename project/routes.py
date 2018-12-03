from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import time
import random
from werkzeug.exceptions import abort
from project import db
from project import knn
bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """Show all the posts, most recent first."""
    questions=db.getQuestions()
    return render_template('index.html', question=questions)

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
        learningStyle="You have a VISUAL learning style"
    if b > a and b > c:
        learningStyle="You have an AUDITORY learning style"
    if c > b and c> a:
        learningStyle="You have a KINAESTHETIC learning style"
       
    print(learningStyle)
    return render_template('result.html',learningStyle=learningStyle)

@bp.route('/knn')
def blog():
    """Run Knn."""
    result=knn.main()
    return render_template('knn.html',result=result)

@bp.route('/showResults', methods=('GET', 'POST'))
def showResults():
    """Generate the suggestion."""
    problem=request.form.get('problem')
    learningStyle=request.form.get('learningStyle')
    knowledgeLevel=request.form.get('knowlevel')
    
    return render_template('knn.html',result=result)

@bp.route('/test')
def course():
    """Show all the posts, most recent first."""

    return render_template('result.html',learningStyle="VISUAL")
