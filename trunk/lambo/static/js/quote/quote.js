var pre_selected, body;

function q_line_clicked(target){ 
	var current = $(target);
	if (pre_selected) pre_selected.removeClass('line_selected');
	current.addClass('line_selected');
	pre_selected = current;
}
function scroll_line(){  
	var cur = pre_selected.position().top;
	var height = pre_selected.height();  
	if(cur > window.innerHeight-20){  
		body.scrollBy(0,height);
	}
	if(cur-height-20 < 0){
		body.scrollBy(0,-height);
	}
}
function next_line(){  
	if(!pre_selected){
		pre_selected = $("#1");
		pre_selected.addClass('line_selected');
		return;
	} 
	if(pre_selected.next().length==0){
		return;
	}
	pre_selected.removeClass('line_selected')
	pre_selected = pre_selected.next();
	pre_selected.addClass('line_selected'); 
	scroll_line();
}
function prev_line(){ 
	if(!pre_selected){
		pre_selected = $("#1");
		pre_selected.addClass('line_selected');
		return;
	}
	if(pre_selected.prev().length==0){
		return;
	}
	pre_selected.removeClass('line_selected')
	pre_selected = pre_selected.prev();
	pre_selected.addClass('line_selected'); 
	scroll_line();
}
$(function(){ 

	body = $('body').get(0); 
	
	$(document).keydown(function(e) {  
		if(e.which==40){ //down
			next_line();  
			return false;
		}else if(e.which==38){ //up
			prev_line();  
			return false;
		}
	}); 
});
 