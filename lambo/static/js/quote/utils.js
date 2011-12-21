function QuotePrint(){}   

var hq = QuotePrint.prototype={
	isZero: function(value){
		return Math.abs(value)<1e-3;
	},
	css: function(value1,value2){
		var value = value1-value2;
		if(this.isZero(value)){
			return "eq";
		}else if(value<0){
			return "neg";
		}else{
			return "pos";
		}
	},
	  
	suspended: function(q){
		return this.isZero(q.price);
	},

	price: function(q){
		if(this.suspended(q)) return '--';
		return sprintf("%.2f",q.price);
	},
	price_delta100: function(q){
		if(this.suspended(q)) return '--';
		return sprintf("%.2f",(q.price-q.closed)*100/q.closed);
	},
	price_delta: function(q){
		if(this.suspended(q)) return '--';
		return sprintf("%.2f",q.price-q.closed);
	},
	
	ask: function(q){
		if(this.suspended(q)) return '--';
		if(this.isZero(q.ask)) return '--';
		return sprintf("%.2f", q.ask);
	},
	
	bid: function(q){
		if(this.suspended(q)) return '--';
		if(this.isZero(q.bid)) return '--'; 
		return sprintf("%.2f", q.bid);
	},
} 