# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014
# created at: 03.01.2014 09:57

from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from model_utils import Choices

BANNER_TYPE_EMERGENCY = "emergency"


class Banner(TimeStampedModel):
	BANNER_TYPES = Choices(
		(BANNER_TYPE_EMERGENCY, 'Emergency'),
		('sec_adv', 'Security Advisory'),
		('calendar', 'Calendar Update'),
		('media', 'New Media Release'),
		('general', 'General Update'),
	)

	title_pl = models.CharField('Title (PL)', max_length=settings.BANNER_TITLE_LENGTH, null=True, blank=True)
	title_en = models.CharField('Title (EN)', max_length=settings.BANNER_TITLE_LENGTH, null=True, blank=True)
	description_pl = models.TextField('Description (PL)', max_length=settings.BANNER_DESCRIPTION_LENGTH, null=True, blank=True)
	description_en = models.TextField('Description (EN)', max_length=settings.BANNER_DESCRIPTION_LENGTH, null=True, blank=True)
	type = models.CharField(max_length=16, choices=BANNER_TYPES)
	enabled = models.BooleanField(default=True)

	def get_absolute_url(self):
		return reverse('banner-update')
