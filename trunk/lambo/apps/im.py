# -*- coding: utf-8 -*-  
import tornado.websocket 
import logging
import json
import time 
from common import BaseHandler   
from websock import WebSocketEventHandler,event
 

def monitor():
    while True:
        logging.warn('sockets connected: %d'%(len(_client_sockets)))
        time.sleep(5)
#import threading
#threading.Thread(target=monitor).start()  

class WebIMHandler(WebSocketEventHandler): 
    cached_sockets = {}
    cached_users = {}
    
    def persist(self,msg):
        logging.warn('persisting %s'%repr(msg))
        self.db.msgs.save(msg)
    
    def timeline(self,start=0,count=20):
        logging.warn('timeline from %s'%start) 
        cursor = self.db.msgs.find({},{'_id':0}).sort('time',-1).limit(count)
        msgs = [m for m in cursor]
        msgs.reverse()
        return msgs
    
    def broadcast(self,msg):
        for k,sock in WebIMHandler.cached_sockets.items():
            sock.write_message(msg) 
            
    @property
    def logged_user(self):
        return {
            'uid': self.get_secure_cookie('uid'),
            'name': self.get_secure_cookie('name')
        } 
    
    @property
    def db(self):
        return self.application.db
    
    def enlist(self):
        user = self.logged_user  
        logging.warning('connected, %s'%user['uid'])    
        WebIMHandler.cached_sockets[user['uid']] = self.ws_connection
        WebIMHandler.cached_users[user['uid']] = user
        return user
    
    def delist(self):
        user = self.logged_user
        logging.warning('disconnected %s'%user['uid'])  
        WebIMHandler.cached_sockets.pop(user['uid']) 
        WebIMHandler.cached_users.pop(user['uid'])
        return user
    
    def open(self, *args, **kwargs):  
        user = self.enlist()
        
        data = {
            'history': self.timeline(),
            'online_users': WebIMHandler.cached_users.values()
        }     
        msg = self.pack_event('init',data)
        self.write_message(msg)
        
        msg = self.pack_event('presence', { 'user': user, 'status': 'online' })
        self.broadcast(msg)
    
    @event('publish')
    def on_publish(self, data): 
        msg = self.pack_event('publish', data)
        self.persist(data)
        self.broadcast(msg)
        
            
    def on_close(self):  
        user = self.delist()

        msg = self.pack_event('presence', { 'user':user, 'status':'offline' })
        self.broadcast(msg)

handlers = [ 
    (r'', WebIMHandler), 
]     