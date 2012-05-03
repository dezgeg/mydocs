from mydocs.edit.models import Document

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django import forms
from django.db import models
from djangotoolbox.fields import ListField
from django.forms import ModelForm, ValidationError
from django.contrib.auth.decorators import login_required

# A form field for ListField: https://gist.github.com/1200165
class StringListField(forms.CharField):
    def prepare_value(self, value):
        return ', '.join(value)

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]

ListField.formfield = lambda self, **kwargs: models.Field.formfield(self, StringListField, **kwargs)

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        exclude = ('permissions', 'owner')

def document_view(get_perm, post_perm=None):
	def generated(view_func):
		def ret(request, id, *args, **kwargs):
			#try:
				#id = args['id']
			#except:
				#raise Document.DoesNotExist()

			doc = get_object_or_404(Document, pk=id)
			required_perm = (post_perm or get_perm) if request.POST else get_perm
			actual_perm = doc.get_permission_for(request.user)
			if actual_perm < required_perm:
				raise PermissionDenied()

			return view_func(request, doc, *args, **kwargs)
		return ret
	return generated
