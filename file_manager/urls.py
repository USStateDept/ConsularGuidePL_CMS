__author__ = 'bwj'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'file_manager.views.manage_files', name="files-home"),
                       url(r'^add_file/$', 'file_manager.views.add_file', name="add-file"),
                       url(r'^edit_file/(?P<file_id>\d+)/$', 'file_manager.views.edit_file', name="edit-file"),
                       url(r'^get_en_file/(?P<file_id>\d+)/$', 'file_manager.views.get_en_file', name="get-en-file"),
                       url(r'^get_pl_file/(?P<file_id>\d+)/$', 'file_manager.views.get_pl_file', name="get-pl-file"),
                       url(r'^delete_file/$', 'file_manager.views.delete_file', name="delete-file"),
                       )