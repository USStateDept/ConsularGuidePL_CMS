# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014
# created at: 10.01.2014 11:07

from __future__ import unicode_literals, absolute_import
import os
import sh
from celery import shared_task
from django.conf import settings

rsync = sh.Command('rsync').bake('-avz', '-e', 'ssh')
rsync_del = rsync.bake('--del')


def sync_path(source, destination):
	if hasattr(settings, 'MIRROR_DELETE') and settings.MIRROR_DELETE:
		rsync_del(source, destination)
	else:
		rsync(source, destination)


@shared_task()
def sync_media(media_path=''):
	sync_path(os.path.join(settings.MEDIA_ROOT, media_path),
				settings.MIRROR_SERVER_SSH_ADDRESS + ':' + os.path.join(settings.MIRROR_SERVER_MEDIA_ROOT, media_path))


@shared_task()
def sync_file_model(file_model):
	from core.models import SyncableFileModel
	file_model.sync_status = SyncableFileModel.SYNC_STATES.started
	file_model.save()
	try:
		for path in file_model.get_syncable_file_paths():
			sync_media(path)
	except:
		file_model.sync_status = SyncableFileModel.SYNC_STATES.failed
	file_model.sync_status = SyncableFileModel.SYNC_STATES.synched
	file_model.save()
