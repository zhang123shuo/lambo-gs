# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver 
import tornado.autoreload 
import tornado.database
from tornado.options import define, options

import os.path  
define('port', default=8080,type=int)    

define("mysql_host", default="127.0.0.1:3306")
define("mysql_database", default="promise")
define("mysql_user", default="root")
define("mysql_password", default="123456")   

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
    import socket
    ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
    tornado.options.parse_command_line()
    settings = dict( 
        debug = True, 
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__),'template'),
        cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        autoescape = None, 
        websocket_host = 'ws://%s:8080/im'%'localhost',
    )   
    handlers = build_handlers()
    app = tornado.web.Application(handlers,**settings) 
    
    app.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)
     
    app.cached_users = {} 
    import apps.quote as hq
    hq.start_sina_quote() 
    hq.start_push_quote() 
    
    server = tornado.httpserver.HTTPServer(app) 
    server.listen(options.port) 
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()

if __name__ == '__main__':  
    main()