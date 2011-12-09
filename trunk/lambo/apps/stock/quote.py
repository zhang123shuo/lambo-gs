# -*- coding: utf-8 -*-
import threading
import time
import urllib2  
from datetime import datetime
import pymongo
from pymongo import Connection
conn = Connection('localhost:27017,localhost:27018,localhost:27019') 
db = conn['promise']

_quotes = {}
_stock_groups = [] 
import redis
r = redis.Redis()
def group_stocks():
    codes = r.smembers('stock_code_set')
    stocks = []
    for s in codes: 
        if s.startswith('6') or s.startswith('5'):  
            stocks.append('sh%s'%s)         
        if s.startswith('0') or s.startswith('3') or s.startswith('1'):  
            stocks.append('sz%s'%s)  
            
        if len(stocks) == 100:
            _stock_groups.append(','.join(stocks))
            stocks = []
    if len(stocks)>0: _stock_groups.append(','.join(stocks)) 
    
def persist_quote(quote):
    db.quotes.update({'code':quote['code']},quote,True)
       
def parse_quote(code,qstr):
    q = qstr.split(',')
    if(code in _quotes): quote = _quotes[code]
    else: _quotes[code] = quote = {}  
    quote['code'] = code
    quote['name'] = q[0]
    quote['open'] = float(q[1])
    quote['closed'] = float(q[2])
    quote['price'] = float(q[3])
    quote['highest'] = float(q[4])
    quote['lowest'] = float(q[5])
    quote['volume'] = int(q[8])
    quote['turnover'] = float(q[9])
    quote['buy1'] = (int(q[10]),float(q[11]))
    quote['buy2'] = (int(q[12]),float(q[13]))
    quote['buy3'] = (int(q[14]),float(q[15]))
    quote['buy4'] = (int(q[16]),float(q[17]))
    quote['buy5'] = (int(q[18]),float(q[19])) 
    quote['sell1'] = (int(q[20]),float(q[21]))
    quote['sell2'] = (int(q[22]),float(q[23]))
    quote['sell3'] = (int(q[24]),float(q[25]))
    quote['sell4'] = (int(q[26]),float(q[27]))
    quote['sell5'] = (int(q[28]),float(q[29]))
    print quote['code'], quote['name'], quote['price']
    persist_quote(quote)
    return quote 

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

def quote_routine(codes,freq=10): 
    while True:
        if is_market_time():
            query_quote(codes) 
        time.sleep(freq)
 

def start_quote():
    group_stocks()   
    for codes in _stock_groups:  
        threading.Thread(target=quote_routine,args=(codes,10)).start()

if __name__=='__main__':   
    start_quote() 
    time.sleep(1000000) 