#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import http.cookiejar as cookielib

class urpLogin(object):

    __agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"

    def __init__(self, user):
        self.loginInfo = {
            'zjh':user[0],
            'mm':user[1]
        }
        self.headers = {
            'User-Agent': self.__agent
        }