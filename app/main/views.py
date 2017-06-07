# -*- coding=utf-8 -*-
from . import main
from flask import render_template, flash, redirect, url_for, request,session,make_response
from flask_login import login_required, current_user, login_user, logout_user
from forms import LoginForm,Answer,RegistrationForm
from ..models import Marks_record , User, Question
from .. import db
from functools import wraps
from flask import current_app
import string
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def Admin_Rquire(func):
    @wraps(func)
    def ADMIN(*args, **kwargs):
        PER = User.query.filter_by(username=session.get('name')).first()
        if PER.permission==0:
            return func(*args, **kwargs)
        else:
            flash(u'你不是管理员')
            return redirect(url_for('main.index'))
    return ADMIN

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['name']=form.username.data
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户密码不正确')

    return render_template('main/login.html', form=form)

@main.route('/record/int:<page>', methods=['GET', 'POST'])
@login_required
def record(page):
    A = User.query.filter_by(username=session.get('name')).first()
    a=A.list.split(' ')
    if A.done==1:
        return redirect(url_for('main.mark'))
    form=Answer()
    page=int(page)
    print(page)
    result=Question.query.filter_by(id=a[page-1]).first()
    if form.validate_on_submit():
        t = session.get('done')
        if t == 1:
            return redirect(url_for('main.mark'))
        a=form.answer.data
        if a=='A':
            a=1
        elif a=='B':
            a=2
        elif a=='C':
            a=3
        else:
            a=4
        record = Marks_record(username=session.get('name'),Q_ID=page,Select=form.answer.data,mark=(a==result.Select_Right))
        db.session.add(record)
        flash(u'答案提交成功')
    return render_template('main/record.html', result=result,page=page,form=form)

@main.route('/mark', methods=['GET', 'POST'])
@login_required
def mark():
    marks=0
    A = User.query.filter_by(username=session.get('name')).first()
    b=A.list
    a=b.split(' ')
    for i in range(1, 21):
        print(i)
        results = Marks_record.query.filter_by(username=session.get('name'),Q_ID=i).order_by(-Marks_record.id).first()
        if (results == None):
            flash(u'你还有题目没有回答,跳转至未回答页')
            return redirect(url_for('main.record', page=i))
        else:
            if (results.mark == '1'):
                marks = marks + 5
    A.done=1
    db.session.commit()
    return render_template('main/mark.html', mark=marks)

@main.route('/Before_exam', methods=['GET', 'POST'])
@login_required
def Before():
    return render_template('main/Before_exam.html')


@main.route('/register', methods=['GET', 'POST'])
@Admin_Rquire
def register():
    register_key = 'zhucema'
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.registerkey.data != register_key:
            flash(u'注册码不符，请返回重试')
            return redirect(url_for('main.register'))
        else:
            if form.password.data != form.password2.data:
                flash(u'两次输入密码不一')
                return redirect(url_for('main.register'))
            else:
                try:
                    user = User(username=form.username.data, permission=1, password=form.password.data)
                    print(user.password_hash)
                    print(user.permission)
                    print(user.username)
                    db.session.add(user)
                    print('done')
                    print('done')
                    flash(u'您已经成功注册')
                    return redirect(url_for('main.login'))
                except:
                    db.session.rollback()
                    flash(u'用户名已存在')
    return render_template('main/register.html', form=form)

@main.route('/out', methods=['GET', 'POST'])
@Admin_Rquire
def out():
    username=[]
    mark=[]
    name=User.query.all()
    marks=0
    for name in name:
        username.append(name.username)
    for name in username:
        for i in range(1, 21):
            results = Marks_record.query.filter_by(username=name, Q_ID=i).order_by(-Marks_record.id).first()
            if (results == None):
                marks=0
                break
            else:
                if (results.mark == '1'):
                    marks = marks + 5
        mark.append(marks)
        marks=0
    le=len(username)
    print le
    return render_template('main/out.html',mark=mark,username=username,len=le)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经登出了系统')
    return redirect(url_for('main.login'))

