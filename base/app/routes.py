from app import app, db
from app.models import *
from app.forms import *
import json, requests, socket, os
from flask import render_template, flash, redirect, url_for, request, jsonify, send_from_directory,flash
from werkzeug.urls import url_parse
from wtforms.validators import ValidationError
from sqlalchemy import func, or_
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
import random


@app.route('/')
@app.route('/index')
def index():
    questions = Question.query.all()
    count = 0
    for i in questions:
        count += 1
    id_1, id_2, id_3 = random.sample(range(1, count), 3)
    question_1 = Question.query.filter_by(id=id_1).first()
    question_2 = Question.query.filter_by(id=id_2).first()
    question_3 = Question.query.filter_by(id=id_3).first()
    user_1 = User.query.filter_by(id=question_1.userid).first()
    user_2 = User.query.filter_by(id=question_2.userid).first()
    user_3 = User.query.filter_by(id=question_3.userid).first()
    questions = [1,2,3,4,5]
    return render_template('index.html',question_1 = question_1, question_2 = question_2,
                            question_3 = question_3,questions=questions, user_1 = user_1,
                            user_2 = user_2, user_3=user_3)

@app.route('/youranswers')
@login_required
def youranswers():
    user = current_user.get_id()
    responses = Response.query.filter_by(user=user)
    questions = Question.query.all()
    tuplelist = {()}
    # for i in responses:
    return render_template('youranswers.html', responses=responses, questions =questions)

