#coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
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
app = Flask(__name__)

# 在app里获取加载信息

app.config.from_object(config)

# 在app里获取mysql数据库的对象
db = SQLAlchemy(app)
# 在app里获取StrictRedis的信息
redis_link = StrictRedis(host=config.REDIS_HOST,port=config.REDIS_POST,db=config.DB)




@app.route('/')
def index():
    return 'kimi'

if __name__ == '__main__':

    app.run(port=8888)