Feature: Add an delete documents
    As a document person.
    I want to have documents in the system.

    Scenario: Add a document
        Given I am logged in as "UserA"
        And I click "Add a document"
        And I fill in "Name" with "Test document"
        And I fill in "Content" with "Test stuff"
        And I fill in "Tags" with "tag1 tag2"
        And I press "Save"
        Then I should be at the index page
        And I should see "Test document"
        When I click "Test document"
        Then I should see "Test stuff" in "Content"

    Scenario: Delete a document
        Given I am logged in as "UserA"
        And I have the document "DONOTWANT"
        And I am at the index page
        When I click "[delete]"
        Then I should be at the index page
        And I should not see "DONOTWANT"
