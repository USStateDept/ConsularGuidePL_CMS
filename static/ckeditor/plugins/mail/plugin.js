/**
 * Created by bwj on 04.12.2013.
 */

function editMailContent(editor, childclass, parentclass, cmd, child_content, attrs) {
    elt = editor.getSelection().getStartElement();
    item = elt.getAscendant('div', true);

    while (item && !item.hasClass(childclass))
    {
        item = item.getAscendant('div', false);
    }

    if (item && item.hasClass(childclass)) {
        editor.fire('saveSnapshot');
        editor.fire('lockSnapshot', { dontUpdate: 1 });

        parent = item.getParent();
        children = parent.getChildren();

        if (cmd == 'add') {
            new_item = new CKEDITOR.dom.element('div');
            new_item.addClass(childclass);
            new_item.appendHtml(child_content);
            new_item.insertAfter(item);
        }
        else if (cmd == 'del') {
            item.remove();
        }

        name = null;
        rows = new Array();

        len = children.count()
        for (i = 0; i < len; ++i) {
            child = children.getItem(i);

            if (child.hasClass('name')) {
                name = child.getHtml();
            }
            if (child.hasClass(childclass)) {
                rows.push(child.getHtml());
            }
        }

        attr_str = '';
        len = attrs.length;
        for (i = 0; i < len; ++i) {
            attr = attrs[i];

            if (parent.hasAttribute(attr)) {
                attr_str = attr_str + attr + '="' + parent.getAttribute(attr) + '" ';
            }
        }

        new_html = '<div class="' + parentclass + '" ' + attr_str + '>';

        for (i= 0; i < rows.length; ++i) {
            new_html = new_html + '<div class="' + childclass + '">' + rows[i] + '</div>';
        }

        new_html = new_html + '</div>';

        widget = editor.widgets.widgetHoldingFocusedEditable;
        editor.widgets.del(widget);
        editor.insertHtml(new_html);

        editor.fire('contentDomInvalidated', {editor:editor});

        editor.fire('unlockSnapshot');
        editor.fire('saveSnapshot');

    }
}

CKEDITOR.plugins.add('mail', {
    requires: 'widget',

    icons: 'mail',

    init: function(editor) {

        editor.addCommand('delMailRow', {
            exec: function(editor) {
                editMailContent(editor, 'row', 'mail', 'del', 'New row', ['data-address']);
            }

        });
        editor.addCommand('addMailRow', {
            exec: function(editor) {
                editMailContent(editor, 'row', 'mail', 'add', 'New row', ['data-address']);
            }
        });
        editor.on('selectionChange', function( e )
        {
            cmd = 'mail';
            start = e.data.selection.getStartElement();

            if (start.getName() == 'p' && start.getHtml() == '<br>') {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
            }
            else
            {
                var focused = editor.widgets.focused;
                if (focused && focused.name == 'mail')
                {
                    editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
                }
                else
                {
                    editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_DISABLED);
                }
            }
        });

        editor.widgets.add('mail', {

            button: 'Add email address',

            template:
                '<div class="mail" data-address="example@example.com">' +
                    '<div class="row">Label for email address</div>' +
                    '<div class="row">example@example.com</div>' +
                '</div>',

            editables: {
                row1: {
                    selector: '.row:nth-child(1)',
                    allowedContent: 'br strong em'
                },
                row2: {
                    selector: '.row:nth-child(2)',
                    allowedContent: 'br strong em'
                },
                row3: {
                    selector: '.row:nth-child(3)',
                    allowedContent: 'br strong em'
                },
                row4: {
                    selector: '.row:nth-child(4)',
                    allowedContent: 'br strong em'
                },
                row5: {
                    selector: '.row:nth-child(5)',
                    allowedContent: 'br strong em'
                }
            },

            allowedContent:
                'div(*)[data-address]',

            requiredContent: 'div(*)[data-address]',

            dialog: 'mail',

            upcast: function( element ) {
                return element.name == 'div' && element.hasClass('mail');
            }
        });

        CKEDITOR.dialog.add('mail', this.path + 'dialogs/mail.js');

        if (editor.contextMenu) {
            editor.addMenuGroup('mailGroup');
            editor.addMenuItem( 'editMail', {
                label: 'Edit email address',
                command: 'mail',
                group: 'mailGroup'
            });
            editor.addMenuItem( 'addMailItem', {
                label: 'Add row',
                command: 'addMailRow',
                group: 'mailGroup'
            });
            editor.addMenuItem( 'delMailItem', {
                label: 'Delete row',
                command: 'delMailRow',
                group: 'mailGroup'
            });

            editor.contextMenu.addListener(function(element) {
                var focused = editor.widgets.focused;
                if (focused && focused.name == 'mail')
                {
                    return {
                            editMail: CKEDITOR.TRISTATE_OFF
                    }
                }

                var e = element.getAscendant('div', true)
                if (e && e.hasClass('row') && e.getParent().hasClass('mail'))
                {
                    child_count = e.getParent().getChildCount();

                    if (child_count == 1)
                    {
                        return {
                            addMailItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else if (child_count == 5) {
                        return {
                            delMailItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else {
                        return {
                            addMailItem: CKEDITOR.TRISTATE_OFF,
                            delMailItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                }
            });
        }
    }
});