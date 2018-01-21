#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urpTools.login import urpLogin
from bs4 import BeautifulSoup
import json
import os
import sys

class getScore(object):

    def __init__(self, user):
        os.chdir(sys.path[0])
        self.__num = user[0]
        self.urp = urpLogin(user)
        # 读取url配置文件
        path = os.path.abspath('..')
        with open(path + '/conf/url.json', 'r') as f:
            self.urls = json.load(f)

    def getThisTerm(self):
        return self.__getScore(self.urls['thisTremScore'])

    def getAll(self):
        return self.__getScore(self.urls['allScore'])

    def __getScore(self, url):
        page = self.urp.open(url)
        soup = BeautifulSoup(page.text, 'lxml')
        data = []
        for x in soup.find_all('tr'):
            i = 0
            tmp = {}
            notClass = False
            for y in x.find_all('td', attrs = {'align': 'center'}):
                if i == 0:
                    if y.string:
                        if y.string.replace(" ", "").replace("\t", "").strip() == '':
                            notClass = True
                        else:
                            notClass = False
                            tmp['classNum'] = y.string.replace(" ", "").replace("\t", "").strip()
                    else:
                        continue
                if notClass:
                    continue
                else:
                    if i == 2:
                        if y.string:
                            tmp['className'] = y.string.replace(" ", "").replace("\t", "").strip()
                        else:
                            tmp['className'] = ''
                    elif i == 4:
                        if y.string:
                            tmp['classCredit'] = y.string.replace(" ", "").replace("\t", "").strip()
                        else:
                            tmp['classCredit'] = ''
                    elif i == 5:
                        if y.string:
                            tmp['classAttr'] = y.string.replace(" ", "").replace("\t", "").strip()
                        else:
                            tmp['classAttr'] = ''
                    elif i == 6:
                        if y.p.string:
                            tmp['score'] = y.p.string.replace(" ", "").replace("\t", "").strip()
                        else:
                            tmp['score'] = ''
                        if y.find_next_sibling('td').p.string:
                            tmp['failRes'] = y.find_next_sibling('td').p.string.replace(" ", "").replace("\t", "").strip()
                        else:
                            tmp['failRes'] = ''
                i += 1
            if not tmp == {}:
                data.append(tmp)
        return data