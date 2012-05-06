Feature: Add an delete documents
    As a document person.
    I want to have documents in the system.

    Scenario: Add a document
        Given I am logged in as "UserA"
        And I click "Add a document"
        And I fill in "Name" with "Test document"
        And I fill in "Content" with "Test stuff"
        And I press "Save"
        Then I should be at the index page
        And I should see "Test document"
        When I click "Test document"
        Then I should see "Test stuff" in "Content"

    Scenario: Delete a document
        Given I am logged in as "UserA"
        And I have the document "DONOTWANT" containing "Dont care"
        And I am at the index page
        When I click "[delete]"
        Then I should not see "DONOTWANT"
        And I should be at the index page

    Scenario: Modify a document
        Given I am logged in as "UserA"
        And I have the document "CHANGEME" containing "Foo"
        And I am at the index page
        When I click "CHANGEME"
        Then I should see "Foo"
        When I fill in "Content" with "Bar"
        And I press "Save"
        And I click "CHANGEME"
        Then I should see "Bar" in "Content"
