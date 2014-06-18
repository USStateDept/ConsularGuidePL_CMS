# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014
# created at: 03.01.2014 11:08

from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.edit import ModelFormMixin
from banner.models import Banner, BANNER_TYPE_EMERGENCY
from utils.decorators import class_permission_required
from push_notification.models import NOTIFICATION_TYPE_ALERT
from push_notification.tasks import push_to_all_devices
from forms import BannerForm, BannerDisableForm


@class_permission_required('banner.change_banner')
class BannerUpdateView(UpdateView):
	form_class = BannerForm
	template_name = 'banner/banner_update.html'
	model = Banner

	def get_object(self, queryset=None):
		try:
			banner = self.model.objects.get()
		except Banner.DoesNotExist:
			banner = Banner()
			banner.save()
		return banner

	def form_valid(self, form):
		self.object.enabled = True
		self.object = form.save()
		banner = self.object

		if banner.enabled and banner.type == BANNER_TYPE_EMERGENCY:
			push_to_all_devices.delay(
				title_en=banner.title_en,
				title_pl=banner.title_pl,
				message_en=banner.description_en,
				message_pl=banner.description_pl,
				notification_type=NOTIFICATION_TYPE_ALERT
			)

		return super(ModelFormMixin, self).form_valid(form)


@class_permission_required('banner.change_banner')
class BannerDisableView(UpdateView):
	form_class = BannerDisableForm
	model = Banner
	template_name = 'banner/banner_update.html'

	def get_object(self, queryset=None):
		try:
			banner = self.model.objects.get()
		except Banner.DoesNotExist:
			banner = Banner()
			banner.save()
		banner.enabled = False
		banner.title_en = None
		banner.title_pl = None
		banner.description_en = None
		banner.description_pl = None
		return banner
