#-*-coding:utf-8-*-
__author__ = 'george.yang'

import pymongo
import utils.webpyutil as ut
import markdown
from lrucache import lrucache
from utils import mdextension

def getMonthlist(table):
    key = ['month']
    cond = None
    initial = {'count' : 0}
    reduce = "function (obj, prev) { prev.count++; }"
    return list(table.group(key,cond,initial,reduce))

def getNewlist(table):
    return list(table.find().sort("addTime",pymongo.DESCENDING).limit(10))

def getClassificationMap(table):
    classificationList = list(table.find({'classification':{'$exists':True}}))
    print 'classification list:'
    print classificationList
    classificationMap = {}
    if classificationList:
        for classBlog in classificationList:
            print 'blog:####'
            print classBlog
            if classBlog['classification']:
                for classKey in classBlog['classification'].split(','):
                    if not classificationMap.has_key(classKey):
                        classificationMap[classKey] = 1
                    else:
                        classificationMap[classKey] += 1
    return classificationMap

def getBlogList(table,page,findWhere):
    cacheKey = 'key_%s-%d-%s'%(str(table),page,str(findWhere))
    print cacheKey
    ret = lrucache.getinstance().get(cacheKey)
    if ret:
        print 'use cache:' + cacheKey
        return ret

    if page<=0:
        page=1

    contentList = list(table.find(findWhere).sort("addTime",pymongo.DESCENDING).limit(10).skip(10*(page-1)))
    filedir = ut.getUploadPath()
    for blogItem in contentList:
        if not blogItem.has_key('addTime'):
            blogItem['addTime']='9999-99-99 99:99:99'

        try:
            fileContent = ut.readFileContent(filedir + '/' + blogItem['filename']).decode('utf-8')
            if len(fileContent) > 250:
                introduction = fileContent[0:250]+ " ..."
            else:
                introduction = fileContent
            introduction = markdown.markdown(introduction)
            blogItem['introduction'] = introduction
        except Exception, e:
            introduction = markdown.markdown('Wrong file:' + blogItem['filename'] + " info:" + str(e))
            blogItem['introduction'] = introduction
            print e

    #两分钟的缓存
    lrucache.getinstance().set(cacheKey,contentList,120)


    return contentList

def getBlogInfo(table,id):
    blogInfo = table.find_one({'id':id})
    filedir = ut.getUploadPath()
    fileContent = ut.readFileContentNoCache(filedir + '/' + blogInfo['filename']).decode('utf-8')
    # blogInfo['content']=markdown.markdown(fileContent)

    configs = {}
    myext = mdextension.CodeExtension(configs=configs)
    md = markdown.markdown(fileContent, extensions=[myext])
    blogInfo['content'] = md

    if not blogInfo.has_key('addTime'):
        blogInfo['addTime']='9999-99-99 99:99:99'
    return blogInfo
