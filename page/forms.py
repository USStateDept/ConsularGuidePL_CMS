# -*- coding: utf-8 -*-
# Author Bartłomiej Wójcicki <bartlomiej.wojcicki@agitive.com>
# Author Witold Sosnowski <albi@jabster.pl>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django.core.exceptions import ValidationError

from django import forms
from django.forms import ModelForm
from django.forms.widgets import Select, TextInput, HiddenInput, Textarea, CheckboxInput
from models import *
from page.utils import clean_content, clean_faq


REQUIRED_TEXT_FIELDS = ("content_en", "content_pl")
OPTIONAL_TEXT_FIELDS = ("additional_en", "additional_pl")


def create_form(page_type, kwargs):
	if page_type == TEXT:
		return TextPageForm(**kwargs)
	if page_type == LIST:
		return ListPageForm(**kwargs)
	if page_type == STEPS:
		return StepsPageForm(**kwargs)
	if page_type == CONTACT:
		return ContactPageForm(**kwargs)
	if page_type == CATEGORY:
		return CategoryPageForm(**kwargs)
	if page_type == FAQ:
		return FAQForm(**kwargs)
	return PageForm(**kwargs)


def get_page_form(page, request):
	page_type = page.type()
	
	new_type = request.POST.get('page_type', None)
	if new_type is not None:
		page_type = new_type
	
	if request.method == 'POST':
		kwargs = {'user': request.user, 'data': request.POST, 'instance': page}
	else:
		kwargs = {'user': request.user, 'instance': page}

	return create_form(page_type, kwargs)


class CustomModelForm(ModelForm):
	TYPE = ""
	REQUIRED = ()
	check_optional = False

	def clean(self):
		cleaned_data = super(ModelForm, self).clean()
		page_type = cleaned_data.get("page_type")
		parent = cleaned_data.get("parent_page")

		if page_type == self.TYPE:
			for field in self.REQUIRED:
				self.check_required(cleaned_data, field)

				if field in REQUIRED_TEXT_FIELDS:
					if page_type == FAQ:
						self.check_faq(cleaned_data, field)
					else:
						self.check_content(cleaned_data, field)

			if self.check_optional:
				for field in OPTIONAL_TEXT_FIELDS:
					self.check_content(cleaned_data, field)

		page = self.instance
		if page.page_type in Page.PARENT_TYPES \
				and page_type not in Page.PARENT_TYPES \
				and page.child_page.filter(active=True).count() > 0:
			raise ValidationError('Selected type cannot have any child pages.')
		if page.page_type in Page.PARENT_TYPES \
				and page_type in (LIST, STEPS, CATEGORY) \
				and page.child_page.filter(active=True, page_type__in=(MENU,STEPS)).count() > 0:
			raise ValidationError('Selected type cannot have children of types: Steps, Menu.')

		# parent tests
		if not parent:
			if (not page.id) or (page.level != 0):
				self._errors['parent_page'] = self.error_class(["Please select page parent."])
		else:
			if not parent.user_can_add_children(self.user):
				raise ValidationError('You do not have permission to edit the subpages of the chosen parent page.')

			if page_type == MENU and parent.page_type != MENU:
				raise ValidationError('Menu has to be a child of other Menu.')

			if page_type == STEPS and parent.page_type != MENU:
				raise ValidationError('Steps have to be a child of a Menu.')

			if page_type in Page.SPECIAL_TYPES and parent.page_type != MENU:
				raise ValidationError('Special page has to be a child of a Menu.')

			if parent != page.parent_page and parent.is_descendant(page):
				raise ValidationError('Parent cannot be a descendant of this page.')

			if not self.errors:
				if parent != page.parent_page:
					page.place = parent.child_page.filter(active=True).count()

					if page.parent_page:
						i = 0
						for child in page.parent_page.child_page.filter(active=True).order_by('place'):
							if page.id != child.id:
								child.place = i
								child.save()
								i += 1

		return cleaned_data

	def check_required(self, cleaned_data, field):
		cleaned_field = cleaned_data.get(field, None)

		if cleaned_field is None or cleaned_field == '':
			self._errors[field] = self.error_class(["This field is required."])

	def check_content(self, cleaned_data, field):
		cleaned_field = cleaned_data.get(field, None)

		if cleaned_field is None or cleaned_field == '':
			return cleaned_data

		cleaned_data[field] = clean_content(cleaned_field)
		return cleaned_data

	def check_faq(self, cleaned_data, field):
		cleaned_field = cleaned_data.get(field)
		cleaned_data[field] = clean_faq(cleaned_field)
		return cleaned_data

	def __init__(self, user, *args, **kwargs):
		super(CustomModelForm, self).__init__(*args, **kwargs)
		self.user = user


class AddPageForm(CustomModelForm):
	class Meta:
		model = Page

		fields = ('parent_page', 'page_type', 'title_en', 'title_pl', 'is_permission_parent')
		widgets = {
			'page_type': Select(attrs={'class': 'form-control'}),
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
			'is_permission_parent': CheckboxInput(attrs={'class': 'form-control'})
		}

	def clean(self):
		cleaned_data = super(AddPageForm, self).clean()
		if (cleaned_data['is_permission_parent'] or cleaned_data['parent_page'] is None)\
			and not self.user.is_superuser:
			raise ValidationError('Only a superuser can add a permission parent.')
		return cleaned_data


