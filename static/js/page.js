// ----------------------------------------------------------
// A short snippet for detecting versions of IE in JavaScript
// without resorting to user-agent sniffing
// ----------------------------------------------------------
// If you're not in IE (or IE version is less than 5) then:
// ie === undefined
// If you're in IE (>=5) then you can determine which version:
// ie === 7; // IE7
// Thus, to detect IE:
// if (ie) {}
// And to detect the version:
// ie === 6 // IE6
// ie > 7 // IE8, IE9 ...
// ie < 9 // Anything less than IE9
// ----------------------------------------------------------

// UPDATE: Now using Live NodeList idea from @jdalton
// https://gist.github.com/padolsey/527683
var ie = (function(){

    var undef,
        v = 3,
        div = document.createElement('div'),
        all = div.getElementsByTagName('i');

    while (
        div.innerHTML = '<!--[if gt IE ' + (++v) + ']><i></i><![endif]-->',
        all[0]
    );
    return v > 4 ? v : undef;
}());

function installSortables()
{
    $('#remove-item').sortable({
        tolerance: 'pointer',
        connectWith: '.sortable',
        dropOnEmpty: true,
        receive: function(event, ui){
            mconfirm('Confirm page removal',
                    'Are you sure you want to remove this page? <br/>' +
                    'Warning: Removing page will result in its child pages removal.', function(){
                $('#'+ui.item.attr('id')).remove();
            });
            $(ui.sender).sortable('cancel');
        }
    });
    $('.sortable').sortable({
        tolerance: 'pointer',
        connectWith: '#remove-item',
        dropOnEmpty: true
    });
}

var form_edited = false;

function exitEditCallback(next)
{
    if (!form_edited) {
        return true;
    }
    mconfirm(
        'Exit page edit',
        'Are you sure you want to exit page edit? Unsaved data will be lost.',
        function(){
            window.location.replace(next);
        }
    );
    return false;
}

$(function() {
    $('#form-content').on('submit', '#page-edit-form', function(){
        var items = [];
        var template = '<input type="hidden" name="children_order" value="">';
        $('#items-list li').each(function(){
            items.push($(this).data('id'));
        });
        $(template).val(JSON.stringify(items)).appendTo($('#page-edit-form'));
    });

    $('#form-content').on('click', '.remove-question', function() {
        $(this).parent().remove();
        return false;
    });

    if (ie && ie < 9) {
        mconfirm(
            'Your browser is not supported. Please use Chrome or Firefox.',
            'Redirect to main page?',
            function(){
                window.location.replace("/");
            }
        );
        return false;
    }

    $('#topnav').on('click', 'a', function(){
        $self = $(this);
        next = $self.attr('href');
        return exitEditCallback(next);
    });

    $('#left-panel .content-tree').on('click', 'a', function(){
        $self = $(this);
        next = $self.attr('href');
        return exitEditCallback(next);
    });

    $('a#parent-link').on('click', function(){
        $self = $(this);
        next = $self.attr('href');
        return exitEditCallback(next);
    });

    $('#form-content').on('click', '#create-child-url', function(){
        $self = $(this);
        next = $self.attr('href');
        return exitEditCallback(next);
    });

    $('#form-content').on('mousedown', '#page-edit-form', function() {
       if (!form_edited) {
           form_edited = true;
       }
       return true;
    });
});
