# -*- coding=utf-8 -*-
from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # 引入密码加密 验证方法
from flask_login import UserMixin  # 引入flask-login用户模型继承类方法


class Marks_record(db.Model):
    __tablename__ = 'marks_record'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username=db.Column(db.String(64))
    time=db.Column(db.DATETIME,default=datetime.utcnow())
    Q_ID=db.Column(db.Integer)
    Select=db.Column(db.String(64))
    mark=db.Column(db.String(64))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    permission = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError(u'密码属性不正确')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        # 增加password会通过generate_password_hash方法来加密储存

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        # 在登入时,我们需要验证明文密码是否和加密密码所吻合

class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer, primary_key=True)
    Stem = db.Column(db.Text)
    Select_1 = db.Column(db.Text)
    Select_2 = db.Column(db.Text)
    Select_3 = db.Column(db.Text)
    Select_4 = db.Column(db.Text)
    Select_Right = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))