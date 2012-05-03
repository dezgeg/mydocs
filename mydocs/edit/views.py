# encoding: UTF-8
from mydocs.edit.models import Document, UserPermission, Permission
from mydocs.edit.view_helpers import DocumentForm, document_view

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import ModelForm, ValidationError
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required

def index(request):
	docs = Document.find_accessible_by(request.user)
	return render(request, 'index.html', { 'docs': docs })

@login_required
def add(request):
	if request.POST:
		doc = DocumentForm(request.POST)
		doc = doc.save(False)
		doc.owner = request.user.email
		doc.save()
		return HttpResponseRedirect('/')
	else:
		return render(request, 'edit.html', { 'document_form': DocumentForm() })

@document_view(Permission.Read, Permission.Modify)
def edit(request, document):
	if request.POST:
		new_doc = DocumentForm(request.POST, instance= document)
		new_doc.save()
		return HttpResponseRedirect('/')
	else:
		return render(request, 'edit.html', { 'id': id, 'document_form': DocumentForm(instance= document) })

@document_view(Permission.Owner)
def delete(request, document):
	document.delete()
	return HttpResponseRedirect('/')

PermissionFormset = modelformset_factory(UserPermission, extra=3, can_delete=True)

@document_view(Permission.ChangePerms)
def change_permissions(request, document):
    if request.POST:
        perms = PermissionFormset(request.POST).save(commit=False)
        document.permissions = perms
        document.save()
        return HttpResponseRedirect('/permissions/' + document.id)
    else:
        # need this hack since django-nonrel's listfields are lists, not QuerySets
        perms = map(lambda p: { 'email': p.email, 'permission': p.permission }, document.permissions)
        forms = PermissionFormset(initial=perms)
        return render(request, 'permissions.html', { 'doc': document, 'forms': forms })
