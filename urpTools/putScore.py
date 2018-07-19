#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urpTools.login import urpLogin
from bs4 import BeautifulSoup
import re
import conf.conf as conf
import os
import sys

class putScore(object):

    def __init__(self, user):
        os.chdir(sys.path[0])
        self.__num = user[0]
        self.urp = urpLogin(user)
        # 读取url配置文件
        path = os.path.abspath('..')
        self.urls = conf.urls()

    # 获取学期数据
    def getTerms(self):
        page = self.urp.open(self.urls['scoreCoefTerm'])
        soup = BeautifulSoup(page.text, 'lxml')
        options = soup.find_all('option')
        data = []
        for x in options:
            tmp = {}
            tmp['value'] = x['value']
            tmp['cn'] = x.string
            data.append(tmp)
        return data

    # 获取成绩系数列表
    def getCoefList(self, term):
        data = {
            'zxjxjhh': term,
            'kcm': '',
            'kch': ''
        }
        page = self.urp.post(self.urls['scoreCoefList'], data)
        soup = BeautifulSoup(page.text, 'lxml')
        data = []
        for x in soup.tbody.find_all('tr'):
            i = 0
            tmp = {}
            for y in x.find_all('td'):
                if i == 0:
                    tmp['department'] = y.string.replace(" ", "").replace("\t", "").strip()
                if i == 1:
                    tmp['className'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 2:
                    tmp['classNum'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 3:
                    tmp['classSeq'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 5:
                    tmp['classYear'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 6:
                    tmp['classTerm'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 8:
                    pattern = re.compile(u"clickButton\(\'(.*?)\',\'(.*?)\',\'(.*?)\',\'(.*?)\'\)\;return false\;", re.S)
                    attrs = pattern.findall(y.img['onclick'])[0]
                    tmp['classTermEn'] = attrs[0]
                    tmp['classType'] = attrs[3]
                i += 1
            data.append(tmp)
        return data

    # 保存成绩系数
    def saveCoef(self, term, classNum, classSeq, dailyScore, examScore, expScore=0.0, examMid=0.0):
        if float(expScore) > 0:
            classScore = 1.0 - float(expScore)
            expScoreCoef = 1.0
        else:
            classScore = 1.0
            expScoreCoef = 0.0
        data = {
            'zxjxjhh': term,
            'kch': classNum,
            'kxh': classSeq,
            'isCheckControlValue': 1,
            'ktcj': classScore,
            'sjcj': expScore,
            'sycj': 0.0,
            'ktcjps': dailyScore,
            'ktcjqz': examMid,
            'ktcjqm': examScore,
            'sjcjps': 0.0,
            'sjcjqz': 0.0,
            'sjcjqm': expScoreCoef,
            'sycjps': 0.0,
            'sycjqz': 0.0,
            'sycjqm': 0.0,
        }
        page = self.urp.post(self.urls['scoreCoefSave'], data)
        pattern = re.compile(u"xx \= \"(.*?)\"", re.S)
        status = pattern.findall(page.text)[0]
        if status == "系数保存成功":
            return True
        return False

    def getCoef(self, term, classNum, classSeq):
        data = {
            'zxjxjhh': term,
            'kch': classNum,
            'kxh': classSeq
        }
        page = self.urp.post(self.urls['scoreCoefSave'], data)
        soup = BeautifulSoup(page.text, 'lxml')
        try:
            return {
                'daily': soup.find('input', attrs= {'name': 'ktcjps'})['value'],
                'exam': soup.find('input', attrs= {'name': 'ktcjqm'})['value'],
                'examMid': soup.find('input', attrs={'name': 'ktcjqz'})['value'],
                'examExp': soup.find('input', attrs={'name': 'sjcj'})['value']
            }
        except:
            return {}

    # 获取课程列表
    def getClassList(self, term):
        data = {
            'zxjxjhh': term,
            'kcm': '',
            'kch': ''
        }
        page = self.urp.post(self.urls['scoreClassList'], data)
        soup = BeautifulSoup(page.text, 'lxml')
        data = []
        for x in soup.tbody.find_all('tr'):
            i = 0
            tmp = {}
            for y in x.find_all('td'):
                if i == 0:
                    tmp['className'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 1:
                    tmp['classNum'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 2:
                    tmp['classSeq'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 4:
                    tmp['classYear'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 5:
                    tmp['classTerm'] = y.string.replace(" ", "").replace("\t", "").strip()
                elif i == 7:
                    pattern = re.compile(u"clickButton\(\'(.*?)\',\'(.*?)\',\'(.*?)\',\'(.*?)\'\)\;return false\;",
                                         re.S)
                    attrs = pattern.findall(y.img['onclick'])[0]
                    tmp['classTermEn'] = attrs[0]
                    tmp['classType'] = attrs[3]
                i += 1
            data.append(tmp)
        return data

    # 判断成绩系数是否录入
    def hasCoef(self, term, classNum, classSeq, classType):
        openData = {
            'zxjxjhh': term,
            'kch': classNum,
            'kxh': classSeq
        }
        self.urp.post(self.urls['scoreSave_'] + '?oper=cjlrAllType&zxjxjhh=' + term + '&kch=' + classNum + '&kxh=' + classSeq + '&cjlrfs=' + classType, openData)
        page = self.urp.open(self.urls['getStudents'])
        soup = BeautifulSoup(page.text, 'lxml')
        if soup.find(text='您的成绩录入系数尚未维护，请先进行成绩系数维护，再录入学生成绩！'):
            return False
        return True

    # 获取学生数据
    def getStudents(self, term, classNum, classSeq, classType):
        coef = self.getCoef(term, classNum, classSeq)
        openData = {
            'zxjxjhh': term,
            'kch': classNum,
            'kxh': classSeq
        }
        self.urp.post(self.urls['scoreSave_'] + '?oper=cjlrAllType&zxjxjhh=' + term + '&kch=' + classNum + '&kxh=' + classSeq + '&cjlrfs=' + classType, openData)
        page = self.urp.open(self.urls['getStudents'])
        soup = BeautifulSoup(page.text, 'lxml')
        data = []
        try:
            table = soup.find_all('table', class_= 'displayTag', id='user')[1]
            for x in table.find_all('tr', class_= 'odd'):
                tmp = {}
                tds = x.find_all('td')
                tmp['number'] = tds[1].string.replace(" ", "").replace("\t", "").strip()
                tmp['name'] = tds[2].string.replace(" ", "").replace("\t", "").strip()
                tmp['class'] = tds[3].string.replace(" ", "").replace("\t", "").strip()
                if float(coef['examExp']) > 0:
                    tmp['examExp'] = x.find('input', attrs={'name': re.compile('\d_sj_qm')})['value']
                if float(coef['daily']) > 0:
                    tmp['daily'] = x.find('input', attrs = {'name': re.compile('\d_kt_ps')})['value']
                if float(coef['examMid']) > 0:
                    tmp['examMid'] = x.find('input', attrs = {'name': re.compile('\d_kt_qz')})['value']
                if float(coef['exam']) > 0:
                    tmp['exam'] = x.find('input', attrs = {'name': re.compile('\d_kt_qm')})['value']
                tmp['total'] = x.find('input', attrs = {'name': re.compile('\d_zcj')})['value']
                selectDom = x.find('select', attrs = {'name': re.compile('\d_wtgyydm')})
                try:
                    option = selectDom.find('option', attrs={'selected': 'selected'})
                    tmp['failRes'] = option['value']
                except:
                    tmp['failRes'] = ''
                data.append(tmp)
        except:
            pass
        return data

    # 保存成绩
    def saveScore(self, term, classNum, classSeq, classType, score):
        coef = self.getCoef(term, classNum, classSeq)
        openData = {
            'zxjxjhh': term,
            'kch': classNum,
            'kxh': classSeq
        }
        self.urp.post(self.urls['scoreSave_']+'?oper=cjlrAllType&zxjxjhh='+term+'&kch='+classNum+'&kxh='+classSeq+'&cjlrfs='+classType, openData)
        data = {
            'zcjlrfs': '001',
            'pageSize': 300,
            'cjlrfs': 'null'
        }
        for x in score:
            if float(coef['daily']) > 0:
                data[x['number'] + '_kt_ps'] = x['daily']
            if float(coef['examMid']) > 0:
                data[x['number'] + '_kt_qz'] = x['examMid']
            if float(coef['examExp']) > 0:
                data[x['number'] + '_sj_qm'] = x['examExp']
            if float(coef['exam']) > 0:
                data[x['number'] + '_kt_qm'] = x['exam']
            data[x['number'] + '_zcj'] = x['total']
            data[x['number'] + '_wtgyydm'] = x['failRes']
        self.urp.open(self.urls['getStudents'])
        page = self.urp.post(self.urls['scoreSave'], data)
        pattern = re.compile(u"\<script language\=\"javascript\"\>alert\(\"(.*?)\"\)\;\<\/script\>", re.S)
        try:
            status = pattern.findall(page.text)[0]
            if status == "成绩信息保存成功！":
                return True
            return False
        except:
            return False