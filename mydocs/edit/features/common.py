# -*- coding: utf-8 -*-
from django.test.client import Client
from django.core.management import call_command
from lettuce.django import django_url
from lettuce import *

from selenium import webdriver
import lettuce_webdriver.webdriver

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

# Stupid lettuce does not integrate with the django test framework
@before.each_scenario
def clean_db(scenario):
    call_command('flush', interactive=False)
    call_command('flush', interactive=False, database='documents')

def login_as(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username, username + "@test.com", "pass")

    # HACHHACKHACK - Steal the session cookie from the django client to log in
    from django.test.client import Client
    cl = Client()
    cl.login(username=username, password="pass")

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

