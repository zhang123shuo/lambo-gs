function showChatRoom(){
	$('#chatroom').modal('show');
	if(!eventSocket){ 
		init_ws("ws://localhost:8000/im");
	}
} 
$(function(){     
	$("#chatroom").draggable({handle: 'div.modal-header'}); 
	$(document).keydown(function(e){
		if(e.keyCode==27){
			$('#chatroom').modal('hide');
		}
	});  
});
 

 
 