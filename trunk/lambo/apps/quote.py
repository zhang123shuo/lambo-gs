# -*- coding: utf-8 -*- 
import tornado.web 
from common import BaseHandler 
  

class QuoteHandler(BaseHandler):   
    def get(self):   
        self.render('quote/quote.html')
 
handlers = [ 
    ('', QuoteHandler), 
]  