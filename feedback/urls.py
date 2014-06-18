__author__ = 'bwj'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'feedback.views.feedback_list', name="feedback-home"),
                       url(r'^deactivate/$', 'feedback.views.deactivate', name="feedback-deactivate"),
                       )