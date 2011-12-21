# -*- coding: utf-8 -*- 
import tornado.web 
import threading
import time
import urllib2  
from datetime import datetime

from random import randrange as rand
from random import uniform

import json
import time

from common import BaseHandler 
from websock import WebSocketEventHandler,event
 
categories = [ u'上证A股', u'中小企业', u'沪深A股', u'权证', u'债券', u'开放式基金', u'封闭式基金',u'三板' ]

cached_quotes = {}
cached_sockets = [] 
sorted_quotes = []
 
def start_sina_quote():
    def parse_quote(code,qstr):
        global cached_quotes 
        q = qstr.split(',')
        if(code in cached_quotes): quote = cached_quotes[code]
        else: cached_quotes[code] = quote = {}  
        quote['code'] = code
        quote['name'] = q[0]
        quote['open'] = float(q[1])
        quote['closed'] = float(q[2])
        quote['price'] = float(q[3])
        quote['highest'] = float(q[4])
        quote['lowest'] = float(q[5])
        quote['volume'] = int(q[8])
        quote['turnover'] = float(q[9])
        quote['buy1'] = [int(q[10]),float(q[11])]
        quote['buy2'] = [int(q[12]),float(q[13])]
        quote['buy3'] = [int(q[14]),float(q[15])]
        quote['buy4'] = [int(q[16]),float(q[17])]
        quote['buy5'] = [int(q[18]),float(q[19])] 
        quote['sell1'] = [int(q[20]),float(q[21])]
        quote['sell2'] = [int(q[22]),float(q[23])]
        quote['sell3'] = [int(q[24]),float(q[25])]
        quote['sell4'] = [int(q[26]),float(q[27])]
        quote['sell5'] = [int(q[28]),float(q[29])]
        #print quote['code'], quote['name'], quote['price'] 
    def query_quote(codes):    
        start = time.time()
        url = urllib2.urlopen('http://hq.sinajs.cn/list=%s'%codes)
        query = url.read().decode('gbk') 
        end = time.time() 
        #print 'time[s]: %f'%(end-start)
        for item in query.split('\n'):
            if not item: continue
            q = item.split('=') 
            code = q[0][-6:]
            qstr = q[1][1:-2]
            if qstr=='': continue 
            parse_quote(code,qstr)
            
    def is_market_time(): 
        return True
        tt = datetime.now().timetuple() 
        if tt[6]>5: return False #week end
        morning = (9*60+15,11*60+30)
        afternoon = (13*60,15*60)
        m = tt[3]*60 + tt[4]
        if m>=morning[0] and m<=morning[1] or m>=afternoon[0] and m<=afternoon[1]:
            return True
        return False      
      
    import redis
    r = redis.Redis()
    stock_groups = []
    stocks = []
    codes = r.smembers('stock_code_set')
    for s in codes: 
        if s.startswith('6') or s.startswith('5'):  
            stocks.append('sh%s'%s)         
        if s.startswith('0') or s.startswith('3') or s.startswith('1'):  
            stocks.append('sz%s'%s)  
            
        if len(stocks) == 100:
            stock_groups.append(','.join(stocks))
            stocks = []
    if len(stocks)>0: stock_groups.append(','.join(stocks)) 
    
    def quote_routine(codes,freq=10): 
        while True:
            if is_market_time():
                query_quote(codes) 
            time.sleep(freq) 
    for codes in stock_groups:   
        threading.Thread(target=quote_routine,args=(codes,10)).start()
    



def push_quote():  
    while True:
        global sorted_quotes
        if len(sorted_quotes)==0:
            sorted_quotes =[v for k,v in sorted(cached_quotes.iteritems())]
        quotes = sorted_quotes[0:60]
        n = len(quotes)
        if n<=0:
            time.sleep(1)
            continue
        q = quotes[rand(n)] 
        
        msg = {'event':'quote','data': q}
        broadcast(json.dumps(msg))
        time.sleep(.5)
        
def broadcast(msg):
    for sock in cached_sockets:
        sock.write_message(msg)  
                 

class QuoteHandler(BaseHandler):   
    def get(self):   
        self.render('quote/quote.html')

class HomeHandler(BaseHandler): 
    def get(self):   
        global sorted_quotes
        if len(sorted_quotes)==0:
            sorted_quotes =[v for k,v in sorted(cached_quotes.iteritems())]
        quotes = sorted_quotes[0:60]
        
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