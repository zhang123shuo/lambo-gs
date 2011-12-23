!function( $ ){

  "use strict"

  /* DROPDOWN PLUGIN DEFINITION
   * ========================== */

  $.fn.dropdown = function ( selector ) {
    return this.each(function () {
      $(this).delegate(selector || d, 'click', function (e) {
        var li = $(this).parent('li')
          , isActive = li.hasClass('open')

        clearMenus()
        !isActive && li.toggleClass('open')
        return false
      })
    })
  }

  /* APPLY TO STANDARD DROPDOWN ELEMENTS
   * =================================== */

  var d = 'a.menu, .dropdown-toggle'

  function clearMenus() {
    $(d).parent('li').removeClass('open')
  }

  $(function () {
    $('html').bind("click", clearMenus)
    $('body').dropdown( '[data-dropdown] a.menu, [data-dropdown] .dropdown-toggle' )
  })

}( window.jQuery || window.ender );


/** Modals **/
!function( $ ){

	  "use strict"

	 /* CSS TRANSITION SUPPORT (https://gist.github.com/373874)
	  * ======================================================= */

	  var transitionEnd

	  $(document).ready(function () {

	    $.support.transition = (function () {
	      var thisBody = document.body || document.documentElement
	        , thisStyle = thisBody.style
	        , support = thisStyle.transition !== undefined || thisStyle.WebkitTransition !== undefined || thisStyle.MozTransition !== undefined || thisStyle.MsTransition !== undefined || thisStyle.OTransition !== undefined
	      return support
	    })()

	    // set CSS transition event type
	    if ( $.support.transition ) {
	      transitionEnd = "TransitionEnd"
	      if ( $.browser.webkit ) {
	      	transitionEnd = "webkitTransitionEnd"
	      } else if ( $.browser.mozilla ) {
	      	transitionEnd = "transitionend"
	      } else if ( $.browser.opera ) {
	      	transitionEnd = "oTransitionEnd"
	      }
	    }

	  })


	 /* MODAL PUBLIC CLASS DEFINITION
	  * ============================= */

	  var Modal = function ( content, options ) {
	    this.settings = $.extend({}, $.fn.modal.defaults, options)
	    this.$element = $(content)
	      .delegate('.close', 'click.modal', $.proxy(this.hide, this))

	    if ( this.settings.show ) {
	      this.show()
	    }

	    return this
	  }

	  Modal.prototype = {

	      toggle: function () {
	        return this[!this.isShown ? 'show' : 'hide']()
	      }

	    , show: function () {
	        var that = this
	        this.isShown = true
	        this.$element.trigger('show')

	        escape.call(this)
	        backdrop.call(this, function () {
	          var transition = $.support.transition && that.$element.hasClass('fade')

	          that.$element
	            .appendTo(document.body)
	            .show()

	          if (transition) {
	            that.$element[0].offsetWidth // force reflow
	          }

	          that.$element.addClass('in')

	          transition ?
	            that.$element.one(transitionEnd, function () { that.$element.trigger('shown') }) :
	            that.$element.trigger('shown')

	        })

	        return this
	      }

	    , hide: function (e) {
	        e && e.preventDefault()

	        if ( !this.isShown ) {
	          return this
	        }

	        var that = this
	        this.isShown = false

	        escape.call(this)

	        this.$element
	          .trigger('hide')
	          .removeClass('in')

	        $.support.transition && this.$element.hasClass('fade') ?
	          hideWithTransition.call(this) :
	          hideModal.call(this)

	        return this
	      }

	  }


	 /* MODAL PRIVATE METHODS
	  * ===================== */

	  function hideWithTransition() {
	    // firefox drops transitionEnd events :{o
	    var that = this
	      , timeout = setTimeout(function () {
	          that.$element.unbind(transitionEnd)
	          hideModal.call(that)
	        }, 500)

	    this.$element.one(transitionEnd, function () {
	      clearTimeout(timeout)
	      hideModal.call(that)
	    })
	  }

	  function hideModal (that) {
	    this.$element
	      .hide()
	      .trigger('hidden')

	    backdrop.call(this)
	  }

	  function backdrop ( callback ) {
	    var that = this
	      , animate = this.$element.hasClass('fade') ? 'fade' : ''
	    if ( this.isShown && this.settings.backdrop ) {
	      var doAnimate = $.support.transition && animate

	      this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />')
	        .appendTo(document.body)

	      if ( this.settings.backdrop != 'static' ) {
	        this.$backdrop.click($.proxy(this.hide, this))
	      }

	      if ( doAnimate ) {
	        this.$backdrop[0].offsetWidth // force reflow
	      }

	      this.$backdrop.addClass('in')

	      doAnimate ?
	        this.$backdrop.one(transitionEnd, callback) :
	        callback()

	    } else if ( !this.isShown && this.$backdrop ) {
	      this.$backdrop.removeClass('in')

	      $.support.transition && this.$element.hasClass('fade')?
	        this.$backdrop.one(transitionEnd, $.proxy(removeBackdrop, this)) :
	        removeBackdrop.call(this)

	    } else if ( callback ) {
	       callback()
	    }
	  }

	  function removeBackdrop() {
	    this.$backdrop.remove()
	    this.$backdrop = null
	  }

	  function escape() {
	    var that = this
	    if ( this.isShown && this.settings.keyboard ) {
	      $(document).bind('keyup.modal', function ( e ) {
	        if ( e.which == 27 ) {
	          that.hide()
	        }
	      })
	    } else if ( !this.isShown ) {
	      $(document).unbind('keyup.modal')
	    }
	  }


	 /* MODAL PLUGIN DEFINITION
	  * ======================= */

	  $.fn.modal = function ( options ) {
	    var modal = this.data('modal')

	    if (!modal) {

	      if (typeof options == 'string') {
	        options = {
	          show: /show|toggle/.test(options)
	        }
	      }

	      return this.each(function () {
	        $(this).data('modal', new Modal(this, options))
	      })
	    }

	    if ( options === true ) {
	      return modal
	    }

	    if ( typeof options == 'string' ) {
	      modal[options]()
	    } else if ( modal ) {
	      modal.toggle()
	    }

	    return this
	  }

	  $.fn.modal.Modal = Modal

	  $.fn.modal.defaults = {
	    backdrop: false
	  , keyboard: false
	  , show: false
	  }


	 /* MODAL DATA- IMPLEMENTATION
	  * ========================== */

	  $(document).ready(function () {
	    $('body').delegate('[data-controls-modal]', 'click', function (e) {
	      e.preventDefault()
	      var $this = $(this).data('show', true)
	      $('#' + $this.attr('data-controls-modal')).modal( $this.data() )
	    })
	  })

}( window.jQuery || window.ender );
 

