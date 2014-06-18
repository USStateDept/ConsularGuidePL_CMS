# -*- coding: utf-8 -*-
# Author Artur Baćmaga <artur.bacmaga@agitive.com>
# Author Witold Sosnowski <albi@jabster.pl>
# Author Szymon Nowicki <szymon.nowicki@agitive.com>
# (C) Agitive sp. z o. o. 2014

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import Group
from page.models import Page


PASSWORD_REQUIREMENTS = _(
	'Password must be at least 8 characters long, it must contain a minimum of '
	'one lowercase character, one uppercase character, one digit and one non-alphanumeric character.'
)
PASSWORD_MIN_LENGTH = 8


class UserPermissionEditMixin(forms.ModelForm):
	groups = forms.ModelMultipleChoiceField(
		label=_("Permission groups"),
		widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
		help_text=_("Select what permissions the user should have."),
		queryset=Group.objects.all(),
		required=False
	)

	edited_pages = forms.ModelMultipleChoiceField(
		label=_("Edited Pages"),
		widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
		help_text=_("Select which pages this user can edit."),
		queryset=Page.objects.filter(is_permission_parent=True, active=True),
		required=False
	)

	def __init__(self, is_superuser, *args, **kwargs):
		self.is_superuser = is_superuser
		super(UserPermissionEditMixin, self).__init__(*args, **kwargs)
		if not self.is_superuser:
			self.fields['groups'].queryset = Group.objects.exclude(pk=1)
		if 'instance' in kwargs:
			self.initial['edited_pages'] = kwargs['instance'].edited_pages.values_list('pk', flat=True)

	def save(self, commit=True):
		obj = super(UserPermissionEditMixin, self).save(False)
		obj.is_superuser = self.cleaned_data['groups'].filter(pk=1).count() > 0
		if commit:
			obj.save()
			self.save_m2m()
			obj.groups = self.cleaned_data['groups']
			obj.edited_pages = self.cleaned_data['edited_pages']
		return obj


class CustomUserChangeForm(UserPermissionEditMixin, forms.ModelForm):
	username = forms.RegexField(
		label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
		help_text=_("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
		error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
		widget=TextInput(attrs={'class': 'form-control'})
	)

	def __init__(self, *args, **kwargs):
		super(CustomUserChangeForm, self).__init__(*args, **kwargs)

		self.fields['email'].required = True

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'edited_pages']
		widgets = {
			'email': TextInput(attrs={'class': 'form-control'}),
			'first_name': TextInput(attrs={'class': 'form-control'}),
			'last_name': TextInput(attrs={'class': 'form-control'}),
		}


class CustomCreateUserForm(UserPermissionEditMixin, UserCreationForm):
	username = forms.RegexField(
		label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
		help_text = _("Required. 30 characters or fewer. Letters, digits and "
					  "@/./+/-/_ only."),
		error_messages = {
			'invalid': _("This value may contain only letters, numbers and "
						 "@/./+/-/_ characters.")},
		widget=TextInput(attrs={'class' : 'form-control'})
		)

	password1 = forms.CharField(
		label=_("Password"),
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		help_text=PASSWORD_REQUIREMENTS
	)
	password2 = forms.CharField(
		label=_("Password confirmation"),
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		help_text=_("Enter the same password as above, for verification.")
	)

	def __init__(self, *args, **kwargs):
		super(CustomCreateUserForm, self).__init__(*args, **kwargs)

		self.fields['email'].required = True

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'groups', 'edited_pages']
		widgets = {
			'email': TextInput(attrs={'class': 'form-control'}),
			'first_name': TextInput(attrs={'class': 'form-control'}),
			'last_name': TextInput(attrs={'class': 'form-control'}),
			'password1': PasswordInput(attrs={'class': 'form-control'}),
			'password2': PasswordInput(attrs={'class': 'form-control'}),
		}

	def clean_password1(self):
		return clean_password1(self, 'password1')


class CustomPasswordChangeForm(SetPasswordForm):
	new_password1 = forms.CharField(
		label=_("Password"),
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		help_text=PASSWORD_REQUIREMENTS
	)
	new_password2 = forms.CharField(
		label=_("Password confirmation"),
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		help_text=_("Enter the same password as above, for verification.")
	)

	def clean_new_password1(self):
		return clean_password1(self, 'new_password1')


def clean_password1(form, field):
	password1 = form.cleaned_data.get(field)

	if len(password1) < PASSWORD_MIN_LENGTH:
		raise forms.ValidationError(PASSWORD_REQUIREMENTS)

	if not any(ch.islower() for ch in password1):
		raise forms.ValidationError(PASSWORD_REQUIREMENTS)

	if not any(ch.isupper() for ch in password1):
		raise forms.ValidationError(PASSWORD_REQUIREMENTS)

	if not any(ch.isdigit() for ch in password1):
		raise forms.ValidationError(PASSWORD_REQUIREMENTS)

	if password1.isalnum():
		raise forms.ValidationError(PASSWORD_REQUIREMENTS)

	return password1
