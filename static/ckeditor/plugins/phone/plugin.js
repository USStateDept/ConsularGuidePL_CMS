/**
 * Created by bwj on 04.12.2013.
 */

function editPhoneContent(editor, childclass, parentclass, cmd, child_content, attrs) {
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

CKEDITOR.plugins.add('phone', {
    requires: 'widget',

    icons: 'phone',

    init: function(editor) {

        editor.addCommand('delPhoneRow', {
            exec: function(editor) {
                editPhoneContent(editor, 'row', 'phone', 'del', 'New row', ['data-number']);
            }

        });
        editor.addCommand('addPhoneRow', {
            exec: function(editor) {
                editPhoneContent(editor, 'row', 'phone', 'add', 'New row', ['data-number']);
            }
        });

        editor.on('selectionChange', function( e )
        {
            cmd = 'phone';
            start = e.data.selection.getStartElement();

            if (start.getName() == 'p' && start.getHtml() == '<br>') {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
            }
            else {
                var focused = editor.widgets.focused;
                if (focused && focused.name == 'phone')
                {
                    editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
                }
                else
                {
                    editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_DISABLED);
                }
            }
        });

        editor.widgets.add('phone', {

            button: 'Add phone number',

            template:
                '<div class="phone" data-number="+48123456789">' +
                    '<div class="row">Label for number</div>' +
                    '<div class="row">+48 (12) 345 67 89</div>' +
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
                'div(*)[data-number]',

            requiredContent: 'div(*)[data-number]',

            dialog: 'phone',

            upcast: function( element ) {
                return element.name == 'div' && element.hasClass('phone');
            }
        });

        CKEDITOR.dialog.add('phone', this.path + 'dialogs/phone.js');

        if (editor.contextMenu) {
            editor.addMenuGroup('phoneGroup');
            editor.addMenuItem( 'editPhone', {
                label: 'Edit phone number',
                command: 'phone',
                group: 'phoneGroup'
            });
            editor.addMenuItem( 'addPhoneItem', {
                label: 'Add row',
                command: 'addPhoneRow',
                group: 'phoneGroup'
            });
            editor.addMenuItem( 'delPhoneItem', {
                label: 'Delete row',
                command: 'delPhoneRow',
                group: 'phoneGroup'
            });

            editor.contextMenu.addListener(function(element) {
                var focused = editor.widgets.focused;
                if (focused && focused.name == 'phone')
                {
                    return {
                            editPhone: CKEDITOR.TRISTATE_OFF
                    }
                }

                var e = element.getAscendant('div', true)
                if (e && e.hasClass('row') && e.getParent().hasClass('phone'))
                {
                    child_count = e.getParent().getChildCount();

                    if (child_count == 1)
                    {
                        return {
                            addPhoneItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else if (child_count == 5) {
                        return {
                            delPhoneItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else {
                        return {
                            addPhoneItem: CKEDITOR.TRISTATE_OFF,
                            delPhoneItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                }
            });
        }
    }
});