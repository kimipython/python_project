#coding=utf-8


from flask import Flask

app = Flask(__name__)


def index():
    return 'kimi'

if __name__ == '__main__':
    app.run()