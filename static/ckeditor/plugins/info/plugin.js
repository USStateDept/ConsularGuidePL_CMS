/**
 * Created by bwj on 04.12.2013.
 */

CKEDITOR.plugins.add('info', {
    requires: 'widget',

    icons: 'info',

    init: function(editor) {
        editor.on('selectionChange', function( e )
        {
            cmd = 'info';
            start = e.data.selection.getStartElement();

            if (start.getName() == 'p' && start.getHtml() == '<br>') {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
            }
            else {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_DISABLED);
            }
        });
        editor.widgets.add('info', {

            button: 'Add info box',

            template:
                '<div class="info">' +
                    '<div class="shortinfo">Info box text</div>' +
                    '<div class="longinfo">Info box popup content</div>' +
                '</div>',

            editables: {
                short: {
                    selector: '.shortinfo',
                    allowedContent: 'br strong ol ul li p'
                },
                long: {
                    selector: '.longinfo',
                    allowedContent: 'br strong ol ul li p; a(btn)[*]'
                }
            },

            allowedContent:
                'div(*);',

            requiredContent: 'div(*)',

            upcast: function( element ) {
                return element.name == 'div' && element.hasClass('info');
            }
        });
    }
});