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
