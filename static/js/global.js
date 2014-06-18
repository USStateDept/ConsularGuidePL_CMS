mconfirm = function(title, text, confirm_callback, close_callback) {
	var confirmed = false;
	$('#mconfirm-modal').find('.modal-body').html(text);
	$('#mconfirm-modal').find('.modal-title').html(title);
	$('#mconfirm-modal').find('.btn-primary').off().click(function(){
		confirmed = true;
		confirm_callback();
		$('#mconfirm-modal').modal('hide');
	});
	$('#mconfirm-modal').off().on('hide.bs.modal', function(){
		if(!confirmed && close_callback)
			close_callback();
	});
	$('#mconfirm-modal').modal();
};

function isNumber(value) {
    if ((undefined === value) || (null === value)) {
        return false;
    }
    if (typeof value == 'number') {
        return true;
    }
    return !isNaN(value - 0);
}

$(function(){
	$('select.form-control').selectpicker({
		style: 'btn-lg'
	});
	$('.hover-tooltip').each(function(){
		$(this).tooltip({
			trigger:'hover',
			placement: 'auto'
		});
	});
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$.fn.directText=function(delim) {
  if (!delim) delim = '';
  return this.contents().map(function() { return this.nodeType == 3 ? this.nodeValue : undefined}).get().join(delim);
};