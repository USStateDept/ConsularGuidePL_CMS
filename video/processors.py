# -*- coding: utf-8 -*-
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014
# created at: 13.01.2014 11:34

from __future__ import unicode_literals
from pilkit.processors import Resize


class ResizeToEdge(object):
	"""
	Downscale the image to the so that ResizeCanvas will not crop the image

	"""
	def __init__(self, width, height, upscale=True):
		"""
		:param width: The target width, in pixels.
		:param height: The target height, in pixels.

		"""
		self.width, self.height = width, height
		self.upscale = upscale

	def process(self, img):
		original_width, original_height = img.size
		ratio = min(float(self.width) / original_width,
					float(self.height) / original_height)
		new_width, new_height = (int(round(original_width * ratio)),
					int(round(original_height * ratio)))
		img = Resize(new_width, new_height, upscale=self.upscale).process(img)
		return img
