# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver 
import tornado.autoreload 
from tornado.options import define, options

import os.path  
define('port', default=8000,type=int)   
define('mongodb_host', default='localhost:27017,localhost:27018,localhost:27019')
  
class TestHandler(tornado.web.RequestHandler):
    def get(self,name):
        self.render(name)  


def prefixing_handlers(handlers, prefix, module_handlers): 
    for i in range(len(module_handlers)):
        module_handlers[i] = (prefix + module_handlers[i][0], module_handlers[i][1])
    handlers.extend(module_handlers)
         
def build_handlers(): 
    all_handlers = [ 
        (r'/test/([^/]+)', TestHandler)
    ] 
    from apps.forum import handlers
    prefixing_handlers(all_handlers, '/', handlers) 
    
    return all_handlers
     
def main():
    tornado.options.parse_command_line()
    settings = dict( 
        debug = True, 
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__),'template'),
        cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        autoescape = None, 
    ) 
    handlers = build_handlers()
    
    app = tornado.web.Application(handlers,**settings) 
    import pymongo
    from pymongo import Connection
    conn = Connection(options.mongodb_host) 
    app.db = conn['promise']
    
    server = tornado.httpserver.HTTPServer(app) 
    server.listen(options.port) 
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()

if __name__ == '__main__':  
    main()