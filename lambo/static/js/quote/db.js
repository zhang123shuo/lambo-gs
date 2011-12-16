var quote = {};
var indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB;

if ('webkitIndexedDB' in window) {
	window.IDBTransaction = window.webkitIDBTransaction;
	window.IDBKeyRange = window.webkitIDBKeyRange;
}

quote.db = {};
quote.db.database = null;
quote.db.onerror = function(e) {
	console.log(e);
};

quote.db.open = function(dbName,version) {
	var request = indexedDB.open(dbName);
	request.onsuccess = function(e) { 
		var db = quote.db.database = e.target.result;
		// We can only create Object stores in a setVersion transaction;
		if (version!= db.version) {
			var setVrequest = db.setVersion(version);  
			setVrequest.onerror = quote.db.onerror;
			setVrequest.onsuccess = function(e) {
				if(db.objectStoreNames.contains("quote")) {
					db.deleteObjectStore("quote");
				} 
				var store = db.createObjectStore("quote", {keyPath: "code"}); 
			};
		}
	}; 
	request.onerror = quote.db.onerror;
}

quote.db.addQuote = function(quote) {
	var db = quote.db.database;
	var trans = db.transaction(["quote"], IDBTransaction.READ_WRITE);
	var store = trans.objectStore("quote");
	var request = store.put(quote);
	request.onsuccess = function(e) { 
	};
	request.onerror = function(e) {
		console.log("Error Adding: ", e);
	};
};

quote.db.deleteQuote = function(code) {
	var db = quote.db.database;
	var trans = db.transaction(["quote"], IDBTransaction.READ_WRITE);
	var store = trans.objectStore("quote");
	var request = store.delete(code);
	request.onsuccess = function(e) { 
		
	};
	request.onerror = function(e) {
		console.log("Error Adding: ", e);
	};
};

quote.db.getQuotes = function() { 
	var db = quote.db.database;
	var trans = db.transaction(["quote"], IDBTransaction.READ_WRITE);
	var store = trans.objectStore("quote"); 
	// Get everything in the store;
	var keyRange = IDBKeyRange.lowerBound(0);
	var cursorRequest = store.openCursor(keyRange);
	cursorRequest.onsuccess = function(e) {
		var result = e.target.result;
		if(!!result == false) return;
		
		//quote handling
		
		result.continue();
	};

	cursorRequest.onerror = quote.db.onerror;
};
