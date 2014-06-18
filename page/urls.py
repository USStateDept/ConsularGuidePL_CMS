__author__ = 'bwj'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'page.views.manage_pages', name="page-home"),
                       url(r'^content_tree/(?P<page_id>\d+)/$', 'page.views.content_tree', name="page-content-tree"),
                       url(r'^content_tree/$', 'page.views.content_tree', name="page-content-tree"),
                       url(r'^add_page/$', 'page.views.add_page', name="add-page"),
                       url(r'^add_page_modal/(?P<page_id>\d+)/$', 'page.views.add_page_modal', name="add-page-modal"),
                       url(r'^add_page/(?P<page_id>\d+)/$', 'page.views.add_child_page', name="add-child-page"),
                       url(r'^edit_page/(?P<page_id>\d+)/$', 'page.views.edit_page', name="edit-page"),
                       url(r'^edit_page_partial/(?P<page_id>\d+)/$', 'page.views.edit_page_partial', name="edit-page-partial"),
                       url(r'^delete_page/$', 'page.views.delete_page', name="delete-page"),
                       url(r'^page_list/$', 'page.views.page_list', name='page-list'),
                       url(r'^children_list/(?P<page_id>\d+)/$', 'page.views.children_list', name='children-list'),
                       url(r'^clean_text/$', 'page.views.clean_text', name='clean-text'),
                       )
