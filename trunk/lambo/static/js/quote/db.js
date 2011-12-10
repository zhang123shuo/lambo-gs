var quote = {};
var indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB;

if ('webkitIndexedDB' in window) {
	window.IDBTransaction = window.webkitIDBTransaction;
	window.IDBKeyRange = window.webkitIDBKeyRange;
}

quote.indexedDB = {};
quote.indexedDB.db = null;

quote.indexedDB.onerror = function(e) {
	console.log(e);
};

quote.indexedDB.open = function() {
	var request = indexedDB.open("todos");
	request.onsuccess = function(e) {
	    var v = "1.99";
	    quote.indexedDB.db = e.target.result;
	    var db = quote.indexedDB.db;
	    // We can only create Object stores in a setVersion transaction;
	    if (v!= db.version) {
	    	var setVrequest = db.setVersion(v);
		    // onsuccess is the only place we can create Object Stores
		    setVrequest.onerror = quote.indexedDB.onerror;
		    setVrequest.onsuccess = function(e) {
		    	if(db.objectStoreNames.contains("todo")) {
		    		  db.deleteObjectStore("todo");
		    	  }
		    	  var store = db.createObjectStore("todo", keyPath: "timeStamp"});
		    	  quote.indexedDB.getAllTodoItems();
		      };
	    }
    else {
      quote.indexedDB.getAllTodoItems();
    }
  };

  request.onerror = quote.indexedDB.onerror;
}

quote.indexedDB.addTodo = function(todoText) {
  var db = quote.indexedDB.db;
  var trans = db.transaction(["todo"], IDBTransaction.READ_WRITE);
  var store = trans.objectStore("todo");

  var data = {
    "text": todoText,
    "timeStamp": new Date().getTime()
  };

  var request = store.put(data);

  request.onsuccess = function(e) {
    quote.indexedDB.getAllTodoItems();
  };

  request.onerror = function(e) {
    console.log("Error Adding: ", e);
  };
};

quote.indexedDB.deleteTodo = function(id) {
  var db = quote.indexedDB.db;
  var trans = db.transaction(["todo"], IDBTransaction.READ_WRITE);
  var store = trans.objectStore("todo");

  var request = store.delete(id);

  request.onsuccess = function(e) {
    quote.indexedDB.getAllTodoItems();
  };

  request.onerror = function(e) {
    console.log("Error Adding: ", e);
  };
};

quote.indexedDB.getAllTodoItems = function() {
  var todos = document.getElementById("todoItems");
  todos.innerHTML = "";

  var db = quote.indexedDB.db;
  var trans = db.transaction(["todo"], IDBTransaction.READ_WRITE);
  var store = trans.objectStore("todo");

  // Get everything in the store;
  var keyRange = IDBKeyRange.lowerBound(0);
  var cursorRequest = store.openCursor(keyRange);

  cursorRequest.onsuccess = function(e) {
    var result = e.target.result;
    if(!!result == false)
      return;

    renderTodo(result.value);
    result.continue();
  };

  cursorRequest.onerror = quote.indexedDB.onerror;
};

function renderTodo(row) {
  var todos = document.getElementById("todoItems");
  var li = document.createElement("li");
  var a = document.createElement("a");
  var t = document.createTextNode(row.text);

  a.addEventListener("click", function() {
    quote.indexedDB.deleteTodo(row.timeStamp);
  }, false);

  a.textContent = " [Delete]";
  li.appendChild(t);
  li.appendChild(a);
  todos.appendChild(li)
}

function addTodo() {
  var todo = document.getElementById("todo");
  quote.indexedDB.addTodo(todo.value);
  todo.value = "";
}

function init() {
  quote.indexedDB.open();
}

window.addEventListener("DOMContentLoaded", init, false);​