# -*- coding: utf-8 -*-
from lettuce import *
from mydocs.edit.features.common import login_as, goto_url, assert_at_url
from mydocs.edit.models import Document, UserPermission, Permission

@step(u'And "([^"]*)" has the permission "([^"]*)" to "([^"]*)"')
def and_group1_has_the_permission_group2_to_group3(step, user, perm, doc_name):
    doc = Document.objects.get(name=doc_name)
    perm = UserPermission.objects.create(email=user + "@test.com", permission=Permission.__dict__[perm])
    doc.permissions += [perm]
    doc.save()
@step(u'And I should not be able to change "([^"]*)"')
def and_i_should_not_be_able_to_change_group1(step, field):
    return world.browser.find_element_by_xpath('//*[@name="%s"][@readonly]' % field.lower())
@step(u'Then the document "([^"]*)" should contain "([^"]*)"')
def then_the_document_group1_should_contain_group2(step, doc_name, content):
    Document.objects.get(name=doc_name, content=content)

@step('And I set "([^"]*)" for the permission #([0-9]+) to "([^"]*)"')
def set_permission_field(step, field, num, value):
    num = int(num) - 1
    if field == "Permission":
        world.browser.find_element_by_xpath(
            '//select[@name="form-%d-permission"]/option[text()="%s"]' % (num, value)
        ).click()
    else:
        field = world.browser.find_element_by_xpath('//input[@name="form-%d-%s"]' % (num, field.lower()))
        field.clear()
        field.send_keys(value)
