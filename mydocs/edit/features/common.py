# -*- coding: utf-8 -*-
import time
from django.test.client import Client
from django.core.management import call_command
from django.core.urlresolvers import reverse
from mydocs.edit.models import Document
from lettuce.django import django_url
from lettuce import *

from selenium import webdriver
import lettuce_webdriver.webdriver

from mydocs.edit.models import Document
from django.contrib.auth.models import User
from nose.tools import ok_

@before.all
def setup():
    world.browser = webdriver.Firefox()

@after.all
def teardown(results):
    world.browser.quit()

def goto_url(url):
    world.browser.get(django_url(url))

@before.each_scenario
def clean_db(scenario):
    call_command('flush', interactive=False)
    call_command('flush', interactive=False, database='documents')

def login_as(user):
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        user = User.objects.create_user(user, user + "@test.com", "pass")

    # HACHHACKHACK - Steal the session cookie from the django client to log in
    from django.test.client import Client
    cl = Client()
    cl.login(username=user, password="pass")

    world.browser.get(django_url('/')) # this seems to be required
    world.browser.add_cookie({
        'name': 'sessionid',
        'value': cl.cookies['sessionid'].value,
        'path': '/',
    })
    world.browser.get(django_url('/'))

def assert_at_url(url):
    current = world.browser.current_url
    expected = django_url(url)
    ok_(current == expected,
         "should be at URL '%s', got '%s'" % (expected, current))

@step(u'Given I am logged in as "([^"]*)"')
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

@step(u'(?:Then|And) I wait a while')
def busy_wait_for_crappy_js(step):
    time.sleep(2)
