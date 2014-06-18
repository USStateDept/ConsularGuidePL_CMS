# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from model_utils.choices import Choices

NOTIFICATION_TYPE_BASIC = 0
NOTIFICATION_TYPE_ALERT = 1
NOTIFICATION_TYPE_UPDATE = 2

TYPE_CHOICES = Choices(
	(NOTIFICATION_TYPE_BASIC, "Basic Notification"),
	(NOTIFICATION_TYPE_ALERT, "Alert Notification"),
    # (NOTIFICATION_TYPE_UPDATE, "Update Notification"),
)
