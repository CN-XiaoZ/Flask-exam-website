# -*- coding=utf-8 -*-
from flask_wtf import Form
from ..models import Question
from wtforms import StringField, SubmitField, PasswordField, TextAreaField,RadioField
from wtforms.validators import Required, length, Regexp, EqualTo,AnyOf
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class LoginForm(Form):
    username = StringField(u'帐号', validators=[Required(), length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'登入')
class Answer(Form):
    answer= StringField(u'答案,只允许填入A,B,C,D',validators=[AnyOf(values=['A','B','C','D'], message='只允许填入A,B,C,D')])
    submit = SubmitField(u'确认')

class RegistrationForm(Form):
    username = StringField(u'用户名', validators=[Required(), length(2, 128)])
    password = PasswordField(
        u'密码', validators=[Required(), EqualTo('password2', message=u'两次密码不一致')])
    password2 = PasswordField(u'重复密码', validators=[Required()])
    # real_name = StringField(u'昵称', validators=[Required()])
    registerkey = StringField(u'注册码', validators=[Required()])
    submit = SubmitField(u'注册')
