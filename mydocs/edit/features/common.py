# -*- coding: utf-8 -*-
from django.test.client import Client
from django.core.management import call_command
from lettuce.django import django_url
from lettuce import *

from selenium import webdriver
import lettuce_webdriver.webdriver

from mydocs.edit.models import Document
from django.contrib.auth.models import User
from nose.tools import ok_

@before.all
def set_browser():
    world.browser = webdriver.Firefox()

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
@step(u'And I have the document "([^"]*)"')
def and_i_have_a_document_group1(step, name):
    Document.objects.create(name=name, content="ASD", owner="UserA@test.com")

@step(u'Then I should see "([^"]*)" in "([^"]*)"')
def then_i_should_see_group1_in_group2(step, value, name):
    return world.browser.find_element_by_xpath('//*[@name="%s"][contains(., "%s")]' % (name.lower(), value))
