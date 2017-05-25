# Flask 实现的考试网站


## 一. 功能:

* 登入(查询数据库并加密)
* 登出(操作cookies)
* 考试(从数据库中查询数据并写入数据)
* 分数统计(数据库端进行计算并且通过表的合理分配了运行的计算量)
* 防止再次进行考试(操作cookies)
* 防止忘记填入答案(最终提交时对于表进行查询和反馈)

## 二. 运行环境

需求插件以及版本号使用`pip`写入到`requirements.txt`文件中.

* 操作系统: `Ubuntu 16.04 LTS`
* 数据库平台: `MySQL Ver 14.14 Distrib 5.7.18, for Linux (x86_64) `
* 编程语言: `Python 2.7.12`以及`HTML`的`Jinja2`引擎
* 框架: `Flask`
* 所需插件以及版本号:写入`/src`下`requirements.txt`文件夹下

## 三. 系统架构

### 文件结构以及文件作用:

文件夹有

* `/app` :保存程序主文件

 * `/main`: 保存了主要的程序运行文件
   * `errors.py`: 访问错误例如404,500等错误时返回的页面的路由
   * `forms.py`: 记录了表单的类
   * `views.py`: 视图文件,记录网站路由,运行逻辑,程序定义,用户管理,cookies管理等
   * `__init__.py`: 初始化main蓝图,蓝图的作用是可以进行多页面,例如之后可以加入一个admin蓝图进行用户管理.
 * `/static`: 静态文件,图标等
 * `/templates`: `Jinja2`文件,用来渲染出网页,主要为HTML文件
 * `__init__.py`:程序初始化文件,初始化各种程序实例
 * `models.py`: 数据库模型文件,插件`SQLAlchemy`会根据这个文件内容连接到数据库进行数据库和表的建立.

* `/migrations`: 数据库迁移的备份文件,通过插件`Flask-Migrate`进行管理

* `/venv`: 虚拟环境文件,通过`virtualenv`建立一个有单独的Python版本,和其他插件版本的虚拟运行环境.

* `config.py`: 配置文件,保存了这个系统的CSRF的安全秘钥,防止跨站请求,也保存了数据库连接的地址,在这个系统中连接到本地的数据库是使用

 `SQLALCHEMY_DATABASE_URI = 'mysql://root:340221zyc@localhost/exam'`

 语句,代表连接到MySQL数据库,用户名为root,密码为340221zyc,地址为localhost,数据库名为exam`

* `manage.py` :设定配置方式和管理程序的总开关.

### 操作说明:

如果需要运行这个网站,请先在数据库建立一个名为`exam`的数据库,并在`config.py`文件中改写数据库地址,安装`Python 2.7.12`,到`requirements.txt`的目录下运行`pip install -r requirements.txt `进行依赖包的安装,

然后进入Python环境,`cd`到`manage.py`的目录下输入`python manage.py db init`进行数据库建立,并且输入

`python manage.py db migrate -m "first init db"`

`python manage.py db upgrade`

进行数据库迁移备份.

并输入`python manage.py runserver`建立本地的web服务器,进入浏览器输入127.0.0.0:5000进行访问.

如果运行出错,请用Pycharm进行运行.

另外因用户的注册界面仍有没有解决的bug,所以加入用户和题目请手动加入MySQL的数据库.

由于用户密码是哈希值储存,手动加入用户时请使用以下方法获取哈希值

```python
Python 2.7.12 (default, Nov 19 2016, 06:48:10)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from werkzeug.security import generate_password_hash
>>> password_hash=generate_password_hash('21zyc')
>>> print(password_hash)
pbkdf2:sha1:1000$MPN0TwYB$78b21264445651fbd176413e6ee17b00e6362aff
>>>
# 21zyc是明文密码
# pbkdf2:sha1:1000$MPN0TwYB$78b21264445651fbd176413e6ee17b00e6362aff为哈希值
# 直接存入哈希值.
```



### 运行逻辑:

数据库在启动之前通过python进行部署,方法在上面已经给出

之后运行,进入首页,点击登录可以进入登录页面

使用`Flask-Login`进行登录管理,密码因为需要进行http传输,所以进行了哈希变换之后存入数据库,数据库存储密码哈希值

登录之后可以进行考试,每个题目可以重复提交,最后计分的时候会提出最后一次的提交信息进行计分

考试界面会判断当前的用户是否进行过考试,如果已经进行会重定向到分数显示界面.

### 数据库的运行逻辑:

分为三个表:

```python
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
       raise AttributeError(u'别想看明文密码嘿嘿嘿')

   @password.setter
   def password(self, password):
       self.password_hash = generate_password_hash(password)

   def verify_password(self, password):
       return check_password_hash(self.password_hash, password)

class Question(db.Model):
   __tablename__='question'
   id = db.Column(db.Integer, primary_key=True)
   Stem = db.Column(db.Text)
   Select_1 = db.Column(db.Text)
   Select_2 = db.Column(db.Text)
   Select_3 = db.Column(db.Text)
   Select_4 = db.Column(db.Text)
   Select_Right = db.Column(db.Integer)
```

* 表`marks_record`: 记录每一次答案提交
 * id: 自动增加,主键.整数型
 * username: 提交答案的用户
 * time: 提交时间(还未完成,需要进行计时,限定时间完成)
 * Q_ID: 题目的题号
 * Select: 本次提交的答案
 * mark: 本次提交的答案是否得分
* 表`users`:
 * id: 主键
 * username: 用户名字
 * permission: 权限值,为0可以进行某些操作,还未完成.
 * password_hash: 用户密码的哈希值
* 表`question`:
 * id: 题目的题号
 * Stem: 题干
