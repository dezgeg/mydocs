# encoding: UTF-8
from mydocs.edit.models import Document, UserPermission, Permission
from mydocs.edit.view_helpers import *

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import ModelForm, ValidationError
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

def index(request):
    others_docs = Document.find_accessible_by(request.user)
    my_docs = Document.find_own(request.user)
    return render(request, 'index.html', {
        'others_docs': others_docs,
        'my_docs': my_docs
    })

@login_required
def add(request):
    if request.POST:
        doc = OwnerDocumentForm(request.POST)
        if doc.is_valid():
            doc = doc.save(False)
            doc.owner = request.user.email
            doc.save()
            messages.success(request, "Document '%s' was created." % doc.name)
            return HttpResponseRedirect('/')
    else:
        doc = OwnerDocumentForm()
    return render(request, 'edit.html', { 'document_form': doc })

@document_view(Permission.Read, Permission.Modify)
def edit(request, document):
    form_class = document_form_for_permission(document.get_permission_for(request.user))
    if request.POST:
        doc = form_class(request.POST, instance= document)
        if doc.is_valid():
            doc = doc.save()
            messages.success(request, "Document '%s' was modified." % doc.name)
            return HttpResponseRedirect('/')
    else:
        doc = form_class(instance=document)
    return render(request, 'edit.html', { 'id': document.id, 'document_form': doc })

@document_view(Permission.Owner)
def delete(request, document):
    document.delete()
    messages.success(request, "Document '%s' was deleted." % document.name)
    return HttpResponseRedirect('/')

@document_view(Permission.ChangePerms)
def change_permissions(request, document):
    if request.POST:
        PermissionFormset = modelformset_factory(UserPermission, can_delete=True)
        forms = PermissionFormset(request.POST)
        anon_perms = AnonPermissionChangeForm(request.POST, instance=document)
        if forms.is_valid() and anon_perms.is_valid():
            anon_perms.save()
            perms = forms.save(commit=False)
            document.permissions = perms
            document.save()
            messages.success(request, "Permissions changed for '%s'." % document.name)
            return HttpResponseRedirect('/')
    else:
        # Real formset data should be populated via a queryset, but django-nonrel's ListFields
        # return ordinary lists. So we hack around this by turning the objects to dicts, which
        # can be entered as the initial form data, and then bump up the number of extra forms accordingly.
        perms = map(lambda p: p.__dict__, document.permissions)
        PermissionFormset = modelformset_factory(UserPermission, extra= 3 + len(perms), can_delete=True)
        forms = PermissionFormset(initial=perms, queryset=UserPermission.objects.none())
    return render(request, 'permissions.html', {
        'doc': document,
        'forms': forms,
        'anon_perms': AnonPermissionChangeForm(instance=document)
    })