class SimpleAddPageForm(CustomModelForm):
	class Meta:
		model = Page

		fields = ('parent_page', 'page_type', 'title_en', 'title_pl')
		widgets = {
			'page_type': Select(attrs={'class': 'form-control'}),
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'})
		}


class PageForm(CustomModelForm):
	class Meta:
		model = Page

		fields = ('parent_page', 'page_type', 'title_en', 'title_pl')
		widgets = {
			'page_type': Select(attrs={'class': 'form-control'}),
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
		}


class ModalPageForm(CustomModelForm):
	REQUIRED = ("content_en", "content_pl")
	TYPE = TEXT
	check_optional = False

	class Meta:
		model = Page

		fields = ('parent_page', 'title_en', 'title_pl', 'content_pl', 'content_en')
		widgets = {
			'title_pl': TextInput(attrs={'class' : 'form-control'}),
			'title_en': TextInput(attrs={'class' : 'form-control'}),
			'content_pl': Textarea(attrs={'class' : 'form-control'}),
			'content_en': Textarea(attrs={'class' : 'form-control'}),
			'parent_page': HiddenInput(),
		}


class TextPageForm(CustomModelForm):
	REQUIRED = ("content_en", "content_pl")
	TYPE = TEXT
	check_optional = True

	class Meta:
		model = Page

		exclude = ('version', 'created', 'modified', 'latitude', 'longitude', 'zoom', 'is_permission_parent', 'editors')
		widgets = {
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'page_type': Select(attrs={'class': 'form-control'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
			'content_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'content_en': Textarea(attrs={'class' : 'lang-en'}),
			'additional_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'additional_en': Textarea(attrs={'class' : 'lang-en'}),
		}


class ListPageForm(CustomModelForm):
	REQUIRED = ("content_en", "content_pl")
	TYPE = LIST
	check_optional = True

	class Meta:
		model = Page

		exclude = ('version', 'created', 'modified', 'latitude', 'longitude', 'zoom', 'is_permission_parent', 'editors')
		widgets = {
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'page_type': Select(attrs={'class': 'form-control'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
			'content_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'content_en': Textarea(attrs={'class' : 'lang-en'}),
			'additional_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'additional_en': Textarea(attrs={'class' : 'lang-en'}),
		}


class StepsPageForm(CustomModelForm):
	REQUIRED = ("content_en", "content_pl")
	TYPE = STEPS
	check_optional = True

	class Meta:
		model = Page

		exclude = ('version', 'created', 'modified', 'latitude', 'longitude', 'zoom', 'is_permission_parent', 'editors')
		widgets = {
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'page_type': Select(attrs={'class': 'form-control'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
			'content_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'content_en': Textarea(attrs={'class' : 'lang-en'}),
			'additional_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'additional_en': Textarea(attrs={'class' : 'lang-en'}),
		}


class ContactPageForm(CustomModelForm):
	REQUIRED = ("content_en", "content_pl", "zoom")
	TYPE = CONTACT
	check_optional = True

	longitude = forms.FloatField(min_value=-180.0, max_value=180.0, required=True, widget=TextInput(attrs={'class' : 'form-control col-md-2'}))
	latitude = forms.FloatField(min_value=-90.0, max_value=90.0, required=True, widget=TextInput(attrs={'class' : 'form-control col-md-2'}))

	class Meta:
		model = Page

		exclude = ('version', 'created', 'modified', 'is_permission_parent', 'editors')
		widgets = {
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
			'page_type': Select(attrs={'class': 'form-control'}),
			'content_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'content_en': Textarea(attrs={'class' : 'lang-en'}),
			'additional_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'additional_en': Textarea(attrs={'class' : 'lang-en'}),
			'zoom': Select(attrs={'class': 'form-control'}),
		}


class CategoryPageForm(CustomModelForm):
	REQUIRED = ("content_en", "content_pl")
	TYPE = CATEGORY
	check_optional = True

	class Meta:
		model = Page

		exclude = ('version', 'created', 'modified', 'latitude', 'longitude', 'zoom', 'is_permission_parent', 'editors')
		widgets = {
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'page_type': Select(attrs={'class': 'form-control'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
			'content_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'content_en': Textarea(attrs={'class' : 'lang-en'}),
			'additional_pl': Textarea(attrs={'class' : 'lang-pl'}),
			'additional_en': Textarea(attrs={'class' : 'lang-en'}),
		}


class FAQForm(CustomModelForm):
	REQUIRED = ("content_en", "content_pl")
	TYPE = FAQ
	class Meta:
		model = Page

		fields = ('parent_page', 'page_type', 'title_en', 'title_pl', 'content_en', 'content_pl')
		widgets = {
			'page_type': Select(attrs={'class': 'form-control'}),
			'title_pl': TextInput(attrs={'class' : 'form-control lang-pl'}),
			'title_en': TextInput(attrs={'class' : 'form-control lang-en'}),
			'parent_page': Select(attrs={'class': 'form-control', 'data-live-search': 'true'}),
			'content_en': HiddenInput(),
			'content_pl': HiddenInput()
		}