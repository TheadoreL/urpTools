#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import jsonify

# urpTools
from urpTools.login import urpLogin
from urpTools.getInfo import getInfo
from urpTools.getScore import getScore

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 验证用户名密码接口
@app.route('/user/verify/<num>/<pwd>')
def userVerify(num, pwd):
    urp = urpLogin([num, pwd])
    return jsonify({'status': urp.isLogin()})

# 获取用户信息接口
@app.route('/user/info/<num>/<pwd>')
def userInfo(num, pwd):
    info = getInfo([num, pwd])
    return jsonify(info.info())

# 获取分数接口
@app.route('/score/<attr>/<num>/<pwd>')
def scores(attr, num, pwd):
    score = getScore([num, pwd])
    if attr == 'all':
        return jsonify({'data': score.getAll()})
    elif attr == 'thisTerm':
        return jsonify({'data': score.getThisTerm()})
    else:
        return jsonify({'data': 'errAttr'})

if __name__ == '__main__':
    app.run()