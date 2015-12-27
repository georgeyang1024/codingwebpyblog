#-*-coding:utf-8-*-
import json


__author__ = 'george.yang'



def successWithDate(outData):
    out = {}
    out['errorCode']=0
    out['data']=outData
    out['message']='success'
    return json.dumps(out)

def success():
    out = {}
    out['errorCode']=1
    out['message']='success'
    return json.dumps(out)

def fail (errCode,message):
    out = {}
    out['errorCode']=errCode
    out['message']=message
    return json.dumps(out)

def html(context):
    head = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title></title></head><body> %s </body></html>'
    return head%context;
