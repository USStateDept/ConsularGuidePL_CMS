# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014
# created at: 07.01.2014 16:31

from __future__ import unicode_literals, absolute_import
from celery import shared_task
from apnsclient import Session, APNs, Message
from django.conf import settings
from push_notifications.models import APNSDevice, GCMDevice
from push_notifications.gcm import gcm_send_bulk_message
from push_notification.models import NOTIFICATION_TYPE_ALERT, NOTIFICATION_TYPE_UPDATE, NOTIFICATION_TYPE_BASIC


@shared_task()
def push_to_all_devices(title_en, title_pl, message_en, message_pl, notification_type=NOTIFICATION_TYPE_BASIC):
	push_to_android_devices(title_en, title_pl, message_en, message_pl, notification_type)
	push_to_ios_devices(title_en, title_pl, notification_type)


@shared_task()
def push_to_android_devices(title_en, title_pl, message_en, message_pl, notification_type=NOTIFICATION_TYPE_BASIC):
	registration_ids = list(GCMDevice.objects.filter(active=True).values_list("registration_id", flat=True))
	collapse_key = ''
	if notification_type is NOTIFICATION_TYPE_BASIC:
		collapse_key = 'basic'
	elif notification_type is NOTIFICATION_TYPE_ALERT:
		collapse_key = 'alert'
	elif notification_type is NOTIFICATION_TYPE_UPDATE:
		collapse_key = 'update'
	data = gcm_send_bulk_message(
		registration_ids=registration_ids,
		data={
			'title_en': title_en,
			'title_pl': title_pl,
			'message_en': message_en,
			'message_pl': message_pl,
			'type': notification_type
		},
		collapse_key=collapse_key
	)
	GCMDevice.deactivate_unused(registration_ids, data)


@shared_task()
def push_to_ios_devices(title_en, title_pl, notification_type=NOTIFICATION_TYPE_BASIC, devices=None):
	if notification_type is NOTIFICATION_TYPE_BASIC:
		pass
	elif notification_type is NOTIFICATION_TYPE_ALERT:
		pass
	elif notification_type is NOTIFICATION_TYPE_UPDATE:
		pass
	data = {
		'loc-key': 'ENPL',
		'loc-args': [
			title_en,
			title_pl,
		],
	}
	extra = {
		'type': notification_type
	}
	push_to_ios_devices_raw(devices, alert=data, sound='default', **extra)

@shared_task()
def push_to_ios_devices_raw(devices=None, **kwargs):
	conn = Session.new_connection(settings.IOS_PUSH_SERVER, cert_file=settings.IOS_CERT)
	srv = APNs(conn)
	if devices is None:
		devices = APNSDevice.objects.filter(active=True).values_list("registration_id", flat=True)
	message = Message(devices, **kwargs)
	res = srv.send(message)
	if res.needs_retry():
		push_to_ios_devices_raw.delay(devices=res.retry().tokens, **kwargs)


@shared_task()
def get_ios_device_feedback():
	conn = Session.new_connection(settings.IOS_FEEDBACK_SERVER, cert_file=settings.IOS_CERT)
	srv = APNs(conn, tail_timeout=10)
	for token, since in srv.feedback():
		print token
		try:
			obj = APNSDevice.objects.get(registration_id=token)
			obj.active = False
			obj.save()
		except APNSDevice.DoesNotExist:
			pass
