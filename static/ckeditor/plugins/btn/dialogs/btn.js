
CKEDITOR.dialog.add('btnDialog', function(editor) {
    return {
        title: 'Button properties',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'info',
                elements: [
                    {
                        id: 'btn',
                        type: 'text',
                        label: 'Button text',
                        validate: CKEDITOR.dialog.validate.notEmpty("Button text cannot be empty"),
                        setup: function(element) {
                            this.setValue(element.getText());
                        },
                        commit: function(element) {
                            element.setText(this.getValue());
                        }
                    },
                    {
                        type: 'html',
                        html: '<style>.cke_disabled{display:none;}.cke_dialog_ui_hbox_first{float:left;}.cke_dialog_ui_hbox_last{float:left;}</style>'
                    },
                    {
                        id: 'radio',
                        type: 'radio',
                        label: 'Button type',
                        items: [['URL', 'url'], ['PAGE', 'page-select']],
                        onChange: function(e) {
                            to_enable = e.data.value;
                            to_disable = to_enable == 'url' ? 'page-select' : 'url';
                            this.getDialog().getContentElement('info', to_enable).enable();
                            this.getDialog().getContentElement('info', to_disable).disable();

                            if (to_disable == 'page-select')
                                this.getDialog().getContentElement('info', to_disable).setValue('');
                            else
                                this.getDialog().getContentElement('info', to_disable).setValue(null);
                        },
                        setup: function(element) {
                            if (element.getAttribute('data-url')) {
                                this.setValue('url');
                            }
                            else {
                                this.setValue('page-select');
                            }
                        }
                    },
                    {
                        id: 'url',
                        type: 'text',
                        label: 'Button url',
                        setup: function(element) {
                            this.setValue(element.getAttribute('data-url'));
                        },
                        commit: function(element) {
                            button_type = this.getDialog().getContentElement('info', 'radio').getValue();

                            val = this.getValue();
                            if (button_type == 'url')
                                element.setAttribute('data-url', val);
                            else
                                element.removeAttribute('data-url');
                        },
                        validate: function() {
                            button_type = this.getDialog().getContentElement('info', 'radio').getValue();

                            if (button_type != 'url')
                                return true;

                            url = this.getValue();
                            re = /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$/;
                            return re.test(url) ? true : 'Not a valid url';
                        }
                    },
                    {
                        id: 'page-select',
                        type: 'select',
                        label: 'Jump to page',
                        items: [[ '------', '' ]],
                        onLoad: function(element) {
                            data = CKEDITOR.ajax.load('/cms/page_list/');
                            arr = JSON.parse(data);

                            for (i = 0; i < arr.length; ++i) {
                                this.add(arr[i][0], arr[i][1]);
                            }

                            this.setValue('');
                        },
                        setup: function(element) {
                            this.setValue(element.getAttribute('data-page'));
                        },
                        commit: function(element) {
                            button_type = this.getDialog().getContentElement('info', 'radio').getValue();

                            val = this.getValue();
                            if (button_type == 'page-select')
                                element.setAttribute('data-page', val);
                            else
                                element.removeAttribute('data-page');
                        },
                        validate: function() {
                            button_type = this.getDialog().getContentElement('info', 'radio').getValue();

                            if (button_type != 'page-select')
                                return true;

                            return this.getValue() != '' ? true : 'Not a valid page';
                        }
                    }
                ]
            }
        ],

        onShow: function() {
            var selection = editor.getSelection(),
            element = selection.getStartElement();
            if (element)
                element = element.getAscendant('a', true);

            if (!element || !element.hasClass('btn') || element.data('cke-realelement')) {
                element = editor.document.createElement('a');
                element.addClass('btn');
                this.insertMode = true;
            }
            else
                this.insertMode = false;

            this.element = element;

            this.setupContent(this.element);
        },

        onOk: function() {
            var dialog = this,
                btn = this.element;

            this.commitContent(btn);

            if (this.insertMode) {
                editor.insertElement(btn);

                var next = btn.getNext();
                var fake_next = null;
                if (next != null && next.type == CKEDITOR.NODE_TEXT) {
                    //chrome fix - text node with &#8023; after button
                    fake_next = next;
                    next = next.getNext();
                }
                if (next != null && next.type == CKEDITOR.NODE_ELEMENT && next.getName() == "br") {
                    next.remove();

                    if (fake_next != null)
                        fake_next.remove();

                    var range = editor.createRange();
                    range.selectNodeContents(btn);
                    range.collapse();
                    editor.getSelection().selectRanges([range]);
                }
            }
        }
   }
});