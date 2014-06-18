CKEDITOR.dialog.add('mail', function(editor) {
    return {
        title: 'Edit email address',
        minWidth: 250,
        minHeight: 100,
        contents: [
            {
                id: 'info',
                elements: [
                        {
                            id: 'mail',
                            type: 'text',
                            label: 'Email address',
                            width: '240px',
                            setup: function(widget) {
                                this.setValue(widget.element.getAttribute('data-address'));
                            },
                            commit: function(widget) {
                                val = this.getValue();
                                if (val)
                                    widget.element.setAttribute('data-address', val);
                                else
                                    widget.element.removeAttribute('data-address');
                            },
                            validate: CKEDITOR.dialog.validate.regex(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/, 'Not a valid email')
                        }
                ]
            }
        ]
    };
});