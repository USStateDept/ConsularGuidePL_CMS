# -*- coding: utf-8 -*-
# Author Witold Sosnowski <albi@jabster.pl>
# (C) Agitive sp. z o. o. 2014

from django import forms
from django.forms.widgets import Select, TextInput, Textarea, HiddenInput
from models import *


class BannerForm(forms.ModelForm):
	title_en = forms.CharField(required=True,
	                           max_length=settings.BANNER_TITLE_LEN,
	                           widget=TextInput(attrs={'class': 'form-control'}))
	title_pl = forms.CharField(required=True,
	                           max_length=settings.BANNER_TITLE_LEN,
	                           widget=TextInput(attrs={'class': 'form-control'}))
	description_en = forms.CharField(required=True,
	                                 max_length=settings.BANNER_TEXT_LEN,
	                                 widget=Textarea(attrs={'class': 'form-control', 'maxlength': settings.BANNER_TEXT_LEN}))
	description_pl = forms.CharField(required=True,
	                                 max_length=settings.BANNER_TEXT_LEN,
	                                 widget=Textarea(attrs={'class': 'form-control', 'maxlength': settings.BANNER_TEXT_LEN}))

	class Meta:
		model = Banner
		fields = ('type', 'title_en', 'title_pl', 'description_en', 'description_pl')
		widgets = {
			'type': Select(attrs={'class': 'form-control'}),
		}


class BannerDisableForm(forms.ModelForm):
	class Meta:
		model = Banner
		fields = ('title_en', 'title_pl', 'description_en', 'description_pl', 'enabled')
