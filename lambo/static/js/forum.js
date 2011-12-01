function enablePopupIMBox() {
	var isCtrl = false;
	$(document).keyup(function(e) {
		if (e.which == 17) isCtrl = false;
	}).keydown(function(e) {
		if (e.which == 17) isCtrl = true;
		if (e.which == 13 && isCtrl) {
			showChatRoom();
		}
	}); 
}
function showChatRoom(){
	$('#chatroom').modal('show');
	$('#msg-box').focus();
	if(!eventSocket){ 
		init_ws("ws://localhost:8000/im");
	}
} 
$(function(){     
	$('#chatroom').modal({keyboard:true})
	$("#chatroom").draggable({handle: 'div.modal-header'}); 
	enablePopupIMBox();
});
 

 
 