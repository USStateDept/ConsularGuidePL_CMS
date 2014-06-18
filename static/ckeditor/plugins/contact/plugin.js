/**
 * Created by bwj on 04.12.2013.
 */

CKEDITOR.plugins.add('contact', {
    requires: 'widget',

    icons: 'contact',

    init: function(editor) {

        editor.addCommand('addContact', {
            exec: function(editor) {
                editor.insertHtml('<div class="contact">' +
                    '<div class="place">' +
                        '<div class="name">Address</div>' +
                        '<div class="row">Fikcyjna 20</div>' +
                        '<div class="row">Warszawa</div>' +
                    '</div>' +
                    '<div class="hours">' +
                        '<div class="row">Pn-Pt 8-18</div>' +
                        '<div class="row">So-Nd ---</div>' +
                    '</div>' +
                    '<div class="phone" number="+48YYXXXYYZZ">' +
                        '<div class="row">Label for number</div>' +
                        '<div class="row">+48 (YY) XXX YY ZZ</div>' +
                    '</div>' +
                    '</div>'
                );
            },
            allowedContent: 'div(*);',

            requiredContent: 'div(*)[*];'
        });

        editor.ui.addButton('Contact', {
            label: 'Insert Contact Info',
            command: 'addContact',
            icon: this.path + 'icons/contact.png'
        });
    }
});