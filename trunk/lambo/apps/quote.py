# -*- coding: utf-8 -*- 
import tornado.web 
from common import BaseHandler 
  
class QuoteHandler(BaseHandler):   
    def get(self):   
        self.render('quote/quote.html')

class HomeHandler(BaseHandler):   
    quotes = []
    def get(self):   
        if not HomeHandler.quotes:  
            cursor = self.db.quotes.find().sort('code',1).limit(40)
            HomeHandler.quotes = [q for q in cursor] 
        self.render('quote/index2.html',quotes=HomeHandler.quotes)
        
class TestHandler(BaseHandler):   
    def get(self,name):   
        if name.endswith('.html') or name.endswith('.htm'):
            self.render('quote/%s'%name)
        else:
            self.render('quote/%s.html'%name) 
handlers = [ 
    ('', HomeHandler), 
    ('/s', QuoteHandler), 
#   ('/([^/]*)', TestHandler), 
]  