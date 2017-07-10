# -*- coding=utf-8 -*-

'''
要注意的是，这里可以写入多个配置，就仿照DevelopmentConfig这个类一样，继承Config类即可。
并在最下方的Config字典里添加对应的key:value。
'''

class Config:
    SECRET_KEY = '340221zyc' #填入密钥
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        '''
        _handler = RotatingFileHandler(
            'app.log', maxBytes=10000, backupCount=1)
        _handler.setLevel(logging.WARNING)
        app.logger.addHandler(_handler)
        '''
        pass

class DevelopmentConfig(Config):
        SQLALCHEMY_DATABASE_URI = 'mysql://root:********@localhost/exam'
    #SQLALCHEMY链接数据库都是以URI方式格式为'mysql://账户名:密码@地址/数据库表名'

config = {
    'default': DevelopmentConfig
}
