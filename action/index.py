#-*-coding:utf-8-*-
__author__ = 'george.yang'

import web

class index:
    def index(self):
        web.seeother('/blog/list')