# -*- coding: utf-8 -*- 
import tornado.web
import time
from common import BaseHandler
from pymongo.objectid import ObjectId as _id
from BeautifulSoup import BeautifulSoup

categories = [
    {'id':'1','name':u'中证资讯'},
    {'id':'2','name':u'原创交流'},
    {'id':'3','name':u'金融大杂烩'},
    {'id':'4','name':u'站务/建议'}
]
hot_tags = [
    {'size':'11','name':u'万 科Ａ'},
    {'size':'18','name':u'广汇股份'},
    {'size':'23','name':u'中石油'},
    {'size':'16','name':u'中国建筑'},   
    {'size':'11','name':u'紫金矿业'},
    {'size':'18','name':u'中信证券'},
    {'size':'23','name':u'包钢股份'},
    {'size':'16','name':u'三一重工'},   
]
 
class ForumBaseHandler(BaseHandler):
    pass
            

class ForumHandler(ForumBaseHandler):  
    #@tornado.web.authenticated
    def get(self):  
        start = self.get_argument('idx',0)  #start of forum threads to pull/for paging
        count = self.get_argument('cnt',20) #count of forum threads to pull/for paging
        threads = [] 
        filter = {}
        for thread in self.db.threads.find(filter,{'content':0}).sort('created_at',-1).skip(start).limit(count):
            threads.append(thread)
         
        self.render('forum/forum.html',cats=categories,threads=threads, hot_tags=hot_tags)

class ForumFilterHandler(ForumBaseHandler):  
    def get(self):
        cid = self.get_argument('cid','-1') #category id, -1 means all
        sort = self.get_argument('sort',None) #category id
        start = self.get_argument('idx',0)  #start of forum threads to pull/for paging
        count = self.get_argument('cnt',20) #count of forum threads to pull/for paging
        
        threads,filter = [],{}
        if cid != '-1':
            filter['category'] = cid
            
        for thread in self.db.threads.find(filter,{'content':0}).sort('created_at',-1).skip(start).limit(count):
            threads.append(thread)
        self.render('forum/thread-list.html',threads=threads)

class ThreadHandler(ForumBaseHandler):  
    def get(self,tid): 
        thread = self.db.threads.find_one({'_id': _id(tid)}) 
        self.render('forum/thread.html',thread=thread)
        
handlers = [ 
    ('', ForumHandler),
    ('filter', ForumFilterHandler),
    ('thread/([^/]*)', ThreadHandler),
]  