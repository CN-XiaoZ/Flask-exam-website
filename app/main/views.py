# -*- coding=utf-8 -*-
from . import main
from flask import render_template, flash, redirect, url_for, request,session,make_response
from flask_login import login_required, current_user, login_user, logout_user
from forms import LoginForm,Answer,RegistrationForm
from ..models import Marks_record , User, Question
from .. import db
from flask import current_app
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def Admin_Rquire(func):
    def ADMIN(*args, **kwargs):
        PER = User.query.filter_by(username=session.get('name')).first()
        if PER.permission==0:
            return func(*args, **kwargs)
        else:
            flash(u'你不是管理员')
            return redirect(url_for('main.index'))
    return ADMIN
#     def ADMIN(*args, **kwargs):
#         PER = User.query.filter_by(username=session.get('name')).first()
#         if not current_user.is_authenticated:
#             return func(*args, **kwargs)
#         elif PER.Permission==0:
#             return func(*args, **kwargs)
        # if not current_user.is_authenticated:
        #     return func(*args, **kwargs)
        # else:
        #     PER = User.query.filter_by(username=session.get('name')).first()
        #     if PER.Permission==0:
        #         return func(*args, **kwargs)
        #     else:
        #         return redirect(url_for('main.index'))
        # return func(*args, **kwargs)

        # if request.method in EXEMPT_METHODS:
        #     return func(*args, **kwargs)
        # elif current_app.login_manager._login_disabled:
        #     return func(*args, **kwargs)
        # elif not current_user.is_authenticated:
        #     return current_app.login_manager.unauthorized()
        # return func(*args, **kwargs)
    # return ADMIN


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

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经登出了系统')
    return redirect(url_for('main.login'))

