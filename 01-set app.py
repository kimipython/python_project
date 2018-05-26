#coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask import session
# 配置文件的加载


class config(object):
    # 开启测试模式
    DEBUG = True

    #  配置数据库的加载，连接信息

    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/flask_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis，建立连接
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = 6379
    DB = 10
    # 设置密钥
    SECRET_KEY = 'jijiewohohjajdcfh'
    # 设置session使用的什么莱存储
    SESSION_TYPE = 'redis'
    #  设置session存储的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_POST,db=DB)
    SESSION_USE_SIGNER = True
app = Flask(__name__)

# 在app里获取加载信息

app.config.from_object(config)

# 在app里获取mysql数据库的对象
db = SQLAlchemy(app)
# 在app里获取StrictRedis的信息
redis_link = StrictRedis(host=config.REDIS_HOST,port=config.REDIS_POST,db=config.DB)

# 开启csrf保护，由于现在使用的不是wtform表单，所有必须使用csrf莱进行保护
CSRFProtect(app)

# 设置session
Session(app)


@app.route('/')
def index():
    session['age'] = '18'
    return 'kimi'

if __name__ == '__main__':

    app.run(port=8888)