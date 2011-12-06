# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver 
import tornado.autoreload 
from tornado.options import define, options

import os.path  
define('port', default=8080,type=int)   
define('mongodb_host', default='localhost:27017,localhost:27018,localhost:27019')
   
def prefixing_handlers(handlers, prefix, module_handlers): 
    for i in range(len(module_handlers)):
        module_handlers[i] = (prefix + module_handlers[i][0], module_handlers[i][1])
    handlers.extend(module_handlers)
         
def build_handlers(): 
    all_handlers = []  
    
    from apps.forum import handlers
    prefixing_handlers(all_handlers, '/', handlers) 
    
    from apps.common import handlers
    prefixing_handlers(all_handlers, '/auth', handlers) 
    
    from apps.im import handlers
    prefixing_handlers(all_handlers, '/im', handlers) 
    
    from apps.quote import handlers
    prefixing_handlers(all_handlers, '/quote', handlers) 
    
    return all_handlers
     
def main():
    tornado.options.parse_command_line()
    settings = dict( 
        debug = True, 
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__),'template'),
        cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        autoescape = None, 
        websocket_host = 'ws://localhost:8080/im',
    ) 
    handlers = build_handlers()
    
    app = tornado.web.Application(handlers,**settings) 
    import pymongo
    from pymongo import Connection
    conn = Connection(options.mongodb_host) 
    app.db = conn['promise']
    app.cached_users = {} 
    
    server = tornado.httpserver.HTTPServer(app) 
    server.listen(options.port) 
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()

if __name__ == '__main__':  
    main()