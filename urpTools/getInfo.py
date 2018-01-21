#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urpTools.login import urpLogin
import conf.conf as conf
import re
import os
import sys

class getInfo(object):

    def __init__(self, user):
        os.chdir(sys.path[0])
        self.__num = user[0]
        self.__photoPath = '../storage/photos/'
        self.urp = urpLogin(user)
        # 读取url配置文件
        self.urls = conf.urls()

    def info(self):
        page = self.urp.open(self.urls['self'])
        data = {}
        htmlStr = page.text
        pattern = re.compile(
            u"\<td class\=\"fieldName\" width\=\"180\"\>\s*姓名\:&nbsp\;\s*\<\/td\>\s*\<td width\=\"275\"\>\s*(.*?)\s*\<\/td\>",
            re.S)
        data['name'] = pattern.findall(htmlStr)[0]
        pattern = re.compile(
            u"\<td class\=\"fieldName\" width\=\"180\"\>\s*身份证号\:&nbsp\;\s*\<\/td\>\s*\<td align\=\"left\" width\=\"275\"\>\s*(.*?)\s*\<\/td\>",
            re.S)
        data['idnum'] = pattern.findall(htmlStr)[0]
        pattern = re.compile(
            u"\<td class\=\"fieldName\" width\=\"180\"\>\s*学生类别\:&nbsp\;\s*\<\/td\>\s*\<td align\=\"left\" width\=\"275\"\>\s*(.*?)\s*\<\/td\>",
            re.S)
        data['classify'] = pattern.findall(htmlStr)[0]
        pattern = re.compile(
            u"\<td class\=\"fieldName\" width\=\"180\"\>\s*年级\:&nbsp\;\s*\<\/td\>\s*\<td align\=\"left\" width\=\"275\"\>\s*(.*?)\s*\<\/td\>",
            re.S)
        data['grade'] = pattern.findall(htmlStr)[0]
        pattern = re.compile(
            u"\<td class\=\"fieldName\" width\=\"180\"\>\s*性别\:&nbsp\;\s*\<\/td\>\s*\<td align\=\"left\" width\=\"275\"\>\s*(.*?)\s*\<\/td\>",
            re.S)
        data['sex'] = pattern.findall(htmlStr)[0]
        pic = self.urp.open(self.urls['photo'])
        with open(self.__photoPath+self.__num+'.jpg', 'wb') as f:
            f.write(pic.content)
        data['photo'] = self.__num+'.jpg'
        return data