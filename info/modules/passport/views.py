#coding=utf-8

from info.modules.passport import passport_blu
from flask import request,abort,jsonify
from info import redis_link,constants
from info.utils.captcha.captcha import captcha
import logging
from flask import json,session
from info import response_code,db
import re,datetime
import random
from info.thirdlibs.yuntongxun.sms import CCP
from info.models_1 import User

def register():
    '''
    注册:
    1.接受参数
    2.校验参数
    3.查询服务器的短信验证码
    4.跟客户输入的短信验证码进行比较
    5.成功，就创建user模型对象，失败就重新输入
    6.将数据同步到数据库中
    7.保持状态的，实现注册及登录
    8.响应注册结果
    :return:
    '''
    # 1 接受参数
    json_dict = request.json
    mobile = json_dict.get('mobile')
    sms_code = json_dict.get('sms_code')
    password = json_dict.get('password')
    if not all([mobile,sms_code,password]):
        return jsonify(errno=response_code.RET.PARAMERR,errmsg='缺少参数')
    if not re.match('^1[3456789][0-9]{9}$',mobile):
        return jsonify(errno=response_code.RET.PARAMERR,errmsg='手机号有误')

    try:
        sms_code_server = redis_link.get('SMS'+mobile)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.DBERR,errmsg='数据库获取数据失败')
    if not sms_code_server:
        return jsonify(errno=response_code.RET.NODATA,errmsg='短信验证码不存在')
    if sms_code != sms_code_server:
        return jsonify(errno=response_code.RET.DATAERR,errmsg='短信验证码有误')
    user = User()
    user.mobile = mobile
    user.nick_name = mobile
    user.password_hash = password
#     记录最后一次登录时间
    user.last_login = datetime.datetime.now()

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=response_code.RET.DBERR,errmsg='同步数据库失败')

    session['user_id'] = user.id
    session['mobile'] = user.mobile
    session['nick_name'] = user.nick_name
    return jsonify(errno=response_code.RET.OK,errmsg='数据同步成功')

@passport_blu.route('/sms_code',methods=['POST'])
def sms_code():
     '''
     发送短信
     1.接受参数（手机号，图片验证码）
     2.校验参数是否齐全，手机号是否正确
     3.查询服务器存储的图片验证码
     4.进行校验
     5.对比成功，发送短信验证码，并发送短信
     6.存储读阿妈性验证码到redis，方便注册时比较
     7.响应短信验证码的验证结果'''

     json_str = request.data
     json_dict = json.loads(json_str)
     mobile = json_dict.get('mobile')
     image_code = json_dict.get('image_code')
     image_code_id = json_dict.get('image_code_id')

     if not all([mobile,image_code,image_code_id]):
         return jsonify(errno=response_code.RET.PARAMERR,errmsg='参数有误' )

     if not re.match(r'^1[345678][0-9]{9}$', mobile):
         return jsonify(errno=response_code. RET.PARAMERR,errmsg='参数有误')

     try:
         image_code_server = redis_link.get('ImageCodeId:'+image_code_id).decode()
     except Exception as e:
         logging.error(e)
         return jsonify(errno=response_code.RET.DBERR,errmsg='数据库读取有误')
     if not image_code_id:
         return jsonify(errno=response_code.RET.NODATA,errmsg='图形验证码不存在')
     if image_code.lower() != image_code_server.lower():
         return jsonify(errno=response_code.RET.DATAERR,errmsg='图形验证码错误')

     sms_code = '%06d'%random.randint(0,999999)
     print('短信验证码：', sms_code)
     send_sms_code = CCP().send_template_sms(mobile,[sms_code,5],1)
     if send_sms_code !=0:
         return jsonify(errnp=response_code.RET.LOGINERR,errmsg='登录失败')
     try:
         redis_link.set('SMS'+mobile,'sms_code',constants.IMAGE_CODE_REDIS_EXPIRES)
     except Exception as e:
         logging.error(e)
         return jsonify(errno=response_code.RET.DBERR,errmsg='存储数据失败')

     return jsonify(errno=response_code.RET.OK ,errmsg='存储成功')


@passport_blu.route('/image_code',methods=['GET'])
def image_code():
    # 提供图片验证码

    imageCodeId = request.args.get('imageCodeId')
    if not imageCodeId:
        abort(403)
    name, text, image = captcha.generate_captcha()
    try:
        redis_link.set('ImageCodeId:'+imageCodeId,text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        logging.error(e)
        abort(500)
    print(text)
    return image