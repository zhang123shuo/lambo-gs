# -*- coding: utf-8 -*-  
import tornado.websocket 
import logging
import json 
def event(name):
    """Event handler decorator."""
    def handler(f):
        f._event_name = name
        return f

    return handler

class EventMeta(type):
    """Event handler metaclass"""
    def __init__(cls, name, bases, attrs): 
        events = {} 
        for a in attrs:
            attr = getattr(cls, a)
            name = getattr(attr, '_event_name', None)

            if name:
                events[name] = attr

        setattr(cls, '_events', events) 
        super(EventMeta, cls).__init__(name, bases, attrs)


class WebSocketEventHandler(tornado.websocket.WebSocketHandler):
    __metaclass__ = EventMeta
    
            
    def pack_event(self, name, data):
        msg = {'event': name,'data':data}
        return json.dumps(msg)
    
    def unpack_event(self, msg_json):
        return json.loads(msg_json)   
    
    def on_event(self,name,data):
        handler = self._events.get(name)
        if handler is not None:
            try:
                handler(self,data)
            except TypeError:
                logging.error('error try to call event handler %s with args %s'%(handler,repr(data)))
                raise
        else:
            logging.error('Invalid event name: %s' % name)
    
    def emit(self, name, data):
        msg = self.pack_event(name,data)
        self.write_message(msg) 
        
    def on_message(self, message): 
        msg = self.unpack_event(message)
        event = msg['event']
        data = msg['data']
        self.on_event(event,data)   
        
  