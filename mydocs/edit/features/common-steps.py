# -*- coding: utf-8 -*-
import time
from lettuce import world, step
from django.core.urlresolvers import reverse
from mydocs.edit.features.common import login_as, goto_url, assert_at_url
from mydocs.edit.models import Document
from django.contrib.auth.models import User
from nose.tools import ok_

@step(u'Given there is a user "([^"]*)"')
def log_in(step, username):
    User.objects.create_user(username, username + "@test.com", "pass")

@step(u'(?:(?:Given|And) I am logged|When I log) in as "([^"]*)"')
def log_in(step, user):
    login_as(user)

@step(u'When I log in as "([^"]*)"')
def when_i_log_in_as_group1(step, user):
    login_as(user)

@step(u'When I log out')
def when_i_log_out(step):
    goto_url('/logout')

@step(u'And I have the document "([^"]*)" containing "([^"]*)"')
def and_i_have_a_document_group1(step, name, content):
    Document.objects.create(name=name, content=content, owner="UserA@test.com")

@step(u'Then I should see "([^"]*)" in "([^"]*)"')
def then_i_should_see_group1_in_group2(step, value, name):
    return world.browser.find_element_by_xpath('//*[@name="%s"][contains(., "%s")]' % (name.lower(), value))

@step(u'(?:And|When) I change the content to "([^"]*)"')
def set_ckeditor_text(step, content):
    world.browser.execute_script("CKEDITOR.instances['id_content'].setData('%s');" % content)

@step(u'(?:And|Then|When) I visit the URL for "([^"]*)"')
def and_i_visit_the_url_for_group1(step, doc_name):
    doc = Document.objects.get(name=doc_name)
    goto_url(reverse('edit', args=[doc.id]))

@step(u'(?:And|Then|When) I visit the change permissions URL for "([^"]*)"')
def and_i_visit_the_url_for_group1(step, doc_name):
    doc = Document.objects.get(name=doc_name)
    goto_url(reverse('change_permissions', args=[doc.id]))

@step(u'Then I should be at the "([^"]*)" page')
def then_i_should_be_at_the_group1_page(step, url):
    assert_at_url(reverse(url))

@step(u'And a document containing "([^"]*)" should not exist')
def and_a_document_containing_group1_should_not_exist(step, content):
    ok_(not Document.objects.filter(content__contains=content).exists())

@step(u'And a document named "([^"]*)" should exist')
def and_a_document_containing_group1_should_not_exist(step, name):
    ok_(Document.objects.filter(name=name).exists())

# There might be a better way...
@step(u'(?:Then|And) I wait a while')
def busy_wait_for_crappy_js(step):
    time.sleep(2)
