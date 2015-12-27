#-*-coding:utf-8-*-
import re

import web
import os
import json
from pymongo import MongoClient
from lrucache import lrucache


__author__ = 'george.yang'


def getInput(input):
    return htmlquote(dict(input))

def htmlquote(inputData):
    if isinstance(inputData,dict) == False:
        return web.net.htmlquote(inputData)
    else:
       for k,v in inputData.items():
            inputData[k] = htmlquote(v)
    return inputData

def getTemplates():
    render=web.template.render('templates')
    return render

def getTemplatesWithBase():
    render = web.template.render('templates', base='base', globals=globals())
    return render

def dbList2Json(list):
    ret = []
    for k,v in enumerate(list):
        obj = {}
        for k1,v1 in enumerate(v):
            value = v[v1]
            if isinstance(value,(int,long)):
                obj[v1]=int(value)
            else:
                # print value
                obj[v1] = str(value)
        ret.append(obj)
    # ret.append({'key':'中文测试'})
    return ret


def getUploadPath():
    out = {}
    envs=os.environ
    if envs.has_key('VCAP_SERVICES'):
        decode = json.loads(envs['VCAP_SERVICES'])
        out['ret'] = decode['filesystem-1.0'][0]['credentials']['host_path']
    if not out.has_key('ret'):
        homedir = os.getcwd()
        filedir = '%s/static/upload/' %homedir
        out['ret'] = filedir
    if out.has_key('ret'):
        return out['ret']
    return ''


def getMongoInfo():
    out = {}
    envs=os.environ
    if envs.has_key('VCAP_SERVICES'):
        decode = json.loads(envs['VCAP_SERVICES'])
        out['host'] = decode['mongodb'][0]['credentials']['host']
        out['port'] = decode['mongodb'][0]['credentials']['port']
        out['username'] = decode['mongodb'][0]['credentials']['username']
        out['password'] = decode['mongodb'][0]['credentials']['password']
        out['uri'] = decode['mongodb'][0]['credentials']['uri']
        out['name'] = decode['mongodb'][0]['credentials']['name']
    if not out.has_key('host'):
        out['host'] = 'localhost'
        out['port'] = 27017
        out['username'] = 'root'
        out['password'] = 'root'
        out['name'] = 'Blog'
    print 'out=%s'%out
    return out

def getMongo():
    info = getMongoInfo()
    print info
    if info.has_key('uri'):
        print 'login by uri:%s'%info['uri']
        client = MongoClient(info['uri'])
    else:
        print 'login by username:%s'%info['username']
        client = MongoClient(info['host'],info['port'])
    db =  client[info['name']]
    table = db.bloglist6
    return table

def getBlogInfo():
    info = getMongoInfo()
    print info
    if info.has_key('uri'):
        print 'login by uri:%s'%info['uri']
        client = MongoClient(info['uri'])
    else:
        print 'login by username:%s'%info['username']
        client = MongoClient(info['host'],info['port'])
    db =  client[info['name']]
    table = db.bloginfo
    return table


def readFileContent(file):
    cacheKey = 'fileContent-%s'%(file)
    print cacheKey
    ret = lrucache.getinstance().get(cacheKey)
    if ret:
        print 'use cache:' + cacheKey
        return ret

    print 'read MD File:%s'%file
    file_object = open(file)
    try:
        content = file_object.read()
        lrucache.getinstance().set(cacheKey,content,3600)
        return content
    finally:
        file_object.close()
    return ''

def readFileContentNoCache(file):
    print 'read MD File:%s'%file
    file_object = open(file)
    try:
        content = file_object.read()
        return content
    finally:
        file_object.close()
    return ''

def readMdFileInfo(dir,filename):
    print 'readMdFileInfo!!'
    content = readFileContent(dir+"/"+filename)
    blogTag = None
    blogClassifiCation = None

    pattern = re.compile(r'<!--(.|\s)*?-->')

    match = pattern.match(content)
    if match:
        # print 'match2:' + match
        blogInfo = match.group()
        if not blogInfo:
            return 'content noRight'
        try:
            #注释里面的内容
            blogTag = re.findall(r'tag:(.*)',blogInfo)[0]
        except Exception, e:
            print e
        try:
            blogClassifiCation = re.findall(r'classification:(.*)',blogInfo)[0]
        except Exception, e:
            print e

    ret = {}
    if blogTag:
        ret['tag']=blogTag
        try:
            for tag in blogTag.split(','):
                ret['tag_%s'%tag]=1
        except Exception:
            pass
    else:
        ret['tag']='<no tag>'

    if blogClassifiCation:
        ret['classification']=blogClassifiCation
        try:
            for classfi in blogClassifiCation.split(','):
                ret['classification_%s'%classfi]=1
        except Exception:
            pass
    else:
        ret['classification']='<no blogClassifiCation>'

    print 'return blogInfo:' + str(ret)
    return ret


