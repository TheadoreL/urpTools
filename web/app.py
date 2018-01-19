#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

# urpTools
from urpTools.login import urpLogin
from urpTools.getInfo import getInfo
from urpTools.getScore import getScore
from urpTools.putScore import putScore

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

# 教师获取学期接口
@app.route('/teacher/terms/<num>/<pwd>')
def getTerms(num, pwd):
    scores = putScore([num, pwd])
    return jsonify({'data': scores.getTerms()})

# 教师获取成绩系数列表接口
@app.route('/teacher/coef/list/<num>/<pwd>/<term>')
def getCoefList(num, pwd, term):
    scores = putScore([num, pwd])
    return jsonify({'data': scores.getCoefList(term)})

# 教师保存成绩系数接口
@app.route('/teacher/coef/save/<num>/<pwd>/<term>/<classNum>/<classSeq>/<dailyScore>/<examScore>')
def saveScoreCoef(num, pwd, term, classNum, classSeq, dailyScore, examScore):
    scores = putScore([num, pwd])
    return jsonify({'data': scores.saveCoef(term, classNum, classSeq, dailyScore, examScore)})

# 教师获取成绩系数接口
@app.route('/teacher/coef/get/<num>/<pwd>/<term>/<classNum>/<classSeq>')
def getScoreCoef(num, pwd, term, classNum, classSeq):
    scores = putScore([num, pwd])
    return jsonify({'data': scores.getCoef(term, classNum, classSeq)})

# 教师获取课程列表接口
@app.route('/teacher/class/list/<num>/<pwd>/<term>')
def getClassList(num, pwd, term):
    scores = putScore([num, pwd])
    return jsonify({'data': scores.getClassList(term)})

# 教师判断成绩系数是否录入接口
@app.route('/teacher/coef/verify/<num>/<pwd>/<term>/<classNum>/<classSeq>/<classType>')
def verifyCoef(num, pwd, term, classNum, classSeq, classType):
    scores = putScore([num, pwd])
    return jsonify({'data': scores.hasCoef(term, classNum, classSeq, classType)})

# 教师保存成绩接口
@app.route('/teacher/score/save/<num>/<pwd>/<term>/<classNum>/<classSeq>/<classType>', methods=['POST'])
def saveScore(num, pwd, term, classNum, classSeq, classType):
    scores = putScore([num, pwd])
    score = []
    for x in request.get_json():
        tmp = []
        if x['num']:
            tmp.append(x['num'])
            if x['daily']:
                tmp.append(x['daily'])
            else:
                tmp.append('')
            if x['exam']:
                tmp.append(x['exam'])
            else:
                tmp.append('')
            if x['total']:
                tmp.append(x['total'])
            else:
                tmp.append('')
            if x['failRes']:
                tmp.append(x['failRes'])
            else:
                tmp.append('')
        score.append(tmp)
    return jsonify({'data': scores.saveScore(term, classNum, classSeq, classType, score)})

# 教师获取学生列表接口
@app.route('/teacher/students/list/<num>/<pwd>/<term>/<classNum>/<classSeq>/<classType>')
def getStudentsList(num, pwd, term, classNum, classSeq, classType):
    scores = putScore([num, pwd])
    return jsonify({'data': scores.getStudents(term, classNum, classSeq, classType)})

if __name__ == '__main__':
    app.run()