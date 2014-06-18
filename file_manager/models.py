# -*- coding: utf-8 -*-
# Author Bartłomiej Wójcicki <bartlomiej.wojcicki@agitive.com>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.db import models
from django.utils import timezone
from django.conf import settings

from core.models import SyncableFileModel


class File(SyncableFileModel):
	name_en = models.CharField('Name (EN)', max_length=settings.FILE_TITLE_LENGTH)
	name_pl = models.CharField('Name (PL)', max_length=settings.FILE_TITLE_LENGTH)
	created = models.DateTimeField(default=timezone.now)
	modified = models.DateTimeField(default=timezone.now)
	version = models.IntegerField(default=0)
	size = models.IntegerField(default=0)
	file_en = models.FileField('File (EN)', upload_to='pdfs')
	file_pl = models.FileField('File (PL)', upload_to='pdfs')

	syncable_file_fields = ['file_pl', 'file_en']

	def save(self, *args, **kwargs):
		if self.pk is not None:
			orig = File.objects.get(pk=self.pk)
			changed = False
			if orig.file_en != self.file_en:
				orig.file_en.delete(save=False)
				changed = True
			if orig.file_pl != self.file_pl:
				orig.file_pl.delete(save=False)
				changed = True
			if changed:
				self.version += 1

		self.modified = timezone.now()
		super(File, self).save(*args, **kwargs)

	def to_dict(self):
		size = (self.file_en.size + self.file_pl.size) / 1e6
		size = int(size * 100 + 0.5) / 100.0
		data = dict(id=self.id, name_en=self.name_en, name_pl=self.name_pl, updated=self.modified.date().isoformat(),
		            version=self.version, size=size, url_en=self.file_en.url, url_pl=self.file_pl.url)

		return data
