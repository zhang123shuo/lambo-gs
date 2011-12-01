# -*- coding: utf-8 -*-  
import tornado.websocket 
import logging
import json
from common import BaseHandler   
from websock import WebSocketEventHandler,event
 
_client_sockets = [] 
def monitor():
    import time
    while True:
        logging.warn('sockets connected: %d'%(len(_client_sockets)))
        time.sleep(5)
#import threading
#threading.Thread(target=monitor).start()  

class MultiChatHandler(WebSocketEventHandler): 
    
    def open(self, *args, **kwargs):   
        logging.warning('connected')   
        _client_sockets.append(self.ws_connection)
    
    @event('publish')
    def on_publish(self, **data):
        logging.warning(data['body']) 
        msg = self.pack_event('publish',**data)
        for sock in _client_sockets:
            sock.write_message(msg) 
        
            
    def on_close(self):  
        logging.warning('socket closed') 
        _client_sockets.remove(self.ws_connection) 

handlers = [ 
    (r'', MultiChatHandler), 
]     