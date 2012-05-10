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
