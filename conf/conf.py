#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def urls():
    return {
              "main": "http://newjw.cduestc.cn",
              "login": "/loginAction.do",
              "thisTremScore": "/bxqcjcxAction.do?pageSize=300",
              "allScore": "/gradeLnAllAction.do?type=ln&oper=fainfo",
              "self": "/xjInfoAction.do?oper=xjxx",
              "user": "/userInfo.jsp",
              "photo": "/xjInfoAction.do?oper=img",
              "scoreCoefList": "/jsKcxzAction.do",
              "scoreCoefTerm": "/rwCjxsAction.do?oper=jskcInfo",
              "scoreCoefSave": "/rwCjxsAction.do?oper=saveCjxs",
              "scoreClassList": "/jsKcxzAction.do?oper=cjlrkc",
              "scoreSave": "/cjlrmxAction.do?oper=SaveOrUpdate&oper1=lrfdjcj",
              "scoreSave_": "/cjlrAction.do",
              "getStudents": "/cjlrmxAction.do?oper=cjlrAllType"
            }