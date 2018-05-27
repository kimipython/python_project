#coding=utf-8
from redis import StrictRedis


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


# 开发模式
class Devlopment(config):

    DEBUG = True


# 测试模式
class Test(config):

    Testing = True


# 生产模式
class Product(config):

    DEBUG = False

configs = {
    'pro': Product,
    'dev': Devlopment,
    'test': Test
}