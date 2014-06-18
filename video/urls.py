# coding=utf-8
__author__ = 'Artur Bacmaga'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'video.views.video_list', name='video-list'),
                       url(r'^add/$', 'video.views.video_add', name='video-add'),
                       url(r'^convert/(?P<video_id>\d+)/$', 'video.views.video_convert', name='video-convert'),
                       url(r'^convert_all/(?P<video_id>\d+)/$', 'video.views.video_convert_all', name='video-convert-all'),
                       url(r'^edit/(?P<video_id>\d+)/$', 'video.views.video_edit', name='video-edit'),
                       url(r'^preview/(?P<video_id>\d+)/$', 'video.views.video_preview', name='video-preview'),
                       url(r'^delete/$', 'video.views.video_delete', name='video-delete'),

)
