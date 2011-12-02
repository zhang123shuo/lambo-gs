function enablePopupIMBox() {
	var isCtrl = false;
	$(document).keyup(function(e) {
		if (e.which == 17) isCtrl = false;
	}).keydown(function(e) {
		if (e.which == 17) isCtrl = true;
		if (e.which == 13 && isCtrl) {
			if(!showChatRoom()){
				isCtrl = false;
			}
		}
	}); 
}
function showChatRoom(){
	if(!$.cookie('uid')){ 
		$("#login input[name=email]").focus();
		alert("亲，你还没登录呢！");
		return false;
	}
	$('#chatroom').modal('show');
	$("#msg-board").prop({ scrollTop : $("#msg-board").prop("scrollHeight")}); 
	$('#msg-box').focus();
	if(!eventSocket){ 
		init_ws("ws://localhost:8080/im");
	}
	return true;
} 
$(function(){       
	$('#chatroom').modal({keyboard:true})
	$("#chatroom").draggable({handle: 'div.modal-header'}); 
	enablePopupIMBox(); 
});
 

 
 