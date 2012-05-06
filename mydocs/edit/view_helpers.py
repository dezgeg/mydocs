from mydocs.edit.models import Document

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django import forms
from django.db import models
from djangotoolbox.fields import ListField
from django.forms import ModelForm, ValidationError
from django.contrib.auth.decorators import login_required

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
