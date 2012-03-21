# encoding: UTF-8
from mydocs.edit.models import Document
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms import ModelForm, ValidationError

class DocumentForm(ModelForm):
	class Meta:
		model = Document

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
