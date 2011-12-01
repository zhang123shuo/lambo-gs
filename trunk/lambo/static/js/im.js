var eventSocket; // event socket
function publish() {
	var value = $('#msg-box').val(); 
	if($.trim(value)=='') return;
	eventSocket.emit('publish', {
		'body' : value
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
function init_ws(host) {
	if ("WebSocket" in window) {
		eventSocket = new EventSocket(host); 
		eventSocket.on("publish", function(data) {
			var title = '<a href="#">洪磊明</a><span>[19:14:23]</span>';
			var msg = "<li>" + title + "<p>" + data.body + "</p></li>";
			$("#msgs").append(msg);
			$("#msg-board").prop({
				scrollTop : $("#msg-board").prop("scrollHeight")
			});
		});
 
	} else {
		alert("WebSocket not supported");
	}
	$("#msg-board").prop({
		scrollTop : $("#msg-board").prop("scrollHeight")
	}); 
	enableQuickSend();
}