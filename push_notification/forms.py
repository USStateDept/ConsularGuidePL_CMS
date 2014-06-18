# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# Author Witold Sosnowski <albi@jabster.pl>
# (C) Agitive sp. z o. o. 2014
# created at: 08.01.2014 11:00

from __future__ import unicode_literals
from django import forms
from push_notification.tasks import push_to_all_devices
from push_notification.models import TYPE_CHOICES
from django.forms.widgets import TextInput


class NotificationForm(forms.Form):
	title_en = forms.CharField(label='Title (EN)', max_length=50, widget=TextInput(attrs={'class': 'form-control'}))
	title_pl = forms.CharField(label='Title (PL)', max_length=50, widget=TextInput(attrs={'class': 'form-control'}))
	message_en = forms.CharField(label='Message (EN)', widget=TextInput(attrs={'class': 'form-control'}))
	message_pl = forms.CharField(label='Message (PL)', widget=TextInput(attrs={'class': 'form-control'}))

	def send_notifications(self):
		push_to_all_devices.delay(
			title_en=self.cleaned_data['title_en'],
			title_pl=self.cleaned_data['title_pl'],
			message_en=self.cleaned_data['message_en'],
			message_pl=self.cleaned_data['message_pl'],
		)

