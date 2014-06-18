/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For the complete reference:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

    config.extraPlugins = 'phone,hours,address,mail,btn,info,ajax,xml';
	config.filebrowserUploadUrl = "/upload";
	// The toolbar groups arrangement, optimized for two toolbar rows.
	config.toolbar = [
  	  	['Phone', 'Hours', 'Address', 'Contact', 'Mail', 'Btn', 'Info'],
  	  	'/',
  	  	['h1', 'h2', 'Bold', 'NumberedList', 'BulletedList', 'Image', 'Format']
	];

    config.contentsCss = [
        CKEDITOR.basePath + 'contents.css?3',
        '/static/css/contents_.css?3'
    ]

	// Remove some buttons, provided by the standard plugins, which we don't
	// need to have in the Standard(s) toolbar.
	config.removeButtons = 'Underline,Subscript,Superscript,Italic';

	// Se the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	// Make dialogs simpler.
	config.removeDialogTabs = 'image:advanced;link:advanced;image:Link';

    config.removePlugins = 'magicline,link';

	config.skin = 'embassy';

    config.entities = false;

    config.language = 'en';

    config.allowedContent = 'div(*)[*]; p h1 h2[id]; ol ul li[id]; img[!src, alt, id]; strong[id]; a(btn)[*]; table tr td;';

    config.height = 600;

};