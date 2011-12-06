# -*- coding: utf-8 -*- 
import tornado.web 
from common import BaseHandler 
  

class QuoteHandler(BaseHandler):   
    def get(self):   
        self.render('quote/quote.html')
        
class TestHandler(BaseHandler):   
    def get(self,name):   
        if name.endswith('.html') or name.endswith('.htm'):
            self.render('quote/%s'%name)
        else:
            self.render('quote/%s.html'%name) 
handlers = [ 
    ('', QuoteHandler), 
    ('/([^/]*)', TestHandler), 
]  