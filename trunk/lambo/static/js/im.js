var eventSocket; // event socket
function publish() {
	var value = $('#msg-box').val(); 
	if($.trim(value)=='') return;
	eventSocket.emit('publish', {
		'user': g_logged_user.name,
		'body': value,
		'time': new Date().getTime()
	});
	$("#msg-box").val('');
}

function enableQuickSend() {
	var isCtrl = false;
	$("#msg-box").keyup(function(e) {
		if (e.which == 17) isCtrl = false;
	}).keydown(function(e) {
		if (e.which == 17) isCtrl = true;
		if (e.which == 13 && isCtrl) {
			publish();
		}
	});
}
function append_msg(data){
	var time = new Date(data.time).format("H:i:s"); 
	var title = '<a href="#">'+data.user+'</a> <span>['+time+']</span>';
	var msg = "<li>" + title + "<p>" + data.body + "</p></li>";
	$("#msgs").append(msg);
}
function scroll_board(){
	$("#msg-board").prop({ scrollTop : $("#msg-board").prop("scrollHeight")});
}

function rand(){
	return Math.floor(Math.random()*10);
}
function set_online_count(){
	$("#online-count").html($("#mem-list").children().length);
}
function user_online(u){
	if($("#"+u.uid).length>0) return;
	var user_item = '<li ' + 'id="' + u.uid + '"class="clearfix">' +
		'<a href="#" class="pull-left"><img src="/static/img/avatar/'+rand()+'.jpg"></a>'+
		'<a href="#" class="pull-left">' + u.name + '</a></li>';
	$("#mem-list").append(user_item);
	set_online_count();
}
function user_offline(u){
	$("#"+u.uid).remove();
	set_online_count();
}
function presence_changed(data){
	var u = data.user;
	if(data.status=='offline'){
		user_offline(u);
	}else if(data.status=='online'){ 
		user_online(u);
	}
	
}
function init_ws(host) {
	if ("WebSocket" in window || 'MozWebSocket' in window ) {
		eventSocket = new EventSocket(host); 
		eventSocket.on("publish", function(data) { 
			append_msg(data);
			scroll_board();
		});
		eventSocket.on("init", function(data) { 
			$("#msgs li").remove();
			var msglist = data.history;
			for(var i=0;i<msglist.length;i++){
				append_msg(msglist[i]);
			}
			var users = data.online_users;
			for(var i=0;i<users.length;i++){
				user_online(users[i]);
			}
			scroll_board();
		});
		eventSocket.on("presence", function(data) {  
			presence_changed(data);
		});
	} else {
		alert("WebSocket not supported");
	}
	$("#msg-board").prop({ scrollTop : $("#msg-board").prop("scrollHeight")}); 
	
	enableQuickSend();
}