#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
import sys
import time
from bs4 import BeautifulSoup

class urpLogin(object):

    __agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

    def __init__(self, user):
        os.chdir(sys.path[0])
        self.loginInfo = {
            'zjh': user[0],
            'mm': user[1]
        }
        self.cookieFile = '../storage/cookies/'+user[0]+'.json'
        # 读取url配置文件
        path = os.path.abspath('..')
        with open(path + '/conf/url.json', 'r') as f:
            self.urls = json.load(f)
        self.__session = requests.session()
        self.__cookie = self.__loadCookie()
        if self.__cookie:
            JSESSIONID = 'JSESSIONID='+self.__cookie['JSESSIONID']
        else:
            JSESSIONID = ''
        self.headers = {
            'User-Agent': self.__agent,
            'Cookie': JSESSIONID
        }
        self.__session.headers = self.headers
        if self.__cookie:
            self.__session.cookies.update(self.__cookie)
            if not self.isLogin():
                self.login()
        else:
            self.login()

    def isLogin(self):
        # 打开主页，根据title判断登陆状态
        page = self.open(self.urls['user'])
        soup = BeautifulSoup(page.text, 'lxml')
        if soup.title.string == '修改密码':
            return True
        return False

    def login(self):
        res = self.__session.post(self.urls['main']+self.urls['login'], data=self.loginInfo)
        soup = BeautifulSoup(res.text, 'lxml')
        if soup.title.string == '学分制综合教务':
            self.__saveCookie()
            return True
        return False

    def open(self, url, delay=0, timeout=100):
        if delay:
            time.sleep(delay)
        return self.__session.get(self.urls['main']+url, timeout=timeout)

    def post(self, url, data, delay=0, timeout=100):
        if delay:
            time.sleep(delay)
        return self.__session.post(self.urls['main']+url, data=data, timeout=timeout)

    def __saveCookie(self):
        with open(self.cookieFile, "w") as output:
            cookies = self.__session.cookies.get_dict()
            json.dump(cookies, output)

    def __loadCookie(self):
        # 读取cookie文件，返回反序列化后的dict对象，没有则返回None
        if os.path.exists(self.cookieFile):
            with open(self.cookieFile, "r") as f:
                cookie = json.load(f)
                return cookie
        return None

    def getSession(self):
        return self.__session