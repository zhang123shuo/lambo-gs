# -*- coding: utf-8 -*-
import time
import urllib2
from BeautifulSoup import BeautifulSoup
import re

stock_code_url = 'http://quote.eastmoney.com/stocklist.html'

url = urllib2.urlopen(stock_code_url)
query = url.read().decode('gbk') 

soup = BeautifulSoup(query)
tag = soup.find('div',{"class":"quotebody"}) 
soup =  BeautifulSoup(str(tag.contents[1]))
tags = soup.findAll('li')

stocks = {} 
for tag in tags:
    text = unicode(tag.text)
    name = text[0:-8]
    code = text[-7:-1]
    stocks[code] = name

import redis
r = redis.Redis()

#del r['stock_code_set']
for k,v in stocks.iteritems():
    r.sadd('stock_code_set',k)



