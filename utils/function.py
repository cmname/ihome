
# 外层函数嵌套内层函数
# 外层函数返回内层函数
# 内层函数调用外层函数的参数

from functools import wraps
from flask import session, redirect, url_for
from flask import session as user_session

import functools


def login_require(func):
    @wraps(func)
    def check(*args, **kwargs):
        if 'user_id' in session:
            # 判断session中是否存在登录的标识user_id
            return func(*args, **kwargs)
        else:
            # 没有登录，跳转到登录页面
            return redirect(url_for('user.login'))
    return check


def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator():
        try:
            if 'user_id' in user_session:
                return view_fun()
            else:
                return redirect('/user/login/')
        except Exception as e:
            return redirect('/user/login/')
        return decorator