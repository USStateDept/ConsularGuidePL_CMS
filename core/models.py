# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models import signals
from model_utils import Choices
from core.tasks import sync_media


class SyncableFileModel(models.Model):
	SYNC_STATES = Choices(
		'waiting',
		'started',
		'synched',
		'failed'
	)
	sync_status = models.CharField(choices=SYNC_STATES, default=SYNC_STATES.waiting, editable=False, max_length=16)

	class Meta:
		abstract = True

	syncable_file_fields = []

	def get_syncable_file_fields(self):
		return self.syncable_file_fields

	def get_syncable_file_paths(self):
		paths = []
		fields = self.get_syncable_file_fields()
		for field_name in fields:
			field_file = getattr(self, field_name, None)
			if field_file:
				paths.append(field_file.name)
		return paths

	def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
		super(SyncableFileModel, self).save(force_insert, force_update, using, update_fields)
		if settings.IS_MASTER:
			sync_media.delay()


class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	force_password_change = models.BooleanField(default=True)


def create_user_profile_signal(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

signals.post_save.connect(create_user_profile_signal, sender=User, dispatch_uid='core.models')