//////////////////////////////////////////////////////////////////////////////////////////////////
function unique(arr) {
	var out=[], obj={};
	for (var i=0; i<arr.length; i++) {
		obj[arr[i]]=0;
	}
	for (i in obj) {
		out.push(i);
	}
	return out;
}
function checkEmail($email){
	var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	if (!filter.test($email.val())) {
		return false;
	}
	return true;
}  
function emailHelper(req, responseFn){
	var emails = ['@gmail.com','@163.com', '@126.com', '@qq.com', '@hotmail.com', '@souhu.com', '@sina.com','@yahoo.com'];
	var source = [];
	for(var i=0;i<emails.length;i++){
		var at = req.term.indexOf('@');
		if(at == -1){
			source[i] = req.term+emails[i];
		}else{
			var pre = req.term.substring(0,at);
			var sub = req.term.substring(at); 
			var match = false;
			for(var j=0;j<emails.length;j++){
				if(emails[j].indexOf(sub)==0){ 
					source[i] = pre + emails[j];
					match = true;
				}
			}
			if( !match ) source[i] = req.term;
		}
	}   
	responseFn(unique(source));
}

function login(){
	var email = $("#login input[name=email]").val();
	var password = $("#login input[name=password]").val(); 	
	$.post("/auth/login",{"email":email, "password":password},function(data){
		if(data.status=="0"){
			$("#login").addClass("hide");
			$(".topbar .fill .container").append(data.data);
			g_logged_user = data.user; //mark the global user, fix it with cookie
		}else if(data.status=="-2"){
			alert("亲，密码错误哦!");
		}else if(data.status=="-1"){
			alert("亲，"+email+" 该用户不存在哦!");
		}
	});
}  
$(function(){    
	$('.topbar').dropdown() 
	
	$("#login input[name=password]").keypress(function(e){
		if(e.which == 13){
			login();
	    }
	});
	$("#login input[name=email]").keypress(function(e){
		if(e.which == 13){
			$("#login input[name=password]").focus();
	    }
	});
 
});
 

 
 