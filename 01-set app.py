#coding=utf-8

from flask import Flask

# 配置文件的加载


class config(object):
    # 开启测试模式
    DEBUG = True

app = Flask(__name__)

# 在app里获取加载信息

app.config.from_object(config)


@app.route('/')
def index():
    return 'kimi'

if __name__ == '__main__':
    app.run()