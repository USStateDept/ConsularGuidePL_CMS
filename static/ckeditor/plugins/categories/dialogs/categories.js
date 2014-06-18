__global_element = 0;

CKEDITOR.dialog.add('categoriesDialog', function(editor) {
    return {
        title: 'Category action',
        minWidth: 400,
        minHeight: 200,
        contents: [
            {
                id: 'info',
                elements: [
                    {
                        id: 'page-select',
                        type: 'select',
                        label: 'Jump to page',
                        items: [[ '------', '' ]],
                        onLoad: function(element) {
                            this.setValue('');
                        },
                        setup: function(element) {
                            data = CKEDITOR.ajax.load('/cms/children_list/' + page_id + '/');
                            arr = JSON.parse(data);
                            this.clear();
                            this.add('------', '');
                            for (i = 0; i < arr.length; ++i) {
                                this.add(arr[i][0], arr[i][1]);
                            }

                            this.setValue(element.getAttribute('data-page'));
                        },
                        commit: function(element) {
                            val = this.getValue();
                            if (val != '')
                                element.setAttribute('data-page', val);
                            else
                                element.removeAttribute('data-page');
                        }
                    },
                    {
                        type: 'html',
                        html : '<p><a id="cke_page_new" href="/cms/add_page_modal/" onclick="CKEDITOR.dialog.getCurrent().hide()" class="btn btn-lg" data-toggle="modal" data-target="#add-page-modal"><img src="/static/img/add.png">Add new page</a></p>'
                    }
                ]
            }
        ],

        onShow: function() {
            var selection = editor.getSelection(),
            element = selection.getStartElement();
            while (element && !(element.hasClass('citem')))
            {
                element = element.getAscendant('div');
            }

            this.element = element;
            this.setupContent(this.element);
            document.getElementById("cke_page_new").setAttribute("href", "/cms/add_page_modal/" + page_id + '/');
            __global_element = element;
        },

        onOk: function() {
            var dialog = this,
            item = this.element;

            this.commitContent(item);
        }
   }
});