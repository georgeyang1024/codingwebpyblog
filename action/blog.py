# -*-coding:utf-8-*-
__author__ = 'george.yang'

import utils.webpyutil as ut
import utils.blogutil as butil
import web
import md5
import time
import string

class blog:
    def index(self):
        web.seeother('/blog/list')

    def post(self):
        params = ut.getInput(web.input())
        if not params.has_key('key'):
            return "not key param"
        key = params['key']
        print key
        todayKey = time.strftime("%m-%d", time.localtime()) + "#blog"
        print todayKey
        m5 = md5.new()
        m5.update(todayKey)
        keyCheck = m5.hexdigest()
        print 'checkKey:' + keyCheck
        if (key == keyCheck):
            return ut.getTemplates().upload(key);
        else:
            return 'check fail'

    def delete(self):
        params = ut.getInput(web.input())
        if not params.has_key('key'):
            return "not key param"
        if not params.has_key('id'):
            return "not id param"
        key = params['key']
        id = params['id']
        print key
        todayKey = time.strftime("%m-%d", time.localtime()) + "#blog"
        print todayKey
        m5 = md5.new()
        m5.update(todayKey)
        keyCheck = m5.hexdigest()
        print 'checkKey:' + keyCheck
        if (key == keyCheck):
            where = {'id':id}
            table = ut.getMongo()
            table.remove(where)
            return 'success'
        else:
            return 'check fail'

    #error:cannot concatenate 'str' and 'OperationFailure' objects
    def upload(self):
        params = web.input(file={})
        # print params
        # print params['file'].filename # 这里是文件名
        # print params['file'].file
        # print params['file'].value # 这里是文件内容
        # print params['file'].file.read() # 或者使用一个文件对象
        if not params.has_key('key'):
            return "not key param"

        key = params['key']
        todayKey = time.strftime("%m-%d", time.localtime()) + "#blog"
        print todayKey
        m5 = md5.new()
        m5.update(todayKey)
        keyCheck = m5.hexdigest()
        print keyCheck
        if key == keyCheck:
            print 'check success'
            filedir = ut.getUploadPath()
            filename = params['file'].filename
            blogTitle = filename.replace('.md','')

            print filedir
            print filename
            if not filename.endswith('.md'):
                return 'file name must be endwith .md'

            m5 = md5.new()
            m5.update(filename)
            filename = m5.hexdigest() + ".md"
            try:
                with open(filedir + '/' + filename, 'wb') as f_out:
                    f_out.write(params['file'].file.read())
                f_out.close()

                table = ut.getMongo()
                ret = None
                try:
                    ret = table.find_one({'filename':filename}) # find a record by query
                    print ret
                except Exception, e:
                    print e

                print ret

                blogInfo = ut.readMdFileInfo(filedir,filename)
                blogInfo['title']=blogTitle
                blogInfo['filename']=filename
                blogInfo['changTime'] = time.time()

                if not ret:
                    blogInfo['month'] = time.strftime("%y-%m", time.localtime())
                    blogInfo['addTime'] = time.strftime("%y-%m-%d %H:%M:%S",time.localtime())
                    blogInfo['changeCount'] = 0
                    blogInfo['readCount'] = 0
                    blogInfo['likeCount'] = 0
                    blogInfo['id']=str(time.strftime("%y%m%d%H%M%S",time.localtime())).decode('utf-8')[::-1]

                    table.insert(blogInfo)
                else:
                    blogInfo['id'] = ret['id']
                    blogInfo['addTime'] = ret['addTime']
                    if ret.has_key('month'):
                        blogInfo['month']=ret['month']
                    else:
                        blogInfo['month']=time.strftime("%y-%m", time.localtime())
                    if ret.has_key('changeCount'):
                        blogInfo['changeCount']=ret['changeCount']+1
                    else:
                        blogInfo['changeCount']=1
                    if ret.has_key('readCount'):
                        blogInfo['readCount'] = ret['readCount']
                    else:
                        blogInfo['readCount'] = 0
                    if ret.has_key('likeCount'):
                        blogInfo['likeCount'] = ret['likeCount']
                    else:
                        blogInfo['likeCount']=0
                    where = {'filename':filename}
                    table.update(where,blogInfo)

                return 'success!'
            except Exception, e:
                print e
                return 'faild:' + e
        else:
            return 'check fail'

    def list(self):
        params = ut.getInput(web.input())
        page = 1
        classification = None
        month = None
        findWhere = {}

        if params.has_key('page'):
            page = string.atoi(params['page'])
        if params.has_key('month'):
            month = params['month']
            findWhere['month']=month
        if params.has_key('classification'):
            classification = params['classification']
            findWhere['classification_%s'%classification]=1
        table = ut.getMongo()

        contentList = butil.getBlogList(table,page,findWhere)

        blogCount = table.count(findWhere)

        newLast = butil.getNewlist(table)

        monthList = butil.getMonthlist(table)

        classificationMap = butil.getClassificationMap(table)
        print classificationMap


        pageCount = 1 if blogCount<=10 else (blogCount/10 if blogCount%10==0 else blogCount/10+1)
        hasNext = page!=pageCount
        hasPrev = page!=1

        pageData = {}
        pageData['blogCount']=blogCount
        pageData['page']=page
        pageData['hasNext']=hasNext
        pageData['hasPrev']=hasPrev
        pageData['pageCount']=pageCount
        pageData['currPage']=page
        pageData['classification']=classification
        pageData['month']=month
        print 'list success'
        return ut.getTemplatesWithBase().showlist(contentList,newLast,monthList,classificationMap,pageData)

    def read(self):
        params = ut.getInput(web.input())
        if params.has_key('id'):
            try:
                id = params['id']
                table = ut.getMongo()

                blogInfo = butil.getBlogInfo(table,id)

                newLast = butil.getNewlist(table)

                monthList = butil.getMonthlist(table)

                classificationMap = butil.getClassificationMap(table)

                return ut.getTemplatesWithBase().showcontent(blogInfo,newLast,monthList,classificationMap)
            except Exception, e:
                return ut.getTemplatesWithBase().error(e)
        return 'id not found'

    def about(self):
            table = ut.getMongo()
            m5 = md5.new()
            m5.update('about.md')
            saveFile = m5.hexdigest() + ".md"
            lineInfo = table.find_one({'filename':saveFile})
            if lineInfo:
                if lineInfo.has_key('id'):
                    web.seeother('/blog/read?id='+lineInfo['id'])
                    return
            return ut.getTemplatesWithBase().error('no file!')





