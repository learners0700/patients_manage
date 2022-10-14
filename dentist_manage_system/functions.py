from flask import request, session
from datetime import datetime
import connect_db as db


def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username != 'admin':
        return '账号有误，请重新输入！'
    else:
        if password == '123':
            session['username'] = username
            return 1
        else:
            return '密码错误，请重新输入！'

def logout():
    session.pop('username')
    return 1

