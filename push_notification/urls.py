# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.conf.urls import patterns, url
from push_notification.views import PushFormView

urlpatterns = patterns('',
                       url(r'^$', PushFormView.as_view(), name='push'),
                       url(r'^all/$', 'push_notification.views.push_all', name='push-all'),
)
