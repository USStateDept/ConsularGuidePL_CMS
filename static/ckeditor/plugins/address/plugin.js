/**
 * Created by bwj on 04.12.2013.
 */

function editAddressContent(editor, childclass, parentclass, cmd, child_content) {
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

        new_html = '<div class="' + parentclass + '">';

        if (name) {
            new_html = new_html + '<div class="name">' + name + '</div>';
        }
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

CKEDITOR.plugins.add('address', {
    requires: 'widget',

    icons: 'address',

    init: function(editor) {

        editor.addCommand('delAddressRow', {
            exec: function(editor) {
                editAddressContent(editor, 'row', 'place', 'del', 'New row');
            }

        });
        editor.addCommand('addAddressRow', {
            exec: function(editor) {
                editAddressContent(editor, 'row', 'place', 'add', 'New row');
            }
        });
        editor.on('selectionChange', function( e )
        {
            cmd = 'address';
            start = e.data.selection.getStartElement();

            if (start.getName() == 'p' && start.getHtml() == '<br>') {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
            }
            else {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_DISABLED);
            }
        });

        editor.widgets.add('address', {

            button: 'Add address',

            template:
                '<div class="place">' +
                    '<div class="name">Address</div>' +
                    '<div class="row">Street</div>' +
                    '<div class="row">City</div>' +
                '</div>',

            editables: {
                name: {
                    selector: '.name',
                    allowedContent: '#'
                },
                row1: {
                    selector: '.row:nth-child(2)',
                    allowedContent: 'br strong em'
                },
                row2: {
                    selector: '.row:nth-child(3)',
                    allowedContent: 'br strong em'
                },
                row3: {
                    selector: '.row:nth-child(4)',
                    allowedContent: 'br strong em'
                },
                row4: {
                    selector: '.row:nth-child(5)',
                    allowedContent: 'br strong em'
                },
                row5: {
                    selector: '.row:nth-child(6)',
                    allowedContent: 'br strong em'
                }
            },

            allowedContent:
                'div(*)',

            requiredContent: 'div(*)',

            upcast: function( element ) {
                return element.name == 'div' && element.hasClass('place');
            }
        });

        if (editor.contextMenu) {
            editor.addMenuGroup('addressGroup');
            editor.addMenuItem( 'addAddressItem', {
                label: 'Add row',
                command: 'addAddressRow',
                group: 'addressGroup'
            });
            editor.addMenuItem( 'delAddressItem', {
                label: 'Delete row',
                command: 'delAddressRow',
                group: 'addressGroup'
            });

            editor.contextMenu.addListener(function(element) {
                e = element.getAscendant('div', true)
                if (e && e.hasClass('row') && e.getParent().hasClass('place'))
                {
                    child_count = e.getParent().getChildCount();

                    if (child_count == 2)
                    {
                        return {
                            addAddressItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else if (child_count == 6) {
                        return {
                            delAddressItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else {
                        return {
                            addAddressItem: CKEDITOR.TRISTATE_OFF,
                            delAddressItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                }
            });
        }
    }
});