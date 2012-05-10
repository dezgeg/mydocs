Feature: Add an delete documents
    As a document person.
    I want to have documents in the system.

    Scenario: Add a document
        Given I am logged in as "UserA"
        And I click "Add a document"
        And I fill in "Name" with "Test document"
        And I change the content to "Test stuff"
        And I press "Save"
        Then I should see "Test stuff" in "Content"
        And I should see "Document 'Test document' was created"
        When I go to the index page
        Then I should see "Test document"

    Scenario: Delete a document
        Given I am logged in as "UserA"
        And I have the document "DONOTWANT" containing "Dont care"
        And I am at the index page
        When I click "[delete]"
        Then I should be at the index page
        And I wait a while
        And I should see "Document 'DONOTWANT' was deleted"
        When I am at the index page
        Then I should not see "DONOTWANT"

    Scenario: Modify a document
        Given I am logged in as "UserA"
        And I have the document "CHANGEME" containing "Foo"
        And I am at the index page
        When I click "CHANGEME"
        And I wait a while
        Then I should see "Foo"
        When I change the content to "Bar"
        And I press "Save"
        Then I should see "Document 'CHANGEME' was modified"
        And I wait a while
        Then I should see "Bar" in "Content"

    Scenario: Rename a document
        Given I am logged in as "UserA"
        And I have the document "CHANGEME" containing "Foo"
        When I visit the URL for "CHANGEME"
        And I fill in "Name" with "NEWME"
        And I press "Save"
        Then I should see "Document 'CHANGEME' was renamed to 'NEWME'"
