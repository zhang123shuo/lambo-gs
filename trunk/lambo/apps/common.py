# -*- coding: utf-8 -*- 
try:
    import cPickle as pickle
except:
    import pickle

import logging
import uuid    
import tornado.web   
from pymongo.objectid import ObjectId as _id
import time
import datetime
one_day = datetime.timedelta(days=1)
one_hour = datetime.timedelta(hours=1)

class QuotePrint:  
    @classmethod
    def css(cls,value1,value2):
        value = float(value1)-float(value2)
        if abs(value)<1e-3:
            return 'eq'
        elif value<0: 
            return 'neg'
        else: return 'pos'

    @classmethod
    def suspended(cls,q):
        return abs(q.price)<1e-3 or abs(q.closed)<1e-3
    
    #涨跌幅 %
    @classmethod
    def price_delta100(cls,q):
        if cls.suspended(q): return '--'
        return '%.2f'%((q.price-q.closed)*100/q.closed)
    
    #价格 %
    @classmethod
    def price(cls,q):
        if cls.suspended(q): return '--'
        return '%.2f'%q.price
    
    #涨跌
    @classmethod
    def price_delta(cls,q):
        if cls.suspended(q): return '--'
        return '%.2f'%(q.price-q.closed)
    
    #成交额
    @classmethod
    def turnover(cls,q):
        if cls.suspended(q): return '--'
        if q.turnover/100000000 >= 1:
            return u'%.1f亿'%(q.turnover/100000000)
        return u'%.0f万'%(q.turnover/10000)
    
    #买入价
    @classmethod
    def ask(cls,q):
        if cls.suspended(q): return '--'
        if abs(q.ask)<1e-3: return '--'
        
        return '%.2f'%(q.ask) 

    #卖出价
    @classmethod 
    def bid(cls,q):
        if cls.suspended(q): return '--'
        if abs(q.bid)<1e-3: return '--'
        return '%.2f'%(q.bid) 
    
    #今开
    @classmethod
    def open(cls,q):
        if cls.suspended(q): return '--'
        return '%.2f'%(q.open) 
    
    #最高价
    @classmethod
    def highest(cls,q):
        if cls.suspended(q): return '--'
        return '%.2f'%(q.highest)
    
    #最低价
    @classmethod
    def lowest(cls,q):
        if cls.suspended(q): return '--'
        return '%.2f'%(q.lowest) 
    
    #振幅
    @classmethod
    def price_amp100(cls,q):
        if cls.suspended(q): return '--'
        return '%.2f'%((q.highest-q.lowest)*100/q.lowest)
    
def time_fmt(value):     
    tm_now = time.localtime()    
    
    tm_lastday = (datetime.date.today() - one_day).timetuple() 
    tm_today = datetime.date.today().timetuple()
    tm_lasthour = (datetime.datetime.now() - one_hour).timetuple()
    
    t = tm_value = time.localtime(value) 
    if tm_value.tm_year < tm_now.tm_year: 
        return u'%d年%d月%d日 %02d:%02d'%(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min)
    
    if tm_value > tm_lasthour:
        minutes = (tm_now.tm_min-t.tm_min+60)%60
        if minutes > 0:
            return u'%d分钟前'%minutes
        else: 
            return u'刚刚'
    
    if tm_value > tm_today:
        return u'今天 %02d:%02d'%(t.tm_hour,t.tm_min)
    
    if tm_value > tm_lastday:
        return u'昨天 %02d:%02d'%(t.tm_hour,t.tm_min)
    
    return u'%d月%d日 %02d:%02d'%(t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min)
 

 
class BaseHandler(tornado.web.RequestHandler):     
    @property  
    def db(self):  #get application mongodb instance
        return self.application.db 
    
    @property  
    def settings(self):  #get application mongodb instance
        return self.application.settings 
    
    @property
    def upload_path(self):
        return self.settings['upload_path']
    
    @property
    def download_url(self):
        return self.settings['download_url']
    
    
    def get_current_user(self): #get current logged in user
        if self.get_secure_cookie('uid', None) is None: 
            return None
        user = {
            'uid': self.get_secure_cookie('uid', None),
            'email': self.get_secure_cookie('email', None) ,
            'name': self.get_secure_cookie('name', None) 
        }
        return user
    
    @property  
    def cached_users(self): 
        return self.application.cached_users
    
    def cache_user(self,user): #to cache use 
        uid = str(user['id'])
        self.cached_users[uid] = user
    
    def user(self,uid): #load user from cache
        uid = str(uid)
        if uid in self.cached_users: return self.cached_users[uid] 
        u = self.db.get("select * from users where id=%s"%uid)
        if u is None: return None
        self.cache_user(u)
        return u
    
    def load_user(self,email): #load user via email 
        u = self.db.get("select * from users where email='%s'"%email)
        if u is not None:   
            self.cache_user(u)
        return u
 
        
class LoginHandler(BaseHandler):  
    def post(self):
        email = self.get_argument('email')  
        password = self.get_argument('password')
        res = {'status': '0'}
        user = self.load_user(email) 
        if user is None:
            res['status'] = '-1'
        elif user['pwd'] == password:  
            self.set_secure_cookie('email',email) 
            self.set_secure_cookie('name',user['name']) 
            self.set_secure_cookie('uid',str(user['id']))    
            res['data'] = u'''
                <ul class="nav secondary-nav">
                    <li class="dropdown">
                      <a href="#" class="dropdown-toggle">%s</a>
                      <ul class="dropdown-menu">
                        <li><a href="#">设 置</a></li> 
                        <li><a href="/auth/logout">退 出</a></li>
                      </ul>
                    </li>
                </ul>'''%user['name']
            res['user'] = {'uid':str(user['id']), 'name': user['name'], 'email': email }
        else:
            res['status'] = '-2' 
        
        self.write(res)

class LogoutHandler(BaseHandler):  
    def get(self):
        self.clear_cookie('uid')   
        self.clear_cookie('email')  
        self.clear_cookie('name')  
        self.redirect('/')
 

    
handlers = [ 
    ('/login', LoginHandler), 
    ('/logout', LogoutHandler)
] 