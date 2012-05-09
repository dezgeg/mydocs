from mydocs.edit.models import Document, Permission

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django import forms
from django.db import models
from djangotoolbox.fields import ListField
from django.forms import ModelForm, ValidationError
from django.contrib.auth.decorators import login_required

class OwnerDocumentForm(ModelForm):
    # used for adding and modifying by owner
    # allows changes to all fields
    class Meta:
        model = Document
        exclude = ('permissions', 'owner')

class WritableDocumentForm(ModelForm):
    # writers can change content, but not the name
    def __init__(self, *args, **kwargs):
        super(WritableDocumentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = 'readonly'
    # the readonly attribute only affects the HTML widgets.
    # this will actually prevent them from being set from POST requests 
    def clean_title(self):
        return self.instance.title

    class Meta:
        model = Document
        exclude = ('permissions', 'owner')

class ReadOnlyDocumentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReadOnlyDocumentForm, self).__init__(*args, **kwargs)
        for f in ('name', 'content'):
            self.fields[f].widget.attrs['readonly'] = 'readonly'

    def clean_title(self):
        return self.instance.title
    def clean_content(self):
        return self.instance.content

    class Meta:
        model = Document
        exclude = ('permissions', 'owner')

def document_form_for_permission(perm):
    if perm >= Permission.Owner: return OwnerDocumentForm
    elif perm >= Permission.Modify: return WritableDocumentForm
    else: return ReadOnlyDocumentForm

# a decorator for view functions acting on existing documents
# checks that the logged-in user has the proper permissions to the document

# usage: in urls.py:
# url(r'^frobnicate/([a-f0-9]+)$', 'frobnicate_document'),
# in views.py:
# @document_view(Permission.Write)
# def frobnicate_document(request, doc):
#    doc.content = frobnicate(doc.content); doc.save()
def document_view(get_perm, post_perm=None):
    def generated(view_func):
        def ret(request, id, *args, **kwargs):
            doc = get_object_or_404(Document, pk=id)
            required_perm = (post_perm or get_perm) if request.POST else get_perm
            actual_perm = doc.get_permission_for(request.user)
            if actual_perm < required_perm:
                raise PermissionDenied()

            return view_func(request, doc, *args, **kwargs)
        return ret
    return generated
