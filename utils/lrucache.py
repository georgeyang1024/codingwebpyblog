#-*-coding:utf-8-*-
import time

__author__ = 'george.yang'
__all__ = ['lrucache']

#encoding=utf-8
class lrucache(object):
    __instance = None

    @classmethod
    def getinstance(cls):
        if(cls.__instance == None):
            cls.__instance = lrucache(999)
        return cls.__instance

    def __init__(self, maxsize):
        # cache 的最大记录数
        self.maxsize = maxsize
        # 用于真实的存储数据
        self.inner_dd = {}
        # 链表-头指针
        self.head = None
        # 链表-尾指针
        self.tail = None
    def set(self, key, value,timeToLive):
        # 达到指定大小
        if len(self.inner_dd) >= self.maxsize:
            self.remove_head_node()
        node = Node()
        node.data = (key, value)
        node.time = time.time() + timeToLive

        self.insert_to_tail(node)
        self.inner_dd[key] = node

    #插入到-尾位置，最后移除的
    def insert_to_tail(self, node):
        if self.tail is None:
            self.tail = node
            self.head = node
        else:
            if self.tail:
                self.tail.next = node
            if node.pre:
                node.pre = self.tail
            self.tail = node

    #移除一个node，在头部，最先移除
    def remove_head_node(self):
        node = self.head
        if node:
            del self.inner_dd[node.data[0]]
        node = None
        self.head = self.head.next
        if self.head:
            self.head.pre = None

    def remove_node(self,node):
        if (node==self.head):
            self.remove_head_node()
        else:
            if node:
                node.pre = node.next.pre


    def get(self, key):
        if key in self.inner_dd:
            # 如果命中, 需要将对应的节点移动到队列的尾部
            node = self.inner_dd.get(key)
            # 如果超时，删除并返回None
            # print '88888888'
            # print("time:%s"%time.time())
            # print("node:%s"%node.time)
            if not node:
                return None
            if (time.time()>node.time):
                del self.inner_dd[key]
                if node.pre:
                    node.pre.next = node.next
                if node.next:
                    node.next.pre = node.pre
                return None
            else:
                self.move_to_tail(node)
                if node:
                    return node.data[1]
        return None

    # 移到首位置
    def move_to_tail(self, node):
        # 只需处理在队列头部和中间的情况
        if not (node == self.tail):
            if node == self.head:
                if self.head:
                    self.head = node.next
                    if self.head:
                        self.head.pre = None
                if self.tail:
                    self.tail.next = node
                if node:
                    node.pre = self.tail
                if node:
                    node.next = None
                self.tail = node
            else:
                pre_node = node.pre
                next_node = node.next
                if pre_node:
                    pre_node.next = next_node
                if next_node:
                    next_node.pre = pre_node
                if self.tail:
                    self.tail.next = node
                if node:
                    node.pre = self.tail
                if node:
                    node.next = None
                self.tail = node

class Node(object):
    def __init__(self):
        self.pre = None
        self.next = None
        # (key, value)
        self.data = None
        # add time
        self.time = time.time()
    def __eq__(self, other):
        if other:
            if self.data[0] == other.data[0]:
                return True
        return False
    def __str__(self):
       return str(self.data)


def printLruData(lru,currNode,ceng):
    if ceng==0:
        printLruData(lru,lru.head,ceng+1)
    else:
        print '===================='
        print ceng
        print currNode
        if (currNode.next):
            printLruData(lru,currNode.next,ceng+1)
        else:
            print 'next is None'


if __name__ == '__main__':
    cache = lrucache(100)



    for i in xrange(10):
        if not i==3:
            cache.set(i, i+1,99)
        else:
            cache.set(3,None,99)
        cache.get(2)
    cache.set(9, 123,99)

    time.sleep(2)
    print cache.get(3)
    # printLruData(cache,None,0)

    for key in range(0,10):
        print key,cache.get(key)

    # for key in cache.inner_dd:
    #     # if key in cache.inner_dd.keys():
    #         # print key,cache.get(key)
    #     print key,cache.inner_dd[key]
    #     # else:
    #     #     print key,'None'

