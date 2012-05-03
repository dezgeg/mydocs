# -*- coding: utf-8 -*-
from lettuce import *

from mydocs.edit.models import Document
from mydocs.edit.features.common import login_as, goto_url

@step(u'And I visit the URL for "([^"]*)"')
def and_i_visit_the_url_for_group1(step, doc_name):
	doc = Document.objects.get(name=doc_name)
	goto_url('/' + doc.id)
