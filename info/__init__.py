#coding=utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import configs


def creat_app(config_name):
    app = Flask(__name__)

    # 在app里获取加载信息

    app.config.from_object(configs[config_name])

    # 在app里获取mysql数据库的对象
    db = SQLAlchemy(app)
    # 在app里获取StrictRedis的信息
    redis_link = StrictRedis(host=configs[config_name].REDIS_HOST,port=configs[config_name].REDIS_POST,db=configs[config_name].DB)

    # 开启csrf保护，由于现在使用的不是wtform表单，所有必须使用csrf莱进行保护
    CSRFProtect(app)

    # 设置session数据名存储的位置
    Session(app)

# 将新创键的app返回回去

    return app


