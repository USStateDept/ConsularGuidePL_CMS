# -*- coding: utf-8 -*-
# Author Witold Sosnowski <albi@jabster.pl>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit
from core.models import SyncableFileModel

# Image uploader for CKEditor


class Image(SyncableFileModel):
	image = ProcessedImageField(
		upload_to='images',
		format='JPEG',
		options={'quality': 60},
		processors=[ResizeToFit(width=2000, height=2000, upscale=False)]
	)

	syncable_file_fields = ['image']
