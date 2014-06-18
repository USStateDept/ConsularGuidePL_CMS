# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from push_notification.models import NOTIFICATION_TYPE_UPDATE
from push_notification.tasks import push_to_all_devices
from django.views.generic import FormView
from push_notification.forms import NotificationForm
from utils.decorators import class_login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

@class_login_required
class PushFormView(FormView):
	form_class = NotificationForm
	template_name = 'push_notification/push_form.html'

	def form_valid(self, form):
		form.send_notifications()
		return render_to_response('push_notification/push_form.html', {'form': form, 'message': 'Push notification successfully sent.'}, context_instance=RequestContext(self.request))



@login_required
def push_all(request):
	push_to_all_devices.delay("Content updated", "Treść zaktualizowana", "", "", notification_type=NOTIFICATION_TYPE_UPDATE)
	return render_to_response('push_notification/push_form.html', {'form': NotificationForm(), 'message': 'Update notification successfully sent.'}, context_instance=RequestContext(request))
