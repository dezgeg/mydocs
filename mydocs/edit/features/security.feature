Feature: Others should not see my non-public documents
    As a security conscious person.
    I do not want others to see my private documents.

    Scenario: Anonymous users should not see my document
        Given I am logged in as "UserA"
        And I have the document "NON-PUBLIC" containing "Secrets"
        When I log out
        And I visit the URL for "NON-PUBLIC"
        Then I should see "Permission denied"

    Scenario: Other users should not see my document
        Given I am logged in as "UserA"
        And I have the document "NON-PUBLIC" containing "Secrets"
        When I log in as "UserB"
        And I visit the URL for "NON-PUBLIC"
        Then I should see "Permission denied"

