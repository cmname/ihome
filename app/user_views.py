import os
import random
import re

from flask import Blueprint, render_template, request, jsonify, session

from utils import status_code
from app.models import User
from utils.function import login_require, is_login
from utils.setting import MEDIA_PATH

user_blue = Blueprint('user', __name__)


@user_blue.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整的参数'})
    # 2.验证手机号是否正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1002, 'msg': '手机号不正确'})
    # 3.验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码不正确'})
    # 4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '密码不一致'})
    # 验证手机号是否已注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code': 1005, 'msg': '手机号已被注册，请重新注册'})
    # 创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码图片的地址
    # 方式2：后端只生成随机参数，返回给页面，在页面中再生成图片
    s = '90qwe1rty2uio3pas4dfg5hjk6lzx7c8vbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blue.route('/my_login/', methods=['POST'])
def my_login():
    # 实现登录
    phone = request.form.get('phone')
    pwd = request.form.get('pwd')
    # 1.校验参数是否填写完整
    if not all([phone, pwd]):
        return jsonify({'code': 1006, 'msg': '请将请求参数填写完整'})
    # 2.获取手机号对应的用户信息
    user = User.query.filter(User.phone == phone).first()
    if not user:
        return jsonify({'code': 1007, 'msg': '该账号没有注册，请先注册'})
    # 3.校验密码是否正确
    if not user.check_pwd(pwd):
        return jsonify({'code': 1008, 'msg': '密码不正确'})
    # 4.登录标识设置
    session['user_id'] = user.id
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/my/', methods=['GET'])
def my():
    return render_template('my.html')


@user_blue.route('/user_info/', methods=['GET'])
def user_info():
    # 获取用户基本信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify({'code': 200, 'msg': '请求成功', 'data': user.to_basic_dict()})


@user_blue.route('/logout/', methods=['DELETE'])
def logout():
    session.clear()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/profile/')
def profile():
    return render_template('profile.html')


@user_blue.route('/profile/', methods=['PATCH'])
def mmy_profile():
    if request.method == 'PATCH':
        avatar = request.files.get('avatar')
        if avatar:
            # 判断图片格式是否正确
            if not re.match(r'image/*', avatar.mimetype):
                return jsonify({'code': 1009, 'msg': '请上传正确的图片格式'})
            # 保存图片
            avatars = os.path.join(MEDIA_PATH, avatar.filename)
            avatar.save(avatars)
            # 修改图片字段
            user = User.query.get(session['user_id'])
            user.avatar = avatar.filename
            try:
                user.add_update()
                return jsonify(code=200, avatar=avatar)
            except:
                return jsonify({'code': 1010, 'mag': '错误'})


@user_blue.route('/profile/', methods=['POST'])
def my_profile():
    name = request.form.get('name')
    if name:
        if User.query.filter(User.name == name).count():
            return jsonify({'code': 1011, 'msg': '错误'})
        user = User.query.get(session['user_id'])
        user.name = name
        try:
            user.add_update()
            return jsonify(code=200)
        except:
            return jsonify({'code': 1012, 'msg': '错误'})


@user_blue.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


@user_blue.route('/auth/', methods=['POST'])
def my_auth():
    read_name = request.form.get('read_name')
    id_card = request.form.get('id_card')
    if not all([read_name, id_card]):
        return jsonify({'code': 1013, 'msg': '错误'})
    if not re.match(r'[1-9]\d{16}[0-9X]', id_card):
        return jsonify({'code': 1014, 'msg': '错误'})

    user = User.query.get(session['user_id'])
    user.id_name = read_name
    user.id_card = id_card
    try:
        user.add_update()
        return jsonify(code=status_code.OK)
    except Exception as e:
        print(e)
        return jsonify({'code': 1015, 'msg': '错误'})


@user_blue.route('/read_user_info/', methods=['GET'])
def read_user_info():
    user = User.query.get(session['user_id'])
    user = user.to_auth_dict()
    return jsonify(code=status_code.OK, user=user)