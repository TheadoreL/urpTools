#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urpTools.getScore import getScore
from urpTools.login import urpLogin
import xlrd
import xlwt
import sys
import os
import time
import pymongo
from pymongo import ReplaceOne

class gp(object):
    def __init__(self):
        os.chdir(sys.path[0])
        self.db = pymongo.MongoClient("mongodb://127.0.0.1:27017/gps").gps

    def savePwd(self):
        data = xlrd.open_workbook('../storage/cache/stu.xlsx')
        table = data.sheet_by_name('stu')
        nrows = table.nrows
        stus = []
        for i in range(nrows):
            tmp = {}
            tmp['num'] = table.row_values(i)[0]
            tmp['pwd'] = table.row_values(i)[1]
            tmp['name'] = table.row_values(i)[6]
            tmp['status'] = 0
            stus.append(ReplaceOne(tmp,tmp,upsert=True))
        result = self.db.users.bulk_write(stus)
        return result

    def queryUser(self):
        conn = self.db.users
        info = conn.find_one_and_update({'status': 10}, {'$set': {'status': 11}})
        if info:
            return [info['num'], info['pwd']], info['_id']
        else:
            return False, False

    def getScore(self):
        userConn = self.db.users
        conn = self.db.score
        user, id = self.queryUser()
        if not user:
            return False
        login = urpLogin(user)
        login.login()
        time.sleep(0.1)
        urpScore = getScore(user)
        score = urpScore.getAll()
        if score:
            scoreInsert = {}
            scoreList = []
            scoreInsert['num'] = user[0]
            scoreInsert['score'] = score
            scoreList.append(ReplaceOne(scoreInsert, scoreInsert, upsert=True))
            result = conn.bulk_write(scoreList)
            userConn.find_one_and_update({'_id': id}, {'$set': {'status': 1}})
            return user[0] + ' -- success'
        else:
            userConn.find_one_and_update({'_id': id}, {'$set': {'status': 0}})
            return user[0] + ' -- fail'

    def getClass(self):
        conn = self.db.score
        info = conn.find({})
        classes = {}
        for x in info:
            if x['num'][0:3] == '154':
                for y in x['score']:
                    classes[y['classNum']] = {}
                    classes[y['classNum']]['name'] = y['className']
                    classes[y['classNum']]['credit'] = y['classCredit']
                    classes[y['classNum']]['attr'] = y['classAttr']
        for x in classes:
            print(x+','+classes[x]['name']+','+classes[x]['credit']+','+classes[x]['attr'])

    def getGP(self):
        gpNums = ['p110', 'p115', 'J351', 'J115', 'J404', 'J389', 'J403', 'J435', 'J370', 'J219', 'J266', 'J264', 'J428', 'J367', 'J397', 'J398', 'J378', 'J446', 'J410', 'J072', 'J372', 'J405', 'J406', 'J069', 'J401', 'J402']
        conn = self.db.score
        info = conn.find({})
        gpScores = {}
        for x in info:
            if x['num'][0:3] == '154':
                gpScores[x['num']] = {}
                for y in x['score']:
                    if y['classNum'] == 'Y179':
                        gpScores.pop(x['num'])
                        break
                    if y['classNum'] in gpNums:
                        if y['classNum'] in gpScores[x['num']]:
                            gpScores[x['num']][y['classNum']]['examNum'] += 1
                            if gpScores[x['num']][y['classNum']]['score'] < float(y['score']):
                                gpScores[x['num']][y['classNum']]['score'] = float(y['score'])
                                gpScores[x['num']][y['classNum']]['name'] = y['className']
                                gpScores[x['num']][y['classNum']]['credit'] = float(y['classCredit'])
                        else:
                            gpScores[x['num']][y['classNum']] = {}
                            gpScores[x['num']][y['classNum']]['examNum'] = 1
                            gpScores[x['num']][y['classNum']]['score'] = float(y['score'])
                            gpScores[x['num']][y['classNum']]['name'] = y['className']
                            gpScores[x['num']][y['classNum']]['credit'] = float(y['classCredit'])
        finalScores = {}
        ok = 0
        good = 0
        c_ok = 0
        c_good = 0
        for x in gpScores:
            TCiPi = 0
            TCi = 0
            for y in gpScores[x]:
                if gpScores[x][y]['score'] == 60:
                    gpScores[x][y]['gp'] = 1.1
                elif gpScores[x][y]['score'] > 60:
                    gpScores[x][y]['gp'] = round(4 - 3 * ((100 - gpScores[x][y]['score']) * (100 - gpScores[x][y]['score']))/1600, 2)
                else:
                    gpScores[x][y]['gp'] = 0.0
                if gpScores[x][y]['examNum'] % 2 == 0 and gpScores[x][y]['score'] == 60:
                    gpScores[x][y]['gp'] = 1.0
                TCi+=gpScores[x][y]['credit']
                TCiPi+=(gpScores[x][y]['credit']*gpScores[x][y]['gp'])
            finalScores[x] = {}
            finalScores[x]['score'] = gpScores[x]
            finalScores[x]['gpa'] = round(TCiPi / TCi, 2)
            gpScores[x]['J000'] = {}
            gpScores[x]['J000']['name'] = '学业完成'
            gpScores[x]['J000']['score'] = 'A+'
            gpScores[x]['J000']['credit'] = 1.0
            gpScores[x]['J000']['examNum'] = 1
            gpScores[x]['J000']['gp'] = 4.0
            TCi += 1.0
            TCiPi += 4.0
            finalScores[x]['c_score'] = gpScores[x]
            finalScores[x]['c_gpa'] = round(TCiPi / TCi, 2)
            if finalScores[x]['gpa'] > 1.5:
                ok+=1
            if finalScores[x]['gpa'] > 1.8:
                good+=1
            if finalScores[x]['c_gpa'] > 1.5:
                c_ok+=1
            if finalScores[x]['c_gpa'] > 1.8:
                c_good+=1
        wb = xlwt.Workbook()
        ws = wb.add_sheet('绩点')
        ws.write(0, 0, 'GPA统计')
        ws.write(1, 0, 'GPA占比')
        ws.write(0, 1, '高于1.5')
        ws.write(1, 1, str(round(ok / len(finalScores), 4) * 100) + '%')
        ws.write(0, 2, '高于1.8')
        ws.write(1, 2, str(round(good / len(finalScores), 4) * 100) + '%')
        ws.write(0, 3, '高于1.5(课程完成)')
        ws.write(1, 3, str(round(c_ok / len(finalScores), 4) * 100) + '%')
        ws.write(0, 4, '高于1.8(课程完成)')
        ws.write(1, 4, str(round(c_good / len(finalScores), 4) * 100) + '%')
        ws.write(2, 0, '学号')
        ws.write(2, 1, 'GPA')
        ws.write(2, 2, 'GPA(课程完成)')
        col = 2
        for x in range(len(gpNums)):
            col += 1
            ws.write(2, col, '课程号')
            col += 1
            ws.write(2, col, '课程名')
            col += 1
            ws.write(2, col, '学分')
            col += 1
            ws.write(2, col, '考试次数')
            col += 1
            ws.write(2, col, '成绩')
            col += 1
            ws.write(2, col, 'GP')
        row = 3
        for x in finalScores:
            col = 0
            ws.write(row, col, x)
            col+=1
            ws.write(row, col, str(finalScores[x]['gpa']))
            col += 1
            ws.write(row, col, str(finalScores[x]['c_gpa']))
            for y in finalScores[x]['score']:
                col += 1
                ws.write(row, col, y)
                col += 1
                ws.write(row, col, finalScores[x]['score'][y]['name'])
                col += 1
                ws.write(row, col, str(finalScores[x]['score'][y]['credit']))
                col += 1
                ws.write(row, col, str(finalScores[x]['score'][y]['examNum']))
                col += 1
                ws.write(row, col, str(finalScores[x]['score'][y]['score']))
                col += 1
                ws.write(row, col, str(finalScores[x]['score'][y]['gp']))
            row+=1
        wb.save('../storage/cache/绩点.xls')
        print("完成")



gpTool = gp()
# gpTool.getScore()
gpTool.getGP()