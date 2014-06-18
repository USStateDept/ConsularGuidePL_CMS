from django.forms import ModelForm
from models import *
from django.forms.widgets import TextInput

class FileForm(ModelForm):
	class Meta:
		model = File
		exclude = ('version', 'created', 'modified', 'size')
		widgets = {
			'name_en': TextInput(attrs={'class': 'form-control'}),
			'name_pl': TextInput(attrs={'class' : 'form-control'}),
		}


	def clean(self):
		cleaned_data = super(FileForm, self).clean()
		file_en = cleaned_data.get('file_en')
		file_pl = cleaned_data.get('file_pl')

		req_msg = 'This field is required.'
		ext_msg = 'Incorrect file extension. Only pdf files are supported.'

		if file_en is None:
			self._errors['file_en'] = self.error_class([req_msg])
		elif not str(file_en).lower().endswith('pdf'):
			self._errors['file_en'] = self.error_class([ext_msg])

		if file_pl is None:
			self._errors['file_pl'] = self.error_class([req_msg])
		elif not str(file_pl).lower().endswith('pdf'):
			self._errors['file_pl'] = self.error_class([ext_msg])

		return cleaned_data