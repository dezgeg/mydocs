# -*- coding: utf-8 -*-
from lettuce import step
from mydocs.edit.features.common import login_as, goto_url, assert_at_url
from mydocs.edit.models import Document

@step(u'(?:When|And) I (?:am at|go to) the index page')
def and_i_am_at_the_index_page(step):
    goto_url('/')

@step(u'(?:Then|And) I should be at the index page')
def then_i_should_be_at_the_index_page(step):
    assert_at_url('/')

@step(u'Then the document "([^"]*)" should contain "([^"]*)"')
def then_the_document_group1_should_contain_group2(step, doc_name, content):
    Document.objects.get(name=doc_name, content__contains=content)
