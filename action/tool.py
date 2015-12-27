#-*-coding:utf-8-*-
import json
import time
import web

__author__ = 'george.yang'


class tool:
    def getip(self):
        print 'getip'
        data={}
        data["ip"]=web.ctx['ip']
        data["id"]=1
        data["time"]= long(time.time())

        outJson={}
        outJson["errorCode"] = 0
        outJson["data"]=data
        outJson["message"]="success"
        jsonStr = json.dumps(outJson)
        return jsonStr