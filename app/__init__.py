# -*- coding=utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap   #引入Flask-Bootstrap
from flask_login import LoginManager    #引入Flask-Login
from config import config
import sys
reload(sys)
sys.setdefaultencoding('utf8')

db = SQLAlchemy()   #实例化对象
bootstrap = Bootstrap() #实例化对象
login_manager = LoginManager()  #实例化对象
login_manager.session_protection = 'strong' #设置flask-login session等级
login_manager.login_view = 'admin.login'    #如果未登入转跳到指定方法
login_manager.login_message = u'请登入账号再进行下一步操作!' #未登入提示语


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app

