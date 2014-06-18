# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014
# created at: 03.01.2014 11:02

from django.conf.urls import patterns, url
from banner.views import BannerUpdateView, BannerDisableView

urlpatterns = patterns('',
						url(r'^$', BannerUpdateView.as_view(), name='banner-update'),
						url(r'^disable/$', BannerDisableView.as_view(), name='banner-disable'),
)
