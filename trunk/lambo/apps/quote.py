# -*- coding: utf-8 -*- 
import tornado.web 
from common import BaseHandler 
 

categories = [ u'上证A股', u'中小企业', u'沪深A股', u'权证', u'债券', u'开放式基金', u'封闭式基金',u'三板' ]
global cached_quotes 
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
        start = self.get_argument('s',0)
        cnt = self.get_argument('n',40)
        quotes = cached_quotes[start:start+cnt]
        res = {'quotes':quotes,'start':start,'count':cnt}
        self.write(res)
              
class IndexedDBHandler(BaseHandler):   
    def get(self): 
        self.render('quote/db.html') 

handlers = [ 
    ('', HomeHandler), 
    ('/s', QuoteHandler), 
    ('/db', IndexedDBHandler), 
    ('/json', JSONQuoteHandler),
]  