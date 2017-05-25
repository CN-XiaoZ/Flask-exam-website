# -*- coding=utf-8 -*-
from flask_wtf import Form
from ..models import Question
from wtforms import StringField, SubmitField, PasswordField, TextAreaField,RadioField
from wtforms.validators import Required, length, Regexp, EqualTo,AnyOf
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(Form):
    username = StringField(u'帐号', validators=[Required(), length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'登入')
class Answer(Form):
    answer= StringField(u'答案,只允许填入A,B,C,D',validators=[AnyOf(values=['A','B','C','D'], message='只允许填入A,B,C,D')])
    submit = SubmitField(u'确认')