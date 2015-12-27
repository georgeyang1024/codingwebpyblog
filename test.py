#-*-coding:utf-8-*-
__author__ = 'george.yang'


import markdown
from utils import mdextension


text = '''
```
!!!python
!
!def foo():

title
```
eeee
'''

configs = {}

myext = mdextension.CodeExtension(configs=configs)
md = markdown.markdown(text, extensions=[myext])
print md