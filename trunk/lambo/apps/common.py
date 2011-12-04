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
        uid = str(user['_id'])
        self.cached_users[uid] = user
    
    def user(self,uid): #load user from cache
        uid = str(uid)
        if uid in self.cached_users: return self.cached_users[uid]
        u = self.db.users.find_one({'_id':_id(uid)})
        if u is None: return None
        self.cache_user(u)
        return u
    
    def load_user(self,email): #load user via email
        u = self.db.users.find_one({'email': email})
        if u is not None:   
            self.cache_user(u)
        return u
 
        
class LoginHandler(BaseHandler): 
    def get(self):  
        self.render('login.html') 
    
    def post(self):
        email = self.get_argument('email')  
        password = self.get_argument('password')
        res = {'status': '0'}
        user = self.load_user(email)
        if user is None:
            res['status'] = '-1'
        elif user['password'] == password:  
            self.set_secure_cookie('email',email) 
            self.set_secure_cookie('name',user['name']) 
            self.set_secure_cookie('uid',str(user['_id']))    
            res['data'] = '''
                <ul class="nav secondary-nav">
                    <li class="dropdown">
                      <a href="#" class="dropdown-toggle">%s</a>
                      <ul class="dropdown-menu">
                        <li><a href="#">设 置</a></li> 
                        <li><a href="/auth/logout">退 出</a></li>
                      </ul>
                    </li>
                </ul>'''%user['name']
            res['user'] = {'uid':str(user['_id']), 'name': user['name'], 'email': email }
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