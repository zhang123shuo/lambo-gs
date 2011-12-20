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
        start = int(self.get_argument('idx',0))  #start of forum threads to pull/for paging
        count = int(self.get_argument('cnt',20)) #count of forum threads to pull/for paging
        threads = self.mysql.query('select id,uid,cid,title,created from entries limit %s,%s',start,count)       
        self.render('forum/forum.html',cats=categories,threads=threads, hot_tags=hot_tags)

class ForumFilterHandler(ForumBaseHandler):  
    def get(self):
        cid = int(self.get_argument('cid',-1)) #category id, -1 means all 
        start = int(self.get_argument('idx',0))  #start of forum threads to pull/for paging
        count = int(self.get_argument('cnt',20)) #count of forum threads to pull/for paging
       
        sql = 'select id,uid,cid,title,created from entries'
        if cid != -1:
            sql += ' where cid=%s'%cid
        sql += ' limit %s,%s'
        threads = self.mysql.query(sql,start,count)
        self.render('forum/thread-list.html',threads=threads)

class ThreadHandler(ForumBaseHandler):  
    def get(self,tid): 
        thread = self.mysql.get('select * from entries where id=%s',tid)
        self.render('forum/thread.html',thread=thread)
        
handlers = [ 
    ('', ForumHandler),
    ('filter', ForumFilterHandler),
    ('thread/([^/]*)', ThreadHandler),
]  