CKEDITOR.dialog.add('phone', function(editor) {
    return {
        title: 'Edit phone number',
        minWidth: 250,
        minHeight: 100,
        contents: [
            {
                id: 'info',
                elements: [
                        {
                            id: 'number',
                            type: 'text',
                            label: 'Phone number (called when icon is tapped)',
                            width: '240px',
                            setup: function(widget) {
                                this.setValue(widget.element.getAttribute('data-number'));
                            },
                            commit: function(widget) {
                                val = this.getValue();
                                if (val)
                                    widget.element.setAttribute('data-number', val);
                                else
                                    widget.element.removeAttribute('data-number');
                            },
                            validate: CKEDITOR.dialog.validate.regex(/^\+?\d+$/, 'Not a valid phone number')
                        }
                ]
            }
        ]
    };
});