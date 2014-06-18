# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.forms.models import ModelForm
from django.forms.widgets import Select, TextInput
from video.models import Video, LOCAL
from django import forms
import os

SEC_MAX_RANGE = 6
SEC_RANGE = [(i, i) for i in range(1, SEC_MAX_RANGE)]

VIDEO_EXTENSION_WHITELIST = (".mp4", ".mov", ".3gp", ".m2v", ".m4v", ".flv", ".avi", ".wmv", ".webm")


class VideoForm(ModelForm):
	class Meta:
		model = Video
		# exclude = ['date', 'conversion', 'poster', 'poster_time', 'video_android1', 'video_ios1', 'video_android2', 'video_ios2', 'video_android3', 'video_ios3', 'active', 'video_ios_variant', 'views']
		fields = ['video_type', 'title_en', 'title_pl', 'url', 'video_original']
		widgets = {
			'title_en': TextInput(attrs={'class' : 'form-control'}),
			'title_pl': TextInput(attrs={'class' : 'form-control'}),
			'video_type': Select(attrs={'class' : 'form-control'}),
			'url': TextInput(attrs={'class' : 'form-control'}),
		}

	def clean(self):
		cleaned_data = super(VideoForm, self).clean()
		video_type = cleaned_data.get('video_type')
		video = cleaned_data.get('video_original')
		url = cleaned_data.get('url')

		msg = 'This field is required.'

		if video_type == LOCAL:
			if video is None:
				self._errors['video_original'] = self.error_class([msg])
			else:
				correct_file = False
				for extension in VIDEO_EXTENSION_WHITELIST:
					if str(video).lower().endswith(extension):
						correct_file = True

				if not correct_file:
					self._errors['video_original'] = \
						self.error_class(["Invalid extension. Try " +
						                  str(VIDEO_EXTENSION_WHITELIST).replace('(', '').replace(')', '')])

		else:
			if url == '':
				self._errors['url'] = self.error_class([msg])

		return cleaned_data


class VideoPosterForm(forms.Form):
	second = forms.ChoiceField(choices=SEC_RANGE, widget=Select(attrs={'class':'form-control'}))

	def __init__(self, seconds=None, *args, **kwargs):
		super(VideoPosterForm, self).__init__(*args, **kwargs)
		if seconds:
			dynamic_range = [(i, i) for i in range(1, seconds + 1)]
			self.fields["second"] = forms.ChoiceField(choices=dynamic_range, widget=Select(attrs={'class':'form-control'}))
