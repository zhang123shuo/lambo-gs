# -*- coding: utf-8 -*- 
import tornado.web 
from random import randrange as rand
from random import uniform

import json
import time

from common import BaseHandler 
from websock import WebSocketEventHandler,event
 

categories = [ u'上证A股', u'中小企业', u'沪深A股', u'权证', u'债券', u'开放式基金', u'封闭式基金',u'三板' ]
global cached_quotes 
cached_quotes = []
cached_sockets = [] 
def broadcast(msg):
    for sock in cached_sockets:
        sock.write_message(msg)  

def push_quote():
    quotes = cached_quotes[0:60]
    while True:
        n = len(quotes)
        q = quotes[rand(n)]
        p = float(q['price'])+uniform(-2,2)
        if p < 0: p = 0
        q['price'] = '%.2f'%p
        msg = {'event':'quote','data': q}
        broadcast(json.dumps(msg))
        time.sleep(.5)
        
def load_quotes(db):
    cursor = db.quotes.find({},{'_id':0}).sort('code',1)
    global cached_quotes 
    cached_quotes = [q for q in cursor]

class QuoteHandler(BaseHandler):   
    def get(self):   
        self.render('quote/quote.html')

class HomeHandler(BaseHandler):  
    def get(self):   
        quotes = cached_quotes[0:60]
        self.render('quote/index.html',quotes=quotes,categories = categories, sel=0)
        
class JSONQuoteHandler(BaseHandler):  
    def get(self):   
        start = self.get_argument('start',0)
        cnt = self.get_argument('count', 40)
        start,cnt = int(start),int(cnt)
        quotes = cached_quotes[start:start+cnt]
        res = {'quotes':quotes,'start':start,'count':cnt}
        self.write(res)
              
class IndexedDBHandler(BaseHandler):   
    def get(self): 
        self.render('quote/db.html')

class QuotePushHandler(WebSocketEventHandler):  
    
    def open(self, *args, **kwargs):  
        cached_sockets.append(self.ws_connection)  
    

    def on_close(self):  
        cached_sockets.remove(self.ws_connection)  


handlers = [ 
    ('', HomeHandler), 
    ('/s', QuoteHandler), 
    ('/push', QuotePushHandler), 
    ('/db', IndexedDBHandler), 
    ('/json', JSONQuoteHandler),
]  