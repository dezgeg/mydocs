Feature: Make sure all the documents are valid.
    As a document person.
    I do not want to have invalid documents in the system.

    Scenario: Try to add a nameless document
        Given I am logged in as "UserA"
        And I click "Add a document"
        And I fill in "Name" with ""
        And I change the content to "This document has no name"
        And I press "Save"
        Then I should be at the "add" page
        And I should see "This field is required."
        And a document containing "This document has no name" should not exist

    Scenario: Try to remove a document's name
        Given I am logged in as "UserA"
        And I have the document "CHANGEME" containing "Foo"
        When I visit the URL for "CHANGEME"
        And I fill in "Name" with ""
        And I press "Save"
        Then I should see "This field is required"
        And a document named "CHANGEME" should exist

    Scenario: Try to a add a permission to an invalid e-mail
        Given I am logged in as "UserA"
        And I have the document "CHANGEME" containing "Foo"
        When I visit the change permissions URL for "CHANGEME"
        And I set "Email" for the permission #1 to "ASDDSDSASD"
        And I set "Permission" for the permission #1 to "Modify"
        And I set "Email" for the permission #2 to "AValid@Email.com"
        And I set "Permission" for the permission #2 to "Access"
        And I press "Save"
        Then I should see "Enter a valid e-mail address"
        And I should see "AValid@Email.com"

    Scenario: Try to a add a nonexisting user
        Given I am logged in as "UserA"
        And I have the document "CHANGEME" containing "Foo"
        When I visit the change permissions URL for "CHANGEME"
        And I set "Email" for the permission #1 to "NotValidEmail@Email.com"
        And I set "Permission" for the permission #1 to "Access"
        And I press "Save"
        Then I should see "This user does not exist"
        And I should see "NotValidEmail@Email.com"

    Scenario: Try to a add duplicate user permissions
        Given I am logged in as "UserA"
        And I have the document "CHANGEME" containing "Foo"
        When I visit the change permissions URL for "CHANGEME"

        And I set "Email" for the permission #1 to "foo@bar.com"
        And I set "Permission" for the permission #1 to "Modify"
        And I set "Email" for the permission #2 to "foo@bar.com"
        And I set "Permission" for the permission #2 to "Access"
        And I press "Save"

        Then I should see "There are multiple permissions specified for this user"
        And I should see "foo@bar.com"
