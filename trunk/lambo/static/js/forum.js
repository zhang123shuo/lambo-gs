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
		init_ws(g_websocket_host);
	}
	return true;
} 

function categoryClicked(target){ 
	$target = $(target);
	if($target.hasClass("active")) return;
	$ul = $target.parent();
	$(".active",$ul).removeClass("active");
	$target.addClass("active");
	
	$.get('./filter',{ 'cid':$target.val()},function(data){
		$("#threads").html(data);
	});
}
function show_body(tid){ 
	if($("#"+tid+" .slide").children().length>0){
		$("#"+tid+" .snapshot").hide();
		$("#"+tid+" .slide").show();
		return;
	}
	$.get('./thread/'+tid,function(data){
		$("#"+tid+" .snapshot").hide();
		$("#"+tid+" .slide").html(data).show();
	});
}

function hide_body(tid){ 
	$("#"+tid+" .snapshot").show();
	$("#"+tid+" .slide").hide();
}

function init_draggable(){
	var drag = new DragResize('drag', { minWidth: 50, minHeight: 50}); 
	drag.isElement = function(elm){
		if (elm.className && elm.className.indexOf('drsElement') > -1) return true;
	};
	drag.isHandle = function(elm){
	 	if (elm.className && elm.className.indexOf('drsMoveHandle') > -1) return true;
	}; 
	drag.apply(document);
}
$(function(){       
	$('#chatroom').modal({keyboard:true}) 
	//$("#chatroom").draggable({handle: 'div.modal-header'}); 
	init_draggable();
	enablePopupIMBox(); 
});
 

 
 