@app.route('/submitthanks')
def submitthanks():
    return render_template('submitthanks.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/youranswers', methods=['GET', 'POST'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, usertype=form.usertype.data)
        user.set_password(form.password.data)
        user.set_nric(form.nric.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login')), flash('Congratulations, you are now a registered user!')
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/yourquestions')
@login_required
def yourquestions():
    questions = Question.query.filter_by(userid=current_user.id)
    return render_template('yourquestions.html',questions=questions)

@app.route('/result/<int:questionid>',methods=['GET','POST'])
@login_required
def result(questionid):
    question = Question.query.filter_by(id=questionid).first()
    responses = Response.query.filter_by(question=questionid)
    name = question.questionTitle
    user = current_user.get_id()
    user = User.query.filter_by(id=user).first()
    data = []
    labels = []
    if question.questionType == 'mcq' or question.questionType == 'yesno':
        questionOption = question.questionOption
        labels = questionOption.split(",")
        dict = {}
        for i in labels:
            for x in responses:
                if i == x.response:
                    if i not in dict.keys():
                        dict[i] = 1
                    else:
                        dict[i] +=1
                else:
                    if i not in dict.keys():
                        dict[i] = 0
                    else:
                        dict[i] +=0
        for i in dict.values():
            data.append(i)
        print(data)
        return render_template("result_chart.html", labels=labels, data=data, name=name)
    else:
        return render_template("result_forum.html", question=question, responses=responses)

@app.route('/askquestion',methods=['GET','POST'])
def askquestion():
    return render_template('askquestion.html')

@app.route('/askquestion/yesno',methods=['GET','POST'])
@login_required
def askquestionyesno():
    news = requests.get('https://newsapi.org/v2/top-headlines?country=sg&category=business&apiKey=7bfce5438bd148d4aee3f50109c32279')
    news = news.json()['articles']
    randNums = []
    while len(randNums) < 3:
        randNum = random.randint(0,len(news)-1)
        if randNum not in randNums:
            randNums.append(randNum)
    newsTable = []
    for x in randNums:
        filtered = news[x]
        title = filtered['title'][0:30]+'...'
        newsTable.append([title,filtered['url']])
    return render_template('askquestionyesno.html',newsTable=newsTable)

@app.route('/askquestion/mcq',methods=['GET','POST'])
@login_required
def askquestionmcq():
    news = requests.get('https://newsapi.org/v2/top-headlines?country=sg&category=business&apiKey=7bfce5438bd148d4aee3f50109c32279')
    news = news.json()['articles']
    randNums = []
    while len(randNums) < 3:
        randNum = random.randint(0,len(news)-1)
        if randNum not in randNums:
            randNums.append(randNum)
    newsTable = []
    for x in randNums:
        filtered = news[x]
        title = filtered['title'][0:30]+'...'
        newsTable.append([title,filtered['url']])
    return render_template('askquestionmcq.html',newsTable=newsTable)

@app.route('/askquestion/openended',methods=['GET','POST'])
@login_required
def askquestionopenended():
    news = requests.get('https://newsapi.org/v2/top-headlines?country=sg&category=business&apiKey=7bfce5438bd148d4aee3f50109c32279')
    news = news.json()['articles']
    randNums = []
    while len(randNums) < 3:
        randNum = random.randint(0,len(news)-1)
        if randNum not in randNums:
            randNums.append(randNum)
    newsTable = []
    for x in randNums:
        filtered = news[x]
        title = filtered['title'][0:30]+'...'
        newsTable.append([title,filtered['url']])
        print(filtered['url'])
    return render_template('askquestionopenended.html',newsTable=newsTable)

@app.route('/askquestion/yesnosubmit',methods=['GET','POST'])
@login_required
def askquestionyesnosubmit():
    questionTitle = request.form['question']
    questionOption = "yes,no"
    user = current_user.get_id()
    type = 'yesno'
    question = Question(questionTitle=questionTitle,questionOption=questionOption,userid=user,questionType=type)
    db.session.add(question)
    db.session.commit()
    return render_template('submitthanks.html')
    # return render_template('askquestionyesno.html')

@app.route('/askquestion/mcqsubmit',methods=['GET','POST'])
@login_required
def askquestionmcqsubmit():
    number = request.form['number']
    questionTitle = request.form['question']
    questionOption =''
    for i in range (int(number)):
        if i == 0:
            questionOption = str(request.form["option"+str(i)])
        else:
            questionOption += ","+str(request.form["option"+str(i)])
    user = current_user.get_id()
    type = 'mcq'
    question = Question(questionTitle=questionTitle,questionOption=questionOption,userid=user,questionType=type)
    db.session.add(question)
    db.session.commit()
    return render_template('submitthanks.html')
    # return render_template('askquestionyesno.html')

@app.route('/askquestion/openendedsubmit',methods=['GET','POST'])
@login_required
def askquestionopenendedsubmit():
    questionTitle = request.form['question']
    questionOption = "open"
    user = current_user.get_id()
    type = 'open'
    question = Question(questionTitle=questionTitle,questionOption=questionOption,userid=user,questionType=type)
    db.session.add(question)
    db.session.commit()
    return render_template('submitthanks.html')


@app.route('/replyquestion/<int:questionid>', methods = ['GET','POST','PUT'])
@login_required
def replyquestion(questionid):
    question = Question.query.filter_by(id=questionid).first()
    user = current_user.get_id()
    users = User.query.filter_by(id=user).first()
    options = ''
    if question.questionType == 'mcq':
        form = FreeTxt()
        questionOption = question.questionOption
        options = questionOption.split(",")
        if request.method == 'POST':
            # print(request.form.values)
            option = request.form['option']
            response = Response(user=user,question=questionid,response=option)
            db.session.add(response)
            db.session.commit()
            users.points = users.points + 1
            db.session.commit()
            print('submitted')
            return render_template('submitthanks.html')
    elif question.questionType == 'open':
        form = FreeTxt()
        if form.validate_on_submit():
            response = Response(user=user,question=questionid,response=form.options.data)
            db.session.add(response)
            db.session.commit()
            users.points = users.points + 1
            db.session.commit()
            return render_template('submitthanks.html')
        else:
            flash('error in response try again')
        # return render_template('yesno.html', form=form, question=question)
    else:
        form = Boolean()
        if request.method == 'POST':
            option = request.form['option']
            response = Response(user=user,question=questionid,response=option)
            db.session.add(response)
            db.session.commit()
            users.points = users.points + 1
            db.session.commit()
            print('submitted')
            return render_template('submitthanks.html')
        else:
            flash('error in response try again')
    return render_template('yesno.html', form=form, question=question, options=options)

# @app.route('/replyquestion/yesno<questionid>', methods = ['GET','POST'])
# def yesno(questionid):
#     question = Question.query.filter_by(id=questionid).first()
#     form = Boolean()
#     return render_template('yesno.html', form=form, question=question)
#
# @app.route('/replyquestion/opentxt<int:id>', methods = ['GET','POST'])
# def OpenTxt(id):
#     question = Question.query.filter_by(id=id).first()
#     form = FreeTxt()
#     question = "Do you have a problem?"
#     return render_template('yesno.html', form=form, question=question)

@app.route('/redeem',methods=['GET','POST'])
def redeem():
    return render_template('redeem.html')
