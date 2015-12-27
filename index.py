#-*-coding:utf-8-*-

import web
import os

urls = (
    '([a-z0-9\/]*)', 'dealRequest',
    '(.*\..{1,4})','StaticFile'
)
# app = web.application(urls, globals())


#非调试模式
web.config.debug = True
app_root = os.path.dirname(__file__)
web.internalerror = web.debugerror
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)


class StaticFile:
    def GET(self, file):
        print file
        web.seeother('/static/'+file)
        # print file
        # homedir = os.getcwd()
        # filePath = '%s/static/%s' %(homedir,file)
        # print filePath
        # if os.path.exists(filePath):
        #     web.seeother('/static/'+file)
        # else:
        #     if '//' in file:
        #         return web.notfound()
        #     else:
        #         filePath = '%s/%s'%(ut.getUploadPath(),file)
        #         web.seeother(filePath); #重定向a

class dealRequest:
    def __init__(self):
        pass
    def GET(self, path):
        return self.__request(path)

    def POST(self, path):
        return self.__request(path)

    def __request(self, path=''):
        modelName = path.strip()[1:]
        controllerName = ''
        try:
            modelName, controllerName = path.strip()[1:].split('/', 1)
        except Exception,e:
            print e

        if not modelName:
            modelName = 'index'
        if not controllerName:
            controllerName = 'index'

        print 'modelName:' + modelName
        print 'controllerName:' + controllerName

        try:
            try:
                moduleList = __import__('action.' + modelName, {}, {}, [modelName])
            except Exception,e:
                return web.notfound()
            modelObj = getattr(moduleList, modelName)()
            if hasattr(modelObj, controllerName):
                result = getattr(modelObj, controllerName)()
                return result
            else:
                return web.notfound()
        except Exception,e:
            return 'error:' + e.message


if __name__ == "__main__":
    # app = web.application(urls, globals(), autoreload=False)
    # # app = web.application(urls, globals())
    # # web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    # app.run()
    app = web.application(urls, globals())
    application = app.wsgifunc()
    app.run()