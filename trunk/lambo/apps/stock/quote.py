# -*- coding: utf-8 -*-
import threading
import time
import urllib2  
from datetime import datetime
import pymongo
from pymongo import Connection
from tornado import database 

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
    
def persist_quote(quote,mysql):
    sql = '''
        insert into hq_quotes(code,name,open,closed,price,highest,lowest,ask,bid,volume,turnover,
        buy1_cnt,buy1_price,buy2_cnt,buy2_price,buy3_cnt,buy3_price,buy4_cnt,buy4_price,buy5_cnt,buy5_price,
        sell1_cnt,sell1_price,sell2_cnt,sell2_price,sell3_cnt,sell3_price,sell4_cnt,sell4_price,sell5_cnt,sell5_price,
        date,time)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
               %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
               %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
               %s,%s,%s)
    ''' 
    mysql.execute(sql,*quote)
    
       
def parse_quote(code,qstr,mysql):
    q = qstr.split(',') 
    q.insert(0, code)
    persist_quote(q,mysql)
    
def query_quote(codes,mysql):    
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
        parse_quote(code,qstr,mysql) 
 
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
    mysql = database.Connection(host='localhost',database='promise',user='root',password='123456')
    while True:
        if is_market_time():
            query_quote(codes,mysql) 
        time.sleep(freq)
 

def start_quote():
    group_stocks()   
    for codes in _stock_groups:  
        threading.Thread(target=quote_routine,args=(codes,10)).start()

if __name__=='__main__':   
    start_quote() 
    time.sleep(1000000) 