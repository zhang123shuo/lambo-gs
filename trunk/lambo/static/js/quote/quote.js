var pre_selected;
var g_quote_frame;
function q_line_clicked(target){ 
	var current = $(target);
	if (pre_selected) pre_selected.removeClass('line_selected');
	current.addClass('line_selected'); 
	pre_selected = current; 
}
function scroll_line(){  
	var cur = pre_selected.position().top; 
	var height = pre_selected.outerHeight();  
	var frameHeight = g_quote_frame.height(); 
	if(cur > frameHeight-height){   
		g_quote_frame.scrollTop(g_quote_frame.scrollTop()+height);
	}
	if(cur < 0){ 
		g_quote_frame.scrollTop(g_quote_frame.scrollTop()-height);
	}
}
function next_line(){  
	if(!pre_selected){ 
		pre_selected = $("#data > ul li:first-child"); 
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
		pre_selected = $("#data > ul li:first-child"); 
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
function isNormalKey(key){
	if(key>=65 && key<=90) return true;
	if(key>=48 && key<=57) return true;
	return false;
}
function showStockQuote(){ 
	$("#quotes").addClass("hide");
	$("#stockQuote").removeClass("hide");
	transform();
}
function showMain(){ 
	$("#quotes").removeClass("hide");
	$("#stockQuote").addClass("hide");
}

function update_column(id,name,value,css){ 
	var $item = $("#" + id + " ."+name);
	
	if(css && !$item.hasClass(css)){  
		$item.removeClass("eq").removeClass("neg").removeClass("pos").addClass(css);
	}
	
	$item.text(value).css("border", "1px solid #C00");
	setTimeout(function(){
		$item.css("border", "1px solid transparent");
	}, 800); 
} 
function init_layout(){
	var header = $("#header"); 
	var top = header.position().top+header.outerHeight();
	var height = $("#footer").position().top - top;
	$("#data").css({"top":top+"px","height":height+"px"}); 
}

function init_ws(host) {
	if ("WebSocket" in window || 'MozWebSocket' in window ) {
		eventSocket = new EventSocket(host); 
		eventSocket.on("quote", function(q) { 
			//depends on hq of hq-utils.js
			if(hq.suspended(q)) return; 
			update_column(q.code,"price-delta100", hq.price_delta100(q), hq.css(q.price,q.closed));
			update_column(q.code,"price",hq.price(q), hq.css(q.price,q.closed));
			update_column(q.code,"price-delta", hq.price_delta(q), hq.css(q.price,q.closed));
			update_column(q.code,"ask",hq.ask(q), hq.css(q.buy1[1],q.closed));
			update_column(q.code,"bid",hq.bid(q), hq.css(q.sell1[1],q.closed));
		}); 
	} else {
		alert("WebSocket not supported");
	} 
}

$(function(){  
	g_quote_frame = $("#data");
	
	var keyshot = $("#keyshot");
	var mouse_in_keyshot = false;
	keyshot.hover(function(){
		mouse_in_keyshot = true;
	},function(){
		mouse_in_keyshot = false;
	});
	function hide_keyshot(){
		$('input',keyshot).val("");
		keyshot.addClass("hide");
	}
	$('body').click(function(e){
		if(!mouse_in_keyshot){
			hide_keyshot();
		}
	});
	$(document).keydown(function(e) {  
		if(e.which==40){ //down
			next_line();  
			return false;
		}else if(e.which==38){ //up
			prev_line();  
			return false;
		}else if(e.which==13){
			showStockQuote();
			
		}else if(e.which==27){
			showMain();
			hide_keyshot();
		}else if(isNormalKey(e.which)){
			keyshot.removeClass("hide");
			$('input',keyshot).focus();
		}
	}); 
	init_layout();
	init_ws("ws://localhost:8080/quote/push");
	$(window).resize(init_layout);
});



 	  
  	  
function transform(){  
	var data = d3.range(40).map(function(i) {
	    return {x: i / 39, y: 20+10*Math.random()};
	});  
  	var	p = 30,
  		w = 1024 - 2*p,
  		h = window.innerHeight - 2*p - 80 ,
  	    x = d3.scale.linear().domain([0, 1]).range([0, w]),
  	    y = d3.scale.linear().domain([20, 30]).range([h, 0]); 
  	
   	d3.select("#my_svg").remove(); 
   	
  	var vis = d3.select("#stockQuote")
  		.data([data])
  		.append("svg:svg")
  		  .attr("id","my_svg")
  		  .attr("width", w + p * 2)
  		  .attr("height", h + p * 2)
  		.append("svg:g")
  		  .attr("transform", "translate(" + p + "," + 4 + ")");
  	 
  	//x-axis
  	var x_ticks = x.ticks(10);
  	var axis_x_count = x_ticks.length;
  	var rules = vis.selectAll("g.rulex")
  	    .data(x_ticks)
  	  .enter().append("svg:g")
  	    .attr("class", "rulex");
  	
  	function axis_x_style(d,i){
  		if(i==0 || i==axis_x_count-1) return "normal";
  		if(i == Math.floor(axis_x_count/2)) return "bold";
  		return "dash";
  	}
  	rules.append("svg:line")
  		.attr("class", axis_x_style)
  		.attr("x1", x)
  		.attr("x2", x)
  		.attr("y1", 0)
  		.attr("y2", h);   
  	rules.append("svg:text")
  		.attr("x", x)
  		.attr("y", h + 3)
  		.attr("dy", ".71em")
  		.attr("text-anchor", "middle")
  		.text(x.tickFormat(axis_x_count));
   
  	
  	//y-axis
  	var y_ticks = y.ticks(20);
  	var axis_y_count = y_ticks.length;
  	var rules = vis.selectAll("g.ruley")
  		.data(y_ticks)
  		.enter().append("svg:g")
  		.attr("class", "ruley");
  	function axis_y_style(d,i){ 
  		if(i == Math.floor(axis_y_count/2)) return "bold";
  		return "normal";
  	}   
  	rules.append("svg:line")
  	    .attr("class", axis_y_style)
  	    .attr("y1", y)
  	    .attr("y2", y)
  	    .attr("x1", 0)
  	    .attr("x2", w + 1);
  	 
  	
  	rules.append("svg:text")
  	    .attr("y", y)
  	    .attr("x", -3)
  	    .attr("dy", ".35em")
  	    .attr("text-anchor", "end")
  	    .text(y.tickFormat(axis_y_count));
  	
  	vis.data([data])
  		.append("svg:path")
  		.attr("class", "line")
  		.attr("d", d3.svg.line()
  				.x(function(d) { return x(d.x); })
  				.y(function(d) { return y(d.y); }));

}
 