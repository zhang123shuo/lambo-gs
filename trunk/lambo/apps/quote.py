# -*- coding: utf-8 -*- 
import tornado.web 
from common import BaseHandler 
 

categories = [ u'上证A股', u'中小企业', u'沪深A股', u'权证', u'债券', u'开放式基金', u'封闭式基金',u'三板' ]
  
class QuoteHandler(BaseHandler):   
    def get(self):   
        self.render('quote/quote.html')

class HomeHandler(BaseHandler):   
    quotes = []
    def get(self):   
        if not HomeHandler.quotes:  
            cursor = self.db.quotes.find().sort('code',1).limit(60)
            HomeHandler.quotes = [q for q in cursor] 
        self.render('quote/index.html',quotes=HomeHandler.quotes,categories = categories, sel=0)
        
class IndexedDBHandler(BaseHandler):   
    def get(self): 
        self.render('quote/db.html') 
handlers = [ 
    ('', HomeHandler), 
    ('/s', QuoteHandler), 
    ('/db', IndexedDBHandler), 
]  