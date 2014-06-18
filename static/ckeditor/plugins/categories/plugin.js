/**
 * Created by bwj on 04.12.2013.
 */

function editCategoriesContent(editor, cmd) {
    elt = editor.getSelection().getStartElement();
    item = elt.getAscendant('div', true);

    while (item && !item.hasClass('citem'))
    {
        item = item.getAscendant('div', false);
    }

    if (item && item.hasClass('citem')) {
        editor.fire('saveSnapshot');
        editor.fire('lockSnapshot', { dontUpdate: 1 });

        parent = item.getParent();
        children = parent.getChildren();

        if (cmd == 'add') {
            new_item = new CKEDITOR.dom.element('div');
            new_item = new CKEDITOR.dom.element('div');
            new_item.addClass('citem');
            new_item.appendHtml('<div class="cname">CAT</div>' +
                                '<div class="ctext">Category name</div>');
            new_item.insertAfter(item);
        }
        else if (cmd == 'del') {
            item.remove();
        }

        var pages = new Array();
        var names = new Array();
        var texts = new Array();

        len = children.count()
        for (i = 0; i < len; ++i) {
            child = children.getItem(i);

            var page = child.getAttribute('data-page');
            if (page)
            {
                pages.push(' data-page="' + page + '"');
            }
            else
            {
                pages.push('');
            }

            grandchildren = child.getChildren();
            grand_len = grandchildren.count()

            for (j = 0; j < grand_len; ++j)
            {
                grandchild = grandchildren.getItem(j);
                if (grandchild.hasClass('cname')) {
                    names.push(grandchild.getHtml());
                }
                if (grandchild.hasClass('ctext')) {
                    texts.push(grandchild.getHtml());
                }
            }
        }

        new_html = '<div class="categories">';

        for (i = 0; i < len; ++i) {
            new_html = new_html + '<div class="citem"' + pages[i] + '>' +
                '<div class="cname">' + names[i] + '</div>' +
                '<div class="ctext">' + texts[i] + '</div>' +
                '</div>';
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

CKEDITOR.plugins.add('categories', {
    requires: 'widget',

    icons: 'categories',

    init: function(editor) {

        editor.addCommand('delCategoriesRow', {
            exec: function(editor) {
                editCategoriesContent(editor, 'del');
            }

        });
        editor.addCommand('addCategoriesRow', {
            exec: function(editor) {
                editCategoriesContent(editor, 'add');
            }
        });

        CKEDITOR.dialog.add('categoriesDialog', this.path + 'dialogs/categories.js');

        editor.addCommand('editCategoriesRow', new CKEDITOR.dialogCommand('categoriesDialog'));

        editor.on('selectionChange', function( e )
        {
            cmd = 'categories';
            start = e.data.selection.getStartElement();

            if (start.getName() == 'p' && start.getHtml() == '<br>') {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_OFF);
            }
            else {
                editor.getCommand(cmd).setState(CKEDITOR.TRISTATE_DISABLED);
            }
        });

        editor.widgets.add('categories', {

            button: 'Add categories list',

            template:
                '<div class="categories">' +
                    '<div class="citem">' +
                        '<div class="cname">CAT</div>' +
                        '<div class="ctext">Category name</div>' +
                    '</div>' +
                    '<div class="citem">' +
                        '<div class="cname">CAT</div>' +
                        '<div class="ctext">Category name</div>' +
                    '</div>' +
                    '<div class="citem">' +
                        '<div class="cname">CAT</div>' +
                        '<div class="ctext">Category name</div>' +
                    '</div>' +
                    '<div class="citem">' +
                        '<div class="cname">CAT</div>' +
                        '<div class="ctext">Category name</div>' +
                    '</div>' +
                    '<div class="citem">' +
                        '<div class="cname">CAT</div>' +
                        '<div class="ctext">Category name</div>' +
                    '</div>' +
                '</div>',

            editables: {
                name1: {
                    selector: '.citem:nth-child(1)>.cname',
                    allowedContent: '#'
                },
                text1: {
                    selector: '.citem:nth-child(1)>.ctext',
                    allowedContent: '#'
                },
                name2: {
                    selector: '.citem:nth-child(2)>.cname',
                    allowedContent: '#'
                },
                text2: {
                    selector: '.citem:nth-child(2)>.ctext',
                    allowedContent: '#'
                },
                name3: {
                    selector: '.citem:nth-child(3)>.cname',
                    allowedContent: '#'
                },
                text3: {
                    selector: '.citem:nth-child(3)>.ctext',
                    allowedContent: '#'
                },
                name4: {
                    selector: '.citem:nth-child(4)>.cname',
                    allowedContent: '#'
                },
                text4: {
                    selector: '.citem:nth-child(4)>.ctext',
                    allowedContent: '#'
                },
                name5: {
                    selector: '.citem:nth-child(5)>.cname',
                    allowedContent: '#'
                },
                text5: {
                    selector: '.citem:nth-child(5)>.ctext',
                    allowedContent: '#'
                },
                name6: {
                    selector: '.citem:nth-child(6)>.cname',
                    allowedContent: '#'
                },
                text6: {
                    selector: '.citem:nth-child(6)>.ctext',
                    allowedContent: '#'
                },
                name7: {
                    selector: '.citem:nth-child(7)>.cname',
                    allowedContent: '#'
                },
                text7: {
                    selector: '.citem:nth-child(7)>.ctext',
                    allowedContent: '#'
                },
                name8: {
                    selector: '.citem:nth-child(8)>.cname',
                    allowedContent: '#'
                },
                text8: {
                    selector: '.citem:nth-child(8)>.ctext',
                    allowedContent: '#'
                },
                name9: {
                    selector: '.citem:nth-child(9)>.cname',
                    allowedContent: '#'
                },
                text9: {
                    selector: '.citem:nth-child(9)>.ctext',
                    allowedContent: '#'
                },
                name10: {
                    selector: '.citem:nth-child(10)>.cname',
                    allowedContent: '#'
                },
                text10: {
                    selector: '.citem:nth-child(10)>.ctext',
                    allowedContent: '#'
                },
                name11: {
                    selector: '.citem:nth-child(11)>.cname',
                    allowedContent: '#'
                },
                text11: {
                    selector: '.citem:nth-child(11)>.ctext',
                    allowedContent: '#'
                },
                name12: {
                    selector: '.citem:nth-child(12)>.cname',
                    allowedContent: '#'
                },
                text12: {
                    selector: '.citem:nth-child(12)>.ctext',
                    allowedContent: '#'
                },
                name13: {
                    selector: '.citem:nth-child(13)>.cname',
                    allowedContent: '#'
                },
                text13: {
                    selector: '.citem:nth-child(13)>.ctext',
                    allowedContent: '#'
                },
                name14: {
                    selector: '.citem:nth-child(14)>.cname',
                    allowedContent: '#'
                },
                text14: {
                    selector: '.citem:nth-child(14)>.ctext',
                    allowedContent: '#'
                },
                name15: {
                    selector: '.citem:nth-child(15)>.cname',
                    allowedContent: '#'
                },
                text15: {
                    selector: '.citem:nth-child(15)>.ctext',
                    allowedContent: '#'
                },
                name16: {
                    selector: '.citem:nth-child(16)>.cname',
                    allowedContent: '#'
                },
                text16: {
                    selector: '.citem:nth-child(16)>.ctext',
                    allowedContent: '#'
                },
                name17: {
                    selector: '.citem:nth-child(17)>.cname',
                    allowedContent: '#'
                },
                text17: {
                    selector: '.citem:nth-child(17)>.ctext',
                    allowedContent: '#'
                },
                name18: {
                    selector: '.citem:nth-child(18)>.cname',
                    allowedContent: '#'
                },
                text18: {
                    selector: '.citem:nth-child(18)>.ctext',
                    allowedContent: '#'
                },
                name19: {
                    selector: '.citem:nth-child(19)>.cname',
                    allowedContent: '#'
                },
                text19: {
                    selector: '.citem:nth-child(19)>.ctext',
                    allowedContent: '#'
                },
                name20: {
                    selector: '.citem:nth-child(20)>.cname',
                    allowedContent: '#'
                },
                text20: {
                    selector: '.citem:nth-child(20)>.ctext',
                    allowedContent: '#'
                },
                name21: {
                    selector: '.citem:nth-child(21)>.cname',
                    allowedContent: '#'
                },
                text21: {
                    selector: '.citem:nth-child(21)>.ctext',
                    allowedContent: '#'
                },
                name22: {
                    selector: '.citem:nth-child(22)>.cname',
                    allowedContent: '#'
                },
                text22: {
                    selector: '.citem:nth-child(22)>.ctext',
                    allowedContent: '#'
                },
                name23: {
                    selector: '.citem:nth-child(23)>.cname',
                    allowedContent: '#'
                },
                text23: {
                    selector: '.citem:nth-child(23)>.ctext',
                    allowedContent: '#'
                },
                name24: {
                    selector: '.citem:nth-child(24)>.cname',
                    allowedContent: '#'
                },
                text24: {
                    selector: '.citem:nth-child(24)>.ctext',
                    allowedContent: '#'
                },
                name25: {
                    selector: '.citem:nth-child(25)>.cname',
                    allowedContent: '#'
                },
                text25: {
                    selector: '.citem:nth-child(25)>.ctext',
                    allowedContent: '#'
                }
            },

            allowedContent:
                'div(*)[*]',

            requiredContent: 'div(*)[*]',

            upcast: function( element ) {
                return element.name == 'div' && element.hasClass('categories');
            }
        });

        if (editor.contextMenu) {
            editor.addMenuGroup('categoriesGroup');
            editor.addMenuItem( 'editCategoriesItem', {
                label: 'Edit action',
                command: 'editCategoriesRow',
                group: 'categoriesGroup'
            });
            editor.addMenuItem( 'addCategoriesItem', {
                label: 'Add row',
                command: 'addCategoriesRow',
                group: 'categoriesGroup'
            });
            editor.addMenuItem( 'delCategoriesItem', {
                label: 'Delete row',
                command: 'delCategoriesRow',
                group: 'categoriesGroup'
            });

            editor.contextMenu.addListener(function(element) {
                e = element.getAscendant('div', true)
                if (e && (e.hasClass('cname') || e.hasClass('ctext')))
                {
                    child_count = e.getParent().getParent().getChildCount();

                    if (child_count == 1)
                    {
                        return {
                            addCategoriesItem: CKEDITOR.TRISTATE_OFF,
                            editCategoriesItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else if (child_count == 25) {
                        return {
                            delCategoriesItem: CKEDITOR.TRISTATE_OFF,
                            editCategoriesItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                    else {
                        return {
                            addCategoriesItem: CKEDITOR.TRISTATE_OFF,
                            delCategoriesItem: CKEDITOR.TRISTATE_OFF,
                            editCategoriesItem: CKEDITOR.TRISTATE_OFF
                        };
                    }
                }
            });
        }
    }
});