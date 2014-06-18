/**
 * Created by bwj on 04.12.2013.
 */

CKEDITOR.plugins.add('btn', {

    icons: 'btn',

    init: function(editor) {

        editor.addCommand('btn', new CKEDITOR.dialogCommand('btnDialog', {
            allowedContent: 'a(btn)[data-url,data-page]',
            requiredContent: 'a(btn)[data-url,data-page]'
        }));

        editor.on('selectionChange', function( e )
        {
            cmd = 'btn';
            start = e.data.selection.getStartElement();

            if (start.getName() == 'p' && start.getHtml() == '<br>') {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
            }
            else {
                el = e.data.selection.getStartElement().getAscendant('a', true);
                if (el && el.hasClass('btn')) {
                    editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
                }
                else {
                    editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_DISABLED);
                }
            }
        });

        editor.ui.addButton('Btn', {
            label: 'Add button',
            command: 'btn'
        });

        if (editor.contextMenu) {
            editor.addMenuGroup('btnGroup');
            editor.addMenuItem('btnItem', {
                label: 'Edit button',
                command: 'btn',
                group: 'btnGroup'
            });

            editor.contextMenu.addListener(function(element) {
                e = element.getAscendant('a', true);
                if (e && e.hasClass('btn')) {
                    return { btnItem: CKEDITOR.TRISTATE_OFF }
                }
            });

        }

        editor.on('doubleclick', function(evt) {
            var selection = evt.editor.getSelection();
            var elt = selection.getStartElement();
            if (elt)
            {
                elt = elt.getAscendant('a', true);
                if (elt && elt.hasClass('btn')) {
                    evt.data.dialog = 'btnDialog';
                }
            }
        });

        CKEDITOR.dialog.add('btnDialog', this.path + 'dialogs/btn.js');
    }
});