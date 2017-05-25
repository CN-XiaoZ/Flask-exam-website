# -*- coding=utf-8 -*-
from . import main
from flask import render_template, flash, redirect, url_for, request,session,make_response
from flask_login import login_required, current_user, login_user, logout_user
from forms import LoginForm,Answer
from ..models import Marks_record , User , Question
from .. import db
from flask import current_app

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
    t = session.get('done')
    if t==1:
        return redirect(url_for('main.mark'))
    form=Answer()
    Right=Question.query.filter_by(id=page).first()
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
        record = Marks_record(username=session.get('name'),Q_ID=page,Select=form.answer.data,mark=(a==Right.Select_Right))
        db.session.add(record)
        flash(u'答案提交成功')
    result = Question.query.filter_by(id=page).first()
    return render_template('main/record.html', result=result,page=page,form=form)

@main.route('/mark', methods=['GET', 'POST'])
@login_required
def mark():
    marks=0
    for i in range(1, 11):
        results = Marks_record.query.filter_by(username=session.get('name'),Q_ID=i).order_by(-Marks_record.id).first()
        print('1')
        if (results == None):
            print('0')
            return redirect(url_for('main.record', page=i))
        else:
            if (results.mark == '1'):
                marks = marks + 1
    session["done"] = 1  # 设置session'

    return render_template('main/mark.html', mark=marks)

@main.route('/Before_exam', methods=['GET', 'POST'])
@login_required
def Before():
    return render_template('main/Before_exam.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经登出了系统')
    return redirect(url_for('main.login'))
