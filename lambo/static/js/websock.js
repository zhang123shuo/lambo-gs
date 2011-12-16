
/** websocket encapsulation **/

function pack_event(event,data){
	msg = { 'event': event, 'data': data } 
	return JSON.stringify(msg);
}
function unpack_event(message){
	return JSON.parse(message); 
}

function EventSocket(host){
	this.connect(host);
}

EventSocket.prototype.connect = function(host){
	var sock;
	if ("WebSocket" in window){
		sock = new WebSocket(host);
	} else if ("MozWebSocket" in window){
		sock = new MozWebSocket(host);
	}
	var $this = this;
	sock.onmessage = function(event){
		var msg = unpack_event(event.data); 
		var handler = $this.event_handler(msg.event); 
		if(handler){
			handler(msg.data);
		}
	};
	sock.onclose = function() {
		setTimeout(function() {
			$this.connect(host);
		}, 1000);
	};
	this.socket = sock;
	return this;
} 
EventSocket.prototype.emit = function(event,data){
	var msg = pack_event(event,data)
	this.socket.send(msg);
}

EventSocket.prototype.on = function(name,fn){
	if( !this.event_handlers ){
		this.event_handlers = {}
	}
	this.event_handlers[name] = fn;
}
EventSocket.prototype.event_handler = function(name){
	if(this.event_handlers){
		return this.event_handlers[name];
	}
	return null;
}
