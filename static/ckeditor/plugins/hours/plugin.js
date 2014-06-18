/**
 * Created by bwj on 04.12.2013.
 */

function editHoursContent(editor, childclass, parentclass, cmd, child_content) {
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

CKEDITOR.plugins.add('hours', {
    requires: 'widget',

    icons: 'hours',

    init: function(editor) {

        editor.addCommand('delHoursRow', {
            exec: function(editor) {
                editHoursContent(editor, 'row', 'hours', 'del', 'New row');
            }

        });
        editor.addCommand('addHoursRow', {
            exec: function(editor) {
                editHoursContent(editor, 'row', 'hours', 'add', 'New row');
            }
        });

        editor.on('selectionChange', function( e )
        {
            cmd = 'hours';
            start = e.data.selection.getStartElement();

            if (start.getName() == 'p' && start.getHtml() == '<br>') {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
            }
            else {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_DISABLED);
            }
        });

        editor.widgets.add('hours', {

            button: 'Add working hours',

            template:
                '<div class="hours">' +
                    '<div class="row">Days Hours</div>' +
                    '<div class="row">Days Hours</div>' +
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
                'div(*)',

            requiredContent: 'div(*)',

            //dialog: 'hours',

            upcast: function( element ) {
                return element.name == 'div' && element.hasClass('hours');
            }
        });

        if (editor.contextMenu) {
            editor.addMenuGroup('hoursGroup');
            editor.addMenuItem( 'addHoursItem', {
                label: 'Add row',
                command: 'addHoursRow',
                group: 'hoursGroup'
            });
            editor.addMenuItem( 'delHoursItem', {
                label: 'Delete row',
                command: 'delHoursRow',
                group: 'hoursGroup'
            });

            editor.contextMenu.addListener(function(element) {
                e = element.getAscendant('div', true)
                if (e && e.hasClass('row') && e.getParent().hasClass('hours'))
                {
                    child_count = e.getParent().getChildCount();

                    if (child_count == 1)
                    {
                        return {
                            addHoursItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else if (child_count == 5) {
                        return {
                            delHoursItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else {
                        return {
                            addHoursItem: CKEDITOR.TRISTATE_OFF,
                            delHoursItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                }
            });
        }
    }
});