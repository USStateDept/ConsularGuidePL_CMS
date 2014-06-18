# coding=utf-8
__author__ = 'Artur Bacmaga'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'template_name': 'registration/logout.html'}, name="logout"),

                       url(r'^manage_users/$', 'core.views.manage_users', name="manage-users"),
                       url(r'^manage_users/adduser/$', 'core.views.adduser', name="add-user"),
                       url(r'^manage_users/edituser/(?P<user_id>\d+)/$', 'core.views.edit_user', name="edit-user"),
                       url(r'^manage_users/deleteuser/$', 'core.views.delete_user',
                           name="delete-user"),

                       url(r'^manage_users/edituser/(?P<user_id>\d+)/password/$', 'core.views.admin_change_password',
                           name="admin-change-password"),

                       url(r'^user_data/$', 'core.views.user_data', name="user-data"),
                       url(r'^user_password/$', 'core.views.user_password', name="user-password"),
)
