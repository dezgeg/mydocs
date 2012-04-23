# encoding: UTF-8
from mydocs.edit.models import Document, UserPermission
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import ModelForm, ValidationError
from django.forms.models import modelformset_factory

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        exclude = ('permissions',)

def index(request):
	docs = Document.objects.all()
	return render(request, 'index.html', { 'docs': docs })

def add(request):
	if request.POST:
		doc = DocumentForm(request.POST)
		doc.save()
		return HttpResponseRedirect('/')
	else:
		return render(request, 'edit.html', { 'document_form': DocumentForm() })

def edit(request, id):
	document = get_object_or_404(Document, pk=id)
	if request.POST:
		new_doc = DocumentForm(request.POST, instance= document)
		new_doc.save()
		return HttpResponseRedirect('/')
	else:
		return render(request, 'edit.html', { 'id': id, 'document_form': DocumentForm(instance= document) })

def delete(request, id):
	document = get_object_or_404(Document, pk=id)
	document.delete()
	return HttpResponseRedirect('/')

PermissionFormset = modelformset_factory(UserPermission, extra=3, can_delete=True)

def change_permissions(request, id):
    document = get_object_or_404(Document, pk=id)
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
